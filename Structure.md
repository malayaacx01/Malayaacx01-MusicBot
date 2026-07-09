# 📁 ˹ʜᴀꜱɪɪ ᴍᴜꜱɪᴄ˼ Project Structure

This document provides a comprehensive overview of the project structure, explaining the purpose of each folder and key files.

---

## 📂 Root Directory Files

### Configuration Files

- **`.env`** - Environment variables (API keys, tokens, database URL, etc.)

  - ⚠️ **Never commit this file!** Contains sensitive credentials
  - Use `sample.env` as a template

- **`config.py`** - Configuration manager that loads and validates environment variables

  - Loads settings from `.env` file
  - Provides default values for optional settings
  - Validates required configurations on startup

- **`requirements.txt`** - Python package dependencies
  - List of all required packages (Pyrogram, motor, yt-dlp, etc.)
  - Install with: `pip install -r requirements.txt`

### Startup Scripts

- **`setup`** - Initial setup script (install dependencies, configure environment)
- **`start`** - Bot startup script (runs the bot)

### Docker Files

- **`Dockerfile`** - Docker build instructions
- **`docker-compose.yml`** - Docker compose configuration

### Documentation

- **`Readme.md`** - Project overview, features, and setup instructions
- **`LICENSE`** - Software license (defines usage rights)
- **`Structure.md`** - This file! Project organization guide
- **`SECURITY.md`** - Security guidelines and best practices
- **`ARCHITECTURE.md`** - System architecture overview
- **`CONTRIBUTING.md`** - Contribution guidelines
- **`CREDITS.md`** - Project credits and acknowledgments
- **`study_roadmap.md`** - Developer roadmap

---

## 📦 HasiiMusic/ - Main Application Package

The core bot application containing all functionality.

### 🔧 HasiiMusic/core/ - Core Components

Contains the fundamental building blocks of the bot.

| File          | Purpose                                                     |
| ------------- | ----------------------------------------------------------- |
| `bot.py`      | Main bot client class (extends Pyrogram Client)             |
| `userbot.py`  | Assistant/userbot clients (for joining voice chats)         |
| `calls.py`    | Voice call management (PyTgCalls integration)               |
| `mongo.py`    | MongoDB database operations (users, chats, blacklist, etc.) |
| `telegram.py` | Telegram API helper functions                               |
| `youtube.py`  | YouTube video/audio downloading and processing              |
| `dir.py`      | Directory management (temp files, downloads, etc.)          |
| `preload.py`  | Background track preloading for seamless playback           |

**What it does:**

- Initializes bot and userbot clients
- Manages voice call connections
- Handles database operations (MongoDB)
- Downloads and processes media from YouTube

---

### 🔌 HasiiMusic/plugins/ - Command Handlers

All bot commands and event handlers, organized by category.

#### 📁 admin/ - Administrator Commands

| File              | Commands              | Description                                  |
| ----------------- | --------------------- | -------------------------------------------- |
| `autoleave.py`    | `/autoleave`          | Configure auto-leave settings for assistants |
| `broadcast.py`    | `/broadcast`          | Send messages to all bot users/chats         |
| `leave.py`        | `/leave`, `/leaveall` | Make assistants leave groups                 |
| `restart.py`      | `/restart`            | Restart the bot                              |
| `sudoers.py`      | `/addsudo`, `/rmsudo` | Manage sudo users                            |
| `vplay_toggle.py` | `/vplaytoggle`        | Toggle video play capability globally        |

**Purpose:** Commands restricted to bot owner and sudo users for administration.

**Command Details:**
- **`/leave`** - Make bot and assistant leave the current chat immediately
- **`/leaveall`** - Make all assistants leave all inactive groups (excludes active calls and logger chat)
- **`/restart`** - Clear cache and restart bot process

---

#### 📁 events/ - Event Handlers

| File           | Events           | Description                    |
| -------------- | ---------------- | ------------------------------ |
| `callbacks.py` | Callback queries | Handle inline button presses   |
| `iquery.py`    | Inline queries   | Handle inline mode requests    |
| `misc.py`      | Miscellaneous    | Auto-leave, voice chat events  |
| `new_chat.py`  | New chat members | Handle bot added to new groups |

**Purpose:** Handle Telegram events (button clicks, inline queries, new members, etc.)

---

#### 📁 info/ - Information Commands

| File        | Commands  | Description                                |
| ----------- | --------- | ------------------------------------------ |
| `start.py`  | `/start`  | Welcome message with bot information       |
| `ping.py`   | `/ping`   | Check bot response time and uptime         |
| `stats.py`  | `/stats`  | Bot statistics (users, chats, system info) |
| `active.py` | `/ac`     | List active voice chats                    |

