import streamlit as st
from yt_dlp import YoutubeDL

st.title("YouTube Downloader")

# حقل لصق رابط الفيديو
url = st.text_input("Paste YouTube URL:")

# اختيار صيغة الفيديو
format_choice = st.selectbox("Choose format:", ["MP4", "MP3"])

if st.button("Generate Direct Link"):
    if not url:
        st.warning("Please paste a valid YouTube URL")
    else:
        try:
            ydl_opts = {}
            if format_choice == "MP3":
                # إعدادات تنزيل صوت فقط
                ydl_opts = {
                    'format': 'bestaudio',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
                }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                st.success("Direct link generated!")
                st.write(info_dict['url'])

        except Exception as e:
            st.error(f"Error: {e}")
