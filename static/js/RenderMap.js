let map,
  markers = [],
  infoWindow;

function initMap(locations) {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 12.865416, lng: -85.207229 },
    zoom: 7,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  });
  infoWindow = new google.maps.InfoWindow();
  locations.forEach((location) => addMarker(location));
}

function addMarker(location) {
  let iconUrl =
    location.type === "critical"
      ? "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
      : location.type === "important"
      ? "http://maps.google.com/mapfiles/ms/icons/orange-dot.png"
      : "http://maps.google.com/mapfiles/ms/icons/blue-dot.png";
  const marker = new google.maps.Marker({
    position: location.coords,
    map: map,
    title: location.name,
    icon: { url: iconUrl, scaledSize: new google.maps.Size(32, 32) },
  });
  const contentString = `<div class="custom-info-window"><h3>${
    location.name
  }</h3><p><strong>Tipo:</strong>${
    location.type === "critical"
      ? "Crítica"
      : location.type === "important"
      ? "Importante"
      : "Normal"
  }</p><p><strong>Población:</strong>${location.population}</p><p>${
    location.description
  }</p><button onclick="showLocationDetails(${JSON.stringify(location).replace(
    /"/g,
    "&quot;"
  )})">Ver detalles completos</button></div>`;
  marker.addListener("click", () => {
    infoWindow.setContent(contentString);
    infoWindow.open(map, marker);
    showLocationDetails(location);
  });
  markers.push(marker);
  console.log(`Marcador agregado: ${location.name}`);
}

function showLocationDetails(location) {
  const panel = document.getElementById("infoPanel");
  const content = document.getElementById("panelContent");
  content.innerHTML = `<div class="location-details"><h4>${
    location.name
  }</h4><p><strong>Tipo:</strong>${
    location.type === "critical"
      ? "Crítica"
      : location.type === "important"
      ? "Importante"
      : "Normal"
  }</p><p><strong>Coordenadas:</strong>${location.coords.lat.toFixed(
    6
  )},${location.coords.lng.toFixed(6)}</p><p><strong>Población:</strong>${
    location.population
  }</p><p>${location.description}</p></div>`;
  panel.classList.add("active");
}

document.getElementById("resetView").addEventListener("click", () => {
  map.setCenter({ lat: 12.865416, lng: -85.207229 });
  map.setZoom(7);
});
document
  .getElementById("togglePanel")
  .addEventListener("click", () =>
    document.getElementById("infoPanel").classList.toggle("active")
  );
document
  .querySelector(".close-panel")
  .addEventListener("click", () =>
    document.getElementById("infoPanel").classList.remove("active")
  );
document.getElementById("addMarker").addEventListener("click", () => {
  const center = map.getCenter();
  const newLocation = {
    name: "Nueva Ubicación",
    coords: { lat: center.lat(), lng: center.lng() },
    type: "normal",
    description: "Ubicación agregada por el usuario.",
    population: "Desconocida",
  };
  addMarker(newLocation);
  showLocationDetails(newLocation);
  infoWindow.close();
});

window.gm_authFailure = () =>
  alert("Error al cargar Google Maps. Verifique que la API key sea válida.");
