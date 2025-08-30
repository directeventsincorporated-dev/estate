from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# Approved users mapping: username -> password
APPROVED_USERS = {
    "admin": "password123",
    "jane": "securepass"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in APPROVED_USERS and APPROVED_USERS[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials or user not approved.'
    return render_template('login.html', error=error)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
