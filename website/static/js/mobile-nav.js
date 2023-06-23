var backdrop = document.querySelector(".backdrop");
var toogleButton = document.querySelector(".toggle-button");
var mobileNav = document.querySelector(".mobile-nav");

backdrop.addEventListener("click", function() {
    mobileNav.classList.remove("open");
    closeModal();
});


function closeModal() {

    backdrop.classList.remove("open");
}
  

toogleButton.addEventListener("click", function() {
    backdrop.classList.add("open");
    mobileNav.classList.add("open");
    
});

