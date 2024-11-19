function updatedata() {
    fetch("/data?"+window.location.search.split("?")[1])
    .then(res => res.json())
    .then(data => document.querySelector("#time").innerText = data["time"])
}

// localisation system

function updateContent(lang, langData) {
    document.querySelectorAll('[data]').forEach(element => {
        const key = element.getAttribute('data');
        // edge cases
        if (key == "profile" && lang == 'en') {
            element.innerHTML = element.innerHTML + langData[key];
        }
        else {
            element.innerHTML = langData[key] + element.innerHTML;
        }
    });
}

async function fetchLanguageData(lang) {
    const response = await fetch(`/static/lang/${lang}.json`);
    return response.json();
}

async function changeLanguage(lang) {
    await setLanguagePreference(lang);
    
    const langData = await fetchLanguageData(lang);
    updateContent(lang, langData);
}

function setLanguagePreference(lang) {
    localStorage.setItem('language', lang);
    location.reload();
}

window.addEventListener('DOMContentLoaded', async () => {
    const userPreferredLanguage = localStorage.getItem('language') || 'en';
    const langData = await fetchLanguageData(userPreferredLanguage);
    updateContent(userPreferredLanguage, langData);
});

let disconnectBtn = document.querySelector("#disconnect");

disconnectBtn.addEventListener('click', () => {
    document.cookie = `exptoken=${new Date()/1000-1000*60*60*24}`;
    location.reload()
})

setInterval(() => {
    updatedata()
}, 1000)