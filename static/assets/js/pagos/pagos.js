




async function ver_datosClientes(id_cliente) {





    console.log('id_cliente: ', id_cliente);


    try {
        const response = await fetch('/datos_prestamoV1', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id_cliente: id_cliente })
        });

        if (!response.ok) {
            throw new Error('Error al obtener los datos del cliente');
        }

        const data = await response.json();
        console.log(data);

        const cliente = data.datos_prestamo[0];
        const tasa_cambio = data.datos_prestamo[1];



        nombre_cliente.forEach((elemento) => {
            elemento.textContent = cliente.nombres + ' ' + cliente.apellidos;
        });
        tiempo_pago.forEach((elemento) => {
            elemento.textContent = cliente.tiempo_pago;
        });
        fecha_prestamo.forEach((elemento) => {
            elemento.textContent = cliente.fechaPrestamo;
        });
        cliente_desde.forEach((elemento) => {
            elemento.textContent = cliente.fecha_prestamo_desde;
        });
        tasa_interes_formateada = (Math.trunc(cliente.tasa_interes) + '%');
        tasa_interes.forEach((elemento) => {
            elemento.textContent = tasa_interes_formateada;
        });

        inputCapitalDolares.value = cliente.monto_solicitado;
        codigoMonedaCapitalDolares.textContent = cliente.codigoMoneda;

        inputPagoMensualDolares.value = cliente.pagoMensual;
        codigoMonedaPagoMensualDolares.textContent = cliente.codigoMoneda;

        inputPagoQuincenalDolares.value = cliente.pagoQuincenal;
        codigoMonedaPagoQuincenalDolares.textContent = cliente.codigoMoneda;

        inputTasaCambio.value = tasa_cambio.cifraTasaCambio;

        gestionarPago.href = '/añadir_pago/' + cliente.id_cliente;


        if (data.datos_prestamo[2] === undefined) {
            ultimoPago.textContent = 'No se ha realizado ningún pago.';
        } else {

            const pagos = data.datos_prestamo[2];

            ultimoPago.textContent = 'Último pago realizado en la ' + pagos.fecha_ultimo_pago_letras + ' (' + pagos.fecha_utlimo_pago_formateado + ')' + ' con un monto de $' + pagos.cifra_ultimo_pagoDolares + ' dólares, ' + ' en cordobas es C$' + pagos.cifra_ultimo_pagoCordobas;
        }

        conversionMoneda();



        modal = new bootstrap.Modal(document.getElementById('ModalDetalleCliente'));
        modal.show();

        console.log('Datos del cliente:', cliente);




    } catch (error) {
        console.error('Error:', error.message);
    }
}


var inputTasaCambio = document.getElementById('inputTasaCambio');

inputTasaCambio.addEventListener('change', function () {
    conversionMoneda();

});






var nombre_cliente = document.querySelectorAll('#nombre_cliente');
// var tipo_cliente = document.getElementById('tipo_cliente');
var tiempo_pago = document.querySelectorAll('#tiempo_pago');
var fecha_prestamo = document.querySelectorAll('#fecha_prestamo');
var cliente_desde = document.querySelectorAll('#cliente_desde');
var gestionarPago = document.getElementById('gestionarPago');


var inputCapitalDolares = document.getElementById('inputCapitalDolares');
var codigoMonedaCapitalDolares = document.getElementById('codigoMonedaCapitalDolares');
var inputCapitalCordobas = document.getElementById('inputCapitalCordobas');
var codigoMonedaCapitalCordobas = document.getElementById('codigoMonedaCapitalCordobas');

var inputPagoMensualDolares = document.getElementById('inputPagoMensualDolares');
var capitalDolaresText = document.getElementById('capitalDolares');
var codigoMonedaPagoMensualDolares = document.getElementById('codigoMonedaPagoMensualDolares');
var tasa_interes = document.querySelectorAll('tasa_interes');
var inputPagoMensualCordobas = document.getElementById('inputPagoMensualCordobas');
var codigoMonedaPagoMensualCordobas = document.getElementById('codigoMonedaPagoMensualCordobas');
var pagoMensualDolaresText = document.getElementById('pagoMensualDolaresText');
var PagoQuincenalDolaresText = document.getElementById('PagoQuincenalDolaresText');

var capitalCordobasText = document.getElementById('capitalCordobas');
var inputPagoQuincenalDolares = document.getElementById('inputPagoQuincenalDolares');
var codigoMonedaPagoQuincenalDolares = document.getElementById('codigoMonedaPagoQuincenalDolares');
var inputPagoQuincenalCordobas = document.getElementById('inputPagoQuincenalCordobas');
var codigoMonedaPagoQuincenalCordobas = document.getElementById('codigoMonedaPagoQuincenalCordobas');
var pagoMensualCordobasText = document.getElementById('pagoMensualCordobasText');
var PagoQuincenalCordobasText = document.getElementById('PagoQuincenalCordobasText');

