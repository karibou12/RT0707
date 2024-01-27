from flask import Flask, jsonify, redirect, request, render_template, url_for,session, g
from werkzeug.security  import generate_password_hash
import requests
import jwt
import functools
import time

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'dashboardSecret'

urlApi = 'http://172.20.0.7:5000'


# verify token
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
    
    if user_id == 'admin':

        if user_id is None:
                g.user =None
        else:
            g.user = user_id
    else:
        g.user =None

# Add login decoration
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


#*****************    INDEX    *******************************

@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


#*****************USER****************************

#login route
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


@app.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('index'))


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


# Read all user's film
@app.route("/dashboard", methods=['GET'])
@login_required
def get_userinfo():
        url = f'{urlApi}/userinfo/{g.user}'
        response = requests.get(url)
        
        if response.status_code == 200:
        
            data = response.json()
            return render_template('dashboard.html', data = data)
            # return render_template('info.html', films=films['films'])
        else:
            return jsonify({'error': 'page not found'}), 404



if __name__ == '__main__':
    app.run(debug=True, port=5000)




