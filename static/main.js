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

function updateContent(langData) {
    console.log("a")
    document.querySelectorAll('[data]').forEach(element => {
        const key = element.getAttribute('data');
        console.log(key)
        element.innerHTML = langData[key] + element.innerHTML;
    });
}

async function fetchLanguageData(lang) {
    const response = await fetch(`/static/lang/${lang}.json`);
    return response.json();
}

async function changeLanguage(lang) {
    await setLanguagePreference(lang);
    
    const langData = await fetchLanguageData(lang);
    updateContent(langData);
}

function setLanguagePreference(lang) {
    localStorage.setItem('language', lang);
    location.reload();
}

window.addEventListener('DOMContentLoaded', async () => {
    console.log("b")
    const userPreferredLanguage = localStorage.getItem('language') || 'en';
    const langData = await fetchLanguageData(userPreferredLanguage);
    updateContent(langData);
});

setInterval(() => {
    updatedata()
}, 1000)