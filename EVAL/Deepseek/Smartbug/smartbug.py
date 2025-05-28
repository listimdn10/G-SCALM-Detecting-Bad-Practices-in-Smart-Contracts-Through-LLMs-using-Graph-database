import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report

# Load the CSV file
df = pd.read_csv("deepseek-smartbug-eval.csv")

# Extract predicted and true labels
y_pred = df["classified_vulnerability"]
y_true = df["True_Label"]

# Clean up multi-labels like "dos, reentrancy"
# → Take the first label only (you can adjust this if needed)
y_pred = y_pred.str.split(",").str[0].str.strip()

# Accuracy
accuracy = accuracy_score(y_true, y_pred)

# Precision, Recall, F1 (macro, micro, weighted)
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')

# Classification report
report = classification_report(y_true, y_pred)

# Print metrics
print(f"Accuracy: {accuracy:.3f}")
print(f"Macro Precision: {precision:.3f}")
print(f"Macro Recall: {recall:.3f}")
print(f"Macro F1-Score: {f1:.3f}\n")

print("Detailed classification report:")
print(report)
