import shap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

def generate_full_shap_analysis(model, X_train, X_test, features_to_plot=None, num_top_features=3):
    """
    Comprehensive SHAP analysis function with labeled summary bar plots.
    """
    start_time = time.time()

    # Ensure X_train and X_test are float types
    X_train_numeric = X_train.astype(float)
    X_test_numeric = X_test.astype(float)

    print("--- STEP 1: INITIALIZING SHAP EXPLAINER ---")
    explainer = shap.TreeExplainer(model)

    print("--- STEP 2: CALCULATING SHAP VALUES (This may take a moment...) ---")
    shap_values = explainer.shap_values(X_test_numeric)

    if isinstance(shap_values, list): shap_values_to_plot = shap_values[1]
    elif len(shap_values.shape) == 3: shap_values_to_plot = shap_values[:, :, 1]
    else: shap_values_to_plot = shap_values

    if features_to_plot is None:
        mean_abs_shap = np.mean(np.abs(shap_values_to_plot), axis=0)
        importance_df = pd.DataFrame({'feature': X_test_numeric.columns, 'importance': mean_abs_shap})
        features_to_plot = importance_df.sort_values('importance', ascending=False).head(num_top_features)['feature'].tolist()
        print(f">> Mode: Auto-detecting top {num_top_features} features: {features_to_plot}")
    else:
        print(f">> Mode: Analyzing user-specified features: {features_to_plot}")

    # --- GLOBAL PLOTS ---
    print("\n--- STEP 3: GENERATING GLOBAL SUMMARY BAR PLOT ---")
    plt.figure(figsize=(10, 5))
    
    # 1. Generate the plot (show=False is critical)
    shap.summary_plot(shap_values_to_plot, X_test_numeric, plot_type="bar", show=False)
    
    # 2. Get the current axes BEFORE plt.show()
    ax = plt.gca()
    
    # 3. Add labels to the containers
    for container in ax.containers:
        # fmt='%.0f' rounds to the nearest dollar/unit for readability
        ax.bar_label(container, fmt='%.0f', padding=5)
    
    plt.title("Global Feature Importance (Mean |SHAP Value|)", fontsize=14, pad=15)
    plt.show() # Now show the labeled plot

    

    print("--- STEP 4: GENERATING GLOBAL BEESWARM PLOT ---")
    plt.figure(figsize=(10, 5))
    shap.summary_plot(shap_values_to_plot, X_test_numeric, show=False)
    plt.title("Feature Impact Distribution (Beeswarm)", fontsize=14, pad=15)
    plt.show()

    # --- ITERATIVE DEPENDENCE & PDP ---
    total_feats = len(features_to_plot)
    print(f"\n--- STEP 5: STARTING ITERATIVE ANALYSIS FOR {total_feats} FEATURES ---")

    for i, feature in enumerate(features_to_plot, 1):
        print(f"[{i}/{total_feats}] Processing feature: '{feature}'...")

        if feature not in X_test_numeric.columns:
            print(f"    ! Warning: Feature '{feature}' not found. Skipping.")
            continue

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

        # 1. Dependence Plot
        shap.dependence_plot(feature, shap_values_to_plot, X_test_numeric, ax=ax1, show=False)
        ax1.set_title(f"Interaction Plot: {feature}")

        # 2. Partial Dependence Plot
        shap.partial_dependence_plot(
            feature,
            model.predict,
            X_train_numeric,
            model_expected_value=True,
            feature_expected_value=True,
            show=False,
            ice=False,
            ax=ax2
        )
        ax2.set_title(f"Average Partial Dependence: {feature}")

        plt.tight_layout()
        plt.show()

    end_time = time.time()
    print(f"\n--- SHAP ANALYSIS COMPLETE (Total Time: {end_time - start_time:.2f} seconds) ---")

# --- EXAMPLES OF HOW TO USE ---

# Option A: Let the function pick the Top 3
generate_full_shap_analysis(best_rf_model, X_train, X_test, num_top_features=5)

# Option B: You choose specific features (e.g., RemoteWork and LanguageCount)
# generate_full_shap_analysis(best_rf_model, X_train, X_test, features_to_plot=['RemoteWork', 'LanguageCount'])