import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns


# 1. 데이터 로드 및 전처리
data = pd.read_csv("D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_copy_for_minute_test.csv")

# 2. Train/Test Split
train_data = data[data['train_test_label'] == 'train']
test_data = data[data['train_test_label'] == 'test']

X_train, y_train = train_data[['tone']], train_data['market_label']
X_test, y_test = test_data[['tone']], test_data['market_label']

# 3. Random Forest 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train.dropna(), y_train.dropna())

# 4. 테스트 세트 예측 및 평가
y_pred = model.predict(X_test.dropna())
accuracy = accuracy_score(y_test.dropna(), y_pred)
print(f"Accuracy: {accuracy:.3f}")  # 정확도를 소수점 아래 세 자리까지 출력
cm = confusion_matrix(y_test.dropna(), y_pred)
print("Confusion Matrix:\n", cm)

# Confusion Matrix 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Class -1', 'Class 0', 'Class 1'], yticklabels=['Class -1', 'Class 0', 'Class 1'])
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()