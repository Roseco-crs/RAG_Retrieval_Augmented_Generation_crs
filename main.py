import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template




def get_pdf_text(pdf_docs):
    text = ""                                   # Empty variable
    for pdf in pdf_docs:                        # For each pdf from pdf_docs
        pdf_reader = PdfReader(pdf)             # We read each pdf.
        for page in pdf_reader.pages:           # For each page that we read
            text += page.extract_text()         # we extract the text and append/concatenate to the previous extracted text

    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(chunks): 
    # Embedding the text_chunks
    #embeddings=HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    embeddings = OpenAIEmbeddings(disallowed_special=())            # Embedding performed by OpenAI

    # create a vector store
    vectorstore = FAISS.from_texts(texts= chunks, embedding= embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    # Initialization of conversation memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)  
    # Initialization of conversation -- converse with the vector store
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever= vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain

    

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)




def main():
    load_dotenv()
    st.set_page_config(page_title= "Chat with multiple PDFs", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents")
    if user_question:
        handle_userinput(user_question)
        

    with st.sidebar :
        st.subheader("Your documents")
        pdf_docs =st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text 
                raw_text = get_pdf_text(pdf_docs)
                

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                

                # embed and create a vector store
                vectorstore = get_vectorstore(text_chunks)
                
                # create a conversation chain 
                st.session_state.conversation= get_conversation_chain(vectorstore)

    



if __name__ == "__main__":
    main()