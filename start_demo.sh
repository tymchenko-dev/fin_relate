#!/bin/bash

echo "🚀 Starting Expense Tracker Demo..."
echo "=================================="

 # Change to project directory
cd /Users/jameskenway/Downloads/Tim/Portfolio/expense_tracker

# Check ngrok
if [ ! -f "./ngrok" ]; then
    echo "❌ ngrok not found!"
    echo "Downloading ngrok..."
    curl -o ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip
    unzip ngrok.zip
    chmod +x ngrok
    rm ngrok.zip
    echo "✅ ngrok installed"
fi

# Check ngrok token
if ! ./ngrok config check &> /dev/null; then
    echo "⚠️  Setting up ngrok token..."
    ./ngrok config add-authtoken 30xhECVbBbkelpzn0g15Sa6c9Fj_d8f3CUXx3iUxnXxRxyJJ
    echo "✅ Token configured"
fi

# Start the application in the background
echo "🔄 Starting Flask application..."
python3 run.py &
FLASK_PID=$!

# Wait for the application to start
sleep 3

# Check if the application started
if curl -s http://localhost:5002 > /dev/null; then
    echo "✅ Application started at http://localhost:5002"
else
    echo "❌ Error starting application"
    kill $FLASK_PID 2>/dev/null
    exit 1
fi

# Start ngrok
echo "🌐 Creating public link..."
echo ""
echo "🎯 ATTENTION: ngrok will now open with a public link"
echo "📋 Copy the link like https://XXXXX.ngrok-free.app"
echo "📱 Send it to your friend along with login: demo_user / demo123"
echo ""
echo "⏹️  To stop: press Ctrl+C"
echo "=================================="

# Start ngrok (blocking)
./ngrok http 5002

# Cleanup on exit
echo "🛑 Stopping application..."
kill $FLASK_PID 2>/dev/null
echo "✅ Done!"
