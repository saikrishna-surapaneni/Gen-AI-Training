# Gen-AI-Training
**7/01/2026**
Before getting into the main topic :
    lets understand the Human Intelligence, AI , GEN AI, NN and DL

**Human Intelligence :**

  Human intelligence is the complex ability to learn, reason, solve problems, adapt, and understand abstract concepts, involving cognitive functions like memory, perception, and decision-making, enabling effective interaction with the world through language, planning, and innovation, though its precise definition and measurement (like IQ) remain debated, with theories suggesting multiple types (e.g., emotional, spatial)

**Artificial Intelligence:**
    
   It does the same exact things what human can do but without emotions, consciousness --it can learn , reason , solve problems and so on ...

**GEN AI**
     It is a one kind of a AI -- where it can create content like text , video , audio , Doc etc, while traditional AI only for reasoning, analysis etc.

**Neural Network** :
     It is like a human brain without consiousness, where it is made up of thousands of transistors made by small workers and called has neurons 
       Each Neuron: 
          1. Listen to input , 2.Does small Calculation , 3.Passes the result forward.
     Example :
        A  NN is taught house prices
           it sees: 1.Area  2.Bedrooms  3.Location  ---so over time , it learns : " bigger the house usually costs more"
  
**DL** 
      Now coming to this we use n number of layers of neuron's to solve a problem 
        For instance, if we ask a NN "Look at the image and tell me what it is "   ---it struggles.
           Because, image have millions of pixels , speech has waves , languages has meaning and content, this small brain (N) cant handle that --
          says complex.
       So, this is where the DL comes into picture with 1000s, millions of layers combine as layers :
                now, 1st layer learns simple things 
                     2nd one learn pattern and Deep layer learns meaning..
      
**Correct Relationship of model**  :     
                   AI
                    └── Machine Learning (ML)
                             └── Neural Networks (NN)
                                       └── Deep Learning (DL)

Neuron → NN → DL → ML (category) → AI (goal/system)

** 8/01/2026**
**Tokens and Transformations :**
A token is a small, manageable unit of text that a machine can convert into numbers and process efficiently. 
  and every LLM has different tokenized number rather then same also not exact number but example number than later processed and                   
  get a result(prediction)..

  While Tranformation -- Changing something from one form into another so it becomes more useful.                                        
   For instance: if we give a sentence to a model, -- " this is an apple "
   model can understand numbers only , so that sentence will be chunks down to small texts and then transforms to a meaningful
  data by model using Transformations..

**Transformations do TWO things at the same time:**
          They help generate human-like language
           They create internal representations that have meaning to the model
                 > The human-readable text is just the surface result.
                 > The real intelligence lives inside the transformations.
**Token limit:**
          Every LLM has a fixed “max token limit”
           This is called the context window size.
               If a model has 32k tokens
                  Prompt (input) = 20k tokens
                  Answer (output) = 12k tokens
                             > Works
           But:
             Prompt = 30k
             Output = 5k
             Fails (exceeds limit)
     
**Parallelism** : 
Means:
  Doing many things at the same time instead of one after another.

**Cooking example**
Sequential (one by one):
Cook rice
Then cut vegetables
Then boil water
 -- that Takes long time.

**Parallel (at the same time)**:
Rice cooking
Vegetables cutting
Water boiling
 -- Much faster.
        That is parallelism.
        
**parallelism in Neural network**        
  In a neural network layer:
      Many neurons exist
      Each neuron computes at the same time
      Matrix multiplication happens in parallel
  --Whole layer processes together.
  
**Parallelism in Deep Learning**:
 When training:
   Millions of weights updated
   Thousands of operations run simultaneously
   GPUs process tensors in parallel
 --That’s why DL training is fast (relatively).
 
**Parallelism in Transformers**
Before (RNNs / LSTMs)
  Read text one word at a time
  Next word waits for previous word
  Slow
  Hard to scale
  Transformers
Read all tokens at once
Attention is computed in parallel
 Fast
 Scales to huge models
This is why:
  ChatGPT exists
  Large context windows are possible

In simple : Parallelism is the ability to process multiple operations or pieces of data simultaneously, rather than sequentially.
Connecting to what you already know
    Transformation → what changes the data
    Parallelism → how fast those changes happen
    Attention → decides what matters
    Tokens → units processed in parallel

 **09/01/2026**
 
**Embeddings**
  An embedding is a way to convert something (text, image, audio, etc.) into numbers so that similar things have similar numbers.
Why embeddings exist
  Computers don’t understand meaning.
  They only understand numbers.
  
  Embeddings are the bridge between:  
         human Meaning --- machine numbers

**Why not use unlimited dimensions?**

Because of:
1) Curse of dimensionality
2) Higher storage cost
3)Slower similarity search
4) Noise & diminishing returns

That’s why most models use:
384 – 2048 dimensions (sweet spot)

**Tasks**

1.Determine the requirements for building a video or image chatbot with streaming capabilities for images and videos using the concept of embeddings.
**Embedding Requirements**
    Embedding Types Needed
**Data Type**   	     **Embedding Model**
Image	            Vision embedding model (CLIP, ViT)
Video frame	        Image embedding model
Video clip	        Aggregated frame embeddings
Audio (optional)	Audio embeddings
Text	            Text embedding model

**Embedding Dimensions (Typical)**
**Model Type**	       **Dimensions**
Image (CLIP)	            512
Vision Transformer	     768 / 1024
Text embeddings	         768 / 1536

Each image/frame → 1 vector
Each video → many vectors

**Embedding Strategy**
**Image**
 1 image → 1 embedding

**Video**
 → Frames (every N seconds)
 → Each frame → embedding
 → Store with timestamp metadata

