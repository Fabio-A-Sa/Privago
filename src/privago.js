const express = require('express');
const path = require('path');
const app = express();
const fs = require('fs');

const cssPath = path.join(__dirname, 'css');
const jsPath = path.join(__dirname, 'js');
const htmlPath = path.join(__dirname, 'html');
const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
const port = process.argv[2] || 3000;

app.use('/css', express.static(cssPath, { 'extensions': ['css'] }));
app.use('/js', express.static(jsPath, { 'extensions': ['js'] }));
app.use(express.static(htmlPath));

app.get('/', (req, res) => {
    const html = fs.readFileSync(path.join(htmlPath, 'index.html'), 'utf8');
    res.send(html);
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
    console.log('Configurations:', config);
});