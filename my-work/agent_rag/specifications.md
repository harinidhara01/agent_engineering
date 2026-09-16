# Employee Policy Assistant

## Requirements

1. Build a web app called **Employee Policy Assistant** using **Flask**, with four pages switchable by tabs/buttons at the top:

   * **Assistant**
   * **Evidence**
   * **Execution Trace**
   * **Knowledge Base**

2. **Assistant page**

   * Initially show a welcome message, question text box, **Submit**, and **Clear** buttons.
   * Support multiple conversations and a **New Chat** option.
   * Send every question to a backend Agent.
   * For employee-policy questions, the Agent should use RAG against the policy knowledge base.
   * Generate the final response using a low-cost **Gemini model**.
   * Display clickable citations for information retrieved from policy documents.
   * If the answer cannot be found in the knowledge base, clearly state that it was not found instead of hallucinating.

3. **Evidence page**

   * Open when a user clicks a citation.
   * Divide the page into two panes:

     * **Left:** user conversation, question, and assistant response.
     * **Right:** source document and the relevant page/section.
   * Highlight the retrieved text/chunk used to generate the response.
   * For tool-generated answers, show the tool name, inputs, returned information, and source instead of a document.
   * Clearly distinguish **Document Evidence** and **Tool Evidence**.

4. **Execution Trace page**

   * Show the high-level flow for each request:

   ```text
   User Request
        ↓
      Agent
        ↓
   RAG / Tool Selection
        ↓
   Vector DB / Tool
        ↓
   Retrieved Context / Tool Result
        ↓
       Gemini
        ↓
      Response
   ```

   * Display Trace ID, timestamp, component, status, duration, retrieved documents/chunks, tool calls, Gemini model, and final response.
   * Do not expose chain-of-thought or hidden reasoning.

5. **Knowledge Base page**

   * Allow users to upload PDF, TXT, and DOCX employee-policy documents.
   * Show the ingestion process:

   ```text
   Upload
      ↓
   Duplicate Check
      ↓
   Extract Text
      ↓
   Chunk
      ↓
   Generate Embeddings
      ↓
   Store in ChromaDB
   ```

   * Show ingestion progress in the UI.
   * Display indexed documents, status, chunk count, and vector database statistics.
   * Provide a **View Chunks** option showing document, page, section, chunk ID, and chunk text.

6. **Duplicate detection**

   * Check for duplicate documents before ingestion.
   * Use a content hash such as SHA-256 rather than filename alone.
   * Detect duplicates even when the same document has a different filename.
   * Give the user the option to cancel or replace the existing document.

