from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import random
import string
import qrcode
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# Модел за базата данни за съхраняване на линкове
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникален идентификатор за всеки запис
    original_url = db.Column(db.String(500), nullable=False)  # Оригиналният URL, който ще се скъсява
    short_code = db.Column(db.String(10), unique=True, nullable=False)  # Уникален код за скъсения линк

# Функция за генериране на случаен кратък код
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits  # Възможни символи за кода (букви и цифри)
    while True:
        short_code = ''.join(random.choices(characters, k=length))  # Генериране на случаен код с дължина 6 символа
        if not URL.query.filter_by(short_code=short_code).first():  # Проверка дали кодът вече не съществува
            return short_code

# Главен маршрут за началната страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('link')  # Получаване на оригиналния линк от формуляра
        custom_suffix = request.form.get('custom_suffix')  # Получаване на потребителски суфикс, ако е добавен
        generate_qr = 'generate_qr' in request.form  # Проверка дали чекбоксът за QR код е отметнат

        # Проверка дали е добавен персонализиран суфикс
        if custom_suffix:
            if URL.query.filter_by(short_code=custom_suffix).first():  # Ако суфиксът вече съществува
                flash('Custom suffix is already taken. Please choose another one.', 'danger')
                return redirect(url_for('index'))
            short_code = custom_suffix  # Използване на персонализирания суфикс като кратък код
        else:
            short_code = generate_short_code()  # Генериране на случаен кратък код, ако няма персонализиран

        # Записване на оригиналния линк и краткия код в базата данни
        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

        # Генериране на QR код, ако е поискано
        qr_code_path = None
        if generate_qr:
            full_short_url = request.host_url + short_code  # Пълен скъсен URL
            qr = qrcode.make(full_short_url)  # Създаване на QR код за скъсения линк
            qr_code_path = f'static/qr_codes/{short_code}.png'  # Път до файла с QR кода
            os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)  # Създаване на папката, ако не съществува
            qr.save(qr_code_path)  # Записване на QR кода като изображение

        # Пренасочване към страницата, която показва скъсения линк (и QR кода, ако е наличен)
        return redirect(url_for('shortened_link', short_code=short_code, qr=qr_code_path))

    return render_template('index.html')

# Маршрут за показване на скъсения линк и QR код (ако е генериран)
@app.route('/link/<short_code>')
def shortened_link(short_code):
    full_short_url = request.host_url + short_code  # Пълен URL за скъсения линк
    qr_code_path = request.args.get('qr')  # Път до QR кода, ако е генериран
    return render_template('shortened_link.html', full_short_url=full_short_url, qr_code_path=qr_code_path)

# Маршрут за пренасочване към оригиналния URL
@app.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()  # Намиране на оригиналния URL по кратък код
    return redirect(url.original_url)  # Пренасочване към оригиналния URL

# Инициализиране на базата данни
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)  # Стартиране на приложението с включен режим за отстраняване на грешки
