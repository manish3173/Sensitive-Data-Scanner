#!/usr/bin/env python3
"""
Database initialization script for Aurva Data Scanner.
This script creates the database tables and ensures proper setup.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize the database with proper tables."""
    try:
        from app import app, db
        
        with app.app_context():
            print("🗄️  Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Test the database by getting stats
            from models.eggplant_models import Tomato
            stats = Tomato.get_scan_stats()
            print(f"📊 Database test successful: {stats}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def main():
    """Main initialization function."""
    print("🥕 Aurva Data Scanner - Database Initialization")
    print("=" * 50)
    
    success = init_database()
    
    if success:
        print("✅ Database initialization completed successfully!")
        print("🚀 You can now run the application with: python app.py")
    else:
        print("❌ Database initialization failed!")
        print("💡 The application will use SQLite as fallback")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
