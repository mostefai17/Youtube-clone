# YouTube Clone

A full-stack video sharing platform built with Django that demonstrates user authentication, cloud media storage, adaptive video streaming, and REST API integration.

---

## Features

- User registration and authentication
- Video upload
- Adaptive HLS video streaming
- ImageKit cloud storage integration
- Like and dislike system
- Dynamic user channels
- View counter
- Responsive interface
- REST API documentation with DRF Spectacular

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django 6 |
| Language | Python 3.12 |
| Database | SQLite |
| Storage | ImageKit |
| API | Django REST Framework |
| Documentation | DRF Spectacular |
| Dependency Manager | uv |
| Containerization | Docker & Docker Compose |

---

## Architecture

```
Browser
     │
     ▼
 Django Views
     │
 ┌── Authentication
 ├── Video Upload
 ├── Streaming
 ├── Likes
 └── Channels
     │
     ▼
SQLite Database
     │
     ▼
ImageKit Cloud Storage
```

---

## Getting Started

### Clone

```bash
git clone https://github.com/USERNAME/Youtube-clone.git

cd Youtube-clone
```

### Configure Environment

```bash
cp .env.example .env
```

Fill in your ImageKit credentials and Django secret key.

### Run with Docker

```bash
docker compose up --build
```

Application:

```
http://localhost:8080
```

---

## Development

Without Docker

```bash
uv sync

uv run python manage.py migrate

uv run python manage.py runserver
```

---

## Environment Variables

```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

IMAGEKIT_PUBLIC_KEY=
IMAGEKIT_PRIVATE_KEY=
IMAGEKIT_URL_ENDPOINT=
```

---

## Project Structure

```
Youtube-clone/

├── youtube/
│   ├── accounts/
│   ├── videos/
│   ├── static/
│   └── templates/
│
├── youtube_clone/
│   ├── settings.py
│   └── urls.py
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## Roadmap

- [x] Authentication
- [x] Video Upload
- [x] ImageKit Integration
- [x] Adaptive Streaming
- [x] Docker Support
- [ ] Pagination
- [ ] Search
- [ ] Unit Tests
- [ ] GitHub Actions CI
- [ ] PostgreSQL Support

---

## Screenshots

> Add screenshots of:
> ![upload.png](../../Pictures/Screenshots/upload.png)
> ![layout.png](../../Pictures/Screenshots/layout.png)
> ![channel.png](../../Pictures/Screenshots/channel.png)
> ![create-account.png](../../Pictures/Screenshots/create-account.png)
> ![sign-in.png](../../Pictures/Screenshots/sign-in.png)

---

## License

MIT

---

## Author

Mohamed Ilias Mostefai

Python Web Developer