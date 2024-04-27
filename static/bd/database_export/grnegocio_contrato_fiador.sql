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
INSERT INTO `contrato_fiador` VALUES (1,1,2,'3','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(2,3,2,'5','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(3,4,1,'5','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(4,7,2,'3','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(5,9,2,'2','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(6,11,1,'4','','<FileStorage: \'\' (\'application/octet-stream\')>',1),(7,13,1,'7','','<FileStorage: \'\' (\'application/octet-stream\')>',1);
/*!40000 ALTER TABLE `contrato_fiador` ENABLE KEYS */;
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
