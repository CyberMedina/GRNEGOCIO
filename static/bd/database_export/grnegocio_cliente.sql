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
INSERT INTO `cliente` VALUES (1,1,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(2,2,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(3,3,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(4,4,3,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(5,5,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(6,6,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(7,7,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(8,8,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(9,9,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(10,10,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(11,11,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(12,12,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(13,13,2,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1),(14,14,4,'<FileStorage: \'\' (\'application/octet-stream\')>','<FileStorage: \'\' (\'application/octet-stream\')>',1);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-27 16:18:20
