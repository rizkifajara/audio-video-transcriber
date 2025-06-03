# Docker Usage Guide

This guide explains how to use the Docker Compose setup for the Audio-Video Transcriber project.

## Prerequisites

- Docker and Docker Compose installed
- Audio/video files to transcribe

## Quick Start

1. **Build and run the main transcriber service:**
   ```bash
   docker-compose up --build transcriber
   ```

2. **Place your audio/video files in the `input/` directory:**
   ```bash
   cp your_audio_file.mp3 input/
   ```

3. **Check results in the `output/` directory**

## Available Services

### 1. Main Transcriber Service (Default)
Runs the example transcription script:
```bash
docker-compose up transcriber
```

### 2. Interactive CLI
For development and custom scripts:
```bash
docker-compose --profile cli up transcriber-cli
```
This drops you into a bash shell inside the container where you can run:
```bash
python transcriber.py
python example_usage.py
```

### 3. Jupyter Lab
For interactive development and experimentation:
```bash
docker-compose --profile jupyter up jupyter
```
Then open: http://localhost:8888

### 4. API Service (Future)
Placeholder for web API development:
```bash
docker-compose --profile api up transcriber-api
```

## Directory Structure

```
project/
├── input/          # Place your audio/video files here
├── output/         # Transcription results appear here
├── docker-compose.yml
├── Dockerfile
└── ...
```

## Volume Mounts

- `./input:/app/input` - Input audio/video files
- `./output:/app/output` - Output transcription files
- `whisper-models:/root/.cache/whisper` - Cached Whisper models (persistent)

## Common Commands

### Run transcription on a specific file:
```bash
# Place file in input/ directory first
docker-compose run --rm transcriber python -c "
from transcriber import AudioVideoTranscriber
transcriber = AudioVideoTranscriber('tiny')
result = transcriber.transcribe_file('input/your_file.mp3')
transcriber.save_transcription(result, 'output/transcription.json')
"
```

### Interactive development:
```bash
docker-compose --profile cli up transcriber-cli
# Inside container:
python example_usage.py
```

### Jupyter for experimentation:
```bash
docker-compose --profile jupyter up jupyter
# Open http://localhost:8888 in browser
```

## Model Sizes

You can change the Whisper model size by modifying the transcriber initialization:
- `tiny` - Fastest, ~39MB (default)
- `base` - ~74MB
- `small` - ~244MB  
- `medium` - ~769MB
- `large` - ~1550MB

## Troubleshooting

### First run takes longer
The first run downloads the Whisper model. Subsequent runs use the cached model.

### Permission issues
If you get permission errors:
```bash
sudo chown -R $USER:$USER input output
```

### Model not found
Clear the model cache:
```bash
docker-compose down
docker volume rm audio-video-transcriber_whisper-models
```

### Container won't start
Rebuild the image:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Development Workflow

1. **Make code changes** in your local files
2. **Run with CLI service** for testing:
   ```bash
   docker-compose --profile cli up transcriber-cli
   ```
3. **Use Jupyter** for interactive development:
   ```bash
   docker-compose --profile jupyter up jupyter
   ```
4. **Rebuild when needed**:
   ```bash
   docker-compose build
   ```

## Production Tips

- Use specific model sizes based on your accuracy/speed requirements
- Mount specific input files instead of entire directories for better security
- Consider using Docker secrets for API keys if you extend the application
- Set resource limits in production environments 