**Purpose:** Informational commands available to all users.

---

#### 📁 playback/ - Music Control Commands

| File              | Commands          | Description                       |
| ----------------- | ----------------- | --------------------------------- |
| `play.py`         | `/play`, `/vplay` | Play audio/video in voice chat    |
| `pause.py`        | `/pause`          | Pause current playback            |
| `resume.py`       | `/resume`         | Resume paused playback            |
| `skip.py`         | `/skip`           | Skip to next song in queue        |
| `stop.py`         | `/stop`, `/end`   | Stop playback and clear queue     |
| `seek.py`         | `/seek`           | Jump to specific timestamp        |
| `loop.py`         | `/loop`           | Toggle loop mode                  |
| `queue.py`        | `/queue`          | Display current queue             |
| `radio.py`        | `/radio`          | Stream live radio stations        |
| `example_radio.py`| -                 | Example radio station presets     |

**Purpose:** Core music playback functionality for voice chats.

---

#### 📁 settings/ - Configuration Commands

| File             | Commands                     | Description                  |
| ---------------- | ---------------------------- | ---------------------------- |
| `auth.py`        | `/auth`, `/unauth`           | Manage authorized users      |
| `blacklist.py`   | `/blacklist`, `/unblacklist` | Block/unblock users/chats    |

**Purpose:** Group-specific settings and user management.

---

#### 📁 utilities/ - Special Features

| File              | Commands                  | Description                     |
| ----------------- | ------------------------- | ------------------------------- |
| `adminmention.py` | `/admins`, `/admin`       | Mention all admins in group     |
| `bots.py`         | `/bots`                   | List all bots in the group      |

**Purpose:** Enhanced group management and information features.

---

#### 📁 games/ - Miscellaneous Features

| File          | Commands                                                   | Description             |
| ------------- | ---------------------------------------------------------- | ----------------------- |
| `dicegame.py` | `/dice`, `/dart`, `/basket`, `/jackpot`, `/ball`, `/football` | Fun dice and dart games |

**Purpose:** Fun entertainment features.

---

#### 📝 Plugin Loader

- **`__init__.py`** - Auto-discovers and loads all plugin modules
  - Recursively scans subdirectories for Python files
  - Returns module paths (e.g., `admin.broadcast`)
  - Exposes `all_modules` list for dynamic loading

---

### 🛠️ HasiiMusic/helpers/ - Helper Functions

Utility functions used throughout the bot.

| File             | Purpose                                               |
| ---------------- | ----------------------------------------------------- |
| `_admins.py`     | Admin permission checks (`is_admin`, `can_manage_vc`) |
| `_dataclass.py`  | Data classes for tracks and media                     |
| `_inline.py`     | Inline keyboard button builders                       |
| `_play.py`       | Music playback helper functions                       |
| `_preload.py`    | Background preloading system for next tracks          |
| `_queue.py`      | Queue management (add, remove, get next)              |
| `_thumbnails.py` | Thumbnail generation and processing                   |
| `_utilities.py`  | General utility functions                             |
| `Inter-Light.ttf`| Font file for thumbnail text rendering               |
| `Raleway-Bold.ttf`| Font file for thumbnail text rendering              |

**Purpose:** Reusable helper functions to keep plugin code clean and DRY.

---

### 🌍 HasiiMusic/locales/ - Message Strings

Bot message strings in JSON format.

| File      | Description      |
| --------- | ---------------- |
| `en.json` | English messages |

**Format:** JSON key-value pairs

```json
{
  "start_welcome": "Hello! I'm a music bot.",
  "play_started": "▶️ Playing: {title}"
}
```

**Purpose:** Centralized message strings for easy maintenance.

---

### 🍪 HasiiMusic/cookies/ - YouTube Cookies

Storage for YouTube authentication cookies.

- Used to access age-restricted and region-locked content
- Cookies are downloaded from URLs specified in `COOKIE_URL` environment variable
- **`README.md`** - Instructions on how to obtain and use cookies

---

### 🚀 HasiiMusic/**main**.py - Entry Point

Main application entry point that:

1. Connects to MongoDB database
2. Starts bot and userbot clients
3. Initializes voice call handler
4. Loads all plugin modules dynamically
5. Downloads YouTube cookies (if configured)
6. Loads sudo users and blacklisted users
7. Keeps bot running until stopped

---

### 📦 HasiiMusic/**init**.py - Package Initialization

