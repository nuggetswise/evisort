# 🚀 Deployment Guide

This guide covers how to deploy the Workday PM Role Demo app on different platforms.

## 📋 Prerequisites

- Python 3.8+
- Git
- Required API keys (optional, app works in demo mode)

## 🏠 Local Development

### Quick Start
```bash
# Clone the repository
git clone <your-repo-url>
cd workday-pm-demo

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Prepare Repository
1. Push your code to GitHub
2. Ensure `requirements.txt` is in the root directory
3. Verify `app.py` is the main entry point

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path to `app.py`
6. Click "Deploy"

### Step 3: Configure Secrets (Optional)
If you have API keys, add them in Streamlit Cloud:
1. Go to your app settings
2. Click "Secrets"
3. Add your API keys:
```toml
openai_api_key = "your-openai-key"
gemini_api_key = "your-gemini-key"
cohere_api_key = "your-cohere-key"
```

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

### Build and Run
```bash
# Build the image
docker build -t workday-pm-demo .

# Run the container
docker run -p 8501:8501 workday-pm-demo
```

### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - ./.streamlit:/app/.streamlit
```

Run with:
```bash
docker-compose up -d
```

## 🌐 Heroku Deployment

### Step 1: Create Heroku App
```bash
# Install Heroku CLI
# Create app
heroku create your-app-name

# Add Python buildpack
heroku buildpacks:set heroku/python
```

### Step 2: Create Procfile
Create `Procfile` in root directory:
```
web: streamlit run app.py --server.port=$PORT --server.headless=true
```

### Step 3: Deploy
```bash
# Add files to git
git add .
git commit -m "Deploy to Heroku"

# Deploy
git push heroku main
```

## 🔧 Environment Variables

### Required Variables
- None (app works in demo mode)

### Optional Variables
- `OPENAI_API_KEY`: OpenAI API key for enhanced AI responses
- `GEMINI_API_KEY`: Google Gemini API key
- `COHERE_API_KEY`: Cohere API key

### Setting Environment Variables

**Local:**
```bash
export OPENAI_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
export COHERE_API_KEY="your-key"
```

**Streamlit Cloud:**
Use the secrets management interface

**Docker:**
```bash
docker run -e OPENAI_API_KEY="your-key" -p 8501:8501 workday-pm-demo
```

**Heroku:**
```bash
heroku config:set OPENAI_API_KEY="your-key"
```

## 📊 Monitoring and Logs

### Streamlit Cloud
- Logs are available in the app dashboard
- Monitor usage in the Streamlit Cloud console

### Docker
```bash
# View logs
docker logs <container-id>

# Follow logs
docker logs -f <container-id>
```

### Heroku
```bash
# View logs
heroku logs --tail
```

## 🔒 Security Considerations

### API Keys
- Never commit API keys to version control
- Use environment variables or secrets management
- Rotate keys regularly

### CORS
- The app is configured for local development
- For production, configure CORS appropriately

### Rate Limiting
- Consider implementing rate limiting for API calls
- Monitor usage to avoid hitting API limits

## 🚨 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

**Port Already in Use:**
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port 8502
```

**API Key Issues:**
- Verify API keys are correctly set
- Check API key permissions
- Ensure sufficient credits/quota

**Docker Issues:**
```bash
# Clean up containers
docker system prune -a

# Rebuild image
docker build --no-cache -t workday-pm-demo .
```

### Getting Help
1. Check the logs for error messages
2. Verify all dependencies are installed
3. Test locally before deploying
4. Check API key configuration

## 📈 Performance Optimization

### For Production
1. **Caching**: Use Streamlit caching for expensive operations
2. **API Limits**: Implement rate limiting and retry logic
3. **Resource Limits**: Monitor memory and CPU usage
4. **CDN**: Use CDN for static assets if needed

### Monitoring
- Set up application monitoring
- Track API usage and costs
- Monitor user engagement metrics

---

**Note**: This app is designed for demonstration purposes. For production use, implement appropriate security measures and monitoring. 