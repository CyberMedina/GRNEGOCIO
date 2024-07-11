SELECT COUNT(*) AS Cantidad,
       cl.id_cliente,
       CONCAT(p.nombres, ' ', p.apellidos) AS 'Nombre',
       d.direccion_escrita AS 'Dirección',
       CONCAT(c.nombre_compania, ' ', t.numero_telefono) AS 'Teléfono',
       cl.estado AS 'Estado'
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE cl.estado = '1'
GROUP BY cl.id_cliente, p.nombres, p.apellidos, d.direccion_escrita, c.nombre_compania, t.numero_telefono, cl.estado;


SELECT COUNT (*) AS cantidad
FROM cliente
WHERE estado = '1'

SELECT cl.id_cliente, P.nombres, p.apellidos, p.cedula, p.fecha_nacimiento, p.genero,
d.direccion_escrita, d.direccion_mapa, d.nombre_direccion,
c.nombre_compania, t.nombre_telefono, t.numero_telefono,
cl.imagenCliente, cl.imagenCedula, cl.estado
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE
cl.id_cliente = '13'
AND
cl.estado = '1';


SELECT p.id_persona p.nombres, p.apellidos, p.genero p.cedula, p.fecha_nacimiento, p.estado,
d.id_direccion, d.nombre_direccion, d.direccion_escrita, d.direccion_mapa, d.estado,
t.id_telefono, t.id_compania, t.nombre_telefono, t.numero_telefono, t.estado,
pd.id_persona, pd.id_direccion, pd.estado,
dt.id_direccion, dt.id_telefono, dt.estado,
cl.id_cliente, cl.id_persona, cl.tipoCliente, cl.imagenCliente, cl.imagenCedula, cl.estado
FROM persona p
JOIN 



SELECT cl.id_cliente, p.id_persona, p.nombres, p.apellidos, p.cedula, p.fecha_nacimiento, p.genero,
d.direccion_escrita, d.direccion_mapa, d.nombre_direccion,
c.nombre_compania, t.nombre_telefono, t.numero_telefono,
cl.imagenCliente, cl.imagenCedula, cl.estado
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE
cl.id_cliente = '6'

SELECT pd.id_direccion, dt.id_telefono
FROM persona p
JOIN persona_direccion pd ON p.id_persona = pd.id_persona 
JOIN direccion_telefono dt ON pd.id_direccion = dt.id_direccion
WHERE p.id_persona = '20'
AND p.estado = '1';

SELECT d.id_direccion, t.id_telefono
        FROM persona_direccion pd
        JOIN direccion d ON pd.id_direccion = d.id_direccion
        JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
        JOIN telefono t ON dt.id_telefono = t.id_telefono
        WHERE pd.id_persona = '20';




-- SELECT para obtener datos basicos del cliente
SELECT cl.id_cliente, cl.id_tipoCliente, p.nombres, p.apellidos
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
WHERE cl.estado = '1' AND
cl.id_tipoCliente = '2' OR
cl.id_tipoCliente = '3';

-- SELECT para obtener los datos de pago del cliente del contrato
SELECT cl.id_cliente, cl.id_tipoCliente, p.nombres, p.apellidos, m.codigoMoneda,
c.monto_solicitado, c.tasa_interes, c.pagoMensual, c.pagoQuincenal, c.fechaPrestamo,
CASE c.intervalo_tiempoPago
           WHEN 15 THEN 'Quincenal'
           WHEN 30 THEN 'Mensual'
           ELSE 'Desconocido' -- Manejar otros casos si es necesario
       END as tiempo_pago
FROM cliente cl
JOIN contrato c ON cl.id_cliente = c.id_cliente
JOIN persona p ON cl.id_persona = p.id_persona
JOIN moneda m ON c.tipo_monedaMonto_solicitado = m.id_moneda
WHERE
cl.id_cliente = '1';


SET lc_time_names = 'es_ES';

SELECT 
    cl.id_cliente, 
    cl.id_tipoCliente, 
    p.nombres, 
    p.apellidos, 
    m.codigoMoneda,
    c.monto_solicitado, 
    c.tasa_interes, 
    c.pagoMensual, 
    c.pagoQuincenal, 
    DATE_FORMAT(c.fechaPrestamo, '%d de %M de %Y') AS fecha_prestamo_formato,
    tp.nombre_tipoCliente,
    CASE 
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 1 THEN CONCAT(TIMESTAMPDIFF(MINUTE, c.fechaPrestamo, NOW()), ' minutos')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 1 THEN 'hace ayer'
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 24 THEN CONCAT(TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()), ' horas')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 2 THEN 'hace 2 días'
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) < 30 THEN CONCAT(TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()), ' días')
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 mes'
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) < 12 THEN CONCAT(TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()), ' meses')
        WHEN TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 año'
        ELSE CONCAT(TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()), ' años')
    END as fecha_prestamo_desde,
    CASE c.intervalo_tiempoPago
           WHEN 15 THEN 'Quincenal'
           WHEN 30 THEN 'Mensual'
           ELSE 'Desconocido' -- Manejar otros casos si es necesario
       END as tiempo_pago
