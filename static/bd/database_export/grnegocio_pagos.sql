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
INSERT INTO `pagos` VALUES (1,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2023-02-17','2024-04-27 10:45:32',3),(2,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-01-31','2024-04-27 15:58:01',0),(3,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-04','2024-04-27 15:58:46',2),(4,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-04','2024-04-27 15:59:15',0),(5,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-20','2024-04-27 16:00:37',2),(6,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-02-20','2024-04-27 16:01:00',0),(7,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-07','2024-04-27 16:05:02',2),(8,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-07','2024-04-27 16:05:35',0),(9,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-25','2024-04-27 16:09:35',2),(10,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-03-25','2024-04-27 16:09:49',0),(11,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-15','2024-04-27 16:11:05',0),(12,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-18','2024-04-27 16:11:25',2),(13,7,13,'','<FileStorage: \'\' (\'application/octet-stream\')>','2024-04-18','2024-04-27 16:11:46',0);
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

-- Dump completed on 2024-04-27 16:18:19
