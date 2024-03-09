FROM python:3.10.13

RUN useradd -ms /bin/bash user && mkdir /app && chown user:user /app

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir . && rm -rf /app

USER user

WORKDIR /home/user/

CMD ["bix"]
