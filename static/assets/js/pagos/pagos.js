




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
        const tasa_interes = data.datos_prestamo[1];

        nombre_cliente.textContent = cliente.nombres + ' ' + cliente.apellidos;
        tipo_cliente.textContent = cliente.nombre_tipoCliente;
        tiempo_pago.textContent = cliente.tiempo_pago;
        fecha_prestamo.textContent = cliente.fechaPrestamo;
        cliente_desde.textContent = cliente.fecha_prestamo_desde;
        tasa_interes_formateada = (Math.trunc(cliente.tasa_interes) + '%');
        tasa_interes.textContent = tasa_interes_formateada;

        inputCapitalDolares.value = cliente.monto_solicitado;
        codigoMonedaCapitalDolares.textContent = cliente.codigoMoneda;

        inputPagoMensualDolares.value = cliente.pagoMensual;
        codigoMonedaPagoMensualDolares.textContent = cliente.codigoMoneda;

        inputPagoQuincenalDolares.value = cliente.pagoQuincenal;
        codigoMonedaPagoQuincenalDolares.textContent = cliente.codigoMoneda;

        inputTasaCambio.value = tasa_interes.cifraTasaCambio;


        conversionMoneda();



        modal = new bootstrap.Modal(document.getElementById('ModalFive'));
        modal.show();
    



    } catch (error) {
        console.error('Error:', error.message);
    }
}


var inputTasaCambio = document.getElementById('inputTasaCambio');

inputTasaCambio.addEventListener('change', function(){
conversionMoneda();

});






var nombre_cliente = document.getElementById('nombre_cliente');
var tipo_cliente = document.getElementById('tipo_cliente');
var tiempo_pago = document.getElementById('tiempo_pago');
var fecha_prestamo = document.getElementById('fecha_prestamo');
var cliente_desde = document.getElementById('cliente_desde');



var inputCapitalDolares = document.getElementById('inputCapitalDolares');
var codigoMonedaCapitalDolares = document.getElementById('codigoMonedaCapitalDolares');
var inputCapitalCordobas = document.getElementById('inputCapitalCordobas');
var codigoMonedaCapitalCordobas = document.getElementById('codigoMonedaCapitalCordobas');

var inputPagoMensualDolares = document.getElementById('inputPagoMensualDolares');
var codigoMonedaPagoMensualDolares = document.getElementById('codigoMonedaPagoMensualDolares');
var tasa_interes = document.getElementById('tasa_interes');
var inputPagoMensualCordobas = document.getElementById('inputPagoMensualCordobas');
var codigoMonedaPagoMensualCordobas = document.getElementById('codigoMonedaPagoMensualCordobas');

var inputPagoQuincenalDolares = document.getElementById('inputPagoQuincenalDolares');
var codigoMonedaPagoQuincenalDolares = document.getElementById('codigoMonedaPagoQuincenalDolares');
var inputPagoQuincenalCordobas = document.getElementById('inputPagoQuincenalCordobas');
var codigoMonedaPagoQuincenalCordobas = document.getElementById('codigoMonedaPagoQuincenalCordobas');


function conversionMoneda() {

    var tasaCambio = inputTasaCambio.value;

    var capitalDolares = inputCapitalDolares.value;
    var pagoMensualDolares = inputPagoMensualDolares.value;
    var pagoQuincenalDolares = inputPagoQuincenalDolares.value;

    inputCapitalCordobas.value = (capitalDolares * tasaCambio).toLocaleString('es-NI', {minimumFractionDigits: 2});
    inputPagoMensualCordobas.value = (pagoMensualDolares * tasaCambio).toLocaleString('es-NI', {minimumFractionDigits: 2});
    inputPagoQuincenalCordobas.value = (pagoQuincenalDolares * tasaCambio).toLocaleString('es-NI', {minimumFractionDigits: 2});
    

}


















