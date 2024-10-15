# Import the required modules from selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# Create a new Firefox webdriver instance
driver = webdriver.Firefox()

# Open the specified URL
driver.get("https://www.zoominfo.com/c/infosys-ltd/58804259")

# Implicitly wait for the DOM to load
driver.implicitly_wait(10)

try:
    # Initialize ActionChains for low-level interactions
    action = ActionChains(driver)

    # Focus on the button with the Tab button
    action.send_keys(Keys.ENTER)
    action.pause(5)
    action.send_keys(Keys.TAB)
    action.pause(5)

    # Press and hold the Enter key to simulate "Press & Hold"
    action.key_down(Keys.ENTER)
    action.pause(10)

    # Release the Enter key after pressing it for 10 seconds
    action.key_up(Keys.ENTER)
    
    # Execute the Action Chain
    action.perform()

    # Wait for 10 seconds to simulate the "hold" action
    time.sleep(10)

except Exception as error:
    print(f"An {error} occurred and PRESS & HOLD button not found")

# Continue scraping...

# Quit the browser and release its resources
driver.quit()
