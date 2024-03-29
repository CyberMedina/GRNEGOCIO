CREATE DATABASE grnegocio;

USE grnegocio;

-- DROP DATABASE grnegocio;

-- Los estados serán de la siguiente manera
-- 0 inactivo, 1 activos


CREATE TABLE moneda(
  id_moneda INT PRIMARY KEY,
  nombreMoneda VARCHAR(25),
  codigoMoneda VARCHAR(20)
);

CREATE TABLE tasaCambioMoneda(
  id_tasaCambioMoneda INT PRIMARY KEY,
  moneda_origen INT,
  moneda_destino INT,
  cifraTasaCambio DECIMAL(9,5), 
  cifraTasaCambioAnterior DECIMAL(9,5),
  fechaModificacion DATETIME,
  
  FOREIGN KEY (moneda_origen) REFERENCES moneda(id_moneda),
  FOREIGN KEY (moneda_destino) REFERENCES moneda(id_moneda)
);

INSERT INTO tasaCambioMoneda (id_tasaCambioMoneda, moneda_origen, moneda_destino, cifraTasaCambio, cifraTasaCambioAnterior, fechaModificacion)
VALUES
('1', '1', '2', '0.00', '0', NOW());


UPDATE tasaCambioMoneda
SET cifraTasaCambioAnterior = cifraTasaCambio,
    cifraTasaCambio = <nuevo_valor_tasa_cambio>,
    fechaModificacion = NOW()
WHERE id_tasaCambioMoneda = <id_de_la_tasa_a_actualizar>;



SELECT 
		tcm.id_tasaCambioMoneda,
    mc.id_moneda AS id_moneda_origen,
    mc.nombreMoneda AS nombre_moneda_origen,
    mc.codigoMoneda AS codigo_moneda_origen,
    md.id_moneda AS id_moneda_destino,
    md.nombreMoneda AS nombre_moneda_destino,
    md.codigoMoneda AS codigo_moneda_destino,
    tcm.cifraTasaCambio,
    tcm.cifraTasaCambioAnterior,
    tcm.fechaModificacion
FROM 
    tasaCambioMoneda tcm
INNER JOIN 
    moneda mc ON tcm.moneda_origen = mc.id_moneda
INNER JOIN 
    moneda md ON tcm.moneda_destino = md.id_moneda;
    
    
 SELECT 
    
    
 

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
  nombre_tipoCliente VARCHAR(50) NOT NULL, -- NO DEFINIDO 0, cliente_inactivo 1, Normal 2, especial 3 o fiador 4
  estado INT NOT NULL
);

CREATE TABLE cliente (
	id_cliente INT PRIMARY KEY,
  id_persona INT NOT NULL,
  id_tipoCliente INT NOT NULL, -- Normal 1, especial 2 o fiador 3
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
  estado INT NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_contrato_fiador) REFERENCES contrato_fiador(id_contrato_fiador),
  FOREIGN KEY (tipo_monedaMonto_solicitado) REFERENCES moneda(id_moneda)
);


 
CREATE TABLE historial_pagos(
   id_historial_pagos INT PRIMARY KEY,
   id_cliente INT NOT NULL,
   fecha_pago DATETIME NOT NULL,
   estado INT NOT NULL,
   FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);


