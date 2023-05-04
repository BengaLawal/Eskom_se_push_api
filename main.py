import requests
import os
from datetime import datetime
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# check if test parameter in area_information() is commented

license_key = os.environ.get("LICENSE_KEY")
twilio_account_sid = os.environ.get("ACCOUNT_SID")
twilio_auth_token = os.environ.get("AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_NUMBER")
my_number = os.environ.get("MY_NUMBER")

today = datetime.today().strftime('%Y-%m-%d')

area_id = "capetown-8-muizenberg"  # Feel free to change id to area you want info on

header = {
    "token": license_key
}

def main():
    # print(get_area_id())  # print area id, name, region
    area_info = area_information()
    send_schedule(area_info)
    print(check_allowance())


def get_area_id():
    """Search for an area and look for its id.
    Counts as 5 calls towards quota"""
    area = "muizenberg"
    url = "https://developer.sepush.co.za/business/2.0/areas_search"
    parameters = {
        "text": area
    }
    response = requests.get(url=url, params=parameters, headers=header)
    response.raise_for_status()
    # data = response.json()
    # return data["areas"][0]["id"]
    return response.text

def area_information():
    """Returns area information based on the id shown in get_area_id().
    Counts as 1 call against your quota.
    Returns json"""
    url = "https://developer.sepush.co.za/business/2.0/area"
    parameters = {
        "id": f"{area_id}",  # id received from checking get_area_id()
        "test": "current"  # set to current or future -- only use when you're testing and don't need current data -- won't count as a call against your quota
    }
    response = requests.get(url=url, params=parameters, headers=header, verify=False)
    return response.json()

def check_allowance():
    """Check how much calls you can make.
    Does not count against your quota"""
    url = "https://developer.sepush.co.za/business/2.0/api_allowance"
    response = requests.get(url=url, headers=header)
    return response.text

def notification(message_):
    """Send notification to whatsapp"""
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(twilio_account_sid, twilio_auth_token, http_client=proxy_client)
    message = client.messages\
        .create(
            from_=f"whatsapp:+{twilio_number}",
            body=f"{message_}",
            to=f"whatsapp:+{my_number}"
    )
    # print(message.status)

def send_schedule(schedule):
    """Sends load shedding times for the day to whatsapp.
    Accept a list of loadshedding details.
    Returns nothing"""
    todays_loadshedding = []
    if len(schedule["events"]) == 0:
        notification("No loadshedding")
    else:
        for event in schedule["events"]:
            start_date = (event["start"].split("T"))[0]
            if str(today) == str(start_date):
                todays_loadshedding.append(event)
        for shed in todays_loadshedding:
            notification(
                f"🚨LOADSHEDDING🚨\nStart - {shed['start'].split('T')[1][:5]}\nEnd - {shed['end'].split('T')[1][:5]}")

if __name__ == '__main__':
    main()
