import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import pickle

# Load Data
def load_data(filepath):
    try:
        df = pd.read_excel(filepath)
        print(f"Data loaded successfully from {filepath}")
        return df
    except Exception as e:
        print(f"Failed to load data from {filepath}: {e}")
        return None

# Preprocess Data
def preprocess_data(poverty_df, unemployed_df):
    combined_df = pd.merge(poverty_df, unemployed_df, on=['Region', 'Source', 'Sex', 'Age', 'Year'], suffixes=('_poverty', '_unemployed'))
    combined_df.dropna(inplace=True)
    combined_df.drop(columns=['Unnamed: 6'], inplace=True)
    
    le = LabelEncoder()
    combined_df['Sex'] = le.fit_transform(combined_df['Sex'])
    combined_df['Age'] = le.fit_transform(combined_df['Age'])
    
    return combined_df

# Modeling and Evaluation
def model_and_evaluate(data):
    X = data[['Sex', 'Age', 'Year', 'Value_unemployed']]
    y = data['Value_poverty']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2, 4]
    }
    model = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    print("Best parameters:", grid_search.best_params_)
    
    y_pred = best_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    print(f'Test RMSE: {rmse}')
    print(f'Test MAE: {mae}')
    
    with open('best_model.pkl', 'wb') as file:
        pickle.dump(best_model, file)
    print("Model saved as 'best_model.pkl'")

    return best_model

# Plot feature importance
def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(10, 5))
    plt.title('Feature Importances')
    plt.bar(range(len(importances)), importances[indices], color='b', align='center')
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
    plt.xlabel('Feature')
    plt.ylabel('Importance')
    plt.show()

# Main function
def main():
    poverty_df = load_data('Poverty.xlsx')
    unemployed_df = load_data('Unemployed.xlsx')
    
    if poverty_df is not None and unemployed_df is not None:
        combined_df = preprocess_data(poverty_df, unemployed_df)
        best_model = model_and_evaluate(combined_df)
        plot_feature_importance(best_model, combined_df.drop('Value_poverty', axis=1).columns)

if __name__ == "__main__":
    main()
