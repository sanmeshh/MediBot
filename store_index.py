from src.helper import load_pdf_file,chunking,download_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv 
import os

load_dotenv()

PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY

extracted_data=load_pdf_file(data="Data/")
text_chunks=chunking(extracted_data)
embeddings=download_embeddings()


pc=Pinecone(api_key="pcsk_2Z5GGi_Rwdk2puM8T3mXyEg1RZb1DnX6wCKcz9GMHizKAdYxk27CgbhtfE9qMF6qzsW7HW")
index_name='medibot'

pc.create_index(
    name=index_name,
    dimension=384,
    metric='cosine',
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

#store the embeddings in the index
docsearch=PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)

