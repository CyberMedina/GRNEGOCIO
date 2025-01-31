const notifications = document.querySelector(".notifications"),
buttons = document.querySelectorAll(".buttons .btn");

const toastDetails = {
    defaultTimer: 5000,
    defaultPosition: 'top-right', // Posición por defecto
    positions: {
        'top-right': 'top-right',
        'top-left': 'top-left',
        'bottom-right': 'bottom-right',
        'bottom-left': 'bottom-left'
    },
    success: {
        icon: 'fa-circle-check',
    },
    error: {
        icon: 'fa-circle-xmark',
    },
    warning: {
        icon: 'fa-triangle-exclamation',
    },
    info: {
        icon: 'fa-circle-info',
    }
}

const removeToast = (toast) => {
    toast.classList.add("hide");
    if(toast.timeoutId) clearTimeout(toast.timeoutId); // Clearing the timeout for the toast
    setTimeout(() => toast.remove(), 500); // Removing the toast after 500ms
}

const createNotificationsContainer = (position = toastDetails.defaultPosition) => {
    const existingContainer = document.querySelector(`.notifications.${position}`);
    if (existingContainer) return existingContainer;

    const notifications = document.createElement('ul');
    notifications.className = `notifications ${position}`;
    document.body.appendChild(notifications);
    return notifications;
}

const createToast = (type, message, timer = toastDetails.defaultTimer, position = toastDetails.defaultPosition) => {
    if (!toastDetails[type]) {
        console.error('Tipo de toast no válido');
        return;
    }

    if (!toastDetails.positions[position]) {
        console.error('Posición no válida');
        position = toastDetails.defaultPosition;
    }

    const notifications = document.querySelector(`.notifications.${position}`) || createNotificationsContainer(position);
    const { icon } = toastDetails[type];
    const toast = document.createElement("li");
    toast.className = `toast ${type}`;
    
    toast.style.setProperty('--progress-time', `${timer}ms`);
    
    toast.innerHTML = `<div class="column">
                         <i class="fa-solid ${icon}"></i>
                         <span>${message}</span>
                      </div>
                      <i class="fa-solid fa-xmark" onclick="removeToast(this.parentElement)"></i>`;
    
    notifications.appendChild(toast);
    toast.timeoutId = setTimeout(() => removeToast(toast), timer);
}

// Nueva función más amigable para mostrar toasts
const showToast = (type, message, timer) => {
    createToast(type, message, timer);
}

// Eliminamos el código de los botones ya que no lo usaremos
buttons.forEach(btn => {
    btn.addEventListener("click", () => createToast(btn.id));
});