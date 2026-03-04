# 🚀 FastHTML Python Web Development Tutorial

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Framework](https://img.shields.io/badge/framework-FastHTML-green)
![Status](https://img.shields.io/badge/status-learning%20project-orange)
![License](https://img.shields.io/badge/license-educational-lightgrey)

A hands-on tutorial demonstrating how to build a simple API using **FastHTML**, a modern Python web framework introduced in 2024.

---

## 📌 Overview

Python provides several powerful web frameworks:

- Django
- Flask
- FastAPI
- FastHTML

Most frameworks share common concepts:

- Routing URLs to functions
- Request handling
- Middleware
- Template rendering

Once you learn one framework, transitioning to others becomes easy.

This project introduces FastHTML by building a simple API step-by-step.

---

## 🧱 Project Structure

```
project/
│
├── index.py           # Main application
├── src/
│   └── queries.py     # Database queries
├── requirements.txt
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.x installed
- pip package manager
- Basic Python knowledge
- Familiarity with APIs (helpful but not required)

---

## 📦 Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd <project-folder>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the server:

```bash
python index.py
```

A local URL will be displayed in the terminal:

```
http://0.0.0.0:5001
```

---

## 🔥 Creating Your First Endpoint

```python
from fasthtml.common import *

app = FastHTML()

@app.route("/")
def get():
    return "Hello World!"
```

Visit:

```
http://0.0.0.0:5001/
```

---

## 📡 Testing with Requests

```python
from requests import get

url = "http://0.0.0.0:5001"

get(url + "/").text
# "Hello World!"
```

---

## 📊 Returning JSON Data

Example endpoint returning JSON:

```python
@app.route("/speakers")
def get():
    from src import queries

    df = queries.speakers()
    json = df.to_dict(orient='records')

    return JSONResponse(json)
```

Request JSON data:

```python
get(url + "/speakers").json()
```

Example output:

```
[{"id": 1, "text": "SAMPSON"}, ...]
```

---

## 🧠 Key Concepts Covered

- FastHTML routing
- API endpoint creation
- Running local servers
- Sending HTTP requests
- Returning JSON responses

---

## ⚠️ Important Notes

Before restarting the application:

Stop any running server:

```bash
Ctrl + C
```

Otherwise you may need to restart your workspace.

---

## 📚 Learning Goals

- Understand similarities across Python web frameworks
- Learn API fundamentals
- Gain hands-on experience with FastHTML

---

## 📄 License

Educational use only.