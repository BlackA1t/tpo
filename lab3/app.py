from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Тестовые пользователи (в реальном приложении используйте базу данных)
USERS = {
    'admin': 'admin123',
    'testuser': 'Test@2024',
    'demo': 'demo_password'
}

def login_required(f):
    """Декоратор для защиты маршрутов"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Пожалуйста, войдите в систему', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Валидация
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('login.html')
        
        # Проверка credentials
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash(f'Добро пожаловать, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Защищенная страница после входа"""
    username = session.get('username')
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    """Выход из системы"""
    username = session.get('username', 'Пользователь')
    session.pop('username', None)
    flash(f'До свидания, {username}!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
