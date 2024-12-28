import yt_dlp
import os
import re
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

PLAYLIST_URL = os.getenv("PLAYLIST_URL")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
LOG_FILE = os.getenv("LOG_FILE")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")



def send_email_notification(subject, body):
    """Send an email notification."""
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    receiver_email = RECEIVER_EMAIL

    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def download_playlist(playlist_url, log_file, download_dir):
    """Downloads a YouTube playlist, logs downloaded videos, and checks for new videos."""

    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save with video title
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Download up to 720p
        'merge_output_format': 'mp4',  # Ensure output is in mp4 format
        'nocheckcertificate': True,  # Handle potential certificate issues
        'no_warnings': True,  # Suppress warnings
        'quiet': True,  # Suppress yt-dlp output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            entries = playlist_info.get('entries', [])
            playlist_title = playlist_info['title']

            downloaded_videos = set()
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        video_id = line.strip().split(" - ")[0] # Extract video ID from log
                        downloaded_videos.add(video_id)


            videos_to_download = []
            newly_downloaded_videos = []
            for entry in entries:
                video_id = entry.get('id')
                if video_id not in downloaded_videos:
                    videos_to_download.append(entry)

            if videos_to_download:
              print(f"Found {len(videos_to_download)} new videos. Downloading...")
              for entry in videos_to_download:
                  try:
                    ydl.download([entry['webpage_url']])
                    with open(log_file, 'a', encoding='utf-8') as f:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"{entry['id']} - {entry['title']} - {now}\n")
                    newly_downloaded_videos.append(entry['title'])
                  except Exception as e:
                    print(f"Error downloading {entry.get('title', 'unknown')}: {e}")
            else:
                print("No new videos found.")
            if newly_downloaded_videos:
                subject = f"\nصباح الخير فى فيديو جديد نزل فى البلايليست ديه {playlist_title} "
                body = "وديه الفيديوهات اللى نزلت:\n\n" + "\n".join(newly_downloaded_videos)
                send_email_notification(subject, body)


    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading playlist: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    playlist_url = PLAYLIST_URL
    download_dir = DOWNLOAD_DIR
    log_file = LOG_FILE

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    download_playlist(playlist_url, log_file, download_dir)
    print("Finished.")
