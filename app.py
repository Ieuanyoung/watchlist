from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import click

# from flask import url_for
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
										os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
	"""Initialize the database."""
	if drop:
		db.drop_all()
	db.create_all()
	click.echo('Initialized database.')

@app.route('/')
def index():
	user = User.query.first()  # 读取用户记录
	movies = Movie.query.all()  # 读取所有电影记录
	return render_template('index.html', user=user, movies=movies)


@app.route('/user/<name>')
def user_page(name):
	return 'User:{}'.format(name)

# @app.route('/test')
# def test_url_for():
# 	print(url_for('hello'))
# 	print(url_for('user_page', name = 'a'))
# 	print(url_for('test_url_for'))
# 	print(url_for('test_url_for', num = 2))
# 	return 'Test page'


@app.cli.command()
def forge():
	"""Generate fake data"""
	db.create_all()

	name = 'Ieuanyoung'
	movies = [
		{'title': 'My Neighbor Totoro', 'year': '1988'},
		{'title': 'Dead Poets Society', 'year': '1989'},
		{'title': 'A Perfect World', 'year': '1993'},
		{'title': 'Leon', 'year': '1994'},
		{'title': 'Mahjong', 'year': '1996'},
		{'title': 'Swallowtail Butterfly', 'year': '1996'},
		{'title': 'King of Comedy', 'year': '1999'},
		{'title': 'Devils on the Doorstep', 'year': '1999'},
		{'title': 'WALL-E', 'year': '2008'},
		{'title': 'The Pork of Music', 'year': '2012'},
	]

	user = User(name=name)
	db.session.add(user)
	for m in movies:
		movie = Movie(title=m['title'], year=m['year'])
		db.session.add(movie)

	db.session.commit()
	click.echo('Done')


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))


class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	year = db.Column(db.String(4))

