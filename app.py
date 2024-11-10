from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import random
import string
import qrcode
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Локация на базата данни (SQLite файл)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Спира допълнителното проследяване за оптимизация
app.config['SECRET_KEY'] = 'your_secret_key'  # Тайна ключова дума за сигурност на сесиите

db = SQLAlchemy(app)

# Модел за базата данни, за да съхраняваме линковете и късите кодове
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникално ID за всяка връзка
    original_url = db.Column(db.String(500), nullable=False)  # Оригиналният линк, който скъсяваме
    short_code = db.Column(db.String(10), unique=True, nullable=False)  # Къс код за скъсения линк

# Функция за генериране на случаен кратък код
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits  # Всички възможни букви и цифри
    while True:
        short_code = ''.join(random.choices(characters, k=length))  # Генериране на случаен код
        if not URL.query.filter_by(short_code=short_code).first():  # Проверка дали кодът е уникален
            return short_code

# Главният маршрут за началната страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('link')  # Вземане на линка от потребителя
        custom_suffix = request.form.get('custom_suffix')  # Вземане на потребителски суфикс, ако има такъв
        generate_qr = 'generate_qr' in request.form  # Проверка дали е отметнато генериране на QR код

        # Проверка дали е предоставен персонализиран суфикс
        if custom_suffix:
            if URL.query.filter_by(short_code=custom_suffix).first():  # Проверка дали суфиксът вече се използва
                flash('Custom suffix is already taken. Please choose another one.', 'danger')
                return redirect(url_for('index'))
            short_code = custom_suffix  # Използва суфикса като къс код
        else:
            short_code = generate_short_code()  # Генериране на случаен код, ако няма суфикс

        # Запазване на оригиналния линк и къс код в базата данни
        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

        # Генериране на QR код, ако потребителят го е избрал
        qr_code_path = None
        if generate_qr:
            full_short_url = request.host_url + short_code  # Пълен линк с къс код
            qr = qrcode.make(full_short_url)  # Създаване на QR код с пълния линк
            # Използва относителен път в папката static
            qr_code_path = f'static/qr_codes/{short_code}.png'
            os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)  # Създава папката, ако я няма
            qr.save(qr_code_path)  # Запазване на QR кода в определеното място

            # Предаване само на пътя, относителен към `static`
            qr_code_path = f'qr_codes/{short_code}.png'

        # Пренасочване към страницата с новия линк (и QR код, ако има)
        return redirect(url_for('shortened_link', short_code=short_code, qr=qr_code_path))
    
    return render_template('index.html')

# Маршрут за показване на скъсения линк и QR кода (ако има)
@app.route('/link/<short_code>')
def shortened_link(short_code):
    full_short_url = request.host_url + short_code  # Пълен линк за късия код
    qr_code_path = request.args.get('qr')  # Път до QR кода, ако има
    return render_template('shortened_link.html', full_short_url=full_short_url, qr_code_path=qr_code_path)

# Маршрут за пренасочване към оригиналния линк
@app.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()  # Намира оригиналния линк по къс кода
    return redirect(url.original_url)  # Пренасочва към оригиналния линк

# Инициализира базата данни
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)  # Стартира приложението в debug режим

