import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the data
df = pd.read_csv('D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_copy.csv')

# Convert date to datetime format
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# Check data
print(f"Dataset shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check distribution of target variable
print("\nDistribution of market_label:")
print(df['market_label'].value_counts())

# Check values of tone
print("\nUnique values in tone:")
print(df['tone'].unique())

# Check statistics of tone
print("\nStatistics of tone:")
print(df['tone'].describe())

# Define features and target
X = df[['tone']]
y = df['market_label']

# 1. Time-based split (January 1, 2024 as cutoff)
cutoff_date = pd.to_datetime('2024-01-01')
train_time = df[df['date'] < cutoff_date]
test_time = df[df['date'] >= cutoff_date]

X_train_time = train_time[['tone']]
y_train_time = train_time['market_label']
X_test_time = test_time[['tone']]
y_test_time = test_time['market_label']

print(f"\nTime-based split - Training set: {len(X_train_time)}, Test set: {len(X_test_time)}")

# 2. Random split (90% train, 10% test)
X_train_random, X_test_random, y_train_random, y_test_random = train_test_split(
    X, y, test_size=0.1, random_state=42
)

print(f"Random split - Training set: {len(X_train_random)}, Test set: {len(X_test_random)}")

# Create function to evaluate and visualize model performance
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name, split_type):
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Print metrics
    print(f"\n{model_name} - {split_type} Split Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Create confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Visualize confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=sorted(np.unique(y_test)), 
                yticklabels=sorted(np.unique(y_test)))
    plt.title(f'Confusion Matrix - {model_name} ({split_type} Split)')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(f'confusion_matrix_{model_name}_{split_type}.png')
    plt.close()
    
    # Visualize the relationship between tone and market_label
    plt.figure(figsize=(10, 6))
    
    # Get decision boundary
    if model_name == 'SVM':
        # For a 1D feature, we can simply plot decision function values
        tone_range = np.linspace(min(X['tone']), max(X['tone']), 100).reshape(-1, 1)
        decision_vals = model.decision_function(tone_range)
        
        plt.plot(tone_range, decision_vals, 'k-', label='Decision Boundary')
    
    # Plot actual data points
    for label in sorted(np.unique(y_test)):
        indices = y_test == label
        plt.scatter(X_test.iloc[indices]['tone'], 
                    [label] * sum(indices), 
                    label=f'Actual {label}', 
                    alpha=0.6)
    
    # Plot predictions
    plt.scatter(X_test['tone'], y_pred, marker='x', color='red', label='Predictions', alpha=0.4)
    
    plt.title(f'Tone vs Market Label - {model_name} ({split_type} Split)')
    plt.xlabel('Tone')
    plt.ylabel('Market Label')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'prediction_plot_{model_name}_{split_type}.png')
    plt.close()
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# Initialize models
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
svm_model = SVC(kernel='rbf', C=1.0, random_state=42)

# Evaluate models with time-based split
rf_time_metrics = evaluate_model(rf_model, X_train_time, X_test_time, y_train_time, y_test_time, 
                                "Random Forest", "Time")
svm_time_metrics = evaluate_model(svm_model, X_train_time, X_test_time, y_train_time, y_test_time, 
                                 "SVM", "Time")

# Evaluate models with random split
rf_random_metrics = evaluate_model(rf_model, X_train_random, X_test_random, y_train_random, y_test_random, 
                                  "Random Forest", "Random")
svm_random_metrics = evaluate_model(svm_model, X_train_random, X_test_random, y_train_random, y_test_random, 
                                   "SVM", "Random")

# Compare all models and splits
models = ['Random Forest (Time)', 'SVM (Time)', 'Random Forest (Random)', 'SVM (Random)']
metrics = [rf_time_metrics, svm_time_metrics, rf_random_metrics, svm_random_metrics]

# Create comparison table
comparison_df = pd.DataFrame(metrics, index=models)
print("\nModel Comparison:")
print(comparison_df)

# Visualize model comparison
plt.figure(figsize=(12, 8))
comparison_df.plot(kind='bar', figsize=(12, 8))
plt.title('Model Performance Comparison')
plt.xlabel('Model')
plt.ylabel('Score')
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Metric')
plt.tight_layout()
plt.savefig('model_comparison.png')
plt.close()

# Feature importance for Random Forest
plt.figure(figsize=(8, 6))
feature_importance = pd.DataFrame(
    {'feature': ['tone'], 
     'importance_time': rf_model.feature_importances_,
     'importance_random': rf_model.feature_importances_}
)
feature_importance.plot(x='feature', y=['importance_time', 'importance_random'], 
                        kind='bar', figsize=(8, 6))
plt.title('Feature Importance - Random Forest')
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.close()

# Analyze relationship between tone and market_label in the entire dataset
plt.figure(figsize=(10, 6))
sns.boxplot(x='market_label', y='tone', data=df)
plt.title('Tone Distribution by Market Label')
plt.xlabel('Market Label')
plt.ylabel('Tone')
plt.tight_layout()
plt.savefig('tone_by_market_label.png')
plt.close()

# Create a scatter plot to see the relationship
plt.figure(figsize=(10, 6))
plt.scatter(df['tone'], df['market_label'], alpha=0.5)
plt.title('Scatter Plot: Tone vs Market Label')
plt.xlabel('Tone')
plt.ylabel('Market Label')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('scatter_tone_vs_market.png')
plt.close()

# Summary of findings
print("\nSummary of Analysis:")
print("1. Time-based Split Results:")
print(f"   - Random Forest: Accuracy = {rf_time_metrics['accuracy']:.4f}, F1 = {rf_time_metrics['f1']:.4f}")
print(f"   - SVM: Accuracy = {svm_time_metrics['accuracy']:.4f}, F1 = {svm_time_metrics['f1']:.4f}")
print("2. Random Split Results:")
print(f"   - Random Forest: Accuracy = {rf_random_metrics['accuracy']:.4f}, F1 = {rf_random_metrics['f1']:.4f}")
print(f"   - SVM: Accuracy = {svm_random_metrics['accuracy']:.4f}, F1 = {svm_random_metrics['f1']:.4f}")