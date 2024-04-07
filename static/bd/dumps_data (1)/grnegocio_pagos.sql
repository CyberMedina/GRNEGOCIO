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
INSERT INTO `pagos` VALUES (6,2,3,'','<FileStorage: \'\' (\'application/octet-stream\')>','2023-11-10','2024-03-23 01:25:14',1),(9,4,7,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-25','2024-03-25 16:12:04',1),(10,4,7,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-25','2024-03-25 16:16:41',1),(12,3,4,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-26','2024-03-26 12:14:10',1),(17,2,3,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-26','2024-03-26 23:11:36',1),(21,4,7,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-19','2024-03-27 15:09:43',1),(22,1,1,'Es su primer pago, por ende la cifra es de 7.16 dólares ','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-28','2024-03-28 01:44:29',1),(25,5,9,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-31','2024-03-31 17:55:40',1),(26,4,7,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-31','2024-03-31 18:21:26',1),(30,1,1,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-19','2024-03-31 21:10:09',1),(32,4,7,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-04','2024-04-04 21:11:49',1),(33,5,9,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-06','2024-04-06 20:12:42',1),(34,5,9,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-06','2024-04-06 20:49:51',0);
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-07 16:05:58
