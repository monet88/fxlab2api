# Flow2API Documentation - API Reference

## 🚀 Overview

Flow2API provides an OpenAI-compatible API interface for Google's VideoFX platform. This allows developers to use familiar OpenAI API patterns to generate images and videos through Google's AI models.

## 📡 Base URL

**Local Development:**
```
http://localhost:8000
```

**Production (replace with your deployed URL):**
```
https://your-domain.com
```

> **Note:** When using Cloudflare Tunnel, your URL will look like:
> `https://xxx-xxx-xxx.trycloudflare.com`

## 🔑 Authentication

All API requests require authentication using an API key passed in the Authorization header:

```http
Authorization: Bearer YOUR_API_KEY
```

The API key is configured in the admin panel or `config/setting.toml` file.

---

## 📋 Available Models

### Image Generation Models

| Model ID | Description | Aspect Ratio | Supports Input Image |
|----------|-------------|--------------|---------------------|
| `gemini-2.5-flash-image-landscape` | Gemini 2.5 Flash | 16:9 Landscape | ✅ Yes |
| `gemini-2.5-flash-image-portrait` | Gemini 2.5 Flash | 9:16 Portrait | ✅ Yes |
| `gemini-3.0-pro-image-landscape` | Gemini 3.0 Pro | 16:9 Landscape | ✅ Yes |
| `gemini-3.0-pro-image-portrait` | Gemini 3.0 Pro | 9:16 Portrait | ✅ Yes |
| `imagen-4.0-generate-preview-landscape` | Imagen 4.0 | 16:9 Landscape | ✅ Yes |
| `imagen-4.0-generate-preview-portrait` | Imagen 4.0 | 9:16 Portrait | ✅ Yes |

### Video Generation Models

#### Text-to-Video (T2V) - Text prompt only, no image input

| Model ID | Description | Aspect Ratio | Image Support |
|----------|-------------|--------------|---------------|
| `veo_3_1_t2v_fast_portrait` | Veo 3.1 Fast | 9:16 Portrait | ❌ None |
| `veo_3_1_t2v_fast_landscape` | Veo 3.1 Fast | 16:9 Landscape | ❌ None |
| `veo_2_1_fast_d_15_t2v_portrait` | Veo 2.1 Fast | 9:16 Portrait | ❌ None |
| `veo_2_1_fast_d_15_t2v_landscape` | Veo 2.1 Fast | 16:9 Landscape | ❌ None |
| `veo_2_0_t2v_portrait` | Veo 2.0 | 9:16 Portrait | ❌ None |
| `veo_2_0_t2v_landscape` | Veo 2.0 | 16:9 Landscape | ❌ None |

#### Image-to-Video (I2V) - First/Last Frame Control

| Model ID | Description | Aspect Ratio | Image Support |
|----------|-------------|--------------|---------------|
| `veo_3_1_i2v_s_fast_fl_portrait` | Veo 3.1 Fast | 9:16 Portrait | 1-2 images |
| `veo_3_1_i2v_s_fast_fl_landscape` | Veo 3.1 Fast | 16:9 Landscape | 1-2 images |
| `veo_2_1_fast_d_15_i2v_portrait` | Veo 2.1 Fast | 9:16 Portrait | 1-2 images |
| `veo_2_1_fast_d_15_i2v_landscape` | Veo 2.1 Fast | 16:9 Landscape | 1-2 images |
| `veo_2_0_i2v_portrait` | Veo 2.0 | 9:16 Portrait | 1-2 images |
| `veo_2_0_i2v_landscape` | Veo 2.0 | 16:9 Landscape | 1-2 images |

> **I2V Notes:**
> - **1 image**: Used as the **first frame** of the video
> - **2 images**: First image = **start frame**, Second image = **end frame**

#### Multi-Reference Image-to-Video (R2V) - Multiple Reference Images

| Model ID | Description | Aspect Ratio | Image Support |
|----------|-------------|--------------|---------------|
| `veo_3_0_r2v_fast_portrait` | Veo 3.0 Fast | 9:16 Portrait | Unlimited |
| `veo_3_0_r2v_fast_landscape` | Veo 3.0 Fast | 16:9 Landscape | Unlimited |

> **R2V Notes:**
> - Can use **multiple reference images** to guide video generation
> - Images are used as style/content references, not as frames

---

## 🔌 API Endpoints

### List Models

Get a list of all available models.

