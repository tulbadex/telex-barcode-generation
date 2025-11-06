#!/bin/bash

echo "🚀 Deploying QR Barcode Agent..."

# Build and run with Docker
docker build -t qr-barcode-agent .
docker run -d -p 8000:8000 --name qr-agent qr-barcode-agent

echo "✅ Agent deployed at http://localhost:8000"
echo "📋 A2A Endpoint: http://localhost:8000/a2a/agent/qrBarcodeAgent"
echo "🔍 Health Check: http://localhost:8000/api/v1/health"

# Test the deployment
sleep 5
curl -f http://localhost:8000/api/v1/health || echo "❌ Health check failed"