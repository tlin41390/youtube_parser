from pytube import YouTube,Playlist,Caption
import urllib.request
from pydub import AudioSegment
import os

def convert_to_mp3(link,output_path = '.'):
    yt = YouTube(link)
    stream = yt.streams.filter(only_audio=True).first()
    old_file = stream.download(filename=f"{yt.title}.mp4", output_path = output_path)
    mp3_file = yt.title+ '.mp3'
    
    AudioSegment.from_file(old_file).export(mp3_file,format='mp3')
    os.remove(old_file)


def main():
    try:
        link = input("Enter a YouTube URL to download: ")
        directory = input("What directory would you like to downolad to?: ")
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()
        old_file = stream.download(filename=f"{yt.title}.mp4", output_path = directory)
        mp3_file = yt.title+ '.mp3'
        
        AudioSegment.from_file(old_file).export(mp3_file,format='mp3')
        os.remove(old_file)
        print("video downloaded in mp3")

        print(yt.publish_date)
        print(yt.author)
        print(link)
        print(yt.thumbnail_url)
        print(yt.metadata)
        
        

        response = urllib.request.urlopen(yt.thumbnail_url)
        image_data= response.read()

        with open(f"{yt.title}.jpg", "wb") as img_file:
            img_file.write(image_data)
        print("Thumbnail downloaded successfully.")

            
    except Exception as e:
        print("An error occured: ", str(e))

if __name__ =="__main__":
    main()
    