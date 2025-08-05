# Vercel Deployment Guide for AI Itinerary Planner

## 📋 Pre-Deployment Checklist

✅ Created `vercel.json` configuration
✅ Created `api/index.py` serverless entry point
✅ Created `.vercelignore` to exclude unnecessary files
✅ `requirements.txt` exists with all dependencies

## 🚀 Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy from your project directory
```bash
cd "c:\Users\223081238.HCAD\OneDrive - GEHealthCare\Desktop\itenery_app"
vercel
```

### 4. Set Environment Variables in Vercel Dashboard
After deployment, go to your Vercel project dashboard and add:

- `FLASK_SECRET_KEY`: `your-secret-key-here`
- `GEMINI_API_KEY`: `AIzaSyALVGrgZqTECJZFwPDApEISygwIUEbxjuE`

### 5. Redeploy to apply environment variables
```bash
vercel --prod
```

## 🔧 What Was Fixed

1. **Serverless Architecture**: Created `api/index.py` as the entry point for Vercel's serverless functions
2. **Routing Configuration**: Added `vercel.json` to route all requests to the Flask app
3. **Path Resolution**: Fixed import paths to work in Vercel's environment
4. **Static Files**: Configured proper paths for templates and static files

## 🌐 After Deployment

Your app will be available at: `https://your-project-name.vercel.app`

## 🐛 Troubleshooting

If you still get 404 errors:
1. Check that all environment variables are set in Vercel dashboard
2. Ensure the deployment completed successfully
3. Check Vercel function logs for any import errors
4. Verify that all required files are included (not in .vercelignore)

## 📁 Project Structure for Vercel

```
your-app/
├── api/
│   └── index.py          # Serverless entry point
├── services/             # Your backend services
├── models/              # Data models
├── templates/           # HTML templates
├── static/             # CSS, JS, images
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
└── .vercelignore      # Files to exclude
```
