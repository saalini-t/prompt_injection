import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Data is in app/data, script is in app/ml
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "data"))
DATA_PATH = os.path.join(DATA_DIR, "prompt_attack_corpus.csv")
ML_DIR = os.path.join(SCRIPT_DIR)
os.makedirs(ML_DIR, exist_ok=True)

# External ethics datasets
ETHICS_DATASETS = [
    r"C:\Saalu_Data\cybersecurity\datasets\ethics_brain\abusive_lang.csv",
    r"C:\Saalu_Data\cybersecurity\datasets\ethics_brain\hate_speech.csv",
    r"C:\Saalu_Data\cybersecurity\datasets\ethics_brain\toxic_comments.csv"
]

# External narrative datasets
NARRATIVE_DATASETS = [
    r"C:\Saalu_Data\cybersecurity\datasets\narrative_brain\SPAM_SMS.csv"
]

def train_injection():
    data_path = os.path.normpath(DATA_PATH)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"CSV not found at {data_path}")
    
    print(f"[Injection] Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"[Injection] Loaded {len(df)} rows")
    
    X = df["text"].astype(str).values
    y = df["label"].astype(str).values

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    pipe.fit(X, y)

    out = os.path.join(ML_DIR, "prompt_injection_pipeline.pkl")
    joblib.dump(pipe, out)
    print(f"[Injection] Saved pipeline to {out}")
    print(f"[Injection] Classes: {pipe.named_steps['clf'].classes_}")

def train_ethics():
    """
    Train ethics model from three datasets:
    - abusive_lang.csv
    - hate_speech.csv
    - toxic_comments.csv
    """
    print(f"\n[Ethics] Loading {len(ETHICS_DATASETS)} datasets...")
    
    all_texts = []
    all_labels = []
    
    for dataset_path in ETHICS_DATASETS:
        if not os.path.exists(dataset_path):
            print(f"[Ethics] WARNING: {dataset_path} not found, skipping...")
            continue
        
        print(f"[Ethics] Loading: {dataset_path}")
        df = pd.read_csv(dataset_path)
        print(f"[Ethics]   → {len(df)} rows")
        
        # Normalize each dataset based on its structure
        if "abusive_lang" in dataset_path:
            # Tweet, Class (normal/hate)
            texts = df["Tweet"].astype(str).values
            labels = (df["Class"] == "hate").astype(int).values
        elif "hate_speech" in dataset_path:
            # tweet, class (0=hate, 1=offensive, 2=neither)
            texts = df["tweet"].astype(str).values
            labels = (df["class"].isin([0, 1])).astype(int).values  # 0/1 = unethical, 2 = safe
        elif "toxic_comments" in dataset_path:
            # comment, toxic (0/1)
            texts = df["comment"].astype(str).values
            labels = df["toxic"].astype(int).values
        else:
            print(f"[Ethics] WARNING: Unknown dataset format, skipping...")
            continue
        
        all_texts.extend(texts)
        all_labels.extend(labels)
        print(f"[Ethics]   → Added {len(texts)} samples")
    
    if not all_texts:
        raise FileNotFoundError("No ethics data loaded")
    
    print(f"[Ethics] Total samples: {len(all_texts)}")
    print(f"[Ethics] Unethical samples: {sum(all_labels)}")
    print(f"[Ethics] Safe samples: {len(all_labels) - sum(all_labels)}")
    
    X = all_texts
    y = all_labels
    
    # Train vectorizer with trigrams to catch deceptive patterns
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 3), max_features=5000)
    X_vec = vectorizer.fit_transform(X)
    
    # Train model with balanced class weights
    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_vec, y)
    
    model_out = os.path.join(ML_DIR, "ethics_model.pkl")
    vec_out = os.path.join(ML_DIR, "ethics_vectorizer.pkl")
    joblib.dump(model, model_out)
    joblib.dump(vectorizer, vec_out)
    
    print(f"[Ethics] Saved model to {model_out}")
    print(f"[Ethics] Saved vectorizer to {vec_out}")
    print(f"[Ethics] Classes: {model.classes_}")

