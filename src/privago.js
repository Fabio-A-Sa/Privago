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
let LOCATIONS;
const PORT = process.argv[2] || 3000;
const CONFIG = {
    "endpoint" : "http://localhost:8983/solr/hotels/select?",
    "parameters" : {
        "indent" : "true",
        "q.op" : "AND",
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
const baseStructure = fs.readFileSync(path.join(htmlPath, 'base-page.html'), 'utf8');
const homePage = baseStructure.replace('<main></main>', fs.readFileSync(path.join(htmlPath, 'home-page.html'), 'utf8')).replace(
    '<locations></locations>', selectLocations(),
);
const searchPage = baseStructure.replace('<main></main>', fs.readFileSync(path.join(htmlPath, 'search-page.html'), 'utf8')).replace(
    '<locations></locations>', selectLocations(),
);
const hotelPage = baseStructure.replace('<main></main>', fs.readFileSync(path.join(htmlPath, 'hotel-page.html'), 'utf8'))

// dependencies
app.use(cors());
app.use((_, res, next) => {
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
async function getReviews(searchInput, location) {
    console.log(location);
    const queryLocation = `{!child of=\"*:* -_nest_path_:*\"}location:` + (
        location ? location.split(' ')[0] : '*'
    )
    console.log(queryLocation)
    const request = `${CONFIG.endpoint}q=${searchInput}&${new URLSearchParams(CONFIG.parameters)}&fq=${queryLocation}`;
    return await getResponse(request);
}

// Fetch hotels with a specified limit
async function getHotels(limit) {
    const request = `${CONFIG.endpoint}q=name:*&rows=${limit}&sort=average_rate%20desc`;
    return (await getResponse(request)).response.docs;
}

// Fetch all unique locations
async function getLocations() {

    try {
        const locationsContent = fs.readFileSync('locations.json', 'utf8');
        LOCATIONS = JSON.parse(locationsContent);

    } catch (error) {

        const hotels = await getHotels(30000);
        const locationsSet = new Set(hotels.map((h) => h.location));
        LOCATIONS = Array.from(locationsSet).sort();

        fs.writeFile('locations.json', JSON.stringify(locations, null, 2), (err) => {
            if (err) throw err;
        });
    }
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

// Transforms specified query tokens in a given text into bold format.
function transformText(text, query) {
    let text_tokens = text.split(' ');
    const query_tokens = query.toLowerCase().split(' ');

    for (let i = 0; i < text_tokens.length; i++) {
        if (query_tokens.includes(text_tokens[i].toLowerCase())) {
            text_tokens[i] = `<b>${text_tokens[i]}</b>`;
        }
    }
    return text_tokens.join(' ');
}

// Create HTML for reviews
async function createReviewsHTML(results, isSearchPage, query = null) {
    const docs = results.response.docs;
    const articlesHTML = await Promise.all(docs.map(async doc => {

        const hotelId = doc.id.split('/')[0]
        const hotel = await getHotelInfo(hotelId);
        const text = query ? transformText(doc.text, query) : doc.text;
        const hotelInfoHTML = isSearchPage 
                                ? `<h3><a href="/hotel?id=${hotelId}">${hotel.name}</a> with ${hotel.average_rate} stars in ${hotel.location}</h3>` 
                                : '' ;
        return `
            <article class="review">
                ${hotelInfoHTML}
                <h4>"${text}"</h4>
                <h5>${doc.date}. Rate: ${doc.rate} stars</h5>
                <h6><a href="/more?id=${doc.id}">More...</a></h6>
            </article>
        `;
    }));

    return docs.length !== 0 ? articlesHTML.join('') : null;
}

// Create HTML for selecting hotels location
function selectLocations() {
    getLocations();
    let htmlString = '<select name="location" id="location"><option value="Any" selected>Any</option>';
    LOCATIONS.forEach(location => {
        htmlString += `<option value="${location}">${location}</option>`;
    });
    return htmlString + '</select>';
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
function getUpdatedSearchPage(reviews, input, location) {
    let updatedHTML = searchPage;
    if (input) updatedHTML = updatedHTML.replace(/id="searchInput"/g, `id="searchInput" value="${input}"`)
    if (location && location !== 'Any') {
        updatedHTML = updatedHTML.replace(
            '<option value="Any" selected="">Any</option>', '<option value="Any">Any</option>'
        ).replace(
            `<option value="${location}">${location}</option>`, `<option value="${location}" selected="">${location}</option>`
        )
    }
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
    const location = req?.query?.location;
    const reviews = await getReviews(input, location);
    const reviewsHTML = await createReviewsHTML(reviews, true, input);
    const updatedHTML = getUpdatedSearchPage(reviewsHTML, input, location);
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
