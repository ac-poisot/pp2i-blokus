function updatedata() {
    fetch("/data?"+window.location.search.split("?")[1])
    .then(res => res.json())
    .then(data => {
        for(i=1; i < 21; i++) {
            for(j=1; j < 21; j++) {
                document.querySelector(`#grid>tbody>tr:nth-child(${i})>td:nth-child(${j})`).className = `c${data[i-1][j-1]}`
            }
        }
    })
}

const players = document.querySelectorAll("#otherPlayers>div");

function closeAll() {
    players.forEach(p => {
        if(!p.classList.contains("closed")) {
            p.classList.add("closed")
        }
    })
}


function playerSelected(i) {
    if(players[i].classList.contains("closed")) {
        closeAll();
        players[i].classList.remove("closed");
    } else {
        players[i].classList.add("closed")
    }
}


for(i = 0; i < players.length; i++) {
    players[i].addEventListener("click", playerSelected.bind(null, i))
}


setInterval(() => {
    updatedata()
}, 1000)