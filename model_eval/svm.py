import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

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


# SVM 모델
svm_model = svm.SVC()
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)
print("SVM Accuracy:", accuracy_score(y_test, y_pred_svm))