def train_narrative():
    """
    Train narrative model to detect:
    - Spam messages
    - Phishing attempts
    - Social engineering
    - Deceptive narratives
    - Manipulation tactics
    """
    print(f"\n[Narrative] Loading {len(NARRATIVE_DATASETS)} datasets...")
    
    all_texts = []
    all_labels = []
    
    for dataset_path in NARRATIVE_DATASETS:
        if not os.path.exists(dataset_path):
            print(f"[Narrative] WARNING: {dataset_path} not found, skipping...")
            continue
        
        print(f"[Narrative] Loading: {dataset_path}")
        
        if "SPAM_SMS" in dataset_path:
            # SPAM_SMS.csv: all messages are spam (label=1)
            df = pd.read_csv(dataset_path, encoding='latin1')
            texts = df["text"].astype(str).values
            labels = [1] * len(texts)  # All spam
            
            all_texts.extend(texts)
            all_labels.extend(labels)
            print(f"[Narrative]   → Added {len(texts)} spam samples")
    
    # Add safe samples from prompt_attack_corpus to balance dataset
    safe_data_path = os.path.join(DATA_DIR, "prompt_attack_corpus.csv")
    if os.path.exists(safe_data_path):
        print(f"[Narrative] Loading safe samples from: {safe_data_path}")
        df_safe = pd.read_csv(safe_data_path)
        safe_texts = df_safe[df_safe["label"] == "safe"]["text"].astype(str).values
        safe_labels = [0] * len(safe_texts)
        
        all_texts.extend(safe_texts)
        all_labels.extend(safe_labels)
        print(f"[Narrative]   → Added {len(safe_texts)} safe samples")
    
    # Add some generic safe messages
    safe_messages = [
        "Hello, how are you doing today?",
        "Can we schedule a meeting for tomorrow?",
        "Thanks for your help with the project",
        "What time is the presentation?",
        "I'll send you the document later",
        "Good morning! Hope you have a great day",
        "Let me know if you need anything",
        "The weather is nice today",
        "I'm working on the report now",
        "See you at the office"
    ] * 10  # Repeat to balance dataset
    
    all_texts.extend(safe_messages)
    all_labels.extend([0] * len(safe_messages))
    print(f"[Narrative]   → Added {len(safe_messages)} generic safe samples")
    
    if not all_texts:
        raise FileNotFoundError("No narrative data loaded")
    
    print(f"[Narrative] Total samples: {len(all_texts)}")
    print(f"[Narrative] Malicious samples: {sum(all_labels)}")
    print(f"[Narrative] Safe samples: {len(all_labels) - sum(all_labels)}")
    
    X = all_texts
    y = all_labels
    
    # Train vectorizer with character-level features to catch obfuscation
    vectorizer = TfidfVectorizer(
        lowercase=True, 
        ngram_range=(1, 3), 
        max_features=5000,
        analyzer='word'
    )
    X_vec = vectorizer.fit_transform(X)
    
    # Train model with balanced class weights
    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_vec, y)
    
    model_out = os.path.join(ML_DIR, "narrative_model.pkl")
    vec_out = os.path.join(ML_DIR, "narrative_vectorizer.pkl")
    joblib.dump(model, model_out)
    joblib.dump(vectorizer, vec_out)
    
    print(f"[Narrative] Saved model to {model_out}")
    print(f"[Narrative] Saved vectorizer to {vec_out}")
    print(f"[Narrative] Classes: {model.classes_}")

def main():
    print("=" * 60)
    print("Training SentinelAI Models - 3 Brains")
    print("=" * 60)
    
    train_injection()
    train_ethics()
    train_narrative()
    
    print("\n" + "=" * 60)
    print("All 3 brains trained successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()