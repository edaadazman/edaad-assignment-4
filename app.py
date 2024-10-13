from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

app = Flask(__name__)


# TODO: Fetch dataset, initialize vectorizer and LSA here

# Fetch the dataset
newsgroups = fetch_20newsgroups(subset="all")
documents = newsgroups.data

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words=stopwords.words("english"), max_features=5000)
X = vectorizer.fit_transform(documents)

# Apply SVD to reduce dimensionality (LSA)
svd = TruncatedSVD(n_components=100)  # Adjust the number of components as needed
X_reduced = svd.fit_transform(X)


def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    try:
        # Transform the query using the same vectorizer and SVD
        query_vector = vectorizer.transform([query])
        query_reduced = svd.transform(query_vector)

        # Compute cosine similarities between the query and all documents
        similarities = cosine_similarity(query_reduced, X_reduced)[0]

        # Get the top 5 most similar documents
        top_indices = np.argsort(similarities)[-5:][::-1]  # Indices of top 5 documents
        top_similarities = similarities[top_indices]

        # Convert NumPy arrays to Python lists
        return (
            [documents[i] for i in top_indices],
            top_similarities.tolist(),
            top_indices.tolist(),
        )

    except Exception as e:
        print(f"Error during search: {e}")
        return [], [], []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form["query"]
    documents, similarities, indices = search_engine(query)
    return jsonify(
        {"documents": documents, "similarities": similarities, "indices": indices}
    )


if __name__ == "__main__":
    app.run(debug=True)
