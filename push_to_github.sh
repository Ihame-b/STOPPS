#!/bin/bash

# Push to GitHub with token
# Usage: ./push_to_github.sh YOUR_GITHUB_TOKEN

if [ -z "$1" ]; then
    echo "❌ Error: GitHub token required"
    echo ""
    echo "Usage: ./push_to_github.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "To get your token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Generate new token (classic) with 'repo' scope"
    echo "3. Copy the token and use it in the command above"
    exit 1
fi

TOKEN=$1
echo "🚀 Pushing to GitHub..."
git push https://${TOKEN}@github.com/Ihame-b/STOPPS.git main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ Push failed. Please check your token and try again."
    exit 1
fi
