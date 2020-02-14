-- ###################################################################################################################################
-- Create Database / Schema
-- ###################################################################################################################################
CREATE DATABASE `dpm-solution`;

-- ###################################################################################################################################
-- Create Tables
-- ###################################################################################################################################
CREATE TABLE `dpm-solution`.`flow` (
  `datetime` DATETIME NOT NULL,
  `site_id` VARCHAR(20) NOT NULL,
  `value` FLOAT NULL,
  INDEX `idx_flow_datetime_site_id` (`site_id` ASC, `datetime` ASC));

CREATE TABLE `dpm-solution`.`pressure` (
  `datetime` DATETIME NOT NULL,
  `site_id` VARCHAR(20) NOT NULL,
  `value` FLOAT NULL,
  INDEX `idx_pres__datetime_site_id` (`site_id` ASC, `datetime` ASC));

-- ###################################################################################################################################
-- Create Views
-- ###################################################################################################################################
USE `dpm-solution`;
CREATE  OR REPLACE VIEW `flow_view` AS
SELECT t1.site_id,
	   t1.all_datetime,
       t2.value
  FROM ( SELECT tp.site_id,
				STR_TO_DATE(CONCAT(CAST(tp.date_values AS CHAR), " ", CAST(l.time_values AS CHAR)),'%Y-%m-%d %H:%i:%s') AS all_datetime
           FROM (SELECT DISTINCT site_id, DATE_FORMAT(datetime, '%Y-%m-%d') AS date_values FROM flow) tp
		  CROSS JOIN (SELECT time_values FROM time_lookup) l
		) t1
LEFT JOIN flow t2 ON (t1.site_id = t2.site_id AND t1.all_datetime = t2.datetime);

USE `dpm-solution`;
CREATE  OR REPLACE VIEW `pressure_view` AS
SELECT t1.site_id,
	   t1.all_datetime,
       t2.value
  FROM ( SELECT tp.site_id,
				STR_TO_DATE(CONCAT(CAST(tp.date_values AS CHAR), " ", CAST(l.time_values AS CHAR)),'%Y-%m-%d %H:%i:%s') AS all_datetime
           FROM (SELECT DISTINCT site_id, DATE_FORMAT(datetime, '%Y-%m-%d') AS date_values FROM pressure) tp
		  CROSS JOIN (SELECT time_values FROM time_lookup) l
		) t1
LEFT JOIN pressure t2 ON (t1.site_id = t2.site_id AND t1.all_datetime = t2.datetime);

-- ###################################################################################################################################
-- Create Lookup Table
-- ###################################################################################################################################
CREATE TABLE `dpm-solution`.`time_lookup` (
  `time_values` VARCHAR(8) NOT NULL);

ALTER TABLE `dpm-solution`.`time_lookup` 
ADD INDEX `time_value_idx` (`time_values` ASC);

-- ###################################################################################################################################
-- Insert data into Lookup Table
-- ###################################################################################################################################
INSERT INTO time_lookup VALUES ('00:00:00');
INSERT INTO time_lookup VALUES ('00:15:00');
INSERT INTO time_lookup VALUES ('00:30:00');
INSERT INTO time_lookup VALUES ('00:45:00');

INSERT INTO time_lookup VALUES ('01:00:00');
INSERT INTO time_lookup VALUES ('01:15:00');
INSERT INTO time_lookup VALUES ('01:30:00');
INSERT INTO time_lookup VALUES ('01:45:00');

INSERT INTO time_lookup VALUES ('02:00:00');
INSERT INTO time_lookup VALUES ('02:15:00');
INSERT INTO time_lookup VALUES ('02:30:00');
INSERT INTO time_lookup VALUES ('02:45:00');

INSERT INTO time_lookup VALUES ('03:00:00');
INSERT INTO time_lookup VALUES ('03:15:00');
INSERT INTO time_lookup VALUES ('03:30:00');
INSERT INTO time_lookup VALUES ('03:45:00');

INSERT INTO time_lookup VALUES ('04:00:00');
INSERT INTO time_lookup VALUES ('04:15:00');
INSERT INTO time_lookup VALUES ('04:30:00');
INSERT INTO time_lookup VALUES ('04:45:00');

INSERT INTO time_lookup VALUES ('05:00:00');
INSERT INTO time_lookup VALUES ('05:15:00');
INSERT INTO time_lookup VALUES ('05:30:00');
INSERT INTO time_lookup VALUES ('05:45:00');

