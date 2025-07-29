const fs = require('fs');

// Read the base64 logo
const logoBase64 = fs.readFileSync('../logo_base64.txt', 'utf8').trim();

// Read the functions file
let functionsContent = fs.readFileSync('index.js', 'utf8');

// Create the new header with logo
const newHeader = `            <!-- Header with Logo -->
            <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #1A237E;">
              <img src="data:image/png;base64,${logoBase64}" alt="Real InvestCo Logo" style="max-width: 200px; height: auto; margin-bottom: 15px;">
              <h1 style="color: #1A237E; margin: 10px 0 0 0; font-size: 24px;">Real InvestCo</h1>
              <p style="color: #666; margin: 5px 0 0 0; font-size: 16px;">Your trusted partner in real estate investment</p>
            </div>`;

// Replace the header section in the SMTP function (around line 674)
const oldHeader = `            <!-- Header with Logo -->
            <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #1A237E;">
              <h1 style="color: #1A237E; margin: 10px 0 0 0; font-size: 24px;">Real InvestCo</h1>
              <p style="color: #666; margin: 5px 0 0 0; font-size: 16px;">Your trusted partner in real estate investment</p>
            </div>`;

functionsContent = functionsContent.replace(oldHeader, newHeader);

// Write the updated content back
fs.writeFileSync('index.js', functionsContent);

console.log('Email template updated with logo!'); 