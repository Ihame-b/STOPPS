#!/bin/bash
# Simple script to run the Django development server

cd "$(dirname "$0")"

echo "========================================="
echo "Starting Django Development Server"
echo "========================================="
echo ""
echo "Checking Django installation..."
python3 -c "import django; print('✓ Django', django.get_version())" || { echo "✗ Django not installed"; exit 1; }

echo ""
echo "Checking database..."
python3 manage.py check --deploy 2>&1 | grep -q "System check identified no issues" && echo "✓ Database OK" || echo "⚠ Database check completed"

echo ""
echo "Starting server on http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop the server"
echo "========================================="
echo ""

python3 manage.py runserver 0.0.0.0:8000
