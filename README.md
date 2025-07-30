# Sensitive Data Scanner

A comprehensive tool for scanning files to identify PII (Personally Identifiable Information), PHI (Protected Health Information), and PCI (Payment Card Information) using advanced regex patterns and machine learning classification.

## Features

- **Advanced Scanning**: Detects various types of sensitive data including SSN, PAN cards, credit cards, medical records, etc.
- **Machine Learning**: Uses trained ML models for intelligent data classification
- **Web Interface**: User-friendly HTML interface for file uploads and result viewing
- **REST API**: Complete API for programmatic access
- **Docker Ready**: Full containerization with Docker Compose

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL 8.0
- **ML Framework**: Scikit-learn
- **Containerization**: Docker & Docker Compose

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**

   ```bash
   git clone https://github.com/manish3173/Sensitive-Data-Scanner.git
   cd Sensitive-Data-Scanner
   ```

2. **Start all services:**

   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Web Interface: http://localhost
   - Direct App: http://localhost:5000
   - API: http://localhost:5000/api/

### Manual Setup

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Database:**

   ```sql
   CREATE DATABASE aurva_scanner;
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## Data Types Detected

### PII (Personally Identifiable Information)

- Social Security Numbers (SSN)
- PAN Card Numbers
- Email Addresses
- Phone Numbers
- Driver's License Numbers
- Passport Numbers

### PHI (Protected Health Information)

- Medical Record Numbers (MRN)
- Health Insurance Information
- Prescription Numbers
- Lab Result IDs
- Diagnosis Codes (ICD)
- National Provider Identifier (NPI)

### PCI (Payment Card Information)

- Credit Card Numbers (Visa, MasterCard, AMEX, Discover)
- CVV Codes
- Bank Account Numbers
- Routing Numbers



## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
