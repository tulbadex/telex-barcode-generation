const QRCode = require('qrcode');

module.exports = (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  
  try {
    if (req.method === 'GET') {
      if (req.url === '/' || req.url === '') {
        return res.status(200).json({
          message: "QR & Barcode Generator Agent",
          status: "active",
          version: "1.0.0"
        });
      }
      
      if (req.url === '/health') {
        return res.status(200).json({
          status: "healthy",
          timestamp: new Date().toISOString()
        });
      }
    }
    
    if (req.method === 'POST') {
      let body = '';
      
      req.on('data', chunk => {
        body += chunk.toString();
      });
      
      req.on('end', async () => {
        try {
          const data = JSON.parse(body || '{}');
          const message = data.text || data.message || '';
          
          if (message.toLowerCase().startsWith('qr ')) {
            const text = message.substring(3).trim();
            if (!text) {
              return res.status(200).json({
                text: "Please provide text to generate QR code. Example: qr Hello World",
                type: "text"
              });
            }
            
            try {
              const qrDataURL = await QRCode.toDataURL(text, {
                width: 300,
                margin: 2
              });
              
              return res.status(200).json({
                text: `QR code generated for: ${text}`,
                type: "image",
                image: qrDataURL
              });
            } catch (qrError) {
              return res.status(200).json({
                text: `QR generation failed: ${qrError.message}`,
                type: "text"
              });
            }
          }
          
          return res.status(200).json({
            text: "QR & Barcode Generator Agent\n\nCommands:\n• qr [text] - Generate QR code\n• barcode [text] - Generate barcode",
            type: "text"
          });
          
        } catch (parseError) {
          return res.status(200).json({
            text: "Invalid request format. Send JSON with 'text' field.",
            type: "text"
          });
        }
      });
      
      return; // Don't send response here, wait for 'end' event
    }
    
    return res.status(404).json({ error: "Not found" });
    
  } catch (error) {
    return res.status(500).json({
      text: `Server error: ${error.message}`,
      type: "text"
    });
  }
};