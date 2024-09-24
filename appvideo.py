#pip install streamlit
#pip install pytube

import pytube
import streamlit as st

class YoutubeDownloader:
    @staticmethod
    def onProgress(stream=None, chunk=None, remaining=None):
        file_size = stream.filesize / 1000000  # Convertir a MB
        file_downloaded = file_size - (remaining / 1000000)
        st.progress(file_downloaded / file_size)

    def __init__(self, url):
        self.url = url
        try:
            # Usamos 'on_progress_callback' en lugar de 'on_progress'
            self.youtube = pytube.YouTube(self.url, on_progress_callback=YoutubeDownloader.onProgress)
        except Exception as e:
            st.error(f"Error al inicializar el video: {e}")
        self.stream = None
  
    def showTitle(self):
        try:
            st.write(f"**Título:** {self.youtube.title}")
            self.showStreams()
        except Exception as e:
            st.error(f"Error al obtener el título del video: {e}")

    def showStreams(self):
        try:
            streams = self.youtube.streams
            stream_options = [
                f"Resolución: {stream.resolution or 'N/A'} / FPS: {getattr(stream, 'fps', 'N/A')} / Tipo: {stream.mime_type}"
                for stream in streams
            ]
            choice = st.selectbox("Selecciona una opción", stream_options)
            self.stream = streams[stream_options.index(choice)]
        except Exception as e:
            st.error(f"Error al obtener streams: {e}")

    def getFileSize(self):
        try:
            file_size = self.stream.filesize / 1000000
            return round(file_size, 1)
        except Exception as e:
            st.error(f"Error al obtener el tamaño del archivo: {e}")
            return None
    
    def getPermissionToContinue(self, file_size):
        try:
            st.write(f"**Título:** {self.youtube.title}")
            st.write(f"**Autor:** {self.youtube.author}")
            st.write(f"**Tamaño:** {file_size:.2f} MB")
            st.write(f"**Resolución:** {self.stream.resolution or 'N/A'}")
            st.write(f"**FPS:** {getattr(self.stream, 'fps', 'N/A')}")

            if st.button("Descargar"):
                self.download()
            else:
                st.warning("Descarga cancelada")
        except Exception as e:
            st.error(f"Error al mostrar la información del video: {e}")

    def download(self):
        try:
            self.stream.download()
            st.success("Descarga completada")
        except Exception as e:
            st.error(f"Error al descargar: {e}")


if __name__ == "__main__":
    st.title("Descargador de videos de YouTube")
    url = st.text_input("Ingresa la URL del video de YouTube")
    if url:
        downloader = YoutubeDownloader(url)
        downloader.showTitle()
        if downloader.stream:
            file_size = downloader.getFileSize()
            if file_size:
                downloader.getPermissionToContinue(file_size)
