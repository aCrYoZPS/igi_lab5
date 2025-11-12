function geoFindMe() {
    const latitudeElement = document.querySelector("#latitude");
    const longitudeElement = document.querySelector("#longitude");

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        latitudeElement.textContent = `Latitude: ${latitude} °`;
        longitudeElement.textContent = `Longitude: ${longitude} °`;
    }

    function error(err) {
        latitudeElement.textContent = "Unable to retrieve your location";
        longitudeElement.textContent = "Unable to retrieve your location";
        console.log(err)
    }

    if (!navigator.geolocation) {
        latitudeElement.textContent = "Geolocation is not supported by your browser";
        longitudeElement.textContent = "Geolocation is not supported by your browser";
    } else {
        latitudeElement.textContent = "Locating…";
        longitudeElement.textContent = "Locating…";
        navigator.geolocation.getCurrentPosition(success, error);
    }
}

document.querySelector("#find-me").addEventListener("click", geoFindMe);
