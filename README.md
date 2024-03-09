# Bix

Simple C.R.U.D. application to manage books/users locally.

## Run

Choose your own adventure.

### Python

```bash
python3 -mpip install .
bix
```

### Docker

```bash
docker build . -t bix
docker run --rm -v ./data:/home/user --network host bix
```

### Docker Compose

```bash
mkdir data
docker compose up
```
