from ollama_service import generate_sql
from sql_validator import validate_select_query

SCHEMA_TEXT = """
Database schema for an E-District system with citizen records, certificate applications, and issued certificates.

Table citizens:
- id INT PRIMARY KEY AUTO_INCREMENT: unique citizen identifier
- full_name VARCHAR(200): citizen full legal name
- date_of_birth DATE: birth date for the citizen
- address VARCHAR(300): residential street address
- phone VARCHAR(50): contact phone number
- district VARCHAR(100): district or zone where the citizen resides

Table certificate_applications:
- id INT PRIMARY KEY AUTO_INCREMENT: unique application record ID
- citizen_id INT: foreign key referencing citizens(id), linking the application to a citizen
- certificate_type VARCHAR(100): certificate type such as 'Income', 'Residence', 'Birth', or 'Domicile'
- status VARCHAR(100): application status values like 'Pending', 'Approved', 'Rejected', or 'Cancelled'
- applied_at DATETIME: timestamp when the citizen submitted the application
- approved_at DATETIME: timestamp when the application was approved, null if not approved yet

Table issued_certificates:
- id INT PRIMARY KEY AUTO_INCREMENT: unique issued certificate ID
- application_id INT: foreign key referencing certificate_applications(id)
- issue_date DATE: date the certificate was issued
- expiration_date DATE: date when the certificate expires, if applicable
- details VARCHAR(400): additional notes or details about the issued certificate
"""

generated = generate_sql('list all citizens', SCHEMA_TEXT)
print('GENERATED:', repr(generated))
try:
    validated = validate_select_query(generated)
    print('VALIDATED:', repr(validated))
except Exception as e:
    print('VALIDATION ERROR:', str(e))
    raise
