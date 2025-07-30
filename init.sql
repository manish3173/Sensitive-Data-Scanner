-- Initialize the database
CREATE DATABASE IF NOT EXISTS aurva_scanner;
USE aurva_scanner;

-- Create user if not exists
CREATE USER IF NOT EXISTS 'aurva_user'@'%' IDENTIFIED BY 'Manish@31';
GRANT ALL PRIVILEGES ON aurva_scanner.* TO 'aurva_user'@'%';
FLUSH PRIVILEGES;

-- Create initial table structure (Flask-Migrate will handle this, but this is backup)
CREATE TABLE IF NOT EXISTS tomato_scans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cucumber_filename VARCHAR(255) NOT NULL,
    lettuce_scan_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    spinach_file_hash VARCHAR(64) NOT NULL UNIQUE,
    carrot_total_matches INT DEFAULT 0,
    potato_risk_score FLOAT DEFAULT 0.0,
    onion_ml_classification TEXT,
    celery_pii_matches TEXT,
    radish_phi_matches TEXT,
    pepper_pci_matches TEXT,
    garlic_file_size INT,
    corn_scan_status VARCHAR(50) DEFAULT 'completed',
    INDEX idx_filename (cucumber_filename),
    INDEX idx_timestamp (lettuce_scan_timestamp),
    INDEX idx_risk_score (potato_risk_score),
    INDEX idx_file_hash (spinach_file_hash)
);
