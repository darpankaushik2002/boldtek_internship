# backend/main.py
from chatbot import generate_response
from data_analysis import build_index, retrieve_relevant_chunks

def main():
    DATA_DIR = "../data"  # Adjust path as necessary
    print("Building document index...")
    index = build_index(DATA_DIR)
    print("Index built successfully!")
    
    while True:
        query = input("\nEnter your question (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        # Retrieve top 3 relevant document chunks
        retrieved = retrieve_relevant_chunks(query, index, top_k=3)
        context = "\n\n".join([chunk for chunk, score in retrieved])
        
        # Construct a prompt combining the context and the question
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        print("\nGenerating answer...")
        answer = generate_response(prompt)
        print("\nAnswer:")
        print(answer)
        print("\nRetrieved Context (for reference):")
        for chunk, score in retrieved:
            print(f"Score: {score:.4f} - {chunk[:40]}...")  # Show first 40 characters

if __name__ == "__main__":
    main()
