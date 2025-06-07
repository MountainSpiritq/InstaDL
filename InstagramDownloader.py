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
        self.root.geometry("600x400") 
        self.download_path = ""
        self.listView=[]
        self.setup_gui()

    def setup_gui(self):
        path_frame = ttk.Frame(self.root)
        path_frame.pack(fill='x', padx=15, pady=(15, 5))

        self.path_label = ttk.Label(path_frame, text="No folder selected", anchor='w')
        self.path_label.pack(side=tk.LEFT, fill='x', expand=True)

        ttk.Button(path_frame, text="Select Download Directory 📁", command=self.get_directory).pack(side=tk.RIGHT)

        url_frame = ttk.Frame(self.root)
        url_frame.pack(fill='x', padx=15, pady=5)

        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.insert(0, "Insta URLs go here")
        self.url_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10))
        self.url_entry.bind("<FocusIn>", self.on_entry_clicked)

        def onEnter(event):
            self.start_download()
            self.on_entry_delete()

        self.url_entry.bind('<Return>', onEnter)

        ttk.Button(url_frame, text="Download", command=self.start_download).pack(side=tk.RIGHT)

    
        self.status_label = ttk.Label(self.root, text="", foreground='blue')
        self.status_label.pack(fill='x', padx=15, pady=(10, 5))

        listbox_frame = ttk.Frame(self.root)
        listbox_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))

        ttk.Label(listbox_frame, text="Downloaded Videos:", font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0,5))

        self.listbox = tk.Listbox(listbox_frame, height=8)
        self.listbox.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.listbox.config(yscrollcommand=scrollbar.set)

    def get_directory(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.download_path = selected_folder
            self.path_label.config(text=self.download_path)

    def on_entry_clicked(self, event):
        if self.url_entry.get() == "Insta URLs go here":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(foreground='black')

    def on_entry_delete(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.config(foreground='black')

    def start_download(self):
        url = self.url_entry.get()
        if not url or url == "Insta URLs go here":
            messagebox.showwarning("Input Required", "Please enter a URL.")
            return

        if not self.download_path:
            messagebox.showwarning("Directory Required", "Please select a download folder first.")
            return

        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url):
        def progress_hook(d):
            
            self.listView=list(filter(lambda i : i.get('info_dict').get('id')!=d.get('info_dict').get('id'),self.listView))
            self.listView.append(d)

            if d['status'] == 'downloading':
                percent = round(d.get('_percent', 0))
                title = d.get('info_dict').get('title')
                self.status_label.config(text=f"Downloading: {title} {percent}%")
                self.root.update_idletasks()
            elif d['status'] == 'finished':
                title = d.get('info_dict').get('title')
                self.status_label.config(text=f"Download of {title} completed.")

            self.listbox.delete(0,tk.END)


            for i in self.listView:
                percent = round(i.get('_percent', 0))
                self.listbox.insert(tk.END,f"{i.get('info_dict').get('title')} {percent}%")

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
