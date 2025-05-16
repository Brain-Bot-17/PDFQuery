# PDFQuery 🚀  
A **document retrieval system** that extracts text from PDFs, stores vector embeddings in **FAISS**, and retrieves relevant chunks using semantic similarity search. 
---

## **🛠️ Tech Stack**
| **Category**        | **Tool/Library Used** |
|---------------------|------------------------|
| **Language**         | Python 3.11             |
| **Embeddings**       | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector Store**     | FAISS                  |
| **API Framework**    | FastAPI                |
| **Data Processing**  | LangChain, pdfplumber, PyMuPDF |

---

## 🔹 Setup  
Clone the repository:  
```sh
git clone https://github.com/Brain-Bot-17/PDFQuery.git
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


The system will now return the most relevant document chunks in response to your query using semantic similarity.

**Example:**  
```sh
Enter your query: What is artificial intelligence?

```
**Output:**  
```sh
Retrieved Chunks:
- "Artificial intelligence (AI) is the simulation of human intelligence in machines..."
- "It includes machine learning, NLP, computer vision, and more..."

```
