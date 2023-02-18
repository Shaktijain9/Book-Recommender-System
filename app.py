from flask import Flask
from flask import render_template, request
import pickle
import numpy as np
from time import time

popular_df = pickle.load(open('top_50.pkl', 'rb'))
pt = pickle.load(open("pt.pkl", 'rb'))
similarity_score = pickle.load(open("similarity_score.pkl", 'rb'))
books_df = pickle.load(open("books_df.pkl", 'rb'))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html", book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Votes'].values),
                           rating=list(popular_df['Average Rating'].values))


@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend_info():
    user_input = request.form.get('user_input')
    # return user_input

    pos = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[pos])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for value in similar_items:
        item = []
        temp_df = books_df[books_df['Book-Title'] == pt.index[value[0]]]

        author_name = list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
        book_name = list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
        book_image = list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)

        item.extend(author_name)
        item.extend(book_name)
        item.extend(book_image)

        data.append(item)
    return render_template('recommend.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
