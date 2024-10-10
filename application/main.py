from pymongo import MongoClient
from datetime import datetime
import json
import os
import re

"""
!!!!! RUN CODE AS A PYTHON FILE TO PROPERLY RUN THE SYSTEM !!!!!
"""

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")


# Create or Switch to a Database in MongoDB
db = client['restaurants']  # Create or switch to database 'restaurants'

existing_dbs = client.list_database_names()
db_name = 'restaurants'
if db_name not in existing_dbs:                 # check to see if the database exists or not
    print(f"Creating database '{db_name}'")

# create a collection in the new database
if 'restaurantInfo' not in db.list_collection_names():
    db.create_collection('restaurantInfo')

if 'restaurantReviews' not in db.list_collection_names():
    db.create_collection('restaurantReviews')

# insertion of the Restaurant Info json into the database

collection = db["restaurantInfo"]

file_path = "RestaurantInfoData.json"

with open(file_path, 'r') as file:
    data = json.load(file)

if collection.count_documents({}) == 0:
    collection.insert_many(data)
    print("Inserted Restaurant Information into DB.")
else:
    print("DB is not empty, skipping insertion of restaurant information.")

# insertion of the customer reviews json into the database

collection = db["restaurantReviews"]

file_path = "CustomerReviews.json"

with open(file_path, 'r') as file:
    data = json.load(file)

if collection.count_documents({}) == 0:
    collection.insert_many(data)
    print("Inserted Customer Reviews into DB.")
else:
    print("DB is not empty, skipping insertion of customer reviews.")


### ================ Python code to establish a UI ========================

def mainMenu():
    """
    Display the main menu to the user, allowing the user to provide input on what option they wish to perform
    """
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("|  Restaurant Review System  |")
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("|                            |")
    print("| 1. Review Restaurant       |")
    print("| 2. Search Reviews          |")
    print("| 3. Search Restaurants      |")
    print("| 4. Database Admin          |")
    print("| 5. Exit                    |")
    print("|                            |")
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")

def adminMenu():
    """
    Display the admin menu for more administrative actions
    """
    print("\n ~~~~~~~~~~~~~ ADMIN MENU ~~~~~~~~~~~~ ")
    print("|                                       |")
    print("| 1. View Restaurant Info Database      |")
    print("| 2. View Restaurant Review Database    |")
    print("| 3. Add New Restaurant                 |")
    print("| 4. Update Restaurant Information      |")
    print("| 5. Delete Restaurant                  |")
    print("| 6. Delete Restaurant Review           |")
    print("| 7. Back to Main Menu                  |")
    print("|                                       |")
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

def reviewSortMenu():
    """
    Display an option list for sorting reviews
    """
    print("""1. Recent Reviews
2. Oldest Reviews
3. Lowest Rated
4. Highest Rated
    """)

def restaurantUpdate():
    """
    Display an option list for updating restaurant information
    """
    print("""1. Restaurant Name
2. Restaurant Address
3. Restaurant City
4. Restaurant State
5. Restaurant Zip Code
6. Restaurant Cuisine
7. Restaurant Price Point
8. Restaurant Phone Number
9. Restaurant Website
""")
    
def validate_phone_number(input):
    """
    Function that validates a phone number
    """
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    if re.match(pattern, input):
        return True
    else:
        return False

def validate_website(input):
    """
    Function that validates a website
    """
    pattern = r'^https://[\w\.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, input):
        return True
    else:
        return False

def generate_new_user_id(data):
    """
    function that generates a new userID based off the last assigned ID in the data set plus one
    """
    if data:
        return data[-1]["UserID"] + 1
    else:
        return 1

