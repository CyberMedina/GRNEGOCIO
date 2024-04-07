CREATE DATABASE  IF NOT EXISTS `grnegocio` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `grnegocio`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: grnegocio
-- ------------------------------------------------------
-- Server version	8.0.33

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
INSERT INTO `contrato` VALUES (1,1,1,1,'4','Yucalteca','<FileStorage: \'\' (\'application/octet-stream\')>',596.00,1,18.00,107.28,53.64,'2024-03-14','2024-09-26',15,7.16,'2024-03-14 23:10:54',1),(2,3,2,2,'2','','<FileStorage: \'\' (\'application/octet-stream\')>',300.00,1,18.00,54.00,27.00,'2024-03-22','2024-12-11',15,16.20,'2024-03-22 00:14:01',1),(3,4,3,1,'5','','<FileStorage: \'\' (\'application/octet-stream\')>',500.00,1,18.00,90.00,45.00,'2024-03-22','2025-07-25',30,27.00,'2024-03-22 00:16:16',1),(4,7,4,1,'1','','<FileStorage: \'\' (\'application/octet-stream\')>',590.00,1,18.00,106.20,53.10,'2024-03-25','2024-09-28',15,21.24,'2024-03-25 16:11:34',1),(5,9,5,2,'4','','<FileStorage: \'\' (\'application/octet-stream\')>',300.00,1,18.00,54.00,27.00,'2024-03-26','2024-11-22',15,9.00,'2024-03-26 23:26:53',1),(6,11,6,1,'3','','<FileStorage: \'\' (\'application/octet-stream\')>',596.00,1,18.00,107.28,53.64,'2024-03-21','2024-11-22',15,35.80,'2024-03-30 23:57:42',1);
/*!40000 ALTER TABLE `contrato` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-07 16:05:57
