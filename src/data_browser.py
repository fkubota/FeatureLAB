'''
data_browser
'''

import sys
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
import pickle



feat_name = ['zcr','energy','energy_entropy','spectral_centroid','spectral_spread','spectral_entropy','spectral_flux','spectral_rolloff',
             'mfcc_1','mfcc_2','mfcc_3','mfcc_4','mfcc_5','mfcc_6','mfcc_7','mfcc_8','mfcc_9','mfcc_10','mfcc_11','mfcc_12','mfcc_13',
             'chroma_1','chroma_2','chroma_3','chroma_4','chroma_5','chroma_6','chroma_7','chroma_8','chroma_9','chroma_10','chroma_11','chroma_12','chroma_std']


class data_browser(QG.QWidget):
    def __init__(self, parent=None):
        super(data_browser, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.setWindowTitle("Data Browser")

        self.btn_data0 = QG.QPushButton('add Data')

        # self.table = QG.QTableWidget()
        # self.table.horizontalHeader().setResizeMode(0, QG.QHeaderView.Stretch)
        # self.table.setColumnCount(1)
        # self.table.setHorizontalHeaderLabels(['path'])
        # header = self.table.horizontalHeader()
        # header.setResizeMode(0, QG.QHeaderView.Stretch)

        self.lv = QG.QListView()
        self.model = QG.QStandardItemModel(self.lv)
        self.lv.setModel(self.model)

        self.vbox= QG.QVBoxLayout()
        self.vbox.addWidget(self.lv)
        self.vbox.addWidget(self.btn_data0)
        self.setLayout(self.vbox)



def main():
    app = QG.QApplication(sys.argv)

    ui =data_browser()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
