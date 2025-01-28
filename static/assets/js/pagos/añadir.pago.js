var inputTasaCambioPago = document.getElementById('inputTasaCambioPago');

var cantidadPagarVerificarC$ = document.getElementById('cantidadPagarVerificarC$');


let cantidadPagarVerificar$ = document.getElementById('cantidadPagarVerificar$');
let pCantidadPagarVerificar$ = document.getElementById('pCantidadPagarVerificar$');
let cantidadPagar$ = document.getElementById('cantidadPagar$');
let cantidadPagoCordobas = document.getElementById('cantidadPagoCordobas');
let fechaPago = document.getElementById('fechaPago'); // Se refiere a la referencia de la quincena
let fechaPagoReal = document.getElementById('fechaPagoReal'); // Se refiere a la fecha en la que se pagó la quiencena
let tiempoPagoLetras = document.getElementById('tiempoPagoLetras');
let tiempoPagoLetrasReal = document.getElementById('tiempoPagoLetrasReal')
let pagoCompleto = document.getElementById('pagoCompleto');
let comboSugerenciaPago = document.getElementById('comboSugerenciaPago');
let formId_cliente = document.getElementById('formId_cliente');
let tipoPagoCompleto = document.getElementById('tipoPagoCompleto');

// Sección para detalle cliente
let detallesCliente = document.getElementById('detallesCliente');
let btnMostrarDetallesCliente = document.getElementById('btnMostrarDetallesCliente');
let btnOcultarDetallesCliente = document.getElementById('btnOcultarDetallesCliente');

// Seccion automatizacion
let spanIgualarFechaQuincenaAFechaReal = document.getElementById('spanIgualarFechaQuincenaAFechaReal');
let spanpagoCompletoDlrs = document.getElementById('spanpagoCompletoDlrs');

//Seccion de etiquetas a para mostrar informacion del pago del cliente
let aCapital = document.getElementById('aCapital');
let aAbonoMensual = document.getElementById('aAbonoMensual');
let aAbonoQuincenal = document.getElementById('aAbonoQuincenal');
let aSaldoPendiente = document.getElementById('aSaldoPendiente');
let aSaldoAFavor = document.getElementById('aSaldoAFavor');



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
  fechaPagoReal.value = fechaFormateada;

  // llama a validacionDolares manualmente
  fechaLetras({ target: fechaPago });


  obtenerTasaCambioConversion();



  obtener_pago();

  // llama a validacionDolares manualmente
  fechaLetras(event);

  tiempoPagoLetrasReal.textContent = fechaLetrasFuncion(fechaFormateada, 'minimalista');

  let checkbox_confirmacion = document.getElementById('checkbox_confirmacion');
  checkbox_confirmacion.checked = true;






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
    // document.getElementById("linkProcdmtoModal").setAttribute("data-bs-target", "#modalNoCalculo");

    // montoPrimerPago = 0;
    // montoPrimerPagoInput.value = pagoQuincenalInput.value; // Redondear a 2 decimales
    // montoPrimerPagoInputModal.value = pagoQuincenalInput.value; // Redondear a 2 decimales
    // return
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

