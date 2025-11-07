module.exports = (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  
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
    return res.status(200).json({
      text: "QR & Barcode Generator Agent is running",
      type: "text"
    });
  }
  
  return res.status(404).json({ error: "Not found" });
};