from transcriber import AudioVideoTranscriber
import json

def main():
    # Initialize transcriber with turbo model (latest, fastest v3 model)
    transcriber = AudioVideoTranscriber(model_size="turbo")
    
    # Example file path - replace with your actual file
    file_path = "sample_audio.mp3"  # Change this to your file
    
    try:
        # Method 1: Basic transcription with timestamps
        print("=== Basic Transcription ===")
        result = transcriber.transcribe_file(file_path)
        print(f"Full text: {result['text']}")
        print(f"Language detected: {result['language']}")
        print(f"Number of segments: {len(result['segments'])}")
        
        # Method 2: Chunked transcription for RAG
        print("\n=== Chunked Transcription for RAG ===")
        chunks = transcriber.get_chunked_transcription(
            file_path, 
            chunk_duration=30  # 30-second chunks
        )
        
        print(f"Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
            print(f"\nChunk {i+1}:")
            print(f"  Time: {chunk['start_time']:.1f}s - {chunk['end_time']:.1f}s")
            print(f"  Text: {chunk['text'][:100]}...")
        
        # Method 3: Save results
        print("\n=== Saving Results ===")
        transcriber.save_transcription(result, "transcription_full.json")
        
        # Save chunks for RAG processing
        with open("transcription_chunks.json", "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        print("Chunks saved to transcription_chunks.json")
        
        # Show RAG-ready format
        print("\n=== RAG-Ready Format ===")
        rag_documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                "id": f"chunk_{i}",
                "content": chunk['text'],
                "metadata": {
                    "start_time": chunk['start_time'],
                    "end_time": chunk['end_time'],
                    "duration": chunk['end_time'] - chunk['start_time'],
                    "source_file": file_path
                }
            }
            rag_documents.append(doc)
        
        with open("rag_documents.json", "w", encoding="utf-8") as f:
            json.dump(rag_documents, f, indent=2, ensure_ascii=False)
        print("RAG-ready documents saved to rag_documents.json")
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        print("Please update the file_path variable with your actual audio/video file.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 