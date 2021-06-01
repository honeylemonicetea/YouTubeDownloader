"""
INTERFACE HERE
Add:
- Text field to paste the link
- Download button
- Radio buttons to choose quality
- Pop up window to notify the user about the completion and location of the download

Further notes:
for PyQt5 version, add:
 - Video thumbnail


"""
import tkinter as tk
import pytube as pt
import tkinter.messagebox as tkm
import tkinter.filedialog as tfd


root = tk.Tk()
root.geometry('600x500')
root.title('YouTube Video Downloader')

default_save_location =  './Downloads'

# FUNCTIONS
def temporary():
    video_url = url_field.get()
    quality= variant.get()

    # video object
    video = pt.YouTube(video_url)

    video_title = video.title
    if quality != 'Audio Only':
        stream = video.streams.get_by_resolution(quality)
    elif quality == 'Audio Only':
        stream  = video.streams.get_audio_only()
    stream.download(default_save_location)
    tkm.showinfo('Download complete', f'The video: {video_title} has been downloaded')

def change_save_location():
    global default_save_location
    new_location  = tfd.askdirectory()
    print(new_location)
    default_save_location = new_location




# WIDGETS

options_frame = tk.Frame(root)

url_label = tk.Label(options_frame, text='Insert the link to the YouTube video here',  font=('Helvetica', 15, 'bold'))
url_label.pack(pady=10)
url_field = tk.Entry(options_frame, width=20)
url_field.pack(pady=10)

qulity_frame = tk.Frame(options_frame)
# Download options
variant = tk.StringVar(root, value='1')
option_1 = tk.Radiobutton(options_frame, text='360p', variable = variant, value='360p')
option_1.pack()
option_2 = tk.Radiobutton(options_frame, text='480p', variable = variant, value='480p')
option_2.pack()
option_3 = tk.Radiobutton(options_frame, text='720p', variable = variant, value='720p')
option_3.pack()
option_4 = tk.Radiobutton(options_frame, text='Audio Only', variable = variant, value='Audio Only')
option_4.pack()
change_dir = tk.Button(options_frame, text='Change Download Location', command = change_save_location)
change_dir.pack(pady=10)
qulity_frame.pack()

download_button = tk.Button(options_frame, text='Download', width=20, height=2, bg='#E20338', fg='white', font=('Helvetica', 15, 'bold'), command=temporary)
download_button.pack(pady=20)

options_frame.pack(pady=100)




root.mainloop()
