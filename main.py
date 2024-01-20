import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
#from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain



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
    # Initialization of conversation memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)  
    # Initialization of conversation -- converse with the vector store
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever= vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain

    






def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    print(OPENAI_API_KEY)

    if "conversation" not in st.session.state:
        st.session.state.conversation = None

    st.set_page_config(page_title= "Chat with multiple PDFs", page_icon=":books:")

    st.header("Chat with multiple PDFs :books:")
    st.text_input("Ask a question about your documents")

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
                st.session.state.conversation= get_conversation_chain(vectorstore)

    


        



if __name__ == "__main__":
    main()