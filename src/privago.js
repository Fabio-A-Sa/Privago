const express = require('express');
const path = require('path');
const app = express();
const cors = require('cors');
const fs = require('fs');

const cssPath = path.join(__dirname, 'css');
const jsPath = path.join(__dirname, 'js');
const htmlPath = path.join(__dirname, 'html');
const port = process.argv[2] || 3000;

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
    // Construir a URL com base no CONFIG
    const url = `${CONFIG.endpoint}q=${input}&${new URLSearchParams(CONFIG.parameters)}`;
    console.log(url)
    try {
        // Fazer a solicitação HTTP usando fetch
        const response = await fetch(url);

        // Verificar se a solicitação foi bem-sucedida (código 200)
        if (!response.ok) {
            throw new Error(`Erro na solicitação: ${response.status}`);
        }

        // Converter a resposta para JSON e retornar
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erro na solicitação:", error);
        throw error;
    }
}

async function getResults(input) {
    const results = await getAPIResults(input);
    // HTML
    return results;
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

    return articlesHTML.join('');
}

app.get('/', (req, res) => {
    const html = fs.readFileSync(path.join(htmlPath, 'index.html'), 'utf8');
    res.send(html);
});

app.get('/search', async (req, res) => {
    const input = req.query.input;
    const results = await getResults(input);
    const articles = createArticles(results);
    
    // Enviar HTML completo com a seção preenchida
    const updatedHTML = getUpdatedHTML(articles);
    res.send(updatedHTML);
});

function getUpdatedHTML(articles) {
    let html = fs.readFileSync(path.join(htmlPath, 'index.html'), 'utf8');
    if (articles) {
        html = html.replace('<p>No results found</p>', articles);
    }
    return html;
}

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
