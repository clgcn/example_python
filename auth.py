from azure.identity import DefaultAzureCredential
import mysql.connector
import os

# Uncomment one of the two lines depending on the identity type
#credential = DefaultAzureCredential() # system-assigned identity
credential = DefaultAzureCredential(managed_identity_client_id='6b256fd2-99db-4872-9d11-7c1a03465fa0') # user-assigned identity

# Get token for Azure Database for MySQL
token = credential.get_token("https://ossrdbms-aad.database.windows.net")

# Set MySQL user depending on the environment
if 'IDENTITY_ENDPOINT' in os.environ:
    mysqlUser = 'myuser@example-sq.mysql.database.azure.com'
else:
    mysqlUser = '<aad-user-name>@<server-name>'

# Connect with the token
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
config = {
  'host': 'example-sq.mysql.database.azure.com',
  'database': 'mysql',
  'user': mysqlUser,
  'password': token.token
}
conn = mysql.connector.connect(**config)
print("Connection established")