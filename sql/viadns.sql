SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema viadns
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `viadns` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `viadns` ;

-- -----------------------------------------------------
-- Table `viadns`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `viadns`.`session` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64) NOT NULL,
  `ipaddr` VARCHAR(64) NOT NULL,
  `session_id` VARCHAR(64) NOT NULL,
  `timeout_secs` INT(11) NOT NULL,
  `start_time` DATETIME NOT NULL,
  `timeout_time` DATETIME NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
