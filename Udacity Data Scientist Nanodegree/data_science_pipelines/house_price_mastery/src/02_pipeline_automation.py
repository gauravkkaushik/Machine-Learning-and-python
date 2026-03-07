import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import warnings
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.metrics import mean_absolute_error

# Advanced Interpretability
from pdpbox import pdp

warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# 1. SETUP DIRECTORIES & DATA LOADING
# ---------------------------------------------------------
PATHS = {
    "data": "./Udacity Data Scientist Nanodegree/data_science_pipelines/house_price_mastery/data/train.csv",
    "models": "./Udacity Data Scientist Nanodegree/data_science_pipelines/house_price_mastery/models/",
    "output": "./Udacity Data Scientist Nanodegree/data_science_pipelines/house_price_mastery/output/plots/"
}

for path in [PATHS["models"], PATHS["output"]]:
    os.makedirs(path, exist_ok=True)

def load_and_clean_data(path):
    df = pd.read_csv(path)
    df = df.drop(df[(df['GrLivArea'] > 4000) & (df['SalePrice'] < 300000)].index)
    return df

train = load_and_clean_data(PATHS["data"])

num_features = ['OverallQual', 'GrLivArea', 'TotalBsmtSF', '1stFlrSF', 'LotFrontage', 'YearBuilt']
cat_features = ['Neighborhood', 'ExterQual', 'KitchenQual']

X = train[num_features + cat_features]
y = train['SalePrice']

# ---------------------------------------------------------
# 2. PIPELINE ARCHITECTURE (FeatureUnion)
# ---------------------------------------------------------


num_engineering = FeatureUnion([
    ('standard', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])),
    ('interactions', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('poly', PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)),
        ('scaler', StandardScaler())
    ]))
])

cat_engineering = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer([
    ('num_rich', num_engineering, num_features),
    ('cat', cat_engineering, cat_features)
])

# ---------------------------------------------------------
# 3. MODEL TUNING
# ---------------------------------------------------------
xgb = XGBRegressor(random_state=42, objective='reg:squarederror', n_jobs=-1)

model_wrapper = TransformedTargetRegressor(
    regressor=xgb,
    func=np.log1p,
    inverse_func=np.expm1
)

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model_wrapper)
])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

param_distributions = {
    'model__regressor__n_estimators': [800, 1000, 1500],
    'model__regressor__learning_rate': [0.01, 0.05],
    'model__regressor__max_depth': [3, 5, 7],
    'model__regressor__subsample': [0.8, 0.9],
    'model__regressor__colsample_bytree': [0.7, 0.8, 0.9]
}

print("Executing Randomized Search CV...")
search = RandomizedSearchCV(
    full_pipeline, 
    param_distributions=param_distributions, 
    n_iter=15, 
    cv=5, 
    scoring='neg_mean_absolute_error',
    verbose=1, random_state=42
)

search.fit(X_train, y_train)
best_model = search.best_estimator_

# ---------------------------------------------------------
# 4. FEATURE NAMES & IMPORTANCE
# ---------------------------------------------------------
num_names = best_model.named_steps['preprocessor'].named_transformers_['num_rich'].get_feature_names_out()
cat_names = best_model.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out()
all_features = list(num_names) + list(cat_names)

importances = best_model.named_steps['model'].regressor_.feature_importances_
feat_imp = pd.Series(importances, index=all_features).sort_values(ascending=False)

# Save Importance Plot
plt.figure(figsize=(10, 8))
feat_imp.head(20).plot(kind='barh', color='teal')
plt.title("Top 20 Features (Including Quality Interactions)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(PATHS["output"], "feature_importance.png"))
plt.close()

# ---------------------------------------------------------
# 5. PDPBOX VISUALIZATION (Fixing n_classes error)
# ---------------------------------------------------------


print("Generating PDPbox plots for top 20 features...")

# 1. Transform the training data for the plotter
X_train_transformed = best_model.named_steps['preprocessor'].transform(X_train)
X_train_df = pd.DataFrame(X_train_transformed, columns=all_features)

# 2. Extract the underlying regressor (XGBoost) from the Target Wrapper
raw_model = best_model.named_steps['model'].regressor_

# 3. Iterate through top 20 features
for feature in feat_imp.head(20).index:
    try:
        # Use the high-level pdp_isolate function
        pdp_isolate_obj = pdp.pdp_isolate(
            model=raw_model,
            dataset=X_train_df,
            model_features=all_features,
            feature=feature
        )
        
        # 
        fig, axes = pdp.pdp_plot(
            pdp_isolate_out=pdp_isolate_obj, 
            feature_name=feature,
            plot_pts_dist=True,
            cluster=True,
            n_cluster_centers=10
        )
        
        # Save to output folder
        plt.savefig(os.path.join(PATHS["output"], f"pdp_{feature.replace(' ', '_')}.png"))
        plt.close()
        
    except Exception as e:
        print(f"Skipping PDP for {feature}: {e}")

# ---------------------------------------------------------
# 6. SAVE MODEL
# ---------------------------------------------------------
joblib.dump(best_model, os.path.join(PATHS["models"], "house_price_production_pipeline.pkl"))
print(f"Workflow Complete. Validation MAE: ${mean_absolute_error(y_val, best_model.predict(X_val)):,.2f}")