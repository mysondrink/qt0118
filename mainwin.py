"""
@Description：主界面
@Author：mysondrink@163.com
@Time：2024/1/18 11:45
"""
# -- coding: utf-8 --
from PySide2.QtCore import Qt, QSize, QDir, Signal, QFileInfo
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTableView, \
    QHBoxLayout, QFileDialog, QHeaderView, QAbstractItemView, QMessageBox, \
    QMainWindow
from PySide2.QtGui import QStandardItemModel, QStandardItem, QCloseEvent
import numpy as np
import pandas as pd
from dialog import DataDialog
from writefile import WriteNewFile

SUCCEED_CODE = 202
FAILED_CODE = 404


class MyMainWin(QMainWindow):
    update_json = Signal(dict)
    def __init__(self):
        super().__init__()
        self.flag_dump = 0
        self.csv_data = []
        self.InitUI()

    def closeEvent(self, event) -> None:
        if self.flag_dump == 1:
            reply = QMessageBox.question(self, '退出', '未保存，确定退出？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.writeNewFile()
            else:
                event.ignore()
                return
        self.close()

    def InitUI(self):
        self.setWindowTitle("荧光分析仪数据修改软件")
        self.setObjectName("MainWin")
        w_size = QSize(800, 600)
        self.setMinimumSize(w_size)
        self.resize(1024, 720)
        layout = QVBoxLayout()
        self.setLayout(layout)
        frame = QWidget()
        frame.setLayout(layout)
        self.setCentralWidget(frame)
        btnOpen = QPushButton()
        btnOpen.setObjectName("btnOpen")
        btnOpen.setText("打开文件")
        btnOpen.clicked.connect(self.fileOpen)
        layout.addWidget(btnOpen)
        self.tableView = QTableView()
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.tableView.doubleClicked.connect(self.showDataDialog)
        self.tableView.verticalHeader().setDefaultSectionSize(100)
        layout.addWidget(self.tableView)
        #
        layout_1 = QHBoxLayout()
        layout.addLayout(layout_1)
        btnModify = QPushButton()
        btnModify.setObjectName("btnModify")
        btnModify.setText("修改")
        btnDump = QPushButton()
        btnDump.setObjectName("btnDump")
        btnDump.setText("保存")
        btnDump.clicked.connect(self.writeNewFile)
        layout_1.addWidget(btnModify)
        layout_1.addWidget(btnDump)
        btnModify.hide()

    def fileOpen(self):
        path, _ = QFileDialog.getOpenFileNames(self, "open excel", QDir.currentPath(), "*.xlsx")
        # import chardet
        # with open(path[0], 'rb') as f:
        #     result = chardet.detect(f.read())
        if not path:
            return
        # input_table = pd.read_csv(path[0])
        try:
            self.file_path = path[0]
            input_table = pd.read_excel(path[0], sheet_name="Sheet2")
        except Exception as e:
            print(e)
            return
        input_table_rows = input_table.shape[0]
        input_table_columns = input_table.shape[1]
        input_table_header = input_table.columns.values.tolist()
        model = QStandardItemModel(0, input_table_columns)

        self.csv_data = []
        self.new_data = []

        for i in range(len(input_table_header)):
            model.setHeaderData(i, Qt.Horizontal, input_table_header[i])

        num = 0
        for j in range(input_table_rows):
            input_table_rows_values = input_table.iloc[[j]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
            self.csv_data.append(input_table_rows_values_list)
            if input_table_rows_values_list[-1] == 0:
                for k in range(input_table_columns):
                    input_table_items_list = input_table_rows_values_list[k]
                    item = QStandardItem(str(input_table_items_list))
                    item.setTextAlignment(Qt.AlignCenter)
                    model.setItem(num, k, item)
                num = num + 1
        self.tableView.setModel(model)

    def showDataDialog(self):
        row = self.tableView.currentIndex().row()
        self.dialog = DataDialog()
        self.update_json.connect(self.dialog.getData)
        self.dialog.update_json.connect(self.getData)
        self.dialog.close_dialog.connect(self.show)
        self.update_json.emit(self.csv_data[row])
        self.hide()
        self.dialog.show()

    def getData(self, msg):
        row = msg['row']
        data = msg['data']
        code = msg['code']
        data[-1] = 1
        self.csv_data[row] = data
        self.new_data.append(data)
        self.flag_dump = 1 if code == SUCCEED_CODE else 0

    def writeNewFile(self):
        if not self.csv_data:
            return
        if self.flag_dump == 0:
            return
        self.flag_dump = 0
        print("writeNewFile!")
        thread = WriteNewFile(self.csv_data, self.new_data, self.file_path)
        thread.finished.connect(lambda: thread.deleteLater())
        thread.finished.connect(lambda: QMessageBox.information(self, "提示", "完成文件修改", QMessageBox.Yes))
        thread.start()