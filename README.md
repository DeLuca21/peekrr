<p align="center">
  <img src="https://raw.githubusercontent.com/DeLuca21/peekrr/refs/heads/main/assets/peekrr_logo.png" alt="peekrr Logo" width="300">
</p>

# Peekrr 🔎🎬  

**Lightning‑fast Jellyseerr CLI for fuzzy search, rich metadata preview, and one‑keypress media requests.**


---

## ✨ Features
- Fuzzy movie / TV search with arrow‑key navigation  
- Rich metadata panel (year, overview, availability status)  
- Accurate status mapping → 📀 Available · 🔄 Requested · 🛠️ Processing · 🛑 Not Available  
- One‑key **request / retry / delete** actions  
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

# Install Peekrr straight from GitHub (swap URL for PyPI once released)
pipx install --force 'git+https://github.com/DeLuca21/peekrr'
```

### 2. Manual dev install

```bash
git clone https://github.com/DeLuca21/peekrr
cd peekrr
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```


### ⚙️ Configuration

Peekrr stores its settings in ~/.peekrr.yaml:

```yaml
jellyseerr_url: "http://192.168.X.XXX:XXXX"
api_key: "YOUR_API_KEY"
sort: "releaseDate:desc"   # default result ordering
fuzzy_threshold: 80        # 0‑100, lower = looser match
```

##### Automatic setup

Run Peekrr once and it will prompt for any missing fields, then create the file.

##### Environment overrides

Override on demand:
```bash
PEEKRR_URL=https://jelly.domain PEEKRR_APIKEY=XYZ peekrr search "kung fu panda"
```

## 🕹️ Usage

 ```bash
Interactive search & request
peekrr search "dune"

# Non‑interactive one‑shot request
peekrr request "The Matrix"

# Delete a request (admin only)
peekrr delete 12345

# Help
peekrr --help``
```

##### Interactive keys
Key	Action
↑ / ↓	Move selection
← / →, PgUp/Dn	Page results
Enter	Context‑aware action
R	Retry request
D	Delete request
Q / Esc	Quit

##### 🛣️ Roadmap

- Inline live filtering
- Poster thumbnails in list view
- “Open in ~~Jellyfin/~~Plex' button when media exists
- Config overrides (result_limit, default sort)
