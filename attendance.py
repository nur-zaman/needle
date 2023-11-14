import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from attendance_data_config import AttendanceData

def get_csrf_token(initial_response):    
    soup = BeautifulSoup(initial_response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '_token'})['value']
    return csrf_token

def perform_login(login_url, csrf_token, email, password,initial_response_cookies):
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
        "cookie": "; ".join([f"{key}={value}" for key, value in initial_response_cookies.items()]),
        "x-requested-with": "XMLHttpRequest",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    # Perform login
    response = requests.post(login_url, data=login_data, headers=login_headers)
    return response

def submit_attendance(attendance_url, csrf_token, session_data):
    # Make the attendance request

    attendance_data = {
        
        "data": AttendanceData.data,
        "lat": AttendanceData.lat,
        "lng": AttendanceData.lng
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
        "x-csrf-token": csrf_token,
        "x-requested-with": "XMLHttpRequest",
        "cookie": "; ".join([f"{key}={value}" for key, value in session_data.items()]),
        "Referer": f"{attendance_url}",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    # Submit attendance
    attendance_response = requests.post(attendance_url, data=attendance_data, headers=headers)
    return attendance_response

def job():
    load_dotenv()

    login_url = os.getenv("LOGIN_URL")
    attendance_url = os.getenv("ATTENDANCE_URL")
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    initial_response = requests.get(login_url)

    csrf_token = get_csrf_token(initial_response)

    response = perform_login(login_url, csrf_token, email, password,initial_response_cookies=initial_response.cookies.get_dict())

    if "login" in response.url:
        print("Login failed. Please check your credentials.")
    else:
        session_data = response.cookies.get_dict()
        attendance_response = submit_attendance(attendance_url, csrf_token, session_data)

        if attendance_response.status_code == 200:
            print("Attendance submitted successfully.")
        else:
            print("Attendance submission failed.")

if __name__ == "__main__":
    job()
