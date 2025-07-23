import time
from selenium.webdriver.remote.webdriver import WebDriver
def is_url_reachable(url) -> bool:
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