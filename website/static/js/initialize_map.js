function initMap() {
    const scriptTag = document.querySelector('script[data-lat][data-lng]');
    const latitude = parseFloat(scriptTag.getAttribute('data-lat'));
    const longitude = parseFloat(scriptTag.getAttribute('data-lng'));
    
    var options = {
        center: {lat: latitude, lng: longitude},
        zoom: 15
    }

    map = new google.maps.Map(document.getElementById("map"), options)
}