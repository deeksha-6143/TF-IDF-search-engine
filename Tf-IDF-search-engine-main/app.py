from flask import Flask, render_template, request
from preprocess import preprocess
from tfidf import compute_tf, compute_idf, compute_tfidf
from search import cosine_similarity

app = Flask(__name__)

# Load docs
with open("data/docs.txt", "r") as f:
    raw_docs = [line.strip() for line in f.readlines()]

processed_docs = [preprocess(doc) for doc in raw_docs]

idf = compute_idf(processed_docs)

doc_vectors = []
for doc in processed_docs:
    tf = compute_tf(doc)
    doc_vectors.append(compute_tfidf(tf, idf))


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form["query"]

        tokens = preprocess(query)
        query_tf = compute_tf(tokens)
        query_vec = compute_tfidf(query_tf, idf)

        scores = []
        for i, doc_vec in enumerate(doc_vectors):
            score = cosine_similarity(query_vec, doc_vec)
            scores.append((raw_docs[i], score))

        scores.sort(key=lambda x: x[1], reverse=True)

        # Filter non-zero results
        results = [r for r in scores if r[1] > 0][:5]

    return render_template("index.html", results=results, query=query)


if __name__ == "__main__":
    app.run(debug=True, port=5000)