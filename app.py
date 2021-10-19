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


# Отображение постов
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    # query - метод, позволяет обратиться через опред. модель к БД
    # desc - функция сортировки в порядке убывания
    return render_template("posts.html", articles=articles)


# Детали
@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)


# Удаление статьи
@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)              # То же, что и get, только с вызовом ошибки 404

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


# Редактирование (обновление) статьи
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)


# Добавление постов
@app.route('/create-article', methods=['POST', 'GET'])   # Указатель, какие используются методы на странице
def create_article():
    if request.method == "POST":                         # Импортируем, т.к. используем
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")

if __name__ == "__main__":
    app.run(debug=True)


