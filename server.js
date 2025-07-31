const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Get the absolute path to the client directory
const clientDir = 'D:\\Real InvestCo\\Websites\\RealInvestCo2025\\client';

// Serve static files from the client directory
app.use(express.static(clientDir));

// Specific route for index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(clientDir, 'index.html'));
});

// Specific route for property.html
app.get('/property.html', (req, res) => {
    res.sendFile(path.join(clientDir, 'property.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    console.log(`Serving files from: ${clientDir}`);
});