// Esta función retorna dos resultados completo o minimalista
function fechaLetrasFuncion(fecha, estructuraResultado) {
  var fechaPagoValue = fecha;
  console.log(fechaPagoValue);

  // Parseamos la fecha desde el formato de string
  const fechaPago = new Date(fechaPagoValue);
  const year = fechaPago.getUTCFullYear();
  const month = fechaPago.getUTCMonth() + 1; // Los meses en JavaScript van de 0 a 11
  const day = fechaPago.getUTCDate();

  const meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
  ];
  const nombreMes = meses[month - 1]; // Restamos 1 porque los índices de los arrays empiezan en 0

  let primeraSegundaQuincena = "";

  if (day <= 15) {
    primeraSegundaQuincena = "Primera quincena de " + nombreMes + " de " + year;
  } else {
    primeraSegundaQuincena = "Segunda quincena de " + nombreMes + " de " + year;
  }

  console.log(primeraSegundaQuincena);


  if (estructuraResultado === 'minimalista') {
    return primeraSegundaQuincena
  }
  else {
    return primeraSegundaQuincena + " (" + day + " de " + nombreMes + " de " + year + ")";
  }

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

  }

  else if (parseFloat(cantidadPagar$.value.replace(/\D/g, '')) === parseFloat(cantidadPagarVerificar$.value.replace(/\D/g, ''))) {
    cantidadPagar$.style.color = 'green';
    tipoPagoCompleto.selectedIndex = 1; // Indica que pagó completo
  }

  else if (parseFloat(cantidadPagar$.value.replace(/\D/g, '')) > parseFloat(cantidadPagarVerificar$.value.replace(/\D/g, ''))) {
    cantidadPagar$.style.color = "skyblue"
    tipoPagoCompleto.selectedIndex = 4; // Indica que pagó completo
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




// spanpagoCompletoDlrs.addEventListener('click', function () {

//   calculoDolaresCordobas();

//   cantidadPagar$.value = cantidadPagarVerificar$.value;

//   // llama a validacionDolares manualmente
//   validacionDolares({ target: cantidadPagar$ });

//   let fechaFormateada = obtenerFecha();

//   fechaPago.value = fechaFormateada;
//   // llama a validacionDolares manualmente
//   fechaLetras({ target: fechaPago });

// });


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
      console.log(pago);

      if (pago.tasa_conversion) {
        modalInformacionPago.innerHTML = `
          <strong>Fecha del pago: </strong><span>${pago.descripcion_quincena}</span>
          <br>
          <strong></strong><span>(${formatoFecha(pago.fecha_pago)})</span>
          <br>
          <strong>Cantidad abonada: </strong><span>${pago.codigoMoneda} ${pago.cifraPago$} ${pago.nombreMoneda}</span>
        `;
      } else {
        modalInformacionPago.innerHTML = `
          <strong>Fecha del pago: </strong><span>${pago.descripcion_quincena}</span>
          <br>
          <strong></strong><span>(${formatoFecha(pago.fecha_pago)})</span>
          <br>
          <strong>Cantidad abonada: </strong><span>${pago.codigoMoneda} ${pago.cifraPago} ${pago.nombreMoneda}</span>
        `;
      }

      // Asignar la función de eliminación al botón
      btnBorrarPago.setAttribute('onclick', `eliminar_pago(${pago.id_pagos})`);

      // Mostrar el modal de confirmación de borrado
      let modalBorrarPago = new bootstrap.Modal(document.getElementById('modalBorrarPago'));
      modalBorrarPago.show();
    })
    .catch(error => {
      console.error('Error al obtener la información del pago:', error);
    });
}

// Inicializar LightGallery dentro de la función o evento que abra o muestre el modal:
function initLightGallery() {
  const lgContainer = document.getElementById('lightgallery');
  // Si ya existe una instancia previa, destrúyela para evitar comportamientos extraños
  if (lgContainer.lgData) {
    lgContainer.lgData.destroy(true);
  }
  // Inicializa LightGallery con los plugins
  lightGallery(lgContainer, {
    selector: '.gallery-item',
    plugins: [lgZoom, lgThumbnail, lgRotate],
    speed: 500,
    download: false,
    counter: true,
    zoom: true,
    zoomFromOrigin: true,
    actualSize: false,
    closeOnTap: true,
    enableZoomAfter: 300,
    scale: 3,
    escKey: true,
    closable: true,
    closeOnClick: true,
    rotate: true,
    rotateLeft: true,
    rotateRight: true,
    flipHorizontal: true,
    flipVertical: true,
    addClass: 'lg-custom-zoom-class',
    mobileSettings: {
      controls: true,
      showCloseIcon: true,
      download: false,
      rotate: true
    },
    onAfterOpen: () => {
      console.log('LightGallery se ha abierto');
    },
  });
}

