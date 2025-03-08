import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load the data
df = pd.read_csv('D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_copy_for_minute_test.csv')

# Split into train and test sets based on the train_test_label column
train_df = df[df['train_test_label'] == 'train']
test_df = df[df['train_test_label'] == 'test']

# Prepare features (X) and target (y)
X_train = train_df[['tone']].values
y_train = train_df['market_label'].values

X_test = test_df[['tone']].values
y_test = test_df['market_label'].values

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train SVM model
svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = svm_model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.4f}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(class_report)

# Visualize the results
plt.figure(figsize=(12, 6))

# Plot 1: Training data and decision boundary
plt.subplot(1, 2, 1)
plt.title('SVM Decision Boundary (Training Data)')

# Create a mesh grid for the decision boundary
tone_min, tone_max = X_train[:, 0].min() - 0.1, X_train[:, 0].max() + 0.1
tone_mesh = np.linspace(tone_min, tone_max, 100).reshape(-1, 1)
tone_mesh_scaled = scaler.transform(tone_mesh)
tone_mesh_pred = svm_model.predict(tone_mesh_scaled)

# Plot decision regions
for i, label in enumerate([-1, 0, 1]):
    plt.scatter(tone_mesh[tone_mesh_pred == label], 
                [i/10] * np.sum(tone_mesh_pred == label), 
                alpha=0.1, 
                color=f'C{i+1}',
                marker='_',
                s=100)

# Plot training data points
for i, label in enumerate([-1, 0, 1]):
    if label in y_train:
        plt.scatter(X_train[y_train == label], 
                    [0.5] * np.sum(y_train == label), 
                    color=f'C{i+1}', 
                    label=f'Class {label}')

plt.yticks([])
plt.xlabel('Tone Value')
plt.legend()

# Plot 2: Test data and predictions
plt.subplot(1, 2, 2)
plt.title('SVM Predictions vs Actual (Test Data)')

# Plot test data points and their predictions
for i, test_label in enumerate([-1, 0, 1]):
    if test_label in y_test:
        indices = y_test == test_label
        correct = y_pred[indices] == test_label
        
        # Correct predictions
        plt.scatter(X_test[indices & correct], 
                    [0.6] * np.sum(indices & correct), 
                    color=f'C{i+1}',
                    marker='o',
                    label=f'Correct Class {test_label}')
        
        # Incorrect predictions
        if np.any(indices & ~correct):
            plt.scatter(X_test[indices & ~correct], 
                        [0.4] * np.sum(indices & ~correct), 
                        color=f'C{i+1}',
                        marker='x',
                        s=100,
                        label=f'Misclassified Class {test_label}')

plt.yticks([])
plt.xlabel('Tone Value')
plt.legend()

plt.tight_layout()
plt.savefig('svm_analysis_results.png')
plt.show()

# Additional analysis: Performance by tone value range
# Group the test data into bins by tone value and analyze performance in each bin
bins = np.linspace(X_test.min(), X_test.max(), 5)
bin_labels = [f"{bins[i]:.2f} to {bins[i+1]:.2f}" for i in range(len(bins)-1)]
X_test_binned = pd.cut(X_test.flatten(), bins, labels=bin_labels)

# Create a DataFrame for analysis
performance_df = pd.DataFrame({
    'tone': X_test.flatten(),
    'actual': y_test,
    'predicted': y_pred,
    'bin': X_test_binned
})

# Calculate accuracy by bin
bin_accuracy = performance_df.groupby('bin').apply(
    lambda x: accuracy_score(x['actual'], x['predicted'])
)

print("\nAccuracy by Tone Range:")
for bin_name, acc in bin_accuracy.items():
    count = performance_df[performance_df['bin'] == bin_name].shape[0]
    print(f"Tone {bin_name}: {acc:.4f} (n={count})")

# Investigate the relationship between tone and market_label
plt.figure(figsize=(10, 6))
plt.scatter(train_df['tone'], train_df['market_label'], alpha=0.6, label='Training Data')
plt.scatter(test_df['tone'], test_df['market_label'], alpha=0.6, label='Test Data')
plt.xlabel('Tone')
plt.ylabel('Market Label')
plt.title('Relationship Between Tone and Market Label')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('tone_vs_market_label.png')
plt.show()