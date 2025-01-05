// Functions to update the game grid and players

var players = document.querySelectorAll("#otherPlayers>div")
var isplaying = -1

var currentShape = [[]]
var currentid = -1
var currx = -1
var curry = -1
var color = parseInt(document.querySelector(".playerInterface").classList[1][1]);
var spots = []
var oriented = 0
var correct = false
var inverted = false

var langData = null
async function fetchLanguageData() {
    const response = await fetch(`/static/lang/${localStorage.getItem('language') || 'fr'}.json`);
    const data = await response.json()

    return data;
}

fetchLanguageData().then(data => langData = data)

function updatedata() {
    fetch(`API//data?${window.location.search.split("?")[1]}`, {credentials: "same-origin"})
    .then(res => res.json())
    .then(data => {
        if (data["error"]) {
            document.location.reload()
            return
        }
        if(data["grid"]) {
            for(i=1; i < 21; i++) {
                for(j=1; j < 21; j++) {
                    document.querySelector(`#grid>tbody>tr:nth-child(${i})>td:nth-child(${j})`).className = `c${data["grid"][i-1][j-1]}`
                }
            }
            for(i = 0; i < data["players"].length; i++) {
                if(document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`)) {
                    if(data["players"][i].slice(0, 6) == "Guest ") {
                        document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`).textContent = langData["guest"] + data["players"][i].slice(6)
                    } else if(data["players"][i].slice(0, 2) == "AI") {
                        document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`).textContent = langData["AI"] + data["players"][i].slice(2)
                    } else {
                        document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`).textContent = data["players"][i]
                    }
                }
            }

        }
        if(data["finished"]) window.location.reload()
        var piecesids = data["piecesids"]
        for(i = 0; i < 4; i++) {
            for(j = 0; j < 21; j++) {
                var pieceNode = document.querySelector(`div.c${i+1} > div:nth-child(2) > div.piece.n${j+1}`)
                if(pieceNode && piecesids[i].indexOf(j+1) == -1) {
                    pieceNode.remove()
                }
            }
        }
        isplaying = data["isplaying"]
        var elt1 = document.querySelector("#player > .playerInterface")
        var elt2 = document.querySelector(`.playerInterface.c${data["you"]}`)
        if (elt1 != elt2) {
            if(elt2.classList.length == 3) {
                elt2.classList.remove("closed")
                elt1.classList.add("closed")
            }
            document.querySelector("#otherPlayers").insertBefore(elt1, elt2)
            document.querySelector("#player").prepend(elt2)
            color = parseInt(document.querySelector("#player > .playerInterface").classList[1][1])
            players = document.querySelectorAll("#otherPlayers>div")
        }
        document.querySelectorAll(".playerInterface").forEach(elt => {
            elt.classList.remove("playing")
        })
        document.querySelector(`.playerInterface.c${isplaying}`).classList.add("playing")

        historyList = Array.from(data["history"])
        var historyelt = document.querySelector("#history")
        interesting = historyList.slice(0, historyList.length - historyelt.children.length)
        interesting.reverse().forEach(elt => {
            var newMove = document.createElement("li")

            console.log(elt)
            if(elt.length != 4) {
                console.log(elt, " forfeited")
                var newPlayer = document.createElement("span")
                newPlayer.textContent = elt

                var newAction = document.createElement("span")
                newAction.textContent = langData["history_forfeit"]
                newAction.data = "history_forfeit"

                newMove.appendChild(newPlayer)
                newMove.appendChild(newAction)

            } else {
                var newPlayer = document.createElement("span")
                newPlayer.textContent = elt[1]

                var newAction = document.createElement("span")
                newAction.textContent = langData["history_played"]
                newAction.data = "history_played"

                var newPiece = document.createElement("div")
                newPiece.className = "piece"
                var newTable = document.createElement("table")
                elt[2].forEach(li => {
                    var newRow = document.createElement("tr")
                    li.forEach(cell => {
                        var newCell = document.createElement("td")
                        newCell.className = `c${cell == 1 ? elt[0] : 0}`
                        newRow.appendChild(newCell)
                    })
                    newTable.appendChild(newRow)
                })
                newPiece.appendChild(newTable)

                var locationIndication = document.createElement("span")
                locationIndication.textContent = langData["history_at"]
                locationIndication.data = "history_at"

                var coords = document.createElement("span")
                coords.textContent = `(${elt[3][0]}, ${elt[3][1]})`

                newMove.appendChild(newPlayer)
                newMove.appendChild(newAction)
                newMove.appendChild(newPiece)
                newMove.appendChild(locationIndication)
                newMove.appendChild(coords)
            }

            historyelt.prepend(newMove)
        })
    })
}

// Functions to open at most one other player's interface in addition to the player's

function closeAll() {
    players.forEach(p => {
        if(!p.classList.contains("closed")) {
            p.classList.add("closed")
        }
    })
}


