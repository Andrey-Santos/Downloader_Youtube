import os
import tkinter as tk
from pytube import YouTube
from moviepy.editor import VideoFileClip

def download_files(urls, extension):
    if urls != "":
        yt = YouTube(urls) 
        status_text.set("Download Iniciado!")
        window.update()

        if extension == "avi":
            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
            video_path = stream.download()
                 
            # Converter para AVI usando moviepy
            output_path = video_path.replace(".mp4", ".avi")
            clip = VideoFileClip(video_path)
            status_text.set("Converção Iniciada!")
            window.update()
            clip.write_videofile(output_path, codec='libxvid')

            # Remover o arquivo de vídeo original
            clip.close()
            os.remove(video_path)
        else:
            yt.streams.filter(progressive=True, file_extension=extension).order_by('resolution').desc().first().download()

        status_text.set("Download concluído!")
    else:
        status_text.set("Favor Inserir Link válido!")


    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Drey Downloader")
    window.geometry("300x200")

    # Adiciona uma coluna extra vazia no início e no final da janela
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(4, weight=1)

    label_urls = tk.Label(window, text="Links para download")
    label_urls.grid(row=0, column=2, sticky="ew", pady=(20, 5))

    field_urls = tk.Entry(window)
    field_urls.grid(row=1, column=2, sticky="ew")

    selected_option = tk.StringVar(window)
    selected_option.set("mp4")  # Define a opção padrão selecionada

    file_extension = tk.OptionMenu(window, selected_option, "mp4", "avi", "mp3")
    file_extension.grid(row=3, column=2, sticky="ew", pady=10)

    button_download = tk.Button(window, text="Baixar", command=lambda: download_files(field_urls.get(), selected_option.get()))
    button_download.grid(row=4, column=2, sticky="ew", pady=(0, 10))

    status_text = tk.StringVar()
    status_text.set("...")

    status_label = tk.Label(window, textvariable=status_text)
    status_label.grid(row=5, column=2, sticky="n", pady=(0, 0))

    window.mainloop()