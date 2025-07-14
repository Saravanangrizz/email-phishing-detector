from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import torch
import numpy as np

from transformers import DistilBertTokenizer, DistilBertModel

app = Flask(__name__)
CORS(app)

clf = joblib.load('model/phishing_model.pkl')
tokenizer = joblib.load('model/tokenizer.pkl')
bert = joblib.load('model/bert_model.pkl')

suspicious_keywords = ['verify', 'account', 'login', 'urgent', 'click', 'password', 'bank']

def prepare_features(text, from_domain, reply_domain):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        emb = bert(**inputs).last_hidden_state[:, 0, :].numpy()
    dm = int(from_domain == reply_domain)
    return np.hstack((emb, [[dm]]))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('email', '')
    from_d = data.get('from', '')
    reply_d = data.get('reply_to', '')
    features = prepare_features(text, from_d, reply_d)
    proba = clf.predict_proba(features)[0]
    pred = clf.predict(features)[0]
    confidence = round(max(proba) * 100, 2)
    
    found = [k for k in suspicious_keywords if k in text.lower()]
    explanation = found if pred == 1 else []

    return jsonify({
        'prediction': 'Phishing' if pred == 1 else 'Legit',
        'confidence': confidence,
        'explanation': explanation
    })

if __name__ == '__main__':
    app.run(debug=True)
