import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
import matplotlib.pyplot as plt

# Set dark background style for all plots
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#0f0e0c',
    'axes.facecolor': '#0f0e0c',
    'savefig.facecolor': '#0f0e0c',
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'axes.edgecolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'grid.color': '#444444',
    'legend.facecolor': '#0f0e0c',
    'legend.edgecolor': 'white'
})

# CSV 파일 로드
df = pd.read_csv('D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_copy.csv')

# date 열을 datetime 형식으로 변환
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# 훈련 데이터와 테스트 데이터 분할
train_df = df[df['date'] <= '2023-12-31']
test_df = df[df['date'] > '2023-12-31']

# X와 Y 데이터 준비
X_train = train_df[['tone']]
y_train = train_df['market_label']

X_test = test_df[['tone']]
y_test = test_df['market_label']

# Scale the data (important for some models like MLP)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Function to evaluate a model
def evaluate_model(model, name, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"\n{name} Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Confusion Matrix:\n {cm}")
    print(classification_report(y_test, y_pred))
    
    # Calculate OvR AUC for multiclass if the model supports predict_proba
    if hasattr(model, "predict_proba"):
        # For multi-class, calculate OvR AUC
        if len(np.unique(y_test)) > 2:
            # One vs Rest AUC
            y_proba = model.predict_proba(X_test)
            auc_scores = []
            
            for i in range(len(np.unique(y_test))):
                if i in model.classes_:  # Check if class is in model's classes
                    class_idx = np.where(model.classes_ == i)[0][0]
                    # Create binary labels (1 for current class, 0 for others)
                    binary_y = (y_test == i).astype(int)
                    try:
                        auc = roc_auc_score(binary_y, y_proba[:, class_idx])
                        auc_scores.append(auc)
                    except:
                        auc_scores.append(np.nan)
            
            print(f"One-vs-Rest AUC scores per class: {auc_scores}")
            print(f"Average AUC: {np.nanmean(auc_scores):.4f}")
    
    return model, accuracy

# Create and evaluate multiple models
models = [
    (LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs'), "Logistic Regression"),
    (GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42), "Gradient Boosting"),
    (AdaBoostClassifier(n_estimators=100, random_state=42), "AdaBoost"),
    (MLPClassifier(hidden_layer_sizes=(10, 5), max_iter=1000, random_state=42), "Neural Network (MLP)")
]

results = []

for model, name in models:
    trained_model, accuracy = evaluate_model(model, name, X_train_scaled, y_train, X_test_scaled, y_test)
    results.append((name, trained_model, accuracy))

# Sort by performance
results.sort(key=lambda x: x[2], reverse=True)

# Plot accuracy comparison
plt.figure(figsize=(10, 6))
names = [result[0] for result in results]
accuracies = [result[2] for result in results]

plt.bar(names, accuracies, color='orange')
plt.xlabel('Models')
plt.ylabel('Accuracy')
plt.title('Model Accuracy Comparison')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot decision boundaries for the best model
best_model_name, best_model, best_accuracy = results[0]
print(f"\nBest model: {best_model_name} with accuracy {best_accuracy:.4f}")

# Plot the decision function across the tone range for the best model
plt.figure(figsize=(10, 6))
tone_range = np.linspace(X_test.values.min() - 0.5, X_test.values.max() + 0.5, 300)
tone_range_scaled = scaler.transform(tone_range.reshape(-1, 1))

if hasattr(best_model, "predict_proba"):
    probas = best_model.predict_proba(tone_range_scaled)
    
    # Plot probability for each class
    for i in range(probas.shape[1]):
        plt.plot(tone_range, probas[:, i], label=f'Class {i} probability')
    
    plt.xlabel('Tone')
    plt.ylabel('Probability')
    plt.title(f'{best_model_name} Decision Function')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Create a scatter plot to see how well the best model classifies the test data
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_test.values, np.zeros(len(X_test)), c=y_test, cmap='plasma', s=80, alpha=0.8, label='True Classes')

# Add predictions as small points above
plt.scatter(X_test.values, np.ones(len(X_test))*0.1, c=best_model.predict(X_test_scaled), cmap='plasma', s=50, alpha=0.6, marker='x', label='Predictions')

plt.yticks([0, 0.1], ['True', 'Pred'])
plt.xlabel('Tone')
plt.title(f'{best_model_name} Predictions vs Actual')
colorbar = plt.colorbar(scatter, label='Class')
colorbar.ax.yaxis.label.set_color('white')
colorbar.ax.tick_params(colors='white')
plt.legend()
plt.tight_layout()
plt.show()