import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
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
train_df = df[df['date'] <= '2023-07-31']
test_df = df[df['date'] > '2023-07-31']

# Check unique values in market_label
print("Unique values in market_label:", df['market_label'].unique())

# X와 Y 데이터 준비
X_train = train_df[['tone']]
y_train = train_df['market_label']

X_test = test_df[['tone']]
y_test = test_df['market_label']

# Force binary classification by ensuring there are only two classes
# If there are more than 2 classes, consider converting to binary
# Example: if market_label is in [0, 1, 2], you might want to make it binary like this:
# y_train = (y_train > 0).astype(int)
# y_test = (y_test > 0).astype(int)

# SVM 모델 - Make sure to specify probability=True for proper ROC curve
svm_model = svm.SVC(kernel='linear', probability=True)
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)
print("SVM Accuracy:", accuracy_score(y_test, y_pred_svm))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_svm)
print("Confusion Matrix:\n", cm)

# ROC Curve - For binary classification
if len(np.unique(y_test)) == 2:
    # Get the probability estimates for the positive class
    y_pred_proba = svm_model.predict_proba(X_test)[:, 1]
    
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
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()
else:
    print("ROC Curve requires binary classification, but found", len(np.unique(y_test)), "classes")
    print("Consider converting your problem to binary classification")

# Scatter Plot with Decision Boundary
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_test.values, np.zeros(len(X_test)), c=y_test, cmap='plasma', s=50, alpha=0.8)

# Only try to plot the decision boundary for binary classification with a linear kernel
if svm_model.kernel == 'linear' and len(np.unique(y_test)) == 2:
    w = svm_model.coef_[0]
    b = svm_model.intercept_[0]
    x_min, x_max = X_test.values.min(), X_test.values.max()
    x_points = np.linspace(x_min - 1, x_max + 1, 100)
    
    # For 1D features, the decision boundary is just a point where w*x + b = 0
    decision_boundary = -b / w[0]
    plt.axvline(x=decision_boundary, color='white', linestyle='-', label='Decision Boundary')
    
    # Highlight the support vectors
    plt.scatter(X_train.values[svm_model.support_], np.zeros(len(svm_model.support_)), 
                s=100, linewidth=1, facecolors='none', edgecolors='r', label='Support Vectors')

colorbar = plt.colorbar(scatter, label='Class')
colorbar.ax.yaxis.label.set_color('white')
colorbar.ax.tick_params(colors='white')
plt.yticks([])  # Hide y-axis ticks since it's a 1D visualization
plt.xlabel('Tone')
plt.title('SVM Decision Boundary')
plt.legend()
plt.tight_layout()
plt.show()