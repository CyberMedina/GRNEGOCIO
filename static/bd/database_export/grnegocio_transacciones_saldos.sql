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

-- Dump completed on 2024-04-23 15:55:41
