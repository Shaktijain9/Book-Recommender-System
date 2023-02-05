import pandas as pd
import json
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://m001-student:tGxrhF35TSNT87dr@sandbox.b27ar.mongodb.net/?retryWrites=true&w=majority")

DATABASE_NAME = "book-recommendation"
COLLECTION_NAME_BOOKS = "books"
COLLECTION_NAME_USER = "users"
COLLECTION_NAME_RATING = "ratings"
BOOK_FILE_NAME = "Books.csv"
RATINGS_FILE_NAME = "Ratings.csv"
USERS_FILE_NAME = "Users.csv"


book_df = pd.read_csv(BOOK_FILE_NAME)
ratings_df = pd.read_csv(RATINGS_FILE_NAME)
user_df = pd.read_csv(USERS_FILE_NAME)

df_list = [book_df, ratings_df, user_df]

# Creation of json records from data-frames
for df in df_list:
    df.reset_index(drop=True, inplace=True)

books_json_record = list(json.loads(book_df.T.to_json()).values())
users_json_record = list(json.loads(user_df.T.to_json()).values())
ratings_json_record = list(json.loads(ratings_df.T.to_json()).values())

# Insertion of json records
db = client[DATABASE_NAME]
collection_books = db[COLLECTION_NAME_BOOKS]
collection_user = db[COLLECTION_NAME_USER]
collection_rating = db[COLLECTION_NAME_RATING]

print("Insertion of Book records")
collection_books.insert_many(books_json_record)
print("Insertion of User records")
collection_user.insert_many(users_json_record)
print("Insertion of Rating records")
collection_rating.insert_many(ratings_json_record)

print("Records Insertion Complete!!")
