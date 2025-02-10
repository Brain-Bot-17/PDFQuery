# GenieRAG 🚀  
A **Retrieval-Augmented Generation (RAG) system** that extracts text from PDFs, stores vector embeddings in **FAISS**, retrieves relevant chunks, and generates responses using an **LLM**.  

## **🛠️ Tech Stack**
| **Category**        | **Tool/Library Used** |
|---------------------|----------------------|
| **Language**       | Python 3.11         |
| **LLM**            | GPT-2 (Hugging Face) |
| **Embeddings**     | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector Store**   | FAISS      |
| **API Framework**  | FastAPI              |
| **Data Processing** | LangChain, pdfplumber, PyMuPDF |
| **Data Tracking** | DVC |

## 🔹 Setup  
Clone the repository:  
```sh
git clone https://github.com/Khushdeep-22102/GenieRAG.git
cd GenieRAG
```

Create a virtual environment and activate it:  
```sh
python -m venv venv  
venv\Scripts\activate
```

Install dependencies:  
```sh
pip install -r requirements.txt
```

## 🔹 Usage  

### **1️⃣ Add Data**  
Place PDFs or text files in `data/raw/`.

### **2️⃣ Extract Text**  
```sh
python src/preprocessing/extract_text.py
```

### **3️⃣ Chunk Text**  
```sh
python src/preprocessing/chunk_text.py
```

### **4️⃣ Generate Embeddings & Store in FAISS**  
```sh
python src/vectorstore/generate_embeddings.py
```

### **5️⃣ Retrieve Relevant Chunks**  
```sh
python src/vectorstore/retrieve.py
```

### **6️⃣ Generate Response**  
```sh
python src/llm/generate_response.py
```
You can now **input a question**, and the model will generate an answer based on the retrieved document chunks.  

**Example:**  
```sh
Enter your question: What is artificial intelligence?
```
**Response:**  
```sh
Artificial intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans. It encompasses various technologies, such as machine learning, natural language processing, and computer vision, to enable machines to perform tasks that typically require human intelligence.
```
