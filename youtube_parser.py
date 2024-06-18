from pytube import YouTube,Playlist,Caption
import requests
from pydub import AudioSegment
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK,TYER, COMM, APIC, TSO2
import ffmpeg
import re

import os

def handle_playlist(link):
    playlist = Playlist(link)
    for videos in playlist.videos:
       convert_to_mp3(videos)
        

def convert_to_mp3(yt,output_path = '.'):
    stream = yt.streams.filter(only_audio=True).first()
    #remove special characters/symbols 
    proccessed_title = re.sub('[^a-zA-Z0-9 \n\.]','',yt.title)
    old_file = stream.download(filename=f"{proccessed_title}.mp4", output_path = output_path)
    mp3_file = proccessed_title+ '.mp3'
    
    AudioSegment.from_file(old_file).export(mp3_file,format='mp3')
    os.remove(old_file)
    
    thumbnail = yt.thumbnail_url
    thumbnail_data = requests.get(thumbnail).content
    thumbnail_path = proccessed_title+'.jpg'
    
    with open(thumbnail_path, 'wb') as f:
        f.write(thumbnail_data)
    
    #Writes metadata to mp3 file
    audio = ID3(mp3_file)
    audio.add(TIT2(encoding=3, text=yt.title))
    audio.add(TPE1(encoding=3, text= yt.author))
    audio.add(TALB(encoding=3, text = yt.title))
    # audio.add(COMM(encoding=3, text=yt.link))
    audio.add(TYER(eoncoding=3, text=str(yt.publish_date)))
    audio.add(APIC(
        encoding=3,
        mime='image/jpeg',
        type=3,
        desc=u'Cover',
        data=thumbnail_data
        
    ))
    audio.save(v2_version=3)
    os.remove(thumbnail_path)
    

    


def main():
    try:
        is_playlist = input("Is playlist(y or n)?: ")
        if is_playlist == "y":
            playlist = input("Enter a YouTube playlist to download: ")
            handle_playlist(playlist)
        else:
            link = input("Enter a YouTube URL to download: ")
            directory = input("What directory would you like to downolad to?: ")
            yt = YouTube(link)
            convert_to_mp3(yt,directory or ".")
    
    except Exception as e:
        print("An error occured: ", str(e))

if __name__ =="__main__":
    main()
    