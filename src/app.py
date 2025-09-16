import streamlit as st
import pandas as pd
import joblib
import json
import numpy as np
import xlsxwriter
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import subprocess
# Load model, vectorizer, and metrics
model = joblib.load('models/phishing_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')
with open('models/classification_metrics.json', 'r') as f:
    metrics = json.load(f)

st.title('AI-GRC Phishing Dashboard with GDPR Integration')

# Sidebar for file upload or sample data
st.sidebar.header('Data Input')
st.sidebar.write("Drag and drop a CSV with columns: email_preview, risk_score, risk_level, grc_control, gdpr_compliance_score")
uploaded_file = st.sidebar.file_uploader('Upload Risk Register CSV (e.g., risk_register_full.csv)', type='csv')
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv('data/risk_register_full.csv')  # Default to full register

# Table 1: Model Training Metrics
st.header('Model Training Metrics')
# Prepare classification report data
class_report = pd.DataFrame({
    'Metric': ['Precision', 'Recall', 'F1-Score', 'Support'],
    'Legitimate (0)': [metrics['0'][m] for m in ['precision', 'recall', 'f1-score', 'support']],
    'Phishing (1)': [metrics['1'][m] for m in ['precision', 'recall', 'f1-score', 'support']]
})
# Add accuracy as a separate row with proper alignment
class_report.loc[len(class_report)] = ['Accuracy', metrics['accuracy'], metrics['accuracy']]  # Use accuracy for both classes
# Add confusion matrix
conf_matrix = np.array([[metrics['0']['support'] - metrics['0']['f1-score'] * metrics['0']['support'], metrics['1']['support'] - metrics['1']['recall'] * metrics['1']['support']],
                       [metrics['0']['support'] - metrics['0']['recall'] * metrics['0']['support'], metrics['1']['recall'] * metrics['1']['support']]])
conf_df = pd.DataFrame(conf_matrix, index=['Predicted Legitimate', 'Predicted Phishing'], columns=['Actual Legitimate', 'Actual Phishing'])
st.table(class_report.style.format({'Legitimate (0)': '{:.2f}', 'Phishing (1)': '{:.2f}', 'Accuracy': '{:.2f}'}))
st.subheader('Confusion Matrix')
st.table(conf_df.style.format('{:.0f}'))

# Table 2: Risk Level Summary
st.header('Risk Level Summary')
risk_counts = df['risk_level'].value_counts().reindex(['High', 'Medium', 'Low'], fill_value=0)
risk_summary = pd.DataFrame({
    'Risk Level': ['High', 'Medium', 'Low'],
    'Count': risk_counts.values,
    'GDPR Reference': ['Article 33 - Breach Notification', 'Article 32 - Security Processing', 'Article 25 - Data Protection by Design']
})
st.table(risk_summary.style.format({'Count': '{:.0f}'}))
st.write(f"**Total Risks**: {len(df)}")

# Filter and Display Risk Register
st.header('Risk Register')
risk_level = st.selectbox('Filter by Risk Level', ['All'] + list(df['risk_level'].unique()))
if risk_level == 'All':
    filtered_df = df
else:
    filtered_df = df[df['risk_level'] == risk_level]
st.dataframe(filtered_df)

# Download as XLSX or PDF
output_xlsx = io.BytesIO()
try:
    with pd.ExcelWriter(output_xlsx, engine='xlsxwriter') as writer:
        filtered_df.to_excel(writer, sheet_name='Risk Register', index=False)
    xlsx_data = output_xlsx.getvalue()
    st.download_button('Download as XLSX', xlsx_data, 'risk_register.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
except Exception as e:
    st.error(f"Error generating XLSX: {e}")

output_pdf = io.BytesIO()
doc = SimpleDocTemplate(output_pdf, pagesize=letter)
table_data = [filtered_df.columns.tolist()] + filtered_df.values.tolist()
table = Table(table_data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
doc.build([table])
pdf_data = output_pdf.getvalue()
st.download_button('Download as PDF', pdf_data, 'risk_register.pdf', 'application/pdf')

# Run: streamlit run src/app.py

# Run: streamlit run src/app.py