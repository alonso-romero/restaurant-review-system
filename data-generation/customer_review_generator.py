from faker import Faker
import pandas as pd
import random

fake = Faker()

restaurant_ID = list(range(1, 100 + 1))

reviews = []
user_count = 1
review_count = 1

for restaurant in restaurant_ID:
    for _ in range(50):
        data = {
            'ReviewID': review_count,
            'UserID': user_count,
            'RestaurantID': restaurant,
            'Username': (fake.first_name() + fake.last_name()),
            'Date_of_Review': (fake.date()),
            'Date_of_Visit': (fake.date()),
            'Rating': (round(random.uniform(1, 5))),
            'Review': (fake.paragraph(nb_sentences=5))
        }
        reviews.append(data)
        review_count += 1
        user_count += 1

df = pd.DataFrame(reviews)

df.to_json("CustomerReviews.json", orient='records')
