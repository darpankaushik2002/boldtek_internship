# **Word Embeddings Comparison: Word2Vec vs BERT**

## **📌 Aim**
The goal of this project is to compare the performance of **Word2Vec** and **BERT** embeddings in capturing word semantics. We analyze how both models represent the meaning of the word **"bank"** in different contexts and measure their similarity using **cosine similarity**.

## **📂 Project Structure**
```
📦 word_embeddings_comparison
 ┣ 📂 data
 ┃ ┣ corpus.txt  # Dataset used for training Word2Vec
 ┣ 📜 word2vec_embeddings.py  # Word2Vec implementation
 ┣ 📜 bert_embeddings.py  # BERT implementation
 ┣ 📜 similarity_analysis.py  # Cosine similarity and visualization
 ┣ 📜 requirements.txt  # Dependencies
 ┣ 📜 README.md  # Project documentation
```

## **🔧 Setup & Installation**
### **1️⃣ Create a Virtual Environment** (Recommended)
```sh
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (Linux/macOS)
venv\Scripts\activate  # Activate (Windows)
```
### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

## **🛠️ Implementation Details**
### **1️⃣ Word2Vec Model**  
- We train a **Word2Vec model from scratch** on the given dataset (`corpus.txt`).
- It learns word representations based on the context in which words appear.
- Uses **CBOW** (Continuous Bag of Words) or **Skip-Gram** architecture.
- We extract embeddings for **"bank"** and **"bat"**.

### **2️⃣ BERT Model**  
- Uses a **pretrained BERT model (`bert-base-uncased`)**.
- Generates contextual embeddings for words based on their usage in a sentence.
- Extracts embeddings for **"bank"** in different contexts (finance vs river).

### **3️⃣ Similarity Analysis**  
- **Cosine similarity** is used to measure how similar the word embeddings are.
- We visualize the similarity scores using **Seaborn bar plots**.

## **📊 Results & Findings**
- **Word2Vec** gives static embeddings, so the word "bank" has the same vector regardless of context.
- **BERT** generates dynamic embeddings, meaning "bank" has different representations in different sentences.
- Cosine similarity scores show that **BERT captures contextual meaning better**.



## **🔍 Future Improvements**
- Compare more embedding models like **GloVe** and **FastText**.
- Fine-tune **BERT** for domain-specific text analysis.
- Increase dataset size for better Word2Vec training.

## Develop by Darpan .For any Queries contact darpankaushik104@gmail.com