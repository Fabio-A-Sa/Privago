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
const PORT = process.argv[2] || 3000;
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

// pages
const baseStructure = fs.readFileSync(path.join(htmlPath, 'base.html'), 'utf8');
const homePage = baseStructure.replace('<main></main>', fs.readFileSync(path.join(htmlPath, 'home.html'), 'utf8'))
const searchPage = baseStructure.replace('<main></main>', fs.readFileSync(path.join(htmlPath, 'search.html'), 'utf8'))
const hotelPage = baseStructure.replace('<main></main>', fs.readFileSync(path.join(htmlPath, 'hotel.html'), 'utf8'))

// dependencies
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

// Fetch the response of a request
async function getResponse(request) {
    const response = await fetch(request);
    if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
}

// Fetch reviews based on search input
async function getReviews(searchInput) {
    const request = `${CONFIG.endpoint}q=${searchInput}&${new URLSearchParams(CONFIG.parameters)}`;
    return await getResponse(request);
}

// Fetch hotels with a specified limit
async function getHotels(limit) {
    const request = `${CONFIG.endpoint}q=name:n&rows=${limit}&sort=average_rate%20desc`;
    return (await getResponse(request)).response.docs;
}

// Fetch hotel information based on ID
async function getHotelInfo(hotelId) {
    const request = `${CONFIG.endpoint}q=id:${hotelId}&rows=${CONFIG.parameters.rows}`;
    return (await getResponse(request)).response.docs[0]
}

// Fetch reviews of a hotel based on ID
async function getHotelReviews(hotelId) {
    const request = `${CONFIG.endpoint}q=id:${hotelId}/*&rows=1000`;
    return await getResponse(request)
}

// Create HTML for reviews
async function createReviewsHTML(results, isSearchPage) {
    const docs = results.response.docs;
    const articlesHTML = await Promise.all(docs.map(async doc => {

        const hotelId = doc.id.split('/')[0]
        const hotel = await getHotelInfo(hotelId);
        const hotelInfoHTML = isSearchPage 
                                ? `<h3><a href="/hotel?id=${hotelId}">${hotel.name}</a> with ${hotel.average_rate} stars in ${hotel.location}</h3>` 
                                : '' ;
        return `
            <article class="review">
                ${hotelInfoHTML}
                <h4>"${doc.text}"</h4>
                <h5>${doc.date}. Rate: ${doc.rate} stars</h5>
            </article>
        `;
    }));

    return docs.length !== 0 ? articlesHTML.join('') : null;
}

// Create HTML for a single hotel
function createHotelHTML(hotel, hotelPage) {
    return `
        <article class="${hotelPage ? '' : 'hotel'}">
            <h3><a href="/hotel?id=${hotel.id}">${hotel.name}</a></h3>
            <h4>${hotel.average_rate} stars, in ${hotel.location}</h4>
        </article>
    `
}

// Create HTML for multiple hotels
function createHotelsHTML(hotels) {
    let hotelsHTML = '';
    hotels.forEach(hotel => {
        hotelsHTML += createHotelHTML(hotel, false);
    });
    return hotelsHTML;
}

// Update the search page with results and search input
function getUpdatedSearchPage(reviews, input) {
    let updatedHTML = searchPage;
    if (input) updatedHTML = updatedHTML.replace(/id="searchInput"/g, `id="searchInput" value="${input}"`)
    if (reviews) updatedHTML = updatedHTML.replace('<p>No results found</p>', reviews)
    return updatedHTML;
}

// Update the hotel page with hotel information and reviews
function getUpdatedHotelPage(hotel, reviews) {
    let updatedHTML = hotelPage;
    if (hotel) updatedHTML = updatedHTML.replace('<p>No hotel found</p>', createHotelHTML(hotel, true));
    if (reviews) updatedHTML = updatedHTML.replace('<p>No reviews found</p>', reviews);
    return updatedHTML;
}   

// home page
app.get('/', async (req, res) => {
    const hotels = await getHotels(20);
    const html = hotels ? homePage.replace('<p>No hotels found</p>', createHotelsHTML(hotels))
                        : homePage
    res.send(html);
});

// search page
app.get('/search', async (req, res) => {
    const input = req?.query?.input;
    const reviews = await getReviews(input);
    const reviewsHTML = await createReviewsHTML(reviews, true);
    const updatedHTML = getUpdatedSearchPage(reviewsHTML, input);
    res.send(updatedHTML);
});

// hotel page
app.get('/hotel', async (req, res) => {
    const id = req?.query?.id;
    const results = await getHotelReviews(id);
    const hotel = await getHotelInfo(id);
    const reviewsHTML = await createReviewsHTML(results, false);
    const updatedHTML = getUpdatedHotelPage(hotel, reviewsHTML);
    res.send(updatedHTML);
});

// create server
app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT}`);
});
