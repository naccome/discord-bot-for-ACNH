from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# https://docs.google.com/spreadsheets/d/{YOUR_SPEADSHEET_ID}/edit#gid=0
sheet_id = 'YOUR_SPREAD_SHEET_ID'
sheet_name = 'YOUR_SHEET_NAME'
range_ = sheet_name + '!A:B'

def updateSheet(stock_price):
	creds=None

	if os.path.exists('token.pickle'):
		with open('token.pickle','rb') as token:
			creds = pickle.load(token)

	# If there are no valid credentials available, let user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		
		# Save the credentials for next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	now = datetime.datetime.now()
	timestamp = '{0:%Y%m%d %p}'.format(now)

	values = [
		[timestamp, stock_price]
		]
	body = {
		'values': values
	}

	value_input_option = 'USER_ENTERED'
	insert_data_option = 'OVERWRITE'

	result = service.spreadsheets().values().append(spreadsheetId = sheet_id, range = range_, valueInputOption = value_input_option, body = body).execute()

	print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))

