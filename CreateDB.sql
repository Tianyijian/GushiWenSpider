CREATE DATABASE `gushiwen` /*!40100 DEFAULT CHARACTER SET utf8 */

CREATE TABLE `fanyi` (
  `fanyi_id` varchar(20) NOT NULL,
  `fanyi_link` varchar(100) DEFAULT NULL,
  `fanyi` mediumblob,
  `zhushi` mediumblob,
  PRIMARY KEY (`fanyi_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `main_content` (
  `view_num` varchar(30) NOT NULL,
  `content` mediumblob NOT NULL,
  PRIMARY KEY (`view_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `view` (
  `view_num` varchar(30) NOT NULL,
  `view_name` varchar(50) DEFAULT NULL,
  `author_name` varchar(20) DEFAULT NULL,
  `fanyi_id` varchar(20) DEFAULT NULL,
  `dynasty` varchar(10) DEFAULT NULL,
  `view_link` varchar(100) DEFAULT NULL,
  `main_content` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`view_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
