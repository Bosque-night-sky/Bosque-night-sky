from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
import sqlite3, os, secrets
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, 'forum.db')
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'change-this-password')
ADMIN_HASH = generate_password_hash(ADMIN_PASSWORD)

CATEGORIES = [
    'Skyglow / Night-Sky Brightness',
    'Glare / Light Trespass',
    'Roadway Visibility / Safety Concern',
    'Wildlife / Livestock Concern',
    'Home / Property Impact',
    'Lhoist Clifton Plant Observation',
    'Photos / Measurements / Evidence',
    'Public Records / Permits',
    'Government Response / Public Meeting',
    'Other Light-Pollution Concern',
]

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS posts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      category TEXT NOT NULL,
      area TEXT,
      observed_at TEXT,
      body TEXT NOT NULL,
      evidence TEXT,
      status TEXT NOT NULL DEFAULT 'pending',
      created_at TEXT NOT NULL
    );
    ''')
    # Safe migration from the original starter database, if present.
    columns = {row['name'] for row in conn.execute('PRAGMA table_info(posts)')}
    if 'area' not in columns:
        conn.execute('ALTER TABLE posts ADD COLUMN area TEXT')
    if 'observed_at' not in columns:
        conn.execute('ALTER TABLE posts ADD COLUMN observed_at TEXT')
    conn.commit(); conn.close()

@app.before_request
def ensure_db():
    init_db()

@app.context_processor
def inject_globals():
    return {'categories': CATEGORIES}

@app.get('/')
def index():
    conn = db()
    posts = conn.execute("SELECT * FROM posts WHERE status='published' ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.get('/about')
def about():
    return render_template('about.html')

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        title = request.form.get('title','').strip()[:160]
        category = request.form.get('category','Other Light-Pollution Concern').strip()[:100]
        area = request.form.get('area','').strip()[:160]
        observed_at = request.form.get('observed_at','').strip()[:80]
        body = request.form.get('body','').strip()[:10000]
        evidence = request.form.get('evidence','').strip()[:4000]
        consent = request.form.get('consent')
        if category not in CATEGORIES:
            category = 'Other Light-Pollution Concern'
        if not title or not body or consent != 'yes':
            flash('Please complete the required fields and confirm the posting rules.')
            return render_template('submit.html')
        conn = db()
        conn.execute('''INSERT INTO posts(title, category, area, observed_at, body, evidence, status, created_at)
                        VALUES(?,?,?,?,?,?,?,?)''',
                     (title, category, area, observed_at, body, evidence, 'pending',
                      datetime.now(timezone.utc).isoformat()))
        conn.commit(); conn.close()
        return render_template('thanks.html')
    return render_template('submit.html')

@app.get('/post/<int:post_id>')
def post(post_id):
    conn = db()
    p = conn.execute("SELECT * FROM posts WHERE id=? AND status='published'", (post_id,)).fetchone()
    conn.close()
    if not p: abort(404)
    return render_template('post.html', post=p)

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if check_password_hash(ADMIN_HASH, request.form.get('password','')):
            session['admin'] = True
            return redirect(url_for('admin'))
        flash('Incorrect password.')
    return render_template('login.html')

@app.get('/admin/logout')
def admin_logout():
    session.clear(); return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = db(); posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall(); conn.close()
    return render_template('admin.html', posts=posts)

@app.post('/admin/post/<int:post_id>/<action>')
def admin_action(post_id, action):
    if not session.get('admin'): abort(403)
    if action not in {'publish','reject','delete'}: abort(400)
    conn = db()
    if action == 'delete': conn.execute('DELETE FROM posts WHERE id=?', (post_id,))
    else: conn.execute('UPDATE posts SET status=? WHERE id=?', ('published' if action=='publish' else 'rejected', post_id))
    conn.commit(); conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=False)
