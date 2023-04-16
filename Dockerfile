FROM python:3.9

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install discord.py pynacl
RUN pip install git+https://github.com/ytdl-org/youtube-dl.git@master

COPY . /app
WORKDIR /app

CMD [ "python", "discord_test.py" ]