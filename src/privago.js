const express = require('express');
const app = express();
const fs = require('fs');
const port = process.argv[2] || 3000;
const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
  
app.get('/', (req, res) => {
    const html = fs.readFileSync('html/index.html', 'utf8');
    res.send(html);
});
  
app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
    console.log('Configurations:', config);
});