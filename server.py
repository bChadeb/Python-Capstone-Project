from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import User, Progress, connect_to_db
from forms import LoginForm, RegisterForm
from crud import create_user, update_progress

app = Flask(__name__)
app.secret_key = "very_very_secret"  


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        create_user(username, password)

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
   form = LoginForm()

   if form.validate_on_submit():
       username = form.username.data
       password = form.password.data

       user = User.query.filter_by(username=username).first()

       if user and user.password == password:
           session['user_id'] = user.id
           flash("Logged in successfully", 'success')
           return redirect(url_for('home'))
       else:
           flash("Invalid username or password", 'error')
           return redirect(url_for('login'))
   
   return render_template("login.html", form = form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully", 'success')
    return redirect(url_for('home'))

@app.route('/chapter1', methods=['GET', 'POST'])
def chapter1():
    if request.method == 'POST':
        pass

    user_id = session.get('user_id')
    progress = Progress.query.filter_by(user_id=user_id).all()
    collectible_statuses = {p.collectible_name: p.collected for p in progress}

    return render_template('chapter1.html', collectible_statuses=collectible_statuses)

@app.route('/update_progress', methods=['POST'])
def update_progress_route():
    collectible_name = request.form['collectible_name']
    collected = request.form.get('collected') == 'true' 
    user_id = session.get('user_id')

    print("Collectible Name:", collectible_name)
    print("Collected:", collected)


    if not user_id:
        return 'User ID not found in session', 403

    success = update_progress(user_id, collectible_name, collected)
    print(success)
    if success:
        session['collected_status'] = session.get('collected_status', {})
        session['collected_status'][collectible_name] = collected
        
    return redirect(url_for('chapter1'))

if __name__ == '__main__':
    with app.app_context():
        connect_to_db(app)
    app.run(debug=True) 