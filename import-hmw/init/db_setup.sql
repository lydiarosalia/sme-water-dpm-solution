-- ###################################################################################################################################
-- Create database / schema
-- ###################################################################################################################################
CREATE DATABASE `dpm-solution`;

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

-- ###################################################################################################################################
-- Create views for non-dernormalized tables
-- ###################################################################################################################################
USE `dpm-solution`;
CREATE  OR REPLACE VIEW `flow_view` AS
SELECT CONCAT(t1.site_id,"_",t1.channel_no) AS site_id_channel_no,
	   t1.all_datetime,
       t2.value
  FROM ( SELECT tp.site_id,
                tp.channel_no,
				STR_TO_DATE(CONCAT(CAST(tp.date_values AS CHAR), " ", CAST(l.time_values AS CHAR)),'%Y-%m-%d %H:%i:%s') AS all_datetime
           FROM (SELECT DISTINCT site_id, channel_no, DATE_FORMAT(datetime, '%Y-%m-%d') AS date_values FROM flow) tp
		  CROSS JOIN (SELECT time_values FROM time_lookup) l
		) t1
LEFT JOIN flow t2 ON (t1.site_id = t2.site_id AND t1.channel_no = t2.channel_no AND t1.all_datetime = t2.datetime);

USE `dpm-solution`;
CREATE  OR REPLACE VIEW `pressure_view` AS
SELECT CONCAT(t1.site_id,"_",t1.channel_no) AS site_id_channel_no,
	   t1.all_datetime,
       t2.value
  FROM ( SELECT tp.site_id,
                tp.channel_no,
				STR_TO_DATE(CONCAT(CAST(tp.date_values AS CHAR), " ", CAST(l.time_values AS CHAR)),'%Y-%m-%d %H:%i:%s') AS all_datetime
           FROM (SELECT DISTINCT site_id, channel_no, DATE_FORMAT(datetime, '%Y-%m-%d') AS date_values FROM pressure) tp
		  CROSS JOIN (SELECT time_values FROM time_lookup) l
		) t1
LEFT JOIN pressure t2 ON (t1.site_id = t2.site_id AND t1.channel_no = t2.channel_no AND t1.all_datetime = t2.datetime);

-- ###################################################################################################################################
-- Create tables (Denormalized)
-- Any new site is added to the configuration.csv, this table(s) must be altered.
-- Field format = [site_id]_[channel_no]
-- For example: site_id is 99999 and channel_no is 1; therefore field name is 99999_1
-- ###################################################################################################################################
CREATE TABLE `dpm-solution`.`flow_denormalized` (
  `datetime` DATETIME NOT NULL,
  `03805_PRV_1` FLOAT NULL,
  `03805_PRV_2` FLOAT NULL,
  `3807_1` FLOAT NULL,
  `03808_1_1` FLOAT NULL,
  `03808_2_1` FLOAT NULL,
  `3809_1` FLOAT NULL,
  `3810_1` FLOAT NULL,
  `3811_1` FLOAT NULL,
  `3812_1` FLOAT NULL,
  `03814_1_1` FLOAT NULL,
  `03814_2_1` FLOAT NULL,
  PRIMARY KEY (`datetime`),
  INDEX `idx_flow_datetime` (`datetime` ASC));

CREATE TABLE `dpm-solution`.`pressure_denormalized` (
  `datetime` DATETIME NOT NULL,
  `90515_1` FLOAT NULL,
  `90516_1` FLOAT NULL,
  `90517_1` FLOAT NULL,
  `90518_1` FLOAT NULL,
  `90519_1` FLOAT NULL,
  `90520_1` FLOAT NULL,
  `90521_1` FLOAT NULL,
  `90522_1` FLOAT NULL,
  `90523_1` FLOAT NULL,
  `03805_PRV_1` FLOAT NULL,
  `03805_PRV_3` FLOAT NULL,
  PRIMARY KEY (`datetime`),
  INDEX `idx_press_datetime` (`datetime` ASC));

-- ###################################################################################################################################
-- Create views (Denormalized)
-- Any new site is added to the configuration.csv, this table(s) must be altered.
-- Field format = [site_id]_[channel_no]
-- For example: site_id is 99999 and channel_no is 1; therefore field name is 99999_1
-- ###################################################################################################################################
USE `dpm-solution`;
CREATE  OR REPLACE VIEW `flow_denormalized_view` AS
SELECT t1.all_datetime,
	   t2.03805_PRV_1,
       t2.03805_PRV_2,
       t2.3807_1,
       t2.03808_1_1,
       t2.03808_2_1,
       t2.3809_1,
       t2.3810_1,
       t2.3811_1,
       t2.3812_1,
       t2.03814_1_1,
       t2.03814_2_1
  FROM ( SELECT STR_TO_DATE(CONCAT(CAST(tp.date_values AS CHAR), " ", CAST(l.time_values AS CHAR)),'%Y-%m-%d %H:%i:%s') AS all_datetime
           FROM (SELECT DISTINCT DATE_FORMAT(datetime, '%Y-%m-%d') AS date_values FROM flow_denormalized) tp
		  CROSS JOIN (SELECT time_values FROM time_lookup) l
		) t1
LEFT JOIN flow_denormalized t2 ON (t1.all_datetime = t2.datetime);

USE `dpm-solution`;
CREATE  OR REPLACE VIEW `pressure_denormalized_view` AS
SELECT t1.all_datetime,
	   t2.90515_1,
	   t2.90516_1,
	   t2.90517_1,
	   t2.90518_1,
	   t2.90519_1,
	   t2.90520_1,
	   t2.90521_1,
	   t2.90522_1,
	   t2.90523_1,
	   t2.03805_PRV_1,
	   t2.03805_PRV_3
  FROM ( SELECT STR_TO_DATE(CONCAT(CAST(tp.date_values AS CHAR), " ", CAST(l.time_values AS CHAR)),'%Y-%m-%d %H:%i:%s') AS all_datetime
           FROM (SELECT DISTINCT DATE_FORMAT(datetime, '%Y-%m-%d') AS date_values FROM pressure_denormalized) tp
		  CROSS JOIN (SELECT time_values FROM time_lookup) l
		) t1
LEFT JOIN pressure_denormalized t2 ON (t1.all_datetime = t2.datetime);
-- ###################################################################################################################################
-- Create Lookup Table
-- ###################################################################################################################################
CREATE TABLE `dpm-solution`.`time_lookup` (
  `time_values` VARCHAR(8) NOT NULL);

ALTER TABLE `dpm-solution`.`time_lookup` 
ADD INDEX `time_value_idx` (`time_values` ASC);

