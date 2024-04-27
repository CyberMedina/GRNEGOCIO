

let inicioFechaImpresion = document.getElementById('inicioFechaImpresion');
let finFechaImpresion = document.getElementById('finFechaImpresion');


document.addEventListener('DOMContentLoaded', function () {

    // Obtenemos el año actual para mostrarlo en el input de fecha de inicio de impresión
    let currentYear = new Date().getFullYear();
    // Asignamos el año actual al input de fecha de inicio de impresión
    inicioFechaImpresion.value = `${currentYear}-01-01`;

    // Asignamos la fecha actual al input de fecha de fin de impresión
    finFechaImpresion.value = new Date().toISOString().slice(0, 10);



});


function abrirModalOpcionImprimir() {

    let ModalOpcionImprimir = document.getElementById('ModalOpcionImprimir');

    labelMostrarQuincenaActualLetras();


    ModalOpcionImprimir = new bootstrap.Modal(ModalOpcionImprimir);

    ModalOpcionImprimir.show();
}

inicioFechaImpresion.addEventListener('change', function () {

    labelMostrarQuincenaActualLetras();

});

finFechaImpresion.addEventListener('change', function () {

    labelMostrarQuincenaActualLetras();



});


// Función para cambiar mostrar la quincena en letras en los labels de la ventana modal
function labelMostrarQuincenaActualLetras() {
    tiempoLetrasFinFechaImpresion.innerHTML = fechaLetrasfuncion(finFechaImpresion.value);
    tiempoLetrasInicioFechaImpresion.innerHTML = fechaLetrasfuncion(inicioFechaImpresion.value);
}




function fechaLetrasfuncion(fechaPagoValue) {


    const [year, month, day] = fechaPagoValue.split('-');

    const fechaPago = new Date(year, month - 1, day);


    const meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];
    const nombreMes = meses[parseInt(month, 10) - 1]; // Restamos 1 porque los índices de los arrays empiezan en 0

    primeraSegundaQuincena = "";

    PrimeraQuincena = 15;
    SegundaQuincena = 30;

    if (fechaPago.getDate() <= 15) {

        primeraSegundaQuincena = "Primera quincena de " + nombreMes + " de " + year;

    }

    else if (fechaPago.getDate() > 15) {

        primeraSegundaQuincena = "Segunda quincena de " + nombreMes + " de " + year;
    }

    return primeraSegundaQuincena;

}



function enviar_datos_imprimir_backend() {

    let fechaInicio = inicioFechaImpresion.value;
    let fechaFin = finFechaImpresion.value;
    let formId_cliente = document.getElementById('formId_cliente');
    let id_cliente = formId_cliente.value;

    let datos = {
        fechaInicio: fechaInicio,
        fechaFin: fechaFin,
        id_cliente: id_cliente
    };




    fetch('/Imprimir_pago', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
      },
    body: JSON.stringify(datos)
})
    .then(response => response.text()) // Cambiado a text() para obtener la respuesta como HTML
    .then(data => {
        console.log(data);

        if (data) {
            var newWindow = window.open("", "_blank"); // Abre una nueva ventana
            newWindow.document.write(data); // Escribe el contenido HTML en la nueva ventana
            newWindow.document.close(); // Cierra el documento para que se cargue en la ventana
        } else {
            alert('No se encontraron pagos en el rango de fechas seleccionado');
        }
    })
    .catch(error => {
        console.log(error);
    });

}
