async function search() {
    const input = document.querySelector('#searchInput').value;
    const location = document.querySelector('#location').value;
    window.location.href = `/search?${new URLSearchParams({
        input: input,
        location: location
    })}`;
}