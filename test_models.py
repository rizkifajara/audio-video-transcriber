from transcriber import AudioVideoTranscriber
import time

def test_model_comparison(file_path: str, models: list = ["tiny", "base", "turbo"]):
    """
    Test different Whisper models for comparison.
    
    Args:
        file_path: Path to your audio/video file
        models: List of model sizes to test
    """
    results = {}
    
    for model_size in models:
        print(f"\n{'='*50}")
        print(f"Testing {model_size.upper()} model")
        print(f"{'='*50}")
        
        try:
            # Initialize transcriber
            start_time = time.time()
            transcriber = AudioVideoTranscriber(model_size=model_size)
            load_time = time.time() - start_time
            
            # Transcribe
            start_time = time.time()
            result = transcriber.transcribe_file(file_path)
            transcribe_time = time.time() - start_time
            
            # Store results
            results[model_size] = {
                'load_time': load_time,
                'transcribe_time': transcribe_time,
                'text_length': len(result['text']),
                'language': result['language'],
                'segments': len(result['segments']),
                'text_preview': result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
            }
            
            print(f"✅ Model loaded in: {load_time:.1f}s")
            print(f"✅ Transcribed in: {transcribe_time:.1f}s")
            print(f"✅ Language detected: {result['language']}")
            print(f"✅ Text length: {len(result['text'])} characters")
            print(f"✅ Number of segments: {len(result['segments'])}")
            print(f"✅ Preview: {results[model_size]['text_preview']}")
            
        except Exception as e:
            print(f"❌ Error with {model_size} model: {e}")
            results[model_size] = {'error': str(e)}
    
    # Summary comparison
    print(f"\n{'='*50}")
    print("COMPARISON SUMMARY")
    print(f"{'='*50}")
    
    for model, data in results.items():
        if 'error' not in data:
            print(f"\n{model.upper()} Model:")
            print(f"  Load Time: {data['load_time']:.1f}s")
            print(f"  Transcribe Time: {data['transcribe_time']:.1f}s")
            print(f"  Total Time: {data['load_time'] + data['transcribe_time']:.1f}s")
            print(f"  Text Length: {data['text_length']} chars")
        else:
            print(f"\n{model.upper()} Model: FAILED - {data['error']}")
    
    return results

if __name__ == "__main__":
    # Test file path - update this to your actual file
    test_file = "sample_audio.mp3"  # Change this to your file
    
    print("🎯 Model Comparison Test")
    print("This will test tiny vs base vs TURBO (latest v3) models")
    
    # Test models including the new turbo model
    models_to_test = ["tiny", "base", "turbo"]
    
    try:
        results = test_model_comparison(test_file, models_to_test)
        print(f"\n✅ Test completed! Results saved in memory.")
        
        print(f"\n🔥 TURBO MODEL INFO:")
        print(f"   - Latest Whisper v3-turbo (Oct 2024 release)")
        print(f"   - 8x faster than large-v3")
        print(f"   - Based on large-v3 with 4 decoder layers instead of 32")
        print(f"   - Best speed/accuracy balance available")
        
    except FileNotFoundError:
        print(f"❌ File not found: {test_file}")
        print("Please update the test_file variable with your actual audio/video file path.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}") 