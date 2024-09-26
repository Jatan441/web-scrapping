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
client = MongoClient('mongodb://firoz:firoz423*t@43.205.16.23:49153/')
db = client['warehouse']  # Replace with your database name
company_collection = db['googlemapscompanies']  # Replace with your collection name

# Firefox WebDriver setup
firefox_options = Options()
# firefox_options.add_argument("--headless")  # Run Firefox in headless mode
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

# Wait configuration
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def unpredictable_choice(arr):
    return random.choice(arr)

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
        # Simulate clicking the first result
        first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
        first_result.click()
    except Exception as e:
        print(f"Google search failed: {e}")




def get_company_employee_count(company_name):

    search_prompts = [
        f"{company_name} employee count",
        f"number of employees at {company_name}",
        f"{company_name} workforce size",
        f"how many people work at {company_name}",
        f"{company_name} total employees",
        f"{company_name} headcount",
        f"{company_name} staff size 2024",
        f"{company_name} number of employees LinkedIn"
    ]
    
    for prompt in search_prompts:
        search_url = f"https://www.google.com/search?q={prompt}"
        driver.get(search_url)
        time.sleep(2)  # Wait for the page to load

        # Parse the page content
        # soup = BeautifulSoup(driver.page_source, 'html.parser')

        # # Find the <mark> tag inside the <span> or any other parent element
        # mark_element = soup.find('mark', class_='QVRyCf')
        # print(mark_element)
        
        # if mark_element:
        #     # Return the text inside the <mark> tag
        #     return mark_element.text


        try:
            span_element = driver.find_element(By.CSS_SELECTOR, 'span.hgKElc')
            
            # Find the <b> tag inside the span
            b_element = span_element.find_element(By.TAG_NAME, 'b')
            
            # If found, return the text inside the <b> tag
            if b_element:
                return b_element.text

        except Exception as e:
            print(f"Couldn't find for {company_name} with prompt '{prompt}'")

    return None


def update_employee_count_in_db(company_name, employee_count):
    """
    Function to update the company employee count in MongoDB.
    """
    # Check if employee count is already present in the database
    existing_company = company_collection.find_one({'name': company_name, 'firmographic.employee_count': {'$exists': True, '$ne': ''}})
    if existing_company:
        print(f"Employee count already exists for {company_name}, skipping.")
        return

    # If no employee count exists, proceed to insert/update the employee count
    if employee_count:
        company_collection.update_one(
            {'name': company_name},
            {'$set': {'firmographic.employee_count': employee_count}},
            upsert=True
        )
        print(f"Updated {company_name} with employee count: {employee_count}")
    else:
        print(f"Employee count not found for {company_name}, skipping.")



# def main():
#     # Fetch companies from MongoDB (you can filter as needed)
#     companies = company_collection.find()

#     for company in companies:
#         company_name = company['name']
#         print(f"Fetching employee count for {company_name}...")

#         # Check if employee count already exists, skip if it does
#         existing_employee_count = company_collection.find_one({'name': company_name, 'firmographic.employee_count': {'$exists': True, '$ne': ''}})
#         if existing_employee_count:
#             print(f"Employee count for {company_name} already exists, skipping.")
#             continue

#         # Get the employee count from Google
#         employee_count = get_company_employee_count(company_name)

#         # Randomly call human search
#         if action.unpredictable_choice([True, False]):
#             human_search()  # Perform the human search simulation

#         # Update the employee count in MongoDB
#         update_employee_count_in_db(company_name, employee_count)


import random

def main():
    # Fetch companies that don't have an employee count in firmographics
    companies_without_employee_count = list(company_collection.find({'firmographic.employee_count': {'$exists': False}}))
  
    try:

        for company in companies_without_employee_count:
            company_name = company['name']
            print(f"Fetching employee count for {company_name}...")

            # Get the employee count from Google
            employee_count = get_company_employee_count(company_name)

            # Randomly call human search
            if random.choice([True, False ]):  # Use random.choice for randomness
                human_search()  # Perform the human search simulation

            # Update the employee count in MongoDB
            update_employee_count_in_db(company_name, employee_count)

    except Exception as e :
        print("Error getting employee count")




if __name__ == "__main__":
    main()

    # Close the driver when done
    driver.quit()