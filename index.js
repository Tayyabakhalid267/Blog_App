const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// In-memory storage for messages
let messages = [];

// API Routes
app.get('/api/messages', (req, res) => {
  res.json(messages);
});

app.post('/api/messages', (req, res) => {
  const { author, content } = req.body;
  
  if (!author || !content) {
    return res.status(400).json({ error: 'Author and content are required' });
  }
  
  const message = {
    id: Date.now(),
    author,
    content,
    timestamp: new Date().toISOString()
  };
  
  messages.push(message);
  res.status(201).json(message);
});

app.delete('/api/messages/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = messages.findIndex(m => m.id === id);
  
  if (index === -1) {
    return res.status(404).json({ error: 'Message not found' });
  }
  
  messages.splice(index, 1);
  res.status(204).send();
});

// Serve the HTML page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(port, () => {
  console.log(`Message board server running at http://localhost:${port}`);
});

module.exports = app;
