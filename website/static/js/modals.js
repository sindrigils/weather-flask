var backdrop = document.querySelector(".backdrop");
var weather_table = document.querySelector(".table-background");
var open_button = document.querySelector(".modal-button");


backdrop.addEventListener("click", function() {
    weather_table.classList.remove("open");
    closeModal();
});



function closeModal() {
    backdrop.classList.remove("open");
}

open_button.addEventListener("click", function() {
    backdrop.classList.add("open");
    weather_table.classList.add("open");
});