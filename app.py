from flask import Flask,render_template,jsonify,request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from src.prompt import *
import os

app=Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["GROQ_API_KEY"]=GROQ_API_KEY

embeddings=download_embeddings()

index_name='medibot'

docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever=docsearch.as_retriever(search_type='similarity',search_kwrags={"k":3})

llm = ChatGroq(model="llama3-8b-8192", temperature=0.2,groq_api_key=GROQ_API_KEY)


prompt=ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","{input}"),
    ]
)

question_answer_chain=create_stuff_documents_chain(llm,prompt)
rag_chain=create_retrieval_chain(retriever,question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route('/get', methods=['POST'])
def chat():
    msg = request.json.get('message', '').strip()
    print("User Input:", msg)

    # Simulated chatbot response (
    response = rag_chain.invoke({"input": msg})
    bot_response = response.get("answer", "Sorry, I didn't understand that.")

    print("Response:", bot_response)
    
    return jsonify({"response": bot_response})  # Return JSON response


if __name__=='__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)