"""
Legal Consultation Platform
Main application entry point
"""
import os
from app import create_app, db
from app.models import User, LawyerProfile, Consultation, Message

# Create Flask application
app = create_app(os.getenv('FLASK_ENV') or 'development')

# Shell context for Flask CLI
@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'LawyerProfile': LawyerProfile,
        'Consultation': Consultation,
        'Message': Message
    }

if __name__ == '__main__':
    # Create instance folder if it doesn't exist
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    # Run the application
    app.run(debug=True, host='127.0.0.1', port=5000)
