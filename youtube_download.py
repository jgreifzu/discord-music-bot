from __future__ import unicode_literals
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '1'
    }]

}


def download_song(input='https://www.youtube.com/watch?v=KYmWZv2n7oM'):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if input.startswith("https://"): # if its a URL
            result = ydl.extract_info(input, download=True)
        else: # if its a search term
            result = ydl.extract_info(f"ytsearch:{input}", download=True)['entries'][0]
        filename = result['title']
        print(filename)
        return filename
