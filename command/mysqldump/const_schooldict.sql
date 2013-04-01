-- MySQL dump 10.13  Distrib 5.5.29, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ProvinceManagement
-- ------------------------------------------------------
-- Server version	5.5.29-0ubuntu0.12.04.2

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
-- Table structure for table `const_schooldict`
--

DROP TABLE IF EXISTS `const_schooldict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `const_schooldict` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `schoolName` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `schoolName` (`schoolName`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `const_schooldict`
--

LOCK TABLES `const_schooldict` WRITE;
/*!40000 ALTER TABLE `const_schooldict` DISABLE KEYS */;
INSERT INTO `const_schooldict` VALUES (1,'东北大学'),(2,'东北财经大学'),(3,'中国刑事警察学院'),(44,'中国医科大学'),(4,'大连东软信息学院'),(5,'大连交通大学'),(6,'大连医科大学'),(7,'大连外国语学院'),(8,'大连大学'),(9,'大连工业大学'),(10,'大连民族学院'),(11,'大连海事大学'),(12,'大连海洋大学'),(13,'大连理工大学'),(14,'大连艺术学院'),(15,'沈阳体育学院'),(16,'沈阳农业大学'),(17,'沈阳化工大学'),(18,'沈阳医学院'),(19,'沈阳大学'),(20,'沈阳工业大学'),(21,'沈阳工程学院'),(22,'沈阳师范大学'),(23,'沈阳建筑大学'),(24,'沈阳理工大学'),(25,'沈阳航空航天大学'),(26,'沈阳药科大学'),(27,'沈阳音乐学院'),(28,'渤海大学'),(29,'辽东学院'),(30,'辽宁中医药大学'),(31,'辽宁何氏医学院'),(32,'辽宁医学院'),(33,'辽宁大学'),(34,'辽宁对外经贸学院'),(35,'辽宁工业大学'),(36,'辽宁工程技术大学'),(37,'辽宁师范大学'),(38,'辽宁石油化工大学'),(39,'辽宁科技大学'),(40,'辽宁科技学院'),(41,'辽宁财贸学院'),(42,'鞍山师范学院'),(43,'鲁迅美术学院');
/*!40000 ALTER TABLE `const_schooldict` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-28 11:26:37
