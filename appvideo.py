import streamlit as st
import pytube
from urllib.error import HTTPError

class YoutubeDownloader:
  def __init__(self, url):
    self.url = url
    self.youtube = pytube.YouTube(self.url, on_progress_callback=YoutubeDownloader.onProgress)
    self.stream = None
  
  def showTitle(self):
    st.write(f"**Título:** {self.youtube.title}")
    self.showStreams()

  def showStreams(self):
    streams = self.youtube.streams
    stream_options = [
        f"Resolución:{stream.resolution or 'N/A'} / FPS: {getattr(stream, 'fps', 'N/A')} / Tipo: {stream.mime_type}"
        for stream in streams
    ]
    choice = st.selectbox("Selecciona una opción", stream_options)
    self.stream = streams[stream_options.index(choice)]

    def getFileSize(self):
      file_size = self.stream.filesize / 1000000
      return round(file_size, 1)
    
    def getPermissionToContinue(self, file_size):
      st.write(f"**Título:{self.youtube.title}")
      st.write(f"**Autor:{self.youtube.author}")
      st.write(f"**Tamaño:{file_size:.2f} MB")
      st.write(f"**Resolución:{self.stream.resolution or 'N/A'}")
      st.write(f"**FPS:{getattr(self.stream, 'fps', 'N/A')}")

      if st.button("Descargar"):
        self.download()
      else:
        st.warning("Descarga cancelada")

    def download(self):
      try:
        self.stream.download()
        st.success("Descarga completada")
      except Exception as e:
        st.error(f"Error al descargar: {e}")

    @staticmethod
    def onProgress(stream=None, chunk=None, remaining=None):
      file_size = stream.filesize / 1000000
      file_downloaded = file_size - (remaining / 1000000)
      st.progress(file_downloaded / file_size)

if __name__ == "__main__":
  st.title("Descargador de videos de YouTube")
  url = st.text_input("Ingresa la URL del video de YouTube")
  if url:
      downloader = YoutubeDownloader(url)
      downloader.showTitle()
      if downloader.stream:
          file_size = downloader.getFileSize()
          downloader.getPermissionToContinue(file_size)