def get_integer_input(prompt):
    """"
    Function that prompts the user to enter an integer value
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter again.")
            continue

def style_document(document):
    """
    Function that prints documents in a more readable format
    """
    for key, value in document.items():
        print(f"{key}: {value}")
    print("\n")

def clear_terminal():
    """
    Function to clear the terminal to clean up the UI interface
    """
    # Check operating System
    if os.name == 'nt':         # Windows
        os.system('cls')
    elif os.name == 'posix':    # Linux/Mac
        os.system('clear')

def exit_verify():
    """
    Prompt user to press x to exit current screen
    """
    while True:
        exit_screen = input("Type X to go back to menu ").upper()
        if exit_screen == "X":
            clear_terminal()
            break
        else:
            print("Invalid choice! Please enter again.")

print()
clear_terminal()
print("Welcome to the Restaurant Review System!")
print("\nPlease enter your username and password.\n")
# prompt user to provide their username
username = input("Enter Username: ")
# prompt user to provide their password (for the sake of this project, there are no checks of password)
password = input("Enter Password: ")

# clear the terminal
clear_terminal()

print("\nLogin Successful!\n")

# Continuously prompt the user to choose an option from the main menu
while True:
    # function to display the main menu
    mainMenu()
    # prompt the user to choose an option from the main menu
    choice = get_integer_input("Enter your option (1-5): ")
    
    if choice == 1: # reviewing a restaurant (CREATE)
        clear_terminal()
        # set the current collection to the restaurantReviews collection
        collection = db['restaurantReviews']

        # read from the CustomerReviews json file and load it
        with open('CustomerReviews.json', 'r') as file:
            data = json.load(file)

        # find the last document in the collection and get the ReviewID value
        last_document = collection.find_one(sort=[("ReviewID", -1)])
        # assign last_review_id as the last value in the ReviewID field
        last_review_id = last_document['ReviewID']
        # assign new_review_id as the last_review_id + 1
        new_review_id = last_review_id + 1
        
        # cycle through the file of the Username field to check if the username exists
        existing_user = next((user for user in data if user['Username'] == username), None)
        
        # if the username exists
        if existing_user:
            # assign the userID to the existing UserID value from the database
            userID = existing_user["UserID"]
        else:
            # otherwise, create a new ID using the generate_new_user_id function
            userID = generate_new_user_id(data)

        # continuously loop until all fields have been filled out correctly
        while True:
            print("-------------- Review Restaurant --------------\n")
            collection = db["restaurantInfo"]
            # ask user for input for restaurantID
            restaurantID_input = input("Enter Restaurant ID (integer): ")
            # if the input is a digit
            if restaurantID_input.isdigit():
                # then assign the value to restaurantID as an integer
                restaurantID = int(restaurantID_input)
                # find the last document in the collection and get the RestaurantID value
                last_document = collection.find({}, {'_id': 0, 'RestaurantID': 1}).sort('RestaurantID', -1).limit(1)
                # extract the RestaurantID value from the last document and converting it to an integer
                for document in last_document:
                    last_restaurant_id = int(document['RestaurantID'])

                # if the restaurantID is between 1 and the last restaurantID
                if 1 <= restaurantID <= last_restaurant_id:
                    collection = db['restaurantReviews']
                    # then move on to the next input question
                    break
                else:
                    # prompt user to input a valid value, loop again
                    print("Invalid ID, Please enter an integer value.")
            else:
                # prompt user to input a valid value, loop again
                print("Please enter a numeric value.")

        # assign the date_of_review as today
        date_of_review = datetime.now().strftime("%Y-%m-%d")
        
        # continuously ask for date of visit until a valid entry has been made
        while True:
            # ask for user input for date of visit
            date_of_visit_input = input("Enter your date of visit (YYYY-MM-DD): ")
            try:
                # if the user's input can be converted into a datetime object
                date_of_visit = datetime.strptime(date_of_visit_input, "%Y-%m-%d").date().strftime("%Y-%m-%d")
                # then move on to the next input question
                break
            except ValueError:
                # if not, then prompt the user to input a valid date
                print("Incorrect data format, please enter date in YYYY-MM-DD format.")
        
        # continuously loop until a valid rating has been entered
        while True:
            # ask for user input for a rating
            rating = input("Enter rating (1 - 5): ")
            # if the rating is a digit and is between 1 and 5 inclusive
            if rating.isdigit() and 1 <= int(rating) <= 5:
                # then assign the value to rating as an integer
                rating = int(rating)
                # move on to the next input question
                break
            else:
                # prompt user to input a valid rating
                print("Invalid rating. Please enter a number between 1 and 5")
        
        # ask user for review
        review = input("Enter your review: ")
        # ensure that the review field is not empty
        while not review.strip():
            # prompt user to leave a review
            print("Review cannot be blank. Please enter your review.")
            # ask user for review
            review = input("Enter your review: ")

        # create the new document as a json document
        new_document = {
            "ReviewID": new_review_id,
            "UserID": userID,
            "RestaurantID": restaurantID,
            "Username": username,
            "Date_of_Review": date_of_review,
            "DateOfVisit": date_of_visit,
            "Rating": rating,
            "Review": review
        }

        # insert the newly created document into the collection
        insert_doc = collection.insert_one(new_document)

        # verify to user that the entry was added successfully
        print("\nSuccessfully added review\n")

        exit_verify()

    elif choice  == 2: # search for reviews (READ)
        # set the collection to the "restaurantReviews" collection
        collection = db["restaurantReviews"]

        # clear the terminal
        clear_terminal()

        print("-------------- Review Search --------------\n")

        # prompt the user to enter the restaurant ID
        restaurant_id = get_integer_input("Enter the restaurant ID: ")

        print("\nHow would you like to sort the reviews?")
        # display the review sort menu

        # function to display the review sort menu
        reviewSortMenu()

        print()
        # continuously prompt the user to enter a valid choice until a valid choice is entered
        while True:
            # get the user's choice
            sort_choice = get_integer_input("Enter your choice: ")

            # clear the terminal
            clear_terminal()

            print("-------------- Review Search --------------\n")

            # if the user enters 1
            if sort_choice == 1:
                # sort the reviews by date in descending order
                review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0, 'ReviewID': 0, 'UserID': 0, 'RestaurantID': 0}).sort("Date_of_Review", -1)

                # display the reviews
                for review in review_sort_results:
                    # style the document
                    style_document(review)

                # break from loop
                exit_verify()
       
            # if the user enters 2
            elif sort_choice == 2:
                # sort the reviews by date in ascending order
                review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0, 'ReviewID': 0, 'UserID': 0, 'RestaurantID': 0}).sort("Date_of_Review", 1)

                # display the reviews
                for review in review_sort_results:
                    # style the document 
                    style_document(review)

                # break from loop
                exit_verify()

            # if the user enters 3
            elif sort_choice == 3:
                # sort the reviews by rating in ascending order
                review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0, 'ReviewID': 0, 'UserID': 0, 'RestaurantID': 0}).sort("Rating", 1)

                # display the reviews
                for review in review_sort_results:
                    # style the document
                    style_document(review)

                # break from loop
                exit_verify()

            # if the user enters 4
            elif sort_choice == 4:
                # sort the reviews by rating in descending order
                review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0, 'ReviewID': 0, 'UserID': 0, 'RestaurantID': 0}).sort("Rating", -1)

                # display the reviews
                for review in review_sort_results:
                    # style the document
                    style_document(review)

                # break from loop
                exit_verify()

            # if the user enters an invalid value
            else:
                # display an error message
                print("Invalid input! Please enter again.")
            
            # break from loop
            break

    elif choice == 3: # search restaurants (READ)
        # set collection to restaurantInfo
        collection = db["restaurantInfo"]

        # clear the terminal
        clear_terminal()

        # continuously ask the user for a restaurant ID
        while True:
            print("-------------- Restaurant Search --------------\n")
            # prompt the user for a restaurant ID
            restaurant_id = get_integer_input("Enter the restaurant ID: ")

            # find the restaurant with the given ID
            user_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0})

            # display the reviews
            for documents in user_results:
                print()
                # style the document
                style_document(documents)

            # ask the user if they want to perform another search
            exit_screen = input("Would you like to perform another search? (Y / N): ").upper()
            # if the user wants to perform another search, continue
            if exit_screen == "Y":
                clear_terminal()
                continue
            # if the user does not want to perform another search, break
            elif exit_screen == "N":
                # clear the terminal
                clear_terminal()
                break
            # if the user enters an invalid choice, display an error message and continue
            else:
                print("Invalid choice! Performing another search.")

    elif choice == 4: # database admin
        # continuously prompt the user for their choice
        while True:
            # clear the terminal
            clear_terminal()

            # display the admin menu
            adminMenu()

            # get the user's choice
            admin_choice = get_integer_input("Enter your option (1-6): ")

            if admin_choice == 1: # view restaurant info database (READ)
                # assign the collection
                collection = db["restaurantInfo"]

                # display the restaurant info
                show_documents = collection.find({}, {'_id': 0})

                for documents in show_documents:
                    style_document(documents)

                # exit screen
                exit_verify()

            elif admin_choice == 2: # view restaurant review database (READ)
                # assign the collection
                collection = db["restaurantReviews"]

                # clear the terminal
                clear_terminal()

                print("-------------- Review Search --------------\n")

                # prompt the user to enter the restaurant ID
                restaurant_id = get_integer_input("Enter the restaurant ID: ")

                print("\nHow would you like to sort the reviews?")
                # Display the menu
                reviewSortMenu()

                print()
                # loop until the user enters a valid choice
                while True:
                    # get the user's choice
                    sort_choice = get_integer_input("Enter your choice: ")

                    clear_terminal()

                    # if the user enters 1, sort the reviews by date in descending order
                    if sort_choice == 1:
                        # sort the reviews by date in descending order
                        review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0}).sort("Date_of_Review", -1)
                        # print the results
                        for review in review_sort_results:
                            # style the review
                            style_document(review)
                        # break from the loop
                        exit_verify()
       
                    # if the user enters 2, sort the reviews by date in ascending order
                    elif sort_choice == 2:
                        # sort the reviews by date in ascending order
                        review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0}).sort("Date_of_Review", 1)

                        # print the results
                        for review in review_sort_results:
                            # style the reviews
                            style_document(review)
                        # break from the loop
                        exit_verify()

                    # if the user enters 3, sort the reviews by rating in ascending order
                    elif sort_choice == 3:
                        # sort the reviews by rating in ascending order
                        review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0}).sort("Rating", 1)

                        # print the reviews
                        for review in review_sort_results:
                            # style the reviews
                            style_document(review)
                        # break from the loop
                        exit_verify()
                    
                    # if the user enters 4, sort the reviews by rating in descending order
                    elif sort_choice == 4:
                        # get the number of
                        review_sort_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0}).sort("Rating", -1)
                        # display the documents
                        for review in review_sort_results:
                            # style the document
                            style_document(review)
                        # break from loop
                        exit_verify()
                    # if the user enters an invalid choice
                    else:
                        # print an error message
                        print("Invalid input! Please enter again.")
                    # break from the loop
                    break

            elif admin_choice == 3: # add a new restaurant (CREATE)
                # set the current collection to restaurantInfo
                collection = db["restaurantInfo"]

                # find the last document in the collection and get the RestaurantID value
                last_document = collection.find_one(sort=[("RestaurantID", -1)])
                # assign last_restaurant_id as the last value in the RestaurantID field
                last_restaurant_id = last_document['RestaurantID']
                # assign new_restaurant_id as the last_restaurant_id + 1
                new_restaurant_id = last_restaurant_id + 1

                while True:
                    # clear the terminal
                    clear_terminal()

                    print("============ Restaurant Creation ============\n")

                    # prompt user for restaurant name
                    restaurant_name = input("Please enter the restaurant name: ")

                    # if the restaurant name is empty
                    if restaurant_name == "":
                        print("Restaurant name cannot be empty! Please enter again.")
                        # prompt user to input a valid restaurant name
                        continue
                    else:
                        # move on to next prompt question
                        break

                while True:
                    # prompt user for restaurant address
                    address_input = input("Please enter the restaurant address: ")

                    # if the restaurant address is empty
                    if address_input == "":
                        print("Restaurant address cannot be empty! Please enter again.")
                        # prompt user to input a valid restaurant address
                        continue
                    else:
                        # move on to next prompt question
                        break
                
                while True:
                    # prompt user for restaurant city
                    city_input = input("Please enter the city the restaurant is located in: ")

                    # if the restaurant city is empty
                    if city_input == "":
                        print("City cannot be empty! Please enter again.")
                        # prompt user to input a valid restaurant city
                        continue
                    else:
                        # move on to next prompt question
                        break
                
                while True:
                    # prompt user for restaurant state
                    state_input = input("Please enter the state the restaurant is located in: ")

                    # if the restaurant state is empty
                    if state_input == "":
                        print("State cannot be empty! Please enter again.")
                        # prompt user to input a valid restaurant state
                        continue
                    else:
                        # move on to next prompt question
                        break
                
                while True:
                    # prompt user for restaurant zip code
                    zip_input = input("Please enter the zip code of the restaurant: ")

                    # if the restaurant zip code has five digits
                    if len(zip_input) == 5 and zip_input.isdigit():
                        # move on to next prompt question
                        break
                    else:
                        print("Zip code must be 5 digits! Please enter again.")
                        # prompt user to input a valid restaurant zip code
                        continue
                
                while True:
                    # prompt user for restaurant cuisine type
                    cuisine_input = input("Please enter the restaurant cuisine type: ")

                    # if the restaurant cuisine type is empty
                    if cuisine_input == "":
                        print("Cuisine cannot be empty! Please enter again.")
                        # prompt user to input a valid restaurant cuisine type
                        continue
                    else:
                        # move on to next prompt question
                        break

                while True:
                    # prompt user for restaurant price range
                    price_input = get_integer_input("Please enter the restaurant price range (1-3): ")

                    # if the restaurant price range is empty
                    if price_input == "":
                        print("Price cannot be empty! Please enter again.")
                        # prompt user to input a valid restaurant price range
                        continue
                    # if the user inputs a value of 1
                    elif price_input == 1:
                        # assign price to the value of 1
                        price = "$"
                        # move on to next prompt question
                        break
                    # if the user inputs a value of 2
                    elif price_input == 2:
                        # assign price to the value of 2
                        price = "$$"
                        # move on to next prompt question
                        break
                    # if the user inputs a value of 3
                    elif price_input == 3:
                        # assign price to the value of 3
                        price = "$$$"
                        # move on to next prompt question
                        break
                    else:
                        print("Please enter a valid value between 1 and 3")
                        # prompt user to input a valid restaurant price range
                        continue

                while True:
                    # prompt user to input a restaurant phone number
                    phone_input = input("Please enter the restaurant phone number (###-###-####): ")
                    
                    # if the user enters a valid phone number
                    if validate_phone_number(phone_input):
                        # move on to the next prompt question
                        break
                    # if the user enters an invalid phone number
                    else:
                        print("Invalid phone number! Please enter again.")
                        # prompt user to enter a valid phone number
                        continue

                while True:
                    # prompt user to input a restaurant website
                    website_input = input("Please enter the restaurant website (https://www.example.com): ")

                    # if the user enters a valid website
                    if validate_website(website_input):
                        # move on to the next prompt question
                        break
                    else:
                        print("Invalid website! Please enter again.")
                        # prompt user to enter a valid website
                        continue

                new_document = {
                    'RestaurantID': new_restaurant_id,
                    'Name': restaurant_name,
                    'Address': address_input,
                    'City': city_input,
                    'State': state_input,
                    'ZIP': zip_input,
                    'Rating': 0,
                    'Cuisine': cuisine_input,
                    'Price': price,
                    'Phone': phone_input,
                    'Website': website_input,
                }

                
                # insert the newly created document into the collection
                insert_doc = collection.insert_one(new_document)

                # verify to user that the entry was added successfully
                print("\nSuccessfully added new restaurant\n")

                exit_verify()

            elif admin_choice == 4: # update restaurant information (UPDATE)
                # assign the collection to restaurantInfo
                collection = db['restaurantInfo']

                # clear the terminal
                clear_terminal()

                print("----------- Update Restaurant Information -----------\n")

                # loop until the user enters a valid restaurant ID
                while True:
                    # get the restaurant ID
                    restaurant_id = get_integer_input("Enter the restaurant ID: ")

                    print("\nThis is your chosen restaurant:")
                    # find the restaurant with the given ID
                    restaurant_results = collection.find({"RestaurantID": restaurant_id})
                    # display the documents
                    for restaurant in restaurant_results:
                        # style the document
                        style_document(restaurant)

                    print("\nIs this correct?")
                    # loop until the user enters a valid choice
                    while True:
                        # get the user's choice
                        correct_choice = get_integer_input("Enter 1 for yes, 2 for no: ")
                        # if the user enters 1
                        if correct_choice == 1:
                            print("\nWhat would you like to update?")
                            # display the options for updating the restaurant
                            restaurantUpdate()

                            # loop until the user enters a valid choice
                            while True:
                                # get the user's choice
                                update_choice = get_integer_input("Option: ")

                                # if the user wants to update the name
                                if update_choice == 1:
                                    # loop until the user enters a valid name
                                    new_name = input("Enter the new name: ")
                                    # update the name in the document
                                    collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"Name": new_name}})
                                    # print a success message
                                    print("\nRestaurant name updated successfully!")
                                    # break out of the loop
                                    break
                                # if the user wants to update the address
                                elif update_choice == 2:
                                    # ask the user to enter a new address
                                    new_address = input("Enter the new address: ")
                                    # update the address in the document
                                    collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"Address": new_address}})
                                    # print a success message
                                    print("\nRestaurant address updated successfully!")
                                    # break out of the loop
                                    break
                                # if the user wants to update the city
                                elif update_choice == 3:
                                    # ask the user to enter a new city
                                    new_city = input("Enter the new city: ")
                                    # update the city in the document
                                    collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"City": new_city}})
                                    # print a success message
                                    print("\nRestaurant city updated successfully!")
                                    # break out of the loop
                                    break
                                # if the user wants to update the state
                                elif update_choice == 4:
                                    # ask the user to enter a new state
                                    new_state = input("Enter the new state: ")
                                    # update the state in the document
                                    collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"State": new_state}})
                                    # print a success message
                                    print("\nRestaurant state updated successfully!")
                                    # break out of the loop
                                    break
                                # if the user wants to update the zip code
                                elif update_choice == 5:
                                    # loop until the user enters a valid zip code
                                    while True:
                                        # ask the user to enter a new zip code
                                        new_zip = input("Enter the new zip code: ")
                                        # if the zip code is 5 digits
                                        if len(new_zip) == 5 and new_zip.isdigit():
                                            # update the zip code of the document
                                            collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"ZIP": new_zip}})
                                            # print successful message if the zip code is updated successfully
                                            print("\nRestaurant zip code updated successfully!")
                                            # break from the loop
                                            break
                                        # if the zip code is not 5 digits
                                        else:
                                            # print an error message if the zip code is invalid
                                            print("Invalid zip code! Please enter again.")
                                    # break from the loop
                                    break
                                # if the user wants to update the cuisine type
                                elif update_choice == 6:
                                    # ask the user to enter a new cuisine type
                                    new_cuisine = input("Enter new cuisine type: ")
                                    # update the cuisine of the document
                                    collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"Cuisine": new_cuisine}})
                                    # print successful message if the cuisine is updated successfully
                                    print("\nRestaurant cuisine updated successfully!")
                                    # break from the loop
                                    break
                                # if the user wants to update the price range
                                elif update_choice == 7:
                                    # ask the user to enter a new price range
                                    while True:
                                        # ask the user to enter a new price range
                                        new_price = input("Enter the new price range (enter as $ [1-3]): ")
                                        # if the user enters a valid price range
                                        if new_price == "$" or new_price == "$$" or new_price == "$$$":
                                            # update the price range of the document
                                            collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"Price": new_price}})
                                            # print successful message if the price range is updated successfully
                                            print("\nRestaurant price range updated successfully!")
                                            # break from the loop
                                            break
                                        # if the user enters an invalid price range
                                        else:
                                            # print an error message if the user enters an invalid price range
                                            print("Invalid price range! Please enter again.")
                                    # break from the loop
                                    break
                                # if the user wants to update the phone number
                                elif update_choice == 8:
                                    # ask the user to enter a new phone number
                                    while True:
                                        # ask the user to enter a new phone number
                                        new_phone = input("Enter the new phone number (###-###-####): ")
                                        # if the user enters a valid phone number
                                        if validate_phone_number(new_phone):
                                            # update the phone number of the document
                                            collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"Phone": new_phone}})
                                            # print successful message if the phone number is updated successfully
                                            print("\nRestaurant phone number updated successfully!")
                                            # break from the loop
                                            break
                                        # if the user enters an invalid phone number
                                        else:
                                            # print an error message if the user enters an invalid phone number
                                            print("Invalid phone number! Please enter again.")
                                    # break from the loop
                                    break
                                # if the user wants to update the website
                                elif update_choice == 9:
                                    # ask the user to enter a new website
                                    while True:
                                        # ask the user to enter a new website
                                        new_website = input("Enter a new website (https://www.website.com): ")
                                        # if the user enters a valid website
                                        if validate_website(new_website):
                                            # update the website of the document
                                            collection.update_one({"RestaurantID": restaurant_id}, {"$set": {"Website": new_website}})
                                            # print successful message if the website is updated successfully
                                            print("\nRestaurant website updated successfully!")
                                            # break from the loop
                                            break
                                        # if the user enters an invalid website
                                        else:
                                            # print an error message if the user enters an invalid website
                                            print("Invalid website! Please enter again.")
                                    # break from the loop
                                    break
                                # if the user enters an invalid choice
                                else:
                                    # print an error message if the user enters an invalid choice
                                    print("Invalid choice! Please enter again.")
                            # break from the loop
                            break
                        # if the user enters 2
                        elif correct_choice == 2:
                            # break the loop
                            break
                        # if the user enters an invalid choice
                        else:
                            # print an error message if the user enters an invalid choice
                            print("Invalid input! Please enter again.")
                    # break from the loop
                    break
                # break from the loop
                exit_verify()

            elif admin_choice == 5: # delete restaurant (DELETE)
                # assign collection to restaurantInfo
                collection = db["restaurantInfo"]

                # clear the terminal
                clear_terminal()

                print("-------------- Delete Restaurant --------------\n")

                # continuously ask for restaurant ID until user enters a valid one
                while True:
                    # prompt user for a restaurant ID
                    restaurant_id = get_integer_input("Enter the restaurant ID: ")
                    # find the document that matches to the user's input
                    user_results = collection.find({"RestaurantID": restaurant_id}, {'_id': 0})

                    # display the documents
                    for documents in user_results:
                        # style the document
                        style_document(documents)

                    print("\nIs this correct?")
                    # continuously ask for user's choice until user enters a valid one
                    while True:
                        # prompt user for a choice
                        correct_choice = get_integer_input("Enter 1 for yes, 2 for no: ")
                        # if user enters 1
                        if correct_choice == 1:
                            # delete the document
                            collection.delete_one({"RestaurantID": restaurant_id})
                            # assign the collection to restaurantReviews
                            collection = db['restaurantReviews']
                            # delete the restaurant's reviews
                            collection.delete_many({"RestaurantID": restaurant_id})
                            # clear the terminal
                            clear_terminal()
                            # print a success message
                            print("Restaurant and its reviews were deleted successfully!\n")
                            # break from the loop
                            break
                        # if user enters 2
                        elif correct_choice == 2:
                            # break from the loop
                            break
                        # if user enters an invalid choice
                        else:
                            # print an error message
                            print("Invalid input! Please enter again.")
                    # break from loop
                    break
                # break from loop
                exit_verify()

            elif admin_choice == 6: # delete restaurant review (DELETE)
                # assign the collection to restaurantReviews
                collection = db["restaurantReviews"]
                # clear the terminal
                clear_terminal()

                print("-------------- Delete Restaurant Review --------------\n")

                while True:
                    # get review id from user
                    review_id = get_integer_input("Enter Review ID: ")
                    # find the review based on user's input
                    user_results = collection.find({"ReviewID": review_id}, {'_id': 0})

                    # display the documents
                    for documents in user_results:
                        # style the documents
                        style_document(documents)

                    print("\nIs this the correct review?")
                    # loop until user enters a valid choice
                    while True:
                        # ask user if the review is correct
                        correct_choice = get_integer_input("Enter 1 for yes, 2 for no: ")

                        # if user enters 1
                        if correct_choice == 1:
                            # delete the review
                            collection.delete_one({"ReviewID": review_id})
                            # display success message
                            print("Review was deleted successfully!")
                            # break from loop
                            break
                        # if user enters 2
                        elif correct_choice == 2:
                            # break from loop
                            break
                        # if user enters invalid choice
                        else:
                            # display error message if user enters invalid choice
                            print("Invalid input! Please enter again.")
                    # break from the inner loop
                    break
                # break from the loop
                exit_verify()

            elif  admin_choice == 7: # back to main menu
                # clear the terminal
                clear_terminal()
                # go back to main menu
                break
            # if user enters invalid choice
            else:
                # display error message if user enters invalid choice
                print("Invalid choice! Please enter again.")
                
    elif choice == 5: # exit the program
        clear_terminal()
        # exit the program
        break
    # if user enters invalid choice
    else:
        # display error message if user enters invalid choice
        print("Invalid choice! Please enter again.")

# close the connection to the MongoDB server
client.close()
