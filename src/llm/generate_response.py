import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import sys

# Add the src directory to the Python path
sys.path.append("C:/Users/HP/OneDrive/Desktop/GenieRAG/src")

from vectorstore.retrieve import retrieve

MODEL_NAME = "gpt2"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def generate_response(query):
    """Retrieve relevant chunks & generate a response."""
    retrieved_chunks = retrieve(query)

    # Limit context to the first 3 retrieved chunks
    context = "\n".join(retrieved_chunks[:3])

    input_text = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

    output = model.generate(
        input_ids, 
        attention_mask=attention_mask, 
        max_new_tokens=200, 
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response

if __name__ == "__main__":
    query = input("Enter your question: ")
    answer = generate_response(query)
    print(f"\n🤖 Response:\n{answer}")
