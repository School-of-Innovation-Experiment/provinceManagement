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
-- Table structure for table `const_insitutecategory`
--

DROP TABLE IF EXISTS `const_insitutecategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `const_insitutecategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `const_insitutecategory`
--

LOCK TABLES `const_insitutecategory` WRITE;
/*!40000 ALTER TABLE `const_insitutecategory` DISABLE KEYS */;
INSERT INTO `const_insitutecategory` VALUES (22,'交通运输学院'),(1,'人文学院'),(31,'信息科学与技术学院'),(50,'公共卫生学院 '),(2,'公共管理与法学学院'),(37,'公共管理学院'),(35,'公共管理硕士（MPA）教育中心'),(13,'制药科学与技术学院'),(11,'化学学院'),(12,'化工学院'),(14,'化工机械学院'),(49,'口腔医学院 '),(40,'国际经济贸易学院'),(20,'土木工程学院'),(47,'城市与环境学院'),(48,'基础医学院'),(4,'外国语学院'),(7,'工商管理学院'),(24,'工程力学系'),(5,'建筑与艺术学院'),(23,'建设管理系'),(46,'心理学系'),(30,'控制科学与工程学院'),(38,'数学与数量经济学院'),(9,'数学科学学院'),(45,'新闻传播学院'),(44,'旅游与酒店管理学院'),(17,'机械工程学院'),(18,'材料科学与工程学院'),(21,'水利工程学院'),(26,'汽车工程学院'),(41,'法学院'),(10,'物理学院'),(15,'环境科学与技术学院'),(16,'生命科学与技术学院'),(33,'生物医学工程系'),(29,'电子科学与技术学院'),(32,'电气工程学院'),(8,'管理科学与工程学院'),(6,'经济学院'),(36,'统计学院'),(43,'网络教育学院'),(19,'能源与动力学院'),(27,'航空航天学院'),(25,'船舶工程学院'),(51,'药学院 '),(28,'计算机科学与工程学院'),(42,'财政税务学院'),(34,'软件工程学院'),(39,'金融学院'),(3,'马克思主义学院');
/*!40000 ALTER TABLE `const_insitutecategory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-28 10:57:01
