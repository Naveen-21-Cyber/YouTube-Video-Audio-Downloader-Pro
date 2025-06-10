# 🎬 YouTube Downloader Pro

A modern, user-friendly desktop application for downloading YouTube videos and audio with a sleek dark-themed interface.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- **🎥 Video & Audio Downloads**: Download videos in various resolutions or extract audio only
- **🎨 Modern UI**: Beautiful dark-themed interface built with CustomTkinter
- **📊 Real-time Progress**: Live download progress with speed and ETA indicators
- **🔍 Smart Analysis**: Automatically analyzes video information and available formats
- **📂 Custom Output**: Choose your preferred download location
- **🎯 Quality Selection**: Pick from available video resolutions and audio bitrates
- **⚡ Fast & Reliable**: Uses yt-dlp for robust video downloading
- **🖥️ Cross-platform**: Works on Windows, macOS, and Linux

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/bc7c2d86-ca4f-4040-8c25-153a9723f5ee)

### Main Interface
The application features a clean, modern interface with organized sections for URL input, download path selection, and quality options.

### Video Analysis
After entering a YouTube URL, the app analyzes the video and displays:
- Video title and uploader
- Duration and view count
- Available quality options with file sizes

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

```bash
pip install customtkinter yt-dlp
```

## 📋 Requirements.txt

Create a `requirements.txt` file with the following content:

```
customtkinter>=5.2.0
yt-dlp>=2023.1.6
```

## 🎯 Usage

1. **Run the Application**
   ```bash
   python youtube_downloader.py
   ```

2. **Enter YouTube URL**
   - Paste your YouTube video URL in the input field
   - Click "🔍 Analyze Video" to fetch video information

3. **Choose Settings**
   - Select format type: Video or Audio only
   - Pick your preferred quality/resolution
   - Set download location (optional)

4. **Download**
   - Click "⬇️ Download Now" to start downloading
   - Monitor progress in real-time

## 🛠️ Technical Details

### Built With

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)**: Modern UI framework for Python
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: Robust YouTube downloader library
- **Threading**: Non-blocking UI during downloads
- **tkinter**: Base GUI framework

### Key Features Implementation

- **Async Operations**: Downloads run in separate threads to keep UI responsive
- **Progress Tracking**: Real-time progress updates with hooks
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Format Selection**: Dynamic quality options based on available formats
- **Responsive Design**: Scrollable interface that adapts to content

## 📁 Project Structure

```
youtube-downloader-pro/
│
├── youtube_downloader.py    # Main application file
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── screenshots/            # Application screenshots (optional)
```

## ⚙️ Configuration

The application automatically configures itself with:
- Dark theme appearance
- Blue color scheme
- Default download location (current directory)
- Optimal window sizing (900x700, minimum 800x600)

## 🐛 Troubleshooting

### Common Issues

1. **"Analysis Failed" Error**
   - Verify the YouTube URL is correct and accessible
   - Check your internet connection
   - Some videos may be region-locked or private

2. **Download Errors**
   - Ensure you have write permissions to the download directory
   - Check available disk space
   - Some videos may have download restrictions

3. **Module Import Errors**
   - Install required dependencies: `pip install customtkinter yt-dlp`
   - Ensure Python version is 3.7 or higher

### Performance Tips

- Close other bandwidth-intensive applications during downloads
- Choose lower quality options for faster downloads
- Ensure stable internet connection for large files

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test on multiple platforms when possible
- Update documentation for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Users are responsible for ensuring they have the right to download and use any content.

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - The powerful backend that makes downloads possible
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - For the beautiful modern UI components
- **YouTube** - For providing the content platform

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) section for existing solutions
2. Create a new issue with detailed information about your problem
3. Include your Python version, OS, and error messages

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
  - Video and audio download support
  - Modern CustomTkinter interface
  - Real-time progress tracking
  - Quality selection options

---

**Made with ❤️ for the YouTube community**

*Star ⭐ this repository if you found it helpful!*
