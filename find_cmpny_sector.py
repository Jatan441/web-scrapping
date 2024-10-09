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
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

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

# List of human-like search strings
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

# Perform a human-like search on Google
def human_search():
    try:
        driver.get('https://www.google.com/')
        search_bar = driver.find_element(By.TAG_NAME, 'textarea')
        search_text = action.unpredictable_choice(get_human_search_text())
        human_typing(search_bar, search_text)
        actions.move_to_element(search_bar).perform()
        time.sleep(random.uniform(0.05, 20))
        search_bar.send_keys(Keys.ENTER)
        time.sleep(5)
        human_mouse_movements(10, 20, 40, 12)
        first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
        first_result.click()
    except Exception as e:
        print(f"Google search failed:")

# Get company sector from Google search results
def get_company_sector(company_name):
    search_prompts = [
        f"{company_name} sector", f"What sector is {company_name} in?", 
        f"{company_name} market sector", f"{company_name} sector classification"
    ]

    for prompt in search_prompts:
        try:
            driver.get('https://www.google.com/')
            search_bar = driver.find_element(By.TAG_NAME, 'textarea')
            human_typing(search_bar, prompt)
            actions.move_to_element(search_bar).perform()
            time.sleep(random.uniform(0.05, 20))
            search_bar.send_keys(Keys.ENTER)
            time.sleep(2)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            span_element = soup.find('span', class_='hgKElc')
            if span_element:
                b_tag = span_element.find('b')
                if b_tag:
                    return b_tag.text
        except Exception as e:
            print(f"Couldn't find sector for {company_name} with prompt '{prompt}'")



def update_sector_in_db(company_id, sector):
    """
    Update MongoDB with the company's sector.
    If sector is not found, update with an empty string.
    """
    # If sector is not found, set it as an empty string
    if not sector:
        sector = ""  # Update with an empty string if no sector is found

    # Update the collection with the found or empty sector value'

    
    result = company_collection.update_one(
        {'_id': company_id},
        {'$set': {'firmographic.sector': sector}},
        upsert=True
    )

    # Check if the document was successfully updated
    if result.matched_count > 0:
        if sector:
            print(f"Updated company with ID {company_id} with sector: {sector}")
        else:
            print(f"Updated company with ID {company_id} but no sector found (set as empty string).")
    else:
        print(f"Failed to update company with ID {company_id}.")


# Main function to process companies
def main():
    try:
        while True :

            company = company_collection.find_one({'firmographic.sector': {'$exists': False}})
        
            if not company :
                print("no companies to process")
                break

            company_name = company['name']
            company_id = company['_id']
            print(f"Fetching sector for {company_name}...")
            sector = get_company_sector(company_name)

            if action.unpredictable_choice([True, False]):
                human_search()

            update_sector_in_db(company_id, sector)
    except Exception as e:
        print(f"Skipped a document due to error:")

if __name__ == "__main__":
    main()
    driver.quit()
