from requests import request
from datetime import date, datetime, timedelta
from ics import Calendar, Event, Organizer, DisplayAlarm

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
    offset = 0
    e = Event()
    e.uid = event['uniqueid']
    e.name = event['activitydesc']
    start = datetime.strptime(event['start'], "%Y-%m-%dT%H:%M")
    if start < datetime(2023, 10, 29):
      offset = 1
    end = datetime.strptime(event['end'], "%Y-%m-%dT%H:%M")
    start = start - timedelta(hours=offset)
    end = end - timedelta(hours=offset)
    e.begin = start
    e.end = end
    e.location = event['locationdesc']
    if len(event['staffs']) > 0:
      lecturer = Organizer(email=event['staffs'][0]['Email'], common_name=event['staffs'][0]['FullName'])
      e.organizer = lecturer
    # e.alarms = [DisplayAlarm(trigger=timedelta(hours=-1))]
    cal.events.add(e)

# Write to ICS file
with open('uolcalendar.ics', 'w') as f:
    f.writelines(cal.serialize_iter())
    f.close()