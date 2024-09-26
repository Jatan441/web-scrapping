import browser
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui


#This behavior makes the function's output unpredictable, as it can return either value with equal probability.
def unpredictable_choice(arr):
    return random.choice(arr)
# Function to mimic human-like typing
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

def human_mouse_movement(action, element):
    action.move_to_element(element).perform()
    time.sleep(random.uniform(0.5, 6))
# Function to mimic human-like mouse movements
def human_mouse_movements(x, y, dx, dy):
    return
    # Move the mouse cursor to the specified coordinates
    pyautogui.moveTo(x, y)

    # Alternatively, you can move the cursor relative to its current position
    pyautogui.moveRel(dx, dy)


# Mimic human-like scrolling
def human_scroll():
    scroll_pause_time = random.uniform(1, 3)
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


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
    return unpredictable_choice(google_search_strings)

def human_search():
    try:
        time.sleep(5)
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get('https://www.google.com/')
        #Type the query to the google search
        search_bar = browser.find_element(By.TAG_NAME,'textarea')
        human_typing(search_bar, get_human_search_text())
        human_mouse_movement(ActionChains(browser),search_bar)
        time.sleep(random.uniform(0.05, 20))
        search_bar.send_keys(Keys.ENTER)
        time.sleep(5)
        human_mouse_movements(10, 20, 40, 12)
        human_mouse_movements(10, 20, 40, 120)
        human_mouse_movements(20, 10, 20, 12)
        human_mouse_movements(10, 20, 40, 12)
        human_mouse_movements(30, 20, 40, 12)
        human_mouse_movements(10, 40, 10, 102)
        human_mouse_movements(100, 300, 40, 12)
        human_mouse_movements(40, 20, 20, 120)
        # Find the first search result link and click it
        first_result = browser.find_element(By.CSS_SELECTOR, 'h3')
        first_result.click()
    except Exception as e:
        print("Google search failed."+str(e))
    browser.close()
    