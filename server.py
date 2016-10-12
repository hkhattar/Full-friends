from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key='supersecretkey'
mysql = MySQLConnector(app,'fullfriendsdb')

@app.route('/')
def index():
	query = "SELECT * FROM users"
	users = mysql.query_db(query)
	return render_template("index.html",all_users = users)

@app.route('/update/<id>/edit')
def update(id):
	query= "SELECT * FROM users WHERE id = :specific_id"
	data={'specific_id':id}
	users=mysql.query_db(query,data)
	return render_template('update.html', all_users = users)




@app.route('/delete/<id>/confirm')
def delete(id):
	query= "SELECT * FROM users WHERE id = :specific_id"
	data={'specific_id':id}
	users=mysql.query_db(query,data)
	return render_template('delete.html', all_users = users)

@app.route('/friends', methods=['POST'])
def friends():
	query = "INSERT INTO users (email, name) VALUES(:email,:name)"
	data = {
			'email' : request.form['email'],
			'name' : request.form['name']
			}
	mysql.query_db(query,data)
	return redirect('/')

@app.route('/friends/<id>', methods=['POST'])
def success(id):
	query = "UPDATE users SET email = :email, name = :name WHERE id = :id"
	data = {
			'email' : request.form['email'],
			'name' : request.form['name'],
			'id': id
			}
	mysql.query_db(query,data)
	return redirect('/')

@app.route('/friends/<id>/delete', methods=['POST'])
def friends_delete(id):
	query = "DELETE FROM users WHERE id= :id"
	data = {'id': id}
	mysql.query_db(query,data)
	return redirect('/')







app.run(debug=True)