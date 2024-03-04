function revision_contrato() {
  let inputsForm1 = document.querySelectorAll(".step-1 input , .step-1 select , .step-1 textarea");
  let inputsForm2 = document.querySelectorAll(".step-2 input , .step-2 select , .step-2 textarea");
  let inputsForm3 = document.querySelectorAll(".step-3 input , .step-3 select , .step-3 textarea");

  var formContrato = {};

  inputsForm1.forEach(function (input) {

    if (input.name == "genero" || input.name == "nombreDireccion" || input.name == "idCompaniTelefonica" || input.name == "nombreTelefono") {

      let selected = input.options[input.selectedIndex]

      formContrato[input.name] = selected.text;
    }

    else {
      formContrato[input.name] = input.value;
    }

  });

  inputsForm2.forEach(function (input) {

    if (input.name == "estadoCivil" || input.name == "nombreDelegacion" || input.name == "tipoCliente" || input.name == "tipoMonedaMontoSolicitado" || input.name == "tipoTiempoPlazoSolicitado") {

      let selected = input.options[input.selectedIndex]

      formContrato[input.name] = selected.text;
    }

    else {
      formContrato[input.name] = input.value;
    }

  });

  inputsForm3.forEach(function (input) {

    if (input.name == "generoFiador" || input.name == "nombreDireccionFiador" || input.name == "idCompaniTelefonicaFiador" || input.name == "nombreTelefonoFiador") {

      let selected = input.options[input.selectedIndex]

      formContrato[input.name] = selected.text;
    }

    else {
      formContrato[input.name] = input.value;
    }

  });



  const mapeo = {
    "nombres": "nombresRevisionContrato",
    "apellidos": "apellidosRevisionContrato",
    "cedula": "cedulaRevisionContrato",
    "fechaNac": "fechaNacRevisionContrato",
    "genero": "generoRevisionContrato",
    "estadoCivil": "estadoCivilRevisionContrato",
    "nombreDelegacion": "nombreDelegacionRevisionContrato",
    "dptoArea": "dptoAreaRevisionContrato",
    "direccion": "direccionRevisionContrato",
    "direccionMaps": "direccionMapsRevisionContrato",
    "nombreDireccion": "nombreDireccionRevisionContrato",
    "idCompaniTelefonica": "companiaTelefonicaRevisionContrato",
    "telefono": "telefonoRevisionContrato",
    "nombreTelefono": "nombreTelefonoRevisionContrato",
    "tipoCliente": "tipoClienteRevisionContrato",
    "montoSolicitado": "montoSolicitadoRevisionContrato",
    "plazoSolicitado": "plazoSolicitadoRevisionContrato",
    "fechaPrestamo": "fechaPrestamoRevisionContrato",
    "nombresFiador": "nombresFiadorRevisionContrato",
    "apellidosFiador": "apellidosFiadorRevisionContrato",
    "cedulaFiador": "cedulaFiadorRevisionContrato",
    "fechaNacFiador": "fechaNacFiadorRevisionContrato",
    "generoFiador": "generoFiadorRevisionContrato",
    "direccionFiador": "direccionFiadorRevisionContrato",
    "direccionMapsFiador": "direccionMapsFiadorRevisionContrato",
    "nombreDireccionFiador": "nombreDireccionFiadorRevisionContrato",
    "idCompaniTelefonicaFiador": "companiaTelefonicaFiadorRevisionContrato",
    "telefonoFiador": "telefonoFiadorRevisionContrato",
    "nombreTelefonoFiador": "nombreTelefonoFiadorRevisionContrato"

  }
  console.log(formContrato);

  // Asignación de valores a los inputs
  for (const objetoName in formContrato) {
    if (formContrato.hasOwnProperty(objetoName)) {
      const inputName = mapeo[objetoName];
      const inputValue = formContrato[objetoName];

      // Verifica si el valor no es null antes de asignarlo
      if (inputValue !== null) {
        const inputElement = document.getElementById(inputName);
        if (inputElement) {
          inputElement.value = inputValue;
        } else {
          console.error('Elemento con ID ' + inputName + ' no encontrado.');
        }
      }
    }
  }


}


var currentStep = 1;
var updateProgressBar;

// Seleccionar los botones
var nextStep = document.querySelector(".next-step");
var prevStep = document.querySelector(".prev-step");

// Seleccionar el elemento span con el id "step-indicator"
var stepIndicator = document.getElementById("step-indicator");

// Agregar una línea al final de la función displayStep para cambiar el contenido del elemento span
function displayStep(stepNumber) {
  if (stepNumber >= 1 && stepNumber <= 4) {
    $(".step-" + currentStep).hide();
    $(".step-" + stepNumber).show();
    currentStep = stepNumber;
    updateProgressBar();

  }
}

