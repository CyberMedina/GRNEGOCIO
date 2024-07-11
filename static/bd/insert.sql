USE grnegocio;

INSERT INTO companias_telefonicas(id_compania, nombre_compania, fecha_realizacion, estado) 
VALUES
('1', 'Claro', NOW(), 1),
('2', 'Tigo', NOW(), 1),
('3', 'Cootel', NOW(), 1),
('4', 'YOTA', NOW(), 1);


-- Insertar tipo de cliente
INSERT INTO tipo_cliente(id_tipoCliente, nombre_tipoCliente, estado)
VALUES
(0, 'Cliente inactivo', 1),
(2, 'Cliente Normal', 1),
(3, 'Cliente Especial', 1),
(4, 'Cliente Fiador', 1),
(5, 'Cliente en proceso', 1);



INSERT INTO moneda(id_moneda, nombreMoneda, codigoMoneda)
VALUES
(1, 'Dólares', '$'),
(2, 'Córdobas', 'C$');

INSERT INTO tasaCambioMoneda (id_tasaCambioMoneda, moneda_origen, moneda_destino, cifraTasaCambio, cifraTasaCambioAnterior, fechaModificacion)
VALUES
('1', '1', '2', '0.00', '0', NOW());

INSERT INTO tipoSaldos_pagos (id_tipoSaldos_pagos, nombreTipoSaldo_pago, simboloSaldos_pagos, estado)
VALUES
('1','A favor','+','1'),
('2','En contra','-','1');