FROM 
    cliente cl
JOIN 
    contrato c ON cl.id_cliente = c.id_cliente
JOIN 
    persona p ON cl.id_persona = p.id_persona
JOIN 
    moneda m ON c.tipo_monedaMonto_solicitado = m.id_moneda
JOIN
		tipo_cliente tp ON cl.id_tipoCliente = tp.id_tipoCliente
WHERE
    cl.id_cliente = '1';
    
    
    
    SELECT m1.nombreMoneda AS moneda_origen,
       m2.nombreMoneda AS moneda_destino,
       t.cifraOficial,
       t.cifraOficialAnterior,
       t.cifraComercial,
       t.cifraComercialAnterior
FROM tasaCambioMoneda t
INNER JOIN moneda m1 ON t.moneda_origen = m1.id_moneda
INNER JOIN moneda m2 ON t.moneda_destino = m2.id_moneda;


UPDATE contrato
SET estado = '1'
WHERE id_contrato = '9'

UPDATE


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
    cl.id_cliente, 
    cl.id_tipoCliente,
    tp.nombre_tipoCliente,
    p.nombres, 
    p.apellidos, 
    m.codigoMoneda,
    c.intervalo_tiempoPago,
    c.monto_solicitado, 
    c.tasa_interes, 
    c.pagoMensual, 
    c.pagoQuincenal,
    c.fechaPrestamo,
    CASE 
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 1 THEN CONCAT(TIMESTAMPDIFF(MINUTE, c.fechaPrestamo, NOW()), ' minutos')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 1 THEN 'hace ayer'
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 24 THEN CONCAT(TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()), ' horas')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 2 THEN 'hace 2 días'
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) < 30 THEN CONCAT(TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()), ' días')
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 mes'
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) < 12 THEN CONCAT(TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()), ' meses')
        WHEN TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 año'
        ELSE CONCAT(TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()), ' años')
    END as fecha_prestamo_desde,
    CASE c.intervalo_tiempoPago
           WHEN 15 THEN 'Quincenal'
           WHEN 30 THEN 'Mensual'
           ELSE 'Desconocido' -- Manejar otros casos si es necesario
       END as tiempo_pago
FROM 
    cliente cl
JOIN 
    contrato c ON cl.id_cliente = c.id_cliente
JOIN 
    persona p ON cl.id_persona = p.id_persona
JOIN 
    moneda m ON c.tipo_monedaMonto_solicitado = m.id_moneda
JOIN
		tipo_cliente tp ON cl.id_tipoCliente = tp.id_tipoCliente
WHERE
    cl.id_cliente = '4';


SELECT COUNT (*) FROM historial_pagos WHERE id_contrato = '1' AND estado = '1';

SELECT id_contrato FROM contrato WHERE id_cliente = '15' AND estado = '1';

SELECT montoPrimerPago FROM contrato WHERE id_contrato = '1';


