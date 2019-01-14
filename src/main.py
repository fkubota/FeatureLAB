"""
MFCC_analysis
"""

import sys
import os
import psutil
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pickle
from src import data_browser as db, scatter_mod as sctr


class mfcc_analysis(QG.QMainWindow):
    def __init__(self, parent=None):
        self.feat_names = ['zcr','energy','energy_entropy','spectral_centroid','spectral_spread','spectral_entropy','spectral_flux','spectral_rolloff',
                            'mfcc_1','mfcc_2','mfcc_3','mfcc_4','mfcc_5','mfcc_6','mfcc_7','mfcc_8','mfcc_9','mfcc_10','mfcc_11','mfcc_12','mfcc_13',
                            'chroma_1','chroma_2','chroma_3','chroma_4','chroma_5','chroma_6','chroma_7','chroma_8','chroma_9','chroma_10','chroma_11','chroma_12','chroma_std']

        # scatter
        self.scatter = -1
        self.w_scatterV = []

        # data_browser
        self.data_id = -1
        self.dataV = []
        self.data_basenameV = []

        # constructor
        super(mfcc_analysis, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.setWindowTitle('MFCC analysis')
        self.resize(1000, 500)
        self.move(200, 100)

        # tool bar
        self.add_scatter = QG.QAction(QG.QIcon('./icon_file/plus_icon2.png'), 'scatter', self)
        self.add_scatter.triggered.connect(self.show_scatter)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.add_scatter)

        # statusbar
        self.mem = psutil.virtual_memory()
        mem0 = self.mem.total/10**9
        mem1 = self.mem.used/10**9
        self.statusBar().showMessage('memory: {}/{} GB'.format(mem1, mem0))
        self.pbur = QG.QProgressBar()
        self.pbur.setFixedHeight(10)
        self.statusBar().addPermanentWidget(self.pbur)

        # timer
        self.timer = QC.QTimer(self)
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(500)

        # multi window
        self.mdi = QG.QMdiArea(self)
        self.setCentralWidget(self.mdi)

        # data browser
        self.data_browser = db.data_browser(self)
        self.data_browser.btn_data0.clicked.connect(self.get_data)


        #layout
        self.mdi.addSubWindow(self.data_browser)


        # self.plot()
        self.get_data()


    def timer_event(self):
        self.mem = psutil.virtual_memory()
        mem0 = self.mem.total/10**9
        mem1 = self.mem.used/10**9
        self.statusBar().showMessage('memory: {:.3f}/{:.3f} GB'.format(mem1, mem0))
        # self.statusBar().showMessage()
        self.pbur.setValue(mem1/mem0* 100)
        self.repaint()


    def get_data(self):
        self.data_id += 1
        # data_path = QG.QFileDialog.getOpenFileName(self, 'Open File', '/home/')
        # data_path = '/home/fkubota/Project/ALSOK/data/稲成ビルFeat/kubota/feat_正常音.pkl'
        # data_path = '/home/fkubota/Project/Yokogawa/data/feat/徳山201809/mfcc-0502/Yokogawa_mfcc-0502_20180831_085430.pkl'
        self.data_path = '/home/fkubota/MyData/030_GoogleDrive/Python/pyfile/my_APP/MFCC_analysis/data/sample.pkl'
        with open(self.data_path, mode='rb') as f:
            self.feat = pickle.load(f)
        self.feat = self.feat['data']
        self.dataV.append(self.feat)
        self.data_basenameV.append(os.path.basename(self.data_path))
        # self.data_browser.table.setRowCount(self.data_id+1)
        # self.data_browser.table.setItem(0, self.data_id, QG.QTableWidgetItem(self.data_path))
        self.item = QG.QStandardItem(self.data_path)
        self.data_browser.model.appendRow(self.item)


        self.update_scatter_cb_edited()



    def show_scatter(self):
        self.scatter += 1
        self.w_scatterV.append(sctr.scatter_mod(self))
        w_scatter = self.w_scatterV[len(self.w_scatterV) -1]
        w_scatter.id = self.scatter
        w_scatter.setWindowTitle('scatter: ' + str(w_scatter.id))

        # overload method
        w_scatter.setting_update = self.setting_update_edited
        w_scatter.change_color = self.change_color_edited
        w_scatter.update_scatter_cb = self.update_scatter_cb_edited

        self.mdi.addSubWindow(w_scatter)
        w_scatter.add_data()
        self.update_scatter_cb_edited()
        w_scatter.show()

    def setting_update_edited(self):
        tab = self.sender().parent()
        scatter = tab.plot_scatter
        id = tab.id
        step = int(tab.le_scatter0.text())
        feat0 = self.feat[::step, int(tab.cb_scatter0.currentIndex())]
        feat1 = self.feat[::step, int(tab.cb_scatter1.currentIndex())]
        scatter.setPoints(feat0, feat1, brush=tab.color+'32')

    def change_color_edited(self):
        btn = self.sender()
        tab = self.sender().parent()
        color = QG.QColorDialog.getColor()
        tab.color = color.name()
        btn.setStyleSheet("background-color: "+ tab.color)


    def update_scatter_cb_edited(self):
        for scatter_idx in range(len(self.w_scatterV)):
            w_scatter = self.w_scatterV[scatter_idx]
            for tab_idx in range(len(w_scatter.tabV)):
                w_scatter.tabV[tab_idx].cb_scatter2.clear()
                w_scatter.tabV[tab_idx].cb_scatter2.addItems(self.data_basenameV)
                w_scatter.tabV[tab_idx].cb_scatter2.update()

            # self.w_scatterV[idx].cb_scatter2.clear()
            # self.w_scatterV[idx].cb_scatter2.addItems(self.data_basenameV)
            # self.w_scatterV[idx].cb_scatter2.update()


def main():
    app = QG.QApplication(sys.argv)

    ui =mfcc_analysis()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
