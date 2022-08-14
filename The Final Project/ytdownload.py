from PyQt5 import QtCore, QtGui, QtWidgets
import pytube as pt
import requests
import os
import time
# import moviepy.editor as mpe
class Ui_MainWindow(object):
    def __init__(self):
        self.video_url = ''
        self.video_title = ''
        self.video_size = ''
        self.video_length = ''
        self.video_image = ''
        self.save_directory = ''
        self.resolution = ''
        self.downloaded = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 778)
        MainWindow.setStyleSheet("background: aliceblue")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        self.centralwidget.setObjectName("centralwidget")
        self.video_image_lbl = QtWidgets.QLabel(self.centralwidget)
        self.video_image_lbl.setGeometry(QtCore.QRect(110, 70, 401, 261))
        self.video_image_lbl.setStyleSheet("border-radius: 8px")
        self.video_image_lbl.setText("")
        self.video_image_lbl.setPixmap(QtGui.QPixmap("yt_placeholder.jpg"))
        self.video_image_lbl.setScaledContents(True)
        self.video_image_lbl.setObjectName("video_image_lbl")
        self.video_title_lbl = QtWidgets.QLabel(self.centralwidget)
        self.video_title_lbl.setGeometry(QtCore.QRect(530, 80, 341, 131))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(16)
        self.video_title_lbl.setFont(font)
        self.video_title_lbl.setScaledContents(True)
        self.video_title_lbl.setWordWrap(True)
        self.video_title_lbl.setObjectName("video_title_lbl")
        self.video_length_lbl = QtWidgets.QLabel(self.centralwidget)
        self.video_length_lbl.setGeometry(QtCore.QRect(530, 230, 331, 51))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(16)
        self.video_length_lbl.setFont(font)
        self.video_length_lbl.setObjectName("video_length_lbl")
        self.file_size_lbl = QtWidgets.QLabel(self.centralwidget)
        self.file_size_lbl.setGeometry(QtCore.QRect(530, 280, 311, 41))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(16)
        self.file_size_lbl.setFont(font)
        self.file_size_lbl.setObjectName("file_size_lbl")
        self.quality_options_box = QtWidgets.QGroupBox(self.centralwidget)
        self.quality_options_box.setGeometry(QtCore.QRect(110, 450, 131, 151))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(9)
        self.quality_options_box.setFont(font)
        self.quality_options_box.setObjectName("quality_options_box")
        self.lq_radio_btn = QtWidgets.QRadioButton(self.quality_options_box, toggled = lambda : self.update_size('360p'))
        self.lq_radio_btn.setGeometry(QtCore.QRect(10, 30, 95, 20))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(9)
        self.lq_radio_btn.setFont(font)
        self.lq_radio_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lq_radio_btn.setObjectName("lq_radio_btn")
        self.hq_radio_btn = QtWidgets.QRadioButton(self.quality_options_box, toggled = lambda : self.update_size('720p'))
        self.hq_radio_btn.setGeometry(QtCore.QRect(10, 60, 95, 20))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(9)
        self.hq_radio_btn.setFont(font)
        self.hq_radio_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hq_radio_btn.setObjectName("hq_radio_btn")

        # self.mq_radio_btn = QtWidgets.QRadioButton(self.quality_options_box, toggled = lambda : self.update_size('480p'))
        # self.mq_radio_btn.setGeometry(QtCore.QRect(10, 60, 95, 20))
        # font = QtGui.QFont()
        # font.setFamily("ALSSchlangeslab-Bold")
        # font.setPointSize(9)
        # self.mq_radio_btn.setFont(font)
        # self.mq_radio_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.mq_radio_btn.setObjectName("mq_radio_btn")
        self.audio_only_radio_btn = QtWidgets.QRadioButton(self.quality_options_box, toggled = lambda : self.update_size('Audio Only'))
        self.audio_only_radio_btn.setGeometry(QtCore.QRect(10, 90, 95, 20))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(9)
        self.audio_only_radio_btn.setFont(font)
        self.audio_only_radio_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.audio_only_radio_btn.setObjectName("audio_only_radio_btn")

        # radio btn group
        self.radio_btn_group = QtWidgets.QButtonGroup()
        self.radio_btn_group.addButton(self.lq_radio_btn)
        # self.radio_btn_group.addButton(self.mq_radio_btn)
        self.radio_btn_group.addButton(self.hq_radio_btn)
        self.radio_btn_group.addButton(self.audio_only_radio_btn)
        self.radio_btn_group.setExclusive(True)



        self.contol_box = QtWidgets.QGroupBox(self.centralwidget)
        self.contol_box.setGeometry(QtCore.QRect(270, 450, 521, 151))
        self.contol_box.setTitle("")
        self.contol_box.setObjectName("contol_box")
        self.dwnld_progress_bar = QtWidgets.QProgressBar(self.contol_box)
        self.dwnld_progress_bar.setGeometry(QtCore.QRect(20, 110, 491, 21))
        self.dwnld_progress_bar.setProperty("value", 0)
        self.dwnld_progress_bar.setObjectName("dwnld_progress_bar")
        self.change_dir_btn = QtWidgets.QPushButton(self.contol_box, clicked = lambda : self.change_dir())
        self.change_dir_btn.setGeometry(QtCore.QRect(20, 20, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.change_dir_btn.setFont(font)
        self.change_dir_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.change_dir_btn.setStyleSheet("border-radius: 9px;\n"
"background-color: #B5FBDD;\n"
"border: 1px solid #45D09E")
        self.change_dir_btn.setObjectName("change_dir_btn")
        self.undo_load_btn = QtWidgets.QPushButton(self.contol_box, clicked = lambda :self.reset_load())
        self.undo_load_btn.setGeometry(QtCore.QRect(290, 20, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.undo_load_btn.setFont(font)
        self.undo_load_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.undo_load_btn.setStyleSheet("border-radius: 9px;\n"
"background-color: #B5FBDD;\n"
"border: 1px solid #45D09E")
        self.undo_load_btn.setObjectName("undo_load_btn")
        self.url_input = QtWidgets.QLineEdit(self.centralwidget)
        self.url_input.setGeometry(QtCore.QRect(110, 370, 521, 51))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(14)
        self.url_input.setFont(font)
        self.url_input.setStyleSheet("border-radius: 9px;\n"
"padding: 5px 10px;\n"
"background-color: white;\n"
"border: 1px solid #AFCFEA")
        self.url_input.setObjectName("url_input")
        self.load_btn = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.load_video())
        self.load_btn.setGeometry(QtCore.QRect(660, 370, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.load_btn.setFont(font)
        self.load_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_btn.setStyleSheet("border-radius: 9px;\n"
"background-color: #B5FBDD;\n"
"border: 1px solid #45D09E;\n"
"")
        self.load_btn.setObjectName("load_btn")
        self.download_btn = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.download_file())
        self.download_btn.setGeometry(QtCore.QRect(210, 640, 441, 61))
        font = QtGui.QFont()
        font.setFamily("ALSSchlangeslab-Bold")
        font.setPointSize(14)
        self.download_btn.setFont(font)
        self.download_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.download_btn.setStyleSheet("border-radius: 9px;\n"
"background-color: #FF6A61;\n"
"border: 1px solid #E20338")
        self.download_btn.setObjectName("download_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.video_title_lbl.setText(_translate("MainWindow", "Video Title: Unknown"))
        self.video_length_lbl.setText(_translate("MainWindow", "Video Length: 00:00"))
        self.file_size_lbl.setText(_translate("MainWindow", ""))
        self.quality_options_box.setTitle(_translate("MainWindow", "Quality Options"))
        self.lq_radio_btn.setText(_translate("MainWindow", "360p"))
        self.hq_radio_btn.setText(_translate("MainWindow", "720p"))
        # self.mq_radio_btn.setText(_translate("MainWindow", "480p"))
        self.audio_only_radio_btn.setText(_translate("MainWindow", "Audio Only"))
        self.change_dir_btn.setText(_translate("MainWindow", "Change Download Location"))
        self.undo_load_btn.setText(_translate("MainWindow", "Undo Load"))
        self.url_input.setPlaceholderText(_translate("MainWindow", "Input the link here"))
        self.load_btn.setText(_translate("MainWindow", "LOAD"))
        self.download_btn.setText(_translate("MainWindow", "Download"))

    def load_video(self):
        try:
            video_url = self.url_input.text()
            self.video_url = video_url

        #     the video object
            video = pt.YouTube(video_url)
            title = video.title.replace('?',' ')
            if len(title) > 50:
                self.video_title = title[0:50] + '...'
            else:
                self.video_title = title

            raw_length = video.length
            self.video_length = time.strftime('%M:%S', time.gmtime(raw_length))
            thumbnail = requests.get(video.thumbnail_url)
            with open(f'{self.video_title}.jpg', 'wb+') as image:
                image.write(thumbnail.content)
            self.video_image = f'{self.video_title}.jpg'

            self.update_labels()

        except Exception:
            pass

    def update_labels(self):
        self.video_image_lbl.setPixmap(QtGui.QPixmap(self.video_image))
        self.video_title_lbl.setText(f'Video Title:\n{self.video_title}')
        self.video_length_lbl.setText(f'Video Length: {self.video_length}')


    def download_file(self):
        try:
            video_url = self.url_input.text()
            os.remove(self.video_image)
            if len(self.resolution) > 0:

                if self.resolution == '480p':
                    video = pt.YouTube(video_url, on_progress_callback=self.progress)
                    stream_video = video.streams.filter(res='480p')[0]
                    stream_video.download(self.save_directory, 'vid.mp4')
                    self.dwnld_progress_bar.setValue(0)
                    audio = pt.YouTube(video_url, on_progress_callback=self.progress)
                    stream_audio = audio.streams.get_audio_only()
                    stream_audio.download(self.save_directory, 'aud.mp3')

                    self.conv_warning()
                    self.dwnld_progress_bar.setValue(0)

                    self.merge(f'vid.mp4', f'aud.mp3', f'{self.save_directory}/{self.video_title} {self.resolution}.mp4')
                    os.remove(f'vid.mp4')
                    os.remove(f'aud.mp3')

                    self.download_complete()
                else:
                    video = pt.YouTube(video_url, on_progress_callback=self.progress,
                                       on_complete_callback=self.download_complete)
                    if self.resolution == 'Audio Only':
                        stream = video.streams.get_audio_only()
                        stream.download(self.save_directory, f'{self.video_title} {self.resolution}.mp3')
                    else:
                        stream = video.streams.get_by_resolution(self.resolution)
                        stream.download(self.save_directory, f'{self.video_title} {self.resolution}.mp4')
        except Exception:
            pass

    def merge(self,vidname, audname, outname, fps=25):

        print('hey')
        my_clip = mpe.VideoFileClip(vidname)
        print('my clip')
        audio_background = mpe.AudioFileClip(audname)
        print('audio')
        final_clip = my_clip.set_audio(audio_background)
        print('final')
        final_clip.write_videofile(outname, fps=fps, logger='bar')
        print('final')

    def download_complete(self):

        dwnld_complete = QtWidgets.QMessageBox()
        dwnld_complete.setWindowTitle('Download Complete')
        dwnld_complete.setText(f'The file {self.video_title} has been downloaded and saved in: {self.save_directory}')
        dwnld_complete.setIcon(QtWidgets.QMessageBox.Information)

        x = dwnld_complete.exec_()

    def conv_warning(self):
        dwnld_complete = QtWidgets.QMessageBox()
        dwnld_complete.setWindowTitle('Download Complete')
        dwnld_complete.setText('Your file has been downloaded and needs to be converted. It may take some time')
        dwnld_complete.setIcon(QtWidgets.QMessageBox.Information)

        x = dwnld_complete.exec_()

    def update_size(self, resolution):

        #     the video object
        try:
            self.resolution = resolution
            video = pt.YouTube(self.video_url)
            if resolution != '480p' and resolution != 'Audio Only':
                stream = video.streams.get_by_resolution(resolution)
                size_bytes = stream.filesize
            elif resolution == '480p':
                stream = video.streams.filter(res='480p')[0]
                size_bytes = stream.filesize

            else:
                stream = video.streams.get_audio_only()
                size_bytes = stream.filesize
            size_megabytes = size_bytes / (1024**2)

            self.video_size = round(size_megabytes, 2) #the size is in bytes, need to convert
            self.file_size_lbl.setText(f'File Size: {self.video_size} MB')
        except Exception:
            pass

    def change_dir(self):
        file_dialog = QtWidgets.QFileDialog()
        new_dir = file_dialog.getExistingDirectory()
        self.save_directory = new_dir

    def reset_load(self):
        self.video_length = '00:00'
        self.video_size = '0'
        self.video_title = ''
        self.video_image = 'yt_placeholder.jpg'
        self.video_url = ''
        self.url_input.clear()
        self.file_size_lbl.setText('')
        self.update_labels()

        #  set the radio btn group unexclusive
        self.radio_btn_group.setExclusive(False)
        self.lq_radio_btn.setChecked(False)
        self.mq_radio_btn.setChecked(False)
        self.hq_radio_btn.setChecked(False)
        self.audio_only_radio_btn.setChecked(False)
        self.radio_btn_group.setExclusive(True)

        self.dwnld_progress_bar.setValue(0)

    def progress(self, stream, data_chunk, bytes_remaining):

        percent = ((stream.filesize - bytes_remaining) / stream.filesize) * 100
        # self.downloaded += data_chunk

        self.dwnld_progress_bar.setValue(round(percent))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
# dkld
# dld
