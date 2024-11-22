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
    console.log(players[i].children)
    players[i].children[0].addEventListener("click", playerSelected.bind(null, i))
}

function selectPiece(elt,shape) {
    if(document.querySelector(".selected")) document.querySelector(".selected").remove()
    var clone = elt.parentNode.cloneNode(true)
    clone.classList.add("selected")
    document.querySelector("#gameInterface").appendChild(clone)
}

document.addEventListener("pointermove", (event) => {
    var selected = document.querySelector(".selected")
    if(!selected) return
    selected.style.left = `${event.clientX - 1.5 * window.innerHeight / 100}px`
    selected.style.top = `${event.clientY - 1.5 * window.innerHeight / 100}px`
})

const playerInterfaces = document.querySelectorAll(".playerInterface")
const grid = document.querySelector("#grid")

document.addEventListener("click", (event) => {
    if(!event.composedPath().includes(grid) && !Array.from(playerInterfaces).map(elt => event.composedPath().includes(elt)).includes(true)) {
        var selected = document.querySelector(".selected")
        if(selected) selected.remove()
    }
})


setInterval(() => {
    updatedata()
}, 1000)