function playerSelected(elt) {
    if(elt.classList.contains("closed") && Array.from(players).indexOf(elt) != -1) {
        closeAll();
        elt.classList.remove("closed");
    } else if (Array.from(players).indexOf(elt) != -1) {
        elt.classList.add("closed")
    }
}


// for(i = 0; i < players.length; i++) {
//     players[i].children[0].addEventListener("click", playerSelected.bind(null, i))
// }


// Functions to select and move pieces


function selectPiece(event, elt, shape, col, id) {
    if(document.querySelector(".selected")) {
        document.querySelector(".selected").remove()
        document.querySelector(".chosenOne").classList.remove("chosenOne")
    }
    if(col != -1 && col != isplaying) return
    var clone = elt.parentNode.cloneNode(true)
    elt.parentNode.classList.add("chosenOne")
    clone.classList.add("selected")
    document.querySelector("#gameInterface").appendChild(clone)
    var selected = document.querySelector(".selected")
    selected.style.left = `${event.clientX - 0.8 / 100 * window.innerHeight}px`
    selected.style.top = `${event.clientY - 0.8 * window.innerWidth / 100}px`
    currentShape = shape
    currentid = id
    oriented = 0
    inverted = false
    color = col
}

function rotateMat(mat) {
    turned = []
    for(var i = 0; i < Math.max(mat.length, mat[0].length); i++) {
        var col = []
        for(j = 0; j < mat.length; j++) {
            if(mat[j] && mat[j][i] != undefined) col.push(mat[j][i])
        }
        turned.push(col.reverse())
    }
    return turned.filter(elt => elt != [])
}

function rotatePiece() {
    currentShape = rotateMat(currentShape)
    if(inverted) {
        oriented = (oriented + 3) % 4
    } else {
        oriented = (oriented + 1) % 4
    }
    var code = "<table>"
    for(let i = 1; i < currentShape.length - 1; i++) {
        code += "<tr>"
        for(let j = 1; j < currentShape[i].length - 1; j++) {
            code += `<td class="c${currentShape[i][j] == 1 ? color : ''}"></td>`
        }
        code += "</tr>"
    }
    code += "</table>"
    document.querySelector(".selected").innerHTML = code
}

function reversePiece() {
    currentShape = currentShape.map(li => li.reverse())
    inverted = !inverted
    var code = "<table>"
    for(let i = 1; i < currentShape.length - 1; i++) {
        code += "<tr>"
        for(let j = 1; j < currentShape[i].length - 1; j++) {
            code += `<td class="c${currentShape[i][j] == 1 ? color : ''}"></td>`
        }
        code += "</tr>"
    }
    code += "</table>"
    document.querySelector(".selected").innerHTML = code
}



function selectSpot(x, y) {
    if(currentid == -1) return
    var possible = true
    var angleContact = false
    var selected = document.querySelector(".selected")
    if(selected) selected.style.visibility = "hidden"
    var currentShapeClean = currentShape.filter(elt => elt.length > 0)
    currx = x
    curry = y
    for(i = 0; i < currentShapeClean.length; i++) {
        for (j = 0; j < currentShapeClean[0].length; j++) {
            if((x+i > 20) || (y+j > 20) || (x+i < 1) || (y+j < 1)) {
                if(currentShapeClean[i][j] == 1) possible = false
            } else if(currentShapeClean[i][j] == 1) {
                spots.push(document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`))
                if(!document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`).classList.contains("c0")) possible = false
            } else if(currentShapeClean[i][j] == 2 && document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`).classList.contains(`c${color}`)) {
                angleContact = true;
            } else if(currentShapeClean[i][j] == 3 && document.querySelector(`#grid > tbody:nth-child(1) > tr:nth-child(${x+i}) > td:nth-child(${y+j})`).classList.contains(`c${color}`)) {
                possible = false
            }
        }
    }
    if(possible && angleContact) {
        spots.forEach(elt => elt.style.border = "solid 3px green")
        correct = true
    } else if(possible && document.querySelectorAll(`#grid > tbody > tr > td.c${color}`).length == 0 && ((x == 0 && y == 0 && currentShapeClean[1][1] == 1) || (x == 0 && y + currentShapeClean[1].length - 3 == 19 && currentShapeClean[1][currentShapeClean[1].length - 2] == 1) || (x + currentShapeClean.length - 3 == 19 && y == 0 && currentShapeClean[currentShapeClean.length - 2][1] == 1) || (x + currentShapeClean.length - 3 == 19 && y + currentShapeClean[1].length - 3 == 19 && currentShapeClean[currentShapeClean.length - 2][currentShapeClean[1].length - 2] == 1))) {
        spots.forEach(elt => elt.style.border = "solid 3px green")
        correct = true
    } else {
        spots.forEach(elt => elt.style.border = "solid 3px red")
        correct = false
    }
    
}

