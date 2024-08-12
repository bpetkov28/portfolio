from flask import Flask, render_template, request, redirect
from flask.helpers import send_from_directory
import csv


app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_db_file(data):
    with open('database.txt') as database_file:
        email = data['email']
        subject = data['subject']
        message = data['message']
        database_file.write(f'\n {email},{subject},{message}')


def write_to_db_csv(data):
    with open(
            'database.csv',
            'a',
    ) as database_csv:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database_csv,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_db_csv(data)
            return redirect('/thankyou.html')
        except:
            return "Didn't save to databse"
    else:
        return "Something went wrong"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
