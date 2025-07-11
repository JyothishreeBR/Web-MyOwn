import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv('placement_data.csv')

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("Cleaned Columns:", df.columns.tolist())

# Common preprocessing
X = df.drop(['placement_readiness', 'company_fit'], axis=1)
cols_to_scale = ['cgpa', 'backlogs', 'certifications', 'aptitude', 'coding',
                 'communication', 'projects', 'resume', 'hackathon','branch']
scaler = StandardScaler()
X[cols_to_scale] = scaler.fit_transform(X[cols_to_scale])

# ======= Model 1: Placement Readiness =======
y1 = df['placement_readiness']
X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y1, test_size=0.2, random_state=42)

model1 = RandomForestClassifier(n_estimators=100, random_state=42)
model1.fit(X_train1, y_train1)
y_pred1 = model1.predict(X_test1)

print("\n📘 Placement Readiness Report")
print(classification_report(y_test1, y_pred1))
print("✅ Accuracy (Placement Readiness):", accuracy_score(y_test1, y_pred1))

joblib.dump(model1, 'placement_model.pkl')

# ======= Model 2: Company Fit =======
y2 = df['company_fit']
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y2, test_size=0.2, random_state=42)

model2 = RandomForestClassifier(n_estimators=100, random_state=42)
model2.fit(X_train2, y_train2)
y_pred2 = model2.predict(X_test2)

print("\n📙 Company Fit Report")
print(classification_report(y_test2, y_pred2))
print("✅ Accuracy (Company Fit):", accuracy_score(y_test2, y_pred2))

joblib.dump(model2, 'company_fit_model.pkl')

# Save the shared scaler
joblib.dump(scaler, 'scaler.pkl')
print("\n🎉 Models and scaler saved as 'placement_model.pkl', 'company_fit_model.pkl', and 'scaler.pkl'")