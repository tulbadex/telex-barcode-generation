# Telex Integration Setup Guide

## Step 1: Get Telex Access
```bash
/telex-invite tulbadex@gmail.com
```

## Step 2: Deploy Your Agent

### Option A: Local Development
```bash
pip install -r requirements.txt
python -m src.main
```

### Option B: Docker Deployment
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option C: Cloud Deployment (Railway/Heroku)
1. Push code to GitHub
2. Connect to Railway/Heroku
3. Set environment variables
4. Deploy

## Step 3: Create Agent in Telex

1. **Go to AI Coworkers** → Add New
2. **Fill Agent Details:**
   - Name: `QR & Barcode Generator`
   - Title: `Code Generator Assistant`
   - Job Description: `Generates QR codes and barcodes for any text, URLs, or data`
   - Tone: `Friendly`
   - Visibility: `Public`

## Step 4: Configure Agent

### Add Skills Tab:
- Search for "API" or "Custom" skills
- Add external API integration skill
- Configure endpoint: `https://your-url.com/a2a/agent/qrBarcodeAgent`

### Add Prompts Tab:
```
Personality Prompt:
"You are a helpful QR code and barcode generator. You create visual codes for any text, URLs, or data users provide. Always be friendly and provide clear instructions."

Tagged Prompts:
#qr: "I can generate QR codes! Just type 'qr [your text]' and I'll create one for you."
#barcode: "Need a barcode? Type 'barcode [your text]' and specify format if needed."
#help: "Commands: 'qr [text]', 'barcode [text]', 'qr size:15 [text]', 'barcode format:ean13 [text]'"
```

### Task List Tab:
```
1. "Generate QR codes for any text or URL provided by users"
2. "Create barcodes in multiple formats (CODE128, EAN13, EAN8, UPC)"
3. "Provide daily QR code tips and usage suggestions"
4. "Help users understand different barcode formats and their uses"
```

## Step 5: Test Integration

### Test Commands in Telex:
```
qr https://example.com
barcode 1234567890
qr size:20 Hello World
barcode format:ean13 123456789012
help
```

## Step 6: Monitor Logs

Check agent logs at:
```
https://api.telex.im/agent-logs/{your-channel-id}.txt
```

## Troubleshooting

### Agent Not Responding:
1. Check if your endpoint is accessible
2. Verify A2A endpoint returns proper JSON
3. Check Telex agent configuration

### Test A2A Endpoint:
```bash
curl -X POST "https://your-url.com/a2a/agent/qrBarcodeAgent" \
  -H "Content-Type: application/json" \
  -d '{"message": "qr test message"}'
```

Expected Response:
```json
{
  "text": "QR code generated for: test message",
  "type": "image",
  "image": "data:image/png;base64,..."
}
```