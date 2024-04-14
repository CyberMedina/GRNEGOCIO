var inputTasaCambioPago = document.getElementById('inputTasaCambioPago');

var cantidadPagarVerificarC$ = document.getElementById('cantidadPagarVerificarC$');


let cantidadPagarVerificar$ = document.getElementById('cantidadPagarVerificar$');
let pCantidadPagarVerificar$ = document.getElementById('pCantidadPagarVerificar$');
let cantidadPagar$ = document.getElementById('cantidadPagar$');
let cantidadPagoCordobas = document.getElementById('cantidadPagoCordobas');
let fechaPago = document.getElementById('fechaPago');
let tiempoPagoLetras = document.getElementById('tiempoPagoLetras');
let pagoCompleto = document.getElementById('pagoCompleto');
let comboSugerenciaPago = document.getElementById('comboSugerenciaPago');
let formId_cliente = document.getElementById('formId_cliente');
let tipoPagoCompleto = document.getElementById('tipoPagoCompleto');

// Sección para detalle cliente
let detallesCliente = document.getElementById('detallesCliente');
let btnMostrarDetallesCliente = document.getElementById('btnMostrarDetallesCliente');
let btnOcultarDetallesCliente = document.getElementById('btnOcultarDetallesCliente');



function calculoDolaresCordobas() {

  let cantidadPagarVerificarC$ = document.getElementById('cantidadPagarVerificarC$');
  let lblCantidadPagarC$ = document.getElementById('lblCantidadPagarC$');
  let inputTasaCambioPago = document.getElementById('inputTasaCambioPago');

  let cantidadPagarVerificar$ = document.getElementById('cantidadPagarVerificar$');


  let cantidadPagarCordobas = (cantidadPagarVerificar$.value * inputTasaCambioPago.value);

  cantidadPagarVerificarC$.value = cantidadPagarCordobas.toFixed(2);
  lblCantidadPagarC$.textContent = cantidadPagarCordobas.toFixed(2);

}

function calculoCordobasDoalres() {

}


function obtenerFecha() {
  let fechaActual = new Date();
  let dia = String(fechaActual.getDate()).padStart(2, '0');
  let mes = String(fechaActual.getMonth() + 1).padStart(2, '0'); // Enero es 0
  let anio = fechaActual.getFullYear();

  let fechaFormateada = anio + '-' + mes + '-' + dia;

  return fechaFormateada;
}

