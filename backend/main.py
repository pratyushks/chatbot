from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag_engine import get_qa_chain, load_retriever

app = FastAPI()
qa_chain = get_qa_chain()
retriever = load_retriever()

class ChatQuery(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: ChatQuery):
    question = query.question.lower()
    docs = retriever.get_relevant_documents(query.question)

    combined_context = " ".join(doc.page_content.lower() for doc in docs)

    relevant = any(word in combined_context for word in question.split())

    if not relevant:
        return {"answer": "I don't know."}

    result = qa_chain.invoke({"query": query.question})
    answer = result.get("result", "").strip()

    if answer.lower() in ["", "i don't know", "unknown"]:
        return {"answer": "I don't know."}

    return {
        "answer": answer,
        "sources": [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
    }
