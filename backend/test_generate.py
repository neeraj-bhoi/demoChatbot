from ollama_service import generate_sql

SCHEMA_TEXT = """
Table citizens(id INT PRIMARY KEY AUTO_INCREMENT, full_name VARCHAR(200), date_of_birth DATE, address VARCHAR(300), phone VARCHAR(50), district VARCHAR(100));
Table certificate_applications(id INT PRIMARY KEY AUTO_INCREMENT, citizen_id INT, certificate_type VARCHAR(100), status VARCHAR(100), applied_at DATETIME, approved_at DATETIME, FOREIGN KEY (citizen_id) REFERENCES citizens(id));
Table issued_certificates(id INT PRIMARY KEY AUTO_INCREMENT, application_id INT, issue_date DATE, expiration_date DATE, details VARCHAR(400), FOREIGN KEY (application_id) REFERENCES certificate_applications(id));
"""

try:
    out = generate_sql('list all citizens', SCHEMA_TEXT)
    print('=== GENERATED ===')
    print(out)
except Exception as e:
    print('=== ERROR ===')
    print(str(e))
