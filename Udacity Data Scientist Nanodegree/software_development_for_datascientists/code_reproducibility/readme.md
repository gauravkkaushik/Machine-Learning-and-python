#  Tutorial: Mastering Python Virtual Environments

This project is a practical guide to **Code Reproducibility**, developed as part of the **Udacity Data Scientist Nanodegree**. You will learn why virtual environments are the industry standard and how to manage them on Windows.

---

##  Table of Contents
1. [What is a Virtual Environment?](#1-what-is-a-virtual-environment)
2. [Why Use Environments?](#2-why-use-environments)
3. [Step-by-Step Setup](#3-step-by-step-setup)
4. [Windows Troubleshooting](#4-windows-troubleshooting)
5. [Summary of Environments](#5-summary-of-environments)

---

## 1. What is a Virtual Environment?

A **Virtual Environment (venv)** is an isolated "sandbox" for your Python projects. 

Imagine you have two different recipes. One requires a wood-fire oven, and the other requires a microwave. If you only have one kitchen (your global Python installation), you can't easily switch between the two. A `venv` gives you a dedicated kitchen for every recipe, containing only the specific tools (libraries) that the recipe needs to succeed.



---

## 2. Why Use Environments?

In Data Science, environments are essential for:
* **Avoiding Version Conflicts:** One project might need `Pandas 1.0`, while another needs `Pandas 2.0`. Environments allow both to exist on the same computer.
* **Reproducibility:** By using a `requirements.txt` file, anyone else can recreate your exact setup with one command.
* **Cleanliness:** It prevents your main computer from being cluttered with hundreds of experimental packages.

---

## 3. Step-by-Step Setup

In this project, we separate the **Art** logic from the **Quotes** logic to keep our dependencies lean.

###  Part A: The Art Environment (`art_env`)
Used for `art.py`. Focuses on image processing and visualization.

1.  **Navigate to the project:**
    ```powershell
    cd "C:\Users\gaura\OneDrive\Documents\GitHub\Machine-Learning-and-python\Udacity Data Scientist Nanodegree\software_development_for_datascientists\code_reproducibility\"
    ```
2.  **Create the environment:**
    ```powershell
    python -m venv art_env
    ```
3.  **Activate it:**
    ```powershell
    .\art_env\Scripts\activate
    ```
4.  **Install tools:**
    ```powershell
    pip install -r requirements_art.txt
    ```



---

### 💬 Part B: The Quotes Environment (`quotes_env`)
Used for `quotes.py`. Focuses on web scraping and text data.

1.  **Deactivate the current environment:**
    ```powershell
    deactivate
    ```
2.  **Create and Activate:**
    ```powershell
    python -m venv quotes_env
    .\quotes_env\Scripts\activate
    ```
3.  **Install tools:**
    ```powershell
    pip install -r requirements_quotes.txt
    ```

---

## 4. Windows Troubleshooting

Working in PowerShell on Windows has specific rules. Here is how to fix common errors:

### "Positional parameter cannot be found"
**The Cause:** You used a folder path with spaces (like `Udacity Data Scientist`) without quotes.
**The Fix:** Always wrap your path in double quotes: 
`cd "C:\Path With Spaces\Project"`

### "Source is not recognized"
**The Cause:** `source` is a Linux/Mac command. 
**The Fix:** On Windows, use the direct path to the script: 
`.\art_env\Scripts\activate`

### "Scripts are disabled on this system"
**The Cause:** PowerShell's security policy.
**The Fix:** Run this once to allow local scripts to run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process