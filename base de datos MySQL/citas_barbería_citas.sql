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
-- Table structure for table `citas`
--

DROP TABLE IF EXISTS `citas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `citas` (
  `ID_cita` int NOT NULL AUTO_INCREMENT,
  `ID_cliente` int NOT NULL,
  `ID_servicio` int NOT NULL,
  `ID_empleado` int NOT NULL,
  `horario` time NOT NULL,
  `fecha` date NOT NULL,
  `estatus` varchar(45) NOT NULL DEFAULT 'Pendiente',
  `día` varchar(45) NOT NULL,
  PRIMARY KEY (`ID_cita`),
  KEY `ID_cliente` (`ID_cliente`),
  KEY `ID_servicio` (`ID_servicio`),
  KEY `ID_empleado` (`ID_empleado`),
  KEY `ID_horario` (`horario`),
  CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`ID_cliente`) REFERENCES `clientes` (`ID_cliente`),
  CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`ID_servicio`) REFERENCES `servicios` (`ID_servicio`),
  CONSTRAINT `citas_ibfk_3` FOREIGN KEY (`ID_empleado`) REFERENCES `empleados` (`ID_empleado`),
  CONSTRAINT `citas_ibfk_5` FOREIGN KEY (`ID_empleado`) REFERENCES `empleados` (`ID_empleado`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citas`
--

LOCK TABLES `citas` WRITE;
/*!40000 ALTER TABLE `citas` DISABLE KEYS */;
INSERT INTO `citas` VALUES (1,1,5,4,'11:00:00','2023-01-30','Completado','Lunes'),(2,2,8,3,'12:15:00','2023-01-30','Completado','Lunes'),(3,3,6,5,'17:00:00','2023-01-30','Cancelado','Lunes'),(4,4,4,3,'09:00:00','2023-02-01','Completado','Miércoles'),(6,11,22,5,'13:45:00','2023-02-01','Cancelado','Miércoles'),(7,13,11,2,'16:30:00','2023-02-02','Completado','Jueves'),(8,10,9,3,'12:45:00','2023-02-03','Completado','Viernes'),(9,8,7,5,'14:30:00','2023-02-03','Completado','Viernes'),(10,7,5,2,'16:15:00','2023-02-03','Completado','Viernes'),(11,6,18,4,'09:30:00','2023-02-04','Completado','Sábado'),(12,5,1,1,'13:00:00','2023-02-04','Cancelado','Sábado'),(13,15,21,2,'14:30:00','2023-02-04','Completado','Sábado'),(14,16,15,5,'18:15:00','2023-02-04','Completado','Sábado'),(15,17,7,4,'13:00:00','2023-02-05','Completado','Domingo'),(16,13,6,3,'14:45:00','2023-02-05','Pendiente','Domingo'),(17,18,1,1,'09:30:00','2023-02-06','Pendiente','Lunes'),(18,19,17,4,'10:30:00','2023-02-06','Pendiente','Lunes'),(19,2,4,2,'10:15:00','2023-02-07','Completado','Martes'),(20,20,11,1,'14:45:00','2023-02-08','Pendiente','Miércoles'),(21,10,1,2,'14:45:00','2023-02-08','Cancelado','Miércoles'),(23,21,5,4,'10:00:00','2023-02-06','Completado','Lunes'),(24,10,1,4,'09:00:00','2023-02-07','Pendiente','Martes'),(25,15,7,12,'09:00:00','2023-02-04','Pendiente','Sábado'),(26,22,6,4,'17:30:00','2023-02-06','Completado','Lunes'),(27,22,6,12,'18:00:00','2023-02-06','Pendiente','Lunes');
/*!40000 ALTER TABLE `citas` ENABLE KEYS */;
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