**Example metadata:**
{
  "video_id": "vid123",
  "frame_time": "00:01:32",
  "embedding": [...]
}

**Vector Database Requirements**
  **Capabilities Needed**

High-dimensional vector storage
Cosine similarity / dot product
Metadata filtering
Fast ANN (Approximate Nearest Neighbor)
Horizontal scaling

 **Suitable Databases**
Pinecone
Weaviate
FAISS
Milvus
MongoDB Atlas Vector Search

**Query Flow (User Interaction)**
**Example Query**
“Show me scenes where a person is holding a phone”
**Steps:**
Convert query → text embedding
Search vector DB against image/video embeddings
Retrieve top-K matching frames
Group frames → scenes
Send context to LLM
Stream response + thumbnails

2.Identify which models support which embedding dimensions. 
  A dimension is one numeric feature used to represent meaning.

**An embedding is just a vector:**
[0.12, -0.98, 1.44, ...]

**If there are:**
3 numbers → 3 dimensions
768 numbers → 768 dimensions
1536 numbers → 1536 dimensions

So:
Embedding dimension = how much “space” the model has to store meaning

**Real-world analogy** :
Think of describing a person:
Height,
Weight,
Age,
Skin tone,
Accent,
Emotion,
Profession.

  Each attribute = one dimension

  More dimensions → richer description
  Too many → noisy, expensive, inefficient


**Retrieval-Augmented Generation (RAG)**
 
1_ingestion_pipeline.py (MOST IMPORTANT)
What problem it solves

LLMs cannot read PDFs or documents directly.

So we must:
Load documents
Split them into chunks
Convert text → embeddings
Store embeddings in a vector database

Core pipeline
Documents → Chunks → Embeddings → Vector Store

Key libraries used

langchain.document_loaders ,
langchain.text_splitter ,
langchain.embeddings ,
langchain.vectorstores

Why this file is critical

Every enterprise RAG starts here:
Company policies,
Internal manuals,
Codebases,
Knowledge bases

 If ingestion is wrong → entire RAG fails

**Chunking, embedding model choice, and metadata design happen here**

**2_retrieval_pipeline.py**
What it does
When a user asks a question:
Convert the query into an embedding ,
Search the vector database,
Retrieve top-k most relevant chunks

Key concept:
Semantic search ≠ keyword search

**Example:**
  User query: “How do I reset my password?”
  Matches text: “Steps to recover login credentials”

Why it matters
Directly controls:
Accuracy ,
Hallucination rate ,
Latency

Poor retrieval = poor answers (even with a strong LLM)

**3_answer_generation.py**
Where the LLM is used

**Flow**
User Query
   ↓
Retriever
   ↓
Relevant Context
   ↓
Prompt to LLM
   ↓
Final Answer

Prompt pattern:   
 Use ONLY the following context to answer the question:
 <context>

Why this is critical

Prevents hallucinations
Makes responses auditable
Mandatory in enterprise GenAI systems

**4_history_aware_generation.py**
What it adds   
Conversation memory

The system can now understand:   
“What about step 3?”
“Explain that again”
based on previous messages.

Real-world usage:   
 Chatbots
 Customer support systems
 Virtual assistants
 Helpdesk automation

**CHUNKING STRATEGIES (Files 5 → 7)**

Chunking quality directly affects retrieval quality

**5_recursive_character_text_spliiter.p**y
What it does

Basic chunking using:
Paragraphs ,
Sentences ,
Fixed character limits

Problems
 Can break meaning ,
 Loses semantic structure

**6_semantic_chunking.py**
Smarter chunking

Splits based on:
Meaning

Topic boundaries
Semantic similarity

Why companies prefer this
Higher retrieval accuracy ,
Fewer irrelevant chunks ,
Better context alignment

**7_agentic_chunking.py**
Next-gen chunking 

Uses an LLM itself to decide:
Where to split  ,
What forms a logical unit

Used for
Legal documents ,
Medical records ,
Contracts ,
Compliance docs

This represents production-grade RAG

**MULTI-MODAL RAG (File 8)** 

**8_multi_modal_rag.ipynb**
What it teaches

RAG is not limited to text.
Supports:  
Text ,
Images ,
Diagrams

Flowcharts

Flow
Image → Vision Embeddings
Text  → Text Embeddings
↓
Store together
↓
Retrieve both

Real-world usage: 
Manufacturing manuals ,
Medical imaging + reports ,
Architecture & engineering diagrams

**ADVANCED RETRIEVAL (Files 9 → 13)**

This is where enterprise RAG systems outperform basic ones

**9_retrieval_methods.py**
Retrieval strategies

Similarity search
MMR (Max Marginal Relevance – diversity-aware)

**10_multi_query_retrieval.py**
Problem
Users ask vague or incomplete questions.

Solution
LLM generates:

Original Query → Multiple rephrased queries

Benefit
Improves recall significantly

**11_reciprocal_rank_fusion.py**
What it does
Combines results from:
Multiple retrievers ,
Multiple strategies

Ranks them intelligently.

Used in  
Search engines ,
Enterprise knowledge systems

**12_hybrid_search.ipynb**
Hybrid = Keyword + Vector Search

Combines:
BM25 (keyword accuracy)
Embeddings (semantic understanding)

Best for
Legal search ,
Product catalogs ,
Structured enterprise data

**13_reranker.ipynb**
Final accuracy booster
LLM re-ranks retrieved chunks before answering.

Pipeline
Retrieve top 20 → Re-rank → Use top 5

This is industry standard in 2024+

**Evaluation**
synthetic_questions.txt

Used to:
Measure accuracy
Test retrieval quality
Compare chunking and retrieval strategies