7. **Embeddings**

   * Use a **Hugging Face embedding model locally**.
   * Make the model configurable through `.env`.
   * Default to:

   ```text
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

   * Do not require Ollama for embeddings.

8. **Vector database**

   * Use **ChromaDB** as the local/private vector database.
   * Store it under:

   ```text
   database/vector_db/
   ```

   * Store metadata with every chunk:

   ```text
   document_id
   filename
   page
   section
   chunk_id
   chunk_index
   text
   ```

9. **Gemini**

   * Use the **existing Gemini API key from the `.env` file only**.
   * Do not ask the user for another API key.
   * Do not hard-code the API key.
   * Use a configurable, low-cost Gemini model through:

   ```text
   GEMINI_MODEL=
   ```

   * All Gemini calls must be made from backend Python code.

10. **Agent and tools**

    * Create a backend Agent that decides whether to use RAG or a tool.
    * Initially provide:

      * `policy_search` — searches the employee-policy vector database.
      * `regional_holiday_tool` — retrieves holidays for a requested region/year from a source that does not require an API key where practical.
    * The architecture should allow additional tools to be added later.

11. Example Agent behavior:

    Policy question:

    ```text
    User
      ↓
    Agent
      ↓
    policy_search
      ↓
    ChromaDB
      ↓
    Retrieved Context
      ↓
    Gemini
      ↓
    Answer + Citation
    ```

    Holiday question:

    ```text
    User
      ↓
    Agent
      ↓
    regional_holiday_tool
      ↓
    Tool Result
      ↓
    Gemini
      ↓
    Answer + Tool Evidence
    ```

12. **Backend/frontend**

    * All backend code must be written in Python.
    * Use Flask for the web application.
    * Use HTML, CSS, and JavaScript for the frontend.
    * The frontend must never directly call Gemini, ChromaDB, Hugging Face models, or external APIs.
    * All external calls must go through backend Python code.

13. **Logging**

    * Log Gemini, vector database, embedding, Agent, and tool interactions in:

    ```text
    database/logs.json
    ```

    * Each log should include:

      * timestamp
      * trace/request ID
      * component
      * call type
      * input/arguments
      * output/response
      * duration
      * status

    * Do not log embeddings, vectors, binary files, images, or other non-text content.

14. **Storage**

    ```text
    database/
    ├── vector_db/
    ├── app.db
    └── logs.json
    ```

    Use SQLite for conversations and execution traces.

15. **Configuration**

    Use `.env`:

    ```text
    GEMINI_API_KEY=
    GEMINI_MODEL=
    EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
    VECTOR_DB_PATH=database/vector_db
    TOP_K=3
    CHUNK_SIZE=
    CHUNK_OVERLAP=
    ```

    Never hard-code secrets.

16. **Project structure**

    Keep the implementation simple:

    ```text
    employee-policy-assistant/
    ├── app.py
    ├── agent.py
    ├── rag.py
    ├── tools.py
    ├── database.py
    ├── config.py
    ├── requirements.txt
    ├── .env.example
    ├── README.md
    │
    ├── documents/
    ├── database/
    ├── templates/
    │   ├── base.html
    │   ├── assistant.html
    │   ├── evidence.html
    │   ├── trace.html
    │   └── knowledge_base.html
    │
    ├── static/
    │   ├── style.css
    │   └── app.js
    │
    └── tests/
    ```

    Do not unnecessarily create separate modules for chunking, embeddings, retrieval, or vector storage. Keep the initial RAG implementation in `rag.py`.

17. Provide a few fictional sample policy documents:

    ```text
    Leave_Policy.pdf
    Remote_Work_Policy.pdf
    Travel_Expense_Policy.pdf
    Benefits_Guide.pdf
    Working_Hours_Policy.pdf
    ```

18. Example questions:

    ```text
    What is the vacation policy?

    How many days of parental leave are available?

    Can employees work remotely?

    What is the business meal reimbursement limit?

    What holidays are observed in Ohio in 2026?
    ```

19. Handle errors gracefully, including:

    * Empty questions
    * Invalid documents
    * Duplicate documents
    * Failed document parsing
    * Embedding errors
    * ChromaDB errors
    * Gemini errors
    * Tool errors
    * No relevant RAG results

20. Create `README.md` containing:

    * System description
    * Architecture
    * Required components
    * Installation
    * `.env` configuration
    * How to start the application
    * How to stop the application
    * How to upload documents
    * How to use the Assistant
    * How to view Evidence
    * How to view Execution Trace
    * Example questions

21. The final application must demonstrate this complete flow:

    ```text
                 KNOWLEDGE BASE
                       │
                  Upload Policy
                       ↓
                  Duplicate Check
                       ↓
                     Parse
                       ↓
                     Chunk
                       ↓
             Hugging Face Embeddings
                       ↓
                    ChromaDB
                       │
                       │
    ```

USER ───────────► AGENT
│
┌─────┴─────┐
▼           ▼
RAG        TOOL
│           │
▼           ▼
ChromaDB   Tool Source
│           │
└─────┬─────┘
↓
Gemini
↓
Answer + Citation
│
┌──────┴──────┐
▼             ▼
Evidence       Trace
│
▼
Highlighted Source
```

22. Prioritize a **simple, working, end-to-end demonstration** over complex architecture or unnecessary features.
