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

function updatedata() {
    fetch("/data?"+window.location.search.split("?")[1])
    .then(res => res.json())
    .then(data => document.querySelector("#time").innerText = data["time"])
}


//adress="http://127.0.0.1:5500/"

setInterval(() => {
    updatedata()
}, 1000)