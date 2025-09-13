#!/bin/bash

# Lucky.io Deployment Script
echo "🚀 Deploying Lucky.io..."

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is not installed. Please install pnpm first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pnpm install

# Build the application
echo "🔨 Building application..."
pnpm build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Ask user for deployment method
    echo "Choose deployment method:"
    echo "1) Start local production server"
    echo "2) Deploy to Vercel"
    echo "3) Deploy with Docker"
    echo "4) Exit"
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            echo "🌐 Starting production server on http://localhost:3000"
            pnpm start
            ;;
        2)
            echo "🚀 Deploying to Vercel..."
            if command -v vercel &> /dev/null; then
                vercel --prod
            else
                echo "❌ Vercel CLI not installed. Install with: pnpm add -g vercel"
            fi
            ;;
        3)
            echo "🐳 Building Docker image..."
            docker build -t lucky-io .
            echo "🚀 Running Docker container..."
            docker run -p 3000:3000 lucky-io
            ;;
        4)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
else
    echo "❌ Build failed!"
    exit 1
fi
