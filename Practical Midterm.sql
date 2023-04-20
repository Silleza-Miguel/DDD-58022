CREATE DATABASE ABC_COMPUTERS;

CREATE TABLE ABC_COMPUTERS.Computer
(SerialNumber BIGINT PRIMARY KEY,
Make Text(12) NULL, 
Model Text(24), 
ProcessorType Text(24), 
ProcessorSpeed BIGINT, 
MainMemory Text(15),
DiskSize Text(15));

INSERT INTO ABC_COMPUTERS.computer
VALUES ('9871234', 'HP', 'Pavillion 500-210qe', 'Intel i5-4530', '3.00', '6.0 Gbytes', '1.0 Tbytes'),
('9871245', 'HP', 'Pavillion 500-210qe', 'Intel i5-4531', '3.00', '6.0 Gbytes', '1.0 Tbytes'), 
('9871256', 'HP', 'Pavillion 500-210qe', 'Intel i5-4532', '3.00', '6.0 Gbytes', '1.0 Tbytes'),
('9871267', 'HP', 'Pavillion 500-210qe', 'Intel i5-4533', '3.00', '6.0 Gbytes', '1.0 Tbytes'), 
('9871278', 'HP', 'Pavillion 500-210qe', 'Intel i5-4534', '3.00', '6.0 Gbytes', '1.0 Tbytes'), 
('9871289', 'HP', 'Pavillion 500-210qe', 'Intel i5-4535', '3.00', '6.0 Gbytes', '1.0 Tbytes'), 

('6541001', 'Dell', 'OptiPlex 9020', 'Intel i7-4770', '3.00', '8.0 Gbytes', '1.0 Tbytes'),
('6541002', 'Dell', 'OptiPlex 9021', 'Intel i7-4771', '3.00', '8.0 Gbytes', '1.0 Tbytes'),
('6541003', 'Dell', 'OptiPlex 9022', 'Intel i7-4772', '3.00', '8.0 Gbytes', '1.0 Tbytes'),
('6541004', 'Dell', 'OptiPlex 9023', 'Intel i7-4773', '3.00', '8.0 Gbytes', '1.0 Tbytes'),
('6541005', 'Dell', 'OptiPlex 9024', 'Intel i7-4774', '3.00', '8.0 Gbytes', '1.0 Tbytes'),
('6541006', 'Dell', 'OptiPlex 9025', 'Intel i7-4775', '3.00', '8.0 Gbytes', '1.0 Tbytes');

SELECT * FROM ABC_COMPUTERS.computer
WHERE Make = 'HP';

SELECT * FROM ABC_COMPUTERS.computer
WHERE Make = 'Dell';

ALTER TABLE ABC_COMPUTERS.computer
ADD COLUMN Graphics Text(40) AFTER DiskSize;

UPDATE ABC_COMPUTERS.computer
SET Graphics = 'Integrated Intel HD Graphics 4600';

ALTER TABLE ABC_COMPUTERS.computer
DROP ProcessorSpeed;

SELECT * FROM ABC_COMPUTERS.computer