function obtenerInformacionPagoEspecifico(id_pago) {

  let modalVisualizarPago = new bootstrap.Modal(document.getElementById('modalVisualizarPago'));
  let tasaCambioRowVP = document.getElementById('tasaCambioRowVP');
  let cantidadPagoCordobasRowVP = document.getElementById('cantidadPagoCordobasRowVP');


  let tipoMonedaPagoVP = document.getElementById('tipoMonedaPagoVP');
  let cantidadPagoCordobasVP = document.getElementById('cantidadPagoCordobasVP');
  let lblPagoC$VP = document.getElementById('lblPagoC$VP');
  let cantidadPagar$VP = document.getElementById('cantidadPagar$VP');
  let lblPago$VP = document.getElementById('lblPago$VP');
  let inputTasaCambioPagoVP = document.getElementById('inputTasaCambioPagoVP');
  let fechaPagoVP = document.getElementById('fechaPagoVP');
  let observacionPagoVP = document.getElementById('observacionPagoVP');
  let evidenciaPagoVP = document.getElementById('evidenciaPagoVP');
  let realizadoPorVP = document.getElementById('realizadoPorVP');
  let lblFechaRealizacionPagoPorVP = document.getElementById('lblFechaRealizacionPagoPorVP');

  console.log(id_pago);


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
      fechaPagoLetras = fechaLetrasFuncion(pago.fecha_pago)
      console.log(pago);

      if (pago.tasa_conversion) {
        cantidadPagoCordobasRowVP.hidden = false;
        lblPagoC$VP.innerHTML = 'Pagó en córdobas';
        lblPago$VP.innerHTML = 'Tasa de cambio: ' + pago.tasa_conversion;

        inputTasaCambioPagoVP.value = pago.tasa_conversion;
        cantidadPagar$VP.value = pago.cifraPago$;
        cantidadPagoCordobasVP.value = pago.cifraPagoC$;
      }
      else {
        cantidadPagoCordobasRowVP.hidden = true;
        lblPago$VP.innerHTML = 'Pagó en dólares';

        inputTasaCambioPagoVP.value = pago.tasa_conversion;
        cantidadPagar$VP.value = pago.codigoMoneda + ' ' + pago.cifraPago;
      }



      fechaPagoVP.value = fechaPagoLetras;
      if (pago.observacion) {
        observacionPagoVP.value = pago.observacion;
      } else {
        observacionPagoVP.value = 'No hay observaciones';
      }

      if (pago.url_imagen !== null) {

        const evidenciaPagoVP = document.querySelector('.evidenciaPagoVP .gallery-item');
        evidenciaPagoVP.setAttribute('data-src', pago.url_imagen);
        evidenciaPagoVP.querySelector('img').setAttribute('src', pago.url_imagen);




      } else {
        console.log('No hay evidencia de pago');
        evidenciaPagoVP = document.querySelector('.evidenciaPagoVP').innerHTML = '<p>No hay evidencia de pago</p>';
      }

      console.log(pago);
      realizadoPorVP.value = pago.nombres_usuario + ' ' + pago.apellidos_usuario;
      lblFechaRealizacionPagoPorVP.textContent = 'Realizado el ' + formatoFechaYHora(pago.fecha_realizacion_pago);

      modalVisualizarPago.show();

      // document.getElementById('modalVisualizarPago').addEventListener('shown.bs.modal', () => {
      //   initLightGallery();
      // });






    })
    .catch(error => {
      console.error('Error al obtener la información del pago:', error);
    });



}

// Función para formatear la fecha
function formatoFecha(fecha) {
  let fechaObjeto = new Date(fecha);
  let dia = fechaObjeto.getDate();
  let mes = fechaObjeto.getMonth() + 1; // Los meses en JavaScript van de 0 a 11
  let año = fechaObjeto.getFullYear();
  return `${dia < 10 ? '0' : ''}${dia}-${mes < 10 ? '0' : ''}${mes}-${año}`;
}


function formatoFechaYHora(fecha) {
  const dbDate = new Date(fecha);

  let dia = dbDate.getUTCDate();
  let mes = dbDate.getUTCMonth() + 1;
  let año = dbDate.getUTCFullYear();
  let hora = dbDate.getUTCHours();
  let minutos = dbDate.getUTCMinutes();
  let segundos = dbDate.getUTCSeconds();
  let ampm = hora >= 12 ? 'PM' : 'AM';

  hora = hora % 12;
  hora = hora ? hora : 12;

  const meses = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
  ];
  let nombreMes = meses[mes - 1];

  return `${dia} de ${nombreMes} de ${año} a las ${hora}:` +
    `${minutos < 10 ? '0' : ''}${minutos}:` +
    `${segundos < 10 ? '0' : ''}${segundos} ${ampm} (UTC)`;
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


function finalizarDeuda(id_cliente) {

  console.log(id_cliente);

  let modalFinalizarDeuda = new bootstrap.Modal(document.getElementById('modalFinalizarDeuda'));

  modalFinalizarDeuda.show();






}




