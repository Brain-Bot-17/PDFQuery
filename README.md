# **GenieRAG: Retrieval-Augmented Generation (RAG) with LLM**

## **📌 Overview**
GenieRAG is a **Retrieval-Augmented Generation (RAG) system** that combines **document retrieval** and **LLM-based response generation**. The system retrieves relevant document snippets and enhances an LLM's response quality by providing **contextualized answers**.

## **🚀 Features**
✅ Document retrieval using **FAISS** or **ChromaDB**
✅ Embedding generation with **Hugging Face Sentence Transformers**
✅ Response generation using **GPT-2**
✅ FastAPI-powered REST API for interaction
✅ NLP preprocessing and chunking using **LangChain**
✅ Experiment tracking with **MLflow** (optional)

---

## **🛠️ Tech Stack**
| **Category**        | **Tool/Library Used** |
|---------------------|----------------------|
| **Language**       | Python 3.9+          |
| **LLM**            | GPT-2 (Hugging Face) |
| **Embeddings**     | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector Store**   | FAISS / ChromaDB     |
| **API Framework**  | FastAPI              |
| **Data Processing** | LangChain, pdfplumber, PyMuPDF |
| **Experiment Tracking** | MLflow (Optional) |

---

## **📂 Project Structure**
```
GenieRAG/
│── models/                 # Store downloaded models
│── data/                   # Input documents
│── src/
│   │── vectorstore/
│   │   │── embed.py         # Convert text into embeddings
│   │   │── retrieve.py      # Retrieve relevant chunks from FAISS/ChromaDB
│   │── llm/
│   │   │── generate_response.py  # Generate responses using GPT-2
│   │   │── api.py           # FastAPI server
│── requirements.txt         # Python dependencies
│── README.md                # Project documentation
```

---

## **📦 Installation & Setup**
### **🔹 Step 1: Clone the Repository**
```sh
git clone https://github.com/yourusername/GenieRAG.git
cd GenieRAG
```

### **🔹 Step 2: Install Dependencies**
```sh
pip install -r requirements.txt
```

### **🔹 Step 3: Download Pretrained Models**
Run the following command to download GPT-2 and embeddings model:
```sh
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('gpt2'); AutoTokenizer.from_pretrained('gpt2')"
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## **🚀 Usage**
### **🔹 Step 1: Create Document Embeddings**
```sh
python src/vectorstore/embed.py
```

### **🔹 Step 2: Run the FastAPI Server**
```sh
python src/llm/api.py
```
Now, open **http://127.0.0.1:8000/docs** to interact with the API.

### **🔹 Step 3: Query the API** (via Postman or cURL)
#### **Postman Instructions**
1️⃣ Open **Postman** → Create a new `POST` request.
2️⃣ Set the URL to:
```
http://127.0.0.1:8000/ask
```
3️⃣ Go to the **Body** tab → Select `raw` → Choose `JSON`
4️⃣ Enter the following JSON payload:
```json
{
    "query": "What are the symptoms of plant disease?"
}
```
5️⃣ Click `Send`

#### **Alternatively, use cURL:**
```sh
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"query": "What are the causes of plant diseases?"}'
```

---

## **📌 Next Steps**
🔹 Enhance the retriever by experimenting with **different embedding models**.
🔹 Fine-tune the LLM for domain-specific tasks.
🔹 Extend with **document ingestion automation** using Prefect or Airflow.

💡 **Enjoy building with RAG + NLP!** 🚀

