# Flow2API Documentation

Welcome to the comprehensive documentation for Flow2API - a full-featured OpenAI-compatible API service that provides a unified interface for Google's VideoFX (Veo) platform.

## Documentation Structure

This documentation is organized into the following sections:

### Core Documentation
1. **[Project Overview](./PROJECT_OVERVIEW.md)** - Introduction to Flow2API, its purpose, and key features
2. **[Architecture Documentation](./ARCHITECTURE.md)** - Detailed technical architecture and component design
3. **[API Documentation](./API.md)** - Complete API reference with examples

### Setup and Operations
4. **[Setup and Installation Guide](./SETUP.md)** - Step-by-step installation instructions
5. **[Configuration Guide](./CONFIGURATION.md)** - Detailed configuration options and examples
6. **[Deployment Guide](./deployment-guide.md)** - Production deployment strategies and best practices
7. **[Troubleshooting Guide](./TROUBLESHOOTING.md)** - Common issues and their solutions

### Development
8. **[Development Guide](./DEVELOPMENT.md)** - Guidelines for developers contributing to the project
9. **[Code Standards](./code-standards.md)** - Coding conventions and best practices
10. **[Codebase Summary](./codebase-summary.md)** - Comprehensive codebase overview

### Planning
11. **[Project Overview PDR](./project-overview-pdr.md)** - Product Development Requirements
12. **[System Architecture](./system-architecture.md)** - Detailed system architecture
13. **[Project Roadmap](./project-roadmap.md)** - Development roadmap and future plans

## 🚀 Quick Start

If you're new to Flow2API, we recommend starting with:

1. **Project Overview** - To understand what Flow2API does
2. **Setup and Installation** - To get the service running quickly
3. **API Documentation** - To start using the service

## 🎯 What is Flow2API?

Flow2API is a sophisticated middleware service that bridges the gap between Google's VideoFX platform and developers who want to use it through a familiar OpenAI-compatible API. It provides:

- **Unified Interface**: Single API endpoint for both image and video generation
- **Token Management**: Automatic token rotation and lifecycle management
- **Load Balancing**: Intelligent token selection across multiple accounts
- **Concurrency Control**: Prevents overloading individual accounts
- **Caching**: Optional file caching for generated content
- **Web Management**: Built-in admin interface for managing tokens and configuration

## 📊 Supported Features

### Image Generation
- Text-to-Image with various models (Gemini 2.5 Flash, Gemini 3.0 Pro, Imagen 4.0)
- Image-to-Image transformations
- Multiple aspect ratios (landscape/portrait)

### Video Generation
- Text-to-Video generation
- Image-to-Video with first and last frames
- Multi-reference image video generation
- Various Veo model versions (2.0, 2.1, 3.0, 3.1)

### Management Features
- Token lifecycle management with automatic refresh
- Real-time balance monitoring
- Usage statistics and error tracking
- Proxy support for network flexibility
- Docker support for easy deployment

## 🏗️ Architecture Highlights

Flow2API is built with modern Python technologies:

- **FastAPI**: High-performance async web framework
- **SQLite**: Lightweight database for data persistence
- **Pydantic**: Data validation and serialization
- **curl-cffi**: HTTP client with browser impersonation
- **AsyncIO**: Full async/await support for high concurrency

## 🔧 Getting Help

If you encounter any issues or have questions:

1. Check the [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Review the [API Documentation](./API.md) for usage examples
3. Check the [Configuration Guide](./CONFIGURATION.md) for setup issues
4. For bugs or feature requests, please create an issue on GitHub

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/TheSmallHanCat/flow2api/issues)
- **GitHub Discussions**: [Community discussions](https://github.com/TheSmallHanCat/flow2api/discussions)

---

**Ready to dive in? Start with the [Project Overview](./PROJECT_OVERVIEW.md)!**

## 📖 Documentation Map

```
┌─────────────────────────────────────────────────────────────┐
│                        Quick Start                          │
├─────────────────────────┬───────────────────────────────────┤
│  New Users              │  Advanced Users                   │
├─────────────────────────┼───────────────────────────────────┤
│ 1. Project Overview     │ 1. API Documentation              │
│ 2. Setup Guide          │ 2. Configuration Guide            │
│ 3. Basic Configuration  │ 3. Deployment Guide               │
│ 4. Troubleshooting      │ 4. Development Guide              │
└─────────────────────────┴───────────────────────────────────┘
```

## 🎯 Use Cases

### For Content Creators
- Generate images and videos through a simple API
- Integrate AI generation into your applications
- Manage multiple Google accounts efficiently

### For Developers
- Build applications with AI generation capabilities
- Use familiar OpenAI-compatible API
- Implement custom generation workflows

### For Enterprises
- Deploy scalable AI generation infrastructure
- Manage team access and quotas
- Monitor usage and performance

## 🔗 Quick Links

- **[Installation](./SETUP.md#🚀-installation-methods)** - Get started in minutes
- **[API Examples](./API.md#📝-usage-examples)** - See the API in action
- **[Configuration](./CONFIGURATION.md#🔧-basic-configuration)** - Customize your setup
- **[Troubleshooting](./TROUBLESHOOTING.md#🚨-common-issues)** - Fix common problems