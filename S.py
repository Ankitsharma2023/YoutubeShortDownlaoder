import os
from datetime import datetime
import yt_dlp

def download_youtube_short(url):
    try:
        if not os.path.exists('youtube_shorts'):
            os.makedirs('youtube_shorts')

       
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ydl_opts = {
            'format': 'mp4/bestaudio/best',  
            'outtmpl': os.path.join('youtube_shorts', f'%(title)s_{timestamp}.%(ext)s'),
            'noplaylist': True,  
            'progress_hooks': [lambda d: print(f"Downloading: {d['_percent_str']} complete") if d['status'] == 'downloading' else None],
        }
        
        
        print("Initializing download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info['title']
            
        print(f"\nDownload completed successfully!")
        print(f"Title: {video_title}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    

def main():
    print("YouTube Shorts Downloader")
    while True:
        url = input("\nEnter YouTube Shorts URL:").strip()
    
        
        if not url:
            print("Please enter a valid URL")
            continue
            
        if "youtube.com" not in url and "youtu.be" not in url:
            print("Error: Please enter a valid YouTube URL")
            continue
            
        download_youtube_short(url)

if __name__ == "__main__":
    main()