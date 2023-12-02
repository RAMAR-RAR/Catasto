var map = L.map('map').setView([45.4642, 9.19], 13);

// Imposta le dimensioni della mappa
function setMapSize(height, width) {
    map.invalidateSize(); // Aggiorna la dimensione della mappa
    map.getContainer().style.height = height + 'px';
    map.getContainer().style.width = width + 'px';
}

//impostare a piacere la misura per la mappa. se da problemi commentare dallaa riga 4 fino alla riga 11
setMapSize(500, 800);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);