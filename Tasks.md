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
