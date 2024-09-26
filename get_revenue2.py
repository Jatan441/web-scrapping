from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from pymongo import MongoClient
import time
import random
import pyautogui
import action  # Assuming 'action' module is available for human_search and unpredictable_choice

# MongoDB connection
client = MongoClient("mongodb://firoz:firoz423*t@43.205.16.23:49153/")
db = client["warehouse"]
collection = db["googlemapscompanies"]

# ChromeDriver setup
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode for automation
chrome_service = Service("C:/Users/jchoudhary/Downloads/chromedriver-win64/chromedriver.exe")  # Update with the correct path

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Wait configuration
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

# Function to mimic human-like typing
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

# Function to mimic human-like mouse movements
def human_mouse_movements(x, y, dx, dy):
    pyautogui.moveTo(x, y)
    pyautogui.moveRel(dx, dy)

# Function to mimic human-like search
def get_human_search_text():
    google_search_strings = [
        # A list of search queries as before
    ]
    return google_search_strings

def human_search():
    try:
        time.sleep(5)
        driver.get('https://www.google.com/')
        search_bar = driver.find_element(By.TAG_NAME, 'textarea')
        human_typing(search_bar, action.unpredictable_choice(get_human_search_text()))
        actions.move_to_element(search_bar).perform()
        time.sleep(random.uniform(0.05, 20))
        search_bar.send_keys(Keys.ENTER)
        time.sleep(5)
        human_mouse_movements(10, 20, 40, 12)
        # Simulate clicking the first result
        first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
        first_result.click()
    except Exception as e:
        print(f"Google search failed: {e}")

def get_company_revenue(company_name):
    print(f"Searching revenue for: {company_name}")
    
    search_query = f"nyse:{company_name}"
    driver.get("https://www.google.com/")
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.submit()
    
    time.sleep(3)
    
    try:
        financials_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Financials')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", financials_tab)
        time.sleep(1)
        actions.move_to_element(financials_tab).click().perform()
        print("Clicked on Financials tab")
        
        time.sleep(3)
        revenue_element = wait.until(EC.presence_of_element_located((By.XPATH, "//th[contains(text(),'Revenue')]/following-sibling::td[1]")))
        revenue = revenue_element.text
        return revenue
    except Exception as e:
        print(f"Not able to find revenue for {company_name}")
        return None


try:
    while True:

        # Find the document without revenue field
        document = collection.find_one({
            "firmographic.revenue_range.revenue": {"$exists": False}
        })
        
        if not document:
            print("No more documents to process.")
            break

        company_name = document.get('name')
                
        if company_name:
            print(f"Fetching revenue for {company_name}...")

            # Set the revenue field to an empty string if it doesn't exist
            collection.update_one(
                {"_id": document['_id']},
                {"$set": {"firmographic.revenue_range.revenue": ""}}
            )

            # Fetch the company's revenue
            revenue = get_company_revenue(company_name)
            
            # Randomly call human search
            if action.unpredictable_choice([True, False]):
                human_search()  # Perform the human search simulation
            
            # If revenue is found, update the field with the actual revenue
            if revenue:
                collection.update_one(
                    {"_id": document['_id']}, 
                    {"$set": {"firmographic.revenue_range.revenue": revenue}}
                )
                print(f"Updated revenue for {company_name}: {revenue}")
            else:
                print(f"Revenue not found for {company_name}")
                
except Exception as e:
    print(f"Not able to find revenue: {e}")

# Close the Selenium driver after all tasks are done
driver.quit()
