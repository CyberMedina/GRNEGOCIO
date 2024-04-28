
function imprimirHistorialySaldo() {

  let tiempoLetrasInicioFechaImpresion
  let tiempoLetrasFinFechaImpresion






  let ModalOpcionImprimir = new bootstrap.Modal(document.getElementById('ModalOpcionImprimir'));
  ModalOpcionImprimir.show();
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



