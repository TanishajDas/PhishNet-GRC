import joblib
import numpy as np
import pandas as pd
from data_preprocessing import load_and_preprocess
import time

def integrate_grc():
    # Step 1: Start timing and load preprocessed data
    start_time = time.time()
    print("Starting full GRC integration process...")
    _, X_test, _, y_test, vectorizer, _ = load_and_preprocess()
    X_test.columns = X_test.columns.astype(str)  # Ensure string feature names
    
    # Step 2: Set sample size for comprehensive analysis
    # Detail: 5000 rows (~30% of 16,698 test set) for robust GRC insights
    sample_size = 5000
    if len(X_test) > sample_size:
        sample_indices = np.random.choice(X_test.index, sample_size, replace=False)
        X_test_sample = X_test.loc[sample_indices].reset_index(drop=True)
    else:
        X_test_sample = X_test.copy()
    
    # Step 3: Load model and generate risk scores
    model = joblib.load('models/phishing_model.pkl')
    probs = model.predict_proba(X_test_sample)[:, 1]  # Risk scores (0-1)
    
    # Step 4: Map risk scores to levels (GDPR-conservative thresholds)
    risk_levels = np.where(probs > 0.7, 'High', np.where(probs > 0.4, 'Medium', 'Low'))
    
    # Step 5: Define detailed GRC control mappings with GDPR
    grc_controls = {
        'High': 'ISO 27001 A.5.26 (Incident Response) - Activate team; NIST PR.IP-9 (Response Planning); GDPR Article 33 (Breach Notification) - Report within 72 hours if data impacted',
        'Medium': 'NIST ID.RA-06 (Risk Prioritization) - Assess threat; ISO 27001 A.12.4.1 (Event Logging); GDPR Article 32 (Security of Processing) - Implement monitoring controls',
        'Low': 'ISO 27001 A.5.25 (Event Assessment) - Log trends; NIST DE.CM-1 (Monitoring); GDPR Article 25 (Data Protection by Design) - Review for ongoing compliance'
    }
    controls = [grc_controls[level] for level in risk_levels]
    
    # Step 6: Generate text previews with inverse_transform
    # Detail: Use only TF-IDF columns (0-499) to avoid IndexError; limit to 5 words for readability
    texts = []
    for i in range(sample_size):
        tfidf_slice = X_test_sample.iloc[i:i+1, :500]  # Only TF-IDF part
        inverse = vectorizer.inverse_transform(tfidf_slice)[0]
        preview = ' '.join(inverse[:5]) + '...' if len(inverse) > 0 else 'No text preview'
        texts.append(preview)
    
    # Step 7: Calculate GDPR compliance score (0-100)
    # Detail: Higher scores for lower risk and strong controls; simple heuristic for demo
    gdpr_scores = np.where(risk_levels == 'Low', 90, 
                          np.where(risk_levels == 'Medium', 70, 50))  # Low: 90, Medium: 70, High: 50
    
    # Step 8: Build detailed risk register
    results = pd.DataFrame({
        'email_preview': texts,
        'risk_score': probs.round(2),
        'risk_level': risk_levels,
        'grc_control': controls,
        'gdpr_compliance_score': gdpr_scores
    })
    results.to_csv('data/risk_register_full.csv', index=False)
    
    # Step 9: Generate detailed GRC compliance report with Markdown table
    with open('reports/grc_compliance_report_full.md', 'w') as f:
        f.write("# Comprehensive GRC Compliance Report\n")
        f.write(f"## Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S IST')}\n\n")
        f.write("This report integrates AI risk scoring with GRC frameworks, emphasizing GDPR for data protection in phishing threats.\n\n")
        
        # Summary Section
        f.write("### Risk Summary\n")
        f.write(f"- Total Sampled: {sample_size}\n")
        f.write(f"- High Risk: {len(results[results['risk_level'] == 'High'])} (GDPR Article 33)\n")
        f.write(f"- Medium Risk: {len(results[results['risk_level'] == 'Medium'])} (GDPR Article 32)\n")
        f.write(f"- Low Risk: {len(results[results['risk_level'] == 'Low'])} (GDPR Article 25)\n")
        f.write(f"- Average GDPR Compliance Score: {results['gdpr_compliance_score'].mean():.1f}/100\n\n")
        
        # Control Mapping Table
        f.write("### GRC Control Mapping\n")
        f.write("| Risk Level | Frameworks |\n")
        f.write("|------------|------------|\n")
        for level, desc in grc_controls.items():
            f.write(f"| {level} | {desc} |\n")
        f.write("\n")
        
        # Recommendations
        f.write("### Recommendations\n")
        f.write("- **High Risk**: Conduct GDPR-compliant breach assessment (Article 33); notify authorities if personal data compromised.\n")
        f.write("- **Medium Risk**: Enhance security measures and employee training (Article 32).\n")
        f.write("- **Low Risk**: Integrate into ongoing data protection by design audits (Article 25).\n")
        f.write("- Overall: Use for TPRM, ensuring GDPR alignment for EU data processing.\n\n")
        
        # Sample Risks Table
        f.write("### Sample Risks\n")
        f.write(results.head(10).to_markdown(index=False))
    
    # Step 10: Report runtime
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Risk register saved to data/risk_register_full.csv")
    print(f"GRC compliance report saved to reports/grc_compliance_report_full.md")
    print(f"Process completed in {runtime:.2f} seconds")
    print(f"Sample of risk register:\n{results.head(5)}")

if __name__ == "__main__":
    integrate_grc()