const btnGuardar = document.getElementById('btnGuardar');
btnGuardar.addEventListener('click', async function (event) {
  event.preventDefault();

  try {
    let data = await verificar_tipo_saldo_insertar();
    console.log(data);
    if (data.estadoPago == 0 || data.estadoPago == 3 || data.estadoPago == 4) {
      let modal_confirmacion_detalle_pago = new bootstrap.Modal(document.getElementById('modal_confirmacion_detalle_pago'));
      let content_modal_detalle_pago = document.getElementById('content_modal_detalle_pago');


      let estadopago_texto = '';
      let color_text = '';

      if (data.estadoPago == 0) {
        estadopago_texto = 'en contra';
        color_text = 'text-danger';
      } else if (data.estadoPago == 4) {
        estadopago_texto = 'a favor';
        color_text = 'text-success';
      }

      content_modal_detalle_pago.innerHTML = `¿Está seguro que desea agregar un saldo <strong class="${color_text}">${estadopago_texto}</strong>
          al cliente <strong>${data.nombres_apellidos}</strong> de <strong class="${color_text}">$ ${data.cantidadPagarDolares} dólares</strong>?`;

      modal_confirmacion_detalle_pago.show();

    }
    else if (data.estadoPago == 1 || data.estadoPago == 2) {
      showPreloader();
      
      try {
        let response = await procesar_pago();
        console.log(response);
        
        // Guardar mensaje de éxito en localStorage
        localStorage.setItem('pagoMessage', JSON.stringify({
          type: 'success',
          message: 'Pago agregado con éxito'
        }));
        
        // Esperar 500ms antes de recargar para que el loader se muestre suavemente
        await new Promise(resolve => setTimeout(resolve, 500));
        window.location.reload();
      } catch (error) {
        // Guardar mensaje de error en localStorage
        localStorage.setItem('pagoMessage', JSON.stringify({
          type: 'error',
          message: `Error al procesar el pago: ${error.message}`
        }));
        
        // Esperar 500ms antes de recargar para que el loader se muestre suavemente
        await new Promise(resolve => setTimeout(resolve, 500));
        window.location.reload();
      }
    }
  } catch (error) {
    console.error('Error:', error);
    // Guardar mensaje de error en localStorage
    localStorage.setItem('pagoMessage', JSON.stringify({
      type: 'error',
      message: `Error: ${error.message}`
    }));
    
    // Esperar 500ms antes de recargar para que el loader se muestre suavemente
    await new Promise(resolve => setTimeout(resolve, 500));
    window.location.reload();
  }
});

// Agregar este código para mostrar el mensaje después de la recarga
document.addEventListener('DOMContentLoaded', function() {
  const message = localStorage.getItem('pagoMessage');
  if (message) {
    const { type, message: msg } = JSON.parse(message);
    hidePreloader();
    createToast(type, msg, 5000, 'bottom-right');
    localStorage.removeItem('pagoMessage'); // Limpiar el mensaje
  }
});

const proceder_pago = document.getElementById('proceder_pago');
proceder_pago.addEventListener('click', async function (event) {

  event.preventDefault();



  try {
    let data = await procesar_pago();
    console.log(data);

    window.location.reload();
  }
  catch (error) {
    console.error('Error:', error);
  }



});

// Registrar los plugins de FilePond
FilePond.registerPlugin(
  FilePondPluginImagePreview,
  FilePondPluginFileValidateType
);

// Convertir el input en una instancia de FilePond
const pond = FilePond.create(document.querySelector('input[name="filepond"]'), {
  allowImagePreview: true,
  acceptedFileTypes: ['image/jpeg', 'image/png', 'image/jpg'],
  dropOnElement: false,
  dropOnPage: false,
  allowMultiple: false,
  maxFiles: 1,
  fileValidateTypeDetectType: (source, type) => new Promise((resolve, reject) => {
    // Para archivos
    if (source instanceof File) {
      resolve(source.type);
    }
    // Para otras fuentes
    resolve(type);
  }),
  server: {
    process: (fieldName, file, metadata, load, error, progress, abort) => {
      // Simular una carga
      const duration = 2000; // 2 segundos
      let current = 0;

      const interval = setInterval(() => {
        current += 10;
        progress(current);

        if (current >= 100) {
          clearInterval(interval);
          load(Date.now()); // Simular ID del archivo
        }
      }, duration / 100);

      // Permitir cancelar la carga
      return {
        abort: () => {
          clearInterval(interval);
          abort();
        }
      };
    },
    // Agregar el método revert para manejar la eliminación
    revert: (uniqueFileId, load, error) => {
      // Simular proceso de eliminación
      setTimeout(() => {
        load();
      }, 1000);
    }
  },
  instantUpload: true,
  allowRevert: true, // Habilitar la opción de eliminar
  labelFileRemoveError: 'Error al eliminar el archivo',
  labelFileProcessingRevertError: 'Error al revertir la carga',
  labelFileRemove: 'Eliminar',
  labelIdle: 'Arrastra y suelta tus archivos o <span class="filepond--label-action">Busca</span>',
  labelFileProcessing: 'Subiendo...',
  labelFileProcessingComplete: '¡Subida completada!',
  labelTapToUndo: 'toca para deshacer',
  labelTapToCancel: 'toca para cancelar',
  labelInvalidField: 'El archivo no es válido',
  labelFileTypeNotAllowed: 'Solamente se permite archivos de imagen',
  fileValidateTypeLabelExpectedTypes: 'Se esperan archivos de tipo: {allTypes}',
});

