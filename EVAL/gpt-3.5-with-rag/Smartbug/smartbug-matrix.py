import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    classification_report, confusion_matrix, ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("gpt3.5-with-rag-smartbug_analysis_results.csv")


# Extract predicted and true labels
y_pred = df["classified_vulnerability"].str.split(",").str[0].str.strip()
y_true = df["True_Label"].str.strip()

# Calculate basic metrics
accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
report = classification_report(y_true, y_pred)

# Print metrics
print(f"Accuracy: {accuracy:.3f}")
print(f"Macro Precision: {precision:.3f}")
print(f"Macro Recall: {recall:.3f}")
print(f"Macro F1-Score: {f1:.3f}\n")
print("Detailed classification report:")
print(report)

# Generate confusion matrix
labels = sorted(df["True_Label"].unique())
cm = confusion_matrix(y_true, y_pred, labels=labels)

# Display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
