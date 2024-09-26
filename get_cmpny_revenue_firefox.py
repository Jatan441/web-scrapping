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


def get_company_revenue(company_name):
    """
    Function to search Google for the company's revenue and find the text inside the <b> tag within
    a span that has the 'hgKElc' class.
    """
    search_url = f"https://www.google.com/search?q={company_name}+revenue"
    driver.get(search_url)
    time.sleep(2)  # Wait for the page to load

    # Parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Look for the span with class 'hgKElc' and then find the <b> tag inside it
    span_element = soup.find('span', class_='hgKElc')
    if span_element:
        b_tag = span_element.find('b')  # Find the <b> tag inside the span
        if b_tag:
            return b_tag.text  # Return the text inside the <b> tag

    return None

def update_revenue_in_db(company_name, revenue):
    """
    Function to update the company revenue in MongoDB.
    """
    # Check if revenue is already present in the database
    existing_company = company_collection.find_one({'name': company_name, 'firmographic.revenue_range.revenue': {'$exists': True, '$ne': ''}})
    if existing_company:
        print(f"Revenue already exists for {company_name}, skipping.")
        return

    # If no revenue exists, proceed to insert/update the revenue
    if revenue:
        company_collection.update_one(
            {'name': company_name},
            {'$set': {'firmographic.revenue_range.revenue': revenue}},
            upsert=True
        )
        print(f"Updated {company_name} with revenue: {revenue}")
    else:
        print(f"Revenue not found for {company_name}, skipping.")

def main():
    # Fetch companies from MongoDB (you can filter as needed)
    companies = company_collection.find()

    for company in companies:
        company_name = company['name']
        print(f"Fetching revenue for {company_name}...")

        # Check if revenue already exists, skip if it does
        existing_revenue = company_collection.find_one({'name': company_name, 'firmographic.revenue_range.revenue': {'$exists': True, '$ne': ''}})
        if existing_revenue:
            print(f"Revenue for {company_name} already exists, skipping.")
            continue

        # Get the revenue from Google
        revenue = get_company_revenue(company_name)

        # Randomly call human search
        if action.unpredictable_choice([True, False]):
            human_search()  # Perform the human search simulation

        # Update the revenue in MongoDB
        update_revenue_in_db(company_name, revenue)

if __name__ == "__main__":
    main()

    # Close the driver when done
    driver.quit()
