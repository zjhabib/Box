from boxsdk import OAuth2, Client
import datetime as dt
import csv

auth = OAuth2(
	client_id='YOUR_CLIENT_ID',
	client_secret='YOUR_CLIENT_SECRET',
	access_token='YOUR_DEVELOPER_TOKEN',
)
client = Client(auth)
user = client.user().get()

#Set last month date
last_month = dt.datetime.today().replace(day=1) - dt.timedelta(1)

#Create Empty List
csv_dict = []

#Set up field names for csv
field_names = ['Event ID','Type', 'Item Name', 'Created By Name', 'Created By Login', 'Event Type', 'Created At']


print('Gathering data from last month…')

#Save Events to Dictionary 
events =client.events().get_admin_events(event_types=['DOWNLOAD','UPLOAD'],created_after=last_month)
for event in events['entries']:
	new_line = {'Event ID' : event.event_id, 'Type' : event.type, 'Item Name' : event.source['item_name'], 'Created By Name' : event.created_by.name, 'Created By Login' : event.created_by.login, 'Event Type' : event.event_type, 'Created At': event.created_at}
	csv_dict.append(new_line)
	
	
#Save dictionary to csv file
with open('Monthly_event_log.csv', 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=field_names)
	writer.writeheader()
	writer.writerows(csv_dict)
	