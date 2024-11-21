// localisation system

function updateContent(lang, langData) {
    document.querySelectorAll('[data]').forEach(element => {
        const key = element.getAttribute('data');
        // edge cases
        if (["profile", "profile_s", "profile_vowel"].includes(key) && lang == 'en') {
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
    const userPreferredLanguage = localStorage.getItem('language') || 'fr';
    const langData = await fetchLanguageData(userPreferredLanguage);
    updateContent(userPreferredLanguage, langData);

    // uncheck checkbox by defeault
    const checkbox = document.querySelector('input[type="checkbox"]');
    checkbox.checked = false;
});

function change_username() {
    window.location.replace = "../../change_username"
}

let disconnectBtn = document.querySelector("#disconnect");

disconnectBtn.addEventListener('click', () => {
    document.cookie = `exptoken=${new Date()/1000-1000*60*60*24}`;
    location.reload()
})

function togglePasswordVisibility() {
    const passwordInput = document.getElementById("password");
    const toggleCheckbox = document.getElementById("togglePassword");
    passwordInput.type = toggleCheckbox.checked ? "text" : "password";
}

function togglePasswordConfVisibility() {
    const passwordInput = document.getElementById("confirmation");
    const toggleCheckbox = document.getElementById("togglePasswordConf");
    passwordInput.type = toggleCheckbox.checked ? "text" : "password";
}