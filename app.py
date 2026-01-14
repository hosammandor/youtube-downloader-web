import streamlit as st
from yt_dlp import YoutubeDL
import os

# إنشاء فولدر التحميل لو مش موجود
if not os.path.exists("downloads"):
    os.makedirs("downloads")

st.set_page_config(page_title="YouTube Downloader Pro", page_icon="📺", layout="centered")
st.title("📺 YouTube Downloader Pro")

# 1. إدخال رابط اليوتيوب
url = st.text_input("Paste YouTube URL here:")

# 2. اختيار الصيغة
format_choice = st.selectbox("Select Format:", ["Video (MP4)", "Audio (MP3)"])

# زر البدء
if st.button("Download"):
    if not url:
        st.warning("⚠ Please paste a valid YouTube URL.")
    else:
        status_text = st.empty()  # مكان لعرض حالة التحميل
        progress_bar = st.progress(0)  # شريط تقدم
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded_bytes = d.get('downloaded_bytes', 0)
                if total_bytes:
                    progress = int(downloaded_bytes / total_bytes * 100)
                    progress_bar.progress(progress)
            elif d['status'] == 'finished':
                progress_bar.progress(100)
                status_text.success("✅ Download finished!")

        try:
            # إعدادات yt-dlp
            output_path = "downloads/%(title)s.%(ext)s"
            ydl_opts = {
                'outtmpl': output_path,
                'restrictfilenames': True,
                'progress_hooks': [progress_hook],
            }

            if format_choice == "Audio (MP3)":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:  # Video MP4
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                })

            # التحميل
            with YoutubeDL(ydl_opts) as ydl:
                status_text.info("🔄 Fetching video info and downloading...")
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

                # تعديل الامتداد لو MP3
                if format_choice == "Audio (MP3)":
                    base, _ = os.path.splitext(file_path)
                    file_path = base + ".mp3"

            # زر تحميل للمستخدم
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    st.download_button(
                        label=f"📥 Download {format_choice}",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                    )
            else:
                st.error("❌ File processing failed.")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