var ultimoPago = document.getElementById('ultimoPago');





function conversionMoneda() {

    var tasaCambio = inputTasaCambio.value;

    var capitalDolares = inputCapitalDolares.value;
    var pagoMensualDolares = inputPagoMensualDolares.value;
    var pagoQuincenalDolares = inputPagoQuincenalDolares.value;

    inputCapitalCordobas.value = (capitalDolares * tasaCambio).toLocaleString('es-NI', { minimumFractionDigits: 2 });
    inputPagoMensualCordobas.value = (pagoMensualDolares * tasaCambio).toLocaleString('es-NI', { minimumFractionDigits: 2 });
    inputPagoQuincenalCordobas.value = (pagoQuincenalDolares * tasaCambio).toLocaleString('es-NI', { minimumFractionDigits: 2 });

    cifraDolares = capitalDolares.toLocaleString('es-NI', { minimumFractionDigits: 2 });

    capitalDolaresText.textContent = '$ ' + cifraDolares;

    pagoMensualDolaresText.textContent = '$ ' + pagoMensualDolares.toLocaleString('es-NI', { minimumFractionDigits: 2 });

    PagoQuincenalDolaresText.textContent = '$ ' + pagoQuincenalDolares.toLocaleString('es-NI', { minimumFractionDigits: 2 });

    capitalCordobasText.textContent = 'C$ ' + (capitalDolares * tasaCambio).toLocaleString('es-NI', { minimumFractionDigits: 2 });
    pagoMensualCordobasText.textContent = 'C$ ' + (pagoMensualDolares * tasaCambio).toLocaleString('es-NI', { minimumFractionDigits: 2 });
    PagoQuincenalCordobasText.textContent = 'C$ ' + (pagoQuincenalDolares * tasaCambio).toLocaleString('es-NI', { minimumFractionDigits: 2 });





}

// Agregar un listener al evento change del input

document.getElementById("filtro-comboBox").addEventListener("change", function () {
    const selectedValue = this.value; // Valor seleccionado en el combobox
    // Enviar una solicitud POST al servidor con el valor seleccionado
    // Puedes usar fetch o axios para hacer la solicitud
    // Ejemplo:
    console.log('Valor seleccionado:', selectedValue)
    fetch("/guardar_en_sesion_ordenar_clientesPrestamos", {
        method: "POST",
        body: JSON.stringify({ selectedValue }), // Convertir a JSON
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log("Valor guardado en sesión:", data);
            location.reload();
        })
        .catch(error => {
            console.error("Error al guardar en sesión:", error);
        });
});

const fileInput = document.querySelector('input[type="file"]');

fileInput.addEventListener('change', function (event) {

    // Definiendo los tipos de imagenes permitidos
    var types = ['image/png', 'image/jpeg', 'image/gif'];

    // Obtener el archivo
    var file = fileInput.files[0];
    // Obtener el tamaño del archivo en bytes
    var size = file.size;

    var type = file.type;

    // Definir el límite en bytes (5 MB = 5 * 1024 * 1024)
    var limit = 5 * 1024 * 1024;
    // Comparar el tamaño con el límite


    if (!types.includes(type)) {
        // Mostrar un mensaje de error
        alert("El archivo no es una imagen.");
        // Limpiar el valor del input
        fileInput.value = "";
    }

    else if (size > limit) {
        // Mostrar un mensaje de error
        alert("El archivo es demasiado grande. El tamaño máximo es 5 MB.");
        // Limpiar el valor del input
        fileInput.value = "";
    }


    else if (fileInput.files.length === 0) {

        // Mostrar un mensaje de error
        alert("No se seleccionó ningún archivo.");
        // Limpiar el valor del input
        fileInput.value = "";
    }


    // Obtén los elementos del formulario
    const formulario = document.getElementById("anadirClientes");
    const btnGuardar = document.getElementById("btnGuardar");

    // Escucha el evento "input" en los campos requeridos
    formulario.addEventListener("input", () => {
        // Verifica si todos los campos requeridos están completados
        const camposCompletados = Array.from(formulario.elements).every(
            (elemento) => elemento.required ? elemento.value.trim() !== "" : true
        );

        // Habilita o deshabilita el botón según los campos completados
        btnGuardar.disabled = !camposCompletados;
    });





});





















