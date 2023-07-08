var backdrop = document.querySelector(".backdrop");
var weather_table = document.querySelector(".table-background");
var open_button = document.querySelector(".modal-button");
var search_history = document.querySelector(".search-history-container");
var search_history_btn = document.querySelector(".history-btn");
var location_container = document.querySelector(".top-locations-container");
var location_btn = document.querySelector(".location-btn");
var forgot_psw_link = document.querySelector(".forgot-psw-link");
var forgot_psw_modal = document.querySelector(".forgot-psw-modal");

backdrop.addEventListener("click", function() {
    if (weather_table) {
        weather_table.classList.remove("open");
    }

    if (search_history) {
        search_history.classList.remove("open");
    }

    if (location_container) {
        location_container.classList.remove("open");
    }

    if (forgot_psw_modal) {
        forgot_psw_modal.classList.remove("open");
    }

    closeModal();
});

function closeModal() {
    backdrop.classList.remove("open");
}

function addButtonClickListener(button, container) {
    if (button && container) {
        button.addEventListener("click", function(event) {
            backdrop.classList.add("open");
            container.classList.add("open");
        });
    }
}

addButtonClickListener(open_button, weather_table);
addButtonClickListener(search_history_btn, search_history);
addButtonClickListener(location_btn, location_container);
addButtonClickListener(forgot_psw_link, forgot_psw_modal)