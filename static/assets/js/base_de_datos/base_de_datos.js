const comboTipoGestion = document.getElementById('comboTipoGestion');
const seccionImportar = document.getElementById('seccionImportar');
const seccionExportar = document.getElementById('seccionExportar');
const seccionBackupsAutomaticos = document.getElementById('seccionBackupsAutomaticos');
const spanfechaHoraBackupCreacionBd = document.getElementById('spanfechaHoraBackupCreacionBd');




// document.addEventListener('DOMContentLoaded', () => {
//     const spanfechaHoraBackupCreacionBd = document.getElementById('spanfechaHoraBackupCreacionBd');
//     const downloadButton = document.getElementById('a_descargarBackup');

//     fetch('/obtener_datos_ultimo_backup')
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
//             spanfechaHoraBackupCreacionBd.textContent = data.backup.fechaHora;

//             // Agregar URL y nombre del archivo como atributos data-* en el botón
//             downloadButton.setAttribute('data-url', data.backup.ruta_backup);
//             downloadButton.setAttribute('data-filename', data.backup.nombre_backup);
//         })
//         .catch(error => console.error('Error:', error));

//     downloadButton.addEventListener('click', () => {
//         const url = downloadButton.getAttribute('data-url');
//         const filename = downloadButton.getAttribute('data-filename');

//         if (url && filename) {
//             // Crear un enlace temporal
//             const tempLink = document.createElement('a');
//             tempLink.href = url;
//             tempLink.download = filename;
//             tempLink.style.display = 'none';

//             // Agregar el enlace temporal al cuerpo del documento
//             document.body.appendChild(tempLink);

//             // Simular clic en el enlace
//             tempLink.click();

//             // Eliminar el enlace temporal
//             document.body.removeChild(tempLink);
//         } else {
//             console.error('URL o nombre de archivo no están definidos');
//         }
//     });
// });


comboTipoGestion.addEventListener('change', function() {

    if (comboTipoGestion.value === 'Importar/restaurar') {
        seccionImportar.hidden = false;
    } else {
        seccionImportar.hidden = true;
    }

    if (comboTipoGestion.value === 'Exportar') {
        seccionExportar.hidden = false;
    } else {
        seccionExportar.hidden = true;
    }

    if (comboTipoGestion.value === 'Backups automáticos') {
        seccionBackupsAutomaticos.hidden = false;
    } else {
        seccionBackupsAutomaticos.hidden = true;
    }




});