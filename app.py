from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__) # Создание экземпляра Flask-приложения: __name__ - имя текущего модуля (для определения корневого пути)

app.secret_key = 'secret_key' # Установка секретного ключа для подписи сессионных cookies

# Функция для чтения пользователей из файла
def read_users():
    users = {}  # Создание пустого словаря для хранения пользователей
    try:
        with open('users.txt', 'r') as file: # Открытие файла в режиме чтения
            for line in file:
                username, password = line.strip().split(':') # Разделение строки по символу ':' и удаление пробелов
                users[username] = password # Добавление пользователя в словарь
    except FileNotFoundError:
        pass # Если файл не найден - пропускаем ошибку
    return users  # Возврат словаря пользователей

# Функция добавления нового пользователя
def add_user(username, password):
    with open('users.txt', 'a') as file:  # Открытие файла в режиме добавления (append)
        file.write(f"{username}:{password}\n") # Запись новой строки с данными пользователя

# Декоратор маршрута для главной страницы
@app.route('/')
def home():
    if 'username' in session: # Проверка наличия пользователя в сессии
        return redirect(url_for('welcome'))  # Перенаправление авторизованного пользователя на страницу приветствия
    return redirect(url_for('login'))  # Перенаправление неавторизованного пользователя на страницу входа

# Маршрут для страницы входа с обработкой GET и POST запросов
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # Если запрос POST (отправка формы)
        username = request.form['username']  # Получение данных из формы
        password = request.form['password']  # Получение данных из формы
        users = read_users()  # Чтение списка пользователей
        if username in users and users[username] == password:  # Проверка существования пользователя и совпадения пароля
            session['username'] = username  # Сохранение имени пользователя в сессии
            return redirect(url_for('welcome'))  # Перенаправление на страницу приветствия
        else:
            return render_template('login.html', error="Неверный логин или пароль")  # Возврат страницы входа с сообщением об ошибке
    return render_template('login.html')   # Если запрос GET, просто отображаем страницу входа


# Маршрут для страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': # Если запрос POST (отправка формы)
        username = request.form['username'] # Получение данных из формы
        password = request.form['password'] # Получение данных из формы
        confirm_password = request.form['confirm_password']  # Получение данных из формы
        users = read_users() # Чтение списка пользователей

        if password != confirm_password:  # Проверка совпадения паролей
            return render_template('register.html', error="Пароли не совпадают")
        if username in users:  # Проверка существования пользователя
            return render_template('register.html', error="Пользователь уже существует")

        add_user(username, password)  # Добавление нового пользователя
        session['username'] = username  # Сохранение имени пользователя в сессии
        return redirect(url_for('welcome'))  # Перенаправление на страницу приветствия
    return render_template('register.html') # Если запрос GET, просто отображаем страницу регистрации

# Маршрут для страницы приветствия
@app.route('/welcome')
def welcome():
    if 'username' not in session: # Проверка авторизации пользователя
        return redirect(url_for('login')) # Перенаправление неавторизованных пользователей
    return render_template('welcome.html', username=session['username']) # Отображение страницы приветствия с именем пользователя

# Маршрут для выхода из системы
@app.route('/logout')
def logout():
    session.pop('username', None) # Удаление имени пользователя из сессии
    return redirect(url_for('login'))  # Перенаправление на страницу входа

if __name__ == '__main__':
    app.run(debug=True)