CREATE TABLE pagos(
   id_pagos INT PRIMARY KEY,
   id_contrato INT NOT NULL,
  observacion VARCHAR(250) NULL,
  evidencia_pago VARCHAR(280) NULL,
   fecha_pago DATETIME NOT NULL,
  fecha_realizacion_pago DATETIME NOT NULL,
   estado INT NOT NULL,
   FOREIGN KEY (id_contrato) REFERENCES contrato(id_contrato)
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

SELECT 
    p.id_pagos,
    p.observacion, 
    p.evidencia_pago, 
    p.fecha_pago, 
    p.fecha_realizacion_pago,
    p.estado AS 'estado_pagos',
    m.codigoMoneda, 
    m.nombreMoneda, 
    dp.cifraPago, 
    dp.tasa_conversion, 
    dp.estado AS 'estado_detallePagos',
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
    c.estado AS 'estado_contrato'
FROM 
    pagos p
JOIN 
    detalle_pagos dp ON p.id_pagos = dp.id_pagos
JOIN 
    moneda m ON dp.id_moneda = m.id_moneda
JOIN 
    contrato c ON p.id_contrato = c.id_contrato
WHERE 
    p.id_pagos = '1'

    

SELECT YEAR(fecha_pago) AS años FROM pagos WHERE id_contrato = '1'
GROUP BY YEAR(fecha_pago);

SELECT YEAR(p.fecha_pago) AS años
FROM pagos p
JOIN contrato c ON p.id_contrato = c.id_contrato
WHERE p.id_cliente = '1' AND c.estado = '1'
GROUP BY YEAR(p.fecha_pago)
ORDER BY YEAR(p.fecha_pago) DESC ;

SELECT
    p.id_pagos,
    p.observacion, 
    p.evidencia_pago, 
    p.fecha_pago, 
    p.fecha_realizacion_pago,
    p.estado AS estado_pago, 
    m.codigoMoneda, 
    m.nombreMoneda, 
    dp.cifraPago, 
    dp.tasa_conversion,
    dp.estado AS estado_detalle_pago,
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    c.estado
FROM 
    pagos p
JOIN 
    detalle_pagos dp ON p.id_pagos = dp.id_pagos
JOIN 
    moneda m ON dp.id_moneda = m.id_moneda
JOIN 
    contrato c ON p.id_contrato = c.id_contrato
WHERE 
    p.id_cliente = "9" 
    AND p.fecha_pago BETWEEN '2024-01-01' AND '2024-12-31' -- Intervalo de tiempo
    AND c.estado = "1" 
    AND dp.estado = "1"
ORDER BY 
    p.fecha_pago, p.id_pagos ASC;
    
    
    
    
SELECT SUM(cifraPago) 
FROM detalle_pagos dp 
JOIN pagos p ON dp.id_pagos = p.id_pagos 
WHERE id_contrato = '1' 
AND fecha_pago BETWEEN '2024-04-01' AND '2024-04-15' 
AND dp.estado = '1';
 
SELECT (cifraPago) 
FROM detalle_pagos dp 
JOIN pagos p ON dp.id_pagos = p.id_pagos 
WHERE id_contrato = '2' 
AND fecha_pago BETWEEN '2024-03-16' AND '2024-03-30' 
AND dp.estado = '1';

SELECT *
FROM detalle_pagos dp 
JOIN pagos p ON dp.id_pagos = p.id_pagos 
WHERE id_contrato = '6' 
AND fecha_pago BETWEEN '2024-04-1' AND '2024-04-15' 
AND dp.estado = '1'
AND p.estado = 3;

SELECT cl.id_cliente, cl.id_tipoCliente, p.nombres, p.apellidos
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
WHERE cl.estado = '1' AND
cl.id_tipoCliente = '2' OR
cl.id_tipoCliente = '3'


SELECT sp.id_saldos_pagos, m.nombreMoneda, m.codigoMoneda, sp.cifraSaldo 
FROM saldos_pagos sp
JOIN moneda m ON m.id_moneda = sp.id_moneda
JOIN cliente c ON c.id_cliente = sp.id_cliente
WHERE c.id_cliente = '9';


SELECT id_saldos_pagos
FROM saldos_pagos
WHERE id_cliente = '11';


SELECT ts.id_transaccion
FROM saldos_pagos sp
JOIN transacciones_saldos ts ON ts.id_saldos_pagos = sp.id_saldos_pagos
WHERE sp.id_saldos_pagos = '2'





DELETE FROM transacciones_saldos WHERE id_pagos = '4'


SELECT ts.monto, ts.tipo_transaccion FROM transacciones_saldos ts
JOIN saldos_pagos sp ON sp.id_saldos_pagos = ts.id_saldos_pagos
JOIN pagos p ON p.id_cliente = sp.id_cliente
WHERE p.id_pagos = '34'
ORDER BY ts.fecha_transaccion DESC
LIMIT 1;


SELECT id_saldos_pagos
FROM saldos_pagos
WHERE id_cliente = '9'
  AND cifraSaldo > 0;
  
SELECT * FROM saldos_pagos WHERE id_cliente = '9'


SELECT cl.id_cliente, cl.id_tipoCliente, p.nombres, p.apellidos, c.id_contrato, c.pagoMensual, c.pagoQuincenal, cl.estado, c.estado
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN contrato c ON cl.id_cliente = c.id_cliente
WHERE cl.estado = '1' AND
c.estado = '1' AND
cl.id_tipoCliente = '2' OR
cl.id_tipoCliente = '3';


SELECT SUM(cifraPago) 
FROM detalle_pagos dp 
JOIN pagos p ON dp.id_pagos = p.id_pagos 
WHERE id_contrato = '7'
AND fecha_pago BETWEEN '2024-01-31' AND '24-12-31' 
AND dp.estado = '1'
AND (p.estado = '1' OR p.estado = '2' OR p.estado = '4');





SELECT cl.id_cliente, p.id_persona, p.nombres, p.apellidos, p.cedula, p.fecha_nacimiento, p.genero,
d.direccion_escrita, d.direccion_mapa, d.nombre_direccion,
c.nombre_compania, t.nombre_telefono, t.numero_telefono, tc.nombre_tipoCliente,
cl.imagenCliente, cl.imagenCedula, cl.estado
FROM cliente cl
JOIN tipo_cliente tc ON cl.id_tipoCliente = tc.id_tipoCliente
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE
cl.id_cliente = '6'





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



-- SELECIONAR TODOS LOS DATOS DEL CLIENTE
SELECT cl.id_cliente, p.id_persona, p.nombres, p.apellidos, p.cedula, p.fecha_nacimiento, p.genero,
d.direccion_escrita, d.direccion_mapa, d.nombre_direccion,
c.nombre_compania, t.nombre_telefono, t.numero_telefono, tc.nombre_tipoCliente,
cl.imagenCliente, cl.imagenCedula, cl.estado
FROM cliente cl
JOIN tipo_cliente tc ON cl.id_tipoCliente = tc.id_tipoCliente
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE
cl.id_cliente = '11'

-- SELECT PARA LOS DATOS DEL CONTRATO
SELECT c.id_contrato_fiador, c.id_cliente, c.estado_civil, c.nombre_delegacion, c.dptoArea_trabajo, c.ftoColillaINSS,
c.monto_solicitado, c.tipo_monedaMonto_solicitado, c.tasa_interes, c.pagoMensual, c.pagoQuincenal,
c.fechaPrestamo, c.fechaPago, c.montoPrimerPago
FROM contrato c
WHERE id_contrato = '7'


SELECT cf.id_contrato_fiador, cf.id_cliente, cf.estado_civil, cf.nombre_delegacion,
cf.dptoArea_trabajo, cf.ftoColillaINSS, cf.estado
FROM contrato_fiador cf
WHERE cf.id_contrato_fiador = '7'

SELECT cl.id_cliente, p.id_persona, p.nombres, p.apellidos, p.cedula, p.fecha_nacimiento, p.genero,
d.direccion_escrita, d.direccion_mapa, d.nombre_direccion,
c.nombre_compania, t.nombre_telefono, t.numero_telefono, tc.nombre_tipoCliente,
cl.imagenCliente, cl.imagenCedula, cl.estado
FROM cliente cl
JOIN tipo_cliente tc ON cl.id_tipoCliente = tc.id_tipoCliente
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE
cl.id_cliente = '13'



SELECT * FROM backupsbd 
GROUP BY fechaHora


CREATE TABLE backupsBD(
  id_backupsBD INT PRIMARY KEY,
  nombre_backup VARCHAR(100) NOT NULL,
  ruta_backup VARCHAR(255) NOT NULL,
  fechaHora DATETIME NOT NULL
);

SELECT *
FROM backupsBD
ORDER BY fechaHora DESC
LIMIT 1;


SELECT 
    cl.id_cliente, 
    cl.id_tipoCliente,
    tp.nombre_tipoCliente,
    p.nombres, 
    p.apellidos, 
    m.codigoMoneda,
    c.intervalo_tiempoPago,
    c.monto_solicitado, 
    c.tasa_interes, 
    c.pagoMensual, 
    c.pagoQuincenal,
    c.fechaPrestamo,
    CASE 
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 1 THEN CONCAT(TIMESTAMPDIFF(MINUTE, c.fechaPrestamo, NOW()), ' minutos')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 1 THEN 'hace ayer'
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 24 THEN CONCAT(TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()), ' horas')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 2 THEN 'hace 2 días'
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) < 30 THEN CONCAT(TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()), ' días')
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 mes'
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) < 12 THEN CONCAT(TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()), ' meses')
        WHEN TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 año'
        ELSE CONCAT(TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()), ' años')
    END as fecha_prestamo_desde,
    CASE c.intervalo_tiempoPago
           WHEN 15 THEN 'Quincenal'
           WHEN 30 THEN 'Mensual'
           ELSE 'Desconocido' -- Manejar otros casos si es necesario
       END as tiempo_pago
