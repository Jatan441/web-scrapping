import random
import pyautogui
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import action
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# MongoDB connection setup
try:
    client = MongoClient('mongodb://firoz:firoz423*t@43.205.16.23:49153/')
    db = client['warehouse']  # Replace with your database name
    company_collection = db['googlemapscompanies']  # Replace with your collection name
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Firefox WebDriver setup
try:
    firefox_options = Options()
    # firefox_options.add_argument("--headless")  # Run Firefox in headless mode
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
except Exception as e:
    print(f"Error setting up Firefox WebDriver: {e}")

# Wait configuration
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def unpredictable_choice(arr):
    return random.choice(arr)

# Function to mimic human-like typing
def human_typing(element, text):
    try:
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
    except Exception as e:
        print(f"Error during human typing: {e}")

# Function to mimic human-like mouse movements
def human_mouse_movements(x, y, dx, dy):
    try:
        pyautogui.moveTo(x, y)
        pyautogui.moveRel(dx, dy)
    except Exception as e:
        print(f"Error during human-like mouse movements: {e}")

# Function to mimic human-like search
def get_human_search_text():
    google_search_strings = [
        # General Information
        "current weather",
        "latest news",
        "current time",
        "what's the date today",
        "events this weekend",

        # Health and Fitness
        "causes of headache",
        "home workout routines",
        "healthy meal plans",
        "side effects of common medicines",
        "benefits of drinking water",

        # Technology
        "how to use Excel",
        "best smartphones 2024",
        "how to fix WiFi connection",
        "iPhone vs Android",
        "latest software updates",

        # Entertainment
        "top movies of 2024",
        "popular TV shows",
        "latest songs",
        "news about celebrities",
        "best video games 2024",

        # Travel
        "best places to visit",
        "cheap flights",
        "best hotels",
        "3-day travel itinerary",
        "hotel reviews",

        # Shopping
        "best online deals",
        "buy electronics online",
        "customer reviews of popular products",
        "best smartphones under $500",
        "stores near me",

        # Education
        "online courses for programming",
        "best books on personal development",
        "top universities for computer science",
        "how to solve algebra problems",
        "scholarships for international students",

        # Finance
        "how to invest in stocks",
        "best personal loans",
        "how to improve credit score",
        "best savings accounts",
        "how to file taxes online",

        # Food and Recipes
        "easy dinner recipes",
        "best restaurants nearby",
        "gluten-free recipes",
        "how to cook steak",
        "common ingredient substitutes",

        # Miscellaneous
        "DIY home improvement projects",
        "how to start gardening",
        "best dog breeds for apartments",
        "latest fashion trends 2024",
        "inspirational quotes",
        
        # Additional Queries
        "interesting facts about space",
        "how to meditate for beginners",
        "best productivity apps",
        "history of ancient civilizations",
        "ways to reduce stress",
        "delicious smoothie recipes",
        "tips for better sleep",
        "how to start a small business",
        "famous quotes about success",
        "best travel destinations for solo travelers",
        "how to improve memory",
        "interesting facts about animals",
        "DIY home decor ideas",
        "how to learn a new language quickly",
        "popular fitness challenges",
        "healthy snack ideas",
        "how to stay motivated",
        "top TED talks of all time",
        "how to write a resume",
        "effective study techniques",
        "famous historical events",
        "ways to boost creativity",
        "how to organize your workspace",
        "self-care activities for mental health",
        "tips for effective time management"
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
        first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
        first_result.click()
    except Exception as e:
        print(f"Google search failed:")

def get_company_employee_count(company_name):
    search_prompts = [
        f"{company_name} employee count", f"{company_name} workforce size",
        f"{company_name} total employees", f"{company_name} staff size 2024"
    ]
    
    for prompt in search_prompts:
        try:
            search_url = f"https://www.google.com/search?q={prompt}"
            driver.get(search_url)
            time.sleep(2)

            span_element = driver.find_element(By.CSS_SELECTOR, 'span.hgKElc')
            b_element = span_element.find_element(By.TAG_NAME, 'b')
            
            if b_element:
                return b_element.text
        except Exception as e:
            print(f"Couldn't find employee count for {company_name} with prompt '{prompt}':")
    
    return None

def update_employee_count_in_db(company_id, employee_count):
    """
    Update MongoDB with the company's employee count.
    If employee count is not found, update with an empty string.
    """
    # If employee_count is not found or is None, set it to an empty string
    if not employee_count:
        employee_count = ""  # Update with an empty string if no employee count is found

    try:
        # Update the collection with the found or empty employee count value
        result = company_collection.update_one(
            {'_id': company_id},
            {'$set': {'firmographic.employee_count': employee_count}},
            upsert=True
        )

        # Check if the document was successfully updated
        if result.matched_count > 0:
            if employee_count:
                print(f"Updated company with ID {company_id} with employee count: {employee_count}")
            else:
                print(f"Updated company with ID {company_id} but no employee count found (set as empty string).")
        else:
            print(f"Failed to update company with ID {company_id}.")
    except Exception as e:
        print(f"Error updating employee count for company ID {company_id}: {e}")


def main():

    while True:

        try:
            company = company_collection.find_one({'firmographic.employee_count': {'$exists': False}})

            if not company :
                print("No companies to process")
                break

            
        
            try:
                company_name = company['name']
                companyId = company['_id']
                print(f"Fetching employee count for {company_name}...")
                employee_count = get_company_employee_count(company_name)
                
                if random.choice([True, False]):
                    human_search()  # Perform the human search simulation
                
                update_employee_count_in_db(companyId, employee_count)
            except Exception as e:
                print(f"Error processing company {company_name}: {e}")
        except Exception as e:
            print(f"Error fetching companies from database: {e}")

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
