from prefect import flow, task
import os

@task
def fetch_new_data():
    """Fetch new documents and store embeddings."""
    os.system("python src/vectorstore/store.py")

@task
def fine_tune_model():
    """Fine-tune the model with new data."""
    os.system("python src/llm/train.py")

@task
def redeploy():
    """Restart FastAPI server."""
    os.system("docker restart generag-api")

@flow
def update_pipeline():
    fetch_new_data()
    fine_tune_model()
    redeploy()

if __name__ == "__main__":
    update_pipeline()