FROM 
    cliente cl
JOIN 
    contrato c ON cl.id_cliente = c.id_cliente
JOIN 
    persona p ON cl.id_persona = p.id_persona
JOIN 
    moneda m ON c.tipo_monedaMonto_solicitado = m.id_moneda
JOIN
		tipo_cliente tp ON cl.id_tipoCliente = tp.id_tipoCliente
WHERE
    cl.id_cliente = '15'
    AND 
    c.estado = '1';




SELECT COUNT(*) 
FROM pagos p
JOIN cliente cl ON p.id_cliente = cl.id_cliente
JOIN contrato c ON cl.id_cliente = c.id_cliente
WHERE
cl.id_cliente = '15' AND
c.estado = '1';

SELECT COUNT(*) 
FROM pagos p
JOIN contrato c ON p.id_contrato = c.id_contrato
WHERE c.id_cliente = '17' AND c.estado = '1';

SELECT COUNT(*) 
        FROM pagos p
        JOIN contrato c ON p.id_contrato = c.id_contrato
        WHERE c.id_cliente = '17' AND c.estado = '1';


SELECT 
    p.id_pagos,
    p.observacion, 
    p.evidencia_pago, 
    p.fecha_pago, 
    p.fecha_realizacion_pago,
    p.estado AS estado_pago, 
    m.codigoMoneda, 
    m.nombreMoneda, 
    dp.cifraPago, 
    dp.tasa_conversion,
    dp.estado AS estado_detalle_pago,
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
    c.estado
