USE edistrict;

INSERT INTO citizens (full_name, date_of_birth, address, phone, district) VALUES
('Anjali Sharma', '1988-04-12', '12 Rose Avenue', '9876543210', 'Central'),
('Rakesh Kumar', '1975-10-21', '45 Lake Road', '9123456780', 'North'),
('Priya Singh', '1993-01-05', '99 Garden Street', '9988776655', 'East');

INSERT INTO certificate_applications (citizen_id, certificate_type, status, applied_at, approved_at) VALUES
(1, 'Income', 'Approved', '2026-05-01 09:30:00', '2026-05-03 14:00:00'),
(2, 'Residence', 'Pending', '2026-05-05 11:20:00', NULL),
(3, 'Income', 'Rejected', '2026-05-02 15:45:00', NULL),
(1, 'Income', 'Approved', '2026-05-10 10:00:00', '2026-05-12 09:00:00');

INSERT INTO issued_certificates (application_id, issue_date, expiration_date, details) VALUES
(1, '2026-05-04', '2027-05-04', 'Income certificate for Anjali Sharma'),
(4, '2026-05-13', '2027-05-13', 'Income certificate for Anjali Sharma');

-- Additional dummy records
INSERT INTO citizens (full_name, date_of_birth, address, phone, district) VALUES
('Vivek Patel', '1982-06-17', '23 Ocean Blvd', '9012345678', 'West'),
('Suman Rao', '1990-07-22', '78 Hill Top', '9023456781', 'South'),
('Meena Iyer', '1979-12-03', '5 Lakeview', '9034567892', 'Central'),
('Arjun Desai', '1985-09-10', '210 River Road', '9045678903', 'East'),
('Kavita Nair', '1992-03-25', '66 Palm Street', '9056789014', 'North'),
('Deepak Singh', '1970-11-30', '11 Market Lane', '9067890125', 'West'),
('Neha Verma', '1995-02-14', '42 Sunset Blvd', '9078901236', 'South'),
('Rahul Joshi', '1988-08-08', '9 Pine Drive', '9089012347', 'Central'),
('Pooja Kulkarni', '1991-04-19', '100 Cedar Ave', '9090123458', 'East'),
('Manish Sharma', '1976-01-05', '31 Oak Road', '9101234569', 'North'),
('Anita Gupta', '1983-10-29', '7 Rosewood', '9112345670', 'West'),
('Sahil Kapoor', '1994-06-02', '55 Brookside', '9123456781', 'South');

INSERT INTO certificate_applications (citizen_id, certificate_type, status, applied_at, approved_at) VALUES
(4, 'Residence', 'Approved', '2026-05-15 10:15:00', '2026-05-16 09:00:00'),
(5, 'Income', 'Pending', '2026-05-16 12:30:00', NULL),
(6, 'Birth', 'Approved', '2026-05-17 08:45:00', '2026-05-18 11:00:00'),
(7, 'Domicile', 'Rejected', '2026-05-18 14:20:00', NULL),
(8, 'Income', 'Approved', '2026-05-19 09:10:00', '2026-05-20 10:00:00'),
(9, 'Residence', 'Pending', '2026-05-20 16:40:00', NULL),
(10, 'Income', 'Approved', '2026-05-21 11:00:00', '2026-05-22 13:30:00'),
(11, 'Birth', 'Approved', '2026-05-22 09:25:00', '2026-05-23 08:00:00'),
(12, 'Domicile', 'Pending', '2026-05-23 15:50:00', NULL),
(13, 'Income', 'Approved', '2026-05-24 10:05:00', '2026-05-25 12:15:00');

INSERT INTO issued_certificates (application_id, issue_date, expiration_date, details) VALUES
(5, '2026-05-16', '2027-05-16', 'Residence certificate for Vivek Patel'),
(6, '2026-05-18', '2027-05-18', 'Income certificate for Suman Rao'),
(7, '2026-05-20', '2027-05-20', 'Birth certificate for Meena Iyer'),
(8, '2026-05-21', '2027-05-21', 'Domicile certificate for Arjun Desai');
