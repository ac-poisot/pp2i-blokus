// localisation system

function updateContent(lang, langData) {
    document.querySelectorAll('[data]').forEach(element => {
        const key = element.getAttribute('data');
        // edge cases
        if ((["profile", "profile_s", "profile_vowel"].includes(key) && lang == 'en') || key == "victory") {
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
});

function change_username() {
    window.location.replace = "../../change_username"
}

function deleteCookies() {
    document.cookie = `exptoken=${new Date()/1000-1000*60*60*24}; path=/`;
    location.reload()
}

function togglePasswordVisibility() {
    const passwordInput = document.getElementById("password");
    const toggleCheckbox = document.getElementById("togglePassword");
    const toggleImage = document.getElementById("toggleImage");
    passwordInput.type = toggleCheckbox.checked ? "text" : "password";
    if (toggleCheckbox.checked) {
        toggleImage.src = "/static/images/cacher.png"; 
    } else {
        toggleImage.src = "/static/images/oeil.png";
    }
}

function togglePasswordConfVisibility() {
    const passwordInput = document.getElementById("confirmation");
    const toggleCheckbox = document.getElementById("togglePasswordConf");
    const toggleImage = document.getElementById("toggleImageConf");
    passwordInput.type = toggleCheckbox.checked ? "text" : "password";
    if (toggleCheckbox.checked) {
        toggleImage.src = "/static/images/cacher.png"; 
    } else {
        toggleImage.src = "/static/images/oeil.png";
    }
}


function openMenuL() {
    console.log(document.getElementById("menu").offsetHeight)
    if (document.getElementById("menu").offsetHeight == 0) {
        document.getElementById("menu").style.height = "14vh";
    }
    else {
        document.getElementById("menu").style.height = "0vh";
    }
}

