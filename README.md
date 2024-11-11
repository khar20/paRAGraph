# paRAGraph: AI-Driven Storytelling and Chatbot Application

## Overview
paRAGraph is an AI-powered storytelling and chatbot application that integrates Ollama's conversational AI with TimescaleDB to provide contextually enriched responses. The application fetches relevant fragments from past user interactions and story data using vector embeddings, creating a seamless conversational experience. The app also leverages TimescaleDB's vector extension, pgvector, and the pgai Vectorizer for efficient semantic search and fast similarity-based retrieval.

## Features
- **Context-Aware Responses**: Uses past chat history and story fragments to generate contextually relevant responses.
- **Vector Search**: Stores and queries vector embeddings of story fragments and conversation history using pgvector and pgai Vectorizer for efficient retrieval.
- **Seamless AI Integration**: Powered by Ollama’s Llama 3.2 model for generating dynamic conversational responses.

## Demo
You can explore the project on GitHub:
[paRAGraph GitHub Repository](https://github.com/khar20/paRAGraph)

To try the app, you can either:
- Use a Timescale service (with an OPENAI_API_KEY set) to run the provided `.sql` files, or
- Install the necessary extensions locally on your own TimescaleDB instance.

## Setup Instructions

### Prerequisites
- TimescaleDB (with pgvector and pgai Vectorizer extensions installed)
- OpenAI API key for generating embeddings (set in `.env` file)
- Python 3.x
- Flask for the web framework
- Ollama API for AI responses (Llama 3.2 model)

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/khar20/paRAGraph.git
    cd paRAGraph
    ```

2. Set up your TimescaleDB instance:
   - You can either use a hosted Timescale service or install TimescaleDB locally with the pgvector and pgai extensions.
   - Enable the required extensions: `pgvector` and `pgai`.
   - Create the necessary database and schema by running the provided `setup.sql` and `insert.sql` files to create tables and indexes needed for storing embeddings of story and chat history.

3. Create the `.env` file and update the following:
    ```
    DATABASE_URL: Your TimescaleDB connection URL.
    ```

4. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the application:
    ```bash
    python app.py
    ```
   The app will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage
- Visit the application in your web browser.
- Enter a query in the chat interface to interact with the AI.
- The app will fetch context from previous conversations and relevant story fragments (from the `insert.sql` file), enriching the AI’s responses.

## How It Works

1. **User Interaction**:
   When you visit the paRAGraph application in your web browser, you interact with a chat interface where you can ask the AI questions or engage in a conversation.

2. **Contextual Response Generation**:
   As you interact with the AI, the application not only generates responses based on the current input but also considers **context from previous conversations**. For example, if you mentioned a character or story element earlier in the chat, the AI will refer to this information and build upon it, providing more coherent responses.

3. **Semantic Search**:
   To generate context-aware responses, the application uses **vector embeddings** stored in TimescaleDB. The system uses **pgvector**'s indexes to perform semantic search.
   Vector embeddings are mathematical representations of words, sentences, or paragraphs. The system compares the current user input with stored embeddings from previous conversations or story fragments, finding semantically similar entries, not just those that match words exactly.

4. **Efficient Retrieval**:
   The system uses **pgvectorscale** to create **StreamingDiskANN indexes**. These indexes make it much faster to search through large amounts of data and retrieve the most relevant vector embeddings quickly.

5. **AI Response Generation**:
   After retrieving the relevant context, the data is sent to **Ollama’s Llama 3.2 model**, which generates a conversational response. The response is informed by the user’s current input and enriched by the retrieved context (previous interactions or story fragments). This makes the AI's replies more personalized, coherent, and relevant to the ongoing conversation.

6. **End Result**:
   The AI provides a response that is contextually enriched, drawing from both the current conversation and previous interactions. The more the user interacts, the more dynamic and personalized the experience becomes.

## Tools Used
- **TimescaleDB with pgvector**: Stores vector embeddings of story fragments and conversation history for efficient retrieval.
- **pgai Vectorizer**: Generates vector embeddings used for semantic search and context retrieval.
- **pgvectorscale**: Creates StreamingDiskANN indexes to speed up the retrieval of vector embeddings from large datasets.
- **Ollama**: Uses Ollama’s Llama 3.2 model for generating AI-based conversational responses.
