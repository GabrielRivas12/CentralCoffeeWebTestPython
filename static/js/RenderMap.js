let map,
  markers = [],
  infoWindow,
  currentUserRole,
  currentMarkerData = {};

function initMap(locations, userRole) {
  console.log("=== DEBUG INICIALIZANDO MAPA ===");
  console.log("Ubicaciones recibidas:", locations);
  console.log("Rol del usuario:", userRole);
  
  currentUserRole = userRole;
  
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 12.865416, lng: -85.207229 },
    zoom: 7,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  });
  infoWindow = new google.maps.InfoWindow();
  
  // Inicializar modal
  initModal();
  
  // Configurar botones según rol
  const addMarkerBtn = document.getElementById('addMarker');
  if (currentUserRole !== 'Administrador') {
    console.log("Usuario NO es administrador, ocultando botón agregar marcador");
    if (addMarkerBtn) {
      addMarkerBtn.style.display = 'none';
    }
  } else {
    console.log("Usuario ES administrador, mostrando botón agregar marcador");
    if (addMarkerBtn) {
      addMarkerBtn.style.display = 'block';
    }
  }
  
  // Agregar marcadores para cada ubicación
  locations.forEach((location) => addMarker(location));
  
  // Verificar si hay un marcador específico que mostrar
  checkForSelectedMarker(locations);
}

function checkForSelectedMarker(locations) {
  // Obtener el ID del marcador seleccionado desde sessionStorage
  const selectedMarkerId = sessionStorage.getItem('selectedMarkerId');
  
  if (selectedMarkerId) {
    console.log("Marcador seleccionado encontrado:", selectedMarkerId);
    
    // Buscar el marcador correspondiente
    const selectedLocation = locations.find(location => location.doc_id === selectedMarkerId);
    
    if (selectedLocation) {
      console.log("Ubicación encontrada:", selectedLocation);
      
      // Centrar el mapa en el marcador seleccionado
      map.setCenter({ 
        lat: selectedLocation.latitud, 
        lng: selectedLocation.longitud 
      });
      map.setZoom(15);
      
      // Encontrar y abrir el infoWindow del marcador seleccionado
      const selectedMarker = markers.find(marker => marker.docId === selectedMarkerId);
      if (selectedMarker) {
        // Simular clic en el marcador para abrir su infoWindow
        google.maps.event.trigger(selectedMarker, 'click');
      }
      
      // Limpiar el sessionStorage después de usar
      setTimeout(() => {
        sessionStorage.removeItem('selectedMarkerId');
      }, 1000);
    } else {
      console.log("No se encontró la ubicación para el ID:", selectedMarkerId);
    }
  }
}

