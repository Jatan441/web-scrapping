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
from selenium.webdriver.support import expected_conditions as EC

# MongoDB connection setup
client = MongoClient('mongodb://firoz:firoz423*t@43.205.16.23:49153/')
db = client['warehouse']  # Replace with your database name
company_collection = db['googlemapscompanies']  # Replace with your collection name

# Firefox WebDriver setup
firefox_options = Options()
firefox_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

# firefox_options = Options()
# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

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
        search_text = unpredictable_choice(get_human_search_text())
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


# Function to move cursor and click
def move_and_click(element):
    actions.move_to_element(element).perform()  # Move cursor to the element
    time.sleep(random.uniform(0.5, 1.5))  # Random delay to simulate human-like behavior
    actions.click(element).perform()  # Click the element

def unpredictable_choice(arr):
    return random.choice(arr)


def handle_human_verification():
    try:
        # Try to locate the "Press & Hold" button by its identifier
        press_and_hold_button = driver.find_element(By.XPATH, "//button[text()='Press & Hold']")

        if press_and_hold_button:
            print("Human verification detected: Press & Hold button found")

            # Use ActionChains to click and hold the button for a specific duration
            action = ActionChains(driver)
            action.click_and_hold(press_and_hold_button).perform()

            # Hold the button for 5 seconds (or adjust this time based on what works)
            time.sleep(5)

            # Release the button
            action.release().perform()

            print("Press & Hold action completed")

            # Wait for any verification process to complete
            time.sleep(3)
            
        else:
            print("Press & Hold button not found, continuing with normal process.")
    
    except Exception as e:
        print(f"No human verification detected or an error occurred: {e}")




def search_company_on_zoominfo(company_name):
    try:
        # Search query for ZoomInfo with the company name
        search_query = f"{company_name} zoominfo"
        driver.get('https://www.google.com/')
        
        # Locate the search bar and simulate typing
        search_bar = driver.find_element(By.TAG_NAME, 'textarea')
        move_and_click(search_bar)
        
        # Simulate human typing in the search bar
        human_typing(search_bar, search_query)
        
        # Simulate a delay to mimic human behavior
        time.sleep(random.uniform(0.5, 2))
        
        # Submit the search query
        search_bar.send_keys(Keys.ENTER)
        
        # Wait for the search results to load
        time.sleep(3)
        
        # Locate the ZoomInfo search result and click on it
        zoominfo_result = driver.find_element(By.PARTIAL_LINK_TEXT, 'zoominfo.com')
        
        move_and_click(zoominfo_result)
        
        # handle_human_verification()
        
        # Wait for the ZoomInfo page to load
        time.sleep(10)
        
        # Extract revenue from the page
        revenue_element = driver.find_element(By.XPATH, '//h3[text()="Revenue"]/following-sibling::span[@class="content"]')
        revenue = revenue_element.text

        if revenue:
            return revenue
        else:
            print(f"No revenue information found for {company_name}")
            return None
                
    except Exception as e:
        print(f"Error fetching revenue for {company_name}: {e}")
        return None



# Update company data in MongoDB with revenue and mark as processed
def update_company_revenue_in_db(company_id, revenue):
    # If no revenue is found, set it to an empty string
    if not revenue:
        revenue = ""

    # Update the company document in MongoDB
    result = company_collection.update_one(
        {'_id': company_id},
        {'$set': {'firmographic.revenue_range.revenue': revenue, 'processed': True}},  # Add 'processed': True field
        upsert=True
    )

    # Check if the document was successfully updated
    if result.matched_count > 0:
        if revenue:
            print(f"Updated company with ID {company_id} with revenue: {revenue}")
        else:
            print(f"Updated company with ID {company_id} but no revenue found (set as empty string).")
    else:
        print(f"Failed to update company with ID {company_id}.")


# Main function to process companies
def main():
    try:
        while True:
            # Find a company where the 'revenue' field is either missing or is an empty string
            # Exclude companies where 'processed' is True
            company = company_collection.find_one({
                '$or': [{'firmographic.revenue_range.revenue': {'$exists': False}}, {'firmographic.revenue_range.revenue': ""}],
                'processed': {'$ne': True}  # Only find unprocessed companies
            })
        
            if not company:
                print("No companies to process")
                break

            company_name = company['name']
            company_id = company['_id']
            print(f"Fetching revenue for {company_name}...")

            # Fetch the revenue for the company from ZoomInfo
            revenue = search_company_on_zoominfo(company_name)
            print(f"Revenue for {company_name}: {revenue}")
            
            # Update the company document in MongoDB with the fetched revenue and mark it as processed
            update_company_revenue_in_db(company_id, revenue)
            
            if unpredictable_choice([True, False]):
                human_search()

    except Exception as e:
        print(f"Skipped a document due to error: {e}")


if __name__ == "__main__":
    main()
    driver.quit()
