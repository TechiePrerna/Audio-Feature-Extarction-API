# Docker Deployment Guide for Hostinger VPS

## Prerequisites
Before deploying, ensure your Hostinger VPS has:
- Docker installed
- Docker Compose installed
- SSH access to your VPS
- At least 2GB RAM and 10GB storage

## Installation on Hostinger VPS

### 1. Install Docker and Docker Compose

```bash
# SSH into your VPS
ssh root@your_vps_ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version
```

### 2. Deploy Your Application

```bash
# Clone or upload your project to the VPS
git clone <your-repo-url> /home/voice-engine
cd /home/voice-engine

# Copy .env.example to .env and configure
cp .env.example .env
nano .env  # Edit with your API key and configuration
```

### 3. Build and Run with Docker Compose

```bash
# Build the Docker image
docker-compose build

# Start the container in background
docker-compose up -d

# Check if running
docker-compose ps

# View logs
docker-compose logs -f voice-engine
```

## Managing the Container

### Useful Commands

```bash
# Stop the container
docker-compose down

# Restart the container
docker-compose restart

# View real-time logs
docker-compose logs -f

# Execute command inside container
docker-compose exec voice-engine bash

# Rebuild after code changes
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Reverse Proxy Setup (Nginx)

For production, use Nginx as a reverse proxy:

```bash
# Install Nginx
apt install nginx -y

# Create Nginx config (edit /etc/nginx/sites-available/voice-engine)
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable the site
ln -s /etc/nginx/sites-available/voice-engine /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Create certificate
certbot certonly --nginx -d your_domain.com

# Update Nginx config to use SSL
```

## Monitoring

```bash
# Check container health
docker-compose ps

# Monitor resource usage
docker stats

# Check logs for errors
docker-compose logs --tail=100
```

## Backup and Persistence

Your volumes (`data/`, `output/`, `logs/`, `models/`) are persistent and stored on the host:

```bash
# Backup your data
tar -czf backup-$(date +%Y%m%d).tar.gz data/ output/ logs/ models/

# Restore from backup
tar -xzf backup-20240407.tar.gz
```

## Troubleshooting

### Container exits immediately
```bash
docker-compose logs voice-engine  # Check error logs
```

### Port already in use
```bash
# Change port in docker-compose.yml
# ports:
#   - "8080:8000"  # External:Internal
```

### Out of disk space
```bash
# Clean up Docker
docker system prune -a

# Check disk usage
df -h
```

## Environment Variables

Ensure `.env` file contains:
```
API_KEY=your_secure_api_key
```

## Support

For Docker Manager on Hostinger, use their web interface to:
- Monitor container logs
- Restart services
- Manage volumes
- Update configurations
