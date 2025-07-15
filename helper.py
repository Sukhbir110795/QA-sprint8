import requests
import time

def is_url_reachable(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

def retrieve_phone_code():
    # Simulate retrieving an SMS verification code from logs
    # In a real system, this might fetch data from a test log or mock SMS API
    time.sleep(2)  # simulate wait for code
    return "1234"  # this should match the code expected by your test environment
