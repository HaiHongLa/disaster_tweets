# Twitter Disaster Detector
A Flask API that detects disasters from news tweets on Twitter and save them in a Google Sheet document.

### Requirements
- Flask==2.0.2
- Flask-RESTful==0.3.9
- pandas==1.3.5
- pygsheets==2.0.5
- scikit-learn==1.0.2
- scipy==1.7.3
- tweepy==4.4.0
- numpy==1.22.0
- pandas==1.3.5
- A Google API service file
- A Twitter API account and token
### API query

/scrape-tweets
  
### The classifier
The app uses Sklearn's TFIDF Vectorizer and Support Vector Machine algorithm to classify tweets
