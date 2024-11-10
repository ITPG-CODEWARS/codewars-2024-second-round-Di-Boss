# URL Shortener

![Лого на URL Shortener](static/logo.png)

URL Shortener е приложение за скъсяване на линкове с възможност за генериране на QR кодове. То позволява на потребителите да въведат дълъг URL и да получат кратък линк, който да използват вместо него. Приложението също така дава опция за персонализиране на краткия линк и генериране на QR код за лесен достъп.

## Технологии

Приложението е разработено с използване на следните технологии:

- **Python** - основен програмен език
- **Flask** - микрофреймуърк за уеб приложения
- **SQLite** - база данни за съхранение на линковете и кратките кодове
- **SQLAlchemy** - ORM библиотека за работа с базата данни
- **QRCode** - библиотека за генериране на QR кодове
- **HTML/CSS** - фронтенд структура и стилизация

## Как да използвам приложението

1. **Клониране на репото**: Изтегли репото и го разархивирай или клонирай директно чрез командата:

   ```bash
   git clone https://github.com/ITPG-CODEWARS/codewars-2024-second-round-Di-Boss
   ```

2. **Инсталиране на зависимостите**: Увери се, че имаш Python и pip инсталирани. След това инсталирай необходимите библиотеки с:

   ```bash
   pip install Flask Flask-SQLAlchemy qrcode[pil]
   ```

3. **Стартиране на приложението**: Отиди в директорията на проекта и стартирай приложението със следната команда:

   ```bash
   python app.py
   ```

4. **Достъп до приложението**: Отвори браузъра и посети [http://127.0.0.1:5000](http://127.0.0.1:5000), за да видиш приложението в действие.

## Как да използвам функционалностите

1. **Скъсяване на линк**: В полето "Enter the Link" въведи URL, който искаш да скъсиш, и натисни бутона "Shorten". Ще се генерира кратък линк, който можеш да копираш и използваш.

2. **Добавяне на персонализиран суфикс**: Ако искаш краткият линк да съдържа специален текст (например за по-добра идентификация), въведи го в полето "Custom Suffix (optional)". Ако този суфикс е наличен, той ще бъде добавен към краткия линк.

3. **Генериране на QR код**: Ако искаш да създадеш QR код за скъсения линк, постави отметка на опцията "Generate QR Code" преди да натиснеш "Shorten". Когато линкът е генериран, ще видиш и QR кода на новата страница.

## Структура на проекта

- `app.py`: Главен файл на приложението, съдържа логиката на сървъра и маршрутите.
- `templates/`: Съдържа HTML файловете за изгледите (index.html, shortened_link.html).
- `static/`: Съдържа статични файлове като CSS, лога и генерирани QR кодове.
- `db.sqlite`: База данни SQLite за съхранение на линковете и късите кодове.

## База данни

Приложението използва SQLite база данни, наречена `db.sqlite`, която автоматично се създава при стартиране на приложението. В нея се съхраняват всички оригинални линкове и техните къси кодове.

## Бележки

- **QR кодове**: QR кодовете се запазват в директорията `static/qr_codes`.
- **Персонализирани суфикси**: Ако суфиксът, който въвеждаш, вече е използван, ще получиш съобщение за грешка и ще трябва да въведеш нов суфикс.

## Лиценз

Този проект е с отворен код и може да бъде използван за лични и образователни цели.
