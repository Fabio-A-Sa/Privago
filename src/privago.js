// imports
const express = require('express');
const path = require('path');
const app = express();
const cors = require('cors');
const fs = require('fs');

// paths
const cssPath = path.join(__dirname, 'css');
const jsPath = path.join(__dirname, 'js');
const htmlPath = path.join(__dirname, 'html');

// constants
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

const port = process.argv[2] || 3000;
const html = fs.readFileSync(path.join(htmlPath, 'index.html'), 'utf8');

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

async function getResponse(request) {
    const response = await fetch(request);
    if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
}

async function getReviews(searchInput) {
    const request = `${CONFIG.endpoint}q=${searchInput}&${new URLSearchParams(CONFIG.parameters)}`;
    return await getResponse(request);
}

async function getHotelInfo(hotelId) {
    const request = `${CONFIG.endpoint}q=id:${hotelId}&rows=${CONFIG.parameters.rows}`;
    return (await getResponse(request)).response.docs[0]
}

async function getHotelReviews(hotelId) {
    const request = `${CONFIG.endpoint}q=id:${hotelId}/*&rows=1000`;
    return await getResponse(request)
}

// TODO: create articles based on hotels page or search page
async function createArticles(results) {
    const docs = results.response.docs;
    const articlesHTML = await Promise.all(docs.map(async doc => {
        const hotelId = doc.id.split('/')[0]
        const hotel = await getHotelInfo(hotelId);
        return `
            <article>
                <h3>${doc.date}</h3>
                <p>${doc.rate}</p>
                <p>${doc.text}</p>
                <p>Regarding <a href="/hotel?id=${hotelId}">${hotel.name}</a> with ${hotel.average_rate} stars in ${hotel.location}</p>
            </article>
        `;
    }));

    return docs.length !== 0 ? articlesHTML.join('') : null;
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
    const results = await getReviews(input);
    const articles = await createArticles(results);
    const updatedHTML = getUpdatedHTML(articles, input);
    res.send(updatedHTML);
});

app.get('/hotel', async (req, res) => {
    const id = req.query.id;
    const results = await getHotelReviews(id);
    const articles = await createArticles(results);
    const updatedHTML = getUpdatedHTML(articles, 'nothing for now');
    res.send(updatedHTML);
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
