"""
Web-based Database Viewer
Run this script and open http://127.0.0.1:5001 in your browser
"""
from flask import Flask, render_template_string
from app import create_app, db
from app.models import User, LawyerProfile, Consultation, Message, LegalAct, LegalSection

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Database Viewer - Law Project</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .section {
            margin-bottom: 40px;
        }
        .section-title {
            background: #f8f9fa;
            padding: 15px 20px;
            border-left: 5px solid #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            background: white;
        }
        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge-admin { background: #ff6b6b; color: white; }
        .badge-lawyer { background: #4ecdc4; color: white; }
        .badge-customer { background: #95e1d3; color: #333; }
        .badge-verified { background: #51cf66; color: white; }
        .badge-pending { background: #ffd93d; color: #333; }
        .badge-active { background: #51cf66; color: white; }
        .badge-inactive { background: #adb5bd; color: white; }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ Database Viewer</h1>
        <p class="subtitle">Law Project - Real-time Database Contents</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.users }}</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.lawyers }}</div>
                <div class="stat-label">Lawyer Profiles</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.consultations }}</div>
                <div class="stat-label">Consultations</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.messages }}</div>
                <div class="stat-label">Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.acts }}</div>
                <div class="stat-label">Legal Acts</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.sections }}</div>
                <div class="stat-label">Legal Sections</div>
            </div>
        </div>

        <!-- Users Table -->
        <div class="section">
            <div class="section-title">👥 Users</div>
            {% if users %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Email</th>
                        <th>Full Name</th>
                        <th>Phone</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.full_name }}</td>
                        <td>{{ user.phone or 'N/A' }}</td>
                        <td>
                            <span class="badge badge-{{ user.role }}">{{ user.role }}</span>
                        </td>
                        <td>
                            <span class="badge badge-{{ 'active' if user.is_active else 'inactive' }}">
                                {{ 'Active' if user.is_active else 'Inactive' }}
                            </span>
                        </td>
                        <td>{{ user.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">No users found in database</div>
            {% endif %}
        </div>

        <!-- Lawyer Profiles -->
        <div class="section">
            <div class="section-title">⚖️ Lawyer Profiles</div>
            {% if lawyers %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Lawyer Name</th>
                        <th>Bar Council ID</th>
                        <th>Experience</th>
                        <th>Fee</th>
                        <th>Verification</th>
                    </tr>
                </thead>
                <tbody>
                    {% for lawyer in lawyers %}
                    <tr>
                        <td>{{ lawyer.id }}</td>
                        <td>{{ lawyer.user.full_name }}</td>
                        <td>{{ lawyer.bar_council_id }}</td>
                        <td>{{ lawyer.experience_years or 'N/A' }} years</td>
                        <td>₹{{ lawyer.consultation_fee or 'N/A' }}</td>
                        <td>
                            <span class="badge badge-{{ lawyer.verification_status }}">
                                {{ lawyer.verification_status }}
                            </span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">No lawyer profiles found</div>
            {% endif %}
        </div>

        <!-- Consultations -->
        <div class="section">
            <div class="section-title">📅 Consultations</div>
            {% if consultations %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Customer</th>
                        <th>Lawyer</th>
                        <th>Date</th>
                        <th>Category</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for consult in consultations %}
                    <tr>
                        <td>{{ consult.id }}</td>
                        <td>{{ consult.customer.full_name }}</td>
                        <td>{{ consult.lawyer.full_name }}</td>
                        <td>{{ consult.consultation_date.strftime('%Y-%m-%d %H:%M') }}</td>
                        <td>{{ consult.category or 'N/A' }}</td>
                        <td>
                            <span class="badge badge-{{ consult.status }}">{{ consult.status }}</span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">No consultations found</div>
            {% endif %}
        </div>

        <!-- Legal Acts -->
        <div class="section">
            <div class="section-title">📚 Legal Acts</div>
            {% if acts %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Short Name</th>
                        <th>Full Name</th>
                        <th>Year</th>
                        <th>Category</th>
                        <th>Total Sections</th>
                    </tr>
                </thead>
                <tbody>
                    {% for act in acts %}
                    <tr>
                        <td>{{ act.id }}</td>
                        <td><strong>{{ act.short_name }}</strong></td>
                        <td>{{ act.name }}</td>
                        <td>{{ act.year }}</td>
                        <td>{{ act.category }}</td>
                        <td>{{ act.total_sections }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">No legal acts found</div>
            {% endif %}
        </div>

        <!-- Legal Sections (Sample) -->
        <div class="section">
            <div class="section-title">📜 Legal Sections (First 20)</div>
            {% if sections %}
            <table>
                <thead>
                    <tr>
                        <th>Section</th>
                        <th>Act</th>
                        <th>Title</th>
                        <th>Bailable</th>
                        <th>Cognizable</th>
                    </tr>
                </thead>
                <tbody>
                    {% for section in sections[:20] %}
                    <tr>
                        <td><strong>{{ section.section_number }}</strong></td>
                        <td>{{ section.act.short_name }}</td>
                        <td>{{ section.title[:80] }}...</td>
                        <td>{{ '✓' if section.is_bailable else '✗' }}</td>
                        <td>{{ '✓' if section.is_cognizable else '✗' }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% if sections|length > 20 %}
            <p style="text-align: center; color: #666; margin-top: 10px;">
                ... and {{ sections|length - 20 }} more sections
            </p>
            {% endif %}
            {% else %}
            <div class="empty-state">No legal sections found</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

def view_database():
    """Create a web viewer for the database"""
    app = create_app()
    
    @app.route('/db-viewer')
    def database_viewer():
        with app.app_context():
            # Fetch all data
            users = User.query.all()
            lawyers = LawyerProfile.query.all()
            consultations = Consultation.query.all()
            messages = Message.query.all()
            acts = LegalAct.query.all()
            sections = LegalSection.query.all()
            
            stats = {
                'users': len(users),
                'lawyers': len(lawyers),
                'consultations': len(consultations),
                'messages': len(messages),
                'acts': len(acts),
                'sections': len(sections)
            }
            
            return render_template_string(
                HTML_TEMPLATE,
                users=users,
                lawyers=lawyers,
                consultations=consultations,
                messages=messages,
                acts=acts,
                sections=sections,
                stats=stats
            )
    
    print("\n" + "="*80)
    print("DATABASE VIEWER STARTED")
    print("="*80)
    print("\n🌐 Open your browser and go to: http://127.0.0.1:5001/db-viewer")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=5001, use_reloader=False)

if __name__ == '__main__':
    view_database()
