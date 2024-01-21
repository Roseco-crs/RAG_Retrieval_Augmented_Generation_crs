# RAG_Retrieval_Augmented_Generation


Retrieval Augmented Generation 

Large Language Models (LLMs) are trained on massive sets of data gleaned from public repositories like stackoverflow, quora, but they don't contain the companies-specific data that your employees or customers may be looking for. So, LLMs can struggle with tasks like answering specific company questions. However, in those circumstances, LLMs may provide hallucination (response with no source or out of date). To address this challenge, Retrieval Augmented will help LLMs to generate contextually relevant insights with updated source and accuracy.

# RAG Steps
Retrieval:
- Load data and convert into text
- Split or chunk that text
- Embed the chunks of text
- create a vector store for the embeddings
- Retrieval the similarity search

Generation:
- Pass the query text and retrieved context to our LLM
- Generate contextually accurate response

# Essentials
For this project: 
 - we built a friendly user interface where users can interact with our RAG system.
 - users can uploads multiples PDFs from their choice.
 - users can ask questions regarding their data they uploaded

# How to install and run this code?
We can clone the repository by copying and pasting in your terminal: 
- `git clone https://github.com/Roseco-crs/RAG_Retrieval_Augmented_Generation_crs.git`
- `python main.py`



