# Lucky.io Deployment Guide

This guide covers multiple deployment options for the Lucky.io Next.js application.

## 🚀 Quick Deploy Options

### 1. Vercel (Recommended for Next.js)

**One-click deploy:**
```bash
# Install Vercel CLI
pnpm add -g vercel

# Deploy to Vercel
pnpm deploy:vercel
```

**Or connect your GitHub repository to Vercel:**
1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Vercel will automatically detect Next.js and deploy

### 2. Netlify

```bash
# Install Netlify CLI
pnpm add -g netlify-cli

# Deploy to Netlify
pnpm deploy:netlify
```

### 3. Docker Deployment

**Local Docker:**
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t lucky-io .
docker run -p 3000:3000 lucky-io
```

**Docker Hub:**
```bash
# Tag and push to Docker Hub
docker tag lucky-io yourusername/lucky-io:latest
docker push yourusername/lucky-io:latest
```

### 4. Railway

1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Next.js app
3. Deploy with one click

### 5. Render

1. Connect your GitHub repository to Render
2. Select "Web Service"
3. Build Command: `pnpm install && pnpm build`
4. Start Command: `pnpm start`

## 🔧 Manual Deployment

### Prerequisites
- Node.js 18+
- pnpm

### Steps
```bash
# Install dependencies
pnpm install

# Build for production
pnpm build

# Start production server
pnpm start
```

## 🌐 Environment Variables

Create a `.env.local` file for local development:
```env
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://rpc1.proov.network
```

## 📊 Performance Optimization

The application is already optimized with:
- ✅ Next.js 14 with App Router
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for optimized styles
- ✅ Static generation where possible
- ✅ Image optimization
- ✅ Code splitting

## 🔒 Security Considerations

- All API calls are client-side (CORS may apply)
- No sensitive data stored locally
- HTTPS recommended for production

## 📈 Monitoring

Consider adding monitoring services:
- Vercel Analytics
- Sentry for error tracking
- Google Analytics

## 🚨 Troubleshooting

### Build Issues
```bash
# Clear cache and rebuild
rm -rf .next
pnpm build
```

### Port Issues
```bash
# Use different port
PORT=3001 pnpm start
```

### Memory Issues
```bash
# Increase Node.js memory
NODE_OPTIONS="--max-old-space-size=4096" pnpm build
```

## 📝 Deployment Checklist

- [ ] All tests pass
- [ ] Build completes successfully
- [ ] Environment variables configured
- [ ] Domain/SSL configured
- [ ] Monitoring set up
- [ ] Performance tested
- [ ] Mobile responsive tested

## 🎯 Recommended Deployment

For the best experience, we recommend **Vercel** because:
- Native Next.js support
- Automatic deployments
- Global CDN
- Built-in analytics
- Zero configuration
- Free tier available
