async function search() {
    const input = document.querySelector('#searchInput').value;
    const location = document.querySelector('#location').value;
    const reviewRateMin = document.querySelector('#reviewRateMin').value;
    const reviewRateMax = document.querySelector('#reviewRateMax').value;
    const hotelRateMin = document.querySelector('#hotelRateMin').value;
    const hotelRateMax = document.querySelector('#hotelRateMax').value;
    window.location.href = `/search?${new URLSearchParams({
        input: input,
        location: location,
        rrmin: reviewRateMin,
        rrmax: reviewRateMax,
        hrmin: hotelRateMin,
        hrmax: hotelRateMax,
    })}`;
}