import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from data_preprocessing import load_and_preprocess
import json

def train_model():
    """Train Random Forest model and save metrics."""
    X_train, X_test, y_train, y_test, vectorizer, _ = load_and_preprocess()
    X_train.columns = X_train.columns.astype(str)
    X_test.columns = X_test.columns.astype(str)
    
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]  # Risk scores
    report = classification_report(y_test, preds, output_dict=True)
    print("Classification Report:\n", classification_report(y_test, preds))
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))
    
    joblib.dump(model, 'models/phishing_model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    with open('models/classification_metrics.json', 'w') as f:
        json.dump(report, f)
    return model, vectorizer

if __name__ == "__main__":
    train_model()