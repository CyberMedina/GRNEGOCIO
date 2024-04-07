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
INSERT INTO `detalle_pagos` VALUES (6,6,1,27.00,NULL,1),(9,9,1,21.24,NULL,1),(10,10,1,25.96,NULL,1),(11,10,2,950.00,36.60,2),(14,12,1,27.00,NULL,1),(19,17,1,22.00,NULL,1),(23,21,1,53.10,NULL,1),(24,22,1,7.16,NULL,1),(27,25,1,9.00,NULL,1),(28,26,1,5.90,NULL,1),(33,30,1,53.64,NULL,1),(35,32,1,53.10,NULL,1),(36,33,1,27.00,NULL,1),(37,34,1,27.00,NULL,1);
/*!40000 ALTER TABLE `detalle_pagos` ENABLE KEYS */;
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
