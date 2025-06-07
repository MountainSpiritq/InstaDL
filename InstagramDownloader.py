import yt_dlp
from tkinter import filedialog, messagebox,ttk
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
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        download_path = selected_folder
        path_label.config(text=download_path)
        messagebox.showinfo("Folder Selected", f"Download folder set to:\n{download_path}")

def startDownload(event=None):
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Required", "Please enter a URL.")
        return

    if not download_path:
        messagebox.showwarning("Directory Required", "Please select a download folder first.")
        return        

    downloadInstaVideo(url, download_path)

def OnEntryClicked(event):
    if url_entry.get() == "Insta url-s go here":
        url_entry.delete(0, tk.END)
        url_entry.config(fg='black')

root = tk.Tk()
root.title("Instagram Downloader")

path_frame = tk.Frame(root)
path_frame.pack(pady=5)

path_label = tk.Label(path_frame, text="No folder selected", anchor='w')
path_label.pack(side=tk.LEFT, padx=5)

tk.Button(path_frame, text="Select Download Directory 📁", command=getDirectory).pack(side=tk.LEFT)

url_entry = tk.Entry(root, width=50)
url_entry.insert(0,"Insta url-s go here")
url_entry.pack(padx=10, pady=5)
url_entry.bind("<FocusIn>",OnEntryClicked)
url_entry.bind("<FocusOut>", startDownload)

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=listbox.yview)

items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
for item in items:
    listbox.insert(tk.END, item)


root.mainloop()
