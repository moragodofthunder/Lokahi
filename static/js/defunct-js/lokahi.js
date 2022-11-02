'use strict';

const logoutBtn = document.querySelector("#log-out");

logoutBtn.addEventListener('click', () => 
    fetch(("/logout", {
        method: "GET"
    }))
)