function initModal() {
  const modal = document.getElementById('editModal');
  const closeBtn = document.querySelector('.close');
  const cancelBtn = document.getElementById('cancelEdit');
  const form = document.getElementById('editForm');

  // Abrir modal
  window.openEditModal = function(markerData) {
    currentMarkerData = markerData;
    
    console.log("Abriendo modal con datos:", markerData);
    
    // Llenar el formulario con los datos actuales
    document.getElementById('editDocId').value = markerData.doc_id || '';
    document.getElementById('editUserId').value = markerData.userId || '';
    document.getElementById('editLatitud').value = markerData.latitud || '';
    document.getElementById('editLongitud').value = markerData.longitud || '';
    document.getElementById('editNombre').value = markerData.nombre || '';
    document.getElementById('editDescripcion').value = markerData.descripcion || '';
    
    // Procesar el horario para separar apertura y cierre
    const horario = markerData.horario || '';
    let horaAperturaActual = '08:00';
    let horaCierreActual = '17:00';
    
    if (horario.includes(' - ')) {
      const [apertura, cierre] = horario.split(' - ');
      horaAperturaActual = apertura.trim();
      horaCierreActual = cierre.trim();
    }
    
    // Establecer valores en los inputs
    document.getElementById('editHoraApertura').value = horaAperturaActual;
    document.getElementById('editHoraCierre').value = horaCierreActual;
    
    // Mostrar los horarios actuales
    document.getElementById('currentApertura').textContent = `Actual: ${horaAperturaActual}`;
    document.getElementById('currentCierre').textContent = `Actual: ${horaCierreActual}`;
    
    // Agregar event listeners para mostrar cambios en tiempo real
    document.getElementById('editHoraApertura').addEventListener('change', actualizarHorarioDisplay);
    document.getElementById('editHoraCierre').addEventListener('change', actualizarHorarioDisplay);
    
    modal.style.display = 'block';
  };

  // Función para actualizar la visualización del horario en tiempo real
  function actualizarHorarioDisplay() {
    const horaApertura = document.getElementById('editHoraApertura').value;
    const horaCierre = document.getElementById('editHoraCierre').value;
    
    if (horaApertura) {
      document.getElementById('currentApertura').textContent = `Nuevo: ${horaApertura}`;
      document.getElementById('currentApertura').className = 'horario-new';
    }
    
    if (horaCierre) {
      document.getElementById('currentCierre').textContent = `Nuevo: ${horaCierre}`;
      document.getElementById('currentCierre').className = 'horario-new';
    }
  }

  // Cerrar modal
  function closeModal() {
    modal.style.display = 'none';
    currentMarkerData = {};
    // Limpiar el formulario y resetear displays
    document.getElementById('editForm').reset();
    document.getElementById('currentApertura').textContent = '';
    document.getElementById('currentCierre').textContent = '';
    document.getElementById('currentApertura').className = 'horario-current';
    document.getElementById('currentCierre').className = 'horario-current';
    
    // Remover event listeners
    const horaAperturaInput = document.getElementById('editHoraApertura');
    const horaCierreInput = document.getElementById('editHoraCierre');
    horaAperturaInput.removeEventListener('change', actualizarHorarioDisplay);
    horaCierreInput.removeEventListener('change', actualizarHorarioDisplay);
  }

  // Event listeners para cerrar modal
  closeBtn.addEventListener('click', closeModal);
  cancelBtn.addEventListener('click', closeModal);

  // Cerrar modal al hacer clic fuera
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  // Manejar envío del formulario - PREVENIR DOBLE ENVÍO
  let isSubmitting = false;
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (isSubmitting) {
      console.log("Formulario ya se está enviando, ignorando clic adicional");
      return;
    }
    
    isSubmitting = true;
    
    // Deshabilitar botón para prevenir doble clic
    const submitBtn = form.querySelector('.btn-guardar');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
    submitBtn.disabled = true;
    
    guardarCambiosMarcador()
      .finally(() => {
        // Rehabilitar botón después de completar
        isSubmitting = false;
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      });
  });
}

function addMarker(location) {
  console.log("Agregando marcador:", location);
  
  const marker = new google.maps.Marker({
    position: { 
      lat: location.latitud, 
      lng: location.longitud 
    },
    map: map,
    title: location.nombre
  });
  
  // Almacenar el docId en el marcador para referencia futura
  marker.docId = location.doc_id;
  
  // Construir el contenido del infoWindow según el rol
  let contentString = `
    <div class="custom-info-window">
      <h3>${location.nombre || 'Sin nombre'}</h3>
      <div class="horario">
        <i class="fas fa-clock"></i> ${location.horario || 'Horario no disponible'}
      </div>
      <div class="info-divider"></div>
      <div class="descripcion">
        ${location.descripcion || 'Sin descripción disponible'}
      </div>
  `;
  
  // Agregar botones de administrador si es necesario
  if (currentUserRole === 'Administrador') {
    contentString += `
      <div class="admin-buttons">
        <button class="btn-editar" onclick="openEditModal(${JSON.stringify(location).replace(/"/g, '&quot;')})">
          <i class="fas fa-edit"></i> Editar
        </button>
        <button class="btn-eliminar" onclick="eliminarMarcador('${location.doc_id}', '${location.nombre.replace(/'/g, "\\'")}', this)">
          <i class="fas fa-trash"></i> Eliminar
        </button>
      </div>
    `;
  }
  
  contentString += `</div>`;
  
  marker.addListener("click", () => {
    infoWindow.setContent(contentString);
    infoWindow.open(map, marker);
    
    setTimeout(() => {
      const iwContainer = document.querySelector('.gm-style-iw-c');
      if (iwContainer) {
        iwContainer.style.padding = '0';
        iwContainer.style.maxWidth = '350px';
        iwContainer.style.minWidth = '250px';
      }
    }, 10);
  });
  
  markers.push(marker);
}