function unselectSpot() {
    spots.forEach(elt => elt.style.border = "0px")
    spots = []
    correct = false
    currx = -1
    curry = -1
}

const playerInterfaces = document.querySelectorAll(".playerInterface")
const grid = document.querySelector("#grid")
const historyelt = document.querySelector("#history")

document.addEventListener("pointermove", (event) => {
    var selected = document.querySelector(".selected")
    if(!selected) return
    if(!event.composedPath().includes(grid) && !event.composedPath().includes(historyelt)) {
        
        var selected = document.querySelector(".selected")
        if(selected) selected.style.visibility = "visible"
        selected.style.left = `${event.clientX - 0.8 * window.innerWidth / 100}px`
        selected.style.top = `${event.clientY - 0.8 * window.innerWidth / 100}px`
    }
})

document.addEventListener("click", (event) => {
    if(!event.composedPath().includes(grid) && !Array.from(playerInterfaces).map(elt => event.composedPath().includes(elt)).includes(true) && document.querySelector(".chosenOne")) {
        var selected = document.querySelector(".selected")
        if(selected) selected.remove()
        currentShape = [[]]
        currentid = -1
        currx = -1
        curry = -1
        document.querySelector(".chosenOne").classList.remove("chosenOne")
    }
})

function play() {
    if(correct && isplaying == color) {
        var selected = document.querySelector(".selected")
        if(selected) selected.remove()
        document.querySelector(".chosenOne").remove()
        fetch(`API//data?${window.location.search.split("?")[1]}`, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"piece": currentid, "orientation": oriented, "x": currx, "y": curry, "inverted": inverted})
        }).then(res => res.json()
        ).then(data => {
            if (data["error"]) {
                document.location.reload()
                return
            }
            if(data["grid"]) {
                for(i=1; i < 21; i++) {
                    for(j=1; j < 21; j++) {
                        document.querySelector(`#grid>tbody>tr:nth-child(${i})>td:nth-child(${j})`).className = `c${data["grid"][i-1][j-1]}`
                    }
                }
                for(i = 0; i < data["players"].length; i++) {
                    if(document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`)) document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`).textContent = data["players"][i]
                }
    
            }
            if(data["finished"]) window.location.reload()
            isplaying = data["isplaying"]
            var elt1 = document.querySelector("#player > .playerInterface")
            var elt2 = document.querySelector(`.playerInterface.c${data["you"]}`)
            if (elt1 != elt2) {
                if(elt2.classList.length == 3) {
                    elt2.classList.remove("closed")
                    elt1.classList.add("closed")
                }
                document.querySelector("#otherPlayers").insertBefore(elt1, elt2)
                document.querySelector("#player").prepend(elt2)
                color = parseInt(document.querySelector("#player > .playerInterface").classList[1][1])
                players = document.querySelectorAll("#otherPlayers>div")
            }
            color = parseInt(document.querySelector("#player > .playerInterface").classList[1][1])
            players = document.querySelectorAll("#otherPlayers>div")
        })
        currentShape = [[]]
        currentid = -1
    }
    
}

function forfeit() {
        fetch(`API//data?${window.location.search.split("?")[1]}`, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({})
        }).then(res => res.json()
        ).then(data => {
            if (data["error"]) {
                document.location.reload()
                return
            }
            if(data["grid"]) {
                for(i=1; i < 21; i++) {
                    for(j=1; j < 21; j++) {
                        document.querySelector(`#grid>tbody>tr:nth-child(${i})>td:nth-child(${j})`).className = `c${data["grid"][i-1][j-1]}`
                    }
                }
                for(i = 0; i < data["players"].length; i++) {
                    if(document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`)) document.querySelector(`div.c${i+1} > div:nth-child(1) > span:nth-child(1)`).textContent = data["players"][i]
                }
    
            }
            if(data["finished"]) window.location.reload()
            isplaying = data["isplaying"]
            var elt1 = document.querySelector("#player > .playerInterface")
            var elt2 = document.querySelector(`.playerInterface.c${data["you"]}`)
            if (elt1 != elt2) {
                if(elt2.classList.length == 3) {
                    elt2.classList.remove("closed")
                    elt1.classList.add("closed")
                }
                document.querySelector("#otherPlayers").insertBefore(elt1, elt2)
                document.querySelector("#player").prepend(elt2)
                color = parseInt(document.querySelector("#player > .playerInterface").classList[1][1])
                players = document.querySelectorAll("#otherPlayers>div")
            }
            color = parseInt(document.querySelector("#player > .playerInterface").classList[1][1])
            players = document.querySelectorAll("#otherPlayers>div")
        })
        currentShape = [[]]
        currentid = -1
    }
    



// Automatically update the game information

setInterval(() => {
    updatedata()
}, 100)