import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
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
train_df = df[df['date'] <= '2024-07-31']
test_df = df[df['date'] > '2024-07-31']

# Check unique values in market_label
print("Unique values in market_label:", df['market_label'].unique())

# X와 Y 데이터 준비
X_train = train_df[['tone']]
y_train = train_df['market_label']

X_test = test_df[['tone']]
y_test = test_df['market_label']

# Random Forest 모델
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_rf)
print("Confusion Matrix:\n", cm)

# Get feature importance
feature_importance = rf_model.feature_importances_
print("Feature Importance:", feature_importance)

# ROC Curve - For binary classification
if len(np.unique(y_test)) == 2:
    # Get the probability estimates for the positive class
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    
    # Calculate ROC curve and AUC
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='orange', lw=2, label='ROC curve (area = %0.2f)' % auc)
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (Random Forest)')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()
else:
    print("ROC Curve requires binary classification, but found", len(np.unique(y_test)), "classes")
    print("Consider converting your problem to binary classification")

# For multiclass problems, we can see how the model is separating classes
# by plotting predicted probabilities
if len(np.unique(y_test)) > 2:
    # Plot the distribution of predictions
    plt.figure(figsize=(10, 6))
    
    # Get all class probabilities
    y_proba = rf_model.predict_proba(X_test)
    
    # Plot each tone value with color based on true class
    scatter = plt.scatter(X_test.values, np.zeros(len(X_test)), c=y_test, cmap='plasma', s=50, alpha=0.8)
    
    # Add a second scatter with symbol size representing prediction confidence
    for i, tone_val in enumerate(X_test.values):
        # Get max probability as confidence
        confidence = np.max(y_proba[i]) 
        plt.scatter(tone_val, 0.1, c='orange', alpha=confidence, s=confidence*100)
    
    plt.yticks([])  # Hide y-axis ticks
    plt.xlabel('Tone')
    plt.title('Random Forest Classification Results')
    colorbar = plt.colorbar(scatter, label='True Class')
    colorbar.ax.yaxis.label.set_color('white')
    colorbar.ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# Create a feature importance plot
plt.figure(figsize=(8, 4))
plt.bar(['Tone'], feature_importance, color='orange')
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.title('Random Forest Feature Importance')
plt.tight_layout()
plt.show()

# Plot the decision function across the tone range
plt.figure(figsize=(10, 6))
tone_range = np.linspace(X_test.values.min() - 0.5, X_test.values.max() + 0.5, 300).reshape(-1, 1)
probas = rf_model.predict_proba(tone_range)

# Plot probability for each class
for i in range(probas.shape[1]):
    plt.plot(tone_range, probas[:, i], label=f'Class {i} probability')

plt.xlabel('Tone')
plt.ylabel('Probability')
plt.title('Random Forest Decision Function')
plt.legend()
plt.tight_layout()
plt.grid(True, alpha=0.3)
plt.show()