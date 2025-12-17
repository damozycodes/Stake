import os
import time
import getpass
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from playsound3 import playsound


# profile_path = f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/{profile}" # path for windows users to have a consistent profile
def create_user_data_dir():
    # Get the current user name and build a chrome profile which will be used consistently
    user = getpass.getuser()
    profile = "stake"
    profile_path = f"/Users/{user}/Library/Application Support/Google/Chrome/{profile}"  # path for macOS users to have a consistent profile
    print("Opened stake.com with user profile:", profile_path)
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
    return profile_path

# Creating an instance of Chrome with default options
# def get_default_chrome_options():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument(f"--user-data-dir={create_user_data_dir()}")
#     options.add_argument("--profile-directory=Default")
#     options.add_argument("--disable-popup-blocking")
#     options.add_argument("--start-maximized")
#     # Initialize the Chrome driver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
#     return driver


# Function to set up Chrome options
def get_default_chrome_options():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument(f"--user-data-dir={create_user_data_dir()}")  # Specify user data directory
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")
    return options


# Function to check if the user is logged in or if Login/Register buttons are present
def check_login_register_buttons(driver):
    try:
        # Check if a specific element is visible that indicates the user is logged in
        # For example, checking if a logout button or user profile button exists
        user_profile_button = driver.find_elements(By.CSS_SELECTOR, '[data-testid="user-dropdown-toggle"]')  # Example selector for logged-in state
        
        if user_profile_button:  # If the list is not empty, the user is logged in
            print("User is already logged in.")
            input("Press Enter to continue...")  # Wait for user to press Enter
            print("Continuing with the process...")

        else:
            # Check for Login/Register buttons if the user is not logged in
            login_button = driver.find_elements(By.CSS_SELECTOR, '[data-testid="login-link"]')
            if login_button:  # If the list is not empty, login button is present
                print("Login/Register buttons detected. Please log in or sign up.")
                input("Press Enter after signing up/logging in to continue...")  # Wait for user to press Enter
                print("Continuing with the process...")

    except Exception as e:
        print(f"An error occurred: {e}")
 
def is_result_red(driver):
    try:
        result_el = driver.find_element(By.CSS_SELECTOR, ".content .result")
        color = result_el.value_of_css_property("color")
        print("Computed color:", color)

        # Handles rgba(...) and rgb(...)
        values = color.replace("rgba(", "").replace("rgb(", "").replace(")", "").split(",")
        r, g, b = map(int, values[:3])

        return r > 200 and g < 100 and b < 100

    except Exception as e:
        print("Failed to read result color:", e)
        return False

# Function that will be called after login/signup or directly if buttons are not present
def click_button_function(driver, max_losses):
    loss_counter = 0

    while True:
        try:
            bet_button = driver.find_elements(By.CSS_SELECTOR, '[data-testid="bet-button"]')

            if not bet_button:
                print("Bet button not found, retrying...")
                time.sleep(1)
                continue

            # Click bet
            bet_button[0].click()
            print("Bet button clicked.")

            # Give UI time to update result
            time.sleep(1.5)

            # Check result color
            if is_result_red(driver):
                loss_counter += 1
                print(f"❌ Loss detected (RED). Loss count: {loss_counter}")
            else:
                print("✅ Win detected (NOT RED). Resetting loss counter.")
                loss_counter = 0

            # Example stop condition
            if loss_counter >= max_losses:
                print("🚨 Max losses reached. Stopping.")
                playsound("Annoying___Super_Loud!__Alarm_Sound_Effect_Ringtone___Alert_Tone_(128k).m4a")  # Play alert sound
                return

            time.sleep(1)

        except Exception as e:
            print("Error in click loop:", e)
            time.sleep(1)


if __name__ == "__main__":
    driver = None
    try:
        max_loss = int(input("Enter the maximum number of allowed losses before stopping: "))

        options = get_default_chrome_options()
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://stake.com/casino/games/limbo")
        driver.implicitly_wait(10)

        check_login_register_buttons(driver)

        while True:
            click_button_function(driver, max_loss)

            condition = input("\nDo you want to start another betting session? (yes/no): ").strip().lower()
            while condition not in ("yes", "no"):
                condition = input("Please enter 'yes' or 'no': ").strip().lower()

            if condition == "no":
                print("Exiting the bot...")
                break

        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()