from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

# MongoDB connection setup
client = MongoClient('mongodb://firoz:firoz423*t@43.205.16.23:49153/')
db = client['warehouse']  # Replace with your database name
company_collection = db['googlemapscompanies']  # Replace with your collection name

# Chrome WebDriver setup
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

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
    # First, create the 'firmographic.revenue_range.revenue' field with an empty string if it doesn't exist
    company_collection.update_one(
        {'name': company_name},
        {
            '$setOnInsert': {'firmographic.revenue_range.revenue': ""}  # Create the field if it doesn't exist
        },
        upsert=True
    )

    # If revenue is found, update the field with the actual value
    if revenue:
        company_collection.update_one(
            {'name': company_name},
            {'$set': {'firmographic.revenue_range.revenue': revenue}}
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
        
        # Get the revenue from Google
        revenue = get_company_revenue(company_name)
        
        # Update the revenue in MongoDB
        update_revenue_in_db(company_name, revenue)

if __name__ == "__main__":
    main()

    # Close the driver when done
    driver.quit()
