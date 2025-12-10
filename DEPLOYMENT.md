# Deployment Guide

This guide covers deploying the GoogleAds Dashboard to production.

## Architecture

- **Frontend**: Next.js 14 on Vercel
- **Backend**: FastAPI (Python) on Render
- **CI/CD**: GitHub Actions

---

## Quick Start

### 1. Push to Repository
```bash
git remote add toastdai https://github.com/toastdai/googleadsdashboard.git
git push toastdai main
```

---

## Frontend (Vercel)

### Setup Steps

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import `toastdai/googleadsdashboard`
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework**: Next.js (auto-detected)

### Environment Variables

Add these in Vercel Dashboard > Project Settings > Environment Variables:

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend URL (e.g., `https://your-app.onrender.com/api`) |
| `NEXT_PUBLIC_APP_NAME` | `TellSpike` |
| `NEXT_PUBLIC_APP_ENV` | `production` |
| `KELKOO_API_TOKEN` | Kelkoo API bearer token |
| `ADMEDIA_AID` | Admedia publisher ID |
| `ADMEDIA_API_KEY` | Admedia API key |
| `MAXBOUNTY_EMAIL` | MaxBounty account email |
| `MAXBOUNTY_PASSWORD` | MaxBounty account password |

### CI/CD Secrets (GitHub)

Add these secrets to GitHub repo settings:

| Secret | Description |
|--------|-------------|
| `VERCEL_TOKEN` | Vercel API token ([create here](https://vercel.com/account/tokens)) |
| `VERCEL_ORG_ID` | From `.vercel/project.json` after first deploy |
| `VERCEL_PROJECT_ID` | From `.vercel/project.json` after first deploy |

---

## Backend (Render)

### Setup Steps

1. Go to [render.com/new](https://render.com/new)
2. Select **Web Service**
3. Connect `toastdai/googleadsdashboard`
4. Configure:
   - **Root Directory**: `backend`
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT secret (auto-generated) |
| `GOOGLE_ADS_DEVELOPER_TOKEN` | Google Ads API token |
| `GOOGLE_ADS_CLIENT_ID` | OAuth client ID |
| `GOOGLE_ADS_CLIENT_SECRET` | OAuth client secret |
| `GOOGLE_ADS_REFRESH_TOKEN` | OAuth refresh token |
| `REDIS_URL` | Redis connection (optional) |
| `ENVIRONMENT` | `production` |

### CI/CD Secret (GitHub)

| Secret | Description |
|--------|-------------|
| `RENDER_DEPLOY_HOOK_URL` | Render deploy hook URL (from Render dashboard) |

---

## Post-Deployment

### 1. Update Frontend API URL
After Render deploys, copy the backend URL and update `NEXT_PUBLIC_API_URL` in Vercel.

### 2. Verify Endpoints
- Frontend: `https://your-app.vercel.app/dashboard`
- Backend: `https://your-app.onrender.com/docs`
- API Routes:
  - `/api/kelkoo`
  - `/api/admedia`
  - `/api/maxbounty`

### 3. Custom Domain (Optional)
- Vercel: Project Settings > Domains
- Render: Service Settings > Custom Domains

---

## Troubleshooting

### Build Fails on Vercel
- Check Node.js version (should be 20.x)
- Verify all environment variables are set
- Check build logs for missing dependencies

### Backend Not Responding
- Check Render logs for startup errors
- Verify Dockerfile is correct
- Ensure health check endpoint exists

### API Routes Return 500
- Check environment variables are set correctly
- Verify API tokens are valid
- Check server logs for specific errors
