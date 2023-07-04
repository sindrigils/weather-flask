var backdrop = document.querySelector(".backdrop");
var weather_table = document.querySelector(".table-background");
var open_button = document.querySelector(".modal-button");
var search_history = document.querySelector(".search-history-container");
var search_history_btn = document.querySelector(".history-btn");
var location_container = document.querySelector(".top-locations-container");
var location_btn = document.querySelector(".location-btn");

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

    closeModal();
});

function closeModal() {
    backdrop.classList.remove("open");
}

function addButtonClickListener(button, container) {
    if (button && container) {
        button.addEventListener("click", function() {
            backdrop.classList.add("open");
            container.classList.add("open");
        });
    }
}

addButtonClickListener(open_button, weather_table);
addButtonClickListener(search_history_btn, search_history);
addButtonClickListener(location_btn, location_container);