document.addEventListener('DOMContentLoaded', function (event) {


  calcularMontoPrimerPago();
  let fechaFormateada = obtenerFecha();

  fechaPago.value = fechaFormateada;

  // llama a validacionDolares manualmente
  fechaLetras({ target: fechaPago });


  obtenerTasaCambioConversion();



  obtener_pago();

  // llama a validacionDolares manualmente
  fechaLetras(event);




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

// Función para calcular el monto del primer pago
function calcularMontoPrimerPago() {

  IniciarliazarcifrasInputsVisualizarPrimerPagoModal();



  // Obtener los inputs del formulario normal
  // EN ESTE INPUT SE DEBERÁ PASAR LA FECHA DEL PRÉSTAMO
  const fechaPrestamoInput = document.getElementById('fechaPrestamoInput');
  const diasHastaProximoCorte = document.getElementById('diasHastaProximoCorte');
  const pagoMensualInput = document.getElementById('pagoMensual');
  const resultadoPagoDiarioModal = document.getElementById('resultadoPagoDiarioModal');
  const pagoDiario2Modal = document.getElementById('pagoDiario2Modal');


  const montoPrimerPagoInput = document.getElementById('montoPrimerPago');
  const montoPrimerPagoInputModal = document.getElementById('montoPrimerPagoModal');
  const pagoQuincenalInput = document.getElementById('pagoQuincenal');



  // Obtener el valor del input de fecha
  const fechaPrestamoValue = fechaPrestamoInput.value;

  const [year, month, day] = fechaPrestamoValue.split('-');

  const meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
  ];
  const nombreMes = meses[parseInt(month, 10) - 1]; // Restamos 1 porque los índices de los arrays empiezan en 0




  // Crear un objeto Date con solo el año, mes y día
  const fechaPrestamo = new Date(year, month - 1, day);

  // Función para obtener el número de días en un mes específico
  function daysInMonth(month, year) {
    return new Date(year, month, 0).getDate();
  }

  // Calcular el número de días en el mes actual
  const totalDaysInMonth = 30 /////////////// MES COMERCIAL ESTO PUEDE CAMBIAR ////////////


  // Calcular la fecha de la primera quincena (siempre es el día 15)
  const firstFortnightDate = 15

  // Calcular la fecha de la segunda quincena (último día del mes)
  const secondFortnightDate = 30

  // Calcular los días restantes hasta la próxima quincena
  let daysUntilNextFortnight;
  let corteQuincena = 0;

  if (fechaPrestamo.getDate() <= 15) {
    daysUntilNextFortnight = Math.abs(fechaPrestamo.getDate() - firstFortnightDate);
    corteQuincena = firstFortnightDate;
  }
  else {
    daysUntilNextFortnight = Math.abs(fechaPrestamo.getDate() - secondFortnightDate);
    corteQuincena = secondFortnightDate;
  }



  diasHastaProximoCorte.value = daysUntilNextFortnight + 1;


  // Obtener la cantidad de pago al día
  const pagoDiario = parseFloat(pagoMensualInput.value) / totalDaysInMonth;
  resultadoPagoDiarioModal.value = pagoDiario.toFixed(2);
  pagoDiario2Modal.value = pagoDiario.toFixed(2);


  // Calcular el monto del primer pago según la fecha del préstamo


  // Verificar si la fecha es válida
  if (!fechaPrestamo || isNaN(fechaPrestamo.getTime())) {
    // Si la fecha no es válida, establecer el valor del monto del primer pago en 0
    montoPrimerPagoInput.value = 0;
    montoPrimerPagoInputModal.value = 0;
    return; // Salir de la función si la fecha no es válida
  }

  else {
    // linkProcdmtoModal.classList.remove('inactive');
  }

  let montoPrimerPago = 0;



  const CopiaModalCalculoPrimerPago = modalCalculoPrimerPago.innerHTML;
  if (fechaPrestamo.getDate() === 1 || fechaPrestamo.getDate() === 15 || fechaPrestamo.getDate() === 30 || fechaPrestamo.getDate() === 31) {
    document.getElementById("linkProcdmtoModal").setAttribute("data-bs-target", "#modalNoCalculo");

    montoPrimerPago = 0;
    montoPrimerPagoInput.value = pagoQuincenalInput.value; // Redondear a 2 decimales
    montoPrimerPagoInputModal.value = pagoQuincenalInput.value; // Redondear a 2 decimales
    return
  }


  else {
    // document.getElementById("linkProcdmtoModal").setAttribute("data-bs-target", "#modalCalculoPrimerPago");
    montoPrimerPago = pagoDiario.toFixed(2) * (daysUntilNextFortnight + 1);
  }


  // Establecer el valor en el campo montoPrimerPago
  // montoPrimerPagoInput.value = montoPrimerPago.toFixed(2); // Redondear a 2 decimales
  montoPrimerPagoInputModal.value = montoPrimerPago.toFixed(2); // Redondear a 2 decimales

  mostrarDiasRestanteModal(fechaPrestamo, corteQuincena, nombreMes);


}

function mostrarDiasRestanteModal(fechaPrestamo, corteQuincena, nombreMes) {
  diasRestantesCorteModal.textContent = "Cantidad de días desde el " + fechaPrestamo.getDate() + " de " + nombreMes + " hasta el " + corteQuincena + " de " + nombreMes;
}



function obtenerTasaCambioConversion() {


  let inputTasaCambio = document.getElementById('inputTasaCambioPago');

  // Crea una función asincrona que mediante fetch haga una peticion de una url de mi backend para luego de recibirla haga una cosa u otra

  try {
    async function obtenerTasaCambio() {
      let response = await fetch('/obtener_tasa_cambio');
      let data = await response.json();
      return data;
    }

    obtenerTasaCambio().then(data => {

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
function verificar_pago_quincenal(data) {

  return fetch("/verificar_pago_quincenal", {
    method: "POST",
    body: JSON.stringify({ data }), // Convertir a JSON
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        throw new Error(data.error);
      }
      return data;
    })
    .catch(error => {
      console.error("Error al verificar el pago:", error);
      throw error; // Propagar el error a los llamadores de la función
    });

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
    tipoPagoCompleto.selectedIndex = 2; // Indica que pagó imcompleto

  } else {
    cantidadPagar$.style.color = 'green';
    tipoPagoCompleto.selectedIndex = 1; // Indica que pagó completo
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

  conversionCordobasDolares = (valorNumerico / inputTasaCambioPago.value).toFixed(2);
  cantidadPagar$.value = conversionCordobasDolares;

  // llama a validacionDolares manualmente
  validacionDolares({ target: cantidadPagar$ });

});




fechaPago.addEventListener('input', function (event) {

  obtener_pago();

  // llama a validacionDolares manualmente
  fechaLetras(event);





});

function obtener_pago() {

  if (comboSugerenciaPago.value === '1') {

    data_enviar = {
      fecha_a_pagar: fechaPago.value,
      id_cliente: formId_cliente.value
    }


    verificar_pago_quincenal(data_enviar)
      .then(data => {
        console.log(data)
        //window.alert(data.monto_pagoEspecial.cifra);
        cantidadPagarVerificar$.value = data.monto_pagoEspecial.cifra;
        pCantidadPagarVerificar$.textContent = `$ ${data.monto_pagoEspecial.cifra}`;

        // Selecciona el elemento span y cambia su atributo title
        var spanElement = document.getElementById('pCantidadPagarVerificar$');
        spanElement.setAttribute('title', data.monto_pagoEspecial.descripcion);

        // Actualiza el tooltip de Bootstrap
        var bootstrapTooltip = new bootstrap.Tooltip(spanElement);
        // bootstrapTooltip.updateTitleContent(data.monto_pagoEspecial.descripcion);

        var checkBoxPrimerPago = document.getElementById('checkBoxPrimerPago');

        // Verifica el estado y agrega los atributos necesarios
        if (data.monto_pagoEspecial.estado == 0) {
          console.log('Agregando atributos');
          spanElement.setAttribute('href', '#');
          spanElement.setAttribute('data-bs-toggle', 'modal');
          spanElement.setAttribute('data-bs-target', '#modalCalculoPrimerPago');
          spanElement.style.cursor = 'pointer';
          spanElement.style.color = '#0728e8';
          checkBoxPrimerPago.checked = true;

        } else {
          console.log('Eliminando atributos');
          spanElement.removeAttribute('href');
          spanElement.removeAttribute('data-bs-toggle');
          spanElement.removeAttribute('data-bs-target');
          checkBoxPrimerPago.checked = false;
        }

      })
      .catch(error => {
        // Manejar el error
      });
  }
}




pagoCompleto.addEventListener('click', function () {

  calculoDolaresCordobas();

  cantidadPagar$.value = cantidadPagarVerificar$.value;

  // llama a validacionDolares manualmente
  validacionDolares({ target: cantidadPagar$ });

  let fechaFormateada = obtenerFecha();

  fechaPago.value = fechaFormateada;
  // llama a validacionDolares manualmente
  fechaLetras({ target: fechaPago });

});


document.getElementById("filtro-comboBox").addEventListener("change", function () {
  const selectedValue = this.value; // Valor seleccionado en el combobox
  // Enviar una solicitud POST al servidor con el valor seleccionado
  // Puedes usar fetch o axios para hacer la solicitud
  // Ejemplo:
  fetch("/guardar_año_seleccionado", {
    method: "POST",
    body: JSON.stringify({ selectedValue }), // Convertir a JSON
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then(response => response.json())
    .then(data => {
      location.reload();
    })
    .catch(error => {
      console.error("Error al guardar en sesión:", error);
    });
});

function eliminar_pago(id_pago) {
  fetch("/eliminar_pago", {
    method: "POST",
    body: JSON.stringify({ id_pago }), // Convertir a JSON
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        throw new Error(data.error);
      }
      location.reload();
    })
    .catch(error => {
      console.error("Error al eliminar el pago:", error);
    });
}

function fetchInformacionPago(id_pago) {
  return fetch('/informacion_pagoEspecifico', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id_pagos: id_pago }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        throw new Error(data.error);
      }
      return data.pago;
    });
}


function obtenerInformacionPagoBorrar(id_pago) {
  fetchInformacionPago(id_pago)
    .then(pago => {
      // Filtrar los pagos con estado 1
      let pagosDolares = pago.filter(p => p.estado_detallePagos === 1);


      modalInformacionPago.innerHTML = pagosDolares.map(pago => `
      <strong>Fecha del pago: </strong><span>${pago.descripcion_quincena}</span>
      <br>
      <strong></strong><span>(${formatoFecha(pago.fecha_pago)})</span>
      <br>
      <strong>Cantidad abonada: </strong><span>${pago.codigoMoneda} ${pago.cifraPago} ${pago.nombreMoneda}</span>
    `).join('');

      pagosDolares.map(pago => {
        btnBorrarPago.setAttribute('onclick', `eliminar_pago(${pago.id_pagos})`);
      })


      let modalBorrarPago = new bootstrap.Modal(document.getElementById('modalBorrarPago'));



      modalBorrarPago.show();
    })
    .catch(error => {
      console.error('Error al obtener la información del pago:', error);
    });
}




function obtenerInformacionPagoEspecifico(id_pago) {

  let modalInformacionPago = document.getElementById('modalInformacionPago');
  let btnBorrarPago = document.getElementById('btnBorrarPago');

  fetch('/informacion_pagoEspecifico', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id_pagos: id_pago }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        throw new Error(data.error);
      }
      let pago = data.pago;



    })
    .catch(error => {
      console.error('Error al obtener la información del pago:', error);
    });

  pagosDolares.forEach(pago => {
  }
  );

}

// Función para formatear la fecha
function formatoFecha(fecha) {
  let fechaObjeto = new Date(fecha);
  let dia = fechaObjeto.getDate();
  let mes = fechaObjeto.getMonth() + 1; // Los meses en JavaScript van de 0 a 11
  let año = fechaObjeto.getFullYear();
  return `${dia < 10 ? '0' : ''}${dia}-${mes < 10 ? '0' : ''}${mes}-${año}`;
}


// Funciones para mostrar y ocultar detalles del cliente
btnMostrarDetallesCliente.addEventListener('click', function () {
  btnMostrarDetallesCliente.hidden = true;
  detallesCliente.hidden = false;

  btnOcultarDetallesCliente.hidden = false;


});

btnOcultarDetallesCliente.addEventListener('click', function () {

  btnMostrarDetallesCliente.hidden = false;
  detallesCliente.hidden = true;

  btnOcultarDetallesCliente.hidden = true;
});




