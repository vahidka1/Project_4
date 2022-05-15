from flask import Flask, render_template, redirect, url_for , request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import insta_scrap , winner_options
app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/projectm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    if current_user.is_authenticated:
        n =current_user.username
        s='hidden'
        s2=''
    else:
        n=''
        s=''
        s2='hidden'
    
    return render_template('index.html',name=n,show=s,show2=s2)

@app.route('/search', methods=["POST","GET"])
def search():
    if current_user.is_authenticated:
        n =current_user.username
        s='hidden'
        s2=''
    else:
        n=''
        s=''
        s2='hidden'
    
    url = request.form['url']

    
    result = insta_scrap.post(url)
    if current_user.is_authenticated:
        insta_scrap.scrapecomment(url)
        insta_scrap.jsontoexel()
        insta_scrap.scrapefollowers(url)
        insta_scrap.scrapelikes(url)
        
        return render_template('search.html',result=result,name=n , show=s ,show2=s2)
    else :
        return redirect(url_for('login'))

@app.route('/options', methods=['GET', 'POST'])
def options():
    if current_user.is_authenticated:
        n =current_user.username
        s='hidden'
        s2=''
    else:
        n=''
        s=''
        s2='hidden'
    if request.method == 'POST':
        checkedlist=request.form.getlist('checkboxs')
        winner_options.excel_creator(checkedlist)
        winner=winner_options.winner_chooser()
        return render_template('winner.html',winner=winner,name=n , show=s ,show2=s2)
        


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == 'adminpass':
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admindashboard'))

            elif user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return render_template('login.html', form=form ,error='wrong username or password')
        

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    user = User.query.filter_by(username=form.username.data).first()
    email= User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user or email :
            s1=''
            return render_template('signup.html', form=form ,error='Username or Email exist!')
        else:
            new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            s2='hidden'
            return redirect(url_for('dashboard'))

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        n =current_user.username
        s='hidden'
        s2=''
    else:
        n=''
        s=''
        s2='hidden'
    
    return render_template('dashboard.html', name=current_user.username , email=current_user.email , password=current_user.password ,show=s,show2=s2)
@app.route('/admindashboard')
@login_required
def admindashboard():
    result = User.query.all()
    if current_user.is_authenticated:
        n =current_user.username
        s='hidden'
        s2=''
    else:
        n=''
        s=''
        s2='hidden'
    if current_user.password == 'adminpass' :
        return render_template('admindashboard.html', name=current_user.username ,result=result,show=s,show2=s2)
    else:
        return '404 not found'
@app.route("/delete/<int:id>")
def delete(id):
    user_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect(url_for('admindashboard'))
    except:
        return "There was problem with deleting"

@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit(id):
    user_edit = User.query.get_or_404(id)
    if request.method == "POST":
        user_edit.username = request.form['user_name']
        user_edit.password = request.form['password']
        user_edit.email = request.form['email']
        try:
            db.session.commit()
            return redirect(url_for('admindashboard'))
        except:
            return "There was problem with editing"
    else:
        return render_template('edit.html',user_edit=user_edit )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
