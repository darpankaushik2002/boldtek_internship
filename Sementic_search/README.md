Semantic Product Search with ChromaDB & Sentence Transformers
----------------------------------------------------------------------------------------------------
This project enables semantic search on product data using ChromaDB and Sentence Transformers. It takes a product CSV file with ProductName, Description, and Price columns, creates dense embeddings, stores them in a vector database, and allows natural-language search across product descriptions.

🚀 Features
-------------------------------------------------------------------------------------------
🔍 Semantic Search: Understands natural language queries beyond keyword matching.

⚡ Efficient Vector Search: Powered by ChromaDB for fast and scalable similarity retrieval.

🧠 Sentence Embeddings: Uses all-mpnet-base-v2 model for high-quality embeddings.

📦 Metadata Handling: Retains product metadata (like price) for display during search.

📁 Project Structure
---------------------------------------

📦 semantic-product-search/
├── main.ipynb        # Main code (load data, embed, store & search)
└── README.md         # You're here!

🛠️ Installation
----------------------------------
Install required packages:


pip install -q chromadb sentence-transformers pandas
Note: This project is designed to run in a Jupyter notebook or Google Colab.

📄 Dataset Format
Your CSV file should include at least the following columns:

ProductName

Description

Price (INR)

Example:
-----------------------------------------------------------------------------

ProductName	Description	Price (INR)
Casual Jacket	A lightweight jacket perfect for winter treks.	2499
Brown Leather Shoes	Stylish brown shoes with lace-up design.	3299
🧪 How It Works
---------------------------------------------------------------------------
1. Upload & Preprocess Dataset
Upload the CSV file during runtime.

Fill missing values and normalize product information into a single document field.

Sample 30% of the data for fast experimentation.

2. Create Embeddings & Store in Chromadb
-----------------------------------------------------------------------
Uses SentenceTransformerEmbeddingFunction to encode documents.

Stores the data in a persistent ChromaDB collection called myantra_products.

3. Run Semantic Search
-------------------------------------------------------------------------------
Example queries:


semantic_search("collection of ornaments")
semantic_search("brown shoe having lace")
semantic_search("light jacket for trekking in cold")
semantic_search("premium-looking outfit under budget for men")
Each result shows:

📦 Product Name

📝 Description

💰 Price

📏 Distance (similarity metric)

🔍 Sample Output
yaml
Copy
Edit
🔹 Result 1
📦 Title: Brown Leather Shoes
📝 Description: Stylish brown shoes with lace-up design.
💰 Price: 3299
📏 Distance: 0.2971

💡 Future Improvements
-----------------------------------------------------------------------------------------------------
UI for query input

Integration with e-commerce platforms

Expand to multilingual support

Index full dataset for larger-scale search


🙌 Acknowledgements
ChromaDB

Sentence-Transformers

Developed by DARPAN , for queries :- darpankaushik104@gmail.com

