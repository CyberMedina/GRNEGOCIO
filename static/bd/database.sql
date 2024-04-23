CREATE DATABASE grnegocio;

USE grnegocio;




CREATE TABLE moneda(
  id_moneda INT PRIMARY KEY,
  nombreMoneda VARCHAR(25),
  codigoMoneda VARCHAR(20)
);

CREATE TABLE tasaCambioMoneda(
  id_tasaCambioMoneda INT PRIMARY KEY,
  moneda_origen INT,
  moneda_destino INT,
  cifraTasaCambio DECIMAL(4,2), 
  cifraTasaCambioAnterior DECIMAL(4,2),
  fechaModificacion DATETIME,
  
  FOREIGN KEY (moneda_origen) REFERENCES moneda(id_moneda),
  FOREIGN KEY (moneda_destino) REFERENCES moneda(id_moneda)
);


CREATE TABLE companias_telefonicas(
	id_compania INT PRIMARY KEY,
	nombre_compania VARCHAR(50) NOT NULL,
	fecha_realizacion DATETIME NOT NULL,
	estado INT NOT NULL -- 0 inactivo, 1 activo
);

CREATE TABLE direccion(
  id_direccion INT PRIMARY KEY NOT NULL,
  nombre_direccion VARCHAR(50) NOT NULL,
  direccion_escrita VARCHAR(150) NOT NULL,
  direccion_mapa VARCHAR(500),
  estado INT NOT NULL 
);

CREATE TABLE telefono(
  id_telefono INT PRIMARY KEY,
  id_compania INT NOT NULL,
	nombre_telefono VARCHAR(35) NOT NULL,
  numero_telefono INT NOT NULL,
  estado INT NOT NULL,
  FOREIGN KEY (id_compania) REFERENCES companias_telefonicas(id_compania)
);

CREATE TABLE persona (
	id_persona INT PRIMARY KEY,
	nombres VARCHAR(150) NOT NULL,
	apellidos VARCHAR(150) NOT NULL,
	genero INT NOT NULL, -- 1 Masculino, 2 femenino, 3 otro
	cedula VARCHAR(50) NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  estado INT NOT NULL
);

CREATE TABLE persona_direccion(
	id_persona INT NOT NULL,
	id_direccion INT NOT NULL,
	estado INT NOT NULL,
  PRIMARY KEY (id_persona, id_direccion),
  FOREIGN KEY (id_persona) REFERENCES persona(id_persona),
  FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion)
);

CREATE TABLE direccion_telefono(
  id_direccion INT NOT NULL,
  id_telefono INT NOT NULL,
  estado INT NOT NULL,
  PRIMARY KEY (id_direccion, id_telefono),
  FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion),
  FOREIGN KEY (id_telefono) REFERENCES telefono(id_telefono)
);


CREATE TABLE tipo_cliente(
	id_tipoCliente INT  PRIMARY KEY,
  nombre_tipoCliente VARCHAR(50) NOT NULL, -- inactivo 0, normal 2, especial 3, fiador 4
  estado INT NOT NULL
);

CREATE TABLE cliente (
	id_cliente INT PRIMARY KEY,
  id_persona INT NOT NULL,
  id_tipoCliente INT NOT NULL,
  imagenCliente VARCHAR(500) NOT NULL,
  imagenCedula VARCHAR(500) NOT NULL,
  estado INT NOT NULL,
  FOREIGN KEY (id_persona) REFERENCES persona(id_persona),
  FOREIGN KEY (id_tipoCliente) REFERENCES tipo_cliente(id_tipoCliente)
);

