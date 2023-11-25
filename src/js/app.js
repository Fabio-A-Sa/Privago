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

async function search() {
    const input = document.getElementById('searchInput').value;
    document.querySelector('.searchResults').innerHTML = await getResults(input);
}