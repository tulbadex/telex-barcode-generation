module.exports = (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  
  if (req.method === 'GET') {
    if (req.url === '/' || req.url === '') {
      return res.status(200).json({
        message: "QR & Barcode Generator Agent",
        status: "active"
      });
    }
    
    if (req.url === '/health') {
      return res.status(200).json({
        status: "healthy"
      });
    }
    
    if (req.url === '/.well-known/agent.json') {
      return res.status(200).json({
        name: "QR & Barcode Generator",
        version: "1.0.0",
        skills: [
          { name: "generate_qr", description: "Generate QR codes" },
          { name: "generate_barcode", description: "Generate barcodes" }
        ]
      });
    }
  }
  
  if (req.method === 'POST') {
    return res.status(200).json({
      jsonrpc: "2.0",
      id: 1,
      result: "Method not implemented yet"
    });
  }
  
  return res.status(404).json({ error: "Not found" });
};