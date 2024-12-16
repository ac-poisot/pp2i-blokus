function getCookie(name) {
    var data = `; ${document.cookie}`
    var c = data.split(`; ${name}=`)
    if (c.length == 2) {
        return c[1].split("; ")[0]
    }
}

function copyLink(roomid) {
    var link = document.querySelector("#roomid")
    navigator.clipboard.writeText(`${window.location.href.split("/create")[0]}/join?roomid=${roomid}`)
}

var players = [getCookie("pid"), undefined, undefined, undefined]
var usernames = players
var playerNameSpans = document.querySelectorAll(".content > .playerName")
var blocks = document.querySelectorAll(".selectPlayer")
var urlParams = new URLSearchParams(window.location.search)

var langData = null
async function fetchLanguageData() {
    const response = await fetch(`/static/lang/${localStorage.getItem('language') || 'fr'}.json`);
    const data = await response.json()

    return data;
}

fetchLanguageData().then(data => langData = data)

function updateNames() {
    fetchLanguageData().then(data => langData = data)
    console.log(usernames)
    for(i = 0; i < players.length; i++) {
        if(!usernames[i]) {
            playerNameSpans[i].setAttribute("data", "")
            playerNameSpans[i].textContent = "None"
        } else if(usernames[i] == "Empty slot") {
            playerNameSpans[i].setAttribute("data", "empty_slot")
            playerNameSpans[i].textContent = langData["empty_slot"]
        } else if(usernames[i].slice(0, 6) == "Guest ") {
            playerNameSpans[i].setAttribute("data", "guest")
            playerNameSpans[i].textContent = langData["guest"] + usernames[i].slice(6)
        } else if(usernames[i].slice(0, 2) == "AI") {
            playerNameSpans[i].setAttribute("data", "AI")
            playerNameSpans[i].textContent = langData["AI"] + usernames[i].slice(2)
        } else {
            playerNameSpans[i].setAttribute("data", "")
            playerNameSpans[i].textContent = usernames[i]
        }
    }
}

function handleError(error) {
    if(error == "Not connected") {
        document.cookie = ""
        window.location.href = '/not_connected'
    }
    if(error == "Not allowed") {
        window.location.href = '/not_allowed'
    }
    if(error == "Non-existent room") {
        window.location.href = '/non_existent_room'
}}

async function handleRes(res) {
    if(!res.ok) throw new Error(`Response status: ${res.status}`)
        var data = await res.json()
        if (data["error"]) {
            handleError(data["error"])
            return
        }
        if(data["redirection"]) window.location.href = data["redirection"]
        players = data["players"]
        usernames = data["usernames"]
        updateNames()
}

function updatedata() {
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "GET",
        headers: {'Content-Type': 'application/json'}
    }).then(async res => {
        if(!res.ok) throw new Error(`Response status: ${res.status}`)
        var data = await res.json()
        if (data["error"]) {
            handleError(data["error"])
            return
        }
        players = data["players"]
        usernames = data["usernames"]
        for(i = 0; i < players.length; i++) {
            if(players[i] == undefined ){
                blocks[i].classList.add("grayed")
                blocks[i].children[0].classList.add("grayed")
                if(blocks[i].children[4]) blocks[i].children[4].classList.add("hidden")
                if(blocks[i].children[5]) blocks[i].children[5].classList.add("hidden")
            } else {
                blocks[i].classList.remove("grayed")
                blocks[i].children[0].classList.remove("grayed")
                if(blocks[i].children.length > 4) {
                    if (!(players[i] == undefined || (typeof players[i] == 'string' && players[i].includes("AI")) || (typeof players[i] == 'string' && players[i].includes("Guest ")))) {
                        blocks[i].children[4].classList.remove("hidden")
                        blocks[i].children[5].classList.add("hidden")
                    } else if (typeof players[i] == 'string' && players[i].includes("Guest ")) {
                        blocks[i].children[4].classList.add("hidden")
                        blocks[i].children[5].classList.remove("hidden")
                    }
                }
            }
        }
        updateNames()
    })
}

function addHumanPlayer(btn, i) {
    btn.parentElement.classList.remove("grayed")
    btn.parentElement.children[0].classList.remove("grayed")
    btn.parentElement.children[4].classList.remove("hidden")
    players[i-1] = -1
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({players})
    }).then(res => handleRes(res))
}

function addAIPlayer(btn, i) {    
    btn.parentElement.classList.remove("grayed")
    btn.parentElement.children[0].classList.remove("grayed")
    var needAI = {
        index: i-1,
        level: 2
    }
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({players, needAI})
    }).then(res => handleRes(res))
}

function removePlayer(btn, i) {
    btn.parentElement.classList.add("grayed")
    btn.parentElement.children[0].classList.add("grayed")
    btn.parentElement.children[4].classList.add("hidden")
    btn.parentElement.children[5].classList.add("hidden")
    players[i-1] = undefined
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({players})
    }).then(res => handleRes(res))
}

function addLocalPlayer(btn, i) {
    players[i-1] = `Guest ${i}`
    btn.classList.add("hidden")
    btn.parentElement.children[5].classList.remove("hidden")
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({players})
    }).then(res => handleRes(res))
}

function removeLocalPlayer(btn, i) {
    players[i-1] = -1
    btn.parentElement.children[4].classList.remove("hidden")
    btn.classList.add("hidden")
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({players})
    }).then(res => handleRes(res))
}




function leaveRoom() {
    i = players.indexOf(parseInt(getCookie("pid")))
    players[i] = -1
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({players})
    }).then(res => handleRes(res))
}


function createGame() {
    fetch(`/API/create?roomid=${urlParams.get("roomid")}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"launch": true})
    }).then(res => {
        window.location.href= `${window.location.href.split("/create")[0]}/game?gameid=${urlParams.get("roomid")}`
    })
}


// Automatically update the game informations

setInterval(() => {
    updatedata()
}, 1000)