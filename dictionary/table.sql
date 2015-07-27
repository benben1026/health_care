CREATE DATABASE /*!32312 IF NOT EXISTS*/ `healthcare` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `healthcare`;

--
-- Table structure for table `Body_Level1`
--

DROP TABLE IF EXISTS `Body_Level1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Body_Level1` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Body_Level1`
--

LOCK TABLES `Body_Level1` WRITE;
/*!40000 ALTER TABLE `Body_Level1` DISABLE KEYS */;
/*!40000 ALTER TABLE `Body_Level1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Body_Level2`
--

DROP TABLE IF EXISTS `Body_Level2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Body_Level2` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `upper_level_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`upper_level_id`) REFERENCES `Body_Level1` (`id`) ON DELETE CASCADE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Body_Level2`
--

LOCK TABLES `Body_Level2` WRITE;
/*!40000 ALTER TABLE `Body_Level2` DISABLE KEYS */;
/*!40000 ALTER TABLE `Body_Level2` ENABLE KEYS */;
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
  `gender` enum('male', 'female', 'both'),
  `body_part_1` smallint unsigned,
  `body_part_2` smallint unsigned,
  PRIMARY KEY (`disease_id`),
  FOREIGN KEY (`body_part_1`) REFERENCES `Body_Level1`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`body_part_2`) REFERENCES `Body_Level2`(`id`) ON DELETE CASCADE
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
  `symptom_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`symptom_id`)
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
  `email` varchar(50) UNIQUE NOT NULL,
  `password` varchar(64) NOT NULL,
  `age` tinyint(4) DEFAULT NULL,
  `gender` ENUM('male', 'female') DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE INDEX email_index ON User(email);

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;