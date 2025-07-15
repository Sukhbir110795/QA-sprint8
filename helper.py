# helpers.py
import requests
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_url_reachable(url="https://cnt-59c08492-c002-4ce8-91fe-2d43434e2332.containerhub.tripleten-services.com/"):
    """
    Checks if the given URL is reachable.
    Replace with your actual app URL if different.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return True
    except requests.exceptions.RequestException as e:
        print(f"URL {url} is not reachable: {e}")
        return False

def retrieve_phone_code(driver):
    """
    Retrieves the phone confirmation code from the browser's performance logs.
    This method assumes the code is logged in the browser's console/network requests.
    You might need to adjust this based on how your specific application logs the code.
    """
    # Wait for the logs to be available
    WebDriverWait(driver, 10).until(
        lambda d: d.get_log('performance')
    )

    logs = driver.get_log('performance')
    for log in logs:
        # Look for a pattern that indicates the SMS code in the log message
        # This is a common pattern for how the code might appear in network logs
        match = re.search(r'\"text\":\"(\d{4})\"', log['message'])
        if match:
            return match.group(1)
    return None # Return None if code not found