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