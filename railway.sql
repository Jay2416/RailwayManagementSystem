-- MySQL dump 10.13  Distrib 5.1.33, for Win32 (ia32)
--
-- Host: localhost    Database: railway
-- ------------------------------------------------------
-- Server version	5.1.33-community

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `fare`
--

DROP TABLE IF EXISTS `fare`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fare` (
  `t_no` int(20) DEFAULT NULL,
  `arrival_station` varchar(40) DEFAULT NULL,
  `destination` varchar(30) DEFAULT NULL,
  `class` varchar(8) DEFAULT NULL,
  `fare` int(20) DEFAULT NULL,
  KEY `t_no` (`t_no`),
  CONSTRAINT `fare_ibfk_1` FOREIGN KEY (`t_no`) REFERENCES `train` (`t_no`) on update cascade on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fare`
--

LOCK TABLES `fare` WRITE;
/*!40000 ALTER TABLE `fare` DISABLE KEYS */;
INSERT INTO `fare` VALUES (821567,'Vapi','Surat','2',60),(821567,'Vapi','Valsad','1',28),(821567,'Valsad','Surat','1',32),(821567,'Vapi','Surat','1',35),(821567,'Vapi','Valsad','2',25),(821567,'Valsad','Surat','2',26),(670381,'Gandhinagar','Valsad','A/C',88),(670381,'Gandhinagar','Baroda','1',50),(670381,'Baroda','Valsad','1',43),(670381,'Baroda','Valsad','2',36),(670381,'Gandhinagar','Valsad','1',75),(670381,'Gandhinagar','Valsad','2',64),(670381,'Gandhinagar','Baroda','2',45),(853562,'Baroda','Ahmedabad','A/C',90),(853562,'Baroda','Ahmedabad','1',80),(853562,'Baroda','Ahmedabad','2',70),(853562,'Baroda','Rajkot','A/C',120),(853562,'Baroda','Rajkot','1',105),(853562,'Baroda','Rajkot','2',82),(853562,'Ahmedabad','Rajkot','A/C',82),(853562,'Ahmedabad','Rajkot','1',69),(853562,'Ahmedabad','Rajkot','2',60);
/*!40000 ALTER TABLE `fare` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passenger` (
  `pid` varchar(10) NOT NULL,
  `p_name` varchar(30) DEFAULT NULL,
  `t_no` int(20) DEFAULT NULL,
  `arrival` varchar(30) DEFAULT NULL,
  `destination` varchar(20) DEFAULT NULL,
  `class` varchar(8) DEFAULT NULL,
  `jy_date` date DEFAULT NULL,
  `adhar_no` varchar(24) DEFAULT NULL,
  `fare` int(10) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `t_no` (`t_no`),
  CONSTRAINT `passenger_ibfk_1` FOREIGN KEY (`t_no`) REFERENCES `train` (`t_no`) on update cascade on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger`
--

LOCK TABLES `passenger` WRITE;
/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;
INSERT INTO `passenger` VALUES ('183809','Ankita',670381,'Valsad','Baroda','1','2022-02-16','355685412475',43),('226888','Anurag',821567,'Surat','Vapi','2','2022-02-16','124568',60);
/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `train`
--

DROP TABLE IF EXISTS `train`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `train` (
  `t_no` int(20) NOT NULL,
  `t_name` varchar(50) DEFAULT NULL,
  `starting_station` varchar(30) DEFAULT NULL,
  `destination_station` varchar(30) DEFAULT NULL,
  `arrival_time` varchar(20) DEFAULT NULL,
  `reaching_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`t_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `train`
--

LOCK TABLES `train` WRITE;
/*!40000 ALTER TABLE `train` DISABLE KEYS */;
INSERT INTO `train` VALUES (670381,'Janta','Gandhinagar','Valsad','9:00 AM','10:30 AM'),(821567,'Memu','Vapi','Surat','7:00 AM','10:10 AM'),(853562,'Gujarat Express','Baroda','Rajkot','11:20 AM','5:55 PM');
/*!40000 ALTER TABLE `train` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `train_stations`
--

DROP TABLE IF EXISTS `train_stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `train_stations` (
  `t_no` int(20) DEFAULT NULL,
  `t_name` varchar(50) DEFAULT NULL,
  `station` varchar(80) DEFAULT NULL,
  KEY `t_no` (`t_no`),
  CONSTRAINT `train_stations_ibfk_1` FOREIGN KEY (`t_no`) REFERENCES `train` (`t_no`) on update cascade on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `train_stations`
--

LOCK TABLES `train_stations` WRITE;
/*!40000 ALTER TABLE `train_stations` DISABLE KEYS */;
INSERT INTO `train_stations` VALUES (821567,'Memu','Vapi, Valsad, Surat'),(670381,'Janta','Gandhinagar, Baroda, Valsad'),(853562,'Gujarat Express','Baroda, Ahmedabad, Rajkot');
/*!40000 ALTER TABLE `train_stations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-16 17:38:50
