# GitHub Actions Setup

This repository includes a GitHub Actions workflow that automatically builds and pushes Docker images to Docker Hub.

## Required Secrets

To use this workflow, you need to set up the following secrets in your GitHub repository:

### Docker Hub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following repository secrets:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token (not password!)

### Creating a Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security**
3. Click **New Access Token**
4. Give it a descriptive name (e.g., "GitHub Actions - ffexec")
5. Copy the generated token and add it as `DOCKERHUB_TOKEN` secret

## Workflow Features

- ✅ **Multi-platform builds**: Builds for both `linux/amd64` and `linux/arm64`
- ✅ **Automatic tagging**: Tags images based on branch/tag names
- ✅ **PR testing**: Tests Docker images on pull requests without pushing
- ✅ **Caching**: Uses GitHub Actions cache for faster builds
- ✅ **Health check**: Verifies the container starts and responds

## Triggered Events

- **Push to main**: Builds and pushes `latest` tag
- **Git tags**: Builds and pushes version tags (e.g., `v1.0.0` → `1.0.0`, `1.0`, `1`)
- **Pull requests**: Builds and tests but doesn't push

## Docker Hub Repository

After setup, your images will be available at:
```
docker.io/YOUR_USERNAME/ffexec-api:latest
docker.io/YOUR_USERNAME/ffexec-api:v1.0.0
```

## Usage

Pull and run your image:
```bash
docker pull YOUR_USERNAME/ffexec-api:latest
docker run -p 8000:8000 YOUR_USERNAME/ffexec-api:latest
```