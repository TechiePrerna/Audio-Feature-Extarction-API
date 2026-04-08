import librosa
import soundfile as sf
from pathlib import Path
from .config import TARGET_SR


def resample_audio(input_path, output_path, target_sr=TARGET_SR):
    input_path = Path(input_path)
    output_path = Path(output_path)

    try:
        audio, sr = librosa.load(str(input_path), sr=None, mono=True)
    except Exception:
        # fallback when soundfile backend is broken / missing class attr (SoundFileRuntimeError)
        import wave
        import numpy as np

        with wave.open(str(input_path), 'rb') as wf:
            sr = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            frames = wf.readframes(wf.getnframes())

        # decode 16-bit PCM (common wav format)
        if sampwidth == 2:
            dtype = np.int16
            audio = np.frombuffer(frames, dtype=dtype).astype(np.float32)
        elif sampwidth == 4:
            dtype = np.int32
            audio = np.frombuffer(frames, dtype=dtype).astype(np.float32)
        else:
            raise RuntimeError(f"Unsupported sample width: {sampwidth}")

        if channels > 1:
            audio = audio.reshape(-1, channels).mean(axis=1)

        # normalize to [-1, 1]
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak
        else:
            audio = audio

    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)

    try:
        sf.write(str(output_path), audio, target_sr)
    except Exception:
        # fallback to stdlib wave writer if libsndfile is broken
        import wave
        import numpy as np

        audio_float = audio.astype(np.float32)
        max_val = np.max(np.abs(audio_float))
        if max_val == 0:
            audio_int16 = np.zeros_like(audio_float, dtype=np.int16)
        else:
            audio_int16 = np.int16(audio_float / max_val * 32767)

        with wave.open(str(output_path), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(target_sr)
            wf.writeframes(audio_int16.tobytes())

    return output_path, target_sr
