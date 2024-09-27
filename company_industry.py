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
db = client['warehouse']
company_collection = db['googlemapscompanies']

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

# Predefined human-like search terms
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
    """
    Perform a human-like search on Google by typing in the search bar and interacting with results.
    """
    try:
        driver.get('https://www.google.com/')
        search_bar = driver.find_element(By.TAG_NAME, 'textarea')
        human_typing(search_bar, action.unpredictable_choice(get_human_search_text()))
        search_bar.send_keys(Keys.ENTER)
        time.sleep(5)
        human_mouse_movements(10, 20, 40, 12)
        first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
        first_result.click()
    except Exception as e:
        print(f"Google search failed: {e}")

def get_company_industry(company_name):
    """
    Search for the company's industry information using Google and scrape it using BeautifulSoup.
    """
    search_url = f"https://www.google.com/search?q={company_name}+primary industry"
    driver.get(search_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    span_element = soup.find('span', class_='hgKElc')
    if span_element:
        b_tag = span_element.find('b')
        if b_tag:
            return b_tag.text

def update_industry_in_db(company_id, industry):
    """
    Update MongoDB with the company's industry if it's not already present.
    """
    if industry:
        result = company_collection.update_one(
            {'_id': company_id},
            {'$set': {'firmographic.industry': industry}},
            upsert=True
        )
        if result.matched_count > 0:
            print(f"Updated company with ID {company_id} with industry: {industry}")
        else:
            print(f"Failed to update company with ID {company_id}.")
    else:
        print(f"Industry not found for company ID {company_id}, skipping.")

def main():
    """
    Main function to fetch companies from MongoDB, get industry info from Google, and update MongoDB.
    """
    try:
        companies = company_collection.find({'firmographic.industry': {'$exists': False}})

        for company in companies:
            try:
                company_name = company['name']
                company_id = company['_id']
                print(f"Fetching industry for {company_name}...")

                industry = get_company_industry(company_name)

                if action.unpredictable_choice([True, False]):
                    human_search()

                update_industry_in_db(company_id, industry)
            except Exception as e:
                print(f"Skipping company {company_name} due to error: {e}")
    except Exception as e:
        print(f"Error fetching companies: {e}")

if __name__ == "__main__":
    main()
    driver.quit()
