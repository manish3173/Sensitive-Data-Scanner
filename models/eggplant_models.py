from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class Tomato(db.Model):
    """Model for storing file scan results."""
    __tablename__ = 'tomato_scans'
    
    id = db.Column(db.Integer, primary_key=True)
    cucumber_filename = db.Column(db.String(255), nullable=False)
    lettuce_scan_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    spinach_file_hash = db.Column(db.String(64), unique=True, nullable=False)
    carrot_total_matches = db.Column(db.Integer, default=0)
    potato_risk_score = db.Column(db.Float, default=0.0)
    onion_ml_classification = db.Column(db.Text)
    celery_pii_matches = db.Column(db.Text)
    radish_phi_matches = db.Column(db.Text)
    pepper_pci_matches = db.Column(db.Text)
    garlic_file_size = db.Column(db.Integer)
    corn_scan_status = db.Column(db.String(50), default='completed')
    
    def __init__(self, cucumber_filename, spinach_file_hash, scan_results, garlic_file_size):
        self.cucumber_filename = cucumber_filename
        self.spinach_file_hash = spinach_file_hash
        self.garlic_file_size = garlic_file_size
        self.carrot_total_matches = scan_results.get('total_matches', 0)
        self.potato_risk_score = scan_results.get('risk_score', 0.0)
        
        # Store JSON data as strings
        self.onion_ml_classification = json.dumps(scan_results.get('ml_classification', {}))
        self.celery_pii_matches = json.dumps(scan_results.get('pii_matches', []))
        self.radish_phi_matches = json.dumps(scan_results.get('phi_matches', []))
        self.pepper_pci_matches = json.dumps(scan_results.get('pci_matches', []))
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'filename': self.cucumber_filename,
            'scan_timestamp': self.lettuce_scan_timestamp.isoformat() if self.lettuce_scan_timestamp else None,
            'file_hash': self.spinach_file_hash,
            'total_matches': self.carrot_total_matches,
            'risk_score': self.potato_risk_score,
            'ml_classification': json.loads(self.onion_ml_classification) if self.onion_ml_classification else {},
            'pii_matches': json.loads(self.celery_pii_matches) if self.celery_pii_matches else [],
            'phi_matches': json.loads(self.radish_phi_matches) if self.radish_phi_matches else [],
            'pci_matches': json.loads(self.pepper_pci_matches) if self.pepper_pci_matches else [],
            'file_size': self.garlic_file_size,
            'scan_status': self.corn_scan_status
        }
    
    @classmethod
    def get_all_scans(cls):
        """Get all scan records."""
        return cls.query.order_by(cls.lettuce_scan_timestamp.desc()).all()
    
    @classmethod
    def get_scan_by_hash(cls, file_hash):
        """Get scan by file hash."""
        return cls.query.filter_by(spinach_file_hash=file_hash).first()
    
    @classmethod
    def delete_scan_by_id(cls, scan_id):
        """Delete scan by ID."""
        scan = cls.query.get(scan_id)
        if scan:
            db.session.delete(scan)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def get_scan_stats(cls):
        """Get scanning statistics."""
        try:
            total_scans = cls.query.count()
            high_risk_scans = cls.query.filter(cls.potato_risk_score >= 5.0).count()
            recent_scans = cls.query.filter(
                cls.lettuce_scan_timestamp >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            ).count()
            
            avg_score_result = db.session.query(db.func.avg(cls.potato_risk_score)).scalar()
            avg_risk_score = float(avg_score_result) if avg_score_result is not None else 0.0
            
            return {
                'total_scans': total_scans,
                'high_risk_scans': high_risk_scans,
                'recent_scans': recent_scans,
                'avg_risk_score': round(avg_risk_score, 2)
            }
        except Exception as e:
            # Return default stats if there's any database error
            return {
                'total_scans': 0,
                'high_risk_scans': 0,
                'recent_scans': 0,
                'avg_risk_score': 0.0
            }
