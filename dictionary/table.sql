CREATE DATABASE /*!32312 IF NOT EXISTS*/ `healthcare` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `healthcare`;

--
-- Table structure for table `Body_Broad_Classification`
--

DROP TABLE IF EXISTS `Body_Broad_Classification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Body_Broad_Classification` (
  `body_part_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`body_part_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Body_Broad_Classification`
--

LOCK TABLES `Body_Broad_Classification` WRITE;
/*!40000 ALTER TABLE `Body_Broad_Classification` DISABLE KEYS */;
/*!40000 ALTER TABLE `Body_Broad_Classification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Body_Detailed_Classification`
--

DROP TABLE IF EXISTS `Body_Detailed_Classification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Body_Detailed_Classification` (
  `body_part_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `broad_classification_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`body_part_id`),
  KEY `broad_classification_id` (`broad_classification_id`),
  CONSTRAINT `Body_Detailed_Classification_ibfk_1` FOREIGN KEY (`broad_classification_id`) REFERENCES `Body_Broad_Classification` (`body_part_id`) ON DELETE CASCADE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Body_Detailed_Classification`
--

LOCK TABLES `Body_Detailed_Classification` WRITE;
/*!40000 ALTER TABLE `Body_Detailed_Classification` DISABLE KEYS */;
/*!40000 ALTER TABLE `Body_Detailed_Classification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Disease`
--

DROP TABLE IF EXISTS `Disease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Disease` (
  `disease_id` int(11) NOT NULL AUTO_INCREMENT,
  `disease_name` varchar(255) NOT NULL,
  `treatment` text,
  `causes` text,
  `prevention` text,
  `description` text,
  `possible complications` text,
  `exams and tests` text,
  PRIMARY KEY (`disease_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Disease`
--

LOCK TABLES `Disease` WRITE;
/*!40000 ALTER TABLE `Disease` DISABLE KEYS */;
/*!40000 ALTER TABLE `Disease` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Disease_Has_Symptom`
--

DROP TABLE IF EXISTS `Disease_Has_Symptom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Disease_Has_Symptom` (
  `disease_id` int(11) NOT NULL,
  `symptom_id` bigint(20) NOT NULL,
  KEY `disease_id` (`disease_id`),
  KEY `symptom_id` (`symptom_id`),
  CONSTRAINT `Disease_Has_Symptom_ibfk_1` FOREIGN KEY (`disease_id`) REFERENCES `Disease` (`disease_id`) ON DELETE CASCADE,
  CONSTRAINT `Disease_Has_Symptom_ibfk_2` FOREIGN KEY (`symptom_id`) REFERENCES `Symptom` (`symptom_id`) ON DELETE CASCADE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Disease_Has_Symptom`
--

LOCK TABLES `Disease_Has_Symptom` WRITE;
/*!40000 ALTER TABLE `Disease_Has_Symptom` DISABLE KEYS */;
/*!40000 ALTER TABLE `Disease_Has_Symptom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Record`
--

DROP TABLE IF EXISTS `Record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Record` (
  `record_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `satisfying` tinyint(4) DEFAULT NULL,
  `comment` text,
  `user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`record_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Record_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Record`
--

LOCK TABLES `Record` WRITE;
/*!40000 ALTER TABLE `Record` DISABLE KEYS */;
/*!40000 ALTER TABLE `Record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Record_Has_Disease`
--

DROP TABLE IF EXISTS `Record_Has_Disease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Record_Has_Disease` (
  `record_id` bigint(20) NOT NULL,
  `disease_id` int(11) NOT NULL,
  KEY `record_id` (`record_id`),
  KEY `disease_id` (`disease_id`),
  CONSTRAINT `Record_Has_Disease_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `Record` (`record_id`) ON DELETE CASCADE,
  CONSTRAINT `Record_Has_Disease_ibfk_2` FOREIGN KEY (`disease_id`) REFERENCES `Disease` (`disease_id`) ON DELETE CASCADE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Record_Has_Disease`
--

LOCK TABLES `Record_Has_Disease` WRITE;
/*!40000 ALTER TABLE `Record_Has_Disease` DISABLE KEYS */;
/*!40000 ALTER TABLE `Record_Has_Disease` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Symptom`
--

DROP TABLE IF EXISTS `Symptom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Symptom` (
  `symptom_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `symptom_name` text NOT NULL,
  `body_parts_1` int(11) DEFAULT NULL,
  `body_parts_2` int(11) DEFAULT NULL,
  `symptom_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`symptom_id`),
  KEY `body_parts_1` (`body_parts_1`),
  KEY `body_parts_2` (`body_parts_2`),
  CONSTRAINT `Symptom_ibfk_1` FOREIGN KEY (`body_parts_1`) REFERENCES `Body_Broad_Classification` (`body_part_id`) ON DELETE CASCADE,
  CONSTRAINT `Symptom_ibfk_2` FOREIGN KEY (`body_parts_2`) REFERENCES `Body_Detailed_Classification` (`body_part_id`) ON DELETE CASCADE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
ALTER TABLE Symptom ADD FULLTEXT INDEX `FullText` (`symptom_name` ASC);
--
-- Dumping data for table `Symptom`
--

LOCK TABLES `Symptom` WRITE;
/*!40000 ALTER TABLE `Symptom` DISABLE KEYS */;
/*!40000 ALTER TABLE `Symptom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `age` tinyint(4) DEFAULT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;