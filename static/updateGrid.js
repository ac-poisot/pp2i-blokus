function updatedata() {
    fetch("/data?"+window.location.search.split("?")[1])
    .then(res => res.json())
    .then(data => {
        for(i=1; i < 21; i++) {
            for(j=1; j < 21; j++) {
                document.querySelector(`tbody>tr:nth-child(${i})>td:nth-child(${j})`).className = `c${data[i-1][j-1]}`
            }
        }
    })
}

setInterval(() => {
    console.log("test")
    updatedata()
}, 1000)