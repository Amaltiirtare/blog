from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
# Для установки времени по умолчанию
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # Отключение мода, т.к. ошибка при запуске app
db = SQLAlchemy(app)


# nullable=False - нельзя установить пустое значение
# Text - для большого объема текста
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)            # ID - задается автоматически, используя primary-key
    title = db.Column(db.String(100), nullable=False)       # Название
    intro = db.Column(db.String(300), nullable=False)       # Вводная часть
    text = db.Column(db.Text, nullable=False)               # Текст сообщения
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Дата. Значение по умолчанию.

    # Из БД выдается объект и ее ID
    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create-article', methods=['POST', 'GET'])   # Указатель, какие используются методы на странице
def create_article():
    if request.method == "POST":                        # Импортируем, т.к. используем
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)


