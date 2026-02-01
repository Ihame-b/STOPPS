#!/bin/bash
# Script to push with Personal Access Token

echo "=========================================="
echo "GitHub Push with Personal Access Token"
echo "=========================================="
echo ""
echo "This script will help you push using your Personal Access Token."
echo ""
read -p "Enter your GitHub Personal Access Token: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "Error: Token cannot be empty!"
    exit 1
fi

# Update remote URL with token
git remote set-url origin https://${TOKEN}@github.com/Ihame-b/STOPPS.git

echo ""
echo "Pushing to GitHub..."
git push -u origin main

# After push, remove token from URL for security
git remote set-url origin https://Ihame-b@github.com/Ihame-b/STOPPS.git

echo ""
echo "Done! Token has been removed from remote URL for security."
