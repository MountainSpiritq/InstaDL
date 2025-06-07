import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import static_ffmpeg

static_ffmpeg.add_paths()

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Downloader")
        self.download_path = ""
        self.setup_gui()

    def setup_gui(self):
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=5)

        self.path_label = tk.Label(path_frame, text="No folder selected", anchor='w')
        self.path_label.pack(side=tk.LEFT, padx=5)

        tk.Button(path_frame, text="Select Download Directory 📁", command=self.get_directory).pack(side=tk.LEFT)

        url_frame = tk.Frame(self.root)
        url_frame.pack(pady=5)
        self.url_entry = tk.Entry( url_frame, width=50)
        self.url_entry.insert(0, "Insta URLs go here")
        self.url_entry.pack(side=tk.LEFT ,padx=10, pady=5)
        self.url_entry.bind("<FocusIn>", self.on_entry_clicked)
        def onEnter(_):
            self.start_download()
            self.on_entry_delete()

        self.url_entry.bind('<Return>',onEnter)
       
        tk.Button(url_frame, text="Download", command=self.start_download).pack(pady=5)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

    def get_directory(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.download_path = selected_folder
            self.path_label.config(text=self.download_path)

    def on_entry_clicked(self, event):
        if self.url_entry.get() == "Insta URLs go here":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg='black')

    def on_entry_delete(self):
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg='black')

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Required", "Please enter a URL.")
            return

        if not self.download_path:
            messagebox.showwarning("Directory Required", "Please select a download folder first.")
            return

        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url):
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = round(d.get('_percent', 0))
                self.status_label.config(text=f"Downloading:{d.get('info_dict').get('title')} {percent}%")
                self.root.update_idletasks()
            elif d['status'] == 'finished':
                self.status_label.config(text=f"Download of {d.get('info_dict').get('title')} completed.")
                

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
