// slider source: https://codepen.io/joosts/pen/rNLdxvK

onload = () => {
    var input = document.getElementById("searchInput");

    input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("searchButton").click();
        }
    });

    const reviewInput = document.querySelectorAll(
            "#reviewRate .range-input input"
        ),
        reviewContent = document.querySelectorAll(
            "#reviewRate .price-content p"
        ),
        reviewRange = document.querySelector("#reviewRate .slider .progress");

    reviewInput.forEach((input) => {
        input.addEventListener("input", (e) => {
            let minVal = parseInt(reviewInput[0].value),
                maxVal = parseInt(reviewInput[1].value);

            reviewContent[0].innerHTML = minVal;
            reviewContent[1].innerHTML = maxVal;
            reviewRange.style.left =
                (minVal / reviewInput[0].max) * 100 * 0.95 + "%";
            reviewRange.style.right =
                (100 - (maxVal / reviewInput[1].max) * 100) * 0.95 + "%";
        });
    });

    const hotelInput = document.querySelectorAll(
            "#hotelRate .range-input input"
        ),
        hotelContent = document.querySelectorAll("#hotelRate .price-content p"),
        hotelRange = document.querySelector("#hotelRate .slider .progress");

    hotelInput.forEach((input) => {
        input.addEventListener("input", (e) => {
            let minVal = parseInt(hotelInput[0].value),
                maxVal = parseInt(hotelInput[1].value);

            hotelContent[0].innerHTML = minVal;
            hotelContent[1].innerHTML = maxVal;
            hotelRange.style.left =
                (minVal / hotelInput[0].max) * 100 * 0.95 + "%";
            hotelRange.style.right =
                (100 - (maxVal / hotelInput[1].max) * 100) * 0.95 + "%";
        });
    });
};
