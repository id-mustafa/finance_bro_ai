# Purpose

The purpose of this document is to describe *how* the Finance Bro AI software shall fulfill the software requirements. It discusses the environment that the software will run in, the software system's architecture, functional specifications associated with each software requirement, and user interface mockups.

This document is written primarily for software engineers working on Finance Bro AI, who have the source code available in addition to this document.

# Scope

The scope of this SDS applies in its entirety to the Finance Bro AI project.

# Definitions

**Finance Bro AI** A financial assistant leveraging retrieval-augmented generation to provide context-aware answers to user queries.

**Chroma** A vector store used to store embeddings for efficient similarity search and retrieval.

**RetrievalQA** A chain combining a retriever and a large language model (LLM) to generate contextually aware answers.

**LLM** Large Language Model used to generate natural language responses, such as GPT-4.

# Acronyms and Abbreviations

**LLM** Large Language Model  
**UI** User Interface  
**API** Application Programming Interface

# Software Description

The Finance Bro AI consists of a web-based application built using Streamlit and LangChain components. It includes a custom-built retrieval system using Chroma as the vector store and OpenAI models for embeddings and responses.

## Features Controlled by Software

The software provides:

- User-friendly chat functionality for financial queries.
- Retrieval-based question answering with relevant sources.
- Management of conversation history for better context awareness.

## Intended Operational Environment

The application is intended to operate in a standalone environment on a server or personal machine with access to OpenAI's API for generating embeddings and responses. It uses a local Chroma vector store to store and retrieve document embeddings.

## Software Layers

The software consists of the following layers:

1. **User Interface Layer**: Developed in Streamlit, enabling interaction with the user.
2. **Retrieval Layer**: Handles fetching relevant documents using Chroma and LangChain’s retriever components.
3. **Processing Layer**: Includes the RetrievalQA chain for integrating LLM-generated answers with retrieved data.
4. **Indexing and Storage Layer**: Manages document embeddings and persistence via Chroma.

# Runtime Environment

The runtime environment includes the following components:

## Operating System

The application runs on any system capable of running Python 3.9 or later. Common environments include Windows, macOS, and Linux.

## Storage and Partitioning

Storage requirements depend on the size of the Chroma vector store and cached embeddings. Typically, the project requires 500MB to 1GB of storage for a medium-sized document corpus.

# Software Items

## Architecture Design Chart

Below is a high-level overview of the architecture:

![Architecture Diagram](/images/architecture/diagram.png)

### Components

- **User Interface**: Implements user interaction through Streamlit.
- **Retriever**: Uses Chroma for vector search.
- **LLM Integration**: Utilizes GPT-4 for generating natural language responses.
- **Document Indexing**: Handles text processing and embedding creation.

## Key Modules

### Chroma Vector Store
Responsible for storing and retrieving embeddings for documents.

### RetrievalQA
Combines retriever functionality with LLM to provide context-aware responses.

### Indexing
Manages the ingestion and splitting of documents into embeddings.

### Streamlit UI
Provides an interface for user input and displays results.

# Design Challenges

## Memory Management
The application does not implement long-term memory for conversations but maintains session-level context via Streamlit’s session state. This approach balances performance with user experience but limits historical context retention across sessions.

### Solution
To address this, a `RunnableWithMessageHistory` component can be integrated to persist conversation history efficiently, enabling a more robust user experience without overwhelming system resources. However this may be kept as a stretch goal due to time constraints.

## Embedding and Storage
Efficient handling of embeddings and retrievals was critical for ensuring fast response times and minimal resource consumption.

### Solution
Chroma’s vector store was selected for its performance and compatibility with LangChain, simplifying the integration process. 

## HuggingFace Open Source LLM Approach Had No Context Awareness
There was a lack of context awareness using this LLM and it couldn't interpret basic queries such as "hey." 

### Solution
To combat this, I moved over to a ChatGPT LLM approach to simplify the user experience. Now the RAG Application is powered behind the OpenAI gpt-4o model for better user interaction.


# Functional Specifications

## User Query Handling

*Requirement:* The system shall accept user queries and display answers generated by the RetrievalQA chain.  
*Functional Specifications:*
- Input: User text input.
- Output: Textual response along with relevant sources.

## Document Retrieval

*Requirement:* The system shall retrieve and rank relevant documents using Chroma.  
*Functional Specifications:*
- Input: User query.
- Output: Ranked list of relevant documents.

## Embedding Management

*Requirement:* The system shall manage and store embeddings for the document corpus.  
*Functional Specifications:*
- Input: Documents for indexing.
- Output: Stored embeddings in Chroma.

# User Interface Mockups

## Chat Interface

### Initial Screen
![Initial Screen](/images/ui-mockups/initial-screen.png)

### Query Response
![Query Response](/images/ui-mockups/query-response.png)

### Sources Expanded
![Sources Expanded](/images/ui-mockups/sources-expanded.png)

# Revision History

| Revision | Notes |
| --- | --- |
| 1 | Initial draft created for Finance Bro AI. |

