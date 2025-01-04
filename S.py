import os
from datetime import datetime
import yt_dlp
import requests
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if 'youtu.be' in url:
        return url.split('/')[-1]
    parsed_url = urlparse(url)
    if '/shorts/' in url:
        return url.split('/shorts/')[-1].split('?')[0]
    return parse_qs(parsed_url.query)['v'][0]

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
            'extract_flat': False,
        }

        print("Fetching video information...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
          
            video_title = info.get('title', 'Unknown Title')
            channel_name = info.get('channel', 'Unknown Channel')
            channel_id = info.get('channel_id', 'Unknown ID')
            channel_url = info.get('channel_url', '')
            channel_handle = info.get('uploader_id', 'Unknown Handle')
            
            
            channel_thumbnails = info.get('channel_thumbnail', info.get('thumbnail', ''))
            
          
            print("\nDownload completed successfully!")
            print(f"Video Title: {video_title}")
            print(f"Creator Information:")
            print(f"- Channel Name: {channel_name}")
            print(f"- Channel Handle: @{channel_handle}")
            print(f"- Channel URL: {channel_url}")
            print(f"- Channel Thumbnail URL: {channel_thumbnails}")
            
           
            if channel_thumbnails:
                try:
                    response = requests.get(channel_thumbnails)
                    if response.status_code == 200:
                        profile_pic_path = os.path.join('youtube_shorts', f'channel_profile_{channel_id}.jpg')
                        with open(profile_pic_path, 'wb') as f:
                            f.write(response.content)
                        print(f"- Profile picture saved to: {profile_pic_path}")
                except Exception as e:
                    print(f"Failed to download profile picture: {str(e)}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    print("YouTube Shorts Downloader")
    while True:
        url = input("\nEnter YouTube Shorts URL: ").strip()
        
        if not url:
            print("Please enter a valid URL")
            continue
            
        if "youtube.com" not in url and "youtu.be" not in url:
            print("Error: Please enter a valid YouTube URL")
            continue
            
        download_youtube_short(url)

if __name__ == "__main__":
    main()