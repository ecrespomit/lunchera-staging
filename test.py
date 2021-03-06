from flask import Flask, session, request, flash, redirect, url_for, jsonify
from flask import render_template
from order_process import OrderProcessor
import requests

app = Flask(__name__)
app.secret_key = 'testingSecretKey'

NAME = "Eric Crespo"
EMAIL = "ecrespo@mit.edu"
PHONE = "787-607-8914"
ADDRESS = "28-15 34th Street, Queens NY, 11103"

@app.route('/order/', methods=['POST'])
def incoming_order():
	DATA = {}
	op = OrderProcessor()
	
	#Get Payload
	payload = request.get_json()
	#Filter order items (non-null)
	order_items = op.get_order_items(payload)
	DATA['Order'] = order_items
	#Get Customer info
	customer_info = op.get_customer_info(payload)
	DATA['Customer'] = customer_info
	#Get Restaurant Name/ID/email
	restaurant = op.get_restaurant(payload)
	DATA['Restaurant'] = restaurant
	#Get Order ID (unique)
	confirmation_link = op.get_confirmation_link(payload)
	DATA['ID'] = confirmation_link
	#Send all info to Restaurant
	url = "http://requestb.in/19fvxns1"
	resp = requests.post(url, json=DATA)
	
	
	
	
	return resp.text

@app.route('/order-test/', methods=['POST'])
def order_test():
	payload = {}
	payload = request.get_json()
	return str(payload)

@app.route('/')
def hello_world():
	return 'Hello World! This is version 1.0'

@app.route('/user/<username>')
def show_user_profile(username):
	return "User %s" % username

@app.route('/demo/')
def demo():
    return render_template('template1.html')

@app.route('/index/')
def index():
	return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
	#After puting in the credentials
	if request.method == 'POST':
		if request.form['password'] == "testing123":
			return redirect(url_for('demo'))
			#return "%s, you have successfully logged in!" % session['username']
		else: 
			return "Sorry, wrong password or username"
	#Logging in
	return render_template('login.html')

@app.route('/personal_info/', methods=['GET', 'POST'])
def personal_info():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		phone = request.form['phone_number']
		address = request.form['address']
		url = "https://35hundred.typeform.com/to/cSWs4j?name="+name+"&email="+email+"&phone="+phone+"&address="+address
		return redirect(url)

	return render_template('personal_info.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')