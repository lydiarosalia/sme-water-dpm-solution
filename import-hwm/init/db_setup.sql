-- ###################################################################################################################################
-- Create database / schema
-- ###################################################################################################################################
CREATE DATABASE `dpm-solution`;

-- ###################################################################################################################################
-- Create tables for non-denormalized tables
-- ###################################################################################################################################
CREATE TABLE `dpm-solution`.`flow` (
  `datetime` DATETIME NOT NULL,
  `site_id` VARCHAR(20) NOT NULL,
  `channel_no` INTEGER,
  `value` FLOAT NULL,
  PRIMARY KEY (`datetime`, `site_id`, `channel_no` ASC),
  INDEX `idx_flow_datetime_site_channel` (`site_id` ASC, `channel_no` ASC, `datetime` ASC));

CREATE TABLE `dpm-solution`.`pressure` (
  `datetime` DATETIME NOT NULL,
  `site_id` VARCHAR(20) NOT NULL,
  `channel_no` INTEGER,
  `value` FLOAT NULL,
  PRIMARY KEY (`datetime`, `site_id`, `channel_no` ASC),
  INDEX `idx_flow_datetime_site_channel` (`site_id` ASC, `channel_no` ASC, `datetime` ASC));
