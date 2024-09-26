import requests
from pymongo import MongoClient
import re

# MongoDB connection details
mongo_url = "mongodb://firoz:firoz423*t@43.205.16.23:49153/"
db_name = "warehouse"
collection_name = "contacts"

# Function to clean and extract the last name
def clean_last_name(last_name):
    match = re.match(r"^\(([^)]+)\)\s*(.+)$", last_name)
    if match:
        return match.group(2).strip()  # Return the last name part after the parentheses
    return last_name.strip()  # Return the full last name if no parentheses found

# Function to predict the email using the external API
def predict_email(first_name, last_name, company_name, domain):
    try:
        url = f"http://192.168.2.165:8002/verify-email?first_name={first_name}&last_name={last_name}&company_name={company_name}&domain={domain}"
        response = requests.post(url)
        response.raise_for_status()  # Raise error for bad responses (4xx/5xx)
        print("predicted email :",response.json().get("email"))
        return response.json().get("email")
    
    except requests.exceptions.RequestException as e:
        print(f"Error predicting email: {str(e)}")
        return None

# Function to update emails in MongoDB
def update_emails():
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[collection_name]

    try:
        while True:
            # Find a document that needs a predicted email and is not skipped
            document = collection.find_one({"predictedEmail": {"$exists": False}})
            if not document:
                print("No more documents to process.")
                break

            first_name = document.get("firstName")
            last_name = document.get("lastName")
            company_name = document.get("companyName")
            email = document.get("email")

            try:
                if email:
                    if '*' in email:
                        # Email contains asterisks, predict the correct email
                        print(f"Email contains asterisks for document with _id: {document['_id']}. Predicting email.")

                        domain = email.split('@')[1] if '@' in email else "example.com"  # Use domain from the email if available
                        cleaned_last_name = clean_last_name(last_name)
                        print(cleaned_last_name)
                        # Predict the correct email
                        predicted_email = predict_email(first_name, cleaned_last_name, company_name, domain)

                        if predicted_email:
                            collection.update_one({"_id": document["_id"]}, {"$set": {"predictedEmail": predicted_email}})
                            print(f"Updated document with _id: {document['_id']}")
                        else:
                            collection.update_one({"_id": document["_id"]}, {"$set": {"predictedEmail": ""}})
                            print(f"Failed to predict email for document with _id: {document['_id']}")
                    elif not re.match(r"^\S+@\S+\.\S+$", email):
                        # Email exists but is not in the proper format
                        print(f"Invalid email format for document with _id: {document['_id']}. Marking predictedEmail as blank.")
                        collection.update_one({"_id": document["_id"]}, {"$set": {"predictedEmail": ""}})
                    else:
                        # Email exists and is valid, no action needed
                        collection.update_one({"_id": document["_id"]}, {"$set": {"predictedEmail": ""}})
                else:
                    # Email does not exist, predict the email
                    print(f"Email missing for document with _id: {document['_id']}. Predicting email.")
                    domain = "example.com"  # Default domain if email is missing
                    cleaned_last_name = clean_last_name(last_name)

                    # Predict the correct email
                    print(first_name, cleaned_last_name, company_name, domain)
                    predicted_email = predict_email(first_name, cleaned_last_name, company_name, domain)
                    print(predicted_email)

                    if predicted_email:
                        collection.update_one({"_id": document["_id"]}, {"$set": {"predictedEmail": predicted_email}})
                        print(f"Updated document with _id: {document['_id']}")
                    else:
                        collection.update_one({"_id": document["_id"]}, {"$set": {"predictedEmail": ""}})
                        print(f"Failed to predict email for document with _id: {document['_id']}")
            except Exception as err:
                print(f"Error processing document with _id: {document['_id']}: {str(err)}")
                collection.update_one({"_id": document["_id"]}, {"$set": {"skipped": True}})
                print(f"Marked document with _id: {document['_id']} as skipped")

    except Exception as error:
        print(f"Error updating emails: {str(error)}")
    finally:
        client.close()

# Call the function
update_emails()
