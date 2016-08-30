from flask import Flask, render_template, request, redirect, url_for, Markup
import string, random, datetime, markdown
from mdx_bleach.extension import BleachExtension, ALLOWED_TAGS
from flask_mongoengine import MongoEngine


app = Flask(__name__)


app.config['MONGODB_SETTINGS'] = {'DB': "txtplz"}
app.config['SECRET_KEY'] = 'DebugSecret'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=3600)

db = MongoEngine(app)

app.jinja_env.autoescape = True

bleach = BleachExtension(tags=ALLOWED_TAGS)
md = markdown.Markdown(extensions=[bleach, 'markdown.extensions.nl2br'])


### Models


class Txt(db.Document):
	timestamp = db.DateTimeField(default=datetime.datetime.now())
	title = db.StringField()
	content = db.StringField(required=True)
	url = db.StringField(required=True, unique=True)
	meta = {'allow_inheritance': True}


### Aux

def url_generator(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


### Views

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/md')
def _md():
	return render_template('md.html')


@app.route('/save', methods=['POST'])
def save():
	title = request.form['title']
	content = md.convert(request.form['text'])
	url = url_generator()
	txt = Txt(title=title, content=content, url=url)
	try:
		txt.save()
	except:
		txt.url = url_generator()
		txt.save()

	return redirect(url)


@app.route('/<url>')
def _url(url):
	try:
		content = Txt.objects.get(url=url)
	except:
		return 'error'
	return render_template('content.html', title=content.title, content=content.content)


if __name__ == '__main__':
	app.run(debug=True)
