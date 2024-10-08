-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema solitaire
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `solitaire` DEFAULT CHARACTER SET utf8 ;
USE `solitaire` ;

-- -----------------------------------------------------
-- Table `solitaire`.`Players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `solitaire`.`Players` ;

CREATE TABLE IF NOT EXISTS `solitaire`.`Players` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (name)
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `solitaire`.`Games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `solitaire`.`Games` ;

CREATE TABLE IF NOT EXISTS `solitaire`.`Games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `score` INT NOT NULL,
  `datetime` DATETIME NOT NULL,
  `Players_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Games_Players_idx` (`Players_id` ASC) VISIBLE,
  CONSTRAINT `fk_Games_Players`
    FOREIGN KEY (`Players_id`)
    REFERENCES `solitaire`.`Players` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;