$(document).ready(function () {
  $('#multi-step-form').find('.step').slice(1).hide();



  $(".next-step").click(function () {

    if (currentStep < 4) {
      // Solo validar si el paso actual es el 2 o el 3
      if (currentStep == 2 || currentStep == 3) {
        var formContrato = document.querySelector(".step-" + currentStep); // selecciona el form del paso actual
        var inputs = formContrato.querySelectorAll("input, select"); // selecciona todos los inputs dentro del form
        var valido = true; // asume que el form es válido

        for (var i = 0; i < inputs.length; i++) { // recorre todos los inputs
          if (!inputs[i].checkValidity()) { // si alguno no es válido
            valido = false; // cambia la variable a false
            window.alert("El campo " + inputs[i].name + " es inválido"); // muestra un mensaje de error
            inputs[i].reportValidity(); // muestra el mensaje de error
            break; // sale del bucle
          }
        }

        if (valido) { // si el form es válido
          $(".step-" + currentStep).addClass("animate__animated animate__fadeOutLeft");
          currentStep++;


          if (currentStep == 4) {
            revision_contrato();
            setTimeout(function () {
              $(".step").removeClass("animate__animated animate__fadeOutLeft").hide();
              $(".step-" + currentStep).show().addClass("animate__animated animate__fadeInRight");
              updateProgressBar();
            }, 500);
          }

          else {
            setTimeout(function () {
              $(".step").removeClass("animate__animated animate__fadeOutLeft").hide();
              $(".step-" + currentStep).show().addClass("animate__animated animate__fadeInRight");
              updateProgressBar();
            }, 500);
          }


        }
      }



      else { // si no hay que validar, solo avanzar al siguiente paso
        // Subir al principio de la página
        $(".step-" + currentStep).addClass("animate__animated animate__fadeOutLeft");
        currentStep++;
        setTimeout(function () {
          $(".step").removeClass("animate__animated animate__fadeOutLeft").hide();
          $(".step-" + currentStep).show().addClass("animate__animated animate__fadeInRight");
          updateProgressBar();
        }, 500);
      }

    }
  });


  $(".prev-step").click(function () {
    if (currentStep > 1) {
      $(".step-" + currentStep).addClass("animate__animated animate__fadeOutRight");
      currentStep--;
      setTimeout(function () {
        $(".step").removeClass("animate__animated animate__fadeOutRight").hide();
        $(".step-" + currentStep).show().addClass("animate__animated animate__fadeInLeft");
        updateProgressBar();
      }, 500);
    }
  });

  updateProgressBar = function () {
    console.log("ENTRO´!")
    console.log(currentStep);
    // Cambiar el contenido del elemento span con el número del paso actual usando javascript puro
    stepIndicator.textContent = "Paso " + currentStep;
    // Subir al principio de la página
    window.scrollTo(0, 0);
    // Esperar un segundo (1000 milisegundos)
    setTimeout(function () {
      // Calcular el porcentaje de progreso
      var progressPercentage = ((currentStep - 1) / 3) * 100;
      // Cambiar el ancho de la barra de progreso
      $(".progress-bar").css("width", progressPercentage + "%");
    }, 500);
  }

});

// Obtener referencias a los elementos del DOM
// Obtenemos los inputs del formlario normal
const montoSolicitadoInput = document.getElementById('montoSolicitado');
const tasaInteresInput = document.getElementById('tasaInteres');
const pagoMensualInput = document.getElementById('pagoMensual');
const pagoQuincenalInput = document.getElementById('pagoQuincenal');
const pagoMensualInputModal = document.getElementById('pagoMensualModal');
const diasHastaProximoCorte = document.getElementById('diasHastaProximoCorte');

// Obtener los inputs del formulario normal
const fechaPrestamoInput = document.getElementById('fechaPrestamo');
const montoPrimerPagoInput = document.getElementById('montoPrimerPago');


///////////////   MODALS //////////////////////////////////////////
//Obtenemos referencias de las etiquetas a para abrirModals
const linkProcdmtoModal = document.getElementById('linkProcdmtoModal')

const montoPrimerPagoInputModal = document.getElementById('montoPrimerPagoModal');

const resultadoPagoDiarioModal = document.getElementById('resultadoPagoDiarioModal');
const pagoDiario2Modal = document.getElementById('pagoDiario2Modal');
const diasRestantesCorteModal = document.getElementById('diasRestantesCorteModal');



// Agregar un evento al cambiar el campo de fechaPrestamo
fechaPrestamoInput.addEventListener('change', function () {
  modalAlertafecha();
});
// Agregar un evento de cambio a los campos de entrada
montoSolicitadoInput.addEventListener('change', function () {

  if (!(tasaInteresInput.value == "") || (!tasaInteresInput.value == "0")) {
    calcularPagos();
    calcularMontoPrimerPago();
  }


});

tasaInteresInput.addEventListener('change', function () {
  if (!(tasaInteresInput.value == "") || (!tasaInteresInput.value == "0")) {
    calcularPagos();
    calcularMontoPrimerPago();
  }
  else{
    pagoMensualInput.value = 0;
    pagoQuincenalInput.value = 0;
  }
});


