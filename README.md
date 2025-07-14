🛡️ Phishing Email Detection Web App

A full-stack cybersecurity project that detects phishing emails using NLP-based machine learning, built with:

🔥 Flask (Python backend)

🧠 BERT (DistilBERT) embeddings for text understanding

🌐 React + Tailwind CSS frontend

🚀 Deployed using Render




🎯 Objective

Detect phishing emails based on their content and header details, and help users understand why an email is flagged as phishing using natural language processing and keyword analysis.




✅ Features

🔍 Email Detection (Backend)

->Uses BERT (DistilBERT) to convert email content into contextual embeddings

->Trained with a RandomForestClassifier to classify emails as:

->Phishing

->Legit

->Supports email header inputs (From, Reply-To) to analyze spoofing

->Handles imbalanced datasets using SMOTE or class_weight='balanced'




📈 Prediction Output Displays:

->Prediction result (Phishing or Legit)

->Confidence score (e.g., "Phishing - 91.4% confident")

->Explanation of suspicious content (keywords, mismatch headers)




🌐 Deployment

->Backend deployed on Render Web Service (gunicorn + Flask)

->Frontend deployed on Render Static Site (React build)

->Managed via a single render.yaml (monorepo structure)



📁 Tech Stack

| Layer      | Technology                                      |
| ---------- | ----------------------------------------------- |
| Frontend   | React, Tailwind CSS                             |
| Backend    | Flask, Gunicorn, CORS                           |
| ML/NLP     | `transformers`, BERT, sklearn, imbalanced-learn |
| Model      | RandomForestClassifier with BERT embeddings     |
| Deployment | Render                                          |
 

