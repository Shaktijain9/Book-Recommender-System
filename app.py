from flask import Flask
from flask import render_template
import pickle

popular_df = pickle.load(open('top_50.pkl', 'rb'))
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Votes'].values),
                           rating=list(popular_df['Average Rating'].values))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
