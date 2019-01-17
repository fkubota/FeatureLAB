"""
MFCC_analysis
"""

import sys
import os
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_path + '/../'))
import psutil
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pickle
import pyqtgraph as pg
from src import data_browser as db, scatter_mod as sctr, feature_plot_mod as fp, histogram_mod as histogram


class mfcc_analysis(QG.QMainWindow):
    def __init__(self, parent=None):
        self.feat_names = ['zcr','energy','energy_entropy','spectral_centroid','spectral_spread','spectral_entropy','spectral_flux','spectral_rolloff',
                            'mfcc_1','mfcc_2','mfcc_3','mfcc_4','mfcc_5','mfcc_6','mfcc_7','mfcc_8','mfcc_9','mfcc_10','mfcc_11','mfcc_12','mfcc_13',
                            'chroma_1','chroma_2','chroma_3','chroma_4','chroma_5','chroma_6','chroma_7','chroma_8','chroma_9','chroma_10','chroma_11','chroma_12','chroma_std']

        # scatter
        self.scatter = -1
        self.w_scatterV = []

        # feat_plot
        self.feat_plot = -1
        self.w_feat_plotV = []

        # hittgram
        self.hist = -1
        self.w_hist_plotV = []

        # data_browser
        self.data_id = -1
        self.dataV = []
        self.data_basenameV = []


        # constructor
        super(mfcc_analysis, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.setWindowTitle('MFCC analysis')
        self.resize(1000, 650)
        self.move(100, 100)

        # tool bar
        self.add_scatter = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'scatter', self)
        self.add_feat = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'feature', self)
        self.add_hist = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'feature', self)
        self.add_scatter.triggered.connect(self.show_scatter)
        self.add_feat.triggered.connect(self.show_feat_plot)
        self.add_hist.triggered.connect(self.show_hist)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.add_scatter)
        self.toolbar.addAction(self.add_feat)
        self.toolbar.addAction(self.add_hist)

        # statusbar
        self.mem = psutil.virtual_memory()
        mem0 = self.mem.total/10**9
        mem1 = self.mem.used/10**9
        # self.statusBar().showMessage('memory: {}/{} GB'.format(mem1, mem0), QC.Qt.AlignRight)
        self.pbur = QG.QProgressBar()
        self.pbur.setFixedHeight(10)
        self.lbl_status = QG.QLabel()
        self.lbl_status.setText('memory: {}/{} GB'.format(mem1, mem0))
        self.statusBar().addPermanentWidget(self.lbl_status)
        self.statusBar().addPermanentWidget(self.pbur)

        # timer
        self.timer = QC.QTimer(self)
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(500)

        # multi window
        self.mdi = QG.QMdiArea(self)
        self.setCentralWidget(self.mdi)

        # data browser
        self.data_browser = db.data_browser()
        self.data_browser.btn_data0.clicked.connect(self.get_data)

        #layout
        w_mdi = self.mdi.addSubWindow(self.data_browser)
        w_mdi.resize(200, 300)

        # self.get_data()


    def timer_event(self):
        self.mem = psutil.virtual_memory()
        mem0 = self.mem.total/10**9
        mem1 = self.mem.used/10**9
        # self.statusBar().showMessage('memory: {:.3f}/{:.3f} GB'.format(mem1, mem0), QC.Qt.AlignRight)
        self.lbl_status.setText('memory: {:.3f}/{:.3f} GB'.format(mem1, mem0))
        # self.statusBar().showMessage()
        self.pbur.setValue(mem1/mem0* 100)
        self.repaint()


    def get_data(self):
        self.data_id += 1
        self.data_path = QG.QFileDialog.getOpenFileName(self, 'Open File', '/home/')
        # data_path = '/home/fkubota/Project/ALSOK/data/稲成ビルFeat/kubota/feat_正常音.pkl'
        # data_path = '/home/fkubota/Project/Yokogawa/data/feat/徳山201809/mfcc-0502/Yokogawa_mfcc-0502_20180831_085430.pkl'
        # self.data_path = '/home/fkubota/MyData/030_GoogleDrive/Python/pyfile/my_APP/MFCC_analysis/data/sample.pkl'
        with open(self.data_path, mode='rb') as f:
            self.feat = pickle.load(f)
        try:
            self.feat = self.feat['data']
        except:
            pass
        self.dataV.append(self.feat)
        self.data_basenameV.append(os.path.basename(self.data_path))
        # self.data_browser.table.setRowCount(self.data_id+1)
        # self.data_browser.table.setItem(0, self.data_id, QG.QTableWidgetItem(self.data_path))
        self.item = QG.QStandardItem(self.data_path)
        self.data_browser.model.appendRow(self.item)


        self.update_scatter_cb_edited()
        self.update_feat_cb_edited()



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

        w_mdi = self.mdi.addSubWindow(w_scatter)
        w_mdi.resize(350, 500)
        w_scatter.add_data()
        self.update_scatter_cb_edited()
        w_mdi.show()

    def setting_update_edited(self):
        tab = self.sender().parent()
        # print(tab.parent().parent().parent())
        # print(tab.parent().parent().parent().parent())
        mod = tab.parent().parent().parent().parent().parent()
        textitem = mod.textitem
        textitem.setText('a')
        textitem.setVisible(False)
        scatter = tab.plot_scatter
        check = tab.check
        step = int(tab.le_scatter0.text())
        data_id = tab.cb_scatter2.currentIndex()
        # feat0 = self.feat[::step, int(tab.cb_scatter0.currentIndex())]
        # feat1 = self.feat[::step, int(tab.cb_scatter1.currentIndex())]
        # scatter.setPoints(feat0, feat1, brush=tab.color+'32')

        if check.isChecked() :
            feat0 = self.dataV[data_id][::step, int(tab.cb_scatter0.currentIndex())]
            feat1 = self.dataV[data_id][::step, int(tab.cb_scatter1.currentIndex())]
            scatter.setPoints(feat0, feat1, brush=tab.color+'32')
        else:
            scatter.clear()

    def change_color_edited(self):
        btn = self.sender()
        tab = self.sender().parent()
        color = QG.QColorDialog.getColor()
        tab.color = color.name()
        btn.setStyleSheet("background-color: "+ tab.color)


    def update_scatter_cb_edited(self):
        # print(self.sender())
        for scatter_idx in range(len(self.w_scatterV)):
            w_scatter = self.w_scatterV[scatter_idx]
            for tab_idx in range(len(w_scatter.tabV)):
                idx = w_scatter.tabV[tab_idx].cb_scatter2.currentIndex()
                w_scatter.tabV[tab_idx].cb_scatter2.clear()
                w_scatter.tabV[tab_idx].cb_scatter2.addItems(self.data_basenameV)
                if idx!=-1:
                    w_scatter.tabV[tab_idx].cb_scatter2.setCurrentIndex(idx)
                w_scatter.tabV[tab_idx].cb_scatter2.update()

    def show_feat_plot(self):
        self.feat_plot += 1
        id = self.feat_plot
        self.w_feat_plotV.append(fp.feature_plot_mod(self))
        w_feat_plot = self.w_feat_plotV[id]
        w_feat_plot.id = self.feat_plot
        w_feat_plot.setWindowTitle('feature plot : ' + str(id))

        # overload method
        w_feat_plot.feat_setting_update = self.feat_setting_update_edited
        w_feat_plot.feat_change_color = self.feat_change_color_edited
        w_feat_plot.update_feat_cb = self.update_feat_cb_edited

        w_mdi = self.mdi.addSubWindow(w_feat_plot)
        w_mdi.resize(350, 500)
        w_feat_plot.add_Data()
        self.update_feat_cb_edited()
        w_mdi.show()

    def feat_setting_update_edited(self):
        tab = self.sender().parent()
        check = tab.check
        step = int(tab.le0.text())
        data_id = tab.cb2.currentIndex()
        if check.isChecked() :
            length = len(self.dataV[data_id])
            x = np.arange(0, length, 1)
            x = x[::step]
            feat = self.dataV[data_id][::step, int(tab.cb0.currentIndex())]
            tab.curve.setData(x/4/60/60, feat, pen=tab.color+'99')
        else:
            tab.curve.clear()


    def feat_change_color_edited(self):
        btn = self.sender()
        tab = self.sender().parent()
        color = QG.QColorDialog.getColor()
        tab.color = color.name()
        btn.setStyleSheet("background-color: "+ tab.color)

    def update_feat_cb_edited(self):
        for feat_idx in range(len(self.w_feat_plotV)):
            w_feat = self.w_feat_plotV[feat_idx]
            for tab_idx in range(len(w_feat.tabV)):
                idx = w_feat.tabV[tab_idx].cb2.currentIndex()
                w_feat.tabV[tab_idx].cb2.clear()
                w_feat.tabV[tab_idx].cb2.addItems(self.data_basenameV)
                if idx!= -1:
                    w_feat.tabV[tab_idx].cb2.setCurrentIndex(idx)
                w_feat.tabV[tab_idx].cb2.update()

    def show_hist(self):
        self.hist += 1
        id = self.hist
        self.w_hist_plotV.append(histogram.histogram_mod(self))
        w_hist_plot = self.w_hist_plotV[id]
        w_hist_plot.id = self.hist
        w_hist_plot.setWindowTitle('histogram plot : ' + str(id))

        # overload method
        w_hist_plot.hist_setting_update = self.hist_setting_update_edited
        w_hist_plot.hist_change_color = self.hist_change_color_edited
        w_hist_plot.update_hist_cb = self.update_hist_cb_edited

        w_mdi = self.mdi.addSubWindow(w_hist_plot)
        w_mdi.resize(350, 500)
        w_hist_plot.add_Data()
        self.update_hist_cb_edited()
        w_mdi.show()

    def hist_setting_update_edited(self):
        tab = self.sender().parent()
        check = tab.check
        step = int(tab.le0.text())
        bins_num = int(tab.le1.text())
        data_id = tab.cb2.currentIndex()
        if check.isChecked() :
            feat = self.dataV[data_id][::step, int(tab.cb0.currentIndex())]
            hist, bins = np.histogram(feat, bins=bins_num)
            # X = []
            # for i in range(1, len(bins)):
            #     X.append((bins[i-1]+bins[i])/2)
            tab.plot_hist.setData(bins, hist, pen=tab.color+'ff', fillBrush=tab.color+'45', fillLevel=0, stepMode=True)
        else:
            tab.plot_hist.clear()

    def hist_change_color_edited(self):
        btn = self.sender()
        tab = self.sender().parent()
        color = QG.QColorDialog.getColor()
        tab.color = color.name()
        btn.setStyleSheet("background-color: "+ tab.color)

    def update_hist_cb_edited(self):
        for hist_idx in range(len(self.w_hist_plotV)):
            w_hist = self.w_hist_plotV[hist_idx]
            for tab_idx in range(len(w_hist.tabV)):
                idx = w_hist.tabV[tab_idx].cb2.currentIndex()
                w_hist.tabV[tab_idx].cb2.clear()
                w_hist.tabV[tab_idx].cb2.addItems(self.data_basenameV)
                if idx!= -1:
                    w_hist.tabV[tab_idx].cb2.setCurrentIndex(idx)
                w_hist.tabV[tab_idx].cb2.update()




def main():
    app = QG.QApplication(sys.argv)

    ui = mfcc_analysis()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
