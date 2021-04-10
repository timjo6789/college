-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema college
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema college
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `college` DEFAULT CHARACTER SET utf8 ;
USE `college` ;

-- -----------------------------------------------------
-- Table `college`.`difficulty`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `college`.`difficulty` (
  `Difficulty` VARCHAR(6) NOT NULL,
  `Multiplier` INT NOT NULL,
  PRIMARY KEY (`Difficulty`),
  UNIQUE INDEX `idDifficulty_UNIQUE` (`Difficulty` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `college`.`classes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `college`.`classes` (
  `Class` VARCHAR(45) NOT NULL,
  `Semester` VARCHAR(45) NOT NULL,
  `Year` VARCHAR(4) NOT NULL,
  `credits` DECIMAL(3,1) NOT NULL,
  `Difficulty` VARCHAR(6) NOT NULL,
  PRIMARY KEY (`Class`),
  UNIQUE INDEX `Class_UNIQUE` (`Class` ASC) VISIBLE,
  INDEX `Difficulty` (`Difficulty` ASC) VISIBLE,
  CONSTRAINT `classes_ibfk_1`
    FOREIGN KEY (`Difficulty`)
    REFERENCES `college`.`difficulty` (`Difficulty`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `college`.`assignment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `college`.`assignment` (
  `Assignment_ID` INT NOT NULL AUTO_INCREMENT,
  `Class` VARCHAR(45) NOT NULL,
  `Week` VARCHAR(3) NOT NULL,
  `Group_name` VARCHAR(200) NULL DEFAULT NULL,
  `Type` VARCHAR(45) NULL DEFAULT NULL,
  `Title` VARCHAR(200) NULL DEFAULT NULL,
  `Deadline` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`Assignment_ID`),
  INDEX `fk_Assignment_Classes1_idx` (`Class` ASC) VISIBLE,
  CONSTRAINT `fk_Assignment_Classes1`
    FOREIGN KEY (`Class`)
    REFERENCES `college`.`classes` (`Class`))
ENGINE = InnoDB
AUTO_INCREMENT = 1118
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `college`.`tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `college`.`tasks` (
  `Assignment_ID` INT NOT NULL,
  `Task_number` INT NOT NULL,
  `Task` MEDIUMTEXT NOT NULL,
  `Duration` INT NOT NULL DEFAULT '0',
  `Done` TINYINT NOT NULL DEFAULT '0',
  `date_completed` DATE NULL DEFAULT NULL,
  INDEX `fk_Tasks_Assignment1_idx` (`Assignment_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Tasks_Assignment1`
    FOREIGN KEY (`Assignment_ID`)
    REFERENCES `college`.`assignment` (`Assignment_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

USE `college` ;

-- -----------------------------------------------------
-- function PRETTY_TIME
-- -----------------------------------------------------

DELIMITER $$
USE `college`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `PRETTY_TIME`(seconds BIGINT) RETURNS varchar(25) CHARSET utf8
BEGIN
	DECLARE pretty VARCHAR(25);
    SET pretty = IF( seconds >= 0,
					CONCAT(FLOOR(seconds / 3600), ':', LPAD(MOD(FLOOR(seconds / 60), 60), 2, '0'), ':', LPAD(MOD(seconds, 60), 2, '0')),
					CONCAT(FLOOR(ABS(seconds) / 3600), ':', LPAD(MOD(FLOOR(ABS(seconds) / 60), 60), 2, '0'), ':', LPAD(MOD(ABS(seconds), 60), 2, '0'), ' overtime')
        );
	RETURN pretty;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
