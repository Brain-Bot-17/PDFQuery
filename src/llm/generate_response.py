import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import sys

# Add the src directory to the Python path
sys.path.append("C:/Users/HP/OneDrive/Desktop/GenieRAG/src")

# Import the retrieve function
from vectorstore.retrieve import retrieve

# Use a smaller model (OPT-350M instead of OPT-1.3B)
MODEL_NAME = "facebook/opt-350m"

# Load tokenizer and model with CPU optimization
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # FP16 if GPU
    low_cpu_mem_usage=True  # Optimize for CPU
)

# Ensure pad token exists
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def generate_response(query):
    """Retrieve relevant chunks & generate a refined response."""
    retrieved_chunks = retrieve(query)
    context = retrieved_chunks[0] if retrieved_chunks else "No relevant context found."

    input_text = f"Question: {query}\nAnswer:"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    with torch.no_grad():  # Disable gradients for faster inference
        output = model.generate(
            input_ids,
            max_new_tokens=50,  # Reduce output length for speed
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            num_beams=2,  # Reduce beams for speed
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response.replace(input_text, "").strip()

if __name__ == "__main__":
    query = input("Enter your question: ")
    answer = generate_response(query)
    print(f"\n🤖 Response:\n{answer}")
