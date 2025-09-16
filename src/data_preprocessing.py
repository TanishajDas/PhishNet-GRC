import pandas as pd
from faker import Faker
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

fake = Faker()

def generate_simulated_data(num_samples=1000):
    """Generate synthetic email data for robustness."""
    data = []
    for _ in range(num_samples):
        is_phishing = random.choice([0, 1])
        subject = fake.sentence(nb_words=5) if is_phishing == 0 else f"Urgent: {fake.sentence(nb_words=4)} Alert!"
        body = fake.paragraph(nb_sentences=3) if is_phishing == 0 else f"Click here: {fake.url()} to verify your account. Urgent action required!"
        features = {
            'subject': subject,
            'body': body,
            'text': subject + ' ' + body,
            'has_url': 1 if 'http' in body else 0,
            'urgency_words': body.lower().count('urgent') + body.lower().count('now'),
            'label': is_phishing,
            'source': 'simulated'
        }
        data.append(features)
    return pd.DataFrame(data)

def load_and_preprocess(data_file='data/phishing_email.csv', simulate=True):
    """Load dataset from a single CSV, preprocess, and split into train/test sets."""
    # Load the dataset
    df = pd.read_csv(data_file)
    
    # Verify and map columns (specific to this dataset)
    expected_columns = {'text_combined', 'label'}
    if not all(col in df.columns for col in expected_columns):
        raise ValueError(f"Expected columns {expected_columns} in {data_file}. Found columns: {df.columns}")
    df = df.rename(columns={'text_combined': 'text'})  # Rename to 'text' for consistency
    
    if simulate:
        sim_df = generate_simulated_data(1000)
        df = pd.concat([df, sim_df], ignore_index=True)
    
    # Feature engineering
    df['has_url'] = df['text'].apply(lambda x: 1 if 'http' in str(x) else 0)
    df['urgency_words'] = df['text'].apply(lambda x: str(x).lower().count('urgent') + str(x).lower().count('now'))
    
    # Handle missing values
    df = df.dropna(subset=['text', 'label'])
    
    # Vectorize text
    vectorizer = TfidfVectorizer(max_features=500)
    X_text = vectorizer.fit_transform(df['text'])
    
    # Combine with numerical features
    X_num = df[['has_url', 'urgency_words']]
    X = pd.concat([pd.DataFrame(X_text.toarray()), X_num.reset_index(drop=True)], axis=1)
    y = df['label']
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test, vectorizer, df  # Return df for later use

# Example run
if __name__ == "__main__":
    X_train, X_test, y_train, y_test, vectorizer, full_df = load_and_preprocess()
    print(f"Training set shape: {X_train.shape}, Test set shape: {X_test.shape}")
    print(f"Dataset sample:\n{full_df.head()}")
    full_df.to_csv('data/processed_dataset.csv', index=False)  # Save processed data for reference