var inputTasaCambioPago = document.getElementById('inputTasaCambioPago');

var cantidadPagarVerificarC$ = document.getElementById('cantidadPagarVerificarC$');


let cantidadPagarVerificar$ = document.getElementById('cantidadPagarVerificar$');
let cantidadPagar$ = document.getElementById('cantidadPagar$');
let cantidadPagoCordobas = document.getElementById('cantidadPagoCordobas');
let fechaPago = document.getElementById('fechaPago');
let tiempoPagoLetras = document.getElementById('tiempoPagoLetras');
let pagoCompleto = document.getElementById('pagoCompleto');


function calculoDolaresCordobas() {

  let cantidadPagarVerificarC$ = document.getElementById('cantidadPagarVerificarC$');
  let lblCantidadPagarC$ = document.getElementById('lblCantidadPagarC$');
  let inputTasaCambioPago = document.getElementById('inputTasaCambioPago');

  let cantidadPagarVerificar$ = document.getElementById('cantidadPagarVerificar$');

  console.log('cantidadPagarVerificar$:', cantidadPagarVerificar$.value);

  let cantidadPagarCordobas = (cantidadPagarVerificar$.value * inputTasaCambioPago.value);

  cantidadPagarVerificarC$.value = cantidadPagarCordobas.toFixed(2);
  lblCantidadPagarC$.textContent = cantidadPagarCordobas.toFixed(2);

}

function calculoCordobasDoalres() {

}

document.addEventListener('DOMContentLoaded', function () {
  configuracionTasaCambio();




  let tasaCambioRow = document.getElementById('tasaCambioRow');
  let inputTasaCambioPago = document.getElementById('inputTasaCambioPago');

  let tipoMonedaPago = document.getElementById('tipoMonedaPago');


  let cantidadPagoCordobasRow = document.getElementById('cantidadPagoCordobasRow');
  let cantidadPagoCordobas = document.getElementById('cantidadPagoCordobas');


  inputTasaCambioPago.addEventListener('input', function () {

    cantidadPagoCordobas.value = '';
    cantidadPagar$.value = '';

    calculoDolaresCordobas();

  });



  tipoMonedaPago.addEventListener('change', function () {

    if (tipoMonedaPago.value === '2') {
      tasaCambioRow.hidden = false;
      cantidadPagoCordobasRow.hidden = false;
      cantidadPagoCordobas.value = '';
      cantidadPagar$.value = '';
      calculoDolaresCordobas();
    } else {
      tasaCambioRow.hidden = true;
      cantidadPagoCordobasRow.hidden = true;
      cantidadPagoCordobas.value = '';
    }

  });

});


function configuracionTasaCambio() {


  let inputTasaCambio = document.getElementById('inputTasaCambioPago');

  // Crea una función asincrona que mediante fetch haga una peticion de una url de mi backend para luego de recibirla haga una cosa u otra

  try {
    async function obtenerTasaCambio() {
      let response = await fetch('/obtener_tasa_cambio');
      let data = await response.json();
      return data;
    }

    obtenerTasaCambio().then(data => {
      console.log('data:', data);
      if (data.tasa_cambio.cifraTasaCambio === "0.00") {
        inputTasaCambio.placeholder = 'Inserte tasa de cambio por favor';
        inputTasaCambio.value = '';
      } else {

        inputTasaCambio.value = data.tasa_cambio.cifraTasaCambio;
      }
    }
    );
  }
  catch (error) {
    console.error('Error:', error.message);
  }



}


function fechaLetras(event) {
  var fechaPagoValue = document.getElementById('fechaPago').value;


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

  console.log(primeraSegundaQuincena);





  tiempoPagoLetras.innerText = primeraSegundaQuincena;

}

function validacionDolares(event) {
  let value = event.target.value.replace(/\D/g, '');
  value = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value / 100);
  event.target.value = value;

  // haz que el estilo de cantidadPagar$ sea en rojo si no menor al valor de cantidadPagarVerificar$ y en verde si es mayor
  if (parseFloat(cantidadPagar$.value.replace(/\D/g, '')) < parseFloat(cantidadPagarVerificar$.value.replace(/\D/g, ''))) {
    cantidadPagar$.style.color = 'red';
  } else {
    cantidadPagar$.style.color = 'green';
  }
}

// crea un evento para cantidadPagar$ para que ponga las , en los miles automaticamente al escribir, y respete los decimales que en este caso son puntos además de opnerle el signo de dolar aumaticamente
cantidadPagar$.addEventListener('input', function (event) {
  validacionDolares(event);
});


cantidadPagoCordobas.addEventListener('input', function () {
  let value = this.value.replace(/\D/g, '');
  value = new Intl.NumberFormat('es-NI', {
    style: 'currency',
    currency: 'NIO'
  }).format(value / 100);
  this.value = value;

  // haz que el estilo de cantidadPagar$ sea en rojo si no menor al valor de cantidadPagarVerificar$ y en verde si es mayor
  if (parseFloat(cantidadPagoCordobas.value.replace(/\D/g, '')) < parseFloat(cantidadPagarVerificarC$.value.replace(/\D/g, ''))) {
    cantidadPagoCordobas.style.color = 'red';
  } else {
    cantidadPagoCordobas.style.color = 'green';
  }

  let valorNumerico = parseFloat(cantidadPagoCordobas.value.replace(/[^0-9.]/g, ''));
  console.log('valorNumerico:', valorNumerico);

  conversionCordobasDolares = (valorNumerico / inputTasaCambioPago.value).toFixed(2);
  console.log('conversionCordobasDolares:', conversionCordobasDolares);
  cantidadPagar$.value = conversionCordobasDolares;

  // llama a validacionDolares manualmente
  validacionDolares({ target: cantidadPagar$ });

});

fechaPago.addEventListener('input', function (event) {

  fechaLetras(event);

  
});


pagoCompleto.addEventListener('click', function () {

  calculoDolaresCordobas();

  cantidadPagar$.value = cantidadPagarVerificar$.value;

  // llama a validacionDolares manualmente
  validacionDolares({ target: cantidadPagar$ });

  let fechaActual = new Date();
  let dia = String(fechaActual.getDate()).padStart(2, '0');
  let mes = String(fechaActual.getMonth() + 1).padStart(2, '0'); // Enero es 0
  let anio = fechaActual.getFullYear();

  let fechaFormateada = anio + '-' + mes + '-' + dia;

  fechaPago.value = fechaFormateada;
    // llama a validacionDolares manualmente
  fechaLetras({ target: fechaPago });

});