// Modificar la función procesar_pago para manejar el archivo
async function procesar_pago() {
  let formData = new FormData(document.getElementById('anadirClientes'));

  // Obtener el archivo de FilePond
  const files = pond.getFiles();
  if (files.length > 0) {
    // Si hay un archivo, agregarlo al FormData
    formData.append('evidenciaPago', files[0].file);
  }

  try {
    const response = await fetch('/procesar_pago', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    if (data.error) {
      throw new Error(data.error);
    }

    return data;
  } catch (error) {
    console.error('Error al verificar el tipo de saldo:', error);
    throw error;
  }
}
async function verificar_tipo_saldo_insertar() {
  let formData = new FormData(document.getElementById('anadirClientes'));

  try {
    const response = await fetch('/verificar_tipo_saldo_insertar', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    return data;
  } catch (error) {
    console.error('Error al verificar el tipo de saldo:', error);
    throw error; // Re-lanzar el error para manejarlo en el bloque try-catch del submit 
  }
}

// const anadirClientes = document.getElementById('anadirClientes');
// anadirClientes.addEventListener('submit', async function (event) { // Marcar esta función como async

//   let proceder_pago_estado = 1;
//   let verificar_pago_estado = 2;

//   event.preventDefault();

//   let procesar_pago = false;

//   try {
//     let data = await verificar_tipo_saldo_insertar(procesar_pago);
//     console.log(data);

//     if (data.message.id_operation === proceder_pago_estado) {
//       // Manejar la respuesta de proceder_pago
//       if (data.message.message === "Pago realizado con éxito") {
//         // Código para manejar éxito
//         console.log("Pago realizado con éxito");
//       } else {
//         // Código para manejar error en proceder_pago
//         console.error("Error en el proceso de pago:", data.message.message);
//       }
//     } else if (data.message.id_operation === verificar_pago_estado) {
//       // Manejar la respuesta de verificar_pago
//       let modal_confirmacion_detalle_pago = new bootstrap.Modal(document.getElementById('modal_confirmacion_detalle_pago'));
//       let content_modal_detalle_pago = document.getElementById('content_modal_detalle_pago');

//       if (data.verificacion_tipo_pago_insertar.estadoPago == 0 || data.verificacion_tipo_pago_insertar.estadoPago == 4) {
//         let checkbox_modal_confirmado = document.getElementById('checkbox_modal_confirmado');
//         checkbox_modal_confirmado.checked = true;

//         let estadopago_texto = '';
//         let color_text = '';

//         if (data.verificacion_tipo_pago_insertar.estadoPago == 0) {
//           estadopago_texto = 'en contra';
//           color_text = 'text-danger';
//         } else if (data.verificacion_tipo_pago_insertar.estadoPago == 4) {
//           estadopago_texto = 'a favor';
//           color_text = 'text-success';
//         }

//         content_modal_detalle_pago.innerHTML = `¿Está seguro que desea agregar un saldo <strong class="${color_text}">${estadopago_texto}</strong>
//           al cliente <strong>${data.verificacion_tipo_pago_insertar.nombres_apellidos}</strong>? de <strong class="${color_text}">$ ${data.verificacion_tipo_pago_insertar.cantidadPagarDolares} dólares</strong>`;

//         modal_confirmacion_detalle_pago.show();
//         console.log(data);
//       } else {
//         procesar_pago = true;
//         try {
//           data = await verificar_tipo_saldo_insertar(procesar_pago);
//           if (data.message.id_operation === proceder_pago_estado) {
//             // Manejar la respuesta de proceder_pago al intentar procesar el pago nuevamente
//             console.log(data.message.message);
//           }
//         } catch (error) {
//           console.error('Error al procesar el pago:', error);
//         }
//       }
//     }

//   } catch (error) {
//     console.error('Error:', error);
//   }
// });


function mismaQuincena(fecha1, fecha2) {
  // Parseamos las fechas desde el formato de string
  const fechaPago1 = new Date(fecha1);
  const fechaPago2 = new Date(fecha2);

  // Obtenemos el año, mes y día de cada fecha
  const year1 = fechaPago1.getUTCFullYear();
  const month1 = fechaPago1.getUTCMonth() + 1; // Los meses en JavaScript van de 0 a 11
  const day1 = fechaPago1.getUTCDate();

  const year2 = fechaPago2.getUTCFullYear();
  const month2 = fechaPago2.getUTCMonth() + 1;
  const day2 = fechaPago2.getUTCDate();

  // Determinamos en qué quincena cae cada fecha
  const quincena1 = (day1 <= 15) ? `Primera quincena de ${month1}-${year1}` : `Segunda quincena de ${month1}-${year1}`;
  const quincena2 = (day2 <= 15) ? `Primera quincena de ${month2}-${year2}` : `Segunda quincena de ${month2}-${year2}`;

  console.log(quincena1);
  console.log(quincena2);

  // Comparamos las quincenas y retornamos true si son iguales, de lo contrario false
  console.log(quincena1 === quincena2);
  return quincena1 === quincena2;
}

// Función para normalizar la fecha
function normalizarFecha(fecha) {
  if (typeof fecha === 'string') {
    // Detectar si el formato es YYYY-MM-DD y convertirlo a Date
    if (fecha.includes('-')) {
      let [year, month, day] = fecha.split('-').map(Number);
      fecha = new Date(year, month - 1, day); // Convertir a Date
    } else {
      fecha = new Date(fecha); // Intentar convertir a Date
    }
  }
  if (!isNaN(fecha.getTime())) {
    fecha.setHours(0, 0, 0, 0); // Ajustar a la medianoche
  }
  return fecha;
}

// Función para actualizar la observación del pago
function actualizarObservacionPago(fechaPagoRealValue, esRetraso) {
  let observacionPago = document.getElementById('observacionPago');
  if (esRetraso) {
    let fechaPagoRealFormateada = normalizarFecha(fechaPagoRealValue);
    let opcionesFecha = { day: 'numeric', month: 'long', year: 'numeric' };
    let fechaPagoRealLetrasFormateada = fechaPagoRealFormateada.toLocaleDateString('es-ES', opcionesFecha);
    observacionPago.value = 'El cliente tuvo un retraso en su pago y realmente pagó el día ' + fechaPagoRealLetrasFormateada;
  } else {
    observacionPago.value = '';
  }
}

let conRetraso = document.getElementById('conRetraso');

fechaPago.addEventListener('input', function () {
  let fechaPagoValue = normalizarFecha(fechaPago.value);
  let fechaActual = normalizarFecha(new Date());
  let divInputFechaPagoReal = document.getElementById('divInputFechaPagoReal');
  let fechaPagoRealValue = fechaPago.value;

  // Actualizamos el label de la quincena
  tiempoPagoLetras.textContent = fechaLetrasFuncion(fechaPago.value, 'minimalista');

  obtener_pago();

  console.log("Fecha actual normalizada:", fechaActual);
  console.log("Fecha de pago normalizada:", fechaPagoValue);

  if (fechaPagoValue < fechaActual) {
    divInputFechaPagoReal.hidden = false;
    fechaPagoRealValue = fechaActual.toISOString().split('T')[0];
    actualizarObservacionPago(fechaPagoRealValue, true);
    conRetraso.hidden = false;
  } else {
    divInputFechaPagoReal.hidden = true;
    actualizarObservacionPago('', false);
    conRetraso.hidden = true;
  }

  fechaPagoReal.value = fechaPagoRealValue;
});

fechaPagoReal.addEventListener('input', function () {
  let fechaPagoValue = normalizarFecha(fechaPago.value);
  let fechaPagoRealValue = normalizarFecha(fechaPagoReal.value);

  console.log("EMPIEZA EL DEBUG!!!");
  console.log("fechaPagoValue:", fechaPagoValue);
  console.log("fechaPagoRealValue:", fechaPagoRealValue);



  if (fechaPagoRealValue <= fechaPagoValue) {
    console.log("La fecha real de pago es anterior a la fecha programada.");
    fechaPagoReal.value = fechaPago.value;
    actualizarObservacionPago('', false);
    conRetraso.hidden = true;
  } else if (fechaPagoRealValue > fechaPagoValue) {
    console.log("La fecha real de pago es posterior a la fecha programada.");
    actualizarObservacionPago(fechaPagoReal.value, true);
    conRetraso.hidden = false;
  } else {
    console.log("La fecha real de pago es igual a la fecha programada.");
    actualizarObservacionPago('', false);

    conRetraso.hidden = true;
  }

  // Actualizamos el label de la quincena
  tiempoPagoLetrasReal.textContent = fechaLetrasFuncion(fechaPagoReal.value, 'minimalista');
});


document.getElementById('spanpagoCompletoDlrs').addEventListener('click', function () {
  calculoDolaresCordobas();

  // Set the amount to pay in dollars
  cantidadPagar$.value = cantidadPagarVerificar$.value;

  if (tipoMonedaPago.value === '2') { // If the selected currency is Cordobas
    // Calculate the amount to pay in Cordobas
    let tasaCambio = parseFloat(inputTasaCambioPago.value);
    let cantidadPagarVerificarDolares = parseFloat(cantidadPagarVerificar$.value);
    let cantidadCordobas = cantidadPagarVerificarDolares * tasaCambio;
    cantidadPagoCordobas.value = cantidadCordobas.toFixed(2);

    // Manually dispatch input event to trigger validation
    cantidadPagoCordobas.dispatchEvent(new Event('input'));
  }

  // Manually dispatch input event for Dollars input
  cantidadPagar$.dispatchEvent(new Event('input'));

});


spanIgualarFechaQuincenaAFechaReal.addEventListener("click", function () {

  fechaPagoReal.value = fechaPago.value;

  fechaPagoReal.dispatchEvent(new Event('input'));

  divInputFechaPagoReal.hidden = true;

});

// aCapital.addEventListener('click', function(){

//   CambioEtiquetasACordobasDetallesCliente();

// });

// function CambioEtiquetasACordobasDetallesCliente(){

//   const capital = document.getElementById('aCapital').dataset.capital;
//   const abonoMensual = document.getElementById('aAbonoMensual').dataset.abonoMensual;
//   const abonoQuincenal = document.getElementById('aAbonoQuincenal').dataset.abonoQuincenal;

//   const asaldoPendiente = document.getElementById('aSaldoPendiente');
//   if (asaldoPendiente){

//     const saldoPendiente= asaldoPendiente.dataset.dataClienteSaldoPendiente;
//   }

//   const aSaldoAFavor = document.getElementById('aSaldoAFavor');
//   if (aSaldoAFavor){
//    const saldoAFavor= aSaldoAFavor.dataset.dataClienteSaldoAFavor;
//   }

//   obtenerValorTasaCambio().then(tasaCambio => {
//     window.alert('Capital: ' + capital + ' Abono mensual: ' + abonoMensual + ' Abono quincenal: ' + abonoQuincenal + ' tasa de cambio: ' + tasaCambio);

//     capitalCordobas = capital * tasaCambio;
//     abonoMensualCordobas = abonoMensual * tasaCambio;
//     abonoQuincenalCordobas = abonoQuincenal * tasaCambio;
//   });












// }  


async function obtenerTasaCambio() {
  let response = await fetch('/obtener_tasa_cambio');
  let data = await response.json();
  return data;
}

async function obtenerValorTasaCambio() {
  let data = await obtenerTasaCambio();
  if (data.tasa_cambio.cifraTasaCambio === "0.00") {
    throw new Error('Inserte tasa de cambio por favor');
  } else {
    return data.tasa_cambio.cifraTasaCambio;
  }
}

function formatearNumero(numero) {
  if (isNaN(numero)) {
    return "0";
  }
  return numero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function cambiarValoresACordobas(tasaCambio) {
  const capitalElement = document.getElementById('aCapital');
  const abonoMensualElement = document.getElementById('aAbonoMensual');
  const abonoQuincenalElement = document.getElementById('aAbonoQuincenal');
  const saldoPendienteElement = document.getElementById('aSaldoPendiente');
  const saldoAFavorElement = document.getElementById('aSaldoAFavor');

  if (capitalElement) {
    const capital = parseFloat(capitalElement.dataset.capital);
    console.log('Capital:', capital);
    capitalElement.querySelector('span').textContent = 'C$ ' + formatearNumero((capital * tasaCambio).toFixed(2));
  }

  if (abonoMensualElement) {
    const abonoMensual = parseFloat(abonoMensualElement.dataset.abonoMensual);
    console.log('Abono Mensual:', abonoMensual);
    abonoMensualElement.querySelector('span').textContent = 'C$ ' + formatearNumero((abonoMensual * tasaCambio).toFixed(2));
  }

  if (abonoQuincenalElement) {
    const abonoQuincenal = parseFloat(abonoQuincenalElement.dataset.abonoQuincenal);
    console.log('Abono Quincenal:', abonoQuincenal);
    abonoQuincenalElement.querySelector('span').textContent = 'C$ ' + formatearNumero((abonoQuincenal * tasaCambio).toFixed(2));
  }

  if (saldoPendienteElement) {
    const saldoPendiente = parseFloat(saldoPendienteElement.dataset.clienteSaldoPendiente);
    console.log('Saldo Pendiente:', saldoPendiente);
    saldoPendienteElement.querySelector('span').textContent = 'C$ ' + formatearNumero((saldoPendiente * tasaCambio).toFixed(2));
  }

  if (saldoAFavorElement) {
    const saldoAFavor = parseFloat(saldoAFavorElement.dataset.clienteSaldoAFavor);
    console.log('Saldo a Favor:', saldoAFavor);
    saldoAFavorElement.querySelector('span').textContent = 'C$ ' + formatearNumero((saldoAFavor * tasaCambio).toFixed(2));
  }
}

function restaurarValoresOriginales() {
  const capitalElement = document.getElementById('aCapital');
  const abonoMensualElement = document.getElementById('aAbonoMensual');
  const abonoQuincenalElement = document.getElementById('aAbonoQuincenal');
  const saldoPendienteElement = document.getElementById('aSaldoPendiente');
  const saldoAFavorElement = document.getElementById('aSaldoAFavor');

  if (capitalElement) {
    console.log('Restaurar Capital:', capitalElement.dataset.original);
    capitalElement.querySelector('span').textContent = '$ ' + formatearNumero(capitalElement.dataset.original);
  }

  if (abonoMensualElement) {
    console.log('Restaurar Abono Mensual:', abonoMensualElement.dataset.original);
    abonoMensualElement.querySelector('span').textContent = '$ ' + formatearNumero(abonoMensualElement.dataset.original);
  }

  if (abonoQuincenalElement) {
    console.log('Restaurar Abono Quincenal:', abonoQuincenalElement.dataset.original);
    abonoQuincenalElement.querySelector('span').textContent = '$ ' + formatearNumero(abonoQuincenalElement.dataset.original);
  }

  if (saldoPendienteElement) {
    console.log('Restaurar Saldo Pendiente:', saldoPendienteElement.dataset.original);
    saldoPendienteElement.querySelector('span').textContent = '$ ' + formatearNumero(saldoPendienteElement.dataset.original);
  }

  if (saldoAFavorElement) {
    console.log('Restaurar Saldo a Favor:', saldoAFavorElement.dataset.original);
    saldoAFavorElement.querySelector('span').textContent = '$ ' + formatearNumero(saldoAFavorElement.dataset.original);
  }
}

let valoresEnCordobas = false;

function alternarValores() {
  if (valoresEnCordobas) {
    restaurarValoresOriginales();
  } else {
    obtenerValorTasaCambio().then(tasaCambio => {
      cambiarValoresACordobas(tasaCambio);
    }).catch(error => {
      console.error(error.message);
      alert(error.message);
    });
  }
  valoresEnCordobas = !valoresEnCordobas;
}

document.addEventListener('DOMContentLoaded', function () {
  const capitalElement = document.getElementById('aCapital');
  const abonoMensualElement = document.getElementById('aAbonoMensual');
  const abonoQuincenalElement = document.getElementById('aAbonoQuincenal');
  const saldoPendienteElement = document.getElementById('aSaldoPendiente');
  const saldoAFavorElement = document.getElementById('aSaldoAFavor');

  if (capitalElement) {
    capitalElement.addEventListener('click', alternarValores);
  }
  if (abonoMensualElement) {
    abonoMensualElement.addEventListener('click', alternarValores);
  }
  if (abonoQuincenalElement) {
    abonoQuincenalElement.addEventListener('click', alternarValores);
  }
  if (saldoPendienteElement) {
    saldoPendienteElement.addEventListener('click', alternarValores);
  }
  if (saldoAFavorElement) {
    saldoAFavorElement.addEventListener('click', alternarValores);
  }
});