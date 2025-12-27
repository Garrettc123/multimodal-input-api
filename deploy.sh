#!/bin/bash
# Deployment helper script for Multimodal Input API

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Multimodal Input API - Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main menu
echo "Select deployment method:"
echo "1) Docker (local)"
echo "2) Docker Compose"
echo "3) Heroku"
echo "4) Railway"
echo "5) Fly.io"
echo "6) Build Docker image only"
echo "7) Exit"
echo ""
read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        print_info "Deploying with Docker..."
        if ! command_exists docker; then
            print_error "Docker is not installed. Please install Docker first."
            exit 1
        fi
        
        print_info "Building Docker image..."
        docker build -t multimodal-input-api:latest .
        print_success "Docker image built successfully"
        
        print_info "Starting container..."
        docker run -d -p 8000:8000 --name multimodal-api multimodal-input-api:latest
        print_success "Container started successfully"
        
        echo ""
        print_success "Deployment complete!"
        echo "API is available at: http://localhost:8000"
        echo "API docs at: http://localhost:8000/docs"
        echo ""
        echo "Useful commands:"
        echo "  View logs: docker logs -f multimodal-api"
        echo "  Stop: docker stop multimodal-api"
        echo "  Remove: docker rm multimodal-api"
        ;;
    
    2)
        print_info "Deploying with Docker Compose..."
        if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
            print_error "Docker Compose is not installed. Please install Docker Compose first."
            exit 1
        fi
        
        print_info "Starting services..."
        if command_exists docker-compose; then
            docker-compose up -d
        else
            docker compose up -d
        fi
        print_success "Services started successfully"
        
        echo ""
        print_success "Deployment complete!"
        echo "API is available at: http://localhost:8000"
        echo "API docs at: http://localhost:8000/docs"
        echo ""
        echo "Useful commands:"
        echo "  View logs: docker-compose logs -f"
        echo "  Stop: docker-compose down"
        ;;
    
    3)
        print_info "Deploying to Heroku..."
        if ! command_exists heroku; then
            print_error "Heroku CLI is not installed."
            echo "Install it from: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        read -p "Enter app name (or press Enter to generate): " app_name
        
        print_info "Logging in to Heroku..."
        heroku login
        
        if [ -z "$app_name" ]; then
            print_info "Creating new Heroku app..."
            heroku create
        else
            print_info "Creating Heroku app: $app_name"
            heroku create "$app_name"
        fi
        
        print_info "Deploying to Heroku..."
        git push heroku main
        
        print_success "Deployment complete!"
        heroku open
        ;;
    
    4)
        print_info "Deploying to Railway..."
        if ! command_exists railway; then
            print_error "Railway CLI is not installed."
            echo "Install it with: npm install -g @railway/cli"
            exit 1
        fi
        
        print_info "Logging in to Railway..."
        railway login
        
        print_info "Initializing Railway project..."
        railway init
        
        print_info "Deploying to Railway..."
        railway up
        
        print_success "Deployment complete!"
        railway open
        ;;
    
    5)
        print_info "Deploying to Fly.io..."
        if ! command_exists flyctl; then
            print_error "Fly.io CLI is not installed."
            echo "Install it from: https://fly.io/docs/hands-on/install-flyctl/"
            exit 1
        fi
        
        print_info "Logging in to Fly.io..."
        flyctl auth login
        
        if [ ! -f "fly.toml" ]; then
            print_info "Launching new Fly.io app..."
            flyctl launch
        else
            print_info "Deploying to Fly.io..."
            flyctl deploy
        fi
        
        print_success "Deployment complete!"
        flyctl open
        ;;
    
    6)
        print_info "Building Docker image..."
        if ! command_exists docker; then
            print_error "Docker is not installed. Please install Docker first."
            exit 1
        fi
        
        docker build -t multimodal-input-api:latest .
        print_success "Docker image built successfully"
        
        echo ""
        echo "To run the image:"
        echo "  docker run -p 8000:8000 multimodal-input-api:latest"
        ;;
    
    7)
        echo "Exiting..."
        exit 0
        ;;
    
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac
