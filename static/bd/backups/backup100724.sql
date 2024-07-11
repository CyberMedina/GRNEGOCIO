CREATE DATABASE  IF NOT EXISTS `grnegocio` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `grnegocio`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: grnegocio
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `backupsbd`
--

DROP TABLE IF EXISTS `backupsbd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backupsbd` (
  `id_backupsBD` int NOT NULL,
  `nombre_backup` varchar(100) NOT NULL,
  `ruta_backup` varchar(255) NOT NULL,
  `fechaHora` datetime NOT NULL,
  PRIMARY KEY (`id_backupsBD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backupsbd`
--

LOCK TABLES `backupsbd` WRITE;
/*!40000 ALTER TABLE `backupsbd` DISABLE KEYS */;
INSERT INTO `backupsbd` VALUES (1,'backup_20240605_222717.sql','D:/Medina Jhonatan/Universidad/ProyectosProgramacion/GRNEGOCIO/static/bd/backups/backup_20240605_222717.sql','2024-06-05 22:27:17');
/*!40000 ALTER TABLE `backupsbd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` int NOT NULL,
  `id_persona` int NOT NULL,
  `id_tipoCliente` int NOT NULL,
  `imagenCliente` varchar(500) NOT NULL,
  `imagenCedula` varchar(500) NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_cliente`),
  KEY `id_persona` (`id_persona`),
  KEY `id_tipoCliente` (`id_tipoCliente`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id_persona`),
  CONSTRAINT `cliente_ibfk_2` FOREIGN KEY (`id_tipoCliente`) REFERENCES `tipo_cliente` (`id_tipoCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,1,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(2,2,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(3,3,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(4,4,3,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(5,5,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(6,6,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(7,7,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(8,8,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(9,9,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(10,10,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(11,11,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(12,12,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(13,13,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(14,14,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(15,15,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(16,16,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(17,18,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(18,19,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(19,20,5,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',5),(20,21,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companias_telefonicas`
--

DROP TABLE IF EXISTS `companias_telefonicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companias_telefonicas` (
  `id_compania` int NOT NULL,
  `nombre_compania` varchar(50) NOT NULL,
  `fecha_realizacion` datetime NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_compania`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companias_telefonicas`
--

LOCK TABLES `companias_telefonicas` WRITE;
/*!40000 ALTER TABLE `companias_telefonicas` DISABLE KEYS */;
INSERT INTO `companias_telefonicas` VALUES (1,'Claro','2024-03-14 22:44:41',1),(2,'Tigo','2024-03-14 22:44:41',1),(3,'Cootel','2024-03-14 22:44:41',1),(4,'YOTA','2024-03-14 22:44:41',1);
/*!40000 ALTER TABLE `companias_telefonicas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contrato`
--

DROP TABLE IF EXISTS `contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contrato` (
  `id_contrato` int NOT NULL,
  `id_cliente` int NOT NULL,
  `id_contrato_fiador` int NOT NULL,
  `estado_civil` int NOT NULL,
  `nombre_delegacion` varchar(100) DEFAULT NULL,
  `dptoArea_trabajo` varchar(80) DEFAULT NULL,
  `ftoColillaINSS` varchar(255) DEFAULT NULL,
  `monto_solicitado` decimal(10,2) NOT NULL,
  `tipo_monedaMonto_solicitado` int NOT NULL,
  `tasa_interes` decimal(5,2) NOT NULL,
  `pagoMensual` decimal(10,2) NOT NULL,
  `pagoQuincenal` decimal(10,2) NOT NULL,
  `fechaPrestamo` date NOT NULL,
  `fechaPago` date NOT NULL,
  `intervalo_tiempoPago` int NOT NULL,
  `montoPrimerPago` decimal(10,2) NOT NULL,
  `fechaCreacionContrato` datetime NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_contrato`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_contrato_fiador` (`id_contrato_fiador`),
  KEY `tipo_monedaMonto_solicitado` (`tipo_monedaMonto_solicitado`),
  CONSTRAINT `contrato_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `contrato_ibfk_2` FOREIGN KEY (`id_contrato_fiador`) REFERENCES `contrato_fiador` (`id_contrato_fiador`),
  CONSTRAINT `contrato_ibfk_3` FOREIGN KEY (`tipo_monedaMonto_solicitado`) REFERENCES `moneda` (`id_moneda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contrato`
--

LOCK TABLES `contrato` WRITE;
/*!40000 ALTER TABLE `contrato` DISABLE KEYS */;
INSERT INTO `contrato` VALUES (1,1,1,1,'4','Yucalteca','<FileStorage: \'\' (\'application/octet-stream\')>',596.00,1,18.00,107.28,53.64,'2024-03-14','2024-09-26',15,7.16,'2024-03-14 23:10:54',1),(2,3,2,2,'2','','<FileStorage: \'\' (\'application/octet-stream\')>',300.00,1,18.00,54.00,27.00,'2024-03-22','2024-12-11',15,16.20,'2024-03-22 00:14:01',1),(3,4,3,1,'5','','<FileStorage: \'\' (\'application/octet-stream\')>',500.00,1,18.00,90.00,45.00,'2024-03-22','2025-07-25',30,27.00,'2024-03-22 00:16:16',1),(4,7,4,1,'1','','<FileStorage: \'\' (\'application/octet-stream\')>',590.00,1,18.00,106.20,53.10,'2024-03-25','2024-09-28',15,21.24,'2024-03-25 16:11:34',1),(5,9,5,2,'4','','<FileStorage: \'\' (\'application/octet-stream\')>',300.00,1,18.00,54.00,27.00,'2024-03-26','2024-11-22',15,9.00,'2024-03-26 23:26:53',1),(6,11,6,1,'3','','<FileStorage: \'\' (\'application/octet-stream\')>',596.00,1,18.00,107.28,53.64,'2024-03-21','2024-11-22',15,35.80,'2024-03-30 23:57:42',1),(7,13,7,2,'7','Informatica','<FileStorage: \'\' (\'application/octet-stream\')>',1077.00,1,15.00,161.55,80.78,'2023-02-21','2023-12-20',15,53.90,'2024-04-27 10:02:09',1),(8,15,8,2,'1','Atenci','<FileStorage: \'\' (\'application/octet-stream\')>',300.00,1,18.00,54.00,27.00,'2024-05-03','2024-11-23',15,23.40,'2024-05-03 21:56:47',2),(9,17,9,1,'6','Informatica','<FileStorage: \'\' (\'application/octet-stream\')>',809.00,1,18.00,145.62,72.81,'2024-05-14','2024-12-31',15,9.70,'2024-06-07 00:47:37',1),(10,15,10,2,'1','Atenci','<FileStorage: \'\' (\'application/octet-stream\')>',550.00,1,18.00,99.00,49.50,'2024-07-02','2024-11-23',15,46.20,'2024-07-02 01:29:19',1);
/*!40000 ALTER TABLE `contrato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contrato_fiador`
--

DROP TABLE IF EXISTS `contrato_fiador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contrato_fiador` (
  `id_contrato_fiador` int NOT NULL,
  `id_cliente` int NOT NULL,
  `estado_civil` int NOT NULL,
  `nombre_delegacion` varchar(100) DEFAULT NULL,
  `dptoArea_trabajo` varchar(80) DEFAULT NULL,
  `ftoColillaINSS` varchar(255) DEFAULT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_contrato_fiador`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `contrato_fiador_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contrato_fiador`
--

LOCK TABLES `contrato_fiador` WRITE;
/*!40000 ALTER TABLE `contrato_fiador` DISABLE KEYS */;
INSERT INTO `contrato_fiador` VALUES (1,1,2,'3','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(2,3,2,'5','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(3,4,1,'5','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(4,7,2,'3','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(5,9,2,'2','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(6,11,1,'4','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(7,13,1,'7','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(8,16,1,'3','Informatica','<FileStorage: \'\' (\'application/octet-stream\')>',1),(9,18,4,'6','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(10,20,1,'3','Informatica','<FileStorage: \'\' (\'application/octet-stream\')>',0);
/*!40000 ALTER TABLE `contrato_fiador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pagos`
--

DROP TABLE IF EXISTS `detalle_pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pagos` (
  `id_detalle_pagos` int NOT NULL,
  `id_pagos` int NOT NULL,
  `id_moneda` int NOT NULL,
  `cifraPago` decimal(10,2) NOT NULL,
  `tasa_conversion` decimal(10,2) DEFAULT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_detalle_pagos`),
  KEY `id_pagos` (`id_pagos`),
  KEY `id_moneda` (`id_moneda`),
  CONSTRAINT `detalle_pagos_ibfk_1` FOREIGN KEY (`id_pagos`) REFERENCES `pagos` (`id_pagos`),
  CONSTRAINT `detalle_pagos_ibfk_2` FOREIGN KEY (`id_moneda`) REFERENCES `moneda` (`id_moneda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pagos`
--

LOCK TABLES `detalle_pagos` WRITE;
/*!40000 ALTER TABLE `detalle_pagos` DISABLE KEYS */;
INSERT INTO `detalle_pagos` VALUES (1,1,1,53.90,NULL,1),(2,2,1,706.13,NULL,1),(3,2,2,25773.88,36.50,2),(4,3,1,21.86,NULL,1),(5,3,2,800.00,36.60,2),(6,4,1,58.92,NULL,1),(7,5,1,60.11,NULL,1),(8,5,2,2200.00,36.60,2),(9,6,1,20.67,NULL,1),(10,7,1,35.52,NULL,1),(11,7,2,1300.00,36.60,2),(12,8,1,45.26,NULL,1),(13,9,1,35.52,NULL,1),(14,9,2,1300.00,36.60,2),(15,10,1,45.26,NULL,1),(16,11,1,80.78,NULL,1),(17,12,1,19.13,NULL,1),(18,12,2,700.00,36.60,2),(19,13,1,61.65,NULL,1),(20,14,1,21.24,NULL,1),(21,15,1,53.10,NULL,1),(22,16,1,23.40,NULL,1),(23,17,1,27.00,NULL,1),(24,18,1,9.70,NULL,1),(25,19,1,72.81,NULL,1),(26,19,2,2664.85,36.60,2),(27,20,1,72.81,NULL,1),(28,21,1,72.81,NULL,1),(29,22,1,80.78,NULL,1),(30,23,1,80.78,NULL,1),(31,24,1,80.78,NULL,1),(32,25,1,80.78,NULL,1),(33,26,1,46.20,NULL,1);
/*!40000 ALTER TABLE `detalle_pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion`
--

DROP TABLE IF EXISTS `direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direccion` (
  `id_direccion` int NOT NULL,
  `nombre_direccion` varchar(50) NOT NULL,
  `direccion_escrita` varchar(150) NOT NULL,
  `direccion_mapa` varchar(500) DEFAULT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_direccion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion`
--

LOCK TABLES `direccion` WRITE;
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` VALUES (1,'1','Semaforos de la julio martinez 2c al norte 2c al e','Semaforos de la julio martinez 2c al norte 2c al e',1),(2,'2','El chilamate ','Semaforos de la julio martinez 2c al norte 2c al e',1),(3,'1','dafsaf','',1),(4,'1','Del 5c al Este 3 c al Oeste','',1),(5,'1','No se xd','',1),(6,'1','NO SE 2','',1),(7,'1','DUDOSA PROCEDENCIA','',1),(8,'1','El chilamate','El chilamate',1),(9,'1','En el mero san judas','',1),(10,'1','El mero San Judas tambi','',1),(11,'1','Del chilamate 3 cuadras arriba','',1),(12,'1','No s','',1),(13,'1','Por el mercado oriental','',1),(14,'1','NO HAY','',1),(15,'1','Hasta el sur','',1),(16,'1','Me gusta el pan','',1),(17,'1','Me gusta el pan','',1),(18,'1','Praderas del doral 4ta Etapa, alueda 3c-633','',1),(19,'1','NO CUENTA CON FIADOR','',1),(20,'1','PRUEBA','',1),(21,'1','Me gusta el pan','',1);
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direccion_telefono`
--

DROP TABLE IF EXISTS `direccion_telefono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direccion_telefono` (
  `id_direccion` int NOT NULL,
  `id_telefono` int NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_direccion`,`id_telefono`),
  KEY `id_telefono` (`id_telefono`),
  CONSTRAINT `direccion_telefono_ibfk_1` FOREIGN KEY (`id_direccion`) REFERENCES `direccion` (`id_direccion`),
  CONSTRAINT `direccion_telefono_ibfk_2` FOREIGN KEY (`id_telefono`) REFERENCES `telefono` (`id_telefono`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direccion_telefono`
--

LOCK TABLES `direccion_telefono` WRITE;
/*!40000 ALTER TABLE `direccion_telefono` DISABLE KEYS */;
INSERT INTO `direccion_telefono` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,1),(12,12,1),(13,13,1),(14,14,1),(15,15,1),(16,16,1),(17,17,1),(18,18,1),(19,19,1),(20,20,1),(21,21,1);
/*!40000 ALTER TABLE `direccion_telefono` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finalizacioncontrato`
--

DROP TABLE IF EXISTS `finalizacioncontrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finalizacioncontrato` (
  `idFinalizacionContrato` int NOT NULL,
  `id_contrato` int DEFAULT NULL,
  `fechaFinalizacion` datetime DEFAULT NULL,
  `observacion` varchar(255) DEFAULT NULL,
  `fechaRealizacionFinalizado` datetime DEFAULT NULL,
  PRIMARY KEY (`idFinalizacionContrato`),
  KEY `id_contrato` (`id_contrato`),
  CONSTRAINT `finalizacioncontrato_ibfk_1` FOREIGN KEY (`id_contrato`) REFERENCES `contrato` (`id_contrato`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finalizacioncontrato`
--

LOCK TABLES `finalizacioncontrato` WRITE;
/*!40000 ALTER TABLE `finalizacioncontrato` DISABLE KEYS */;
/*!40000 ALTER TABLE `finalizacioncontrato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moneda`
--

DROP TABLE IF EXISTS `moneda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moneda` (
  `id_moneda` int NOT NULL,
  `nombreMoneda` varchar(25) DEFAULT NULL,
  `codigoMoneda` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_moneda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moneda`
--

LOCK TABLES `moneda` WRITE;
/*!40000 ALTER TABLE `moneda` DISABLE KEYS */;
INSERT INTO `moneda` VALUES (1,'D','$'),(2,'C','C$');
/*!40000 ALTER TABLE `moneda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos` (
  `id_pagos` int NOT NULL,
  `id_contrato` int NOT NULL,
  `id_cliente` int NOT NULL,
  `observacion` varchar(250) DEFAULT NULL,
  `evidencia_pago` varchar(280) DEFAULT NULL,
  `fecha_pago` date NOT NULL,
  `fecha_realizacion_pago` datetime NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_pagos`),
  KEY `id_contrato` (`id_contrato`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_contrato`) REFERENCES `contrato` (`id_contrato`),
  CONSTRAINT `pagos_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
INSERT INTO `pagos` VALUES (1,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2023-02-17','2024-04-27 10:45:32',3),(2,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-01-31','2024-04-27 15:58:01',0),(3,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-04','2024-04-27 15:58:46',2),(4,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-04','2024-04-27 15:59:15',0),(5,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-20','2024-04-27 16:00:37',2),(6,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-20','2024-04-27 16:01:00',0),(7,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-07','2024-04-27 16:05:02',2),(8,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-07','2024-04-27 16:05:35',0),(9,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-25','2024-04-27 16:09:35',2),(10,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-25','2024-04-27 16:09:49',0),(11,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-15','2024-04-27 16:11:05',0),(12,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-18','2024-04-27 16:11:25',2),(13,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-18','2024-04-27 16:11:46',0),(14,4,7,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-01','2024-04-27 17:28:37',3),(15,4,7,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-27','2024-04-27 17:28:45',1),(16,8,15,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-05-03','2024-05-03 21:57:03',3),(17,8,15,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-06-04','2024-06-04 17:21:59',1),(18,9,17,'Este pago es solamente simb�lico para el sistema, ya que este cuenta es vieja pero hasta ahora se est� ingresando al sistema.','<FileStorage: \'\' (\'application/octet-stream\')>','2023-01-01','2024-06-07 00:48:47',3),(19,9,17,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-05-15','2024-06-07 00:51:21',1),(20,9,17,'Est� pago se realiz� el d�a 06 de Junio de 2024','<FileStorage: \'\' (\'application/octet-stream\')>','2024-05-30','2024-06-07 00:53:18',1),(21,9,17,'T� pagaste $600 d�lares - $400 del capital d�lares \n\nTe quedan $200 d�lares \n\nMenos los intereses al 12 de Mayo $109 d�lares por lo tanto los $91 d�lares que sobran te lo resto a t� deuda que era de $900 d�lares \n\n Saldo a la fecha:�$809','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-30','2024-06-07 00:59:06',1),(22,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-05-15','2024-07-08 23:22:13',0),(23,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-05-30','2024-07-08 23:22:41',0),(24,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-06-15','2024-07-08 23:23:15',0),(25,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-06-30','2024-07-08 23:23:32',0),(26,10,15,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-07-10','2024-07-10 00:40:22',3);
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona`
--

DROP TABLE IF EXISTS `persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona` (
  `id_persona` int NOT NULL,
  `nombres` varchar(150) NOT NULL,
  `apellidos` varchar(150) NOT NULL,
  `genero` int NOT NULL,
  `cedula` varchar(50) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_persona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,'Jhonatan','Medina',1,'001-150902-1014A','2024-03-14',1),(2,'Germ','Medina Mayorga ',1,'201-311045-0008S','2024-03-14',1),(3,'Matilda','Louis',1,'001-211185-003214','2024-03-18',1),(4,'Lidia Celina','Aguirre Santos',2,'201-311045-0008S','2024-03-21',1),(5,'Gloria Del Carmen','Rodriguez Canales',2,'201-311045-0008S','2024-03-22',1),(6,'Ana Gabriel','Montoya Canales',2,'201-311045-0008S','2024-03-22',1),(7,'Marlen del Rosario','Guevara Canales',2,'201-311045-0008S','2024-03-23',1),(8,'Germ','Medina Mayorga',1,'201-311045-0008S','2024-03-25',1),(9,'Denise Nayely ','Marchena Aburto ',1,'','2024-03-25',1),(10,'Gloria Del Carmen','Sobervia',2,'201-150902-1014D','2024-03-26',1),(11,'Chihiro ','Carmona',1,'001-150902-1014A','2024-03-30',1),(12,'Mu','Del carmen',2,'001-150902-1013S','2024-03-30',1),(13,'Juan','Ram',1,'001-000000-0000A','1988-02-10',1),(14,'NO HAY','NO HAY',1,'001-000000-000A','2024-04-27',1),(15,'Marta Gabriela','Lucia Cano',1,'001-189547-002S','2024-05-03',1),(16,'Juan Carlos','Garc',1,'001-150289-008F','2024-05-03',1),(17,'Juan Carlos','Garc',1,'001-150289-008F','2024-05-03',1),(18,'Claudia Jarquin','Martinez',2,'001-281079-0009Y','1979-10-28',1),(19,'NO CUENTA CON FIADOR','NO CUENTA CON FIADOR',3,'000-000000-0000A','2024-06-07',1),(20,'Prueb','Prueba',1,'001-000000-0000A','2024-07-02',1),(21,'Juan Carlos','Garc',1,'001-150289-008F','2024-05-03',1);
/*!40000 ALTER TABLE `persona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_direccion`
--

DROP TABLE IF EXISTS `persona_direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona_direccion` (
  `id_persona` int NOT NULL,
  `id_direccion` int NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_persona`,`id_direccion`),
  KEY `id_direccion` (`id_direccion`),
  CONSTRAINT `persona_direccion_ibfk_1` FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id_persona`),
  CONSTRAINT `persona_direccion_ibfk_2` FOREIGN KEY (`id_direccion`) REFERENCES `direccion` (`id_direccion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_direccion`
--

LOCK TABLES `persona_direccion` WRITE;
/*!40000 ALTER TABLE `persona_direccion` DISABLE KEYS */;
INSERT INTO `persona_direccion` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,1),(12,12,1),(13,13,1),(14,14,1),(15,15,1),(16,16,1),(17,17,1),(18,18,1),(19,19,1),(20,20,1),(21,21,1);
/*!40000 ALTER TABLE `persona_direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saldos_pagos`
--

DROP TABLE IF EXISTS `saldos_pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saldos_pagos` (
  `id_saldos_pagos` int NOT NULL,
  `id_cliente` int NOT NULL,
  `id_moneda` int NOT NULL,
  `cifraSaldo` decimal(10,2) NOT NULL,
  `fecha_saldo` datetime NOT NULL,
  `estado` int DEFAULT NULL,
  PRIMARY KEY (`id_saldos_pagos`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_moneda` (`id_moneda`),
  CONSTRAINT `saldos_pagos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `saldos_pagos_ibfk_2` FOREIGN KEY (`id_moneda`) REFERENCES `moneda` (`id_moneda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saldos_pagos`
--

LOCK TABLES `saldos_pagos` WRITE;
/*!40000 ALTER TABLE `saldos_pagos` DISABLE KEYS */;
INSERT INTO `saldos_pagos` VALUES (1,13,1,-1341.79,'2024-07-08 23:23:32',1),(2,15,1,0.00,'2024-07-08 21:29:45',1);
/*!40000 ALTER TABLE `saldos_pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasacambiomoneda`
--

DROP TABLE IF EXISTS `tasacambiomoneda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasacambiomoneda` (
  `id_tasaCambioMoneda` int NOT NULL,
  `moneda_origen` int DEFAULT NULL,
  `moneda_destino` int DEFAULT NULL,
  `cifraTasaCambio` decimal(4,2) DEFAULT NULL,
  `cifraTasaCambioAnterior` decimal(4,2) DEFAULT NULL,
  `fechaModificacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id_tasaCambioMoneda`),
  KEY `moneda_origen` (`moneda_origen`),
  KEY `moneda_destino` (`moneda_destino`),
  CONSTRAINT `tasacambiomoneda_ibfk_1` FOREIGN KEY (`moneda_origen`) REFERENCES `moneda` (`id_moneda`),
  CONSTRAINT `tasacambiomoneda_ibfk_2` FOREIGN KEY (`moneda_destino`) REFERENCES `moneda` (`id_moneda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasacambiomoneda`
--

LOCK TABLES `tasacambiomoneda` WRITE;
/*!40000 ALTER TABLE `tasacambiomoneda` DISABLE KEYS */;
INSERT INTO `tasacambiomoneda` VALUES (1,1,2,36.60,36.80,'2024-03-19 00:10:51');
/*!40000 ALTER TABLE `tasacambiomoneda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `telefono`
--

DROP TABLE IF EXISTS `telefono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telefono` (
  `id_telefono` int NOT NULL,
  `id_compania` int NOT NULL,
  `nombre_telefono` varchar(35) NOT NULL,
  `numero_telefono` int NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_telefono`),
  KEY `id_compania` (`id_compania`),
  CONSTRAINT `telefono_ibfk_1` FOREIGN KEY (`id_compania`) REFERENCES `companias_telefonicas` (`id_compania`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telefono`
--

LOCK TABLES `telefono` WRITE;
/*!40000 ALTER TABLE `telefono` DISABLE KEYS */;
INSERT INTO `telefono` VALUES (1,2,'2',81719517,1),(2,1,'2',87393929,1),(3,1,'1',76785562,1),(4,1,'1',76785562,1),(5,1,'1',85920121,1),(6,1,'1',85920121,1),(7,1,'2',85513587,1),(8,2,'1',87393929,1),(9,2,'2',85920121,1),(10,1,'1',81719517,1),(11,2,'2',85920121,1),(12,2,'2',76789975,1),(13,2,'2',85636879,1),(14,1,'3',87979879,1),(15,1,'1',85920121,1),(16,1,'2',85920125,1),(17,1,'2',85920125,1),(18,2,'2',85130836,1),(19,1,'3',0,1),(20,1,'1',11111111,1),(21,1,'2',85920125,1);
/*!40000 ALTER TABLE `telefono` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_cliente`
--

DROP TABLE IF EXISTS `tipo_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_cliente` (
  `id_tipoCliente` int NOT NULL,
  `nombre_tipoCliente` varchar(50) NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_tipoCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_cliente`
--

LOCK TABLES `tipo_cliente` WRITE;
/*!40000 ALTER TABLE `tipo_cliente` DISABLE KEYS */;
INSERT INTO `tipo_cliente` VALUES (0,'Cliente inactivo',1),(2,'Cliente Normal',1),(3,'Cliente Especial',1),(4,'Cliente Fiador',1),(5,'Cliente en proceso',1);
/*!40000 ALTER TABLE `tipo_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposaldos_pagos`
--

DROP TABLE IF EXISTS `tiposaldos_pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiposaldos_pagos` (
  `id_tipoSaldos_pagos` int NOT NULL,
  `nombreTipoSaldo_pago` varchar(50) NOT NULL,
  `simboloSaldos_pagos` varchar(20) NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id_tipoSaldos_pagos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposaldos_pagos`
--

LOCK TABLES `tiposaldos_pagos` WRITE;
/*!40000 ALTER TABLE `tiposaldos_pagos` DISABLE KEYS */;
INSERT INTO `tiposaldos_pagos` VALUES (1,'A favor','+',1),(2,'En contra','-',1);
/*!40000 ALTER TABLE `tiposaldos_pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacciones_saldos`
--

DROP TABLE IF EXISTS `transacciones_saldos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transacciones_saldos` (
  `id_transaccion` int NOT NULL,
  `id_saldos_pagos` int NOT NULL,
  `id_pagos` int DEFAULT NULL,
  `id_moneda` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `tipo_transaccion` enum('Aumento','Disminucion') NOT NULL,
  `fecha_transaccion` datetime NOT NULL,
  PRIMARY KEY (`id_transaccion`),
  KEY `id_saldos_pagos` (`id_saldos_pagos`),
  KEY `id_pagos` (`id_pagos`),
  CONSTRAINT `transacciones_saldos_ibfk_1` FOREIGN KEY (`id_saldos_pagos`) REFERENCES `saldos_pagos` (`id_saldos_pagos`),
  CONSTRAINT `transacciones_saldos_ibfk_2` FOREIGN KEY (`id_pagos`) REFERENCES `pagos` (`id_pagos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacciones_saldos`
--

LOCK TABLES `transacciones_saldos` WRITE;
/*!40000 ALTER TABLE `transacciones_saldos` DISABLE KEYS */;
INSERT INTO `transacciones_saldos` VALUES (1,1,2,2,-706.13,'Disminucion','2024-04-27 15:58:01'),(2,1,4,1,-58.92,'Disminucion','2024-04-27 15:59:15'),(3,1,6,1,-20.67,'Disminucion','2024-04-27 16:01:00'),(4,1,8,1,-45.26,'Disminucion','2024-04-27 16:05:35'),(5,1,10,1,-45.26,'Disminucion','2024-04-27 16:09:49'),(6,1,11,1,-80.78,'Disminucion','2024-04-27 16:11:05'),(7,1,13,1,-61.65,'Disminucion','2024-04-27 16:11:46'),(8,1,22,1,-80.78,'Disminucion','2024-07-08 23:22:13'),(9,1,23,1,-80.78,'Disminucion','2024-07-08 23:22:41'),(10,1,24,1,-80.78,'Disminucion','2024-07-08 23:23:15'),(11,1,25,1,-80.78,'Disminucion','2024-07-08 23:23:32');
/*!40000 ALTER TABLE `transacciones_saldos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-10 21:56:11
