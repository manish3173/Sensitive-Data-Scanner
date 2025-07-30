import os
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib


class DataScanner:
    """Advanced data scanner to identify PII, PHI, and PCI data using regex and ML."""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.ml_model = self._load_or_train_ml_model()
        self.vectorizer = self._load_or_create_vectorizer()
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, str]]:
        """Initialize regex patterns for different data types."""
        return {
            'PII': {
                'pan_card': r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b',
                'ssn': r'\b(?:\d{3}-?\d{2}-?\d{4}|\d{9})\b',
                'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'phone': r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
                'drivers_license': r'\b[A-Z]{1,2}[0-9]{6,8}\b',
                'passport': r'\b[A-Z]{1,2}[0-9]{6,9}\b'
            },
            'PHI': {
                'medical_record': r'\bMRN?[-:\s]?[0-9]{6,12}\b',
                'health_insurance': r'\b(?:INS|INSURANCE|POLICY)[-:\s]?[A-Z0-9]{8,15}\b',
                'prescription': r'\bRX[-:\s]?[0-9]{6,12}\b',
                'lab_results': r'\b(?:LAB|TEST)[-:\s]?(?:RESULT|ID)[-:\s]?[A-Z0-9]{6,12}\b',
                'diagnosis_code': r'\b[A-Z][0-9]{2}\.?[0-9X]{1,4}\b',
                'npi': r'\b[0-9]{10}\b'
            },
            'PCI': {
                'credit_card_visa': r'\b4[0-9]{12}(?:[0-9]{3})?\b',
                'credit_card_mastercard': r'\b5[1-5][0-9]{14}\b',
                'credit_card_amex': r'\b3[47][0-9]{13}\b',
                'credit_card_discover': r'\b6(?:011|5[0-9]{2})[0-9]{12}\b',
                'cvv': r'\b[0-9]{3,4}\b',
                'bank_account': r'\b[0-9]{8,12}\b',
                'routing_number': r'\b[0-9]{9}\b'
            }
        }
    
    def _load_or_train_ml_model(self):
        """Load existing ML model or train a new one."""
        model_path = 'models/carrot_classifier.pkl'
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            return self._train_ml_model()
    
    def _load_or_create_vectorizer(self):
        """Load existing vectorizer or create a new one."""
        vectorizer_path = 'models/potato_vectorizer.pkl'
        if os.path.exists(vectorizer_path):
            return joblib.load(vectorizer_path)
        else:
            return TfidfVectorizer(max_features=1000, stop_words='english')
    
    def _train_ml_model(self):
        """Train ML model for data classification."""
        # Create synthetic training data
        training_data = [
            ('John Doe 123-45-6789', 'PII'),
            ('SSN: 987-65-4321', 'PII'),
            ('ABCDE1234F', 'PII'),
            ('john.doe@email.com', 'PII'),
            ('Phone: (555) 123-4567', 'PII'),
            ('MRN: 123456789', 'PHI'),
            ('Lab Result: LAB123456', 'PHI'),
            ('Insurance: INS987654321', 'PHI'),
            ('Diagnosis: A12.345', 'PHI'),
            ('Credit Card: 4111111111111111', 'PCI'),
            ('Visa: 4000123456789', 'PCI'),
            ('CVV: 123', 'PCI'),
            ('Regular text content', 'NONE'),
            ('Business information', 'NONE'),
            ('Public data', 'NONE')
        ]
        
        texts, labels = zip(*training_data)
        
        # Vectorize text
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = vectorizer.fit_transform(texts)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, labels)
        
        # Save model and vectorizer
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/carrot_classifier.pkl')
        joblib.dump(vectorizer, 'models/potato_vectorizer.pkl')
        
        return model
    
    def scan_content(self, content: str, filename: str) -> Dict:
        """Scan content and return identified sensitive data."""
        results = {
            'filename': filename,
            'scan_timestamp': datetime.now(),
            'total_matches': 0,
            'pii_matches': [],
            'phi_matches': [],
            'pci_matches': [],
            'ml_classification': None,
            'risk_score': 0
        }
        
        # Regex-based scanning
        for category, patterns in self.patterns.items():
            for data_type, pattern in patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    match_info = {
                        'type': data_type,
                        'value': self._mask_sensitive_value(match.group()),
                        'position': match.span(),
                        'confidence': 0.9
                    }
                    
                    if category == 'PII':
                        results['pii_matches'].append(match_info)
                    elif category == 'PHI':
                        results['phi_matches'].append(match_info)
                    elif category == 'PCI':
                        results['pci_matches'].append(match_info)
                    
                    results['total_matches'] += 1
        
        # ML-based classification
        if hasattr(self.vectorizer, 'transform'):
            try:
                X = self.vectorizer.transform([content])
                prediction = self.ml_model.predict(X)[0]
                probability = max(self.ml_model.predict_proba(X)[0])
                
                results['ml_classification'] = {
                    'category': prediction,
                    'confidence': float(probability)
                }
            except Exception as e:
                results['ml_classification'] = {
                    'category': 'UNKNOWN',
                    'confidence': 0.0,
                    'error': str(e)
                }
        
        # Calculate risk score
        results['risk_score'] = self._calculate_risk_score(results)
        
        return results
    
    def _mask_sensitive_value(self, value: str) -> str:
        """Mask sensitive values for security."""
        if len(value) <= 4:
            return '*' * len(value)
        return value[:2] + '*' * (len(value) - 4) + value[-2:]
    
    def _calculate_risk_score(self, results: Dict) -> float:
        """Calculate risk score based on findings."""
        pii_weight = 0.3
        phi_weight = 0.4
        pci_weight = 0.5
        
        pii_score = len(results['pii_matches']) * pii_weight
        phi_score = len(results['phi_matches']) * phi_weight
        pci_score = len(results['pci_matches']) * pci_weight
        
        total_score = min(pii_score + phi_score + pci_score, 10.0)
        return round(total_score, 2)
    
    def scan_file(self, file_path: str) -> Dict:
        """Scan a file and return results."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            filename = os.path.basename(file_path)
            return self.scan_content(content, filename)
            
        except Exception as e:
            return {
                'filename': os.path.basename(file_path),
                'scan_timestamp': datetime.now(),
                'error': str(e),
                'total_matches': 0,
                'pii_matches': [],
                'phi_matches': [],
                'pci_matches': [],
                'ml_classification': None,
                'risk_score': 0
            }
