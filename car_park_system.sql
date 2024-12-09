/*
 Navicat MySQL Dump SQL

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 90001 (9.0.1)
 Source Host           : localhost:3306
 Source Schema         : car_park_system

 Target Server Type    : MySQL
 Target Server Version : 90001 (9.0.1)
 File Encoding         : 65001

 Date: 09/12/2024 16:11:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for edge_information
-- ----------------------------
DROP TABLE IF EXISTS `edge_information`;
CREATE TABLE `edge_information` (
  `edge_id` int NOT NULL AUTO_INCREMENT,
  `source_id` int DEFAULT NULL,
  `target_id` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  PRIMARY KEY (`edge_id`),
  KEY `source_id` (`source_id`),
  KEY `target_id` (`target_id`),
  CONSTRAINT `edge_information_ibfk_1` FOREIGN KEY (`source_id`) REFERENCES `parking_slots` (`slot_id`),
  CONSTRAINT `edge_information_ibfk_2` FOREIGN KEY (`target_id`) REFERENCES `parking_slots` (`slot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of edge_information
-- ----------------------------
BEGIN;
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (1, 1, 2, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (2, 1, 3, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (3, 2, 4, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (4, 2, 5, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (5, 3, 4, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (6, 3, 6, 2);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (7, 4, 9, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (8, 5, 7, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (9, 6, 8, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (10, 8, 10, 1);
INSERT INTO `edge_information` (`edge_id`, `source_id`, `target_id`, `weight`) VALUES (11, 5, 9, 1);
COMMIT;

-- ----------------------------
-- Table structure for parking_slots
-- ----------------------------
DROP TABLE IF EXISTS `parking_slots`;
CREATE TABLE `parking_slots` (
  `slot_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(20) DEFAULT NULL,
  `state` int DEFAULT NULL,
  `position_x` int DEFAULT NULL,
  `position_y` int DEFAULT NULL,
  `position_z` int DEFAULT NULL,
  `is_elevator` tinyint(1) DEFAULT '0',
  `is_charger` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`slot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of parking_slots
-- ----------------------------
BEGIN;
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (1, '中', 0, 0, 0, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (2, '小', 1, 1, 0, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (3, '大', 1, 0, 1, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (4, '中', 1, 1, 1, -1, 1, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (5, '中', 0, 2, 0, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (6, '中', 0, 0, 3, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (7, '中', 0, 3, 0, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (8, '中', 0, 1, 3, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (9, '中', 1, 2, 1, -1, 0, 0);
INSERT INTO `parking_slots` (`slot_id`, `type`, `state`, `position_x`, `position_y`, `position_z`, `is_elevator`, `is_charger`) VALUES (10, '中', 1, 2, 3, -1, 0, 1);
COMMIT;

-- ----------------------------
-- Table structure for vehicles
-- ----------------------------
DROP TABLE IF EXISTS `vehicles`;
CREATE TABLE `vehicles` (
  `car_id` bigint NOT NULL AUTO_INCREMENT,
  `license_plate` varchar(20) DEFAULT NULL,
  `car_length` float DEFAULT NULL,
  `car_width` float DEFAULT NULL,
  `car_type` varchar(20) DEFAULT NULL,
  `slot_id` int DEFAULT NULL,
  PRIMARY KEY (`car_id`),
  KEY `f_slot_id` (`slot_id`),
  CONSTRAINT `f_slot_id` FOREIGN KEY (`slot_id`) REFERENCES `parking_slots` (`slot_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of vehicles
-- ----------------------------
BEGIN;
INSERT INTO `vehicles` (`car_id`, `license_plate`, `car_length`, `car_width`, `car_type`, `slot_id`) VALUES (1, '沪C·015WP', 4.99, 1.8, '油', 3);
INSERT INTO `vehicles` (`car_id`, `license_plate`, `car_length`, `car_width`, `car_type`, `slot_id`) VALUES (2, '沪K·A6101', 4.99, 2, NULL, 4);
INSERT INTO `vehicles` (`car_id`, `license_plate`, `car_length`, `car_width`, `car_type`, `slot_id`) VALUES (3, '沪A·12345', 4.99, 1.8, NULL, 2);
INSERT INTO `vehicles` (`car_id`, `license_plate`, `car_length`, `car_width`, `car_type`, `slot_id`) VALUES (5, '沪A·123456', 4.99, 1.9, '电', 10);
INSERT INTO `vehicles` (`car_id`, `license_plate`, `car_length`, `car_width`, `car_type`, `slot_id`) VALUES (6, '沪Q·12345', 5.7, 2.7, '油', 9);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