CREATE TABLE contrato_fiador(
  id_contrato_fiador INT PRIMARY KEY,
  id_cliente INT NOT NULL, -- Referncia a los datos del fiador que están en la tabla cliente con estado 4
  estado_civil INT NOT NULL, -- Soltero 1, casado 2, viud@ 3
  nombre_delegacion VARCHAR(100),
  dptoArea_trabajo VARCHAR(80),
  ftoColillaINSS VARCHAR(255) NULL,
  estado INT NOT NULL, -- 5 SIGNIFICA QUE NO TIENE FIADOR
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE contrato(
  id_contrato INT PRIMARY KEY,
  id_cliente INT NOT NULL,
  id_contrato_fiador INT NOT NULL,
  estado_civil INT NOT NULL, -- Soltero 1, casado 2, viud@ 3
  nombre_delegacion VARCHAR(100) NULL,
  dptoArea_trabajo VARCHAR(80) NULL,
  ftoColillaINSS VARCHAR(255) NULL,
  monto_solicitado DECIMAL(10,2) NOT NULL,
  tipo_monedaMonto_solicitado INT NOT NULL,
  tasa_interes DECIMAL(5,2) NOT NULL,
  pagoMensual DECIMAL(10,2) NOT NULL,
  pagoQuincenal DECIMAL(10,2) NOT NULL,
  fechaPrestamo DATE NOT NULL,
  fechaPago DATE NOT NULL,
  intervalo_tiempoPago INT NOT NULL,
  montoPrimerPago DECIMAL(10,2) NOT NULL,
  fechaCreacionContrato DATETIME NOT NULL,
  estado INT NOT NULL, -- 1 activo: 0 inactivo
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_contrato_fiador) REFERENCES contrato_fiador(id_contrato_fiador),
  FOREIGN KEY (tipo_monedaMonto_solicitado) REFERENCES moneda(id_moneda)
);



CREATE TABLE pagos(
   id_pagos INT PRIMARY KEY,
   id_contrato INT NOT NULL,
  id_cliente INT NOT NULL,
  observacion VARCHAR(250) NULL,
  evidencia_pago VARCHAR(280) NULL,
   fecha_pago DATE NOT NULL,
  fecha_realizacion_pago DATETIME NOT NULL,
   estado INT NOT NULL, -- 0 NO HAY PAGO -- 1 completo, -- 2 incompleto
   FOREIGN KEY (id_contrato) REFERENCES contrato(id_contrato),
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- estados en detalles pagos: 1 pago moneda original - 2 pago moneda conversion
CREATE TABLE detalle_pagos(
  id_detalle_pagos INT PRIMARY KEY,
  id_pagos INT NOT NULL,
  id_moneda INT NOT NULL,
  cifraPago DECIMAL(10,2) NOT NULL,
  tasa_conversion DECIMAL(10,2) NULL,
  estado INT NOT NULL, 
  
  FOREIGN KEY (id_pagos) REFERENCES pagos(id_pagos),
  FOREIGN KEY (id_moneda) REFERENCES moneda(id_moneda)
);

CREATE TABLE tipoSaldos_pagos(
  id_tipoSaldos_pagos INT PRIMARY KEY,
  nombreTipoSaldo_pago VARCHAR(50) NOT NULL,
  simboloSaldos_pagos VARCHAR(20) NOT NULL, 
  estado INT NOT NULL
);

CREATE TABLE saldos_pagos(
	id_saldos_pagos INT PRIMARY KEY,
  id_cliente INT NOT NULL,
  id_moneda INT NOT NULL,
  cifraSaldo DECIMAL(10,2) NOT NULL,
  fecha_saldo DATETIME NOT NULL,
  estado INT,
  
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_moneda) REFERENCES moneda(id_moneda)
  
);

SELECT * from saldos_pagos WHERE id_cliente = '1';


CREATE TABLE transacciones_saldos (
    id_transaccion INT PRIMARY KEY,
    id_saldos_pagos INT NOT NULL,
    id_pagos INT NULL,
  	id_moneda INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    tipo_transaccion ENUM('Aumento', 'Disminucion') NOT NULL,
    fecha_transaccion DATETIME NOT NULL,
    FOREIGN KEY (id_saldos_pagos) REFERENCES saldos_pagos(id_saldos_pagos),
  	FOREIGN KEY (id_pagos) REFERENCES pagos(id_pagos)
);


SELECT sp.id_saldos_pagos, m.nombreMoneda, m.codigoMoneda, sp.cifraSaldo 
FROM saldos_pagos sp
JOIN moneda m ON m.id_moneda = sp.id_moneda
JOIN cliente c ON c.id_cliente = sp.id_cliente
WHERE id_tipoSaldos_pagos = 2 AND c.id_cliente = '11'


