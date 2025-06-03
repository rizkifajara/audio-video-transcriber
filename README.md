# Audio-Video Transcriber for RAG

A Python-based transcription system using OpenAI Whisper (tiny model) for preparing audio and video content for Retrieval-Augmented Generation (RAG) systems.

## Features

- **Free & Local**: Uses OpenAI Whisper tiny model (runs entirely offline)
- **Multi-format Support**: Handles audio (MP3, WAV, M4A, FLAC, OGG) and video (MP4, AVI, MOV, MKV, WEBM)
- **Timestamp Precision**: Provides word-level timestamps for accurate chunking
- **RAG-Ready Output**: Automatically chunks transcriptions for vector database ingestion
- **Lightweight**: Uses the smallest Whisper model for faster processing

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg** (required for audio processing):
   
   **macOS**:
   ```bash
   brew install ffmpeg
   ```
   
   **Ubuntu/Debian**:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **Windows**:
   Download from https://ffmpeg.org/download.html

## Usage

### Basic Transcription

```python
from transcriber import AudioVideoTranscriber

# Initialize with tiny model (fastest)
transcriber = AudioVideoTranscriber(model_size="tiny")

# Transcribe a file
result = transcriber.transcribe_file("your_audio.mp3")
print(result['text'])
```

### RAG-Ready Chunking

```python
# Get 30-second chunks for RAG processing
chunks = transcriber.get_chunked_transcription(
    "your_audio.mp3", 
    chunk_duration=30
)

for chunk in chunks:
    print(f"Time: {chunk['start_time']}-{chunk['end_time']}s")
    print(f"Text: {chunk['text']}")
```

### Complete Example

Run the example script:
```bash
python example_usage.py
```

## Output Formats

### 1. Full Transcription
```json
{
  "text": "Complete transcription text...",
  "segments": [...],
  "language": "en"
}
```

### 2. RAG Chunks
```json
[
  {
    "text": "Chunk text content...",
    "start_time": 0.0,
    "end_time": 30.0,
    "words": [...]
  }
]
```

### 3. RAG Documents (Vector DB Ready)
```json
[
  {
    "id": "chunk_0",
    "content": "Text content...",
    "metadata": {
      "start_time": 0.0,
      "end_time": 30.0,
      "source_file": "audio.mp3"
    }
  }
]
```

## Supported Formats

**Audio**: MP3, WAV, M4A, FLAC, OGG
**Video**: MP4, AVI, MOV, MKV, WEBM

## Model Options

- `tiny`: Fastest, smallest (~39 MB) - **Default**
- `base`: Better accuracy (~74 MB)
- `small`: Good balance (~244 MB)
- `medium`: Higher accuracy (~769 MB)
- `large`: Best accuracy (~1550 MB)

## Integration with RAG Systems

The chunked output is designed to work with:
- **Vector Databases**: Chroma, Pinecone, Weaviate
- **Embedding Models**: OpenAI, Sentence-Transformers
- **RAG Frameworks**: LangChain, LlamaIndex

## Performance Notes

- **Tiny Model**: ~10x faster than large model, good enough for most use cases
- **Processing Speed**: ~2-5x real-time (varies by hardware)
- **Memory Usage**: Low (~200MB for tiny model)

## Next Steps for RAG

1. **Generate Embeddings**: Use your preferred embedding model on the chunks
2. **Store in Vector DB**: Insert chunks with embeddings and metadata
3. **Implement Retrieval**: Query by semantic similarity with timestamp context
4. **Citation Support**: Use timestamps to reference specific moments in audio/video 