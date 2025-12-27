# Deployment Guide

This guide covers multiple deployment options for the Multimodal Input API.

## Table of Contents
- [Docker Deployment](#docker-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Railway Deployment](#railway-deployment)
- [Render Deployment](#render-deployment)
- [Fly.io Deployment](#flyio-deployment)
- [GitHub Container Registry](#github-container-registry)
- [Manual Deployment](#manual-deployment)

## Prerequisites

Before deploying, ensure you have:
- Git installed
- Docker installed (for container-based deployments)
- An account on your chosen platform

## Docker Deployment

### Local Docker

1. Build the image:
```bash
docker build -t multimodal-input-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e ENVIRONMENT=production multimodal-input-api
```

### Docker Compose

1. Start the application:
```bash
docker-compose up -d
```

2. Check status:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the application:
```bash
docker-compose down
```

## Heroku Deployment

### Using Heroku CLI

1. Login to Heroku:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Deploy:
```bash
git push heroku main
```

4. Open the app:
```bash
heroku open
```

### Using Heroku Button

Click the button below to deploy directly to Heroku:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Using Docker on Heroku

1. Login to Heroku Container Registry:
```bash
heroku container:login
```

2. Push the Docker image:
```bash
heroku container:push web -a your-app-name
```

3. Release the image:
```bash
heroku container:release web -a your-app-name
```

## Railway Deployment

### Using Railway CLI

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Initialize project:
```bash
railway init
```

4. Deploy:
```bash
railway up
```

### Using Railway Dashboard

1. Go to [Railway](https://railway.app/)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose this repository
5. Railway will automatically detect the Dockerfile and deploy

### Configuration

Railway will use the `railway.json` configuration file automatically.

## Render Deployment

### Using Render Dashboard

1. Go to [Render](https://render.com/)
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file and configure automatically
5. Click "Apply" to deploy

### Manual Web Service Setup

1. Click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: multimodal-input-api
   - **Environment**: Docker
   - **Plan**: Choose your plan (Free tier available)
   - **Region**: Choose closest to your users
4. Add environment variables:
   - `ENVIRONMENT=production`
   - `LOG_LEVEL=INFO`
5. Click "Create Web Service"

## Fly.io Deployment

### Prerequisites

1. Install flyctl:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login to Fly.io:
```bash
flyctl auth login
```

### Deploy

1. Launch the app (first time):
```bash
flyctl launch
```

Follow the prompts. The `fly.toml` file will be used for configuration.

2. Deploy updates:
```bash
flyctl deploy
```

3. Open the app:
```bash
flyctl open
```

### Monitoring

Check status:
```bash
flyctl status
```

View logs:
```bash
flyctl logs
```

Scale the app:
```bash
flyctl scale count 2
```

## GitHub Container Registry

The API is automatically published to GitHub Container Registry (ghcr.io) when code is merged to main.

### Pull and Run

```bash
docker pull ghcr.io/garrettc123/multimodal-input-api:latest
docker run -p 8000:8000 ghcr.io/garrettc123/multimodal-input-api:latest
```

### Using in Docker Compose

```yaml
version: '3.8'

services:
  api:
    image: ghcr.io/garrettc123/multimodal-input-api:latest
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
```

## Manual Deployment

### On a VPS or Cloud VM

1. Clone the repository:
```bash
git clone https://github.com/Garrettc123/multimodal-input-api.git
cd multimodal-input-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run with uvicorn:
```bash
uvicorn multimodal_input_api:app --host 0.0.0.0 --port 8000
```

### Using a Process Manager (systemd)

Create a systemd service file at `/etc/systemd/system/multimodal-api.service`:

```ini
[Unit]
Description=Multimodal Input API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/multimodal-input-api
Environment="PATH=/opt/multimodal-input-api/venv/bin"
ExecStart=/opt/multimodal-input-api/venv/bin/uvicorn multimodal_input_api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable multimodal-api
sudo systemctl start multimodal-api
sudo systemctl status multimodal-api
```

## Environment Variables

Configure these environment variables for your deployment:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Application environment | `production` |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `PORT` | Port to run the server on | `8000` |

## Health Checks

All deployments should configure health checks using the `/health` endpoint:

- **Path**: `/health`
- **Method**: GET
- **Expected Status**: 200
- **Interval**: 30 seconds
- **Timeout**: 5 seconds

## SSL/HTTPS

For production deployments:

- **Heroku**: Automatic SSL for all apps
- **Railway**: Automatic SSL for all services
- **Render**: Automatic SSL for all services
- **Fly.io**: Automatic SSL with Let's Encrypt
- **Manual**: Use a reverse proxy (nginx/Caddy) with Let's Encrypt

### Example nginx configuration:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring and Logging

### Logging

The application logs to stdout/stderr. Configure your platform's logging:

- **Heroku**: `heroku logs --tail`
- **Railway**: View logs in dashboard
- **Render**: View logs in dashboard
- **Fly.io**: `flyctl logs`
- **Docker**: `docker logs -f <container-id>`

### Monitoring

Consider integrating monitoring services:
- **Sentry** for error tracking
- **Prometheus** for metrics
- **Grafana** for visualization
- **UptimeRobot** for uptime monitoring

## Scaling

### Horizontal Scaling

**Heroku**:
```bash
heroku ps:scale web=3
```

**Fly.io**:
```bash
flyctl scale count 3
```

**Railway/Render**: Scale through dashboard

### Vertical Scaling

Upgrade your plan or instance size through each platform's dashboard.

## Troubleshooting

### Common Issues

1. **Port binding errors**: Ensure your app uses `$PORT` environment variable
2. **Dependencies not found**: Verify `requirements.txt` is complete
3. **Docker build fails**: Check Dockerfile and build logs
4. **Health check fails**: Verify `/health` endpoint is accessible

### Getting Help

- Check platform-specific documentation
- Review application logs
- Test locally with Docker first
- Ensure all environment variables are set

## CI/CD

The repository includes GitHub Actions workflows for automated deployment:

- **CI Pipeline**: Runs tests and builds on every push
- **Deployment Pipeline**: Publishes Docker images on releases

See `.github/workflows/` for configuration details.

## Security Considerations

1. Never commit secrets to the repository
2. Use environment variables for sensitive configuration
3. Keep dependencies updated
4. Enable HTTPS in production
5. Configure CORS appropriately
6. Use authentication if needed
7. Monitor for security vulnerabilities

## Cost Estimation

### Free Tiers Available

- **Heroku**: Free dyno (sleeps after 30 min inactivity)
- **Railway**: $5 credit per month
- **Render**: Free tier with limitations
- **Fly.io**: Free allowance (3 VMs with 256MB RAM)

### Paid Plans Start At

- **Heroku**: $7/month (Eco dyno)
- **Railway**: $5/month per service
- **Render**: $7/month (Starter)
- **Fly.io**: Pay-as-you-go

## Next Steps

After deployment:

1. Test the `/health` endpoint
2. Access the API documentation at `/docs`
3. Set up monitoring
4. Configure a custom domain
5. Set up CI/CD for automatic deployments
6. Implement rate limiting if needed

## Support

For issues related to:
- **Application code**: Open an issue on GitHub
- **Deployment platforms**: Contact platform support
- **Docker**: Check Docker documentation

---

**Last Updated**: December 2025
**Version**: 1.0.0
