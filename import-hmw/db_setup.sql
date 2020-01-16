CREATE DATABASE `dpm-solution`;

CREATE TABLE `dpm-solution`.`flow` (
  `datetime` DATETIME NOT NULL,
  `site_id` VARCHAR(20) NOT NULL,
  `value` FLOAT NULL);

CREATE TABLE `dpm-solution`.`pressure` (
  `datetime` DATETIME NOT NULL,
  `site_id` VARCHAR(20) NOT NULL,
  `value` FLOAT NULL);
