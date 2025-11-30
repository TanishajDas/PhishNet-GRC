
# PhishNet-GRC
AI-Integrated GRC Simulation for Cyber Threats (Phishing Use Case)

## Implementation
Phishing remains the leading cause of enterprise security breaches in 2025, responsible for over **90% of successful incidents**.  
Traditional GRC (Governance, Risk, Compliance) workflows often rely on manual threat detection and reporting, which leads to:
- Delayed response times
- Incomplete compliance mapping
- Increased residual risk

This project shows how **AI can enhance GRC** by predicting phishing emails, scoring risks, and mapping them directly to **ISO 27001** and **NIST CSF** controls.

---

## Objectives
- Simulate **enterprise phishing threats** with realistic datasets.  
- Build an **AI/ML model** to detect phishing emails.  
- Automate **risk scoring** (likelihood × impact).  
- Map outputs to **ISO 27001 Annex A** and **NIST CSF** functions.  
- Generate a **risk register** and a **governance dashboard**.  

---

## Project Structure

<img width="776" height="437" alt="Screenshot 2025-09-16 184337" src="https://github.com/user-attachments/assets/a93976e5-b5df-44f4-a9ee-3daa1f53d845" />

### 1. Use Case Definition
- **Threat Focus**: Phishing emails (mass, spear, AI-generated).  
- **Business Processes Impacted**:  
  - Email communication (HR, Finance, Operations)  
  - GDPR/HIPAA data exposure  
  - Financial fraud (wire transfers, payroll redirection)  
- **Impact Example**: A single successful phishing attack costs ~$4.5M in 2025 (IBM).  

---

### 2. Dataset
- **Sources**:  
  - Figshare Phishing Dataset (2024) – 200k+ labeled emails.  
  - MeAJOR Corpus (2025) – AI-generated phishing examples.  
  - Kaggle Phishing Dataset – ~10k emails from Enron/Ling corpora.  
- **Features Extracted**:
  - Email subject/body text  
  - Presence of suspicious URLs/domains  
  - Urgency keywords ("urgent", "verify", "reset")  
  - Attachment type flags  
  - Sender reputation  

---

### 3. AI/ML Component
python
# Core AI workflow
1. Preprocess dataset (clean + tokenize text).
2. Vectorize text features (TF-IDF / embeddings).
3. Train classification model (Logistic Regression, Random Forest, or BERT).
4. Evaluate using accuracy, precision, recall, F1-score.
5. Output a probability score (0–1) = likelihood of phishing.

# Model Choices:
1. Logistic Regression → interpretable, simple baseline.
2. Random Forest → robust, non-linear feature handling.
In this project the second option has been implemented

## 4. Risk Scoring & Mapping
Equation:
Risk Score = Likelihood (from AI model) × Impact (business value of asset)

## 5.Governance Mapping
ISO 27001 (2022 Annex A)

A.5.24 – Planning & preparation (AI alerts for phishing attempts)

A.5.25 – Event assessment (risk scoring)

A.5.26 – Incident response (quarantine/high-risk email)

A.5.27 – Lessons learned (retrain ML on false positives)

A.5.28 – Evidence collection (logs for audits)

NIST CSF 2.0

ID.RA – Risk assessment (AI-driven scoring)

PR.DS – Data security (flagging risky email data flow)

DE.CM – Continuous monitoring (model scanning)

RS.MI – Mitigation (automated isolation)

GV.RM – Risk management strategy updates

## 6. Built with Streamlit (Python) for interactivity.

Key Features:

  Threats detected 

  Risk levels (high, medium, low)

  Controls triggered (table)

  Risk register export (Excel/PDF) 

## 7. Deliverables

1. risk_register.csv or pdf – Risk entries with likelihood, impact, and mapped controls.

2. Governance Dashboard 



## Author

Tanisha Jamie Das

🎓 Email: dasit.tanisha@gmail.com 
🌐 Linkedin: https://www.linkedin.com/in/tanishajdas/
