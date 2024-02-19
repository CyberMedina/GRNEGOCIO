// Crear una función para subir imágenes a Cloudinary
function subirImagen(input, preset) {
    // Configurar el nombre de la nube
    var cloudName = 'dcfrtfw8x';
    // Crear un formData para enviar el archivo
    var formData = new FormData();
    formData.append('file', input.files[0]);
    formData.append('upload_preset', preset);
    // Retornar una promesa con la URL del archivo subido
    return new Promise(function(resolve, reject) {
      // Hacer una petición POST a la API de Cloudinary
      fetch(`https://api.cloudinary.com/v1_1/${cloudName}/upload`, {
        method: 'POST',
        body: formData
      })
      .then(function(response) {
        return response.json();
      })
      .then(function(result) {
        // Obtener la URL del archivo subido
        var url = result.secure_url;
        // Resolver la promesa con la URL
        resolve(url);
      })
      .catch(function(error) {
        // Rechazar la promesa con el error
        reject(error);
      });
    });
  }
  