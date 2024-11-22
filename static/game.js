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
    players[i].children[0].addEventListener("click", playerSelected.bind(null, i))
}

var currentShape = [[]]
var color;

function selectPiece(event, elt, shape, col) {
    if(document.querySelector(".selected")) document.querySelector(".selected").remove()
    var clone = elt.parentNode.cloneNode(true)
    clone.classList.add("selected")
    document.querySelector("#gameInterface").appendChild(clone)
    var selected = document.querySelector(".selected")
    selected.style.left = `${event.clientX - 1.5 * window.innerHeight / 100}px`
    selected.style.top = `${event.clientY - 1.5 * window.innerHeight / 100}px`
    currentShape = shape
    color = col
}

var overCell = false
spots = []

function selectSpot(x, y) {
    var possible = true
    var angleContact = false 
    overCell = true
    var selected = document.querySelector(".selected")
    if(selected) selected.style.visibility = "hidden"
    for(i = 0; i < currentShape.length; i++) {
        for (j = 0; j < currentShape[0].length; j++) {
            if((x+i > 20) || (y+j > 20) || (x+i < 1) || (y+j < 1)) {
                if(currentShape[i][j] == 1) possible = false
            } else if(currentShape[i][j] == 1) {
                spots.push(document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`))
                if(!document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`).classList.contains("c0")) possible = false
            } else if(currentShape[i][j] == 2 && document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`).classList.contains(`c${color}`)) {
                angleContact = true;
            } else if(currentShape[i][j] == 3 && document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`).classList.contains(`c${color}`)) {
                possible = false
            }
        }
    }
    if(possible && angleContact) {
        spots.forEach(elt => elt.style.border = "solid 3px green")
    } else {
        spots.forEach(elt => elt.style.border = "solid 3px red")
    }
    
}

function unselectSpot() {
    spots.forEach(elt => elt.style.border = "0px")
    spots = []
    // var selected = document.querySelector(".selected")
    // if(selected) selected.style.visibility = "visible"
    overCell = false
}

document.addEventListener("pointermove", (event) => {
    var selected = document.querySelector(".selected")
    if(!selected) return
    if(overCell) return
    if(!event.composedPath().includes(grid)) {
        
        var selected = document.querySelector(".selected")
        if(selected) selected.style.visibility = "visible"
        selected.style.left = `${event.clientX - 1.5 * window.innerHeight / 100}px`
        selected.style.top = `${event.clientY - 1.5 * window.innerHeight / 100}px`
    }
})

const playerInterfaces = document.querySelectorAll(".playerInterface")
const grid = document.querySelector("#grid")

document.addEventListener("click", (event) => {
    if(!event.composedPath().includes(grid) && !Array.from(playerInterfaces).map(elt => event.composedPath().includes(elt)).includes(true)) {
        var selected = document.querySelector(".selected")
        if(selected) selected.remove()
            currentShape = [[]]
    }
})


setInterval(() => {
    //updatedata()
}, 1000)