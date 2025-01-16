function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 38.262128, lng: 21.750417 },
        zoom: 13,
    });

    const locations = [
        { lat: 38.262128, lng: 21.750417 },
        { lat: 38.277013, lng: 21.745342 },
        { lat: 38.237902, lng: 21.725841 },
        { lat: 38.290672, lng: 21.780164 },
        { lat: 38.245566, lng: 21.730981 },
        { lat: 38.246877, lng: 21.735854 },
    ];

    locations.forEach(location => {
        new google.maps.Marker({
            position: location,
            map: map,
            icon: {
                url: "https://maps.google.com/mapfiles/kml/shapes/placemark_circle.png",
                scaledSize: new google.maps.Size(20, 20),
            },
        });
    });
}

window.onload = initMap;