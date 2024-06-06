

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

      if (input.name == "generoFiador" || input.name == "nombreDireccionFiador" || input.name == "idCompaniTelefonicaFiador" || input.name == "nombreTelefonoFiador" || input.name == "estadoCivilFiador" || input.name == "nombreDelegacionFiador") {

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
      "fechaPagoLetras": "plazoSolicitadoRevisionContrato",
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
      "nombreTelefonoFiador": "nombreTelefonoFiadorRevisionContrato",
      "tipoMonedaMontoSolicitado": "tipoMonedaRevisionContrato",
      "tasaInteres": "tasaInteresRevisionContrato",
      "pagoMensual" : "pagoMensualRevisionContrato",
      "pagoQuincenal": "pagoQuincenalRevisionContrato",
      "fechaPrestamo": "fechaPrestamoRevisionContrato",
      "fechaPago": "fechaPagoRevisionContrato",
      "fechaPagoLetras": "fechaPagoLetrasRevisionContrato",
      "montoPrimerPago": "montoPrimerPagoRevisionContrato",
      "IntervaloPagoClienteEspecial": "intervaloTiempoPagoRevisionContrato",



    }

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

    return formContrato;

  }


  var currentStep = 1;
  var updateProgressBar;
  let chckbxNoDeudor = document.getElementById('chckbxNoDeudor');

  // Seleccionar los botones
  var nextStep = document.querySelector(".next-step");
  var prevStep = document.querySelector(".prev-step");


  var datos_fiador = document.getElementById('datos_fiador');

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


          datos_fiador.hidden = false;

          if (currentStep == 3 && chckbxNoDeudor.checked) {
            $(".step-" + currentStep).addClass("animate__animated animate__fadeOutLeft");
            currentStep++;

            revision_contrato();




            datos_fiador.hidden = true;

            setTimeout(function () {
              $(".step").removeClass("animate__animated animate__fadeOutLeft").hide();
              $(".step-" + currentStep).show().addClass("animate__animated animate__fadeInRight");
              updateProgressBar();
            }, 500);
            return;

          }



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
  let tipoClienteComboBox = document.getElementById('tipoCliente');
  let divIntervaloPagoClienteEspecial = document.getElementById('divIntervaloPago');
  let IntervaloPagoClienteEspecial = document.getElementById('IntervaloPagoClienteEspecial');
  let montoSolicitadoInput = document.getElementById('montoSolicitado');
  let tasaInteresInput = document.getElementById('tasaInteres');
  let pagoMensualInput = document.getElementById('pagoMensual');
  let pagoQuincenalInput = document.getElementById('pagoQuincenal');
  let pagoMensualInputModal = document.getElementById('pagoMensualModal');
  let diasHastaProximoCorte = document.getElementById('diasHastaProximoCorte');



  // Obtener los inputs del formulario normal
  let fechaPrestamoInput = document.getElementById('fechaPrestamo');
  let montoPrimerPagoInput = document.getElementById('montoPrimerPago');
  let fechaPagoLetras = document.getElementById('fechaPagoLetras');
  let fechaPago = document.getElementById('fechaPago');


  ///////////////   MODALS //////////////////////////////////////////
  //Obtenemos referencias de las etiquetas a para abrirModals
  const linkProcdmtoModal = document.getElementById('linkProcdmtoModal')

  const montoPrimerPagoInputModal = document.getElementById('montoPrimerPagoModal');

  const resultadoPagoDiarioModal = document.getElementById('resultadoPagoDiarioModal');
  const pagoDiario2Modal = document.getElementById('pagoDiario2Modal');
  const diasRestantesCorteModal = document.getElementById('diasRestantesCorteModal');




  // Agregar un evento de cambio al campo de entrada tipoCliente
  tipoClienteComboBox.addEventListener('change', function () {

    const tipoCliente = tipoClienteComboBox.value;

    if (tipoCliente == "2") {

      divIntervaloPagoClienteEspecial.hidden = true;

    }

    else if (tipoCliente == "3") {
      divIntervaloPagoClienteEspecial.hidden = false;
      IntervaloPagoClienteEspecial.selectedIndex = 1;
    }


  });

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
    else {
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



  fechaPago.addEventListener('change', function () {
    calcularFechaQuincena();
  });



  function calcularFechaQuincena() {

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


    fechaPagoLetras.value = primeraSegundaQuincena;






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


    diasHastaProximoCorte.value = daysUntilNextFortnight + 1;


    // Obtener la cantidad de pago al día
    const pagoDiario = parseFloat(pagoMensualInput.value) / totalDaysInMonth;
    resultadoPagoDiarioModal.value = pagoDiario.toFixed(2);
    pagoDiario2Modal.value = pagoDiario.toFixed(2);



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
    if (fechaPrestamo.getDate() === 1 || fechaPrestamo.getDate() === 15 || fechaPrestamo.getDate() === 30 || fechaPrestamo.getDate() === 31) {
      document.getElementById("linkProcdmtoModal").setAttribute("data-bs-target", "#modalNoCalculo");
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


  function enviarCarta(event) {

    event.preventDefault();

    revision_contrato();

    var contrato = revision_contrato();

    var nombresPrint = contrato.nombres;
    var apellidosPrint = contrato.apellidos;
    var cedulaPrint = contrato.cedula;
    var estadoCivilPrint = contrato.estadoCivil;
    var montoSolicitado = contrato.montoSolicitado;
    var tipoMonedaMontoSolicitadoFiadorPrint = contrato.tipoMonedaMontoSolicitado;
    var fechaPrestamoPrint = contrato.fechaPrestamo;
    var fechaPagoLetrasPrint = contrato.fechaPagoLetras;
    var montoSolicitadoLetras = "";
    var fechaLetras = "";

    async function fetchData() {
      try {
        const dataMontoFetch1 = { fecha: fechaPrestamoPrint };

        // Primer fetch
        const responseMonto = await fetch('/convertir_fechas_a_letras', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(dataMontoFetch1)
        });

        const dataMontoResult = await responseMonto.json();

        fechaLetras = dataMontoResult.fecha_letras;

        // Segundo fetch
        const dataFetch2 = { monto: montoSolicitado };
        const response = await fetch('/convertir_numeros_a_letras', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(dataFetch2)
        });

        const dataResult = await response.json();
        montoSolicitadoLetras = dataResult.monto_letras;

        // Generar contenido HTML y abrir una nueva ventana
        var contenidoHTML = `
        <!DOCTYPE html>
      <html lang="es">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Solicitud de Préstamo</title>
          <style>
              body {
                  font-family: Arial, sans-serif;
                  margin: 2cm 3cm; /* Márgenes similares a una carta */
              }
      
              h2 {
                  text-align: center; /* Centrar los títulos */
                  margin-bottom: 20px; /* Espacio inferior para el título */
              }
      
              p {
      
                  text-align: justify; /* Justificar el texto */
                  margin-bottom: 20px; /* Espacio inferior para los párrafos */
              }
      
              .firmas {
                  display: flex;
                  justify-content: space-between; /* Distribuir las firmas */
                  align-items: flex-start; /* Alinear las firmas arriba */
                  margin-top: 50px; /* Espacio superior para las firmas */
              }
      
              .firmas > div {
                  text-align: center; /* Centrar el contenido de las firmas */
              }
          </style>
      </head>
      <body>
      
          <h2>Solicitud de préstamo</h2>
          <p>Yo, ${nombresPrint} ${apellidosPrint} mayor de edad, ${estadoCivilPrint}, oficinista, con cédula de identidad No. ${cedulaPrint}, y del domicilio de Managua. Por el presente documento hago constar que soy en deberle al señor Germán René Medina Mayorga la suma de ${montoSolicitadoLetras} ${tipoMonedaMontoSolicitadoFiadorPrint} .</p>
          
          <p>Dinero que será cancelado en la ${fechaPagoLetrasPrint}, al mismo tiempo autorizo al señor Medina Mayorga que si no cancelo en la fecha antes estipulada podrá hacerme una demanda judicial en mi contra.</p>
          
          <p>Dado en la ciudad de Managua ${fechaLetras}. Estando ambos de común acuerdo, firmamos una hoja del mismo tenor.</p>
          
          <div class="firmas">
              <div>
                  <p>_________________</p>
                  <p><strong>${nombresPrint} ${apellidosPrint}</strong></p>
                  <p><strong>Deudor</strong></p>
              </div>
              <div>
                  <p>_______________</p>
                  <p><strong>Germán René Medina Mayorga</strong></p>
                  <p><strong>Acreedor</strong></p>
              </div>
          </div>
      
      
          <script>
          // Imprimir la ventana después de cargar el contenido
          window.onload = function() {
              window.print(); // Imprimir la ventana
          };
      </script>
      
      </body>
      </html>
        `;

        var nuevaVentana = window.open('', '_blank');
        nuevaVentana.document.write(contenidoHTML);
        nuevaVentana.document.close(); // Finalizar escritura en la ventana
      } catch (error) {
        console.error('Error:', error);
      }
    }

    // Llamada a la función fetchData
    fetchData();



  }

  function enviarFormulario(event) {
    event.preventDefault();
    // Capturar los valores de los campos
    revision_contrato();

    // Obtener el formulario
    var contrato = revision_contrato();
    var nombresPrint = contrato.nombres;
    var apellidosPrint = contrato.apellidos;
    var cedulaPrint = contrato.cedula;
    var fechaNacPrint = contrato.fechaNac;
    var estadoCivilPrint = contrato.estadoCivil;
    var dptoAreaPrint = contrato.dptoArea;
    var nombreDelegacionPrint = contrato.nombreDelegacion;
    var direccionPrint = contrato.direccion;
    var telefonoPrint = contrato.telefono;



    var montoSolicitado = contrato.montoSolicitado;
    var plazoSolicitado = contrato.plazoSolicitado;
    var tipoTiempoPlazoSolicitadoPrint = contrato.tipoTiempoPlazoSolicitado;
    var tipoMonedaMontoSolicitadoFiadorPrint = contrato.tipoMonedaMontoSolicitado;
    var fechaPrestamoPrint = contrato.fechaPrestamo;
    var fechaPagoLetrasPrint = contrato.fechaPagoLetras;

    var nombresFiadorPrint = contrato.nombresFiador;
    var apellidosFiadorPrint = contrato.apellidosFiador;
    var cedulaFiadorPrint = contrato.cedulaFiador;
    var fechaNacFiadorPrint = contrato.fechaNacFiador;
    var estadiCivilFiadorPrint = contrato.estadoCivilFiador;
    var dptoAreaFiadorPrint = contrato.dptoAreaFiador;
    var nombreDelegacionFiadorPrint = contrato.nombreDelegacionFiador;
    var direccionFiadorPrint = contrato.direccionFiador;
    var telefonoFiadorPrint = contrato.telefonoFiador;


    // Construir el contenido HTML para la nueva ventana
    var contenidoHTML = `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solicitud de Préstamo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 2cm 2cm; /* Márgenes similares a una carta */
        }

        h2 {
            text-align: center; /* Centrar los títulos */
        }

        .firmas {
            display: flex;
            justify-content: center;
            align-items: flex-start; /* Alinear las firmas arriba */
            margin-top: 20px; /* Espacio superior para las firmas */
        }

        .firmas > div {
            margin: 0 10px; /* Ajustar el espacio entre las firmas */
        }

        .firmas p {
            margin: 0;
        }
    </style>
</head>
<body>

<h2>Solicitud de préstamo</h2>
<p><strong>Nombre: </strong>${nombresPrint} ${apellidosPrint}</p>
<p><strong>Cédula: </strong>${cedulaPrint}</p>
<p><strong>Fecha de nacimiento: </strong>${fechaNacPrint}</p>
<p><strong>Estado Civil: </strong>${estadoCivilPrint}</p>
<p><strong>Departamento o área de trabajo: </strong>${dptoAreaPrint}</p>
<p><strong>Nombre de la delegación: </strong>${nombreDelegacionPrint}</p>
<p><strong>Dirección: </strong>${direccionPrint}</p>
<p><strong>Número de teléfono: </strong>${telefonoPrint}</p>

<h2>Datos del préstamo</h2>
<p><strong>Monto solicitado: </strong>$${montoSolicitado} ${tipoMonedaMontoSolicitadoFiadorPrint} </p>
<p><strong>Fecha del préstamo: </strong>${fechaPrestamoPrint}</p>
<p><strong>Fecha de pago: </strong>${fechaPagoLetrasPrint}</p>

<h2>Datos del fiador</h2>
<p><strong>Nombre: </strong>${nombresFiadorPrint} ${apellidosFiadorPrint}</p>
<p><strong>Cédula: </strong>${cedulaFiadorPrint}</p>
<p><strong>Fecha de nacimiento: </strong>${fechaNacFiadorPrint}</p>
<p><strong>Estado Civil: </strong>${estadiCivilFiadorPrint}</p>
<p><strong>Departamento o área de trabajo: </strong>${dptoAreaFiadorPrint}</p>
<p><strong>Nombre de la delegación: </strong>${nombreDelegacionFiadorPrint}</p>
<p><strong>Dirección: </strong>${direccionFiadorPrint}</p>
<p><strong>Número de teléfono: </strong>${telefonoFiadorPrint}</p>

<br>

<div class="firmas">
    <div>
        <p>________________________________</p>
        <br>
        
        <p><strong>Firma deudor</strong></p>
    </div>
    <div>
        <p>________________________________</p>
        <br>
        <p><strong>Firma fiador</strong></p>
    </div>
</div>

<script>
    // Imprimir la ventana después de cargar el contenido
    window.onload = function() {
        window.print(); // Imprimir la ventana
    };
</script>

</body>
</html>
`;

    // Abrir una nueva ventana y escribir el contenido
    var nuevaVentana = window.open('', '_blank');
    nuevaVentana.document.write(contenidoHTML);
    nuevaVentana.document.close(); // Finalizar escritura en la ventana

  }

