from flask import Flask, request, render_template
from urllib.parse import urlparse, quote
import ipaddress
import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import whois
import pickle
from urllib.error import URLError
from urllib.request import urlopen

app = Flask(__name__)

# Load the trained model
with open('XGBoostClassifier.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the URL feature extraction functions
def havingIP(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip

def haveAtSign(url):
    return 1 if "@" in url else 0

def getLength(url):
    return 0 if len(url) < 54 else 1

def getDepth(url):
    s = urlparse(url).path.split('/')
    depth = 0
    for j in range(len(s)):
        if len(s[j]) != 0:
            depth = depth + 1
    return depth

def redirection(url):
    pos = url.rfind('//')
    return 1 if pos > 6 else 0

def httpDomain(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else 0

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
def tinyURL(url):
    return 1 if re.search(shortening_services, url) else 0

def prefixSuffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

import requests
def web_traffic(url):
    try:
        similarweb_api_url = f"https://api.similarweb.com/v1/website/{url}/total-traffic-and-engagement/visits"
        headers = {
            'Authorization': 'Bearer SimilarWebApp_API_Key'
        }
        response = requests.get(similarweb_api_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        visits = data.get('visits', 0)
        return visits
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return 0

def get_single_date(date):
    if isinstance(date, list):
        return date[0]
    return date

def domainAge(domain_name):
    creation_date = get_single_date(domain_name.creation_date)
    expiration_date = get_single_date(domain_name.expiration_date)
    if isinstance(creation_date, str) or isinstance(expiration_date, str):
        try:
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if not creation_date or not expiration_date:
        return 1
    ageofdomain = abs((expiration_date - creation_date).days)
    return 1 if (ageofdomain / 30) < 6 else 0

def domainEnd(domain_name):
    expiration_date = get_single_date(domain_name.expiration_date)
    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if not expiration_date:
        return 1
    today = datetime.now()
    end = abs((expiration_date - today).days)
    return 0 if (end / 30) < 6 else 1


def iframe(response):
    return 1 if not response or re.findall(r"[<iframe>|<frameBorder>]", response.text) else 0

def mouseOver(response):
    return 1 if not response or re.findall("<script>.+onmouseover.+</script>", response.text) else 0

def rightClick(response):
    return 1 if not response or re.findall(r"event.button ?== ?2", response.text) else 0

def forwarding(response):
    return 1 if not response or len(response.history) <= 2 else 0

# Function to extract features
def featureExtraction(url):
    features = []
    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(getLength(url))
    features.append(getDepth(url))
    features.append(redirection(url))
    features.append(httpDomain(url))
    features.append(tinyURL(url))
    features.append(prefixSuffix(url))
    
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    features.append(web_traffic(url))
    features.append(1 if dns == 1 else domainAge(domain_name))
    features.append(1 if dns == 1 else domainEnd(domain_name))
    
    try:
        response = requests.get(url)
    except:
        response = ""

    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))
    
    return features

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        url = request.form['url']
        features = featureExtraction(url)
        prediction = model.predict([features])[0]
        print(features)
        print(prediction)
        lst = []
        t1 = features[-1]
        t2 = features[-2]
        t3 = features[-3]
        if t1 and t2 and t3:
            lst.append(t1)
            lst.append(t2)
            lst.append(t3)
        prediction = 'Phishing Website' if len(lst) == 3 else 'Legitimate'
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
