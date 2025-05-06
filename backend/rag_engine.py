import os
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
load_dotenv()

VECTORSTORE_DIR = "./vectorstore"

def load_retriever():
    embedding_model = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    db = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
    return db.as_retriever()

def get_qa_chain():
    retriever = load_retriever()

    model_name = os.getenv("MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
    llm = HuggingFacePipeline(pipeline=pipe)

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful support assistant. Answer the question using only the information provided in the context below.

Context:
{context}

Question:
{question}

If the answer is not found in the context, do NOT attempt to answer. Just reply: "I don't know."
Also if the answer is not related to the context, immediately reply "I don't know."
""".strip()
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )

    return qa
