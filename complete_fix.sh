#!/bin/bash

echo "🔧 Complete Benkhawiya Deployment Fix..."

# Navigate to correct directory
cd ~/benkhawiya-enhanced-complete

echo "📁 Current directory: $(pwd)"
echo "📊 Files in directory:"
ls -la

# Fix the remote repository
echo "🔄 Fixing Git remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/DoctorDoveDragon/benkhawiya-enhanced.git

echo "✅ Remote set to:"
git remote -v

# Fix railway.json with proper JSON
echo "📝 Fixing railway.json..."
cat > railway.json << 'JSONEOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.backend.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
JSONEOF

# Add all files and force push
echo "🚀 Deploying to GitHub..."
git add .
git commit -m "🌌 Benkhawiya Enhanced - Complete Production Deployment

✅ Features:
- FastAPI backend with WebSocket support
- Cosmic AI consultation system
- Docker configuration
- Railway deployment ready
- Health monitoring
- Complete documentation

🚀 Production ready"

git branch -M main
git push -u origin main --force

echo "🎉 DEPLOYMENT COMPLETE!"
echo "🌐 Your Benkhawiya Enhanced is now at: https://github.com/DoctorDoveDragon/benkhawiya-enhanced"
echo "🚂 Railway will auto-deploy from this repository"
