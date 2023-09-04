from requests import request
from datetime import date
from ics import Calendar, Event, Organizer

start = date(date.today().year, 1, 1).strftime("%Y-%m-%dT%H:%M:%S")
end = date(date.today().year+10, 12, 31).strftime("%Y-%m-%dT%H:%M:%S")

url = f"https://timetables.liverpool.ac.uk/services/get-events?start={start}&end={end}"

# PASTE Set-Cookie TOKEN HERE (e.g., 'uol_ttweb_auth=nRD7uaQMD...')
token = ''

if not token:
    raise Exception("Auth token not provided. See README.")

payload = {}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Cookie': token
}

# Make http request
response = request("GET", url, headers=headers, data=payload)
events = response.json()

cal = Calendar()

# Create events
for event in events:
    e = Event()
    e.uid = event['uniqueid']
    e.name = event['activitydesc']
    e.begin = event['start']
    e.end = event['end']
    e.location = event['locationdesc']
    if len(event['staffs']) > 0:
      lecturer = Organizer(email=event['staffs'][0]['Email'], common_name=event['staffs'][0]['FullName'])
      e.organizer = lecturer
    cal.events.add(e)

# Write to ICS file
with open('uolcalendar.ics', 'w') as f:
    f.writelines(cal.serialize_iter())
    f.close()