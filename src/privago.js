const express = require('express');
const path = require('path');
const app = express();
const cors = require('cors');
const fs = require('fs');

const cssPath = path.join(__dirname, 'css');
const jsPath = path.join(__dirname, 'js');
const htmlPath = path.join(__dirname, 'html');
const port = process.argv[2] || 3000;
const html = fs.readFileSync(path.join(htmlPath, 'index.html'), 'utf8');

const CONFIG = {
    "endpoint" : "http://localhost:8983/solr/hotels/select?",
    "parameters" : {
        "indent" : "true",
        "q.op" : "AND",
        "fq" : "{!child of=\"*:* -_nest_path_:*\"}location:*",
        "sort" : "score desc",
        "start" : "0",
        "rows" : "20",
        "fl" : "*, [child]",
        "defType" : "edismax",
        "qf" : "text^7 name location^2",
        "pf" : "text^10",
        "ps" : 3
    }
}

app.use(cors());

app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

app.use('/css', express.static(cssPath, { 'extensions': ['css'] }));
app.use('/js', express.static(jsPath, { 'extensions': ['js'] }));
app.use(express.static(htmlPath));

async function getAPIResults(input) {
    const url = `${CONFIG.endpoint}q=${input}&${new URLSearchParams(CONFIG.parameters)}`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Erro na solicitação: ${response.status}`);
    }
    return await response.json();
}

function createArticles(results) {

    const docs = results.response.docs;

    const articlesHTML = docs.map(doc => {
        return `
            <article>
                <h3>${doc.date}</h3>
                <p>${doc.text}</p>
            </article>
        `;
    });

    return docs.length != 0 ? articlesHTML.join('') : null;
}

function getUpdatedHTML(articles, input) {
    const updatedHTML = html.replace(/id="searchInput"/g, `id="searchInput" value="${input}"`)
    return articles ? updatedHTML.replace('<p>No results found</p>', articles)
                    : updatedHTML
}

app.get('/', (req, res) => {
    res.send(html);
});

app.get('/search', async (req, res) => {
    const input = req.query.input;
    console.log("input é")
    console.log(input)
    const results = await getAPIResults(input);
    const articles = createArticles(results);
    const updatedHTML = getUpdatedHTML(articles, input);
    res.send(updatedHTML);
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