FROM 
    pagos p
JOIN 
    detalle_pagos dp ON p.id_pagos = dp.id_pagos
JOIN 
    moneda m ON dp.id_moneda = m.id_moneda
JOIN 
    contrato c ON p.id_contrato = c.id_contrato
WHERE 
    p.id_cliente = :id_cliente 
    AND p.fecha_pago BETWEEN :añoInicio AND :añoFin 
    AND dp.estado = '1'
ORDER BY 
    p.fecha_pago, p.id_pagos ASC;


SELECT cl.id_cliente, cl.id_tipoCliente, p.nombres, p.apellidos, c.id_contrato, c.pagoMensual, c.pagoQuincenal, cl.estado, c.estado
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN contrato c ON cl.id_cliente = c.id_cliente
WHERE cl.estado = '1' AND
c.estado = '1' AND
cl.id_tipoCliente = '2' OR
cl.id_tipoCliente = '3';


SELECT
    p.id_cliente, 
    p.id_pagos,
    p.observacion, 
    p.evidencia_pago, 
    p.fecha_pago, 
    p.fecha_realizacion_pago,
    p.estado AS 'estado_pagos', 
    m.codigoMoneda, 
    m.nombreMoneda, 
    dp.cifraPago, 
    dp.tasa_conversion, 
    dp.estado AS 'estado_detallePagos',
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
    c.estado AS 'estado_contrato'
FROM 
    pagos p
JOIN 
    detalle_pagos dp ON p.id_pagos = dp.id_pagos
JOIN 
    moneda m ON dp.id_moneda = m.id_moneda
JOIN 
    contrato c ON p.id_contrato = c.id_contrato
WHERE 
    p.id_pagos = '22'
    
    
    
    
UPDATE contrato SET estado = 0 
WHERE estado IN (1, 3) AND id_cliente = tu_id_cliente;


SELECT
            p.id_pagos,
            p.observacion, 
            p.evidencia_pago, 
            p.fecha_pago, 
            p.fecha_realizacion_pago,
            p.estado AS estado_pago, 
            m.codigoMoneda, 
            m.nombreMoneda, 
            dp.cifraPago, 
            dp.tasa_conversion,
            dp.estado AS estado_detalle_pago,
            c.id_contrato,
            c.monto_solicitado,
            c.fechaPrestamo,
            c.estado as estado_contrato,
            
            CASE 
                WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
                ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
            END AS descripcion_quincena,
            MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
            c.estado
        FROM 
            pagos p
        JOIN 
            detalle_pagos dp ON p.id_pagos = dp.id_pagos
        JOIN 
            moneda m ON dp.id_moneda = m.id_moneda
        JOIN 
            contrato c ON p.id_contrato = c.id_contrato
        WHERE 
            p.id_cliente = '15' 
            AND p.fecha_pago BETWEEN '2024-01-01' AND '2024-12-31'
            AND c.estado = 1 OR c.estado =2
       
        ORDER BY 
            p.fecha_pago, p.id_pagos ASC;

