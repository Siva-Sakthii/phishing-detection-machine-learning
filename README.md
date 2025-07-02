# Phishing Detection using Machine Learning 🛡️

A practical project to detect phishing websites using a custom dataset and multiple machine learning models.  

---

## 🎯 Objective

Identify phishing websites by extracting rich URL and page-content features and training several ML models. Evaluate and compare their performance to determine the most effective approach.  

---

## 📁 Repository Structure

```text
.
├── DataFiles/  
│   ├── phishing_final.csv  
│   ├── legitimate_final.csv  
│   ├── raw_benign_url.csv  
│   └── url_data.csv  # Extracted features (16 total)
├── URLFeatureExtraction.py        # Script for feature extraction
├── URL Feature Extraction.ipynb   # Colab notebook for feature exploration
├── Phishing Website Detection_Models & Training.ipynb  # Model training notebook
├── XGBoostClassifier.pickle.dat   # Best-performing model
├── app.py                         # Flask app for URL prediction
├── templates/index.html           # Web UI for prediction
├── requirements.txt
└── .gitignore
```
---

## 🧪Data Collection
- Phishing URLs: 5,000 samples from [PhishTank].  

- Legitimate URLs: 5,000 samples from UNB’s 2016 dataset.  

- Merged and processed into url_data.csv containing 16 distinct URL and webpage-based features  

--- 

## 🔧 Feature Extraction
Features are grouped as:  
- Address-bar based (e.g., length, @, //, etc.)

- Domain-based (e.g., age, subdomain count)

- HTML/JS-based (e.g., presence of <iframe>, suspicious JS patterns)

Explore the extraction pipeline and details in [URL Feature Extraction.ipynb](./"URL Feature Extraction.ipynb") and URLFeatureExtraction.py

---

## 🧠 Models & Training
Train/Test Split: 80/20 (8,000 train, 2,000 test)  

Algorithms Trained:
- Decision Tree
- Random Forest
- Multilayer Perceptron (MLP)
- XGBoost
- Support Vector Machine (SVM)

All model training and evaluation steps are documented in [Phishing Website Detection_Models & Training.ipynb](./"Phishing Website Detection_Models & Training.ipynb")

---

## 📊 Results
Best Performer: XGBoost (86.4% accuracy)  

The trained XGBoost model is saved in XGBoostClassifier.pkl for easy deployment   

---

## 🚀 How to Run
### Project Setup

```
git clone https://github.com/Siva-Sakthii/phishing-detection-machine-learning.git
cd phishing-detection-machine-learning
pip install -r requirements.txt
```
### Feature Extraction (if using raw CSVs)  

- URLFeatureExtraction.ipynb

### Training / Evaluation  
Launch the Jupyter notebook: 
jupyter notebook "Phishing Website Detection_Models & Training.ipynb"

### Web App Deployment
Run the Flask app:  
```
python app.py
```
Visit http://127.0.0.1:5000/ in your browser to test URL predictions.  
---

## 🚧 Future Work  
🎯 Develop a browser extension (e.g., Chrome/Firefox) to check URLs in-browser.  

🖥️ Build a GUI (desktop/web) for broader accessibility.  

⚙️ Explore live-data crawling and real-time detection pipelines.  

--- 

## 📄 References & Resources
PhishTank, UNB datasets, and UCI Phishing Website repository   
--- 

## ❤️ Acknowledgements
Thanks to:
PhishTank & UNB for datasets
Open-source community (e.g., scikit-learn, XGBoost, Flask)
Sri Shakthi Institute of Engineering and Technology for project support