-- MySQL dump 10.13  Distrib 8.0.30, for macos12 (x86_64)
--
-- Host: localhost    Database: citas_barbería
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `servicios`
--

DROP TABLE IF EXISTS `servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios` (
  `ID_servicio` int NOT NULL AUTO_INCREMENT,
  `nombre_servicio` varchar(45) NOT NULL,
  `precio` varchar(45) NOT NULL,
  `disponible` varchar(45) NOT NULL,
  PRIMARY KEY (`ID_servicio`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios`
--

LOCK TABLES `servicios` WRITE;
/*!40000 ALTER TABLE `servicios` DISABLE KEYS */;
INSERT INTO `servicios` VALUES (1,'Recorte y Alineado de Bigote','$150','Si'),(2,'Recorte y Alineado de Barba y Bigote','$270','Si'),(3,'Recorte y Alineado de Barba y Bigote','$100','Si'),(4,'Afeitado de Cabeza','$320','Si'),(5,'Corte de Cabello','$330','No'),(6,'Corte de Cabello Niño','$250','Si'),(7,'Corte Express','$250','No'),(8,'Paquete Clásico','$480','Si'),(9,'Paquete Silver','$800','Si'),(10,'Paquete Gold','$950','Si'),(11,'Parches de Colágeno Anti-Ojeras','$100','Si'),(13,'Mascarilla Negra de Carbón','$170','SI'),(15,'Mascarilla Negra de Yogurt','$250','Si'),(16,'Mascarilla de Oro Colágeno Líquida','$320','Si'),(17,'Mascarilla Colágeno de Oro','$370','Si'),(18,'Facial Limpieza Profunda','$770','Si'),(19,'Facial Colágeno','$870','Si'),(20,'Paquete Platinum Spa','$1200','Si'),(21,'Paquete Padre Santo VIP','$1500','Si'),(22,'Tinte Cabello','$370','Si'),(23,'Tinte Barba','$220','Si'),(24,'Tinte Cabello y Barba','$530','Si'),(25,'Corte Dama','$300','No');
/*!40000 ALTER TABLE `servicios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-09  7:50:54
