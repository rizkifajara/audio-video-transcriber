import whisper
import os
from pathlib import Path
import json
from typing import Dict, List, Union

class AudioVideoTranscriber:
    def __init__(self, model_size: str = "tiny"):
        """
        Initialize the transcriber with Whisper model.
        
        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
        """
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")
    
    def transcribe_file(self, file_path: str, language: str = None) -> Dict:
        """
        Transcribe audio or video file with timestamps.
        
        Args:
            file_path: Path to audio/video file
            language: Optional language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            Dict with transcription results including segments with timestamps
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Transcribing: {file_path}")
        
        # Transcribe with word-level timestamps
        result = self.model.transcribe(
            file_path,
            language=language,
            word_timestamps=True
        )
        
        return result
    
    def get_chunked_transcription(self, file_path: str, chunk_duration: int = 30, language: str = None) -> List[Dict]:
        """
        Get transcription chunked by time intervals for RAG processing.
        
        Args:
            file_path: Path to audio/video file
            chunk_duration: Duration of each chunk in seconds
            language: Optional language code
            
        Returns:
            List of chunks with text, start_time, end_time
        """
        result = self.transcribe_file(file_path, language)
        
        chunks = []
        current_chunk = {
            'text': '',
            'start_time': 0,
            'end_time': 0,
            'words': []
        }
        
        for segment in result['segments']:
            segment_start = segment['start']
            segment_end = segment['end']
            segment_text = segment['text'].strip()
            
            # If segment fits in current chunk
            if segment_end <= current_chunk['start_time'] + chunk_duration:
                if not current_chunk['text']:
                    current_chunk['start_time'] = segment_start
                current_chunk['text'] += ' ' + segment_text
                current_chunk['end_time'] = segment_end
                if 'words' in segment:
                    current_chunk['words'].extend(segment['words'])
            else:
                # Save current chunk if it has content
                if current_chunk['text'].strip():
                    current_chunk['text'] = current_chunk['text'].strip()
                    chunks.append(current_chunk.copy())
                
                # Start new chunk
                current_chunk = {
                    'text': segment_text,
                    'start_time': segment_start,
                    'end_time': segment_end,
                    'words': segment.get('words', [])
                }
        
        # Add final chunk
        if current_chunk['text'].strip():
            current_chunk['text'] = current_chunk['text'].strip()
            chunks.append(current_chunk)
        
        return chunks
    
    def save_transcription(self, result: Dict, output_path: str):
        """Save transcription result to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Transcription saved to: {output_path}")
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported audio/video formats."""
        return [
            '.mp3', '.wav', '.m4a', '.flac', '.ogg',
            '.mp4', '.avi', '.mov', '.mkv', '.webm'
        ]

if __name__ == "__main__":
    # Example usage
    transcriber = AudioVideoTranscriber(model_size="tiny")
    
    # Example file path (replace with your actual file)
    # file_path = "path/to/your/audio_or_video_file.mp3"
    
    print("Transcriber initialized with tiny model.")
    print("Supported formats:", transcriber.get_supported_formats())
    print("\nUsage example:")
    print("transcriber.transcribe_file('your_file.mp3')")
    print("transcriber.get_chunked_transcription('your_file.mp3', chunk_duration=30)") 