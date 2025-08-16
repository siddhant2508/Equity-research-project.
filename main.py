import os
import time
import streamlit as st
from dotenv import load_dotenv


from langchain_openai import OpenAI                    # LLM
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain

load_dotenv()  #  OPENAI_API_KEY in .env

st.title("News Research Tool 📈")
st.sidebar.title("News Article URLs")

# Collect 3 URLs
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url.strip())

process_url_clicked = st.sidebar.button("Process URLs")

# We'll store the FAISS index in a folder instead of pickling
INDEX_DIR = "faiss_index_openai"

main_placeholder = st.empty()

# Initialize LLM
llm = OpenAI(temperature=0.9, max_tokens=500)

if process_url_clicked:
    # Filter out empty inputs
    urls = [u for u in urls if u]
    if not urls:
        st.warning("Please enter at least one valid URL.")
    else:
        try:
            # 1) Load data
            main_placeholder.text("Data Loading... Started ✅")
            loader = UnstructuredURLLoader(urls=urls)
            data = loader.load()

            # 2) Split into chunks
            main_placeholder.text("Splitting text into chunks... ✅")
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '.', ','],
                chunk_size=1000,
                chunk_overlap=150
            )
            docs = text_splitter.split_documents(data)

            # 3) Embed + build vector store
            main_placeholder.text("Building embeddings and vector index... ✅")
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(docs, embeddings)

            # 4) Save the FAISS index (recommended approach)
            vectorstore.save_local(INDEX_DIR)

            main_placeholder.text("Index ready! You can ask questions below. ✅")
            time.sleep(0.6)
            main_placeholder.empty()

        except Exception as e:
            st.error(f"Failed to process URLs: {e}")

# Q&A
query = st.text_input("Question:")
if query:
    try:
        # Recreate embeddings for loading the index
        embeddings = OpenAIEmbeddings()
        if not os.path.isdir(INDEX_DIR):
            st.error("No index found. Please process URLs first.")
        else:
            # allow_dangerous_deserialization is needed for FAISS load in some envs
            vectorstore = FAISS.load_local(
                INDEX_DIR,
                embeddings,
                allow_dangerous_deserialization=True
            )
            chain = RetrievalQAWithSourcesChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
            )

            result = chain({"question": query}, return_only_outputs=True)

            st.header("Answer")
            st.write(result.get("answer", "").strip() or "No answer returned.")

            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources")
                for src in [s for s in sources.split("\n") if s.strip()]:
                    st.write(src.strip())
    except Exception as e:
        st.error(f"Failed to answer the question: {e}")
# RUN THIS FILE ON :

''' 
conda activate base
#/opt/anaconda3/bin/python3 -m pip install -U streamlit langchain langchain-community langchain-openai faiss-cpu unstructured python-dotenv
#/opt/anaconda3/bin/python3 -m streamlit run main.py

'''
