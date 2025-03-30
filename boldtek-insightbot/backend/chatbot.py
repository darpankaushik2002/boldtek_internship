

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv

# Load environment variables

load_dotenv(dotenv_path=".env")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

MODEL_PATH = r"D:\opensource\hf-env\models\meta-llama\Llama-3.2-1B"
TOKENIZER_PATH = r"D:\opensource\hf-env\tokenizers\meta-llama\Llama-3.2-1B"

# Load tokenizer and model separately
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, token=ACCESS_TOKEN)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, token=ACCESS_TOKEN)

def generate_response(prompt: str, max_new_tokens: int = 150) -> str:
    """
    Generates a response from the Llama model based on the provided prompt.
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    response_tokens = model.generate(**inputs, max_new_tokens=max_new_tokens)
    answer = tokenizer.decode(response_tokens[0], skip_special_tokens=True)
    return answer 