function modalAlertafecha() {



  const fechaPrestamoValue = fechaPrestamoInput.value;

  const [year, month, day] = fechaPrestamoValue.split('-');

  // Crear un objeto Date con solo el año, mes y día
  const fechaPrestamo = new Date(year, month - 1, day);

  // Función para obtener el número de días en un mes específico
  function daysInMonth(month, year) {
    return new Date(year, month, 0).getDate();
  }

  const meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
  ];
  const nombreMes = meses[parseInt(month, 10) - 1]; // Restamos 1 porque los índices de los arrays empiezan en 0

  diasDelMes = daysInMonth(fechaPrestamo.getMonth() + 1, fechaPrestamo.getFullYear());

  if (diasDelMes > 30 || diasDelMes < 30) {

    var pModalAlertaFecha = document.getElementById('pModalAlertaFecha');
    pModalAlertaFecha.textContent = "El mes de " + nombreMes + " tiene " + diasDelMes + " días y no 30 días del mes comercial. Por favor tengalo en cuenta!";


    var modalAlerta = new bootstrap.Modal(document.getElementById('modalAlertaFecha'));
    modalAlerta.show();
  }
}

// Función para calcular los pagos mensuales y quincenales
function calcularPagos() {
  // Obtener los valores de los campos de entrada
  const montoSolicitado = parseFloat(montoSolicitadoInput.value);
  const tasaInteres = parseFloat(tasaInteresInput.value);

  // Calcular los pagos mensuales y quincenales (fórmula de ejemplo)
  const pagoMensual = montoSolicitado * tasaInteres / 100;
  const pagoQuincenal = pagoMensual / 2;

  // Mostrar los resultados en los campos de entrada correspondientes
  pagoMensualInput.value = pagoMensual.toFixed(2); // Redondear a 2 decimales
  pagoMensualInputModal.value = pagoMensual.toFixed(2); // Este va hacia el modal de la comprobación de formula
  pagoQuincenalInput.value = pagoQuincenal.toFixed(2); // Redondear a 2 decimales
}





// Agregar un evento de cambio al campo de entrada fechaPrestamo
fechaPrestamoInput.addEventListener('change', calcularMontoPrimerPago);

// Función para calcular el monto del primer pago
function calcularMontoPrimerPago() {



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

  // Mostrar los días restantes hasta la próxima quincena
  console.log('Días restantes hasta la próxima quincena: ' + daysUntilNextFortnight);

  diasHastaProximoCorte.value = daysUntilNextFortnight + 1;


  // Obtener la cantidad de pago al día
  const pagoDiario = parseFloat(pagoMensualInput.value) / totalDaysInMonth;
  resultadoPagoDiarioModal.value = pagoDiario.toFixed(2);
  pagoDiario2Modal.value = pagoDiario.toFixed(2);


  // Calcular el monto del primer pago según la fecha del préstamo

  console.log(fechaPrestamo.getDate());
  // Verificar si la fecha es válida
  if (!fechaPrestamo || isNaN(fechaPrestamo.getTime())) {
    // Si la fecha no es válida, establecer el valor del monto del primer pago en 0
    montoPrimerPagoInput.value = 0;
    montoPrimerPagoInputModal.value = 0;
    return; // Salir de la función si la fecha no es válida
  }

  else {
    linkProcdmtoModal.classList.remove('inactive');
  }

  let montoPrimerPago = 0;



  const CopiaModalCalculoPrimerPago = modalCalculoPrimerPago.innerHTML;
  console.log(CopiaModalCalculoPrimerPago);
  if (fechaPrestamo.getDate() === 1 || fechaPrestamo.getDate() === 15 || fechaPrestamo.getDate() === 30 || fechaPrestamo.getDate() === 31) {
    document.getElementById("linkProcdmtoModal").setAttribute("data-bs-target", "#modalNoCalculo");
    console.log("Es el primer día del mes");
    montoPrimerPago = 0;
    montoPrimerPagoInput.value = pagoQuincenalInput.value; // Redondear a 2 decimales
    montoPrimerPagoInputModal.value = pagoQuincenalInput.value; // Redondear a 2 decimales
    return
  }


  else {
    document.getElementById("linkProcdmtoModal").setAttribute("data-bs-target", "#modalCalculoPrimerPago");
    montoPrimerPago = pagoDiario.toFixed(2) * (daysUntilNextFortnight + 1);
  }


  // Establecer el valor en el campo montoPrimerPago
  montoPrimerPagoInput.value = montoPrimerPago.toFixed(2); // Redondear a 2 decimales
  montoPrimerPagoInputModal.value = montoPrimerPago.toFixed(2); // Redondear a 2 decimales

  mostrarDiasRestanteModal(fechaPrestamo, corteQuincena, nombreMes);


}

function mostrarDiasRestanteModal(fechaPrestamo, corteQuincena, nombreMes) {
  diasRestantesCorteModal.textContent = "Cantidad de días desde el " + fechaPrestamo.getDate() + " de " + nombreMes + " hasta el " + corteQuincena + " de " + nombreMes;
}