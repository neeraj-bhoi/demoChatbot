CREATE DATABASE IF NOT EXISTS edistrict;
USE edistrict;

CREATE TABLE IF NOT EXISTS citizens (
  id INT PRIMARY KEY AUTO_INCREMENT,
  full_name VARCHAR(200) NOT NULL,
  date_of_birth DATE,
  address VARCHAR(300),
  phone VARCHAR(50),
  district VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS certificate_applications (
  id INT PRIMARY KEY AUTO_INCREMENT,
  citizen_id INT NOT NULL,
  certificate_type VARCHAR(100) NOT NULL,
  status VARCHAR(100) NOT NULL,
  applied_at DATETIME,
  approved_at DATETIME,
  FOREIGN KEY (citizen_id) REFERENCES citizens(id)
);

CREATE TABLE IF NOT EXISTS issued_certificates (
  id INT PRIMARY KEY AUTO_INCREMENT,
  application_id INT NOT NULL,
  issue_date DATE,
  expiration_date DATE,
  details VARCHAR(400),
  FOREIGN KEY (application_id) REFERENCES certificate_applications(id)
);
