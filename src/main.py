"""
MFCC_analysis
"""

import sys
import os
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_path + '/../'))
# sys.path.insert(0, os.path.join(script_path + '/../src'))
import psutil
import numpy as np
import pandas as pd
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pickle
import pyqtgraph as pg
import pyqtgraph.opengl as gl
# from src import data_browser as db
# from src import scatter_mod as sctr
# from src import scatter_3d_mod as sctr_3d
# from src import feature_plot_mod as fp
# from src import histogram_mod as histogram
# from src import tile_plot_mod as sp
import data_browser as db
import scatter_mod as sctr
import scatter_3d_mod as sctr_3d
import feature_plot_mod as fp
import histogram_mod as histogram
import tile_plot_mod as sp


class FeatureLAB(QG.QMainWindow):
    def __init__(self, parent=None):
        # constructor
        super(FeatureLAB, self).__init__(parent)  # superclassのコンストラクタを使用。
        # f = open("./../myStyle_BlackBlue.txt", "r")
        # style = f.read()
        # self.setStyleSheet(style)

        self.feat_nameV = []

        # scatter
        self.scatter = -1
        self.w_scatterV = []
        self.lastClicked = []

        # scatter_3d
        self.scatter_3d = -1
        self.w_scatter_3d_plotV = []

        # feat_plot
        self.feat_plot = -1
        self.w_feat_plotV = []

        # hittgram
        self.hist = -1
        self.w_hist_plotV = []

        # tile_plot
        self.tile = -1
        self.w_tile_plotV = []

        # data_browser
        self.data_id = -1
        self.dataV = []
        self.data_basenameV = []

        self.setWindowTitle('FeatureLAB')
        self.resize(1000, 650)
        self.move(100, 100)

        # tool bar
        self.add_scatter = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'scatter', self)
        self.add_scatter_3d = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'scatter_3d', self)
        self.add_feat = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'feature', self)
        self.add_hist = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'histogram', self)
        self.add_tile = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'), 'tile plot', self)
        self.add_scatter.triggered.connect(self.show_scatter)
        self.add_scatter_3d.triggered.connect(self.show_scatter_3d)
        self.add_feat.triggered.connect(self.show_feat_plot)
        self.add_hist.triggered.connect(self.show_hist)
        self.add_tile.triggered.connect(self.show_tile_plot)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.add_scatter)
        self.toolbar.addAction(self.add_scatter_3d)
        self.toolbar.addAction(self.add_feat)
        self.toolbar.addAction(self.add_hist)
        self.toolbar.addAction(self.add_tile)

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

        # with open(self.data_path, mode='rb') as f:
        #     df = pickle.load(f)

        # csv のみ許可
        df = pd.read_csv(self.data_path)

        self.feat = np.array(df)
        self.feat_nameV.append(df.columns)
        self.dataV.append(self.feat)
        self.data_basenameV.append(os.path.basename(self.data_path))
        # self.data_browser.table.setRowCount(self.data_id+1)
        # self.data_browser.table.setItem(0, self.data_id, QG.QTableWidgetItem(self.data_path))
        self.item = QG.QStandardItem(self.data_path)
        self.data_browser.model.appendRow(self.item)

        self.update_scatter_cb_edited()
        self.update_scatter_3d_cb_edited()
        self.update_feat_cb_edited()
        self.update_hist_cb_edited()
        self.update_tile_cb_edited()

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
        w_scatter.point_clicked = self.point_clicked_edited

        w_mdi = self.mdi.addSubWindow(w_scatter)
        w_mdi.resize(350, 500)
        w_scatter.add_data()
        self.update_scatter_cb_edited()
        w_mdi.show()

    def point_clicked_edited(self, plot, points):
        # print(plot.getViewWidget())
        # print(plot.getViewWidget().parent())
        # print(plot.getViewWidget().parent().parent())
        p0_scatter = plot.getViewWidget().parent().parent().p0_scatter
        tab = p0_scatter.hasTab
        data_idx = tab.cb_scatter2.currentIndex()
        pos = points[0].pos()
        textitem = plot.getViewWidget().parent().parent().textitem

        feats = self.dataV[data_idx]
        idx = np.where(feats == pos[0])
        # b = np.where(feats == pos[1])
        # print(pos[0], pos[1])


        # print(textitem)
        # text = pg.TextItem(str(pos), color='b')#, pos=(pos[0], pos[1]))
        textitem.setPos(pos[0], pos[1])
        text = 'data idx: ' + str(data_idx) +  '\n Time(h) = ' + str(idx[0][0]/4/60/60)
        text = 'data idx : {} \n Time(h) = {:.3f}'.format(data_idx, idx[0][0]/4/60/60)
        # text = 'data idx: {} \n Time(h) {}'
        textitem.setText(text)
        textitem.setVisible(True)
        # w_plot_scatter.addItem(textitem)
        # print(points[0].parent())
        # print(points[0].parent())
        for p in self.lastClicked:
            p.resetPen()
        for p in points:
            if p == points[0]:
                p.setPen('b', width=2)
        self.lastClicked = points

    def setting_update_edited(self):
        print('setting_update_edited')
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
        feat0_id = tab.cb_scatter0.currentIndex()
        feat1_id = tab.cb_scatter1.currentIndex()

        # disconnect
        tab.cb_scatter0.currentIndexChanged.disconnect(self.setting_update_edited)
        tab.cb_scatter1.currentIndexChanged.disconnect(self.setting_update_edited)
        tab.cb_scatter2.currentIndexChanged.disconnect(self.setting_update_edited)

        # feat name update
        tab.cb_scatter0.clear()
        tab.cb_scatter1.clear()
        tab.cb_scatter0.addItems(self.feat_nameV[data_id])
        tab.cb_scatter1.addItems(self.feat_nameV[data_id])
        tab.cb_scatter0.setCurrentIndex(feat0_id)
        tab.cb_scatter1.setCurrentIndex(feat1_id)

        if check.isChecked():
            feat0 = self.dataV[data_id][::step, int(tab.cb_scatter0.currentIndex())]
            feat1 = self.dataV[data_id][::step, int(tab.cb_scatter1.currentIndex())]
            scatter.setPoints(feat0, feat1, brush=tab.color+'32')
        else:
            scatter.clear()

        # reconnect
        tab.cb_scatter0.currentIndexChanged.connect(self.setting_update_edited)
        tab.cb_scatter1.currentIndexChanged.connect(self.setting_update_edited)
        tab.cb_scatter2.currentIndexChanged.connect(self.setting_update_edited)

    def change_color_edited(self):
        btn = self.sender()
        tab = self.sender().parent()
        color = QG.QColorDialog.getColor()
        tab.color = color.name()
        btn.setStyleSheet("background-color: " + tab.color)

    def update_scatter_cb_edited(self):
        # print(self.sender())
        for scatter_idx in range(len(self.w_scatterV)):
            w_scatter = self.w_scatterV[scatter_idx]
            for tab_idx in range(len(w_scatter.tabV)):
                idx = w_scatter.tabV[tab_idx].cb_scatter2.currentIndex()
                w_scatter.tabV[tab_idx].cb_scatter2.clear()
                w_scatter.tabV[tab_idx].cb_scatter2.addItems(self.data_basenameV)
                if idx != -1:
                    w_scatter.tabV[tab_idx].cb_scatter2.setCurrentIndex(idx)
                w_scatter.tabV[tab_idx].cb_scatter2.update()

    def show_scatter_3d(self):
        self.scatter_3d += 1
        id = self.scatter_3d
        self.w_scatter_3d_plotV.append(sctr_3d.scatter_3d_mod(self))
        w_scatter_3d_plot = self.w_scatter_3d_plotV[id]
        w_scatter_3d_plot.id = self.scatter_3d
        w_scatter_3d_plot.setWindowTitle('scatter_3dogram plot : ' + str(id))

        # overload method
        w_scatter_3d_plot.scatter_3d_setting_update = self.scatter_3d_setting_update_edited
        w_scatter_3d_plot.scatter_3d_change_color = self.scatter_3d_change_color_edited
        w_scatter_3d_plot.update_scatter_3d_cb = self.update_scatter_3d_cb_edited

        w_mdi = self.mdi.addSubWindow(w_scatter_3d_plot)
        w_mdi.resize(350, 500)
        w_scatter_3d_plot.add_Data()
        self.update_scatter_3d_cb_edited()
        w_mdi.show()

    def scatter_3d_setting_update_edited(self):
        tab = self.sender().parent()
        check = tab.check
        step = int(tab.le0.text())
        point_size = int(tab.le_point_size.text())
        data_id = tab.cb2.currentIndex()
        feat0_id = tab.cb_feat0.currentIndex()
        feat1_id = tab.cb_feat1.currentIndex()
        feat2_id = tab.cb_feat2.currentIndex()

        # disconnect
        tab.cb2.currentIndexChanged.disconnect(self.scatter_3d_setting_update_edited)
        tab.cb_feat0.currentIndexChanged.disconnect(self.scatter_3d_setting_update_edited)
        tab.cb_feat1.currentIndexChanged.disconnect(self.scatter_3d_setting_update_edited)
        tab.cb_feat2.currentIndexChanged.disconnect(self.scatter_3d_setting_update_edited)

        # feat name update
        tab.cb_feat0.clear()
        tab.cb_feat1.clear()
        tab.cb_feat2.clear()
        tab.cb_feat0.addItems(self.feat_nameV[data_id])
        tab.cb_feat1.addItems(self.feat_nameV[data_id])
        tab.cb_feat2.addItems(self.feat_nameV[data_id])
        tab.cb_feat0.setCurrentIndex(feat0_id)
        tab.cb_feat1.setCurrentIndex(feat1_id)
        tab.cb_feat2.setCurrentIndex(feat2_id)

        if check.isChecked():
            feat0 = self.dataV[data_id][::step, int(tab.cb_feat0.currentIndex())]
            feat1 = self.dataV[data_id][::step, int(tab.cb_feat1.currentIndex())]
            feat2 = self.dataV[data_id][::step, int(tab.cb_feat2.currentIndex())]
            pos = np.array([feat0, feat1, feat2]).T
            c = tab.color
            color = np.array((int(c[1:3],16),int(c[3:5],16),int(c[5:7],16), 99)) / 255
            color = np.array([[color] for _ in range(len(feat0))])
            tab.scatter_3d_plot_item.setData(pos=pos, color=color, size=point_size)
        else:
            tab.scatter_3d_plot_item.setData(pos=None)

        # reconnect
        tab.cb2.currentIndexChanged.connect(self.scatter_3d_setting_update_edited)
        tab.cb_feat0.currentIndexChanged.connect(self.scatter_3d_setting_update_edited)
        tab.cb_feat1.currentIndexChanged.connect(self.scatter_3d_setting_update_edited)
        tab.cb_feat2.currentIndexChanged.connect(self.scatter_3d_setting_update_edited)



    def scatter_3d_change_color_edited(self):
        btn = self.sender()
        tab = self.sender().parent()
        # print(tab.color, type(tab.color))
        color = QG.QColorDialog.getColor()
        tab.color = color.name()
        # print(tab.color, type(tab.color))
        btn.setStyleSheet("background-color: "+ tab.color)

    def update_scatter_3d_cb_edited(self):
        for scatter_3d_idx in range(len(self.w_scatter_3d_plotV)):
            w_scatter_3d = self.w_scatter_3d_plotV[scatter_3d_idx]
            for tab_idx in range(len(w_scatter_3d.tabV)):
                idx = w_scatter_3d.tabV[tab_idx].cb2.currentIndex()
                w_scatter_3d.tabV[tab_idx].cb2.clear()
                w_scatter_3d.tabV[tab_idx].cb2.addItems(self.data_basenameV)
                if idx!= -1:
                    w_scatter_3d.tabV[tab_idx].cb2.setCurrentIndex(idx)
                w_scatter_3d.tabV[tab_idx].cb2.update()

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
        feat_id = tab.cb0.currentIndex()

        # disconnect
        tab.cb0.currentIndexChanged.disconnect(self.feat_setting_update_edited)
        tab.cb2.currentIndexChanged.disconnect(self.feat_setting_update_edited)

        # feat name update
        tab.cb0.clear()
        tab.cb0.addItems(self.feat_nameV[data_id])
        tab.cb0.setCurrentIndex(feat_id)

        if check.isChecked():
            length = len(self.dataV[data_id])
            x = np.arange(0, length, 1)
            x = x[::step]
            feat = self.dataV[data_id][::step, int(tab.cb0.currentIndex())]
            tab.curve.setData(x/4/60/60, feat, pen=tab.color+'99')

            # legend = self.p0_feat.addLegend()
            # print(tab.cb0.currentIndex())
            # tab.legend.addItem(tab.curve, name=self.feat_nameV[data_id][tab.cb0.currentIndex()])

        else:
            tab.curve.clear()

        # reconnect
        tab.cb0.currentIndexChanged.connect(self.feat_setting_update_edited)
        tab.cb2.currentIndexChanged.connect(self.feat_setting_update_edited)

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
        feat_id = tab.cb0.currentIndex()

        # disconnect
        tab.cb0.currentIndexChanged.disconnect(self.hist_setting_update_edited)
        tab.cb2.currentIndexChanged.disconnect(self.hist_setting_update_edited)

        # feat name update
        tab.cb0.clear()
        tab.cb0.addItems(self.feat_nameV[data_id])
        tab.cb0.setCurrentIndex(feat_id)

        if check.isChecked():
            feat = self.dataV[data_id][::step, int(tab.cb0.currentIndex())]
            hist, bins = np.histogram(feat, bins=bins_num)
            # X = []
            # for i in range(1, len(bins)):
            #     X.append((bins[i-1]+bins[i])/2)
            tab.plot_hist.setData(bins, hist, pen=tab.color+'ff', fillBrush=tab.color+'50', fillLevel=0, stepMode=True)
        else:
            tab.plot_hist.clear()

        # reconnect
        tab.cb0.currentIndexChanged.connect(self.hist_setting_update_edited)
        tab.cb2.currentIndexChanged.connect(self.hist_setting_update_edited)



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

    def show_tile_plot(self):
        self.tile += 1
        id = self.tile
        self.w_tile_plotV.append(sp.tile_plot_mod(self))
        w_tile_plot = self.w_tile_plotV[id]
        w_tile_plot.id = self.tile
        w_tile_plot.setWindowTitle('histogram plot : ' + str(id))

        # overload method
        w_tile_plot.tile_setting_update = self.tile_setting_update_edited
        w_tile_plot.tile_change_color = self.tile_change_color_edited
        w_tile_plot.update_tile_cb = self.update_tile_cb_edited
        w_tile_plot.tile_doit = self.tile_doit_edited

        w_mdi = self.mdi.addSubWindow(w_tile_plot)
        w_mdi.resize(350, 500)
        w_tile_plot.add_Data()
        self.update_tile_cb_edited()
        w_mdi.show()

    def tile_setting_update_edited(self):
        pass

    def tile_change_color_edited(self):
        btn = self.sender()
        tab = self.sender().parent()
        color = QG.QColorDialog.getColor()
        tab.color = color.name()
        btn.setStyleSheet("background-color: "+ tab.color)

    def update_tile_cb_edited(self):
        for tile_idx in range(len(self.w_tile_plotV)):
            w_tile = self.w_tile_plotV[tile_idx]
            for tab_idx in range(len(w_tile.tabV)):
                idx = w_tile.tabV[tab_idx].cb2.currentIndex()
                w_tile.tabV[tab_idx].cb2.clear()
                w_tile.tabV[tab_idx].cb2.addItems(self.data_basenameV)
                if idx!= -1:
                    w_tile.tabV[tab_idx].cb2.setCurrentIndex(idx)
                w_tile.tabV[tab_idx].cb2.update()

    def tile_doit_edited(self):
        a = self.sender().parent().parent().parent()
        win = a.parent().parent().parent()
        # win.w_tile_plot.resize(100, 100)
        for tab in win.tabV:
            step = int(tab.le0.text())
            data_id = tab.cb2.currentIndex()
            for idx, feat_name in enumerate(self.feat_nameV[data_id]):
                feat0 = self.dataV[data_id][::step, idx]
                tab.curves[idx].setData(feat0, pen=tab.color+'99')
                win.plots[idx].setTitle(title=feat_name)

        # tab = self.sender().parent()

        # check = tab.check
        # step = int(tab.le0.text())
        # data_id = tab.cb2.currentIndex()
        # if check.isChecked() :


def main():
    app = QG.QApplication(sys.argv)

    ui = FeatureLAB()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
