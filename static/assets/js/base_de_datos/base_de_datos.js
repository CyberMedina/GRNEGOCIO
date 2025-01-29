const comboTipoGestion = document.getElementById('comboTipoGestion');
const seccionImportar = document.getElementById('seccionImportar');
const seccionExportar = document.getElementById('seccionExportar');
const seccionBackupsAutomaticos = document.getElementById('seccionBackupsAutomaticos');
const spanfechaHoraBackupCreacionBd = document.getElementById('spanfechaHoraBackupCreacionBd');

// Al inicio del archivo, verificar si hay una acción pendiente
document.addEventListener('DOMContentLoaded', function() {
    const pendingAction = localStorage.getItem('pendingBackupAction');
    if (pendingAction) {
        // Limpiar la acción pendiente
        localStorage.removeItem('pendingBackupAction');
        
        // Mostrar el toast
        createToast('success', 'El archivo de respaldo ha sido eliminado correctamente.', 5000, 'bottom-right');
        
        // Abrir el modal y cambiar el select
        const modalThree = new bootstrap.Modal(document.getElementById('ModalThree'));
        modalThree.show();
        
        // Cambiar el valor del select
        const comboTipoGestion = document.getElementById('comboTipoGestion');
        comboTipoGestion.value = 'Exportar';
        // Disparar el evento change manualmente
        comboTipoGestion.dispatchEvent(new Event('change'));
    }
});

// Modificar el event listener del delete
document.addEventListener('click', function(e) {
    // Detectar si el clic fue en un enlace de eliminar
    if (e.target.closest('a[href*="/delete_backup"]')) {
        e.preventDefault();
        const deleteLink = e.target.closest('a');
        
        fetch(deleteLink.href)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Guardar la acción pendiente antes de recargar
                    localStorage.setItem('pendingBackupAction', 'delete_success');
                    // Recargar la página
                    window.location.reload();
                } else {
                    createToast('error', 'No se pudo eliminar el archivo de respaldo.', 5000, 'bottom-right');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                createToast('error', 'Ocurrió un error al eliminar el archivo.', 5000, 'bottom-right');
            });
    }
});

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
    const valor = this.value;
    document.getElementById('seccionExportar').hidden = valor !== 'Exportar';
    document.getElementById('seccionImportar').hidden = valor !== 'Importar/restaurar';
    document.getElementById('seccionBackupsAutomaticos').hidden = valor !== 'Backups automáticos';
});

function iniciarBackup() {
    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById('modalBackupProgress'));
    modal.show();
    
    const progressBar = document.getElementById('backupProgressBar');
    const statusText = document.getElementById('backupStatus');
    
    // Obtener el token de la sesión actual
    const access_token = document.getElementById('access_token').value;
    
    // Conectar al SSE con el token
    const eventSource = new EventSource(`/backup_progress?access_token=${access_token}`);
    
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        // Actualizar barra de progreso
        progressBar.style.width = `${data.progress}%`;
        progressBar.textContent = `${data.progress}%`;
        statusText.textContent = data.status;
        
        // Manejar errores
        if (data.error) {
            progressBar.classList.remove('blue-light-bg');
            progressBar.classList.add('red-bg');
            eventSource.close();
            return;
        }
        
        // Manejar completado
        if (data.completed) {
            eventSource.close();
            setTimeout(() => {
                modal.hide();
                window.location.reload();
            }, 1000);
        }
    };
    
    eventSource.onerror = function() {
        statusText.textContent = "Error de conexión";
        progressBar.classList.remove('blue-light-bg');
        progressBar.classList.add('red-bg');
        eventSource.close();
    };
}

function iniciarRestauracion(fileUrl) {
    const modal = new bootstrap.Modal(document.getElementById('modalBackupProgress'));
    modal.show();
    
    const progressBar = document.getElementById('backupProgressBar');
    const statusText = document.getElementById('backupStatus');
    
    document.querySelector('#modalBackupProgress .modal-header h5').textContent = 'Restaurando base de datos';
    
    // Iniciar el proceso de restauración
    fetch(`/restore_progress?file_url=${encodeURIComponent(fileUrl)}`)
        .then(response => response.json())
        .then(data => {
            if (data.started) {
                // Iniciar polling
                pollRestoreStatus();
            }
        })
        .catch(error => {
            statusText.textContent = "Error al iniciar la restauración";
            progressBar.classList.remove('blue-light-bg');
            progressBar.classList.add('red-bg');
        });
}

function pollRestoreStatus() {
    const progressBar = document.getElementById('backupProgressBar');
    const statusText = document.getElementById('backupStatus');
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalBackupProgress'));
    
    const checkStatus = () => {
        fetch('/restore_status')
            .then(response => response.json())
            .then(data => {
                progressBar.style.width = `${data.progress}%`;
                progressBar.textContent = `${data.progress}%`;
                statusText.textContent = data.status;
                
                if (data.error) {
                    progressBar.classList.remove('blue-light-bg');
                    progressBar.classList.add('red-bg');
                    return;
                }
                
                if (data.completed) {
                    progressBar.classList.remove('blue-light-bg');
                    progressBar.classList.add('green-bg');
                    
                    // Esperar 2 segundos antes de recargar para que el usuario vea el mensaje de éxito
                    setTimeout(() => {
                        modal.hide();
                        createToast('success', '¡Base de datos restaurada exitosamente!', 5000, 'bottom-right');
                        window.location.reload();
                    }, 2000);
                    return;
                }
                
                // Continuar el polling solo si no hay error ni está completado
                setTimeout(checkStatus, 1000);
            })
            .catch(error => {
                console.error('Error:', error);
                statusText.textContent = "Error de conexión";
                progressBar.classList.remove('blue-light-bg');
                progressBar.classList.add('red-bg');
            });
    };
    
    checkStatus();
}

document.getElementById('cargarMasBackups').addEventListener('click', function() {
    const button = this;
    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cargando...';

    fetch('/cargar_historial_backups')
        .then(response => response.json())
        .then(data => {
            const historialContainer = document.getElementById('historial-backups');
            
            data.backups.forEach(backup => {
                const backupHtml = `
                    <div class="kanban-header mb-3" id="backupBaseDeDatos">
                        <div class="kanban-header-members">
                            <div class="add-member-button text-gray">
                                <i class="fa-solid fa-database"></i>
                                Backup del día ${backup.fileDate}
                            </div>
                        </div>
                        <div class="add-task-button">
                            <div class="more-btn-wrapper">
                                <button class="more-btn dropdown-toggle border-0 bg-transparent" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="lni lni-more-alt"></i>
                                </button>
                                <ul class="dropdown-menu dropdown-menu-end px-1">
                                    <li class="dropdown-item">
                                        <a href="#" onclick="iniciarRestauracion('${backup.import_link}'); return false;" class="text-gray text-sm">
                                            <i class="fa-solid fa-file-import"></i>
                                            Importar
                                        </a>
                                    </li>
                                    <li class="dropdown-item">
                                        <a href="${backup.download_link}" target="_blank" class="text-gray text-sm">
                                            <i class="fa-solid fa-download"></i>
                                            Ver / Descargar
                                        </a>
                                    </li>
                                    <li class="dropdown-item">
                                        <a href="${backup.delete_link}" class="text-gray text-sm">
                                            <i class="fa-solid fa-trash"></i>
                                            Eliminar
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                `;
                historialContainer.insertAdjacentHTML('beforeend', backupHtml);
            });

            // Ocultar el botón después de cargar
            button.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            button.innerHTML = '<i class="fa-solid fa-exclamation-triangle"></i> Error al cargar';
        })
        .finally(() => {
            button.disabled = false;
        });
});