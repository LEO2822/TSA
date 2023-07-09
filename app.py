
from flask import Flask , render_template , session , request , redirect
from werkzeug.utils import append_slash_redirect
from get_tweet import scrape
from csv_to_db import *
import os
from delete import del_

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/analyze' , methods = ['GET', 'POST'])
def analyze():
    
    if request.method == 'POST':
        words = request.form['words']
        date_since = request.form['date_since']
        numtweet = 10
        scrape(words,date_since,numtweet)
        os.system('python csv_to_db.py')
        os.system('python tsa_positive.py')
        
        
    return render_template('analyze.html')


@app.route('/search' , methods = ['GET', 'POST'])
def search():
    
    if request.method == 'POST':
        del_()
        words = request.form['words']
        date_since = request.form['date_since']
        numtweet = 10
        scrape(words,date_since,numtweet)
        os.system('python csv_to_db.py')
        
        return render_template('search.html')
    
    elif request.method == "GET":
        connection = sqlite3.connect("table_name.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tweets")
        rows = cursor.fetchall()
        return render_template("search.html",rows = rows)
    
    return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
    