```http
GET /v1/models
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "gemini-2.5-flash-image-landscape",
      "object": "model",
      "owned_by": "flow2api",
      "description": "Image generation - GEM_PIX"
    },
    {
      "id": "veo_3_1_t2v_fast_landscape",
      "object": "model",
      "owned_by": "flow2api",
      "description": "Video generation - veo_3_1_t2v_fast"
    }
  ]
}
```

### Create Chat Completion

Generate images or videos using the chat completions endpoint (OpenAI-compatible).

```http
POST /v1/chat/completions
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Request Body:**
```json
{
  "model": "model-id",
  "messages": [
    {
      "role": "user",
      "content": "Your prompt here"
    }
  ],
  "stream": true
}
```

> ⚠️ **Important:** Always set `"stream": true` for actual generation. Non-streaming mode only checks token availability.

---

## 📝 Usage Examples

### 1. Text-to-Image Generation

Generate an image from a text prompt.

#### cURL
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [
      {
        "role": "user",
        "content": "A serene mountain landscape at sunset with a lake reflection"
      }
    ],
    "stream": true
  }'
```

#### Python
```python
import requests

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [
        {
            "role": "user",
            "content": "A serene mountain landscape at sunset with a lake reflection"
        }
    ],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

#### JavaScript (Node.js)
```javascript
const response = await fetch("http://localhost:8000/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gemini-2.5-flash-image-landscape",
    messages: [
      {
        role: "user",
        content: "A serene mountain landscape at sunset with a lake reflection"
      }
    ],
    stream: true
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(decoder.decode(value));
}
```

---

### 2. Image-to-Image Generation (Style Transfer/Edit)

Transform an existing image using a prompt.

#### cURL
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "imagen-4.0-generate-preview-landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Transform this image into a watercolor painting style"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

#### Python
```python
import requests
import base64

# Read and encode image
with open("input_image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "imagen-4.0-generate-preview-landscape",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Transform this image into a watercolor painting style"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

---

### 3. Text-to-Video Generation (T2V)

Generate a video from text prompt only. No image input supported.

#### cURL
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_1_t2v_fast_landscape",
    "messages": [
      {
        "role": "user",
        "content": "A time-lapse of a flower blooming in a garden with soft morning light"
      }
    ],
    "stream": true
  }'
```

#### Python
```python
import requests

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "veo_3_1_t2v_fast_landscape",
    "messages": [
        {
            "role": "user",
            "content": "A time-lapse of a flower blooming in a garden with soft morning light"
        }
    ],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

---

### 4. Image-to-Video with First Frame Only (I2V - 1 Image)

Use an image as the starting frame of the video.

#### cURL
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_1_i2v_s_fast_fl_landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "The camera slowly zooms out revealing more of the scene"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<first_frame_base64>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

#### Python
```python
import requests
import base64

# Read first frame image
with open("first_frame.jpg", "rb") as f:
    first_frame_base64 = base64.b64encode(f.read()).decode('utf-8')

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "veo_3_1_i2v_s_fast_fl_landscape",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "The camera slowly zooms out revealing more of the scene"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{first_frame_base64}"
                    }
                }
            ]
        }
    ],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

---

### 5. Image-to-Video with First AND Last Frames (I2V - 2 Images)

Control both the starting and ending frames of the video.

#### cURL
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_1_i2v_s_fast_fl_landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Smooth transition from day to night in a city skyline"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<first_frame_base64>"
            }
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<last_frame_base64>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

#### Python
```python
import requests
import base64

# Read first and last frame images
with open("day_city.jpg", "rb") as f:
    first_frame_base64 = base64.b64encode(f.read()).decode('utf-8')
    
with open("night_city.jpg", "rb") as f:
    last_frame_base64 = base64.b64encode(f.read()).decode('utf-8')

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "veo_3_1_i2v_s_fast_fl_landscape",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Smooth transition from day to night in a city skyline"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{first_frame_base64}"
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{last_frame_base64}"
                    }
                }
            ]
        }
    ],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

---

### 6. Multi-Reference Image-to-Video (R2V)

Use multiple reference images to guide video generation (style, characters, objects).

#### cURL
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_0_r2v_fast_landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "A character walking through a scenic forest path, maintaining consistent style and appearance"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<character_reference_base64>"
            }
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<environment_reference_base64>"
            }
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<style_reference_base64>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

