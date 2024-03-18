document.addEventListener('DOMContentLoaded', function () {
  configuracionTasaCambio();


  let tasaCambioRow = document.getElementById('tasaCambioRow');
  let inputTasaCambioPago = document.getElementById('inputTasaCambioPago');

  let tipoMonedaPago = document.getElementById('tipoMonedaPago');


  let cantidadPagoCordobasRow = document.getElementById('cantidadPagoCordobasRow');
  let cantidadPagoCordobas = document.getElementById('cantidadPagoCordobas');



  tipoMonedaPago.addEventListener('change', function () {

    if (tipoMonedaPago.value === '2') {
      tasaCambioRow.hidden = false;
      cantidadPagoCordobasRow.hidden = false;
      cantidadPagoCordobas.value = '';
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



