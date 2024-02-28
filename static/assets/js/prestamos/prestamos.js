

function revision_contrato(){
    let inputsForm1 = document.querySelectorAll(".step-1 input , .step-1 select , .step-1 textarea");
    let inputsForm2 = document.querySelectorAll(".step-2 input , .step-2 select , .step-2 textarea");
    let inputsForm3 = document.querySelectorAll(".step-3 input , .step-3 select , .step-3 textarea");

   

    var formContrato = {};

    inputsForm1.forEach(function(input){
        
        if (input.name == "genero" || input.name == "nombreDireccion" || input.name == "idCompaniTelefonica" || input.name == "nombreTelefono" ) {

            let selected = input.options[input.selectedIndex]

            formContrato[input.name] = selected.text;
        }

        else{
            formContrato[input.name] = input.value;
        }

    });

    inputsForm2.forEach(function(input){

        if (input.name == "estadoCivil" || input.name == "nombreDelegacion" || input.name == "tipoCliente" || input.name == "tipoMonedaMontoSolicitado"  || input.name == "tipoTiempoPlazoSolicitado" ) {

            let selected = input.options[input.selectedIndex]

            formContrato[input.name] = selected.text;
        }

        else{
            formContrato[input.name] = input.value;
        }

    });

    inputsForm3.forEach(function(input){
            
            if (input.name == "generoFiador" || input.name == "nombreDireccionFiador" || input.name == "idCompaniTelefonicaFiador" || input.name == "nombreTelefonoFiador" ) {
    
                let selected = input.options[input.selectedIndex]
    
                formContrato[input.name] = selected.text;
            }
    
            else{
                formContrato[input.name] = input.value;
            }
    
        });
        

    console.log(formContrato);
}

function revision_contrato_HTML(formContrato){

    let html_contrato = document.querySelectorAll(".step-4");






}

