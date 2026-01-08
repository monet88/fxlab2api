# Flow2API

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.119.0-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)

**A full-featured OpenAI-compatible API service, providing a unified interface for Flow**

</div>

## ✨ Core Features

- 🎨 **Text-to-Image** / **Image-to-Image**
- 🎬 **Text-to-Video** / **Image-to-Video**
- 🎞️ **First and Last Frame Video**
- 🔄 **AT Auto-refresh**
- 📊 **Balance Display** - Real-time query and display VideoFX Credits
- 🚀 **Load Balancing** - Multi-token polling and concurrency control
- 🌐 **Proxy Support** - Supports HTTP/SOCKS5 proxy
- 📱 **Web Management Interface** - Intuitive token and configuration management
- 🎨 **Image Generation Continuous Dialogue**

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- Or Python 3.8+

- Since Flow added additional captcha verification, you can choose to use browser captcha or third-party captcha:
Register at [YesCaptcha](https://yescaptcha.com/i/13Xd8K) and get an API key, then fill it in the `YesCaptcha API Key` field in the system configuration page

- Auto-update ST browser extension: [Flow2API-Token-Updater](https://github.com/TheSmallHanCat/Flow2API-Token-Updater)

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
docker-compose -f docker-compose.warp.yml up -d

# View logs
docker-compose -f docker-compose.warp.yml logs -f
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

After the service starts, visit the admin panel: **http://localhost:8000**. Please change the password immediately after first login!

- **Username**: `admin`
- **Password**: `admin`

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

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [PearNoDec](https://github.com/PearNoDec) for the YesCaptcha solution
- [raomaiping](https://github.com/raomaiping) for the headless captcha solution

Thanks to all contributors and users for their support!

---

## 📞 Contact

- Submit Issues: [GitHub Issues](https://github.com/TheSmallHanCat/flow2api/issues)

---

**⭐ If this project is helpful to you, please give it a Star!**

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=TheSmallHanCat/flow2api&type=date&legend=top-left)](https://www.star-history.com/#TheSmallHanCat/flow2api&type=date&legend=top-left)
