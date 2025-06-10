import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(800, 600)

        # Variables
        self.url_var = ctk.StringVar()
        self.download_path = ctk.StringVar(value=os.getcwd())
        self.format_var = ctk.StringVar(value="video")
        self.quality_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Ready to download")
        self.progress_var = ctk.DoubleVar(value=0.0)

        self.video_info = None
        self.available_formats = []
        self.quality_options_map = {}

        self.build_gui()

    def build_gui(self):
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Main scrollable frame
        main_scrollable = ctk.CTkScrollableFrame(
            self.root, 
            corner_radius=0,
            fg_color=("gray95", "gray10")
        )
        main_scrollable.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        main_scrollable.grid_columnconfigure(0, weight=1)

        # Header section with gradient-like effect
        header_frame = ctk.CTkFrame(
            main_scrollable, 
            corner_radius=25,
            height=120,
            fg_color=("white", "gray20"),
            border_width=2,
            border_color=("gray80", "gray40")
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 20))
        header_frame.grid_propagate(False)

        # Title with enhanced styling
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🎬 YouTube Downloader Pro", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("gray20", "white")
        )
        title_label.pack(expand=True)

        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text="Download videos and audio in high quality", 
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray70")
        )
        subtitle_label.pack()

        # URL Input Section with enhanced styling
        url_section = ctk.CTkFrame(
            main_scrollable, 
            corner_radius=20,
            fg_color=("white", "gray20"),
            border_width=1,
            border_color=("gray85", "gray35")
        )
        url_section.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 20))
        
        url_header = ctk.CTkFrame(url_section, fg_color="transparent")
        url_header.pack(fill='x', padx=25, pady=(20, 10))
        
        url_icon_label = ctk.CTkLabel(
            url_header, 
            text="🔗", 
            font=ctk.CTkFont(size=18)
        )
        url_icon_label.pack(side='left')
        
        url_title = ctk.CTkLabel(
            url_header, 
            text="Video URL", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray20", "white")
        )
        url_title.pack(side='left', padx=(10, 0))
        
        url_input_container = ctk.CTkFrame(url_section, fg_color="transparent")
        url_input_container.pack(fill='x', padx=25, pady=(0, 20))
        
        self.url_entry = ctk.CTkEntry(
            url_input_container, 
            textvariable=self.url_var, 
            height=50,
            font=ctk.CTkFont(size=13),
            placeholder_text="Paste your YouTube URL here...",
            corner_radius=15,
            border_width=2,
            border_color=("gray80", "gray40")
        )
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        self.clear_url_btn = ctk.CTkButton(
            url_input_container, 
            text="🗑️ Clear", 
            command=self.clear_url,
            height=50,
            width=100,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            corner_radius=15
        )
        self.clear_url_btn.pack(side='right')

        # Download Path Section
        path_section = ctk.CTkFrame(
            main_scrollable, 
            corner_radius=20,
            fg_color=("white", "gray20"),
            border_width=1,
            border_color=("gray85", "gray35")
        )
        path_section.grid(row=2, column=0, sticky="ew", padx=25, pady=(0, 20))
        
        path_header = ctk.CTkFrame(path_section, fg_color="transparent")
        path_header.pack(fill='x', padx=25, pady=(20, 10))
        
        path_icon_label = ctk.CTkLabel(
            path_header, 
            text="📁", 
            font=ctk.CTkFont(size=18)
        )
        path_icon_label.pack(side='left')
        
        path_title = ctk.CTkLabel(
            path_header, 
            text="Download Location", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray20", "white")
        )
        path_title.pack(side='left', padx=(10, 0))
        
        path_input_container = ctk.CTkFrame(path_section, fg_color="transparent")
        path_input_container.pack(fill='x', padx=25, pady=(0, 20))
        
        self.path_entry = ctk.CTkEntry(
            path_input_container, 
            textvariable=self.download_path, 
            height=50,
            font=ctk.CTkFont(size=13),
            corner_radius=15,
            border_width=2,
            border_color=("gray80", "gray40")
        )
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        self.browse_btn = ctk.CTkButton(
            path_input_container, 
            text="📂 Browse", 
            command=self.browse_path,
            height=50,
            width=120,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=15
        )
        self.browse_btn.pack(side='right')

        # Analyze Button with enhanced styling
        analyze_container = ctk.CTkFrame(main_scrollable, fg_color="transparent")
        analyze_container.grid(row=3, column=0, sticky="ew", padx=25, pady=20)
        
        self.analyze_btn = ctk.CTkButton(
            analyze_container, 
            text="🔍 Analyze Video", 
            command=self.start_analysis,
            height=55,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=25,
            fg_color=("gray20", "#1f538d"),
            hover_color=("gray30", "#14375e")
        )
        self.analyze_btn.pack()

        # Video Info Card with enhanced design
        self.info_card = ctk.CTkFrame(
            main_scrollable, 
            corner_radius=20,
            fg_color=("white", "gray20"),
            border_width=1,
            border_color=("gray85", "gray35")
        )
        
        # Video Details Section
        self.video_details_frame = ctk.CTkFrame(
            self.info_card, 
            fg_color="transparent"
        )
        self.video_details_frame.pack(fill='x', padx=25, pady=(20, 15))

        # Format and Quality Selection Container
        options_container = ctk.CTkFrame(self.info_card, fg_color="transparent")
        options_container.pack(fill='x', padx=25, pady=(0, 15))
        
        # Format Selection with enhanced styling
        format_frame = ctk.CTkFrame(
            options_container, 
            corner_radius=15,
            fg_color=("gray95", "gray15"),
            border_width=1,
            border_color=("gray80", "gray40")
        )
        format_frame.pack(fill='x', pady=(0, 15))
        
        format_header = ctk.CTkFrame(format_frame, fg_color="transparent")
        format_header.pack(fill='x', padx=20, pady=(15, 10))
        
        format_icon = ctk.CTkLabel(
            format_header, 
            text="🎞️", 
            font=ctk.CTkFont(size=16)
        )
        format_icon.pack(side='left')
        
        format_label = ctk.CTkLabel(
            format_header, 
            text="Format Type", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray20", "white")
        )
        format_label.pack(side='left', padx=(10, 0))
        
        self.format_combo = ctk.CTkComboBox(
            format_frame, 
            variable=self.format_var, 
            values=["video", "audio"],
            state='readonly',
            width=150,
            height=40,
            font=ctk.CTkFont(size=13),
            command=self.on_format_change,
            corner_radius=10
        )
        self.format_combo.pack(padx=20, pady=(0, 15))

        # Quality Selection with enhanced styling
        quality_frame = ctk.CTkFrame(
            options_container, 
            corner_radius=15,
            fg_color=("gray95", "gray15"),
            border_width=1,
            border_color=("gray80", "gray40")
        )
        quality_frame.pack(fill='x')
        
        quality_header = ctk.CTkFrame(quality_frame, fg_color="transparent")
        quality_header.pack(fill='x', padx=20, pady=(15, 10))
        
        quality_icon = ctk.CTkLabel(
            quality_header, 
            text="📶", 
            font=ctk.CTkFont(size=16)
        )
        quality_icon.pack(side='left')
        
        quality_label = ctk.CTkLabel(
            quality_header, 
            text="Quality Selection", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray20", "white")
        )
        quality_label.pack(side='left', padx=(10, 0))
        
        self.quality_combo = ctk.CTkComboBox(
            quality_frame, 
            variable=self.quality_var, 
            state='disabled', 
            width=500,
            height=40,
            font=ctk.CTkFont(size=13),
            corner_radius=10
        )
        self.quality_combo.pack(padx=20, pady=(0, 10))

        # Quality Info Label
        self.quality_info_label = ctk.CTkLabel(
            quality_frame, 
            text="", 
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        self.quality_info_label.pack(padx=20, pady=(0, 15))

        # Download Button with enhanced styling
        download_container = ctk.CTkFrame(self.info_card, fg_color="transparent")
        download_container.pack(fill='x', padx=25, pady=(10, 25))
        
        self.download_btn = ctk.CTkButton(
            download_container, 
            text="⬇️ Download Now", 
            command=self.start_download, 
            state='disabled',
            height=55,
            width=250,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=25,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#17a2b8")
        )
        self.download_btn.pack()

        # Progress Section with enhanced styling
        progress_section = ctk.CTkFrame(
            main_scrollable, 
            corner_radius=20,
            fg_color=("white", "gray20"),
            border_width=1,
            border_color=("gray85", "gray35")
        )
        progress_section.grid(row=5, column=0, sticky="ew", padx=25, pady=20)
        
        progress_header = ctk.CTkFrame(progress_section, fg_color="transparent")
        progress_header.pack(fill='x', padx=25, pady=(20, 10))
        
        progress_icon = ctk.CTkLabel(
            progress_header, 
            text="⚡", 
            font=ctk.CTkFont(size=16)
        )
        progress_icon.pack(side='left')
        
        progress_title = ctk.CTkLabel(
            progress_header, 
            text="Progress", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray20", "white")
        )
        progress_title.pack(side='left', padx=(10, 0))

        # Progress Bar with enhanced styling
        self.progressbar = ctk.CTkProgressBar(
            progress_section, 
            height=25, 
            corner_radius=15,
            progress_color=("#28a745", "#20c997")
        )
        self.progressbar.pack(fill='x', padx=25, pady=(0, 10))
        self.progressbar.set(0)

        # Status Label with enhanced styling
        self.status_label = ctk.CTkLabel(
            progress_section, 
            textvariable=self.status_var, 
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray70")
        )
        self.status_label.pack(pady=(0, 20))

        # Add some bottom padding
        bottom_spacer = ctk.CTkFrame(main_scrollable, height=30, fg_color="transparent")
        bottom_spacer.grid(row=6, column=0, sticky="ew")

    def clear_url(self):
        """Clear the URL input field and hide info card if visible"""
        self.url_var.set("")
        self.info_card.grid_forget()
        self.status_var.set("Ready to download")
        self.progressbar.set(0)
        
        # Clear video details
        for widget in self.video_details_frame.winfo_children():
            widget.destroy()
        
        # Reset button states
        self.analyze_btn.configure(state='normal', text="🔍 Analyze Video")
        self.download_btn.configure(state='disabled', text="⬇️ Download Now")

    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.download_path.get())
        if path:
            self.download_path.set(path)

    def start_analysis(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Input Error", "Please enter a YouTube video URL.")
            return

        self.analyze_btn.configure(state='disabled', text="🔄 Analyzing...")
        self.status_var.set("Analyzing video information...")
        self.progress_var.set(0)
        self.progressbar.set(0)
        self.quality_var.set("")
        self.quality_combo.configure(state='disabled')
        self.download_btn.configure(state='disabled')
        
        # Clear previous video details
        for widget in self.video_details_frame.winfo_children():
            widget.destroy()
        
        # Hide info card during analysis
        self.info_card.grid_forget()

        threading.Thread(target=self._analyze_thread, args=(url,), daemon=True).start()

    def _analyze_thread(self, url):
        try:
            ydl_opts = {'quiet': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.video_info = info
                self.available_formats = info.get("formats", [])
            self.root.after(0, self.update_ui_post_analysis)
        except Exception as e:
            self.root.after(0, lambda: self.analysis_failed(str(e)))

    def analysis_failed(self, error_msg):
        self.status_var.set("Analysis failed - please check the URL")
        self.analyze_btn.configure(state='normal', text="🔍 Analyze Video")
        messagebox.showerror("Analysis Error", f"Could not analyze video.\n\n{error_msg}")

    def update_ui_post_analysis(self):
        self.status_var.set("Analysis complete - select quality and download")
        self.analyze_btn.configure(state='normal', text="🔍 Analyze Video")
        
        # Show info card
        self.info_card.grid(row=4, column=0, sticky="ew", padx=25, pady=(0, 20))

        # Display video information with enhanced styling
        title = self.video_info.get("title", "Unknown Title")
        uploader = self.video_info.get("uploader", "Unknown")
        duration = self.video_info.get("duration", 0)
        view_count = self.video_info.get("view_count", 0)
        formatted_duration = f"{duration // 60}m {duration % 60}s" if duration else "Unknown"
        formatted_views = f"{view_count:,}" if view_count else "Unknown"

        # Video info header
        info_header = ctk.CTkFrame(
            self.video_details_frame, 
            corner_radius=15,
            fg_color=("gray95", "gray15"),
            border_width=1,
            border_color=("gray80", "gray40")
        )
        info_header.pack(fill='x', pady=(0, 15))

        title_label = ctk.CTkLabel(
            info_header, 
            text=f"🎬 {title}", 
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=750,
            text_color=("gray20", "white")
        )
        title_label.pack(padx=20, pady=(15, 5))
        
        # Video metadata in a grid-like layout
        metadata_frame = ctk.CTkFrame(info_header, fg_color="transparent")
        metadata_frame.pack(fill='x', padx=20, pady=(5, 15))
        
        uploader_label = ctk.CTkLabel(
            metadata_frame, 
            text=f"👤 {uploader}", 
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray60")
        )
        uploader_label.pack(side='left', padx=(0, 20))
        
        duration_label = ctk.CTkLabel(
            metadata_frame, 
            text=f"⏱️ {formatted_duration}", 
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray60")
        )
        duration_label.pack(side='left', padx=(0, 20))
        
        views_label = ctk.CTkLabel(
            metadata_frame, 
            text=f"👁️ {formatted_views} views", 
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray60")
        )
        views_label.pack(side='left')

        self.update_quality_options()

    def update_quality_options(self):
        selected_format = self.format_var.get()
        self.quality_options_map.clear()
        quality_labels = []

        for fmt in self.available_formats:
            if selected_format == "video" and fmt.get('vcodec') != 'none':
                filesize = fmt.get('filesize_approx', 0) // 1_000_000 if fmt.get('filesize_approx') else '?'
                resolution = fmt.get('resolution', 'Unknown')
                fps = fmt.get('fps', '')
                fps_text = f" @ {fps}fps" if fps else ""
                label = f"{resolution}{fps_text} - {fmt.get('ext', 'mp4').upper()} - ~{filesize}MB"
                self.quality_options_map[label] = fmt
                quality_labels.append(label)
            elif selected_format == "audio" and fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                filesize = fmt.get('filesize_approx', 0) // 1_000_000 if fmt.get('filesize_approx') else '?'
                abr = fmt.get('abr', 'Unknown')
                label = f"{abr}kbps - {fmt.get('ext', 'mp3').upper()} - ~{filesize}MB"
                self.quality_options_map[label] = fmt
                quality_labels.append(label)

        if quality_labels:
            # Sort by quality (attempt to put highest first)
            quality_labels.sort(reverse=True)
            self.quality_combo.configure(state='readonly', values=quality_labels)
            self.quality_combo.set(quality_labels[0])
            self.download_btn.configure(state='normal')
            self.quality_info_label.configure(
                text="✅ Quality options loaded - select your preferred format above",
                text_color=("#28a745", "#20c997")
            )
        else:
            self.quality_combo.configure(state='disabled')
            self.download_btn.configure(state='disabled')
            self.quality_info_label.configure(
                text="❌ No formats available for the selected type",
                text_color=("#dc3545", "#e74c3c")
            )

    def on_format_change(self, choice=None):
        self.update_quality_options()

    def start_download(self):
        selected_label = self.quality_var.get()
        if not selected_label or selected_label not in self.quality_options_map:
            messagebox.showwarning("Quality Not Selected", "Please select a quality option.")
            return

        format_info = self.quality_options_map[selected_label]
        format_id = format_info.get('format_id')
        if not format_id:
            messagebox.showerror("Format Error", "Invalid format selected.")
            return

        self.status_var.set("Preparing download...")
        self.download_btn.configure(state='disabled', text="⬇️ Downloading...")
        threading.Thread(target=self._download_thread, args=(format_id,), daemon=True).start()

    def _download_thread(self, format_id):
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent_str = d.get('_percent_str', '0.0%').replace('%', '')
                speed = d.get('_speed_str', 'Unknown')
                eta = d.get('_eta_str', 'Unknown')
                try:
                    percent = float(percent_str)
                    self.root.after(0, lambda: self.progressbar.set(percent / 100))
                    self.root.after(0, lambda: self.status_var.set(f"Downloading... {percent_str}% | Speed: {speed} | ETA: {eta}"))
                except:
                    pass
            elif d['status'] == 'finished':
                self.root.after(0, lambda: self.status_var.set("Processing download..."))

        try:
            output_path = os.path.join(self.download_path.get(), '%(title)s.%(ext)s')
            ydl_opts = {
                'format': f"{format_id}+bestaudio/best",
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
                'progress_hooks': [progress_hook],
                'quiet': True,
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url_var.get().strip()])
            self.root.after(0, self.download_complete)
        except Exception as e:
            self.root.after(0, lambda: self.download_failed(str(e)))

    def download_complete(self):
        self.status_var.set("Download completed successfully! 🎉")
        self.download_btn.configure(
            state='normal', 
            text="✅ Download Complete",
            fg_color=("#28a745", "#20c997")
        )
        self.progressbar.set(1.0)
        messagebox.showinfo("Success", "Your download has been completed successfully!")
        
        # Reset download button after a delay
        self.root.after(5000, lambda: self.download_btn.configure(
            text="⬇️ Download Now",
            fg_color=("#28a745", "#20c997")
        ))

    def download_failed(self, error_msg):
        self.status_var.set("Download failed - please try again ❌")
        self.download_btn.configure(
            state='normal', 
            text="⬇️ Download Now",
            fg_color=("#28a745", "#20c997")
        )
        self.progressbar.set(0)
        messagebox.showerror("Download Error", f"Failed to download video.\n\n{error_msg}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = YouTubeDownloader(root)
    root.mainloop()