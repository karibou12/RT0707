from flask import Flask, jsonify, redirect, request, render_template, url_for,session, g
from werkzeug.security  import generate_password_hash
import requests
import jwt
import functools


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'your_secret_key'

urlApi = 'http://172.20.0.5:5000'


# Token check
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Le token a expiré
    except jwt.InvalidTokenError:
        return None  # Le token est invalide


# Add g.user to session
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
            g.user =None
    else:
        g.user = user_id

# Add a login required decoration
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


#*****************    INDEX    *******************************
#default route
@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


#*****************USER****************************

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        url = f'{urlApi}/login'
        username = request.form['username']
        password = request.form['password']
        data = {'username': username, 'password': password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data,headers=headers)

        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            token_id = data.get('token_id')

            if token:
                decoded_token = verify_token(token)
                if decoded_token:
                    session.clear()
                    session['user_id'] = decoded_token['user_id']
                    return redirect(url_for('get_userinfo'))

        elif response.status_code == 401:
            return render_template('login.html', message='Mot de passe incorrect')
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html')

#logout route
@app.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('index'))

#Create user
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            return render_template('register.html', message='les password ne correpondent pas')

        else:
            data = {'username': username, 'email': email, 'password': password}
            url = f'{urlApi}/adduser'
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data,headers=headers)
            
            if response.status_code == 201:
                return redirect(url_for('login'))
            elif response.status_code == 500:
                return render_template('register.html',message= 'user déja creé'),500
            else:
                return jsonify({'error': 'page not found'}), 404
        
    else:
        return render_template('register.html')

#read a specific user
@app.route('/user/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    url = f'{urlApi}/user/{user_id}'
    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()
        return render_template('user.html', user_id=user)
    else:
        return jsonify({'error': 'page not found'}), 404

#add ticket
@app.route('/addBillet', methods=['GET', 'POST'])
@login_required
def create_Billet():
    if request.method == 'POST':
        NbBunit = request.form['NbBunit']
        NbBjour = request.form['NbBjour']
        
        data = {'username': g.user, 'NbBunit': NbBunit, 'NbBjour': NbBjour}
        url = f'{urlApi}/addBillet'
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data,headers=headers)

        if response.status_code == 201:
            return redirect(url_for('get_userinfo', message='Billet unitaire acheter'))
            # return render_template('info.html', message='Billet unitaire acheter'),201
        elif response.status_code == 500:
            return render_template('addfilm.html', message='Achat reffusé'),500
        else:
            return jsonify({'error': 'page not found'}), 404
    else:
        return render_template('info.html')


# Read user account
@app.route("/myaccount", methods=['GET'])
@login_required
def get_userinfo():
    url = f'{urlApi}/userinfo/{g.user}'
    response = requests.get(url)
    
    if response.status_code == 200:
       
        data = response.json()
        return render_template('info.html', info = data)
     
    else:
        return jsonify({'error': 'page not found'}), 404



if __name__ == '__main__':
    app.run(debug=True, port=5000)




