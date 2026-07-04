<div align="center">

<img src="https://i.ibb.co/cKzySsgr/yy.png" alt="Hasii Music" width="300"/>
<img src="https://files.catbox.moe/f3i3yi.png" alt="Hasii Music" width="300"/>

# 🎵 ˹ʜᴀꜱɪɪ ᴍᴜꜱɪᴄ˼

**An Advanced & Powerful Telegram Music Player Bot Written in Python**

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/hasindu-nagolla/HasiiMusicBot?style=for-the-badge&color=yellow)](https://github.com/hasindu-nagolla/HasiiMusicBot/stargazers)

[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/TheInfinityAI)
[![Telegram Support](https://img.shields.io/badge/Telegram-Support-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Hasindu_Lakshan)

</div>

---

# 📑 Table of Contents

- [✨ Features](#-features)
- [🚀 Deployment](#-deployment)
  - [✔️ Prerequisites](#️-prerequisites)
  - [⚙️ Environment Variables](#️-environment-variables)
  - [🛠 Installation](#-installation)
- [📖 Commands](#-commands)
- [🤝 Contributing](#-contributing)
- [📞 Support & Contact](#-support--contact)
- [🙏 Credits](#-credits)

---

# ✨ Features

- 🎵 **High-Quality Streaming** — Crystal-clear audio powered by the Opus codec.
- 📻 **Live Radio** — Stream 50+ international and local radio stations.
- 🎧 **YouTube Support** — Play music using YouTube URLs or search queries.
- 📝 **Smart Queue System** — Queue multiple tracks with ease.
- ⚡ **Fast & Reliable** — Built with Pyrogram and PyTgCalls.
- 🎛 **Playback Controls** — Pause, Resume, Skip, Seek and Stop.
- 👥 **Authorization System** — Only authorized users can control playback.
- 🔄 **Auto Leave** — Automatically exits inactive voice chats.

---

# 🚀 Deployment

## ✔️ Prerequisites

Install the following before running the bot:

- Python **3.10+**
- Deno
- FFmpeg

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg curl unzip

curl -fsSL https://deno.land/install.sh | sh
```

---

## ⚙️ Environment Variables

Create a `.env` file inside the project root.

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

MONGO_DB_URI=your_mongodb_uri

LOGGER_ID=your_logger_group_id
OWNER_ID=your_user_id

STRING_SESSION=your_pyrogram_string

COOKIE_URL=your_cookie_url
```

| Variable | Description |
|----------|-------------|
| `API_ID` | Telegram API ID from https://my.telegram.org |
| `API_HASH` | Telegram API Hash |
| `BOT_TOKEN` | Bot Token from @BotFather |
| `MONGO_DB_URI` | MongoDB Connection URI |
| `LOGGER_ID` | Log Group ID |
| `OWNER_ID` | Telegram User ID |
| `STRING_SESSION` | Pyrogram String Session |
| `COOKIE_URL` | *(Optional)* YouTube Cookies URL |

---

## 🛠 Installation

### Method 1 — Standard Installation

Clone the repository.

```bash
git clone https://github.com/hasindu-nagolla/HasiiMusicBot.git
cd HasiiMusicBot
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create the environment file.

```bash
cp sample.env .env
```

Run the bot.

```bash
bash start
```

---

### Method 2 — Docker 🐳

Build the Docker image.

```bash
docker build -t hasiimusicbot:latest .
```

Run the container.

```bash
docker run -d \
  --restart unless-stopped \
  --env-file .env \
  -v ./HasiiMusic/cookies:/app/HasiiMusic/cookies \
  -v ./downloads:/app/downloads \
  --name hasiimusicbot \
  hasiimusicbot:latest
```

Or simply use Docker Compose.

```bash
docker-compose up -d --build
```

---

# 📖 Commands

## 👤 User Commands

| Command | Description |
|---------|-------------|
| `/play <song/url>` | Play music using a YouTube link or search query |
| `/radio` | Browse live radio stations |
| `/queue` | Show current playlist |
| `/ping` | Check bot latency |
| `/help` | Show help menu |

---

## 🛡 Admin Commands

| Command | Description |
|---------|-------------|
| `/pause` | Pause playback |
| `/resume` | Resume playback |
| `/skip` | Skip current song |
| `/next` | Skip current song |
| `/stop` | Stop playback |
| `/end` | Stop playback and clear queue |
| `/seek <time>` | Seek to a specific timestamp |
| `/reload` | Reload admin cache |

---

## 👑 Sudo / Owner Commands

| Command | Description |
|---------|-------------|
| `/stats` | Show bot statistics |
| `/broadcast` | Broadcast a message |
| `/addsudo` | Add sudo user |
| `/rmsudo` | Remove sudo user |
| `/gban` | Global ban a user |
| `/ungban` | Remove global ban |
| `/maintenance` | Toggle maintenance mode |
| `/restart` | Restart the bot |
| `/logs` | Fetch latest logs |

---

# 🤝 Contributing

Contributions are always welcome.

1. Fork the repository.
2. Create your feature branch.

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes.

```bash
git commit -m "Add AmazingFeature"
```

4. Push your branch.

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request.

If you find a bug or have a feature request, feel free to open an Issue.

---

# 📞 Support & Contact

| Platform | Link |
|----------|------|
| 👨‍💻 Developer | https://github.com/hasindu-nagolla |
| 📢 Telegram Channel | https://t.me/TheInfinityAI |
| 💬 Telegram Support | https://t.me/Hasindu_Lakshan |

---

# 🙏 Credits

- ❤️ Inspired by **AnonymousX1025**
- 💙 Built using **Pyrogram**
- 🎙 Voice streaming powered by **PyTgCalls**

---

<div align="center">

### ⭐ If you like this project, don't forget to leave a star on GitHub!

Made with ❤️ by **Hasindu Nagolla**

</div>