INSERT INTO time_lookup VALUES ('06:00:00');
INSERT INTO time_lookup VALUES ('06:15:00');
INSERT INTO time_lookup VALUES ('06:30:00');
INSERT INTO time_lookup VALUES ('06:45:00');

INSERT INTO time_lookup VALUES ('07:00:00');
INSERT INTO time_lookup VALUES ('07:15:00');
INSERT INTO time_lookup VALUES ('07:30:00');
INSERT INTO time_lookup VALUES ('07:45:00');

INSERT INTO time_lookup VALUES ('08:00:00');
INSERT INTO time_lookup VALUES ('08:15:00');
INSERT INTO time_lookup VALUES ('08:30:00');
INSERT INTO time_lookup VALUES ('08:45:00');

INSERT INTO time_lookup VALUES ('09:00:00');
INSERT INTO time_lookup VALUES ('09:15:00');
INSERT INTO time_lookup VALUES ('09:30:00');
INSERT INTO time_lookup VALUES ('09:45:00');

INSERT INTO time_lookup VALUES ('10:00:00');
INSERT INTO time_lookup VALUES ('10:15:00');
INSERT INTO time_lookup VALUES ('10:30:00');
INSERT INTO time_lookup VALUES ('10:45:00');

INSERT INTO time_lookup VALUES ('11:00:00');
INSERT INTO time_lookup VALUES ('11:15:00');
INSERT INTO time_lookup VALUES ('11:30:00');
INSERT INTO time_lookup VALUES ('11:45:00');

INSERT INTO time_lookup VALUES ('12:00:00');
INSERT INTO time_lookup VALUES ('12:15:00');
INSERT INTO time_lookup VALUES ('12:30:00');
INSERT INTO time_lookup VALUES ('12:45:00');

INSERT INTO time_lookup VALUES ('13:00:00');
INSERT INTO time_lookup VALUES ('13:15:00');
INSERT INTO time_lookup VALUES ('13:30:00');
INSERT INTO time_lookup VALUES ('13:45:00');

INSERT INTO time_lookup VALUES ('14:00:00');
INSERT INTO time_lookup VALUES ('14:15:00');
INSERT INTO time_lookup VALUES ('14:30:00');
INSERT INTO time_lookup VALUES ('14:45:00');

INSERT INTO time_lookup VALUES ('15:00:00');
INSERT INTO time_lookup VALUES ('15:15:00');
INSERT INTO time_lookup VALUES ('15:30:00');
INSERT INTO time_lookup VALUES ('15:45:00');

INSERT INTO time_lookup VALUES ('16:00:00');
INSERT INTO time_lookup VALUES ('16:15:00');
INSERT INTO time_lookup VALUES ('16:30:00');
INSERT INTO time_lookup VALUES ('16:45:00');

INSERT INTO time_lookup VALUES ('17:00:00');
INSERT INTO time_lookup VALUES ('17:15:00');
INSERT INTO time_lookup VALUES ('17:30:00');
INSERT INTO time_lookup VALUES ('17:45:00');

INSERT INTO time_lookup VALUES ('18:00:00');
INSERT INTO time_lookup VALUES ('18:15:00');
INSERT INTO time_lookup VALUES ('18:30:00');
INSERT INTO time_lookup VALUES ('18:45:00');

INSERT INTO time_lookup VALUES ('19:00:00');
INSERT INTO time_lookup VALUES ('19:15:00');
INSERT INTO time_lookup VALUES ('19:30:00');
INSERT INTO time_lookup VALUES ('19:45:00');

INSERT INTO time_lookup VALUES ('20:00:00');
INSERT INTO time_lookup VALUES ('20:15:00');
INSERT INTO time_lookup VALUES ('20:30:00');
INSERT INTO time_lookup VALUES ('20:45:00');

INSERT INTO time_lookup VALUES ('21:00:00');
INSERT INTO time_lookup VALUES ('21:15:00');
INSERT INTO time_lookup VALUES ('21:30:00');
INSERT INTO time_lookup VALUES ('21:45:00');

INSERT INTO time_lookup VALUES ('22:00:00');
INSERT INTO time_lookup VALUES ('22:15:00');
INSERT INTO time_lookup VALUES ('22:30:00');
INSERT INTO time_lookup VALUES ('22:45:00');

INSERT INTO time_lookup VALUES ('23:00:00');
INSERT INTO time_lookup VALUES ('23:15:00');
INSERT INTO time_lookup VALUES ('23:30:00');
INSERT INTO time_lookup VALUES ('23:45:00');

COMMIT;
