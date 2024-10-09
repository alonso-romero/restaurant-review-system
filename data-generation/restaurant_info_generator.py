from faker import Faker
import pandas as pd
import random

fake = Faker()

num_records = 100

# assign cuisine types to a list of different ethnic cuisines since faker can't produce it for us
cuisine_types = ['Italian', 'French', 'Chinese', 'Japanese', 'Mexican', 'Indian', 'Thai', 'Spanish', 'Greek', 'Lebanese', 'Korean', 'Brazilian', 'Vietnamese', 'Moroccan', 'American']
# randomly shuffle between the cuisine type list
random.shuffle(cuisine_types)

def PriceIcon():
    """
    Convert the random value generated by the faker function to a $ based on a scale of 1 to 3
    
    Returns:
        String: '$'
    """
    # Randomly assign a price point on a scale of 1 to 3
    price_point = random.randint(1, 3)
    
    # if the value is 1
    if price_point == 1:
        # assign it as cheap
        price = '$'
    # if the value is 2
    elif price_point == 2:
        # assign it as moderate
        price = '$$'
    # if the value is 3
    elif price_point == 3:
        # assign it as expensive
        price = '$$$'
    
    return price

def PhoneNumber():
    """
    Generate a fake phone number that has 10 digits and is separated by a hyphen

    Returns:
        String: '###-###-####'
    """
    
    # Generate the fake unfiltered number
    phone_number = fake.phone_number()
    # Remove an extension if it is present in the generated phone number
    phone_number = phone_number.split('x')[0]
    # Remove any non-digit characters from the generated number
    phone_number = ''.join(filter(str.isdigit, phone_number))
    
    # if the generated phone number is greater than 10 digits
    if len(phone_number) > 10:
        # assign the phone number to be 10 digits
        phone_number = phone_number[:10]
    # if the generated phone number is less than 10 digits
    elif len(phone_number) < 10:
        # assign the phone number to be 10 digits
        phone_number = phone_number + '0' * (10 - len(phone_number))
    
    # format the 10 digit phone number with hyphens in between
    format_number = '{}-{}-{}'.format(phone_number[:3], phone_number[3:6], phone_number[6:])
    
    # return the formatted number to the function
    return format_number

data = {
    'RestaurantID': list(range(1, num_records + 1)),
    'Name': [fake.word() + ' ' + fake.word() for _ in range(num_records)],
    'Address': [fake.address() for _ in range(num_records)],
    'City': [fake.city() for _ in range(num_records)],
    'State': [fake.state() for _ in range(num_records)],
    'ZIP': [fake.zipcode() for _ in range(num_records)],
    'Rating': [round(random.uniform(1, 5)) for _ in range(num_records)],
    'Cuisine': [cuisine_types[i % len(cuisine_types)] for i in range(num_records)],
    'Price': [PriceIcon() for _ in range(num_records)],
    'Phone': [PhoneNumber() for _ in range(num_records)],
    'Website': [fake.url() for _ in range(num_records)]
}

df = pd.DataFrame(data)

# df.to_csv('RestaurantInfoData.csv', index=False)
df.to_json('RestaurantInfoData.json', orient='records')
