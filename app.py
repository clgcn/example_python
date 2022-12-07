from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from azure.identity import DefaultAzureCredential
import mysql.connector
import os
app = Flask(__name__)


@app.route('/')
def index():
    credential = DefaultAzureCredential(managed_identity_client_id='6b256fd2-99db-4872-9d11-7c1a03465fa0') # user-assigned identity
    token = credential.get_token("https://ossrdbms-aad.database.windows.net")
    if 'IDENTITY_ENDPOINT' in os.environ:
        mysqlUser = 'myuser@example-sq.mysql.database.azure.com'
    else:
        mysqlUser = '<aad-user-name>@<server-name>'

    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    config = {
    'host': 'example-sq.mysql.database.azure.com',
    'database': 'mysql',
    'user': mysqlUser,
    'password': token.token
    }
    conn = mysql.connector.connect(**config)
    print('Request for index page received'+conn)
    return render_template('index.html',conn)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))





if __name__ == '__main__':
   app.run()