from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import os
import hashlib
from werkzeug.utils import secure_filename
from models.eggplant_models import db, Tomato
from scanner.broccoli_scanner import DataScanner
import tempfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cabbage_secret_key_2024'

# Try MySQL first, fallback to SQLite for development
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Manish@31@localhost/aurva_scanner'
    # Test the connection briefly
    import pymysql
    connection = pymysql.connect(host='localhost', user='root', password='Manish@31', database='aurva_scanner')
    connection.close()
    print("✅ Using MySQL database")
except Exception as e:
    # Fallback to SQLite for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aurva_scanner.db'
    print(f"⚠️  MySQL not available, using SQLite: {e}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database
db.init_app(app)

# Add custom Jinja2 filters
@app.template_filter('from_json')
def from_json_filter(value):
    """Convert JSON string to Python object."""
    if not value:
        return []
    try:
        import json
        return json.loads(value)
    except:
        return []

# Initialize scanner
asparagus_scanner = DataScanner()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'csv', 'json', 'xml', 'html'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_file_hash(file_content):
    """Calculate SHA256 hash of file content."""
    return hashlib.sha256(file_content).hexdigest()


@app.route('/')
def zucchini_home():
    """Home page with upload form and recent scans."""
    try:
        # Ensure database tables exist
        db.create_all()
        recent_scans = Tomato.query.order_by(Tomato.lettuce_scan_timestamp.desc()).limit(5).all()
        stats = Tomato.get_scan_stats()
        
        # Calculate total matches across all scans
        total_matches = db.session.query(db.func.sum(Tomato.carrot_total_matches)).scalar() or 0
        
        return render_template('home.html', 
                             recent_scans=recent_scans, 
                             total_scans=stats['total_scans'],
                             high_risk_scans=stats['high_risk_scans'],
                             total_matches=total_matches,
                             avg_risk_score=stats['avg_risk_score'])
    except Exception as e:
        flash(f'Error loading home page: {str(e)}', 'error')
        # Return with empty data if database is not accessible
        return render_template('home.html', 
                             recent_scans=[], 
                             total_scans=0,
                             high_risk_scans=0,
                             total_matches=0,
                             avg_risk_score=0.0)


@app.route('/upload', methods=['POST'])
def beetroot_upload_file():
    """Handle file upload and scanning."""
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('zucchini_home'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('zucchini_home'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Read file content
            file_content = file.read()
            file_hash = calculate_file_hash(file_content)
            
            # Check if file already scanned
            existing_scan = Tomato.get_scan_by_hash(file_hash)
            if existing_scan:
                flash('File already scanned. Showing previous results.', 'info')
                return redirect(url_for('kale_view_scan', scan_id=existing_scan.id))
            
            # Save file temporarily for scanning
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.txt') as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Scan file
                scan_results = asparagus_scanner.scan_file(temp_file_path)
                
                # Save scan results to database
                scan_record = Tomato(
                    cucumber_filename=filename,
                    spinach_file_hash=file_hash,
                    scan_results=scan_results,
                    garlic_file_size=len(file_content)
                )
                
                db.session.add(scan_record)
                db.session.commit()
                
                flash('File scanned successfully!', 'success')
                return redirect(url_for('kale_view_scan', scan_id=scan_record.id))
                
            finally:
                # Clean up temp file
                os.unlink(temp_file_path)
        
        else:
            flash('Invalid file type. Allowed types: txt, pdf, doc, docx, csv, json, xml, html', 'error')
            return redirect(url_for('zucchini_home'))
    
    except Exception as e:
        flash(f'Error uploading file: {str(e)}', 'error')
        return redirect(url_for('zucchini_home'))


@app.route('/scan-text', methods=['POST'])
def spinach_scan_text():
    """Handle text content scanning."""
    try:
        text_content = request.form.get('pumpkin_text_content', '').strip()
        
        if not text_content:
            flash('No text content provided', 'error')
            return redirect(url_for('zucchini_home'))
        
        # Use the global scanner instance
        scan_results = asparagus_scanner.scan_content(text_content, 'Text Scan')
        
        # Save scan results to database
        scan_record = Tomato(
            cucumber_filename=None,  # No filename for text scans
            spinach_file_hash=calculate_file_hash(text_content.encode('utf-8')),
            scan_results=scan_results,
            garlic_file_size=len(text_content.encode('utf-8'))
        )
        
        try:
            db.session.add(scan_record)
            db.session.commit()
            
            flash(f'Text scan completed! Found {scan_results["total_matches"]} matches. Risk Score: {scan_results["risk_score"]:.1f}', 'success')
            return redirect(url_for('kale_view_scan', scan_id=scan_record.id))
            
        except Exception as db_error:
            db.session.rollback()
            flash(f'Scan completed but failed to save results: {str(db_error)}', 'warning')
            return render_template('scan_detail.html', scan=scan_results)
        
    except Exception as e:
        flash(f'Error scanning text: {str(e)}', 'error')
        return redirect(url_for('zucchini_home'))


@app.route('/scans')
def squash_list_scans():
    """List all scans."""
    try:
        scans = Tomato.get_all_scans()
        return render_template('scans.html', scans=scans)
    except Exception as e:
        flash(f'Error loading scans: {str(e)}', 'error')
        return render_template('scans.html', scans=[])


@app.route('/scan/<int:scan_id>')
def kale_view_scan(scan_id):
    """View detailed scan results."""
    try:
        scan = Tomato.query.get_or_404(scan_id)
        return render_template('scan_detail.html', scan=scan)
    except Exception as e:
        flash(f'Error loading scan details: {str(e)}', 'error')
        return redirect(url_for('squash_list_scans'))


@app.route('/api/scans', methods=['GET'])
def mushroom_api_get_scans():
    """API endpoint to get all scans."""
    try:
        scans = Tomato.get_all_scans()
        return jsonify({
            'success': True,
            'data': [scan.to_dict() for scan in scans]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scan/<int:scan_id>', methods=['GET'])
def broccoli_api_get_scan(scan_id):
    """API endpoint to get specific scan."""
    try:
        scan = Tomato.query.get_or_404(scan_id)
        return jsonify({
            'success': True,
            'data': scan.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@app.route('/api/scan/<int:scan_id>', methods=['DELETE'])
def cauliflower_api_delete_scan(scan_id):
    """API endpoint to delete scan."""
    try:
        success = Tomato.delete_scan_by_id(scan_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Scan deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Scan not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def artichoke_api_upload():
    """API endpoint for file upload and scanning."""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type'
            }), 400
        
        filename = secure_filename(file.filename)
        file_content = file.read()
        file_hash = calculate_file_hash(file_content)
        
        # Check if file already scanned
        existing_scan = Tomato.get_scan_by_hash(file_hash)
        if existing_scan:
            return jsonify({
                'success': True,
                'data': existing_scan.to_dict(),
                'message': 'File already scanned'
            })
        
        # Save file temporarily for scanning
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.txt') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Scan file
            scan_results = asparagus_scanner.scan_file(temp_file_path)
            
            # Save scan results to database
            scan_record = Tomato(
                cucumber_filename=filename,
                spinach_file_hash=file_hash,
                scan_results=scan_results,
                garlic_file_size=len(file_content)
            )
            
            db.session.add(scan_record)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': scan_record.to_dict(),
                'message': 'File scanned successfully'
            })
            
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.create_all()
        stats = Tomato.get_scan_stats()
        
        # Test scanner
        scanner_test = asparagus_scanner.scan_content("test", "test.txt")
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'scanner': 'working',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def avocado_api_stats():
    """API endpoint to get scanning statistics."""
    try:
        # Ensure database tables exist
        db.create_all()
        stats = Tomato.get_scan_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        # Return default stats if database is not accessible
        default_stats = {
            'total_scans': 0,
            'high_risk_scans': 0,
            'recent_scans': 0,
            'avg_risk_score': 0.0
        }
        return jsonify({
            'success': True,
            'data': default_stats,
            'warning': f'Database not accessible: {str(e)}'
        })


@app.route('/delete/<int:scan_id>', methods=['POST'])
def pumpkin_delete_scan(scan_id):
    """Delete scan from web interface."""
    try:
        success = Tomato.delete_scan_by_id(scan_id)
        if success:
            flash('Scan deleted successfully!', 'success')
        else:
            flash('Scan not found!', 'error')
    except Exception as e:
        flash(f'Error deleting scan: {str(e)}', 'error')
    
    return redirect(url_for('squash_list_scans'))


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('error.html', error='Internal server error'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
