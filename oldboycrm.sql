-- MySQL dump 10.13  Distrib 5.6.19, for osx10.9 (x86_64)
--
-- Host: localhost    Database: oldboycrm
-- ------------------------------------------------------
-- Server version	5.6.26

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'test');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,2),(2,1,3),(3,1,7);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add 用户信息',6,'add_userprofile'),(17,'Can change 用户信息',6,'change_userprofile'),(18,'Can delete 用户信息',6,'delete_userprofile'),(19,'Can add customer',7,'add_customer'),(20,'Can change customer',7,'change_customer'),(21,'Can delete customer',7,'delete_customer'),(22,'Can add consult record',8,'add_consultrecord'),(23,'Can change consult record',8,'change_consultrecord'),(24,'Can delete consult record',8,'delete_consultrecord'),(25,'Can add 交款纪录',9,'add_paymentrecord'),(26,'Can change 交款纪录',9,'change_paymentrecord'),(27,'Can delete 交款纪录',9,'delete_paymentrecord'),(28,'Can add 班级列表',10,'add_classlist'),(29,'Can change 班级列表',10,'change_classlist'),(30,'Can delete 班级列表',10,'delete_classlist'),(31,'Can add 上课纪录',11,'add_courserecord'),(32,'Can change 上课纪录',11,'change_courserecord'),(33,'Can delete 上课纪录',11,'delete_courserecord'),(34,'Can add 学员学习纪录',12,'add_studyrecord'),(35,'Can change 学员学习纪录',12,'change_studyrecord'),(36,'Can delete 学员学习纪录',12,'delete_studyrecord'),(37,'Can add 调查问卷问题列表',13,'add_surveryitem'),(38,'Can change 调查问卷问题列表',13,'change_surveryitem'),(39,'Can delete 调查问卷问题列表',13,'delete_surveryitem'),(40,'Can add 调查问卷',14,'add_survery'),(41,'Can change 调查问卷',14,'change_survery'),(42,'Can delete 调查问卷',14,'delete_survery'),(43,'Can add 调查问卷',15,'add_surveryrecord'),(44,'Can change 调查问卷',15,'change_surveryrecord'),(45,'Can delete 调查问卷',15,'delete_surveryrecord'),(49,'Can add 学员投诉\\建议',17,'add_compliant'),(50,'Can change 学员投诉\\建议',17,'change_compliant'),(51,'Can delete 学员投诉\\建议',17,'delete_compliant'),(52,'Can add 学员常见问题汇总',18,'add_studentfaq'),(53,'Can change 学员常见问题汇总',18,'change_studentfaq'),(54,'Can delete 学员常见问题汇总',18,'delete_studentfaq');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_classlist`
--

