import yt_dlp
from tkinter import filedialog, messagebox
import tkinter as tk
import static_ffmpeg
static_ffmpeg.add_paths()

download_path = ""

def downloadInstaVideo(url, path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def getDirectory():
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        messagebox.showinfo("Folder Selected", f"Download folder set to:\n{download_path}")

def startDownload():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Required", "Please enter a URL.")
        return

    if not download_path:
        messagebox.showwarning("Directory Required", "Please select a download folder first.")
        return        

    downloadInstaVideo(url, download_path)

# GUI Setup
root = tk.Tk()
root.title("Instagram Downloader")

tk.Label(root, text="Instagram URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10, pady=5)

tk.Button(root, text="Select Download Directory", command=getDirectory).pack()
tk.Button(root, text="Download", command=startDownload).pack(pady=10)

root.mainloop()
