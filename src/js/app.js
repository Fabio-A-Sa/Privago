async function search() {
    const input = document.querySelector('#searchInput').value;
    window.location.href = `/search?input=${input}`;
}