// Función para guardar cambios del marcador
async function guardarCambiosMarcador() {
  const docId = document.getElementById('editDocId').value;
  const nombre = document.getElementById('editNombre').value;
  const horaApertura = document.getElementById('editHoraApertura').value;
  const horaCierre = document.getElementById('editHoraCierre').value;
  const descripcion = document.getElementById('editDescripcion').value;
  
  // Formatear el horario
  const horario = `${horaApertura} - ${horaCierre}`;
  
  console.log("Guardando cambios para docId:", docId);
  
  if (!docId) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudo identificar el marcador a actualizar',
      icon: 'error',
      confirmButtonColor: '#e74c3c'
    });
    return;
  }
  
  if (!nombre || !horaApertura || !horaCierre || !descripcion) {
    Swal.fire({
      title: 'Error',
      text: 'Todos los campos son obligatorios',
      icon: 'error',
      confirmButtonColor: '#e74c3c'
    });
    return;
  }
  
  try {
    const response = await fetch(`/api/marcadores/${docId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        nombre: nombre,
        horario: horario,
        descripcion: descripcion
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      // Cerrar modal inmediatamente
      document.getElementById('editModal').style.display = 'none';
      
      Swal.fire({
        title: '¡Éxito!',
        text: result.message,
        icon: 'success',
        confirmButtonColor: '#ED6D4A'
      }).then(() => {
        location.reload();
      });
    } else {
      Swal.fire({
        title: 'Error',
        text: result.error || 'Error al actualizar el marcador',
        icon: 'error',
        confirmButtonColor: '#e74c3c'
      });
    }
  } catch (error) {
    console.error('Error:', error);
    Swal.fire({
      title: 'Error',
      text: 'Error de conexión',
      icon: 'error',
      confirmButtonColor: '#e74c3c'
    });
  }
}

// Función para eliminar marcador - AHORA ES INSTANTÁNEO
async function eliminarMarcador(docId, nombre, buttonElement) {
  if (!docId) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudo identificar el marcador a eliminar',
      icon: 'error',
      confirmButtonColor: '#e74c3c'
    });
    return;
  }

  Swal.fire({
    title: '¿Eliminar marcador?',
    html: `¿Estás seguro de que quieres eliminar <strong>"${nombre}"</strong>?<br><br>Esta acción no se puede deshacer.`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e74c3c',
    cancelButtonColor: '#3498db',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        // Mostrar loading en el botón
        if (buttonElement) {
          const originalHTML = buttonElement.innerHTML;
          buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Eliminando...';
          buttonElement.disabled = true;
        }
        
        const response = await fetch(`/api/marcadores/${docId}`, {
          method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
          // Cerrar el infoWindow
          infoWindow.close();
          
          // Eliminar el marcador del mapa inmediatamente
          eliminarMarcadorDelMapa(docId);
          
          Swal.fire({
            title: '¡Eliminado!',
            text: result.message,
            icon: 'success',
            confirmButtonColor: '#ED6D4A',
            timer: 1500,
            showConfirmButton: false
          });
        } else {
          Swal.fire({
            title: 'Error',
            text: result.error || 'Error al eliminar el marcador',
            icon: 'error',
            confirmButtonColor: '#e74c3c'
          });
          
          // Restaurar botón si hay error
          if (buttonElement) {
            buttonElement.innerHTML = '<i class="fas fa-trash"></i> Eliminar';
            buttonElement.disabled = false;
          }
        }
      } catch (error) {
        console.error('Error:', error);
        Swal.fire({
          title: 'Error',
          text: 'Error de conexión',
          icon: 'error',
          confirmButtonColor: '#e74c3c'
        });
        
        // Restaurar botón si hay error
        if (buttonElement) {
          buttonElement.innerHTML = '<i class="fas fa-trash"></i> Eliminar';
          buttonElement.disabled = false;
        }
      }
    }
  });
}

// Función para eliminar marcador del mapa sin recargar
function eliminarMarcadorDelMapa(docId) {
  // Encontrar el marcador por docId y eliminarlo
  for (let i = markers.length - 1; i >= 0; i--) {
    const marker = markers[i];
    if (marker.docId === docId) {
      marker.setMap(null); // Eliminar del mapa
      markers.splice(i, 1); // Eliminar del array
      break;
    }
  }
}

// Función para agregar nuevo marcador
async function agregarNuevoMarcador(locationData) {
  try {
    const response = await fetch('/api/marcadores', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(locationData)
    });
    
    const result = await response.json();
    
    if (result.success) {
      Swal.fire({
        title: '¡Éxito!',
        text: result.message,
        icon: 'success',
        confirmButtonColor: '#ED6D4A'
      }).then(() => {
        location.reload();
      });
    } else {
      Swal.fire({
        title: 'Error',
        text: result.error || 'Error al crear el marcador',
        icon: 'error',
        confirmButtonColor: '#e74c3c'
      });
    }
  } catch (error) {
    console.error('Error:', error);
    Swal.fire({
      title: 'Error',
      text: 'Error de conexión',
      icon: 'error',
      confirmButtonColor: '#e74c3c'
    });
  }
}

// Event listeners
document.getElementById("resetView").addEventListener("click", () => {
  map.setCenter({ lat: 12.865416, lng: -85.207229 });
  map.setZoom(7);
});

// Agregar nuevo marcador - DISEÑO CORREGIDO
const addMarkerBtn = document.getElementById("addMarker");
if (addMarkerBtn) {
  addMarkerBtn.addEventListener("click", () => {
    const center = map.getCenter();
    
    // Crear el contenido HTML personalizado para el modal de agregar
    const addMarkerHTML = `
      <div class="custom-swal-content">
        <div class="custom-form-group">
          <label for="swal-nombre">Nombre del lugar:</label>
          <input type="text" id="swal-nombre" placeholder="Ingresa el nombre del lugar" required>
        </div>
        
        <div class="custom-horario-section">
          <span class="section-title">Horario de atención:</span>
          <div class="custom-horario-selector">
            <div class="custom-time-group">
              <label>Hora de apertura:</label>
              <input type="time" id="swal-hora-apertura" value="08:00" required>
            </div>
            <div class="custom-time-separator">-</div>
            <div class="custom-time-group">
              <label>Hora de cierre:</label>
              <input type="time" id="swal-hora-cierre" value="17:00" required>
            </div>
          </div>
        </div>
        
        <div class="custom-form-group">
          <label for="swal-descripcion">Descripción:</label>
          <textarea id="swal-descripcion" placeholder="Describe el lugar, servicios que ofrece, etc." rows="4" required></textarea>
        </div>
      </div>
    `;
    
    Swal.fire({
      title: 'Agregar Nuevo Marcador',
      html: addMarkerHTML,
      width: '500px',
      showCancelButton: true,
      confirmButtonText: 'Agregar Marcador',
      cancelButtonText: 'Cancelar',
      confirmButtonColor: '#ED6D4A',
      cancelButtonColor: '#95a5a6',
      reverseButtons: true,
      focusConfirm: false,
      customClass: {
        popup: 'custom-swal',
        title: 'custom-swal-title',
        htmlContainer: 'custom-swal-content'
      },
      didOpen: () => {
        // Aplicar estilos a los inputs después de que se abra el modal
        const inputs = document.querySelectorAll('#swal-nombre, #swal-hora-apertura, #swal-hora-cierre, #swal-descripcion');
        inputs.forEach(input => {
          input.style.width = '100%';
          input.style.padding = '10px 12px';
          input.style.border = '2px solid #ddd';
          input.style.borderRadius = '6px';
          input.style.fontSize = '1rem';
          input.style.boxSizing = 'border-box';
          input.style.fontFamily = 'Arial, sans-serif';
        });
        
        // Estilo específico para el textarea
        const textarea = document.getElementById('swal-descripcion');
        if (textarea) {
          textarea.style.minHeight = '100px';
          textarea.style.resize = 'vertical';
        }
        
        // Enfocar el primer input
        document.getElementById('swal-nombre').focus();
      },
      preConfirm: () => {
        const nombre = document.getElementById('swal-nombre').value;
        const horaApertura = document.getElementById('swal-hora-apertura').value;
        const horaCierre = document.getElementById('swal-hora-cierre').value;
        const descripcion = document.getElementById('swal-descripcion').value;
        
        if (!nombre || !horaApertura || !horaCierre || !descripcion) {
          Swal.showValidationMessage('Por favor, completa todos los campos');
          return false;
        }
        
        if (horaApertura >= horaCierre) {
          Swal.showValidationMessage('La hora de apertura debe ser anterior a la hora de cierre');
          return false;
        }
        
        return { 
          nombre: nombre.trim(),
          horaApertura: horaApertura,
          horaCierre: horaCierre,
          descripcion: descripcion.trim()
        };
      }
    }).then((result) => {
      if (result.isConfirmed) {
        const horario = `${result.value.horaApertura} - ${result.value.horaCierre}`;
        
        const newLocation = {
          nombre: result.value.nombre,
          latitud: center.lat(),
          longitud: center.lng(),
          horario: horario,
          descripcion: result.value.descripcion
        };
        
        agregarNuevoMarcador(newLocation);
        infoWindow.close();
      }
    });
  });
}

window.gm_authFailure = () =>
  alert("Error al cargar Google Maps. Verifique que la API key sea válida.");