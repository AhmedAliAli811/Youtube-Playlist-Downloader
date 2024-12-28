# YouTube Playlist Downloader

A Python script to automate downloading videos from a YouTube playlist. It checks for new videos in a playlist and downloads them to a specified directory. Additionally, it sends email notifications listing the newly downloaded videos.

## Features

- **Automated Downloads**: Manually run the script to check for new videos in a specified YouTube playlist and download them.
- **Email Notifications**: Sends an email summarizing the newly downloaded videos after each check.
- **Download Tracking**: Maintains a log of downloaded videos to prevent duplicate downloads.

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`):
  - `yt-dlp`
  - `ffmpeg`
 
## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AhmedAliAli811/YouTube-Playlist-Downloader-.git
   cd YouTube-Playlist-Downloader-
   ```

2. **Install Dependencies**:
   Use `pip` to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Rename `.env.example` to `.env`.
   - Update the `.env` file with your configuration:
     ```env
     PLAYLIST_URL=your_playlist_url_here
     DOWNLOAD_PATH=your_download_path_here
     LOG_FILE=downloaded_videos.json
     SENDER_EMAIL=your_email@example.com
     SENDER_PASSWORD=your_email_password
     RECEIVER_EMAIL=receiver_email@example.com
     ```

   **Parameters**:
   - `PLAYLIST_URL`: The URL of the YouTube playlist.
   - `DOWNLOAD_PATH`: The directory where downloaded videos will be stored.
   - `LOG_FILE`: The name of the .txt file used to track downloaded videos.
   - `SENDER_EMAIL`: The email address used to send notifications.
   - `SENDER_PASSWORD`: The password or app-specific password for the sender email.
   - `RECEIVER_EMAIL`: The email address where notifications will be sent.

## Usage

Run the script using Python:
```bash
python main.py
```

The script will check for new videos in the specified playlist and download them.

## Automating with Windows Task Scheduler

To automate the script and run it at specific intervals:

1. **Open Task Scheduler**:
   - Search for "Task Scheduler" in the Start menu.

2. **Create a New Task**:
   - Click **"Create Task"**.
   - In the **General** tab, set a name (e.g., "YouTube Playlist Downloader").
   - Check **"Run whether user is logged on or not"**.
   - Check **"Run with highest privileges"**.

3. **Set the Trigger**:
   - Go to the **Triggers** tab and click **"New"**.
   - Set the trigger to **Weekly** and choose the desired day and time (e.g., every Friday at 12:00 PM).

4. **Set the Action**:
   - Go to the **Actions** tab and click **"New"**.
   - Set the action to **"Start a Program"**.
   - Program/script: `python`.
   - Add arguments: `C:\path\to\main.py`.
   - Start in: `C:\path\to\your\project\directory`.

5. **Complete the Setup**:
   - Click **OK** to save the task.
   - Enter your Windows credentials if prompted.

The script will now run automatically at the specified time.
