import time
import requests
from selenium.webdriver.remote.webdriver import WebDriver

# Replace this with your container URL if needed
APP_URL = "https://cnt-159fc465-580d-4de5-9a1a-146a4fa61bf1.containerhub.tripleten-services.com/"

def is_url_reachable(url: str = APP_URL) -> bool:
    """
    Checks if the given URL is reachable.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def retrieve_phone_code(driver: WebDriver) -> str:
    """
    Extracts the SMS code sent to the phone from Chrome performance logs.
    This assumes logging was enabled via DesiredCapabilities in setup_class.
    """
    logs = driver.get_log("performance")
    for entry in logs:
        try:
            message = entry["message"]
            if "SMS code" in message or "code" in message:
                # Parse the log entry and extract a 4-digit code
                import re
                match = re.search(r"\b(\d{4})\b", message)
                if match:
                    return match.group(1)
        except Exception:
            continue

    # Fallback if not found immediately
    time.sleep(2)
    return retrieve_phone_code(driver)