#### Python
```python
import requests
import base64
import glob

# Read multiple reference images
reference_images = []
for image_path in glob.glob("references/*.jpg"):
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
        reference_images.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img_base64}"
            }
        })

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Build content array with text prompt + all reference images
content = [
    {
        "type": "text",
        "text": "A character walking through a scenic forest path, maintaining consistent style"
    }
] + reference_images

data = {
    "model": "veo_3_0_r2v_fast_landscape",
    "messages": [
        {
            "role": "user",
            "content": content
        }
    ],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

---

## 🔄 Streaming Response Format

Flow2API uses Server-Sent Events (SSE) for streaming responses. The response follows OpenAI's streaming pattern.

### Progress Updates (reasoning_content)

During generation, you'll receive progress updates in `reasoning_content`:

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1234567890,"model":"flow2api","choices":[{"index":0,"delta":{"role":"assistant","reasoning_content":"✨ Image generation task started\n"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1234567890,"model":"flow2api","choices":[{"index":0,"delta":{"reasoning_content":"正在生成图片...\n"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1234567890,"model":"flow2api","choices":[{"index":0,"delta":{"reasoning_content":"进度: 50%\n"},"finish_reason":null}]}
```

### Final Result (content)

The final result is delivered in `content` with `finish_reason: "stop"`:

**Image Result:**
```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1234567890,"model":"flow2api","choices":[{"index":0,"delta":{"content":"![Generated Image](https://storage.googleapis.com/ai-sandbox-videofx/image/...)"},"finish_reason":"stop"}]}

data: [DONE]
```

**Video Result:**
```
data: {"id":"chatcmpl-456","object":"chat.completion.chunk","created":1234567890,"model":"flow2api","choices":[{"index":0,"delta":{"content":"<video src='https://storage.googleapis.com/...' controls style='max-width:100%'></video>"},"finish_reason":"stop"}]}

data: [DONE]
```

### Parsing Streaming Response (Python)

```python
import requests
import json

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [{"role": "user", "content": "A cute cat"}],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)

result_url = None
for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data: '):
            json_str = line_str[6:]  # Remove 'data: ' prefix
            if json_str == '[DONE]':
                break
            try:
                chunk = json.loads(json_str)
                delta = chunk['choices'][0]['delta']
                
                # Progress updates
                if 'reasoning_content' in delta:
                    print(f"Progress: {delta['reasoning_content']}", end='')
                
                # Final result
                if 'content' in delta:
                    result_url = delta['content']
                    print(f"\nResult: {result_url}")
                    
            except json.JSONDecodeError:
                pass

print(f"\nFinal URL: {result_url}")
```

---

## 📊 Response Formats

### Successful Image Generation

The final chunk contains a markdown image:

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1234567890,
  "model": "flow2api",
  "choices": [{
    "index": 0,
    "delta": {
      "content": "![Generated Image](https://storage.googleapis.com/ai-sandbox-videofx/image/uuid?signature...)"
    },
    "finish_reason": "stop"
  }]
}
```

### Successful Video Generation

The final chunk contains an HTML video element:

```json
{
  "id": "chatcmpl-456",
  "object": "chat.completion.chunk",
  "created": 1234567890,
  "model": "flow2api",
  "choices": [{
    "index": 0,
    "delta": {
      "content": "<video src='https://storage.googleapis.com/ai-sandbox-videofx/video/uuid?signature...' controls style='max-width:100%'></video>"
    },
    "finish_reason": "stop"
  }]
}
```

### Extracting URLs from Response

**For Images (Markdown format):**
```python
import re

content = "![Generated Image](https://storage.googleapis.com/...)"
match = re.search(r'\!\[.*?\]\((.*?)\)', content)
if match:
    image_url = match.group(1)
```

**For Videos (HTML format):**
```python
import re

content = "<video src='https://storage.googleapis.com/...' controls>"
match = re.search(r"src='(.*?)'", content)
if match:
    video_url = match.group(1)
