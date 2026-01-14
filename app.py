import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("📺 YouTube Downloader Pro")

# 1. إدخال الرابط
url = st.text_input("Paste YouTube URL here:")

# 2. اختيار الصيغة
format_choice = st.selectbox("Select Format:", ["Video (MP4)", "Audio (MP3)"])

# زر البدء
if st.button("Download"):
    if not url:
        st.warning("Please paste a valid YouTube URL.")
    else:
        status_text = st.empty() # مكان لعرض حالة التحميل
        status_text.info("Fetching video info...")
        
        try:
            # إعدادات المجلد المؤقت والاسم
            output_path = "downloads/%(title)s.%(ext)s"
            
            ydl_opts = {
                'outtmpl': output_path,
                'restrictfilenames': True, # لضمان أسماء ملفات آمنة
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
            else: # Video MP4
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                })

            # عملية التحميل
            with YoutubeDL(ydl_opts) as ydl:
                status_text.info("Downloading content to server... please wait.")
                info = ydl.extract_info(url, download=True)
                
                # الحصول على اسم الملف الذي تم تحميله
                file_path = ydl.prepare_filename(info)
                
                # تصحيح الامتداد في حالة MP3 لأن الاسم المبدئي قد لا يتغير مباشرة في المتغير
                if format_choice == "Audio (MP3)":
                    base, _ = os.path.splitext(file_path)
                    file_path = base + ".mp3"

            # عرض زر التحميل للمستخدم
            if os.path.exists(file_path):
                status_text.success("Ready for download!")
                with open(file_path, "rb") as file:
                    st.download_button(
                        label=f"📥 Download {format_choice}",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                    )
            else:
                st.error("File processing failed.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
