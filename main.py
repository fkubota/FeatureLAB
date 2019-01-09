"""
MFCC_analysis
"""

import sys
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
import pickle


class play_music(QG.QMainWindow):
    def __init__(self, parent=None):
        # app = QG.QApplication(sys.argv)
        super(play_music, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.resize(1000, 500)

        # widget
        self.w = QG.QWidget(self)
        self.setCentralWidget(self.w)

        # グラフウィンドウ
        self.w_plot = pg.PlotWidget(self)
        self.plotitem0 = self.w_plot.getPlotItem()
        self.plotitem0.setYRange(-30000, 30000)
        self.curve_wave = self.plotitem0.plot()

        # label
        self.lbl0 = QG.QLabel(self)
        self.lbl0.setText('hello')

        # button
        self.btn0 = QG.QPushButton('play')
        self.btn0.setFixedWidth(60)
        self.btn0.clicked.connect(self.play)
        # layout
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addWidget(self.w_plot)
        self.vbox0.addWidget(self.lbl0)
        self.vbox0.addWidget(self.btn0)
        self.w.setLayout(self.vbox0)



    def play(self):
        wav_path = '/home/fkubota/MyData/040_Programming/010_Python/' \
                   'Python/020_APP/MFCC_analysis/data/test/window_broken.wav'

        BUFFER_SIZE = 1024 * 4

        # 取り込み
        wav_file = wave.open( wav_path, 'rb')
        wav_file_data = wave.open(wav_path, 'rb')

        # 数値に変換
        # self.data = wav_file.readframes(wav_file_data.getnframes())
        # self.data = np.fromstring(self.data, dtype=np.int16)

        def callback(in_data, frame_count, time_info, status):
            pass


        # stream の作成
        p = pa.PyAudio()
        stream = p.open (
            format = p.get_format_from_width ( wav_file . getsampwidth ()) ,
            channels = wav_file.getnchannels () ,
            rate = wav_file.getframerate () ,
            output = True,
            stream_callback=callback
        )

        start = 0
        remain = wav_file.getnframes ()
        while remain > 0:
            # x = self.data[start:start+BUFFER_SIZE]
            # print(self.data.shape)
            # self.curve_wave.setData(x)
            buf = wav_file.readframes ( min ( BUFFER_SIZE , remain ))

            stream.write (buf)
            # print('OK')

            data = np.frombuffer(buf)
            # self.curve_wave.setData(data)

            # self.lbl0.setText('OK')


            remain -= BUFFER_SIZE
            start += BUFFER_SIZE
            # print('ok')

        stream.close ()
        p.terminate ()
        wav_file.close ()
















def main():
    app = QG.QApplication(sys.argv)

    ui = play_music()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
