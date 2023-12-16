from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from transformers import pipeline
from fileinput import filename 
import io
import csv

csv.field_size_limit(100000000)

app = Flask(__name__)
CORS(app)

#Commeting out as Transformer models were giving better results compared to Naive Bayes and SVM
# Load the dataset
#df = pd.read_csv('student_feedback.csv', encoding="ISO-8859-1")
#X = df['comment']
#y = df['quality']

# Split the dataset into training and testing sets
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Naive Bayes model
#nb_model = MultinomialNB()
#nb_vectorizer = CountVectorizer()
#X_train_nb = nb_vectorizer.fit_transform(X_train)
#nb_model.fit(X_train_nb, y_train)

# Train SVM model
#svm_model = SVC(probability=True)
#svm_vectorizer = CountVectorizer()
#X_train_svm = svm_vectorizer.fit_transform(X_train)
#svm_model.fit(X_train_svm, y_train)

# Create a BERT sentiment analysis pipeline
bert_model = pipeline("sentiment-analysis")
bert_summarizer = pipeline("summarization")

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        file = request.files['file']  
        if not file:
            return "No file"

        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        csv_length = 0
        positive_prediction = []
        negative_prediction = []
        neutral_prediction = []
        #print(csv_input)
        for row in csv_input:
            #print(row)
            row_value = row[0]
            csv_length+=1
            bert_prediction = bert_model(row_value)[0]['label']
            if bert_prediction == 'POSITIVE':
                 positive_prediction.append(row_value)
            elif bert_prediction == 'NEGATIVE':
                 negative_prediction.append(row_value)
            else:
                 neutral_prediction.append(row_value)
        pos_score = len(positive_prediction)/csv_length
        neg_score = len(negative_prediction)/csv_length
        neu_score = len(neutral_prediction)/csv_length
        print(pos_score,neg_score,neu_score)

        if pos_score>=neg_score and pos_score>=neu_score:
             result = 'Positive with '+str(pos_score*100)+' score. '
        elif neg_score>=pos_score and  neg_score>=neu_score:
             result = 'Negative with '+str(neg_score*100)+' score '
        else:
             result = 'Neutral with '+str(neu_score*100)+' score '
        summarized_pos_feedback = str(bert_summarizer("\n".join(positive_prediction),min_length=20, max_length=50)[0]['summary_text'])
        summarized_neg_feedback = str(bert_summarizer("\n".join(negative_prediction),min_length=20, max_length=50)[0]['summary_text'])
        response = "The Overall Feedback of course is "+result+"\nSummarized Positive Feedback: "+summarized_pos_feedback+"\nSummarized Negative Feedback: "+summarized_neg_feedback
        print(response)
        return jsonify({'feedback': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
        

if __name__ == '__main__':
    app.run(debug=True)
