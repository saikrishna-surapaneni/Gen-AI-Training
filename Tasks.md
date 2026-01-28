# GEN AI TRAINING – TASKS & SYSTEM DESIGN

## Task 1: Build a Video/Image Chatbot Using Embeddings

### Goal
Create a chatbot that can understand and retrieve information from:
- Images
- Video frames
- (Optional) Audio
- Text

---

## Embedding Types Needed

| Data Type            | Embedding Model Type |
|----------------------|----------------------|
| Image                | Vision model (CLIP, ViT) |
| Video Frame          | Same as image embedding |
| Video Clip           | Aggregated frame embeddings |
| Audio (optional)     | Audio embedding model |
| Text                 | Text embedding model |

---

## Typical Embedding Dimensions

| Model Type          | Dimensions |
|---------------------|------------|
| CLIP Image          |    512     |
| Vision Transformer  | 768 / 1024 |
| Text Embeddings     | 768 / 1536 |

---

## 🔹 Embedding Strategy

### Images
1 Image → 1 Embedding

### Videos
Video → Extract frames every N seconds  
Each frame → Embedding → Store with timestamp

**Example Metadata**
```json
{
  "video_id": "vid123",
  "frame_time": "00:01:32",
  "embedding": [...]
}

### **Vector Database Requirements**

**The database must support:**

High-dimensional vector storage
Cosine similarity / Dot product search
Metadata filtering
Fast Approximate Nearest Neighbor (ANN) search
Horizontal scaling

**Suitable Databases**
Pinecone
Weaviate
FAISS
Milvus
MongoDB Atlas Vector Search

**Query Flow (User Interaction)**

Example user query:
“Show me scenes where a person is holding a phone”

Steps:
1.Convert query → Text embedding
2.Search vector DB against stored image/video embeddings
3.Retrieve Top-K matching frames
4.Group nearby frames into scenes
5.Send scene context to LLM
6.Stream response + thumbnails to user


## **Task 2: Embedding Dimension Understanding**

An embedding is a vector:
[0.12, -0.98, 1.44, ...]

**|Number of Values	| Meaning       |**
  |-----------------|---------------|
  |3	              |3 dimensions   |
  |768	            |768 dimensions |
  |1536	            |1536 dimensions|

Embedding dimension = how much “space” a model has to store meaning.

### **Analogy**
Describing a person using attributes:
Height
Weight
Age
Profession
Emotion

Each attribute = one dimension

More dimensions → richer meaning
Too many → inefficient and noisy