```

---

## ⚠️ Error Handling

### 400 Bad Request
```json
{
  "detail": "Messages cannot be empty"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid API key"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Generation failed: No available tokens"
}
```

### Model-Specific Errors

**T2V with images:**
```json
{
  "detail": "⚠️ Text-to-Video models do not support image input"
}
```

**I2V with wrong image count:**
```json
{
  "detail": "❌ I2V models require 1-2 images, but received 3"
}
```

---

## 🔧 Model Selection Guide

### Quick Reference

| Use Case | Recommended Model |
|----------|-------------------|
| Fast image generation | `gemini-2.5-flash-image-*` |
| High quality image | `gemini-3.0-pro-image-*` or `imagen-4.0-*` |
| Fast video from text | `veo_3_1_t2v_fast_*` |
| Video with start frame | `veo_3_1_i2v_s_fast_fl_*` |
| Video with start+end frames | `veo_3_1_i2v_s_fast_fl_*` |
| Video with multiple references | `veo_3_0_r2v_fast_*` |
| Social media (vertical) | `*_portrait` models |
| YouTube/TV (horizontal) | `*_landscape` models |

### Model Naming Convention

```
[model_family]_[version]_[type]_[variant]_[aspect]
```

- **model_family**: `gemini`, `imagen`, `veo`
- **version**: `2.5`, `3.0`, `4.0`, `2_0`, `2_1`, `3_0`, `3_1`
- **type**: `t2v` (text-to-video), `i2v` (image-to-video), `r2v` (reference-to-video)
- **variant**: `fast`, `d_15` (duration), `s_fast_fl` (short fast first/last)
- **aspect**: `portrait`, `landscape`

---

## 📚 Best Practices

1. **Always use streaming mode**: Set `"stream": true` for real-time progress updates and actual generation
2. **Handle SSE properly**: Parse each `data:` line separately
3. **Check for [DONE]**: The stream ends with `data: [DONE]`
4. **Extract URLs correctly**: Use regex to parse markdown/HTML format
5. **Base64 encoding**: Ensure images are properly base64-encoded with correct MIME type prefix
6. **Choose correct model type**:
   - T2V for text-only prompts
   - I2V for frame control
   - R2V for style/character consistency

---

## 🔍 Debugging Tips

1. **Enable debug mode** in config to see detailed logs
2. **Check token availability** using non-streaming mode first
3. **Verify image encoding**: Ensure base64 strings are valid
4. **Monitor progress**: Watch `reasoning_content` for generation status
5. **Check model compatibility**: Ensure image count matches model requirements

---

## 📖 Complete Python Client Example

```python
import requests
import json
import base64
import re
from typing import Optional, List

class Flow2APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def list_models(self):
        """List all available models"""
        response = requests.get(
            f"{self.base_url}/v1/models",
            headers=self.headers
        )
        return response.json()
    
    def generate_image(self, prompt: str, model: str = "gemini-2.5-flash-image-landscape",
                       input_images: Optional[List[str]] = None) -> str:
        """Generate an image from prompt"""
        content = self._build_content(prompt, input_images)
        return self._generate(model, content)
    
    def generate_video(self, prompt: str, model: str = "veo_3_1_t2v_fast_landscape",
                       input_images: Optional[List[str]] = None) -> str:
        """Generate a video from prompt"""
        content = self._build_content(prompt, input_images)
        return self._generate(model, content)
    
    def _build_content(self, prompt: str, image_paths: Optional[List[str]] = None):
        """Build content array with text and optional images"""
        if not image_paths:
            return prompt
        
        content = [{"type": "text", "text": prompt}]
        for path in image_paths:
            with open(path, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
            })
        return content
    
    def _generate(self, model: str, content) -> str:
        """Generate content and return result URL"""
        data = {
            "model": model,
            "messages": [{"role": "user", "content": content}],
            "stream": True
        }
        
        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            headers=self.headers,
            json=data,
            stream=True
        )
        
        result = None
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: ') and line_str != 'data: [DONE]':
                    try:
                        chunk = json.loads(line_str[6:])
                        delta = chunk['choices'][0]['delta']
                        if 'reasoning_content' in delta:
                            print(delta['reasoning_content'], end='')
                        if 'content' in delta:
                            result = delta['content']
                    except:
                        pass
        
        # Extract URL from result
        if result:
            # For images: ![...](url)
            img_match = re.search(r'\!\[.*?\]\((.*?)\)', result)
            if img_match:
                return img_match.group(1)
            # For videos: <video src='url'>
            vid_match = re.search(r"src='(.*?)'", result)
            if vid_match:
                return vid_match.group(1)
        return result


# Usage Example
if __name__ == "__main__":
    client = Flow2APIClient(
        base_url="http://localhost:8000",
        api_key="YOUR_API_KEY"
    )
    
    # List models
    models = client.list_models()
    print("Available models:", [m['id'] for m in models['data']])
    
    # Generate image
    image_url = client.generate_image(
        prompt="A beautiful sunset over the ocean",
        model="gemini-2.5-flash-image-landscape"
    )
    print(f"\nImage URL: {image_url}")
    
    # Generate video
    video_url = client.generate_video(
        prompt="Waves crashing on the beach",
        model="veo_3_1_t2v_fast_landscape"
    )
    print(f"\nVideo URL: {video_url}")
```

---

For more information, see the [Configuration Guide](./CONFIGURATION.md) and [Troubleshooting Guide](./TROUBLESHOOTING.md).