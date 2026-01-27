# Predicting Software Developer Salaries: A Data-Driven Approach

## Project Overview
This project is part of the **Udacity Data Scientist Nanodegree**. It utilizes the **2023 Stack Overflow Developer Survey** to explore the factors that influence software developer compensation globally. Using the **CRISP-DM** (Cross-Industry Standard Process for Data Mining) methodology, I performed extensive data cleaning, feature engineering, and predictive modeling.



## Blog Post
A write-up of the findings and technical approach can be found here: [\[Medium/Blog Link Here\]](https://medium.com/@gaurav.k.kaushik/show-me-the-money-what-truly-drives-developer-salaries-in-2026-c45ae50a2aae?postPublishedType=initial)

---

## Business Questions
Following the CRISP-DM framework, this project seeks to answer:
1. **Experience vs. Salary:** How much does an additional year of professional coding actually add to your bottom line?
2. **The Geography Premium:** Which countries offer the highest purchasing power for developers after controlling for experience?
3. **Skill Breadth:** Does knowing more programming languages (being a "polyglot") lead to a higher salary?
4. **Leadership Impact:** Does decision-making power (Purchase Influence) impact salary more than technical skills?

---

## Tech Stack & Library Requirements
* **Language:** Python 3.x
* **Data Manipulation:** `pandas`, `numpy`
* **Visualization:** `matplotlib`, `seaborn`, `shap`
* **Machine Learning:** `scikit-learn` (Random Forest, GridSearchCV)
* **Explainable AI:** `shap` (SHapley Additive exPlanations)

---

## Project Structure
- `Predicting_Software_Developer_Salaries.ipynb`: The main Google Colab notebook.
- `README.md`: Project documentation and summary.
- `data`: Zip file containing dataset.

---

## Data Preparation & Cleaning
The raw survey data is highly "messy." Key steps included:
* **Target Variable:** Cleaned `ConvertedCompYearly` by removing extreme outliers using the IQR method.
* **Feature Extraction:** Created a `LanguageCount` feature by parsing the multi-select `LanguageHaveWorkedWith` column.
* **Binary Flags:** Engineered `Is_FullTime` and `Is_Contractor` columns to capture employment status nuances.
* **Encoding:** Transformed categorical variables (`Country`, `DevType`, `Industry`) into numerical format using One-Hot Encoding.

---

## Modeling and Evaluation
I trained a **Random Forest Regressor** to capture non-linear relationships in the data.

### Hyperparameter Tuning
I used `GridSearchCV` with **multiprocessing** to optimize:
* `n_estimators`
* `max_depth`
* `min_samples_split`

### Model Performance
* **R² Score:** 0.528
* **Mean Absolute Error (MAE):** $27,264.87


---

## Explainable AI (SHAP Analysis)
To move beyond "Black Box" predictions, I implemented a custom SHAP analysis suite to interpret the model:

1. **Global Importance:** Identified that **YearsCodePro** and **Country (USA)** are the most significant salary drivers.
2. **Beeswarm Plots:** Visualized how high values of experience and specific roles push salary predictions higher.
3. **Partial Dependence Plots (PDP):** Discovered at which year of experience salary growth begins to plateau.
4. **Interaction Analysis:** Explored how the value of experience changes depending on the country of residence.



---

## Key Findings
* **Experience is King:** Years of professional experience remains the most consistent predictor of salary.
* **The Location Multiplier:** Geographic location acts as a massive multiplier; a developer in the US with 5 years of experience often earns more than a developer in other regions with 15 years.
* **Specialization over Generalization:** While knowing 3-5 languages increases salary, the "polyglot" benefit diminishes significantly after 8 languages.

---

## Conclusion
Understanding your market value is about more than just your code. This project demonstrates that while technical skills are the foundation, **geography, industry, and leadership influence** are the true keys to maximizing compensation in the tech industry.

---

## License
This project is for educational purposes as part of the Udacity Nanodegree program. Data is provided by Stack Overflow under the ODbL license.