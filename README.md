


[![GitHub License](https://img.shields.io/github/license/DeLuca21/peekrr?style=for-the-badge&labelColor=%23585b70&color=%23f5e0dc&logo=github)](https://github.com/DeLuca21/peekrr)
[![GitHub Release](https://img.shields.io/github/v/release/DeLuca21/peekrr?include_prereleases&style=for-the-badge&labelColor=%23585b70&color=%23cba6f7&logo=github)](https://github.com/DeLuca21/peekrr/releases)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/DeLuca21/peekrr/total?style=for-the-badge&label=Downloads&labelColor=%23585b70&color=%23a6da95&logo=github)](https://github.com/DeLuca21/peekrr/releases)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/DeLuca21/peekrr?style=for-the-badge&labelColor=%23585b70&color=%23eba0ac&logo=github)](https://github.com/DeLuca21/peekrr/issues)


# Peekrr 🔎🎬  

**Lightning‑fast Jellyseerr CLI for fuzzy search, rich metadata preview, and one‑keypress media requests.**

---
<p align="center">
<img src="https://github.com/DeLuca21/peekrr/blob/main/assetts/peekrr_logo.png?raw=true" alt="peekrr Logo" width="150">
</p>

---

## ✨ Features

- Fuzzy movie / TV search with arrow‑key navigation  
- Rich metadata panel (year, overview, availability status)  
- Accurate status mapping → 📀 Available · 🔄 Requested · 🛠️ Processing · 🛑 Not Available  
- One‑key **request / retry** actions  
- Pagination with “Showing X–Y of N” and last‑page indicator  
- Works in `pipx`, virtualenv  

---

## 🚀 Install

> **Tip:** Use **pipx** if your global `pip` is messy—pipx keeps Peekrr isolated.

### 1. pipx (recommended)

```bash
# Install pipx if needed
python -m pip install --user pipx
pipx ensurepath

# Install Peekrr from GitHub (will be on PyPI in a future release)
pipx install --force 'git+https://github.com/DeLuca21/peekrr'
```

### 2. Manual install (via Git clone)

```bash
git clone https://github.com/DeLuca21/peekrr
cd peekrr
pipx install --force .
```

### 3. Developer install (for contributing)

```bash
git clone https://github.com/DeLuca21/peekrr
cd peekrr
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```


## ⚙️ Configuration

Peekrr stores its settings at ~/.peekrr.yaml:

```yaml
jellyseerr_url: "http://192.168.X.XXX:XXXX"
api_key: "YOUR_API_KEY"
sort: "releaseDate:desc"   # default result ordering
fuzzy_threshold: 80        # 0‑100, lower = looser match
```

### 🔧 Setup Options

- **Automatic:** Just run `peekrr` once — it will guide you through setup and create the config file
- **Manual:** Use inline config updates:

```bash
peekrr config --set jellyseerr_url=https://your-domain
peekrr config --edit  # re-run interactive setup
```

### 🌍 Environment overrides

Override on demand:
```bash
PEEKRR_URL=https://jelly.domain PEEKRR_APIKEY=XYZ peekrr search kung fu panda
```

## 🕹️ Usage

 ```bash
# Interactive search & request
peekrr search kung fu panda

# Request instantly
peekrr request The Matrix

# View current requests (all statuses)
peekrr requests

# Filter by status
peekrr requests --status available

# View current config
peekrr config

# Update config
peekrr config --set api_key=abc123
```

### ⌨️ Interactive Keys

| Key        | Action             |
|------------|--------------------|
| ↑ / ↓      | Move selection     |
| ← / →      | Page results       |
| PgUp/Dn    | Page results       |
| Enter      | Context-aware action |
| R          | Retry request      |
| D          | Delete request     |
| Q / Esc    | Quit               |


## 🛣️ Roadmap

- Inline live filtering
- Poster thumbnails in list view
- "Open in Plex" button when media exists
- Config overrides (result_limit, default sort)

## 🤝 Contributing

- Fork → pip install -e .[dev]
- pytest -q (all tests green)
- Open a PR—CI will lint & test automatically.