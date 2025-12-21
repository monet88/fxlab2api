# Flow2API

**A full-featured OpenAI-compatible API service, providing a unified interface for Flow**

## ✨ Core Features

- 🎨 **Text-to-Image** / **Image-to-Image**
- 🎬 **Text-to-Video** / **Image-to-Video**
- 🎞️ **First and Last Frame Video**
- 🔄 **AT Auto-refresh**
- 📊 **Balance Display** - Real-time query and display VideoFX Credits
- 🚀 **Load Balancing** - Multi-token polling and concurrency control
- 🌐 **Proxy Support** - Supports HTTP/SOCKS5 proxy
- 📱 **Web Management Interface** - Intuitive token and configuration management

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- Or Python 3.8+

### Method 1: Docker Deployment (Recommended)

#### Standard Mode (No Proxy)

```bash
# Clone the project
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

#### WARP Mode (Using Proxy)

```bash
# Start with WARP proxy
docker-compose -f docker-compose.proxy.yml up -d

# View logs
docker-compose -f docker-compose.proxy.yml logs -f
```

### Method 2: Local Deployment

```bash
# Clone the project
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start service
python main.py
```

### First Access

After the service starts, visit the admin panel: **http://localhost:8000**

- **Username**: `admin`
- **Password**: `admin`

⚠️ **Important**: Please change the password immediately after first login!

## 📋 Supported Models

### Image Generation

| Model Name | Description | Size |
|---------|--------|--------|
| `gemini-2.5-flash-image-landscape` | Image/Text-to-Image | Landscape |
| `gemini-2.5-flash-image-portrait` | Image/Text-to-Image | Portrait |
| `gemini-3.0-pro-image-landscape` | Image/Text-to-Image | Landscape |
| `gemini-3.0-pro-image-portrait` | Image/Text-to-Image | Portrait |
| `imagen-4.0-generate-preview-landscape` | Image/Text-to-Image | Landscape |
| `imagen-4.0-generate-preview-portrait` | Image/Text-to-Image | Portrait |

### Video Generation

#### Text-to-Video (T2V - Text to Video)
⚠️ **Image upload not supported**

| Model Name | Description | Size |
|---------|---------|--------|
| `veo_3_1_t2v_fast_portrait` | Text-to-Video | Portrait |
| `veo_3_1_t2v_fast_landscape` | Text-to-Video | Landscape |
| `veo_2_1_fast_d_15_t2v_portrait` | Text-to-Video | Portrait |
| `veo_2_1_fast_d_15_t2v_landscape` | Text-to-Video | Landscape |
| `veo_2_0_t2v_portrait` | Text-to-Video | Portrait |
| `veo_2_0_t2v_landscape` | Text-to-Video | Landscape |

#### First and Last Frame Model (I2V - Image to Video)
📸 **Supports 1-2 images: First and Last Frame**

| Model Name | Description | Size |
|---------|---------|--------|
| `veo_3_1_i2v_s_fast_fl_portrait` | Image-to-Video | Portrait |
| `veo_3_1_i2v_s_fast_fl_landscape` | Image-to-Video | Landscape |
| `veo_2_1_fast_d_15_i2v_portrait` | Image-to-Video | Portrait |
| `veo_2_1_fast_d_15_i2v_landscape` | Image-to-Video | Landscape |
| `veo_2_0_i2v_portrait` | Image-to-Video | Portrait |
| `veo_2_0_i2v_landscape` | Image-to-Video | Landscape |

#### Multi-image Generation (R2V - Reference Images to Video)
🖼️ **Supports multiple images**

| Model Name | Description | Size |
|---------|---------|--------|
| `veo_3_0_r2v_fast_portrait` | Image-to-Video | Portrait |
| `veo_3_0_r2v_fast_landscape` | Image-to-Video | Landscape |

## 📡 API Usage Examples (Streaming Required)

### Text-to-Image

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [
      {
        "role": "user",
        "content": "A cute cat playing in the garden"
      }
    ],
    "stream": true
  }'
```

### Image-to-Image

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "imagen-4.0-generate-preview-landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Transform this image into watercolor painting style"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<base64_encoded_image>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

### Text-to-Video

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_1_t2v_fast_landscape",
    "messages": [
      {
        "role": "user",
        "content": "A kitten chasing butterflies on a lawn"
      }
    ],
    "stream": true
  }'
```

### Generate Video with First and Last Frame

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_1_i2v_s_fast_fl_landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Transition from the first image to the second image"
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

## 🌐 Expose API to Internet (Cloudflare Tunnel)

Share your API with others without deploying to a server. Uses Cloudflare's free tunnel service.

### Install Cloudflared

**Windows:**
```bash
winget install Cloudflare.cloudflared
```

**Linux/Mac:**
```bash
# Linux
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# Mac
brew install cloudflared
```

### Start Tunnel

```bash
# Make sure Flow2API is running first
python main.py

# In another terminal, start the tunnel
cloudflared tunnel --url http://localhost:8000
```

You'll get a public URL like:
```
https://xxx-xxx-xxx.trycloudflare.com
```

### Usage

Share the tunnel URL with others. They can access your API:

```bash
# List models
curl https://xxx-xxx-xxx.trycloudflare.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Generate image
curl -X POST https://xxx-xxx-xxx.trycloudflare.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [{"role": "user", "content": "A cute cat"}],
    "stream": true
  }'
```

> ⚠️ **Note:** 
> - The tunnel URL changes every time you restart cloudflared
> - Your computer must stay on for the API to work
> - Access admin panel only via `http://localhost:8000`, not the tunnel URL

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Thanks to all contributors and users for their support!

---

## 📞 Contact

- Submit Issues: [GitHub Issues](https://github.com/TheSmallHanCat/flow2api/issues)
- Discussions: [GitHub Discussions](https://github.com/TheSmallHanCat/flow2api/discussions)

---

**⭐ If this project is helpful to you, please give it a Star!**
