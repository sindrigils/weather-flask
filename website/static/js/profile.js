document.querySelector(".upload-icon-button").addEventListener("click", function() {
  document.getElementById("profile-pic-input").click();
});

document.getElementById("profile-pic-input").addEventListener("change", function() {
  document.getElementById("profile-pic-form").submit();
});