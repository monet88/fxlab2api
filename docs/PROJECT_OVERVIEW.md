# Flow2API - Project Overview

## 🎯 What is Flow2API?

Flow2API is a sophisticated middleware service that acts as a bridge between Google's VideoFX (Veo) platform and developers who need a standardized, OpenAI-compatible API interface. It transforms the complex VideoFX workflow into a simple, familiar API that developers can integrate into their applications.

## 🌟 Key Features

### 🤖 AI Generation Capabilities

#### Image Generation
- **Text-to-Image**: Generate images from text descriptions
- **Image-to-Image**: Transform existing images based on prompts
- **Multiple Models**: Support for Gemini 2.5 Flash, Gemini 3.0 Pro, and Imagen 4.0
- **Aspect Ratios**: Both landscape and portrait orientations

#### Video Generation
- **Text-to-Video**: Create videos from text prompts
- **Image-to-Video with First/Last Frames**: Generate videos using start and end images
- **Multi-Reference Video**: Create videos using multiple reference images
- **Multiple Models**: Support for Veo 2.0, 2.1, 3.0, and 3.1 models

### 🔧 Advanced Features

#### Token Management
- **Automatic AT Refresh**: Session tokens are automatically converted and refreshed
- **Multi-Token Support**: Manage multiple Google accounts simultaneously
- **Token Health Monitoring**: Track token status, errors, and usage
- **Auto-Disable**: Automatically disable tokens that exceed error thresholds

#### Load Balancing & Concurrency
- **Intelligent Token Selection**: Random selection with availability checks
- **Concurrency Limits**: Prevent overloading individual accounts
- **Model-Specific Filtering**: Route requests to appropriate tokens based on model requirements

#### Caching System
- **Optional File Caching**: Cache generated images and videos locally
- **Configurable TTL**: Set cache expiration times
- **Base URL Support**: Serve cached files through custom domains

#### Proxy Support
- **HTTP/SOCKS5 Proxy**: Route requests through proxies
- **Per-Token Proxy**: Different tokens can use different proxies
- **Automatic Failover**: Switch proxies on connection failures

### 🌐 Management Interface

#### Web Dashboard
- **Token Management**: Add, edit, enable/disable tokens
- **Real-time Monitoring**: View token status and balances
- **Usage Statistics**: Track generation statistics
- **Configuration Management**: Update settings through the web interface

#### API Features
- **OpenAI Compatibility**: Drop-in replacement for OpenAI API
- **Streaming Support**: Real-time progress updates
- **Error Handling**: Detailed error messages and status codes
- **Request Logging**: Track all API requests and responses

## 🏗️ Architecture Overview

Flow2API is built on a modern, asynchronous architecture:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Client Apps   │────▶│   Flow2API       │────▶│  Google VideoFX │
│                 │     │   FastAPI Server │     │   Platform      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   SQLite DB      │
                        │                  │
                        └──────────────────┘
```

### Core Components

1. **FastAPI Server**: Main application server handling HTTP requests
2. **Generation Handler**: Orchestrates image/video generation workflows
3. **Token Manager**: Manages token lifecycle and refresh
4. **Load Balancer**: Selects optimal tokens for requests
5. **Flow Client**: Interfaces with Google VideoFX APIs
6. **Database Layer**: Persists tokens, tasks, and configuration

## 🚀 Use Cases

### Content Creation Platforms
- Integrate AI-generated images and videos into content workflows
- Provide AI-powered creative tools to users
- Batch process content generation requests

### Application Development
- Add AI generation capabilities to existing applications
- Replace expensive AI service providers with cost-effective VideoFX
- Build custom AI-powered features

### Research & Experimentation
- Test different AI models and parameters
- Compare generation quality across models
- Analyze usage patterns and costs

## 💡 Why Flow2API?

### For Developers
- **Familiar API**: Use the same interface as OpenAI
- **Comprehensive Documentation**: Clear examples and guides
- **Easy Integration**: Minimal code changes required
- **Type Safety**: Full Pydantic models for all data structures

### For Operations
- **Production Ready**: Built with async architecture for high performance
- **Monitoring**: Built-in logging and statistics
- **Configuration Management**: Runtime configuration updates
- **Docker Support**: Easy deployment with Docker Compose

### For Business
- **Cost Effective**: Leverage Google's VideoFX platform
- **Scalable**: Support for multiple accounts and tokens
- **Reliable**: Automatic error handling and recovery
- **Flexible**: Support for various deployment scenarios

## 📊 Supported Models

### Image Models
| Model | Description | Type |
|-------|-------------|------|
| gemini-2.5-flash-image-landscape | Gemini 2.5 Flash (Landscape) | Text-to-Image |
| gemini-2.5-flash-image-portrait | Gemini 2.5 Flash (Portrait) | Text-to-Image |
| gemini-3.0-pro-image-landscape | Gemini 3.0 Pro (Landscape) | Text-to-Image |
| gemini-3.0-pro-image-portrait | Gemini 3.0 Pro (Portrait) | Text-to-Image |
| imagen-4.0-generate-preview-landscape | Imagen 4.0 (Landscape) | Text-to-Image |
| imagen-4.0-generate-preview-portrait | Imagen 4.0 (Portrait) | Text-to-Image |

### Video Models
| Model | Description | Type | Images Support |
|-------|-------------|------|----------------|
| veo_3_1_t2v_fast_landscape | Veo 3.1 Fast (Landscape) | Text-to-Video | ❌ |
| veo_3_1_t2v_fast_portrait | Veo 3.1 Fast (Portrait) | Text-to-Video | ❌ |
| veo_3_1_i2v_s_fast_fl_landscape | Veo 3.1 I2V (Landscape) | First/Last Frame | ✅ (1-2) |
| veo_3_1_i2v_s_fast_fl_portrait | Veo 3.1 I2V (Portrait) | First/Last Frame | ✅ (1-2) |
| veo_3_0_r2v_fast_landscape | Veo 3.0 R2V (Landscape) | Multi-Reference | ✅ (Unlimited) |
| veo_3_0_r2v_fast_portrait | Veo 3.0 R2V (Portrait) | Multi-Reference | ✅ (Unlimited) |

## 🎯 Next Steps

Ready to get started? Here's what to do next:

1. **[Installation Guide](./SETUP.md)** - Get Flow2API up and running
2. **[Configuration Guide](./CONFIGURATION.md)** - Configure tokens and settings
3. **[API Documentation](./API.md)** - Learn how to use the API
4. **[Architecture Guide](./ARCHITECTURE.md)** - Deep dive into the technical implementation

## 🔗 Related Links

- **GitHub Repository**: [TheSmallHanCat/flow2api](https://github.com/TheSmallHanCat/flow2api)
- **Google VideoFX**: [labs.google/fx](https://labs.google/fx)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

*Flow2API - Making AI generation accessible through familiar interfaces*