DROP TABLE IF EXISTS `crm_classlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_classlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course` varchar(64) NOT NULL,
  `semester` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `graduate_date` date,
  PRIMARY KEY (`id`),
  UNIQUE KEY `crm_classlist_course_419e54df_uniq` (`course`,`semester`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_classlist`
--

LOCK TABLES `crm_classlist` WRITE;
/*!40000 ALTER TABLE `crm_classlist` DISABLE KEYS */;
INSERT INTO `crm_classlist` VALUES (1,'PythonDevOps',12,'2015-12-13','2015-12-27'),(2,'LinuxL2',3,'2015-12-27',NULL);
/*!40000 ALTER TABLE `crm_classlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_classlist_teachers`
--

DROP TABLE IF EXISTS `crm_classlist_teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_classlist_teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classlist_id` int(11) NOT NULL,
  `userprofile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `classlist_id` (`classlist_id`,`userprofile_id`),
  KEY `crm_classl_userprofile_id_13308a9cac9f6e26_fk_crm_userprofile_id` (`userprofile_id`),
  CONSTRAINT `crm_classl_userprofile_id_13308a9cac9f6e26_fk_crm_userprofile_id` FOREIGN KEY (`userprofile_id`) REFERENCES `crm_userprofile` (`id`),
  CONSTRAINT `crm_classlist__classlist_id_35df9e41f3aedc90_fk_crm_classlist_id` FOREIGN KEY (`classlist_id`) REFERENCES `crm_classlist` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_classlist_teachers`
--

LOCK TABLES `crm_classlist_teachers` WRITE;
/*!40000 ALTER TABLE `crm_classlist_teachers` DISABLE KEYS */;
INSERT INTO `crm_classlist_teachers` VALUES (1,1,1),(2,1,2),(3,2,2);
/*!40000 ALTER TABLE `crm_classlist_teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_compliant`
--

DROP TABLE IF EXISTS `crm_compliant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_compliant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `compliant_type` varchar(32) NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` longtext NOT NULL,
  `name` varchar(32) NOT NULL,
  `date` datetime(6) NOT NULL,
  `status` varchar(32) NOT NULL,
  `comment` longtext,
  `dealing_time` datetime(6) DEFAULT NULL,
  `dealer_id` int(11),
  PRIMARY KEY (`id`),
  KEY `crm_compliant_fad77b25` (`dealer_id`),
  CONSTRAINT `crm_compliant_dealer_id_f2784667_fk_crm_userprofile_id` FOREIGN KEY (`dealer_id`) REFERENCES `crm_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_compliant`
--

LOCK TABLES `crm_compliant` WRITE;
/*!40000 ALTER TABLE `crm_compliant` DISABLE KEYS */;
INSERT INTO `crm_compliant` VALUES (1,'compliant','网速太慢','太慢慢慢','alex','2016-01-09 22:13:04.698059','unread','',NULL,NULL),(2,'compliant','我要投诉老男孩老师','我觉得吧，这个不好，那个不好，都 不好','alex','2016-01-09 23:34:16.420755','unread',NULL,NULL,NULL),(3,'suggestion','我要投诉老男孩老师','sdfsfsfsdfsfsddddddddd','alex','2016-01-09 23:37:01.806712','unread',NULL,NULL,NULL),(4,'suggestion','我要投诉老男孩老师','sdfsfsfsdfsfsddddddddd','alex','2016-01-09 23:40:22.799991','unread',NULL,NULL,NULL),(5,'suggestion','我要投诉老男孩老师','sdfsfsfsdfsfsddddddddd','alex','2016-01-09 23:42:03.106797','sovled','开除老男孩','2016-01-09 23:44:33.000000',1),(6,'compliant','老男孩教育在美国纳斯达克成功上市','sdfAlexander  20:27:07\r\nhttp://www.3wedu.net/ \r\nAlexander  20:27:15\r\n我之前的一个同事搞的培训','alex','2016-01-10 04:34:11.010984','unread',NULL,NULL,NULL);
/*!40000 ALTER TABLE `crm_compliant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_consultrecord`
--

DROP TABLE IF EXISTS `crm_consultrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_consultrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `note` longtext NOT NULL,
  `status` int(11) NOT NULL,
  `date` date NOT NULL,
  `consultant_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `crm_consultrecord_ca2bd156` (`consultant_id`),
  KEY `crm_consultrecord_cb24373b` (`customer_id`),
  CONSTRAINT `crm_consultr_consultant_id_74c097e9c676054_fk_crm_userprofile_id` FOREIGN KEY (`consultant_id`) REFERENCES `crm_userprofile` (`id`),
  CONSTRAINT `crm_consultrecord_customer_id_e8baf176580869f_fk_crm_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `crm_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_consultrecord`
--

LOCK TABLES `crm_consultrecord` WRITE;
/*!40000 ALTER TABLE `crm_consultrecord` DISABLE KEYS */;
INSERT INTO `crm_consultrecord` VALUES (1,'又做了跟进。。。',1,'2015-12-13',1,1),(3,'测试',4,'2015-12-13',2,2);
/*!40000 ALTER TABLE `crm_consultrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_courserecord`
--

DROP TABLE IF EXISTS `crm_courserecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_courserecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day_num` int(11) NOT NULL,
  `date` date NOT NULL,
  `course_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `crm_courserecord_course_id_611c2ae3_uniq` (`course_id`,`day_num`),
  KEY `crm_courserecord_d9614d40` (`teacher_id`),
  CONSTRAINT `crm_courserecord_course_id_15d9d0c8_fk_crm_classlist_id` FOREIGN KEY (`course_id`) REFERENCES `crm_classlist` (`id`),
  CONSTRAINT `crm_courserecord_teacher_id_3ace9808_fk_crm_userprofile_id` FOREIGN KEY (`teacher_id`) REFERENCES `crm_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_courserecord`
--

LOCK TABLES `crm_courserecord` WRITE;
/*!40000 ALTER TABLE `crm_courserecord` DISABLE KEYS */;
INSERT INTO `crm_courserecord` VALUES (4,2,'2015-12-27',1,1),(5,1,'2015-12-27',1,1),(6,2,'2015-12-27',2,1),(7,3,'2015-12-28',1,1),(8,4,'2015-12-28',1,1),(9,5,'2015-12-28',1,2),(10,6,'2015-12-28',1,2),(11,7,'2015-12-28',1,1),(12,8,'2015-12-28',1,1),(13,9,'2015-12-28',1,1),(14,10,'2015-12-28',1,1),(15,11,'2015-12-28',1,1),(16,12,'2015-12-28',1,1),(17,13,'2015-12-28',1,1),(18,14,'2015-12-28',1,1),(19,15,'2015-12-28',1,1),(20,16,'2015-12-28',1,1),(21,17,'2015-12-28',1,1),(22,18,'2015-12-28',1,1),(23,19,'2015-12-28',1,1),(24,20,'2015-12-28',1,1),(25,21,'2015-12-28',1,1);
/*!40000 ALTER TABLE `crm_courserecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_customer`
--

DROP TABLE IF EXISTS `crm_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qq` varchar(64) NOT NULL,
  `qq_name` varchar(64) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `source` varchar(64) NOT NULL,
  `course` varchar(64) NOT NULL,
  `class_type` varchar(64) NOT NULL,
  `customer_note` longtext NOT NULL,
  `status` varchar(64) NOT NULL,
  `date` date NOT NULL,
  `consultant_id` int(11) NOT NULL,
  `referral_from_id` int(11),
  `stu_id` varchar(64),
  PRIMARY KEY (`id`),
  UNIQUE KEY `qq` (`qq`),
  KEY `crm_customer_c7eb9c4e` (`consultant_id`),
  KEY `crm_customer_789b85d3` (`referral_from_id`),
  CONSTRAINT `crm_custome_consultant_id_5eaf38ccf6334a90_fk_crm_userprofile_id` FOREIGN KEY (`consultant_id`) REFERENCES `crm_userprofile` (`id`),
  CONSTRAINT `crm_custome_referral_from_id_42e8f5ed7170388e_fk_crm_customer_id` FOREIGN KEY (`referral_from_id`) REFERENCES `crm_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_customer`
--

LOCK TABLES `crm_customer` WRITE;
/*!40000 ALTER TABLE `crm_customer` DISABLE KEYS */;
INSERT INTO `crm_customer` VALUES (1,'32d','sdf','吴天帅',2012738472,'qq','LinuxL1','online','test','unregistered','2015-12-13',1,NULL,''),(2,'333','张三','王浩',NULL,'referral','LinuxL1','offline_weekend','就是随便问一下。。。','paid_in_full','2015-12-13',1,NULL,''),(3,'317828332','Little one','景丽洋',NULL,'referral','LinuxL2','offline_weekend','全报了','signed','2015-12-13',2,1,'333'),(4,'31782833244444','','张杰',NULL,'referral','PythonDevOps','offline_fulltime','这个人只是随便问问，我也不知道 他要不要报','signed','2015-12-13',1,NULL,NULL),(5,'4608','test','Jack',NULL,'qq','PythonDevOps','offline_weekend','sdsfd','signed','2016-01-11',1,NULL,''),(6,'1982','','',NULL,'qq','PythonDevOps','online','fff','signed','2016-01-11',3,NULL,'');
/*!40000 ALTER TABLE `crm_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_customer_class_list`
--

DROP TABLE IF EXISTS `crm_customer_class_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_customer_class_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `classlist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_id` (`customer_id`,`classlist_id`),
  KEY `crm_customer_class_lis_classlist_id_d6308406_fk_crm_classlist_id` (`classlist_id`),
  CONSTRAINT `crm_customer_class_lis_classlist_id_d6308406_fk_crm_classlist_id` FOREIGN KEY (`classlist_id`) REFERENCES `crm_classlist` (`id`),
  CONSTRAINT `crm_customer_class_list_customer_id_bd17a54f_fk_crm_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `crm_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_customer_class_list`
--

LOCK TABLES `crm_customer_class_list` WRITE;
/*!40000 ALTER TABLE `crm_customer_class_list` DISABLE KEYS */;
INSERT INTO `crm_customer_class_list` VALUES (4,1,1),(5,1,2),(2,2,1),(6,2,2),(3,3,1),(7,3,2),(1,4,1),(8,5,1),(9,6,1);
/*!40000 ALTER TABLE `crm_customer_class_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_paymentrecord`
--

DROP TABLE IF EXISTS `crm_paymentrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_paymentrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course` varchar(64) NOT NULL,
  `class_type` varchar(64) NOT NULL,
  `pay_type` varchar(64) NOT NULL,
  `paid_fee` int(11) NOT NULL,
  `note` longtext,
  `date` datetime(6) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `consultant_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `crm_paymentrecord_cb24373b` (`customer_id`),
  KEY `crm_paymentrecord_ca2bd156` (`consultant_id`),
  CONSTRAINT `crm_payment_consultant_id_39e3f657f347c3ee_fk_crm_userprofile_id` FOREIGN KEY (`consultant_id`) REFERENCES `crm_userprofile` (`id`),
  CONSTRAINT `crm_paymentrecor_customer_id_339f7ed43a4ade39_fk_crm_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `crm_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_paymentrecord`
--

LOCK TABLES `crm_paymentrecord` WRITE;
/*!40000 ALTER TABLE `crm_paymentrecord` DISABLE KEYS */;
INSERT INTO `crm_paymentrecord` VALUES (4,'LinuxL1','online','refund',-500,'fsf','2015-12-13 07:09:36.524835',1,1),(5,'LinuxL1','offline_weekend','deposit',77,'','2015-12-13 07:09:55.229107',1,1),(6,'PythonDevOps','offline_weekend','deposit',200,'','2015-12-13 12:29:44.717973',4,1);
/*!40000 ALTER TABLE `crm_paymentrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_studentfaq`
--

DROP TABLE IF EXISTS `crm_studentfaq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_studentfaq` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `solution` longtext NOT NULL,
  `date` datetime(6) NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `crm_studentfaq_4f331e2f` (`author_id`),
  CONSTRAINT `crm_studentfaq_author_id_9906ce1b_fk_crm_userprofile_id` FOREIGN KEY (`author_id`) REFERENCES `crm_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_studentfaq`
--

LOCK TABLES `crm_studentfaq` WRITE;
/*!40000 ALTER TABLE `crm_studentfaq` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_studentfaq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_studyrecord`
--

DROP TABLE IF EXISTS `crm_studyrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_studyrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `record` varchar(64) NOT NULL,
  `score` int(11) NOT NULL,
  `date` datetime(6) NOT NULL,
  `course_record_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `note` varchar(255),
  PRIMARY KEY (`id`),
  UNIQUE KEY `crm_studyrecord_course_record_id_c1b4eb36_uniq` (`course_record_id`,`student_id`),
  KEY `crm_studyrecord_30a811f6` (`student_id`),
  CONSTRAINT `crm_studyrecord_student_id_18b0c323_fk_crm_customer_id` FOREIGN KEY (`student_id`) REFERENCES `crm_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=170 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_studyrecord`
--

LOCK TABLES `crm_studyrecord` WRITE;
/*!40000 ALTER TABLE `crm_studyrecord` DISABLE KEYS */;
INSERT INTO `crm_studyrecord` VALUES (16,'checked',100,'2015-12-27 03:37:05.372554',4,1,NULL),(17,'checked',70,'2015-12-27 03:37:05.376323',4,2,NULL),(18,'checked',50,'2015-12-27 03:37:05.378983',4,4,NULL),(19,'late',-1,'2015-12-27 03:37:05.381559',4,3,NULL),(23,'checked',-1,'2015-12-27 05:18:08.151536',5,1,NULL),(24,'checked',-1,'2015-12-27 05:18:08.156154',5,2,NULL),(25,'checked',-1,'2015-12-27 05:18:08.159358',5,4,NULL),(26,'checked',-1,'2015-12-27 05:18:08.163437',5,3,NULL),(27,'checked',60,'2015-12-27 06:18:09.757620',6,1,NULL),(28,'checked',-1,'2015-12-27 06:18:09.762232',6,2,NULL),(29,'checked',-1,'2015-12-28 18:55:23.133831',7,1,NULL),(30,'checked',-1,'2015-12-28 18:55:23.143011',7,2,NULL),(31,'checked',-1,'2015-12-28 18:55:23.145686',7,4,NULL),(32,'checked',-1,'2015-12-28 18:55:23.148243',7,3,NULL),(33,'checked',-1,'2015-12-28 18:55:34.837208',8,1,NULL),(34,'checked',-1,'2015-12-28 18:55:34.841843',8,2,NULL),(35,'checked',-1,'2015-12-28 18:55:34.844494',8,4,NULL),(36,'checked',-1,'2015-12-28 18:55:34.847134',8,3,NULL),(37,'checked',-1,'2015-12-28 18:55:44.858379',9,1,NULL),(38,'checked',-1,'2015-12-28 18:55:44.863501',9,2,NULL),(39,'checked',-1,'2015-12-28 18:55:44.866167',9,4,NULL),(40,'checked',-1,'2015-12-28 18:55:44.869514',9,3,NULL),(41,'checked',85,'2015-12-28 19:32:22.202059',10,1,NULL),(42,'checked',-1,'2015-12-28 19:32:22.207180',10,2,NULL),(43,'checked',-1000,'2015-12-28 19:32:22.209887',10,4,NULL),(44,'checked',-100,'2015-12-28 19:32:22.212923',10,3,NULL),(45,'checked',-1,'2015-12-28 19:32:28.305423',11,1,NULL),(46,'checked',-1,'2015-12-28 19:32:28.310741',11,2,NULL),(47,'checked',-1,'2015-12-28 19:32:28.314963',11,4,NULL),(48,'checked',-1,'2015-12-28 19:32:28.317628',11,3,NULL),(49,'checked',-1,'2015-12-28 19:32:35.407487',12,1,NULL),(50,'checked',-1,'2015-12-28 19:32:35.413953',12,2,NULL),(51,'checked',-1,'2015-12-28 19:32:35.417302',12,4,NULL),(52,'checked',-1,'2015-12-28 19:32:35.420464',12,3,NULL),(53,'checked',-1,'2015-12-28 19:32:40.531106',13,1,NULL),(54,'checked',-1,'2015-12-28 19:32:40.536376',13,2,NULL),(55,'checked',-1,'2015-12-28 19:32:40.539626',13,4,NULL),(56,'checked',-1,'2015-12-28 19:32:40.542505',13,3,NULL),(57,'checked',-1,'2015-12-28 19:32:45.064066',14,1,NULL),(58,'checked',-1,'2015-12-28 19:32:45.068553',14,2,NULL),(59,'checked',-1,'2015-12-28 19:32:45.071302',14,4,NULL),(60,'checked',-1,'2015-12-28 19:32:45.073870',14,3,NULL),(61,'checked',80,'2015-12-28 19:32:49.460982',15,1,NULL),(62,'checked',-1,'2015-12-28 19:32:49.465929',15,2,NULL),(63,'checked',-1,'2015-12-28 19:32:49.469225',15,4,NULL),(64,'checked',-1,'2015-12-28 19:32:49.471811',15,3,NULL),(65,'checked',-1,'2015-12-28 19:32:53.720445',16,1,NULL),(66,'checked',-1,'2015-12-28 19:32:53.724789',16,2,NULL),(67,'checked',-1,'2015-12-28 19:32:53.727251',16,4,NULL),(68,'checked',-1,'2015-12-28 19:32:53.729876',16,3,NULL),(69,'checked',-1,'2015-12-28 19:34:35.688675',17,1,NULL),(70,'checked',-1,'2015-12-28 19:34:35.694031',17,2,NULL),(71,'checked',-1,'2015-12-28 19:34:35.696647',17,4,NULL),(72,'checked',-1,'2015-12-28 19:34:35.700046',17,3,NULL),(73,'checked',100,'2015-12-28 19:34:43.262016',18,1,NULL),(74,'checked',-1,'2015-12-28 19:34:43.264892',18,2,NULL),(75,'checked',-1,'2015-12-28 19:34:43.267412',18,4,NULL),(76,'checked',-1,'2015-12-28 19:34:43.270031',18,3,NULL),(77,'checked',-1,'2015-12-28 19:34:47.856176',19,1,NULL),(78,'checked',-1,'2015-12-28 19:34:47.860798',19,2,NULL),(79,'checked',-1,'2015-12-28 19:34:47.863481',19,4,NULL),(80,'checked',-1,'2015-12-28 19:34:47.866459',19,3,NULL),(81,'checked',-1,'2015-12-28 19:34:52.517869',20,1,NULL),(82,'checked',-1,'2015-12-28 19:34:52.522531',20,2,NULL),(83,'checked',-1,'2015-12-28 19:34:52.525199',20,4,NULL),(84,'checked',-1,'2015-12-28 19:34:52.527897',20,3,NULL),(85,'checked',-1,'2015-12-28 19:34:59.586429',21,1,NULL),(86,'checked',-1,'2015-12-28 19:34:59.591113',21,2,NULL),(87,'checked',-1,'2015-12-28 19:34:59.593765',21,4,NULL),(88,'checked',40,'2015-12-28 19:34:59.596646',21,3,NULL),(89,'checked',0,'2015-12-28 19:35:05.097906',22,1,NULL),(90,'checked',70,'2015-12-28 19:35:05.102781',22,2,NULL),(91,'checked',80,'2015-12-28 19:35:05.105423',22,4,NULL),(92,'checked',100,'2015-12-28 19:35:05.108659',22,3,NULL),(93,'checked',90,'2015-12-28 19:35:09.761699',23,1,NULL),(94,'checked',85,'2015-12-28 19:35:09.765729',23,2,NULL),(95,'checked',60,'2015-12-28 19:35:09.768338',23,4,NULL),(96,'checked',-1,'2015-12-28 19:35:09.771017',23,3,NULL),(97,'checked',-1,'2015-12-28 19:35:15.347133',24,1,NULL),(98,'checked',-1,'2015-12-28 19:35:15.352337',24,2,NULL),(99,'checked',-1,'2015-12-28 19:35:15.355588',24,4,NULL),(100,'checked',-1,'2015-12-28 19:35:15.358247',24,3,NULL),(101,'checked',-1,'2015-12-28 20:34:58.472816',25,1,NULL),(102,'checked',-1,'2015-12-28 20:34:58.477884',25,2,NULL),(103,'checked',-1,'2015-12-28 20:34:58.480566',25,4,NULL),(104,'checked',-1,'2015-12-28 20:34:58.483126',25,3,NULL),(121,'checked',100,'2016-01-01 18:26:46.440186',6,3,NULL),(122,'checked',-1,'2016-01-11 18:06:23.743652',10,5,NULL),(123,'checked',-1,'2016-01-11 18:06:33.661761',11,5,NULL),(124,'checked',-1,'2016-01-12 04:43:01.943599',25,5,NULL),(125,'checked',-1,'2016-01-12 04:43:01.949655',25,6,NULL),(126,'noshow',-1,'2016-01-12 04:58:39.133361',4,5,NULL),(127,'noshow',-1,'2016-01-12 04:58:39.138393',5,5,NULL),(128,'noshow',-1,'2016-01-12 04:58:39.141183',7,5,NULL),(129,'noshow',-1,'2016-01-12 04:58:39.143923',8,5,NULL),(133,'noshow',-1,'2016-01-12 05:02:36.677544',12,5,NULL),(134,'noshow',-1,'2016-01-12 05:02:36.680830',13,5,NULL),(135,'noshow',-1,'2016-01-12 05:02:36.683976',14,5,NULL),(136,'noshow',-1,'2016-01-12 05:02:36.687083',15,5,NULL),(137,'noshow',-1,'2016-01-12 05:02:36.690082',16,5,NULL),(138,'noshow',-1,'2016-01-12 05:02:36.692797',17,5,NULL),(139,'noshow',-1,'2016-01-12 05:02:36.695425',18,5,NULL),(140,'noshow',-1,'2016-01-12 05:02:36.698098',19,5,NULL),(141,'noshow',-1,'2016-01-12 05:02:36.700862',20,5,NULL),(142,'noshow',-1,'2016-01-12 05:02:36.703709',21,5,NULL),(143,'noshow',-1,'2016-01-12 05:02:36.706387',22,5,NULL),(144,'noshow',-1,'2016-01-12 05:02:36.709407',23,5,NULL),(145,'noshow',-1,'2016-01-12 05:02:36.712320',24,5,NULL),(147,'noshow',-1,'2016-01-12 05:02:36.719180',9,5,NULL),(149,'noshow',-1,'2016-01-12 05:02:36.731948',4,6,NULL),(150,'noshow',-1,'2016-01-12 05:02:36.734882',5,6,NULL),(151,'noshow',-1,'2016-01-12 05:02:36.737636',7,6,NULL),(152,'noshow',-1,'2016-01-12 05:02:36.740357',8,6,NULL),(153,'noshow',-1,'2016-01-12 05:02:36.743090',11,6,NULL),(154,'noshow',-1,'2016-01-12 05:02:36.745835',12,6,NULL),(155,'noshow',-1,'2016-01-12 05:02:36.748473',13,6,NULL),(156,'noshow',-1,'2016-01-12 05:02:36.751890',14,6,NULL),(157,'noshow',-1,'2016-01-12 05:02:36.755489',15,6,NULL),(158,'noshow',-1,'2016-01-12 05:02:36.759333',16,6,NULL),(159,'noshow',-1,'2016-01-12 05:02:36.762256',17,6,NULL),(160,'noshow',-1,'2016-01-12 05:02:36.764991',18,6,NULL),(161,'noshow',-1,'2016-01-12 05:02:36.767750',19,6,NULL),(162,'noshow',-1,'2016-01-12 05:02:36.770486',20,6,NULL),(163,'noshow',-1,'2016-01-12 05:02:36.773184',21,6,NULL),(164,'noshow',-1,'2016-01-12 05:02:36.775879',22,6,NULL),(165,'noshow',-1,'2016-01-12 05:02:36.778614',23,6,NULL),(166,'noshow',-1,'2016-01-12 05:02:36.781255',24,6,NULL),(168,'noshow',-1,'2016-01-12 05:02:36.788201',9,6,NULL),(169,'noshow',-1,'2016-01-12 05:02:36.790875',10,6,NULL);
/*!40000 ALTER TABLE `crm_studyrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_survery`
--

DROP TABLE IF EXISTS `crm_survery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_survery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `date` datetime(6) NOT NULL,
  `by_class_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `crm_survery_by_class_id_8a9f81a6_fk_crm_classlist_id` (`by_class_id`),
  CONSTRAINT `crm_survery_by_class_id_8a9f81a6_fk_crm_classlist_id` FOREIGN KEY (`by_class_id`) REFERENCES `crm_classlist` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_survery`
--

LOCK TABLES `crm_survery` WRITE;
/*!40000 ALTER TABLE `crm_survery` DISABLE KEYS */;
INSERT INTO `crm_survery` VALUES (1,'python 11期第2节课满意度调查','2015-12-27 08:05:36.854063',1),(2,'python 11期第5节课满意度调查','2015-12-27 13:07:14.401800',1),(3,'老男孩教育学员满意度调查','2015-12-29 05:00:10.724808',2);
/*!40000 ALTER TABLE `crm_survery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_survery_questions`
--

DROP TABLE IF EXISTS `crm_survery_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_survery_questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `survery_id` int(11) NOT NULL,
  `surveryitem_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `crm_survery_questions_survery_id_9a0b3540_uniq` (`survery_id`,`surveryitem_id`),
  KEY `crm_survery_questi_surveryitem_id_9936b114_fk_crm_surveryitem_id` (`surveryitem_id`),
  CONSTRAINT `crm_survery_questi_surveryitem_id_9936b114_fk_crm_surveryitem_id` FOREIGN KEY (`surveryitem_id`) REFERENCES `crm_surveryitem` (`id`),
  CONSTRAINT `crm_survery_questions_survery_id_ebc46438_fk_crm_survery_id` FOREIGN KEY (`survery_id`) REFERENCES `crm_survery` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_survery_questions`
--

LOCK TABLES `crm_survery_questions` WRITE;
/*!40000 ALTER TABLE `crm_survery_questions` DISABLE KEYS */;
INSERT INTO `crm_survery_questions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,2,2),(7,2,4),(8,3,1),(9,3,2),(10,3,3),(11,3,4),(12,3,5),(13,3,6),(14,3,7),(15,3,8);
/*!40000 ALTER TABLE `crm_survery_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_surveryitem`
--

DROP TABLE IF EXISTS `crm_surveryitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_surveryitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `anwser_type` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_surveryitem`
--

LOCK TABLES `crm_surveryitem` WRITE;
/*!40000 ALTER TABLE `crm_surveryitem` DISABLE KEYS */;
INSERT INTO `crm_surveryitem` VALUES (1,'你对本课程讲师的满意程度','2015-12-27','score'),(2,'你对学校教学设施的满意程度','2015-12-27','score'),(3,'你愿意向身边的朋友推荐老男孩教育的程度','2015-12-27','score'),(4,'你对课程内容设置的满意程度','2015-12-27','score'),(5,'请写你对我们的其它建议','2015-12-27','suggestion'),(6,'Alex长的有多帅','2015-12-29','score'),(7,'你有多不喜欢共产党','2015-12-29','score'),(8,'学费价格相比课程价格来讲你觉得合理程度怎样','2015-12-29','score');
/*!40000 ALTER TABLE `crm_surveryitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_surveryrecord`
--

DROP TABLE IF EXISTS `crm_surveryrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_surveryrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_name` varchar(255) DEFAULT NULL,
  `score` int(11) NOT NULL,
  `suggestion` longtext,
  `date` datetime(6) NOT NULL,
  `survery_id` int(11) NOT NULL,
  `survery_item_id` int(11) NOT NULL,
  `client_id` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `crm_surveryrecord_survery_id_dfe3774a_fk_crm_survery_id` (`survery_id`),
  KEY `crm_surveryrecord_survery_item_id_e8f5bb48_fk_crm_surveryitem_id` (`survery_item_id`),
  CONSTRAINT `crm_surveryrecord_survery_id_dfe3774a_fk_crm_survery_id` FOREIGN KEY (`survery_id`) REFERENCES `crm_survery` (`id`),
  CONSTRAINT `crm_surveryrecord_survery_item_id_e8f5bb48_fk_crm_surveryitem_id` FOREIGN KEY (`survery_item_id`) REFERENCES `crm_surveryitem` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_surveryrecord`
--

LOCK TABLES `crm_surveryrecord` WRITE;
/*!40000 ALTER TABLE `crm_surveryrecord` DISABLE KEYS */;
INSERT INTO `crm_surveryrecord` VALUES (71,'',7,'','2015-12-27 13:40:58.445850',2,2,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(72,'',8,'','2015-12-27 13:40:58.448383',2,4,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(73,'',4,'tet','2015-12-27 13:41:26.143116',1,1,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(74,'',9,'','2015-12-27 13:41:26.146692',1,3,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(75,'',4,'','2015-12-27 13:41:26.149214',1,2,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(76,'',0,'$(\"#response_data\")$(\"#response_data\")$(\"#response_data\")$(\"#response_data\")$(\"#response_data\")','2015-12-27 13:41:26.151662',1,5,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(77,'',10,'','2015-12-27 13:41:26.152740',1,4,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(78,'张三',10,'http://localhost:8010/crm/survery/1/','2015-12-29 02:54:52.204694',1,1,'Yy77Oz0Xgvwb2DOLl6vX0oQ9UARcI1Yn'),(79,'张三',9,'老师很负责 ','2015-12-29 02:54:52.206825',1,3,'Yy77Oz0Xgvwb2DOLl6vX0oQ9UARcI1Yn'),(80,'张三',2,'学校设施太烂','2015-12-29 02:54:52.208385',1,2,'Yy77Oz0Xgvwb2DOLl6vX0oQ9UARcI1Yn'),(81,'张三',0,'目前都 挺好，不过还需要再观查，哈哈','2015-12-29 02:54:52.224545',1,5,'Yy77Oz0Xgvwb2DOLl6vX0oQ9UARcI1Yn'),(82,'张三',8,'希望更多些实战','2015-12-29 02:54:52.227069',1,4,'Yy77Oz0Xgvwb2DOLl6vX0oQ9UARcI1Yn'),(83,'Alex Li',10,'非常 好','2015-12-29 05:02:18.636557',3,1,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(84,'Alex Li',10,'必须推荐','2015-12-29 05:02:18.640177',3,3,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(85,'Alex Li',1,'除了有桌子，其它的不说了','2015-12-29 05:02:18.643160',3,2,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(86,'Alex Li',0,'垃圾学校,哈呈，不标杆sdfsfskj；要地 标杆 ','2015-12-29 05:02:18.645525',3,5,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(87,'Alex Li',10,'很好','2015-12-29 05:02:18.646885',3,4,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(88,'Alex Li',2,'垃圾政府','2015-12-29 05:02:18.648003',3,7,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(89,'Alex Li',10,'非常帅','2015-12-29 05:02:18.649028',3,6,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(90,'Alex Li',6,'too fucking expensive','2015-12-29 05:02:18.650119',3,8,'8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM'),(91,'',6,'','2015-12-29 21:26:10.031010',3,1,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm'),(92,'',2,'','2015-12-29 21:26:10.036113',3,3,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm'),(93,'',2,'','2015-12-29 21:26:10.037668',3,2,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm'),(94,'',0,'http://127.0.0.1:8010/crm/survery/report/3/http://127.0.0.1:8010/crm/survery/report/3/http://127.0.0.1:8010/crm/survery/report/3/','2015-12-29 21:26:10.039224',3,5,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm'),(95,'',2,'','2015-12-29 21:26:10.040927',3,4,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm'),(96,'',3,'','2015-12-29 21:26:10.042454',3,7,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm'),(97,'',2,'','2015-12-29 21:26:10.046822',3,6,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm'),(98,'',1,'','2015-12-29 21:26:10.050268',3,8,'HbuVTuh5MdEwVlHbqa4u0UaB6E8M09Mm');
/*!40000 ALTER TABLE `crm_surveryrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_userprofile`
--

DROP TABLE IF EXISTS `crm_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `name` varchar(32) NOT NULL,
  `department` varchar(32) DEFAULT NULL,
  `tel` varchar(32) DEFAULT NULL,
  `mobile` varchar(32) DEFAULT NULL,
  `memo` longtext,
  `date_joined` datetime(6) NOT NULL,
  `valid_begin_time` datetime(6) NOT NULL,
  `valid_end_time` datetime(6) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_userprofile`
--

LOCK TABLES `crm_userprofile` WRITE;
/*!40000 ALTER TABLE `crm_userprofile` DISABLE KEYS */;
INSERT INTO `crm_userprofile` VALUES (1,'pbkdf2_sha256$24000$WFdadHx9AEUm$kxSEM9BWrNS9GIjUdj/X32ow1gRzkqgRurXbHfjhQVk=','2016-01-17 08:03:26.307817','317828332@qq.com',1,1,'Alex Li',NULL,NULL,NULL,NULL,'2015-12-13 04:01:59.217359','2015-12-13 04:01:59.065725','2016-03-12 04:01:35.744156',0,NULL),(2,'pbkdf2_sha256$24000$jxlP44jQZQhU$CGFpPvZWTSrAd3iCIJeqb47yVJp291ILwNy/aaGtIlc=',NULL,'rain@126.com',1,1,'Rain Wang','','','','','2015-12-13 07:43:12.684302','2015-12-13 07:43:00.000000','2016-03-12 07:41:00.000000',0,NULL),(3,'pbkdf2_sha256$24000$z0nSWjFwwVgz$wonHqQcb6J5LiTN+1jFc8vrAjCCHyJ+q9UFX5NtpJnk=','2016-01-17 08:16:00.890688','lijie3721@126.com',1,1,'Alex Li',NULL,NULL,NULL,NULL,'2016-01-11 17:16:48.618530','2016-01-11 17:16:48.448769','2016-04-10 17:16:36.285862',0,NULL),(4,'pbkdf2_sha256$24000$vomkv0Sly7Ms$4SeWOI70DAplXcWi0kWbeTGNzNfJusvXX/3ZGJyaXpE=','2016-01-17 08:12:18.819182','t1@126.com',1,0,'t1','','','','','2016-01-17 08:04:59.601261','2016-01-17 08:04:00.000000','2016-04-16 07:59:00.000000',0,NULL);
/*!40000 ALTER TABLE `crm_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_userprofile_groups`
--

DROP TABLE IF EXISTS `crm_userprofile_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_userprofile_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `crm_userprofile_groups_userprofile_id_3639bc47_uniq` (`userprofile_id`,`group_id`),
  KEY `crm_userprofile_groups_group_id_50fd12ae_fk_auth_group_id` (`group_id`),
  CONSTRAINT `crm_userprofile_gr_userprofile_id_c8440cbf_fk_crm_userprofile_id` FOREIGN KEY (`userprofile_id`) REFERENCES `crm_userprofile` (`id`),
  CONSTRAINT `crm_userprofile_groups_group_id_50fd12ae_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_userprofile_groups`
--

LOCK TABLES `crm_userprofile_groups` WRITE;
/*!40000 ALTER TABLE `crm_userprofile_groups` DISABLE KEYS */;
INSERT INTO `crm_userprofile_groups` VALUES (1,2,1);
/*!40000 ALTER TABLE `crm_userprofile_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_userprofile_user_permissions`
--

DROP TABLE IF EXISTS `crm_userprofile_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_userprofile_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `crm_userprofile_user_permissions_userprofile_id_d2888764_uniq` (`userprofile_id`,`permission_id`),
  KEY `crm_userprofile_use_permission_id_28bdda74_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `crm_userprofile_us_userprofile_id_566784f9_fk_crm_userprofile_id` FOREIGN KEY (`userprofile_id`) REFERENCES `crm_userprofile` (`id`),
  CONSTRAINT `crm_userprofile_use_permission_id_28bdda74_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_userprofile_user_permissions`
--

LOCK TABLES `crm_userprofile_user_permissions` WRITE;
/*!40000 ALTER TABLE `crm_userprofile_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_userprofile_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_crm_userprofile_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_crm_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `crm_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2015-12-13 06:45:26.277952','1','QQ:32d,QQName:sdf,Name:df',1,'',7,1),(2,'2015-12-13 06:46:46.516974','1','QQ:32d,QQName:sdf,Name:df',2,'Added 客户跟进记录 \"QQ:32d,QQName:sdf,Name:df, 1\".',7,1),(3,'2015-12-13 07:09:36.527497','1','QQ:32d,QQName:sdf,Name:df',2,'Added 交款纪录 \"QQ:32d,QQName:sdf,Name:df, 类型:deposit,数额:500\".',7,1),(4,'2015-12-13 07:09:55.230024','1','QQ:32d,QQName:sdf,Name:df',2,'Added 交款纪录 \"QQ:32d,QQName:sdf,Name:df, 类型:deposit,数额:77\".',7,1),(5,'2015-12-13 07:13:01.139706','2','QQ:333,QQName:张三,Name:',1,'',7,1),(6,'2015-12-13 07:43:12.685235','2','',1,'',6,1),(7,'2015-12-13 07:50:29.192301','2','',2,'No fields changed.',6,1),(8,'2015-12-13 07:56:36.632915','2','Rain Wang',2,'Changed name.',6,1),(9,'2015-12-13 07:57:21.728188','3','QQ:333,QQName:张三,Name:, 4',1,'',8,1),(10,'2015-12-13 08:18:26.143964','3','QQ:317828332,QQName:Little one,Name:',1,'',7,1),(11,'2015-12-13 08:18:34.557822','3','QQ:317828332,QQName:Little one,Name:',2,'Changed status.',7,1),(12,'2015-12-13 08:19:02.607743','3','QQ:317828332,QQName:Little one,Name:',2,'Changed status.',7,1),(13,'2015-12-13 08:19:07.102797','3','QQ:317828332,QQName:Little one,Name:',2,'Changed status.',7,1),(14,'2015-12-13 08:19:27.938686','2','QQ:333,QQName:张三,Name:',2,'Changed status.',7,1),(15,'2015-12-13 08:19:42.662392','1','QQ:32d,QQName:sdf,Name:df',2,'Changed status.',7,1),(16,'2015-12-13 08:41:42.828484','1','PythonDevOps(12)',1,'',10,1),(17,'2015-12-13 12:29:44.719194','4','QQ:31782833244444,QQName:,Name:',1,'',7,1),(18,'2015-12-13 12:33:22.740115','4','QQ:31782833244444,QQName:,Name:',2,'Changed status and class_list. Changed class_type for 交款纪录 \"QQ:31782833244444,QQName:,Name:, 类型:deposit,数额:200\".',7,1),(19,'2015-12-18 14:20:55.675859','3','Python自动化开发(12) 第1天',1,'Added.',11,1),(20,'2015-12-18 14:21:27.029948','1','QQ:333,QQName:张三,Name:, 4,学员:df,纪录:checked, 得分:C',1,'Added.',12,1),(21,'2015-12-18 14:39:48.058181','2','QQ:32d,QQName:sdf,Name:df, 1,学员:,纪录:late, 得分:C',1,'Added.',12,1),(22,'2015-12-18 14:39:58.293217','3','QQ:32d,QQName:sdf,Name:df, 1,学员:,纪录:checked, 得分:A+',1,'Added.',12,1),(23,'2015-12-18 14:40:09.120484','2','QQ:32d,QQName:sdf,Name:df, 1,学员:,纪录:late, 得分:A',2,'Changed score.',12,1),(24,'2015-12-18 14:40:24.641009','4','QQ:32d,QQName:sdf,Name:df, 1,学员:df,纪录:late, 得分:B+',1,'Added.',12,1),(25,'2015-12-18 14:41:01.729477','5','QQ:333,QQName:张三,Name:, 4,学员:,纪录:late, 得分:B',1,'Added.',12,1),(26,'2015-12-18 14:41:11.375200','6','QQ:32d,QQName:sdf,Name:df, 1,学员:df,纪录:noshow, 得分:B-',1,'Added.',12,1),(27,'2015-12-18 14:41:19.462385','7','QQ:32d,QQName:sdf,Name:df, 1,学员:,纪录:late, 得分:C+',1,'Added.',12,1),(28,'2015-12-18 14:41:29.434175','8','QQ:333,QQName:张三,Name:, 4,学员:,纪录:checked, 得分:C',1,'Added.',12,1),(29,'2015-12-18 14:41:39.310596','9','QQ:333,QQName:张三,Name:, 4,学员:,纪录:checked, 得分:C-',1,'Added.',12,1),(30,'2015-12-18 14:41:46.876657','10','QQ:32d,QQName:sdf,Name:df, 1,学员:,纪录:checked, 得分:D',1,'Added.',12,1),(31,'2015-12-18 14:41:54.130502','11','QQ:333,QQName:张三,Name:, 4,学员:df,纪录:checked, 得分:COPY',1,'Added.',12,1),(32,'2015-12-27 02:40:09.296077','12','QQ:32d,QQName:sdf,Name:df, 1,学员:,纪录:checked, 得分:N/A',1,'Added.',12,1),(33,'2015-12-27 02:43:14.986746','3','Python自动化开发(12) 第1天',2,'No fields changed.',11,1),(34,'2015-12-27 02:49:52.400949','12','QQ:32d,Name:df, 1,学员:,纪录:checked, 得分:N/A',3,'',12,1),(35,'2015-12-27 02:49:52.402846','11','QQ:333,Name:, 4,学员:df,纪录:checked, 得分:COPY',3,'',12,1),(36,'2015-12-27 02:49:52.404011','10','QQ:32d,Name:df, 1,学员:,纪录:checked, 得分:D',3,'',12,1),(37,'2015-12-27 02:49:52.405351','9','QQ:333,Name:, 4,学员:,纪录:checked, 得分:C-',3,'',12,1),(38,'2015-12-27 02:49:52.406668','8','QQ:333,Name:, 4,学员:,纪录:checked, 得分:C',3,'',12,1),(39,'2015-12-27 02:49:52.407795','7','QQ:32d,Name:df, 1,学员:,纪录:late, 得分:C+',3,'',12,1),(40,'2015-12-27 02:49:52.408863','6','QQ:32d,Name:df, 1,学员:df,纪录:noshow, 得分:B-',3,'',12,1),(41,'2015-12-27 02:49:52.409913','5','QQ:333,Name:, 4,学员:,纪录:late, 得分:B',3,'',12,1),(42,'2015-12-27 02:49:52.411032','4','QQ:32d,Name:df, 1,学员:df,纪录:late, 得分:B+',3,'',12,1),(43,'2015-12-27 02:49:52.412232','3','QQ:32d,Name:df, 1,学员:,纪录:checked, 得分:A+',3,'',12,1),(44,'2015-12-27 02:49:52.413644','2','QQ:32d,Name:df, 1,学员:,纪录:late, 得分:A',3,'',12,1),(45,'2015-12-27 02:49:52.415073','1','QQ:333,Name:, 4,学员:df,纪录:checked, 得分:C',3,'',12,1),(46,'2015-12-27 02:51:06.852958','1','QQ:32d,Name:吴天帅',2,'Changed name and customer_note.',7,1),(47,'2015-12-27 02:51:19.452161','2','QQ:333,Name:王浩',2,'Changed name.',7,1),(48,'2015-12-27 02:51:33.186459','3','QQ:317828332,Name:景丽洋',2,'Changed name.',7,1),(49,'2015-12-27 02:51:46.476976','4','QQ:31782833244444,Name:张杰',2,'Changed name.',7,1),(50,'2015-12-27 02:54:08.771641','13','Python自动化开发(12) 第1天,学员:吴天帅,纪录:checked, 得分:N/A',1,'Added.',12,1),(51,'2015-12-27 02:54:16.221747','14','Python自动化开发(12) 第1天,学员:吴天帅,纪录:checked, 得分:N/A',1,'Added.',12,1),(52,'2015-12-27 02:54:27.687861','14','Python自动化开发(12) 第1天,学员:吴天帅,纪录:checked, 得分:N/A',3,'',12,1),(53,'2015-12-27 02:54:27.689526','13','Python自动化开发(12) 第1天,学员:吴天帅,纪录:checked, 得分:N/A',3,'',12,1),(54,'2015-12-27 02:55:34.905018','15','Python自动化开发(12) 第1天,学员:吴天帅,纪录:checked, 得分:N/A',1,'Added.',12,1),(55,'2015-12-27 03:10:34.777545','4','Python自动化开发(12) 第2天',1,'Added.',11,1),(56,'2015-12-27 03:27:20.720199','1','Python自动化开发(12)',2,'Added customer-classlist relationship \"Customer_class_list object\". Added customer-classlist relationship \"Customer_class_list object\". Added customer-classlist relationship \"Customer_class_list object\".',10,1),(57,'2015-12-27 03:43:31.019833','22','Python自动化开发(12) 第1天,学员:景丽洋,纪录:noshow, 成绩:C+',2,'Changed score and record.',12,1),(58,'2015-12-27 03:43:37.306456','19','Python自动化开发(12) 第2天,学员:景丽洋,纪录:late, 成绩:N/A',2,'Changed record.',12,1),(59,'2015-12-27 03:43:37.310022','18','Python自动化开发(12) 第2天,学员:张杰,纪录:checked, 成绩:C',2,'Changed score.',12,1),(60,'2015-12-27 03:43:55.396260','21','Python自动化开发(12) 第1天,学员:张杰,纪录:checked, 成绩:C',2,'Changed score.',12,1),(61,'2015-12-27 03:43:55.399080','20','Python自动化开发(12) 第1天,学员:王浩,纪录:checked, 成绩:B-',2,'Changed score.',12,1),(62,'2015-12-27 03:44:05.053568','17','Python自动化开发(12) 第2天,学员:王浩,纪录:checked, 成绩:B-',2,'Changed score.',12,1),(63,'2015-12-27 03:44:05.056337','16','Python自动化开发(12) 第2天,学员:吴天帅,纪录:checked, 成绩:A+',2,'Changed score.',12,1),(64,'2015-12-27 03:44:05.058971','15','Python自动化开发(12) 第1天,学员:吴天帅,纪录:checked, 成绩:COPY',2,'Changed score.',12,1),(65,'2015-12-27 03:46:21.727726','21','Python自动化开发(12) 第1天,学员:张杰,纪录:late, 成绩:C',2,'Changed record.',12,1),(66,'2015-12-27 03:46:21.730581','20','Python自动化开发(12) 第1天,学员:王浩,纪录:noshow, 成绩:B-',2,'Changed record.',12,1),(67,'2015-12-27 03:46:21.733329','15','Python自动化开发(12) 第1天,学员:吴天帅,纪录:leave_early, 成绩:COPY',2,'Changed record.',12,1),(68,'2015-12-27 03:46:26.983860','21','Python自动化开发(12) 第1天,学员:张杰,纪录:checked, 成绩:C',2,'Changed record.',12,1),(69,'2015-12-27 05:12:52.848335','2','Linux架构师(3)',1,'Added.',10,1),(70,'2015-12-27 05:16:24.595553','3','Python自动化开发(12) 第1天',3,'',11,1),(71,'2015-12-27 05:18:03.042691','5','Python自动化开发(12) 第1天',1,'Added.',11,1),(72,'2015-12-27 05:21:16.838442','3','QQ:317828332 -- Stu:333 -- Name:景丽洋',2,'Changed stu_id.',7,1),(73,'2015-12-27 05:24:27.619575','1','Python自动化开发(12)',2,'Changed graduate_date.',10,1),(74,'2015-12-27 06:17:05.745714','6','Linux架构师(3) 第2天',1,'Added.',11,1),(75,'2015-12-27 06:17:49.699137','1','QQ:32d -- Stu: -- Name:吴天帅',2,'Changed class_list.',7,1),(76,'2015-12-27 06:17:56.732383','2','QQ:333 -- Stu: -- Name:王浩',2,'Changed class_list.',7,1),(77,'2015-12-27 06:18:03.770645','6','Linux架构师(3) 第2天',2,'No fields changed.',11,1),(78,'2015-12-27 08:00:33.115975','1','你对本课程讲师的满意程度',1,'Added.',13,1),(79,'2015-12-27 08:00:55.769842','2','你对学校教学设施的满意程度',1,'Added.',13,1),(80,'2015-12-27 08:01:33.754149','3','你愿意向身边的朋友推荐老男孩教育的程度',1,'Added.',13,1),(81,'2015-12-27 08:02:17.045114','4','你对课程内容设置的满意程度',1,'Added.',13,1),(82,'2015-12-27 08:05:36.859557','1','python 11期第2节课满意度调查',1,'Added.',14,1),(83,'2015-12-27 08:06:58.800876','2','python 11期第2节课满意度调查 --  -- 你对本课程讲师的满意程度 -- 8',1,'Added.',15,1),(84,'2015-12-27 08:07:09.701976','3','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 4',1,'Added.',15,1),(85,'2015-12-27 10:13:21.954460','5','请写你对我们的其它建议',1,'Added.',13,1),(86,'2015-12-27 10:13:31.890135','1','python 11期第2节课满意度调查',2,'Changed questions.',14,1),(87,'2015-12-27 10:20:27.519524','5','请写你对我们的其它建议',2,'Changed anwser_type.',13,1),(88,'2015-12-27 10:20:33.238188','5','请写你对我们的其它建议',2,'Changed anwser_type.',13,1),(89,'2015-12-27 12:47:13.756934','8','python 11期第2节课满意度调查 -- Alex  -- 你对课程内容设置的满意程度 -- 6',3,'',15,1),(90,'2015-12-27 12:47:13.758390','7','python 11期第2节课满意度调查 -- Alex  -- 请写你对我们的其它建议 -- 0',3,'',15,1),(91,'2015-12-27 12:47:13.759552','6','python 11期第2节课满意度调查 -- Alex  -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(92,'2015-12-27 12:47:13.761212','5','python 11期第2节课满意度调查 -- Alex  -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(93,'2015-12-27 12:47:13.762433','4','python 11期第2节课满意度调查 -- Alex  -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(94,'2015-12-27 12:47:13.763478','3','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 4',3,'',15,1),(95,'2015-12-27 12:47:13.764492','2','python 11期第2节课满意度调查 --  -- 你对本课程讲师的满意程度 -- 8',3,'',15,1),(96,'2015-12-27 13:02:03.267965','33','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(97,'2015-12-27 13:02:03.271183','32','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(98,'2015-12-27 13:02:03.272974','31','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(99,'2015-12-27 13:02:03.274292','30','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(100,'2015-12-27 13:02:03.275404','29','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(101,'2015-12-27 13:02:03.276464','28','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(102,'2015-12-27 13:02:03.277637','27','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(103,'2015-12-27 13:02:03.279543','26','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(104,'2015-12-27 13:02:03.281833','25','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(105,'2015-12-27 13:02:03.283190','24','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(106,'2015-12-27 13:02:03.284398','23','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(107,'2015-12-27 13:02:03.285570','22','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(108,'2015-12-27 13:02:03.286660','21','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(109,'2015-12-27 13:02:03.287882','20','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(110,'2015-12-27 13:02:03.289001','19','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(111,'2015-12-27 13:02:03.290081','18','python 11期第2节课满意度调查 -- Alex  -- 你对课程内容设置的满意程度 -- 6',3,'',15,1),(112,'2015-12-27 13:02:03.291496','17','python 11期第2节课满意度调查 -- Alex  -- 请写你对我们的其它建议 -- 0',3,'',15,1),(113,'2015-12-27 13:02:03.292533','16','python 11期第2节课满意度调查 -- Alex  -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(114,'2015-12-27 13:02:03.293673','15','python 11期第2节课满意度调查 -- Alex  -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(115,'2015-12-27 13:02:03.295146','14','python 11期第2节课满意度调查 -- Alex  -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(116,'2015-12-27 13:02:03.297352','13','python 11期第2节课满意度调查 -- Alex  -- 你对课程内容设置的满意程度 -- 6',3,'',15,1),(117,'2015-12-27 13:02:03.299038','12','python 11期第2节课满意度调查 -- Alex  -- 请写你对我们的其它建议 -- 0',3,'',15,1),(118,'2015-12-27 13:02:03.300332','11','python 11期第2节课满意度调查 -- Alex  -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(119,'2015-12-27 13:02:03.301494','10','python 11期第2节课满意度调查 -- Alex  -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(120,'2015-12-27 13:02:03.302583','9','python 11期第2节课满意度调查 -- Alex  -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(121,'2015-12-27 13:06:38.225472','53','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(122,'2015-12-27 13:06:38.229143','52','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(123,'2015-12-27 13:06:38.230919','51','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(124,'2015-12-27 13:06:38.232857','50','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(125,'2015-12-27 13:06:38.234129','49','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(126,'2015-12-27 13:06:38.235260','48','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(127,'2015-12-27 13:06:38.236340','47','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(128,'2015-12-27 13:06:38.237390','46','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(129,'2015-12-27 13:06:38.238501','45','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(130,'2015-12-27 13:06:38.239536','44','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(131,'2015-12-27 13:06:38.241205','43','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(132,'2015-12-27 13:06:38.242246','42','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(133,'2015-12-27 13:06:38.243337','41','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(134,'2015-12-27 13:06:38.244477','40','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(135,'2015-12-27 13:06:38.245828','39','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(136,'2015-12-27 13:06:38.247174','38','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(137,'2015-12-27 13:06:38.248767','37','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(138,'2015-12-27 13:06:38.249928','36','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(139,'2015-12-27 13:06:38.251329','35','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(140,'2015-12-27 13:06:38.252365','34','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(141,'2015-12-27 13:07:14.406701','2','python 11期第5节课满意度调查',1,'Added.',14,1),(142,'2015-12-27 13:19:54.843130','60','python 11期第5节课满意度调查 --  -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(143,'2015-12-27 13:19:54.845197','59','python 11期第5节课满意度调查 --  -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(144,'2015-12-27 13:19:54.846582','58','python 11期第2节课满意度调查 -- ddd -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(145,'2015-12-27 13:19:54.847719','57','python 11期第2节课满意度调查 -- ddd -- 请写你对我们的其它建议 -- 0',3,'',15,1),(146,'2015-12-27 13:19:54.848807','56','python 11期第2节课满意度调查 -- ddd -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(147,'2015-12-27 13:19:54.849872','55','python 11期第2节课满意度调查 -- ddd -- 你愿意向身边的朋友推荐老男孩教育的程度 -- 5',3,'',15,1),(148,'2015-12-27 13:19:54.850962','54','python 11期第2节课满意度调查 -- ddd -- 你对本课程讲师的满意程度 -- 5',3,'',15,1),(149,'2015-12-27 13:20:46.242283','62','python 11期第5节课满意度调查 --  -- 你对课程内容设置的满意程度 -- 7',3,'',15,1),(150,'2015-12-27 13:20:46.245479','61','python 11期第5节课满意度调查 --  -- 你对学校教学设施的满意程度 -- 7',3,'',15,1),(151,'2015-12-27 13:21:52.607896','64','python 11期第5节课满意度调查 --  -- 你对课程内容设置的满意程度 -- 5',3,'',15,1),(152,'2015-12-27 13:21:52.611621','63','python 11期第5节课满意度调查 --  -- 你对学校教学设施的满意程度 -- 4',3,'',15,1),(153,'2015-12-27 13:22:08.919950','66','python 11期第5节课满意度调查 --  -- 你对课程内容设置的满意程度 -- 9',3,'',15,1),(154,'2015-12-27 13:22:08.923103','65','python 11期第5节课满意度调查 --  -- 你对学校教学设施的满意程度 -- 8',3,'',15,1),(155,'2015-12-27 13:23:35.534617','68','python 11期第5节课满意度调查 --  -- 你对课程内容设置的满意程度 -- 9',3,'',15,1),(156,'2015-12-27 13:23:35.537915','67','python 11期第5节课满意度调查 --  -- 你对学校教学设施的满意程度 -- 8',3,'',15,1),(157,'2015-12-27 13:40:56.006263','70','python 11期第5节课满意度调查 --  -- 你对课程内容设置的满意程度 -- 6',3,'',15,1),(158,'2015-12-27 13:40:56.009912','69','python 11期第5节课满意度调查 --  -- 你对学校教学设施的满意程度 -- 5',3,'',15,1),(159,'2015-12-28 18:55:00.148513','7','Python自动化开发(12) 第3天',1,'Added.',11,1),(160,'2015-12-28 18:55:06.293982','8','Python自动化开发(12) 第4天',1,'Added.',11,1),(161,'2015-12-28 18:55:15.017302','9','Python自动化开发(12) 第5天',1,'Added.',11,1),(162,'2015-12-28 19:31:20.907417','10','Python自动化开发(12) 第6天',1,'Added.',11,1),(163,'2015-12-28 19:31:26.921911','11','Python自动化开发(12) 第7天',1,'Added.',11,1),(164,'2015-12-28 19:31:33.733547','12','Python自动化开发(12) 第8天',1,'Added.',11,1),(165,'2015-12-28 19:31:39.799405','13','Python自动化开发(12) 第9天',1,'Added.',11,1),(166,'2015-12-28 19:31:46.253869','14','Python自动化开发(12) 第10天',1,'Added.',11,1),(167,'2015-12-28 19:31:52.354564','15','Python自动化开发(12) 第11天',1,'Added.',11,1),(168,'2015-12-28 19:31:57.918253','16','Python自动化开发(12) 第12天',1,'Added.',11,1),(169,'2015-12-28 19:33:39.248847','17','Python自动化开发(12) 第13天',1,'Added.',11,1),(170,'2015-12-28 19:33:48.449407','18','Python自动化开发(12) 第14天',1,'Added.',11,1),(171,'2015-12-28 19:33:54.446893','19','Python自动化开发(12) 第15天',1,'Added.',11,1),(172,'2015-12-28 19:34:02.188138','20','Python自动化开发(12) 第16天',1,'Added.',11,1),(173,'2015-12-28 19:34:08.950552','21','Python自动化开发(12) 第17天',1,'Added.',11,1),(174,'2015-12-28 19:34:14.806915','22','Python自动化开发(12) 第18天',1,'Added.',11,1),(175,'2015-12-28 19:34:22.133288','23','Python自动化开发(12) 第19天',1,'Added.',11,1),(176,'2015-12-28 19:34:28.532859','24','Python自动化开发(12) 第20天',1,'Added.',11,1),(177,'2015-12-28 19:41:56.014685','95','Python自动化开发(12) 第19天,学员:张杰,纪录:checked, 成绩:C+',2,'Changed score.',12,1),(178,'2015-12-28 19:49:10.434428','94','Python自动化开发(12) 第19天,学员:王浩,纪录:checked, 成绩:B+',2,'Changed score.',12,1),(179,'2015-12-28 19:49:10.437971','93','Python自动化开发(12) 第19天,学员:吴天帅,纪录:checked, 成绩:A',2,'Changed score.',12,1),(180,'2015-12-28 19:49:10.440828','92','Python自动化开发(12) 第18天,学员:景丽洋,纪录:checked, 成绩:A+',2,'Changed score.',12,1),(181,'2015-12-28 19:49:10.443551','91','Python自动化开发(12) 第18天,学员:张杰,纪录:checked, 成绩:B',2,'Changed score.',12,1),(182,'2015-12-28 19:49:10.446283','90','Python自动化开发(12) 第18天,学员:王浩,纪录:checked, 成绩:B-',2,'Changed score.',12,1),(183,'2015-12-28 19:49:10.449708','89','Python自动化开发(12) 第18天,学员:吴天帅,纪录:checked, 成绩:D',2,'Changed score.',12,1),(184,'2015-12-28 19:49:10.454525','88','Python自动化开发(12) 第17天,学员:景丽洋,纪录:checked, 成绩:C-',2,'Changed score.',12,1),(185,'2015-12-28 19:53:00.679987','73','Python自动化开发(12) 第14天,学员:吴天帅,纪录:checked, 成绩:COPY',2,'Changed score.',12,1),(186,'2015-12-28 20:13:36.426666','73','Python自动化开发(12) 第14天,学员:吴天帅,纪录:checked, 成绩:A+',2,'Changed score.',12,1),(187,'2015-12-28 20:13:36.429942','61','Python自动化开发(12) 第11天,学员:吴天帅,纪录:checked, 成绩:B',2,'Changed score.',12,1),(188,'2015-12-28 20:13:36.433346','41','Python自动化开发(12) 第6天,学员:吴天帅,纪录:checked, 成绩:B+',2,'Changed score.',12,1),(189,'2015-12-28 20:13:36.439434','27','Linux架构师(3) 第2天,学员:吴天帅,纪录:checked, 成绩:C+',2,'Changed score.',12,1),(190,'2015-12-28 20:33:20.644989','25','Python自动化开发(12) 第21天',1,'Added.',11,1),(191,'2015-12-28 20:33:27.823606','26','Python自动化开发(12) 第22天',1,'Added.',11,1),(192,'2015-12-28 20:33:34.063893','27','Python自动化开发(12) 第23天',1,'Added.',11,1),(193,'2015-12-28 20:33:41.486225','28','Python自动化开发(12) 第24天',1,'Added.',11,1),(194,'2015-12-28 20:33:48.772954','29','Python自动化开发(12) 第25天',1,'Added.',11,1),(195,'2015-12-28 20:49:06.589206','29','Python自动化开发(12) 第25天',3,'',11,1),(196,'2015-12-28 20:49:06.590646','28','Python自动化开发(12) 第24天',3,'',11,1),(197,'2015-12-28 20:49:06.591916','27','Python自动化开发(12) 第23天',3,'',11,1),(198,'2015-12-28 20:49:06.593369','26','Python自动化开发(12) 第22天',3,'',11,1),(199,'2015-12-28 23:21:48.683682','4','QQ:32d -- Stu: -- Name:吴天帅, 类型:refund,数额:-500',2,'Changed pay_type and paid_fee.',9,1),(200,'2015-12-29 04:58:25.553669','6','Alex长的有多帅',1,'Added.',13,1),(201,'2015-12-29 04:58:49.875772','7','你有多不喜欢共产党',1,'Added.',13,1),(202,'2015-12-29 04:59:23.055133','8','学费价格相比课程价格来讲你觉得合理程度怎样',1,'Added.',13,1),(203,'2015-12-29 05:00:10.730674','3','老男孩教育学员满意度调查',1,'Added.',14,1),(204,'2016-01-01 18:25:28.225648','3','QQ:317828332 -- Stu:333 -- Name:景丽洋',2,'Changed class_list.',7,1),(205,'2016-01-01 18:26:54.269307','121','Linux架构师(3) 第2天,学员:景丽洋,纪录:checked, 成绩:A+',2,'Changed score.',12,1),(206,'2016-01-05 02:07:43.396738','44','Python自动化开发(12) 第6天,学员:景丽洋,纪录:checked, 成绩:COPY',2,'Changed score.',12,1),(207,'2016-01-05 03:31:14.525400','43','Python自动化开发(12) 第6天,学员:张杰,纪录:checked, 成绩:F',2,'Changed score.',12,1),(208,'2016-01-09 22:13:04.699199','1','网速太慢 --- unread',1,'Added.',17,1),(209,'2016-01-09 23:44:36.985338','5','我要投诉老男孩老师 --- sovled',2,'Changed status, comment, dealing_time and dealer.',17,1),(210,'2016-01-11 17:19:00.929194','5','QQ:4608 -- Stu: -- Name:Jack',1,'Added.',7,3),(211,'2016-01-11 17:19:41.327178','6','QQ:1982 -- Stu: -- Name:',1,'Added.',7,3),(212,'2016-01-11 18:06:23.749725','122','Python自动化开发(12) 第6天,学员:Jack,纪录:checked, 成绩:N/A',1,'Added.',12,3),(213,'2016-01-11 18:06:33.663521','123','Python自动化开发(12) 第7天,学员:Jack,纪录:checked, 成绩:N/A',1,'Added.',12,3),(214,'2016-01-17 08:00:25.751419','1','test',1,'Added.',3,1),(215,'2016-01-17 08:00:50.413241','2','Rain Wang',2,'已修改 password 。',6,1),(216,'2016-01-17 08:01:12.251608','2','Rain Wang',2,'已修改 groups 和 valid_end_time 。',6,1),(217,'2016-01-17 08:02:59.140480','2','Rain Wang',2,'没有字段被修改。',6,3),(218,'2016-01-17 08:03:38.759697','2','Rain Wang',2,'已修改 password 。',6,1),(219,'2016-01-17 08:04:27.415760','2','Rain Wang',2,'已修改 is_admin 。',6,3),(220,'2016-01-17 08:04:59.602114','4','',1,'Added.',6,3),(221,'2016-01-17 08:05:06.887943','4','t1',2,'已修改 name 和 valid_end_time 。',6,3),(222,'2016-01-17 08:12:01.284943','4','t1',2,'已修改 is_admin 。',6,3),(223,'2016-01-17 08:12:51.440680','4','t1',2,'已修改 is_admin 。',6,4);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(10,'crm','classlist'),(17,'crm','compliant'),(8,'crm','consultrecord'),(11,'crm','courserecord'),(7,'crm','customer'),(9,'crm','paymentrecord'),(18,'crm','studentfaq'),(12,'crm','studyrecord'),(14,'crm','survery'),(13,'crm','surveryitem'),(15,'crm','surveryrecord'),(6,'crm','userprofile'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'crm','0001_initial','2015-12-13 03:56:46.040027'),(2,'contenttypes','0001_initial','2015-12-13 03:56:46.095393'),(3,'admin','0001_initial','2015-12-13 03:56:46.175760'),(4,'contenttypes','0002_remove_content_type_name','2015-12-13 03:56:46.275656'),(5,'auth','0001_initial','2015-12-13 03:56:46.465377'),(6,'auth','0002_alter_permission_name_max_length','2015-12-13 03:56:46.506862'),(7,'auth','0003_alter_user_email_max_length','2015-12-13 03:56:46.527380'),(8,'auth','0004_alter_user_username_opts','2015-12-13 03:56:46.548376'),(9,'auth','0005_alter_user_last_login_null','2015-12-13 03:56:46.570177'),(10,'auth','0006_require_contenttypes_0002','2015-12-13 03:56:46.573271'),(11,'sessions','0001_initial','2015-12-13 03:56:46.614258'),(12,'crm','0002_auto_20151213_0401','2015-12-13 04:01:31.951192'),(13,'crm','0003_auto_20151213_0629','2015-12-13 06:29:46.825998'),(14,'crm','0004_auto_20151213_0639','2015-12-13 06:39:35.180659'),(15,'crm','0005_auto_20151213_0706','2015-12-13 07:06:08.499150'),(16,'crm','0006_auto_20151213_0716','2015-12-13 07:16:12.963080'),(17,'crm','0007_auto_20151213_0754','2015-12-13 07:54:50.589313'),(18,'crm','0008_auto_20151213_0802','2015-12-13 08:02:21.258858'),(19,'crm','0009_auto_20151213_0839','2015-12-13 08:40:04.108240'),(20,'admin','0002_logentry_remove_auto_add','2015-12-18 14:18:34.502539'),(21,'auth','0007_alter_validators_add_error_messages','2015-12-18 14:18:34.628842'),(22,'crm','0010_auto_20151218_1418','2015-12-18 14:18:35.602446'),(23,'crm','0011_auto_20151227_0249','2015-12-27 02:50:19.235199'),(24,'crm','0012_auto_20151227_0250','2015-12-27 02:50:19.293859'),(25,'crm','0013_auto_20151227_0255','2015-12-27 02:55:24.812647'),(26,'crm','0014_auto_20151227_0256','2015-12-27 02:56:39.976412'),(27,'crm','0015_auto_20151227_0257','2015-12-27 02:57:28.855573'),(28,'crm','0016_auto_20151227_0258','2015-12-27 02:58:45.276080'),(29,'crm','0017_auto_20151227_0423','2015-12-27 04:24:01.320279'),(30,'crm','0018_auto_20151227_0524','2015-12-27 05:24:12.011024'),(31,'crm','0019_auto_20151227_0759','2015-12-27 07:59:33.569288'),(32,'crm','0020_auto_20151227_0806','2015-12-27 08:06:25.464730'),(33,'crm','0021_auto_20151227_1011','2015-12-27 10:11:28.806546'),(34,'crm','0022_auto_20151227_1017','2015-12-27 10:17:29.665726'),(35,'crm','0023_auto_20151227_1302','2015-12-27 13:02:22.064878'),(36,'crm','0024_auto_20151227_1302','2015-12-27 13:02:40.146397'),(37,'crm','0002_auto_20160109_2210','2016-01-09 22:10:17.027464'),(38,'crm','0003_auto_20160109_2210','2016-01-09 22:11:02.825299'),(39,'crm','0004_auto_20160109_2211','2016-01-09 22:11:47.096654'),(40,'crm','0005_auto_20160109_2211','2016-01-09 22:12:19.795535'),(41,'crm','0006_auto_20160109_2212','2016-01-09 22:12:20.012325'),(42,'crm','0007_auto_20160110_0444','2016-01-10 04:45:01.428780'),(43,'crm','0008_auto_20160117_0715','2016-01-17 07:16:04.723412'),(44,'crm','0009_auto_20160117_0721','2016-01-17 07:21:18.932445'),(45,'crm','0002_auto_20160117_0729','2016-01-17 07:29:14.820606'),(46,'crm','0003_auto_20160117_0756','2016-01-17 07:56:12.733317'),(47,'crm','0004_auto_20160117_0815','2016-01-17 08:15:47.370067'),(48,'crm','0005_auto_20160117_0817','2016-01-17 08:17:18.526676'),(49,'crm','0006_auto_20160117_0817','2016-01-17 08:18:44.150796'),(50,'crm','0007_auto_20160117_0818','2016-01-17 08:18:44.216220'),(51,'crm','0008_auto_20160117_0819','2016-01-17 08:19:02.077831'),(52,'crm','0009_auto_20160117_0819','2016-01-17 08:19:30.175131'),(53,'crm','0010_auto_20160117_0819','2016-01-17 08:19:30.246076'),(54,'crm','0011_auto_20160117_0821','2016-01-17 08:23:44.400500'),(55,'crm','0012_auto_20160117_0823','2016-01-17 08:23:44.441051'),(56,'crm','0013_userprofile_is_staffs','2016-01-17 08:34:40.503759'),(57,'crm','0014_remove_userprofile_is_staffs','2016-01-17 08:34:40.573421');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4wvz53548rhwewo75jxsvriq8qjt0cig','YjdhNzM4NjljNDQ1ZTBiYzRhNjA1M2RmMGFjNDY1MmE4MWE3NzBlNTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc2OGIzNWU3NTc2ZGM2Zjk4ZDNlMWIxMTI2NzdjMDc3MjM0MTUxYzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=','2016-01-25 17:17:06.165377'),('bqxo6q5j08510ve7j7gcf8t2ijvjwl85','MTllNWJlZDQ3NjQwN2NiNGUyOTVjMmIxYTU3ZGVlMTY1NTA0MTlmMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjllYTdkMzdmODhiZjZjZTBhODk1ODJmNDMxZTc5MTk0YTQ2YzZiNmYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-01-01 13:43:23.687775'),('bsbx6tgt7c5gpff5xiqb2irt8a9w5e05','YjdhNzM4NjljNDQ1ZTBiYzRhNjA1M2RmMGFjNDY1MmE4MWE3NzBlNTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijc2OGIzNWU3NTc2ZGM2Zjk4ZDNlMWIxMTI2NzdjMDc3MjM0MTUxYzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=','2016-01-31 08:16:00.895089'),('pul6um6d3fmm74r97boltkvu4pe3vogf','MTllNWJlZDQ3NjQwN2NiNGUyOTVjMmIxYTU3ZGVlMTY1NTA0MTlmMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjllYTdkMzdmODhiZjZjZTBhODk1ODJmNDMxZTc5MTk0YTQ2YzZiNmYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-01-01 13:35:10.513597'),('txtnxm7a01cy3i5g0c9xaappp5hnpkrp','ZTA1NWEzNGViYWQxMmM5YjY4NTM4NzRhZjIzNTUzZTI5YWIyZmJhMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjcwZDdmOGI2NTkwZjcwNWNiNjY3Nzk0Nzk0ZmYzYWZiMTQzMmUyODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2015-12-27 12:38:07.068266'),('x5it7e5vqj5217d82cu5ahqvc81jkuo9','MTllNWJlZDQ3NjQwN2NiNGUyOTVjMmIxYTU3ZGVlMTY1NTA0MTlmMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjllYTdkMzdmODhiZjZjZTBhODk1ODJmNDMxZTc5MTk0YTQ2YzZiNmYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-01-01 14:18:52.687453');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-17 16:41:39
