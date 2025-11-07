const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  
  if (req.method === 'GET') {
    try {
      // Read the agent.json file
      const agentJsonPath = path.join(process.cwd(), '.well-known', 'agent.json');
      const agentJson = fs.readFileSync(agentJsonPath, 'utf8');
      const agentData = JSON.parse(agentJson);
      
      return res.status(200).json(agentData);
    } catch (error) {
      return res.status(500).json({ 
        error: 'Failed to load agent configuration',
        details: error.message 
      });
    }
  }
  
  return res.status(405).json({ error: 'Method not allowed' });
};