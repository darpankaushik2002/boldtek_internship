
from chatbot import generate_response
from data_analysis import build_index, retrieve_relevant_chunks

def extract_answer(response: str) -> str:
    """
    Extract the answer portion from the model's output by using the [BEGIN ANSWER] marker.
    If the marker is found, only the text after it is returned.
    """
    marker = "[BEGIN ANSWER]"
    if marker in response:
        return response.split(marker)[-1].strip()
    return response.strip()

def main():
    DATA_DIR = "../data"  # Ensure this path points to your text files folder.
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
        
        # (Optional) Uncomment the next two lines for debugging to see the retrieved context.
        # print("\n[DEBUG] Retrieved Context:")
        # print(context)
        
        # Construct the prompt with strong instructions to use ONLY the provided context.
        prompt = (
            "Below is the context extracted from our documents. "
            "Answer the following question using ONLY the provided context. "
            "Do NOT use any external knowledge or repeat any text from the context in your answer.\n\n"
            "Context:\n" + context + "\n\n"
            "Question: " + query + "\n"
            "[BEGIN ANSWER]\n"
        )
        print("\nGenerating answer...")
        answer = generate_response(prompt)
        
        # Extract only the answer portion using our marker
        final_answer = extract_answer(answer)
        print("\nAnswer:")
        print(final_answer)

if __name__ == "__main__":
    main()