Initializes and exports core components:

```python
from HasiiMusic.core import app, userbot, tune, db, yt, logger
from HasiiMusic import config
```

Makes core objects accessible throughout the application.

---

## 🔄 How It Works

### Startup Flow

```
1. __main__.py executes
2. Load config from .env
3. Connect to MongoDB
4. Start bot client
5. Start userbot clients
6. Initialize PyTgCalls
7. Load plugins dynamically
8. Download YouTube cookies
9. Load sudo/blacklist users
10. Bot is ready! 🎉
```

### Request Flow

```
User sends /play →
  plugins/playback/play.py →
    helpers/_play.py (process request) →
      core/youtube.py (download media) →
        core/calls.py (stream to voice chat) →
          helpers/_queue.py (add to queue)
```

### Database Flow

```
User action →
  core/mongo.py methods →
    MongoDB Atlas →
      Store/retrieve data
```

---

## 📁 Directory Organization

### Complete Project Tree

```
HasiiMusicBot/
│
├── 📄 Configuration & Setup
│   ├── .env                      # Environment variables (sensitive - not committed)
│   ├── sample.env                # Environment template
│   ├── config.py                 # Configuration loader and validator
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Docker build instructions
│   ├── docker-compose.yml        # Docker compose configuration
│   ├── setup                     # Setup script
│   └── start                     # Bot startup script
│
├── 📚 Documentation
│   ├── Readme.md                 # Project overview and setup guide
│   ├── LICENSE                   # Software license
│   ├── Structure.md              # This file
│   ├── SECURITY.md               # Security guidelines
│   ├── ARCHITECTURE.md           # System architecture overview
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   ├── CREDITS.md                # Project credits and acknowledgments
│   └── study_roadmap.md          # Developer roadmap
│
└── 📦 HasiiMusic/                # Main application package
    │
    ├── __init__.py               # Package initialization
    ├── __main__.py               # Application entry point
    │
    ├── 🔧 core/                  # Core functionality
    │   ├── bot.py                # Main bot client
    │   ├── userbot.py            # Assistant clients
    │   ├── calls.py              # Voice call handler
    │   ├── mongo.py              # Database operations
    │   ├── telegram.py           # Telegram helpers
    │   ├── youtube.py            # YouTube downloader
    │   ├── lang.py               # Language system
    │   ├── dir.py                # Directory manager
    │   └── preload.py            # Track preloader
    │
    ├── 🔌 plugins/               # Command handlers
    │   ├── __init__.py           # Plugin loader
    │   │
    │   ├── admin/                # Owner/sudo commands
    │   │   ├── autoleave.py      # Auto-leave configuration
    │   │   ├── broadcast.py      # Broadcast messages
    │   │   ├── leave.py          # Leave groups
    │   │   ├── restart.py        # Bot restart/update
    │   │   ├── sudoers.py        # Sudo management
    │   │   └── vplay_toggle.py   # Video play toggle
    │   │
    │   ├── events/               # Event handlers
    │   │   ├── callbacks.py      # Button callbacks
    │   │   ├── iquery.py         # Inline queries
    │   │   ├── misc.py           # Miscellaneous events
    │   │   └── new_chat.py       # New chat handler
    │   │
    │   ├── info/                 # Info commands
    │   │   ├── start.py          # Start command
    │   │   ├── ping.py           # Ping command
    │   │   ├── stats.py          # Statistics
    │   │   └── active.py         # Active chats
    │   │
    │   ├── playback/             # Music controls
    │   │   ├── play.py           # Play command
    │   │   ├── pause.py          # Pause command
    │   │   ├── resume.py         # Resume command
    │   │   ├── skip.py           # Skip command
    │   │   ├── stop.py           # Stop command
    │   │   ├── seek.py           # Seek command
    │   │   ├── loop.py           # Loop mode
    │   │   ├── queue.py          # Queue display
    │   │   ├── radio.py          # Radio streams
    │   │   └── example_radio.py  # Radio presets
    │   │
    │   ├── settings/             # Settings commands
    │   │   ├── auth.py           # Authorization
    │   │   └── blacklist.py      # User blocking
    │   │
    │   ├── utilities/            # Special features
    │   │   ├── adminmention.py   # Mention admins
    │   │   └── bots.py           # List bots
    │   │
    │   └── games/                # Miscellaneous
    │       └── dicegame.py       # Fun games
    │
    ├── 🛠️ helpers/               # Helper functions
    │   ├── __init__.py           # Helper exports
    │   ├── _admins.py            # Admin checks
    │   ├── _dataclass.py         # Data structures
    │   ├── _inline.py            # Inline keyboards
    │   ├── _play.py              # Playback helpers
    │   ├── _preload.py           # Background preloading
    │   ├── _queue.py             # Queue management
    │   ├── _thumbnails.py        # Thumbnail generator
    │   ├── _utilities.py         # General utilities
    │   ├── Inter-Light.ttf       # Font file
    │   └── Raleway-Bold.ttf      # Font file
    │
    ├── 🌍 locales/               # Translations
    │   └── en.json               # English
    │
    └── 🍪 cookies/               # YouTube cookies
        └── README.md             # Cookie instructions
```

