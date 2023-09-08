import subprocess
import tkinter as tk
import os
from yt_dlp import YoutubeDL

def download_files(urls, extension):
    try:
        if urls == "":
            status_text.set("Favor Inserir Link válido!")
            return

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(urls, download=False)
            video_url = info['formats'][0]['url']
            title = info['title']

            status_text.set("Download Iniciado!")
            window.update()

            if extension == "mp4":
                ydl.download([urls])
                
            elif extension == "mp3":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                ydl.download([urls])

            else:
                ydl.download([urls])
                input_file = f"{title}.mp4"
                output_file = f"{title}.vob"

                # Define as opções de conversão
                options = [
                    '-i', input_file,
                    '-target', 'ntsc-dvd',
                    '-q:v', '0',
                    '-q:a', '0',
                    output_file
                ]

                status_text.set("Conversão Iniciada!")
                window.update()
                # Executa o comando ffmpeg
                subprocess.call(['ffmpeg'] + options)
                # Remove o arquivo original
                os.remove(input_file)

            status_text.set("Download concluído!")       
            window.update()
    
    except Exception as e:
        status_text.set(f"Erro: {str(e)}")

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

    file_extension = tk.OptionMenu(window, selected_option, "mp4", "vob", "mp3")
    file_extension.grid(row=3, column=2, sticky="ew", pady=10)

    button_download = tk.Button(window, text="Baixar", command=lambda: download_files(field_urls.get(), selected_option.get()))
    button_download.grid(row=4, column=2, sticky="ew", pady=(0, 10))

    status_text = tk.StringVar()
    status_text.set("...")

    status_label = tk.Label(window, textvariable=status_text)
    status_label.grid(row=5, column=2, sticky="n", pady=(0, 0))

    window.mainloop()
