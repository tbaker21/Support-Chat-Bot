import streamlit as st
from utils import *
import constants 


#creating Session State Variable 
if 'HuggingFace_API_Key' not in st.session_state:
    st.session_state['HuggingFace_API_Key'] = ''
if 'Pinecone_API_Key' not in st.session_state:
    st.session_state['Pinecone_API_Key'] = ''

st.title('AI Assistance for Website')

#***Side Bar Functionality***

#Sidebar to capture the API Keys
st.sidebar.title("KEY")
st.session_state['HuggingFace_API_Key'] = st.sidebar.text_input("What's your HuggingFace API Key?", type="password")
st.session_state['Pinecone_API_Key']= st.sidebar.text_input("What is your Pinecone API Key?", type="password")

load_button = st.sidebar.button("Load data to Pinecone",key="load_button")

#If the above button is clicked, pushing the data to pinecone: 
if load_button:
    #Proceed only if API keys are provided: 
    if st.session_sate['HuggingFace_API_Key'] !="" and st.session_state['Pinecone_API_Key']!="":
        
        #Fetch Data from sit
        site_data = get_website_data(constants.WEBSITE_URL) #add an input? TO DO 
        st.write("Data pull done...")

        #Split data into chunks
        chunked_docs = split_data(site_data)
        st.write("Splitting data done...")

        #Crearing embeddings instance 
        embeddings = create_embeddings(chunked_docs)
        st.write("Embeddings instance creation done...")

        #Push data to Pinecone 
        push_to_pinecone(st.session_state['Pinecone_API_Key'],constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings,chunked_docs)
        st.write("Pushing data to Pinecone Done")

        st.sidebar.success("Data pushed to Pinecone successfully")
    else:
        st.sidebar.error("Ooopsss!!! Pelase provide API Keys.....")



#Capture User Inputs
prompt = st.text_input('How can I help you?')
document_count = st.slider('# of links to return')

submit = st.button("Search")

if submit:
    #Proceed only if API keys are provided
    if st.session_state['HuggingFace_API_Key'] !="" and st.session_sate['Pinecone_API_Key']!="":

        #Creating embeddings instance 
        embeddings = create_embeddings(chunked_docs)
        st.write("Embeddings instance creation done...")
        
        #Pull index data from Pinecone
        index = pull_from_pinecone(st.session_state['Pinecone_API_Key'],constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings) 
        st.write("Pinecone index retrieval done...")

        #Fetch relevant documents
        similiar_docs = get_similar_docs(index,prompt,document_count)
        st.write(similiar_docs)

        for document in similiar_docs:
            st.write("➡️**Result : " + str(similiar_docs.index(document)+1)+"**")
            st.write("**Info**: "+document.page_content)
            st.write("**LInk**: "+ document.metadata['source'])

        st.success("Please find the search results ")

        #Display search results
        st.write("search results list....")