### Directory Naming Conventions

**Package Directories (lowercase with underscores):**

- `core/` - Core functionality modules
- `helpers/` - Reusable helper functions
- `locales/` - Localization files
- `cookies/` - Cookie storage

**Plugin Directories (lowercase):**

- `admin/` - Administrative controls
- `playback/` - Music playback controls
- `events/` - Event handlers
- `info/` - Information commands
- `settings/` - Configuration commands
- `utilities/` - Utility commands
- `games/` - Mini games

**File Naming:**

- Python modules: `lowercase_with_underscores.py`
- Private helpers: `_leading_underscore.py`
- Package initializers: `__init__.py`
- Entry point: `__main__.py`

### Import Patterns

**Core imports:**

```python
from HasiiMusic import app, userbot, tune, db, config, logger
```

**Helper imports:**

```python
from HasiiMusic.helpers import buttons, thumb, utils
from HasiiMusic.helpers import is_admin, Queue, Track
```

**Plugin imports:**

```python
# Plugins are auto-loaded, no manual imports needed
# Each plugin imports what it needs from core and helpers
```

---

## 🎯 Key Concepts

### Plugin System

- **Modular Design:** Each feature is a separate plugin file
- **Auto-Discovery:** `plugins/__init__.py` automatically finds all plugins
- **Dynamic Loading:** `__main__.py` imports plugins at runtime
- **Organized Categories:** Plugins grouped by functionality

### Assistant Bots

- **Purpose:** Join voice chats on behalf of the bot (bots can't join voice chats directly)
- **Multiple Assistants:** Support for 1-3 assistants for load balancing
- **Session Strings:** Pyrogram user sessions (get from @StringFatherBot)

### Queue System

- **Per-Chat Queues:** Each group has its own music queue
- **In-Memory Storage:** Active queues stored in RAM for fast access
- **Database Persistence:** Queue state can be saved to MongoDB

### Permission System

- **Owner:** Full access to all commands (set in `OWNER_ID`)
- **Sudo Users:** Trusted users with elevated permissions
- **Admins:** Group admins can control playback in their groups
- **Authorized Users:** Group-specific users allowed to add songs

---

## 🔒 Security Notes

### Sensitive Files (Never Commit!)

- `.env` - Contains API keys, tokens, database credentials
- Session strings - User account access tokens

### Environment Variables

All sensitive data is stored in environment variables, not hardcoded:

- `API_ID`, `API_HASH` - Telegram API credentials
- `BOT_TOKEN` - Bot authentication token
- `MONGO_DB_URI` - Database connection string
- `STRING_SESSION` - Userbot session string

---

## 📚 Learning Path

### For Beginners

1. Start with `README.md` - Understand what the bot does
2. Read `config.py` - See what settings are available
3. Explore `plugins/info/` - Simple command examples
4. Check `core/bot.py` - How the bot client works

### For Contributors

1. Understand the plugin system (`plugins/__init__.py`)
2. Study helper functions (`helpers/`)
3. Learn database operations (`core/mongo.py`)
4. Review existing plugins for patterns
5. Test changes in a separate group

### For Advanced Users

1. Explore `core/calls.py` - PyTgCalls integration
2. Study `core/youtube.py` - Media downloading logic
3. Review `helpers/_queue.py` - Queue management
4. Understand async/await patterns throughout codebase

---

## 🤝 Contributing

When adding new features:

1. Create plugin in appropriate subdirectory
2. Use existing helpers when possible
3. Follow naming conventions
4. Add language strings to `locales/*.json`
5. Test thoroughly before committing
6. Update this document if adding new folders/major features

---

## 📞 Support

- **Support Channel:** [TheInfinityAI](https://t.me/TheInfinityAI)
- **Developer:** [Hasindu Lakshan](https://t.me/Hasindu_Lakshan)

---

---

**Last Updated:** March 4, 2026
