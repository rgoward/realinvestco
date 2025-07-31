const fs = require('fs');

// Read the functions file
let functionsContent = fs.readFileSync('functions/index.js', 'utf8');

// Find the SMTP function
const smtpFunctionStart = functionsContent.indexOf('exports.sendEmailSMTP = functions.https.onRequest(async (req, res) => {');
if (smtpFunctionStart === -1) {
    console.error('SMTP function not found');
    process.exit(1);
}

// Find the img tag in the SMTP function
const imgTagStart = functionsContent.indexOf('<img src="data:image/png;base64,', smtpFunctionStart);
if (imgTagStart === -1) {
    console.error('Logo img tag not found in SMTP function');
    process.exit(1);
}

// Find the end of the img tag
const imgTagEnd = functionsContent.indexOf('"', imgTagStart + 25);
if (imgTagEnd === -1) {
    console.error('Could not find end of img tag');
    process.exit(1);
}

// Replace with external hosted logo URL
const newImgTag = '<img src="https://realinvestco.com/Pics/logo.png" alt="Real InvestCo Logo" style="max-width: 200px; height: auto; margin-bottom: 15px;">';

// Replace the old img tag with the new one
const beforeImg = functionsContent.substring(0, imgTagStart);
const afterImg = functionsContent.substring(imgTagEnd + 1);

functionsContent = beforeImg + newImgTag + afterImg;

// Write the updated content back to the file
fs.writeFileSync('functions/index.js', functionsContent);

console.log('SMTP function updated with external logo URL');
console.log('New img tag:', newImgTag); 