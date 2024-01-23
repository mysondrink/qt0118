"""
@Description：过敏原窗口
@Author：mysondrink@163.com
@Time：2024/1/18 13:26
"""
from PySide2.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, \
    QHBoxLayout, QTableView, QHeaderView, QAbstractItemView, QPushButton, QMessageBox
from PySide2.QtCore import Signal, QSize, Qt
from PySide2.QtGui import QCloseEvent, QStandardItem, QStandardItemModel
import re

# label_list = ["序号", "图片名称", "时间", "样本条码", "医生", "类别", "阵列", "病人名", "病人性别", "病人年龄", "数据"]
LABEL_LIST = ["序号", "图片名称", "时间", "样本条码", "医生", "类别", "阵列", "病人名", "病人性别", "病人年龄"]
SUCCEED_CODE = 202
FAILED_CODE = 404


class DataDialog(QWidget):
    update_json = Signal(dict)
    close_dialog = Signal()

    def __init__(self):
        super().__init__()
        self.flag_dump = 0
        self.InitUI()

    def closeEvent(self, event) -> None:
        if self.flag_dump == 1:
            reply = QMessageBox.question(self, '退出', '未保存，确定退出？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                pass
            else:
                event.ignore()
                return
        self.close_dialog.emit()
        self.close()

    def InitUI(self):
        size = QSize(800, 600)
        self.setMinimumSize(size)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.gridlayout = QGridLayout()
        self.gridlayout.setVerticalSpacing(0)
        layout.addLayout(self.gridlayout)
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        layout.addWidget(self.tableView)
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        for i in range(len(LABEL_LIST)):
            item = QLabel()
            item.setText(LABEL_LIST[i])
            self.gridlayout.addWidget(item, i, 0)
        self.btnModify = QPushButton()
        self.btnModify.setObjectName("btnModify")
        self.btnModify.setText("编辑")
        self.btnModify.clicked.connect(self.on_btnModify_clicked)
        self.btnDump = QPushButton()
        self.btnDump.setObjectName("btnDump")
        self.btnDump.setText("保存")
        self.btnDump.clicked.connect(self.on_btnDump_clicked)
        self.btnDump.setEnabled(False)
        self.gridlayout.addWidget(self.btnModify, len(LABEL_LIST), 0)
        self.gridlayout.addWidget(self.btnDump, len(LABEL_LIST), 1)

    def getData(self, msg):
        self.reagent_info = msg
        for i in range(len(msg) - 2):
            item = QLabel()
            item.setText(str(msg[i]))
            self.gridlayout.addWidget(item, i, 1)
        self.setTableView(msg[-2])

    def setTableView(self, data):
        model = QStandardItemModel(0, 5)
        title_list = ["定位点", "", "", "", "定位点"]
        data_copy = re.split(r",", data)
        data_copy = title_list + data_copy
        for i in range(len(data_copy)):
            pix_num = data_copy[i]
            item = QStandardItem(str(pix_num))
            item.setTextAlignment(Qt.AlignCenter)
            model.setItem(int(i / 5), i % 5, item)
        self.tableView.setModel(model)

    def on_btnModify_clicked(self):
        self.flag_dump = 1
        if self.tableView.editTriggers() == QAbstractItemView.NoEditTriggers:
            self.tableView.setEditTriggers(QAbstractItemView.DoubleClicked)
            self.btnDump.setEnabled(True)
        else:
            self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.btnDump.setEnabled(False)

    def on_btnDump_clicked(self):
        row = self.reagent_info[0] - 1
        code = FAILED_CODE
        # test = (self.readTableView() == self.reagent_info[-1])
        if self.flag_dump == 1:
            self.reagent_info[-2] = self.readTableView()
            code = SUCCEED_CODE
        self.update_json.emit(dict(row=row, data=self.reagent_info, code=code))
        self.flag_dump = 0
        QMessageBox.information(self, "提示", "保存成功", QMessageBox.Yes)

    def readTableView(self):
        model = self.tableView.model()
        row = model.rowCount()
        column = model.columnCount()
        reagent_info = ""
        for i in range(1, row):
            for j in range(column):
                index = model.index(i, j)
                data = "" if index.data() == None else index.data()
                reagent_info = reagent_info + "," + data
        return reagent_info[1:]
