# Needle
![needle](needle.jpg)


## Prerequisites

Before running the script, ensure that you have the necessary dependencies installed. You can install them using the following command:

```bash
pip install -r requirement.txt
```

## Configuration

1. Configure `attendance_data_config.py` with the following content:

```python
# attendance_data_config.py
class AttendanceData:
    data = "15"  
    lat = "23.7968856"  # Customize with your latitude
    lng = "90.4219536"  # Customize with your longitude
```

2. Create a `.env` file in the project root directory with the following content:

```dotenv
LOGIN_URL=<your_login_url>
ATTENDANCE_URL=<your_attendance_url>
EMAIL=<your_email>
PASSWORD=<your_password>
```

Replace `<your_login_url>`, `<your_attendance_url>`, `<your_email>`, and `<your_password>` with your actual login URL, attendance URL, email, and password.

## Usage

Run the script using the following command:

```bash
python main.py
```

The script will execute the attendance job at 9:00 AM every day, excluding Fridays and Saturdays.
