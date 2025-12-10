#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flow2API Index Updater

Automatically updates PROJECT_INDEX.md and PROJECT_INDEX.json
Run this script to keep repository index current.

Usage:
    python scripts/update_index.py          # Update both files
    python scripts/update_index.py --check  # Check if update needed
    python scripts/update_index.py --md     # Update only markdown
    python scripts/update_index.py --json   # Update only json
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any
import argparse
import sys

# Set UTF-8 encoding for Windows
if os.name == 'nt':
    os.system('chcp 65001 > nul')  # Set console to UTF-8


class IndexUpdater:
    """Repository index updater for Flow2API"""

    def __init__(self, root_dir: Path):
        self.root = root_dir
        self.stats = {
            "total_files": 0,
            "python_files": 0,
            "config_files": 0,
            "doc_files": 0,
            "directories": 0
        }

    def scan_directory(self) -> Dict[str, Any]:
        """Scan repository and collect metadata"""
        print("[INFO] Scanning repository structure...")

        # Count files and collect structure
        structure = {
            "files": [],
            "directories": [],
            "python_files": [],
            "config_files": [],
            "doc_files": []
        }

        for item in self.root.rglob("*"):
            if item.is_file():
                # Skip cache and git files
                if any(skip in str(item) for skip in ["__pycache__", ".git", ".pyc"]):
                    continue

                rel_path = item.relative_to(self.root)
                structure["files"].append(str(rel_path))
                self.stats["total_files"] += 1

                # Categorize files
                if rel_path.suffix == ".py":
                    structure["python_files"].append(str(rel_path))
                    self.stats["python_files"] += 1
                elif rel_path.suffix in [".toml", ".yaml", ".yml", ".json"]:
                    structure["config_files"].append(str(rel_path))
                    self.stats["config_files"] += 1
                elif rel_path.suffix in [".md", ".txt"] and "README" in rel_path.name.upper():
                    structure["doc_files"].append(str(rel_path))
                    self.stats["doc_files"] += 1
            elif item.is_dir():
                rel_path = item.relative_to(self.root)
                if not any(skip in str(rel_path) for skip in ["__pycache__", ".git", ".pyc"]):
                    structure["directories"].append(str(rel_path))
                    self.stats["directories"] += 1

        return structure

    def get_supported_models(self) -> Dict[str, Any]:
        """Return supported AI models configuration"""
        return {
            "image_generation": [
                "gemini-2.5-flash-image-landscape",
                "gemini-2.5-flash-image-portrait",
                "gemini-3.0-pro-image-landscape",
                "gemini-3.0-pro-image-portrait",
                "imagen-4.0-generate-preview-landscape",
                "imagen-4.0-generate-preview-portrait"
            ],
            "video_generation": {
                "text_to_video": [
                    "veo_3_1_t2v_fast_portrait",
                    "veo_3_1_t2v_fast_landscape",
                    "veo_2_1_fast_d_15_t2v_portrait",
                    "veo_2_1_fast_d_15_t2v_landscape",
                    "veo_2_0_t2v_portrait",
                    "veo_2_0_t2v_landscape"
                ],
                "first_last_frame": [
                    "veo_3_1_i2v_s_fast_fl_portrait",
                    "veo_3_1_i2v_s_fast_fl_landscape",
                    "veo_2_1_fast_d_15_i2v_portrait",
                    "veo_2_1_fast_d_15_i2v_landscape",
                    "veo_2_0_i2v_portrait",
                    "veo_2_0_i2v_landscape"
                ],
                "multi_image": [
                    "veo_3_0_r2v_fast_portrait",
                    "veo_3_0_r2v_fast_landscape"
                ]
            }
        }

    def generate_markdown_index(self, structure: Dict[str, Any]) -> str:
        """Generate PROJECT_INDEX.md content"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""# Project Index: Flow2API

Generated: {now}

## 📁 Project Structure

```
flow2api/
├── .beads/                    # Beads workflow tracking
├── .serena/                   # Serena project config
├── config/                    # Configuration files
│   ├── setting.toml          # Main configuration
│   └── setting_warp.toml     # WARP proxy configuration
├── docs/                      # Documentation (generated)
├── src/                       # Source code
│   ├── api/                  # API endpoints
│   ├── core/                 # Core functionality
│   └── services/             # Business logic
├── static/                    # Web UI files
├── docker-compose.yml         # Docker configuration
├── main.py                    # Entry point
└── requirements.txt           # Python dependencies
```

## 🚀 Entry Points

- **CLI**: `main.py` - Application startup with uvicorn server
- **API**: `src/main.py` - FastAPI application initialization
- **Config**: `config/setting.toml` - Main configuration file

## 📦 Core Modules

### Module: API
- **Path**: `src/api/`
- **Files**:
  - `routes.py` - OpenAI-compatible endpoints (/v1/models, /v1/chat/completions)
  - `admin.py` - Admin panel endpoints
  - `__init__.py` - Module initialization
- **Purpose**: HTTP API interface for external clients

### Module: Core
- **Path**: `src/core/`
- **Files**:
  - `config.py` - Configuration management (TOML-based)
  - `database.py` - SQLite database operations
  - `auth.py` - Bearer token authentication
  - `models.py` - Pydantic data models
  - `logger.py` - Logging configuration
- **Purpose**: Core infrastructure and shared utilities

### Module: Services
- **Path**: `src/services/`
- **Files**:
  - `flow_client.py` - Google Labs API client wrapper
  - `token_manager.py` - Token lifecycle management
  - `load_balancer.py` - Multi-token load balancing
  - `generation_handler.py` - Content generation orchestration
  - `concurrency_manager.py` - Request concurrency control
  - `proxy_manager.py` - HTTP/SOCKS5 proxy support
  - `file_cache.py` - File caching system
- **Purpose**: Business logic and external service integration

## 🔧 Configuration

- `config/setting.toml` - Main configuration (server, auth, tokens)
- `config/setting_warp.toml` - WARP proxy configuration
- `docker-compose.yml` - Docker service definition
- `docker-compose.proxy.yml` - Proxy-enabled Docker setup

## 📚 Documentation

- `README.md` - Project overview and quick start
- `DOCUMENTATION.md` - Comprehensive documentation
- `docs/` - Generated documentation sections
  - `API.md` - API reference
  - `ARCHITECTURE.md` - System architecture
  - `CONFIGURATION.md` - Configuration guide
  - `DEPLOYMENT.md` - Deployment instructions
  - `DEVELOPMENT.md` - Development guide
  - `SETUP.md` - Installation guide
  - `TROUBLESHOOTING.md` - Common issues

## 🧪 Test Coverage

- **Unit Tests**: Not present (opportunity for improvement)
- **Integration Tests**: Not present
- **Manual Testing**: Via API endpoints and web UI

## 🔗 Key Dependencies

- **fastapi 0.119.0** - Web framework
- **uvicorn 0.32.1** - ASGI server
- **pydantic 2.10.4** - Data validation
- **aiosqlite 0.20.0** - Async SQLite
- **curl-cffi** - HTTP client with enhanced features
- **bcrypt 4.2.1** - Password hashing

## 📝 Quick Start

1. **Setup**:
   ```bash
   git clone https://github.com/TheSmallHanCat/flow2api.git
   cd flow2api
   ```

2. **Run with Docker**:
   ```bash
   docker-compose up -d
   ```

3. **Access**:
   - API: http://localhost:8000/v1/
   - Admin: http://localhost:8000/
   - Login: admin/admin

4. **Test API**:
   ```bash
   curl -H "Authorization: Bearer your-token" \\
        -H "Content-Type: application/json" \\
        http://localhost:8000/v1/models
   ```

## 🎯 Key Features

- OpenAI-compatible API endpoints
- Text-to-Image generation
- Text-to-Video generation
- Image-to-Video generation
- Multi-token load balancing
- Automatic token refresh
- Web management interface
- Docker support

## 🔐 Security

- Bearer token authentication
- Bcrypt password hashing
- Configurable admin credentials
- Token-based API access

## 📊 Performance

- Async/await throughout
- Connection pooling
- Request queuing
- Load balancing across tokens
- File caching system

## 🚀 Next Steps

1. Add comprehensive test suite
2. Implement monitoring/metrics
3. Add rate limiting
4. Enhance error handling
5. Add more model support

---

**Index Last Updated**: {self.stats['total_files']} files, {self.stats['python_files']} Python files
**Languages**: Python, TOML, YAML, Markdown
**Framework**: FastAPI with async SQLite
"""

    def generate_json_index(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PROJECT_INDEX.json content"""
        return {
            "project": {
                "name": "Flow2API",
                "version": "1.0.0",
                "generated": datetime.datetime.now().isoformat(),
                "description": "OpenAI-compatible API service for Google Flow (Labs) AI content generation"
            },
            "structure": {
                "directories": structure.get("directories", []),
                "files": {
                    "total": structure.get("files", []),
                    "python": structure.get("python_files", []),
                    "config": structure.get("config_files", []),
                    "docs": structure.get("doc_files", [])
                }
            },
            "modules": {
                "api": {
                    "path": "src/api/",
                    "files": {
                        "routes.py": "OpenAI-compatible endpoints",
                        "admin.py": "Admin panel endpoints"
                    }
                },
                "core": {
                    "path": "src/core/",
                    "files": {
                        "config.py": "Configuration management",
                        "database.py": "Database operations",
                        "auth.py": "Authentication logic",
                        "models.py": "Data models"
                    }
                },
                "services": {
                    "path": "src/services/",
                    "files": {
                        "flow_client.py": "Google Labs API client",
                        "token_manager.py": "Token lifecycle management",
                        "load_balancer.py": "Multi-token load balancing"
                    }
                }
            },
            "supported_models": self.get_supported_models(),
            "dependencies": {
                "fastapi": "0.119.0",
                "uvicorn": "0.32.1",
                "pydantic": "2.10.4",
                "aiosqlite": "0.20.0"
            },
            "statistics": self.stats,
            "last_updated": datetime.datetime.now().isoformat()
        }

    def update_files(self, structure: Dict[str, Any], update_md: bool = True, update_json: bool = True):
        """Update index files"""
        if update_md:
            print("[INFO] Updating PROJECT_INDEX.md...")
            md_content = self.generate_markdown_index(structure)
            md_path = self.root / "PROJECT_INDEX.md"
            md_path.write_text(md_content, encoding="utf-8")
            print(f"   [OK] Updated: {md_path}")

        if update_json:
            print("[INFO] Updating PROJECT_INDEX.json...")
            json_content = self.generate_json_index(structure)
            json_path = self.root / "PROJECT_INDEX.json"
            json_path.write_text(json.dumps(json_content, indent=2), encoding="utf-8")
            print(f"   [OK] Updated: {json_path}")

    def check_needs_update(self) -> bool:
        """Check if index files need updating"""
        try:
            json_path = self.root / "PROJECT_INDEX.json"
            if not json_path.exists():
                return True

            json_data = json.loads(json_path.read_text())
            last_updated = json_data.get("last_updated")

            if not last_updated:
                return True

            # Check if files have changed since last update
            last_update_time = datetime.datetime.fromisoformat(last_updated)
            for item in self.root.rglob("*"):
                if item.is_file() and not any(skip in str(item) for skip in ["__pycache__", ".git", ".pyc"]):
                    if datetime.datetime.fromtimestamp(item.stat().st_mtime) > last_update_time:
                        return True

            return False
        except Exception:
            return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Update Flow2API index files")
    parser.add_argument("--check", action="store_true",
                       help="Check if update is needed")
    parser.add_argument("--md", action="store_true",
                       help="Update only markdown file")
    parser.add_argument("--json", action="store_true",
                       help="Update only JSON file")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")

    args = parser.parse_args()

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    updater = IndexUpdater(repo_root)

    # Check if update needed
    if args.check:
        print("[INFO] Checking if index needs update...")
        needs_update = updater.check_needs_update()
        if needs_update:
            print("   [WARN] Index is out of date")
            return 1
        else:
            print("   [OK] Index is up to date")
            return 0

    # Scan repository
    structure = updater.scan_directory()

    # Determine what to update
    update_md = not args.json or args.md
    update_json = not args.md or args.json

    # Update files
    updater.update_files(structure, update_md=update_md, update_json=update_json)

    # Display statistics
    print("\n[INFO] Repository Statistics:")
    print(f"   Files: {updater.stats['total_files']}")
    print(f"   Python files: {updater.stats['python_files']}")
    print(f"   Config files: {updater.stats['config_files']}")
    print(f"   Documentation files: {updater.stats['doc_files']}")
    print(f"   Directories: {updater.stats['directories']}")
    print("\n[SUCCESS] Index update completed!")

    return 0


if __name__ == "__main__":
    exit(main())
