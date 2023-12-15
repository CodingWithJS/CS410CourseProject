from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Load the dataset
df = pd.read_csv('student_feedback.csv', encoding="ISO-8859-1")
X = df['comment']
y = df['quality']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Naive Bayes model
nb_model = MultinomialNB()
nb_vectorizer = CountVectorizer()
X_train_nb = nb_vectorizer.fit_transform(X_train)
nb_model.fit(X_train_nb, y_train)

# Train SVM model
svm_model = SVC()
svm_vectorizer = CountVectorizer()
X_train_svm = svm_vectorizer.fit_transform(X_train)
svm_model.fit(X_train_svm, y_train)

# Create a BERT sentiment analysis pipeline
bert_model = pipeline("sentiment-analysis", model="bert-base-uncased")

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        review = data.get('review', '')

        if not review.strip():
            raise ValueError('Review cannot be empty.')

        # Naive Bayes prediction
        X_review_nb = nb_vectorizer.transform([review])
        nb_prediction = nb_model.predict(X_review_nb)[0]

        # SVM prediction
        X_review_svm = svm_vectorizer.transform([review])
        svm_prediction = svm_model.predict(X_review_svm)[0]

        # BERT prediction
        bert_prediction = bert_model(review)[0]['label']

        # Provide feedback based on the majority vote
        predictions = [nb_prediction, svm_prediction, bert_prediction]
        majority_vote = max(set(predictions), key=predictions.count)

        feedback = {'label': majority_vote}
        return jsonify({'feedback': feedback})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
#Uncomment below lines to run in local
#if __name__ == '__main__':
#    app.run(debug=True)
