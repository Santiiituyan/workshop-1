-- -----------------------------------------------------
-- Schema etl_workshop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `etl_workshop` DEFAULT CHARACTER SET utf8 ;
USE `etl_workshop` ;

-- ==========================================
-- DATA WAREHOUSE CREATION SCRIPT (DDL)
-- ==========================================

-- 1. Create Location Dimension
CREATE TABLE IF NOT EXISTS Dim_Location (
    Location_SK INT AUTO_INCREMENT PRIMARY KEY,
    Country VARCHAR(100) NOT NULL
);

-- 2. Create Technology Dimension
CREATE TABLE IF NOT EXISTS Dim_Technology (
    Technology_SK INT AUTO_INCREMENT PRIMARY KEY,
    Technology_Name VARCHAR(100) NOT NULL
);

-- 3. Create Date Dimension
CREATE TABLE IF NOT EXISTS Dim_Date (
    Date_SK INT PRIMARY KEY, 
    Full_Date DATE NOT NULL,
    Year INT NOT NULL,
    Month INT NOT NULL,
    Day INT NOT NULL
);

-- 4. Create Candidate Dimension
CREATE TABLE IF NOT EXISTS Dim_Candidate (
    Candidate_SK INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(100) NOT NULL,
    Last_Name VARCHAR(100) NOT NULL,
    Email VARCHAR(150) NOT NULL,
    Seniority VARCHAR(50) NOT NULL,
    YOE INT NOT NULL
);

-- 5. Create Fact Table
-- This table is created last as it depends on the Foreign Keys (FK) from the dimensions.
CREATE TABLE IF NOT EXISTS Fact_Applications (
    Application_SK INT AUTO_INCREMENT PRIMARY KEY,
    Candidate_SK INT NOT NULL,
    Technology_SK INT NOT NULL,
    Location_SK INT NOT NULL,
    Date_SK INT NOT NULL,
    Code_Challenge_Score INT NOT NULL,
    Technical_Interview_Score INT NOT NULL,
    Is_Hired BOOLEAN NOT NULL,
    
    -- Referential Integrity Constraints (Foreign Keys)
    FOREIGN KEY (Candidate_SK) REFERENCES Dim_Candidate(Candidate_SK),
    FOREIGN KEY (Technology_SK) REFERENCES Dim_Technology(Technology_SK),
    FOREIGN KEY (Location_SK) REFERENCES Dim_Location(Location_SK),
    FOREIGN KEY (Date_SK) REFERENCES Dim_Date(Date_SK)
);