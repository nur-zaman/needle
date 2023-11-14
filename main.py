import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup




# Load environment variables from .env file
load_dotenv()

login_url = os.getenv("LOGIN_URL")
attendance_url = os.getenv("ATTENDANCE_URL")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Fetch the login page to get the initial _token
initial_response = requests.get(login_url)
soup = BeautifulSoup(initial_response.text, 'html.parser')
csrf_token = soup.find('input', {'name': '_token'})['value']



# Login data
login_data = {
    "_token": csrf_token,
    "email": email,
    "password": password,
}
login_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrf-token": csrf_token,  
    "cookie": "; ".join([f"{key}={value}" for key, value in initial_response.cookies.get_dict().items()]),
    "x-requested-with": "XMLHttpRequest",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}

# Perform login
response = requests.post(login_url, data=login_data,headers=login_headers)
response.text

session_data = response.cookies.get_dict()




if "login" in response.url:
    print("Login failed. Please check your credentials.")
else:
    # Make the attendance request
    attendance_data = {
        "data": "15",
        "lat": "23.7968856",
        "lng": "90.4219536",
    }

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-csrf-token": csrf_token,  # Use the csrf_token obtained during login
        "x-requested-with": "XMLHttpRequest",
        "cookie": "; ".join([f"{key}={value}" for key, value in session_data.items()]),
        "Referer": f"{attendance_url}",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    attendance_response = requests.post(attendance_url, data=attendance_data, headers=headers)

    if attendance_response.status_code == 200:
        print("Attendance submitted successfully.")
    else:
        print("Attendance submission failed.")


