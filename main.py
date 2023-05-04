import requests
import os
from datetime import datetime, timedelta

licence_key = os.environ.get("LICENSE_KEY")

today = datetime.today().strftime('%Y-%m-%d')

tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

header = {
    "token": licence_key
}

# Feel free to change id to area you want info on
area_id = "capetown-8-muizenberg"

def main():
    # print(get_area_id())  # print area id, name, region

    area_info = area_information()

    if len(area_info["events"]) == 0:
        print("No load-shedding")
    else:
        for event in area_info["events"]:
            stage = event["note"]
            start_date = (event["start"].split("T"))[0]
            start_time = event["start"].split("T")[1][:5]
            end_time = event["end"].split("T")[1][:5]

            if str(today) == str(start_date):
                print("Today")
                print(f"{stage}\n{start_date}\nStart {start_time}\nEnd {end_time}")
                print("-----------")
            elif str(start_date) == str(tomorrow):
                print("Tomorrow")
                print(f"{stage}\n{start_date}\nStart {start_time}\nEnd {end_time}")
                print("-----------")

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
    data = response.json()
    return response.text
    # return data["areas"][0]["id"]

def check_allowance():
    """Check how much calls you can make.
    Does not count against your quota"""
    url = "https://developer.sepush.co.za/business/2.0/api_allowance"
    response = requests.get(url=url, headers=header)
    return response.text

def area_information():
    """Returns area information based on the id shown in get_area_id().
    Counts as 1 call against your quota"""
    url = "https://developer.sepush.co.za/business/2.0/area"
    parameters = {
        "id": f"{area_id}",  # id received from checking get_area_id()
        "test": "current"  # set to current or future -- only use when you're testing and don't need current data -- won't count as a call against your quota
    }
    response = requests.get(url=url, params=parameters, headers=header)
    return response.json()

if __name__ == '__main__':
    main()
