from flask import Flask, render_template, redirect, session ,flash, request
from mysqlconnection import MySQLConnector
import time
import re

app = Flask(__name__)
app.secret_key = "secretkey"
mysql = MySQLConnector(app, 'emailsdb')

@app.route('/')
def index():

    return render_template('index.html') 
@app.route('/process', methods=['post'])
def create():
    email = request.form['emailaddress']
    data = { 'emailaddress': request.form['email'] }
    query = "INSERT INTO emails (emailsaddress) VALUES (:emailaddress)"
    check = "SELECT * FROM emails"
    my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    
    for i in (mysql.query_db(check)):
        if i['emailaddress'] == email:
            flash("email already in database")
            return redirect('/')
    if not my_re.match(email):
        flash("bad email")
    else:
        print "good email"
        mysql.query_db(query, data)
        return redirect('/success')
    return redirect('/')

@app.route('/success', methods=['post'])
def success():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)

    return render_template("success.html", all_emails = emails)
    # query = "INSERT INTO emails (emailaddress) VALUES (:emailaddress)"

    # data = {
    #          'emailaddress': request.form['emailaddress'],
    #        }    
    # emails = request.form['emails']
    # if emails == 'emails' :
    #     flash("email cannot be empty")
    #     return redirect('/')
    # else:
    #     query = "SELECT * FROM emails WHERE id = :specific_id"
    #     data = {'specific_id': emails_id}
    #     emails = mysql.query_db(query, data)
    #     return render_template('Success.html')                    
    # emails = mysql.query_db(query)                           
    # return render_template('index.html', all_emails=emails) 


# @app.route('/success')
# def create():
#     emails = request.form['emails']
#     if len(email) < 1 :
#         flash("email cannot be empty")
#         return redirect('/')
#     else:
#         query = "SELECT * FROM emails WHERE id = :specific_id"
#         data = {'specific_id': emails_id}
#         emails = mysql.query_db(query, data)
#         return render_template('Success.html')

# @app.route('/emails/<emails_id>')
# def show(emails_id):

#     # query = "SELECT * FROM emails WHERE id = :specific_id"

#     # data = {'specific_id': emails_id}
  
#     # emails = mysql.query_db(query, data)

#     return render_template('index.html', one_email=emails[0])
app.run(debug=True)