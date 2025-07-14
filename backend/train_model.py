import pandas as pd
import numpy as np
import joblib

from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Load and preprocess data
df = pd.read_csv('data/emails.csv')  # expects 'text','label','from','reply_to'

# Header features
df['from_domain'] = df['from'].str.split('@').str[-1].fillna('')
df['reply_domain'] = df['reply_to'].str.split('@').str[-1].fillna('')
df['domain_match'] = (df['from_domain'] == df['reply_domain']).astype(int)

# Load BERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
bert = DistilBertModel.from_pretrained('distilbert-base-uncased')

def get_embeddings(texts):
    inputs = tokenizer(texts.tolist(), return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = bert(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

X_embeds = get_embeddings(df['text'])
X_headers = df['domain_match'].values.reshape(-1, 1)
X = np.hstack([X_embeds, X_headers])
y = df['label']

# Handle imbalance
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)

# Train classifier with class weights
clf = RandomForestClassifier(class_weight='balanced', n_estimators=100, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)
print(classification_report(y_test, clf.predict(X_test)))

# Persist artifacts
joblib.dump(clf, 'model/phishing_model.pkl')
joblib.dump(tokenizer, 'model/tokenizer.pkl')
joblib.dump(bert, 'model/bert_model.pkl')
