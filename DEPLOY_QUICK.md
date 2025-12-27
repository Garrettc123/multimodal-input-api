# Quick Deployment Reference

## Quick Start

Choose your deployment method:

```bash
# Interactive deployment script
./deploy.sh

# Docker
docker build -t multimodal-input-api . && docker run -p 8000:8000 multimodal-input-api

# Docker Compose
docker-compose up -d

# Pre-built image from GitHub Container Registry
docker pull ghcr.io/garrettc123/multimodal-input-api:latest
docker run -p 8000:8000 ghcr.io/garrettc123/multimodal-input-api:latest
```

## Platform-Specific Quick Deploy

### Heroku
```bash
heroku create
git push heroku main
```

### Railway
```bash
railway init
railway up
```

### Fly.io
```bash
flyctl launch
```

### Render
- Import repository in Render dashboard
- render.yaml will be auto-detected

## Files

- `DEPLOYMENT.md` - Complete deployment guide
- `deploy.sh` - Interactive deployment helper
- `Procfile` - Heroku configuration
- `app.json` - Heroku app metadata
- `railway.json` - Railway configuration
- `render.yaml` - Render configuration
- `fly.toml` - Fly.io configuration
- `docker-compose.yml` - Development Docker Compose
- `docker-compose.prod.yml` - Production Docker Compose

## API Access

After deployment, your API will be available at:
- Documentation: `https://your-domain/docs`
- Health check: `https://your-domain/health`
- API root: `https://your-domain/`

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)
