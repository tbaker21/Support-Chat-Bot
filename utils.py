from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import pinecone
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import pinecone
import asyncio
from langchain.document_loaders.sitemap import SitemapLoader

#function to fetch data from website
def get_website_data(sitemap_url):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loader = SitemapLoader(
        sitemap_url
    )

    docs = loader.load()

    return docs 

#function to split data into smaller chunks 
def split_data(docs):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
    )
    
    docs_chunk = text_splitter.split_documents(docs)
    return docs_chunk

def create_embeddings():

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings 

def push_to_pinecone(pinecone_apikey,pinecone_envrionment,pinecone_index_name,embeddings,docs):
    
    pinecone.init(
        api_key=pinecone_apikey,

    )

def pull_from_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings):

    pinecone.init(
        api_key=pinecone_apikey,
        environment = pinecone_environment
    )

    index_name = pinecone_index_name 

    index = pinecone.from_existing_index(index_name,embeddings)
    return index 

def get_similar_docs(index,query,k=2):

    similar_docs = index.similarity_search(query, k=k)
    return similar_docs


