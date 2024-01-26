"""
@Description：覆盖文件线程类
@Author：mysondrink@163.com
@Time：2024/1/19 9:24
"""
from PySide2.QtCore import QThread, Signal, QFileInfo
import pandas as pd
import os


class WriteNewFile(QThread):
    def __init__(self, data, new_data, save_path):
        super().__init__()
        self.csv_data = data
        self.new_data = new_data
        self.save_path = save_path

    def run(self) -> None:
        # QFileInfo
        # fileInfo(filePath);
        # QString
        # parentPath = fileInfo.dir().path(); // 获取上一级路径
        fileInfo = QFileInfo(self.save_path)
        parentPath = fileInfo.dir().path()
        save_path = parentPath + '/new_data.xlsx'
        dataone = pd.DataFrame(self.csv_data)
        new_data = pd.DataFrame(self.new_data)
        head = ["序号", "图片名称", "时间", "样本条码", "医生", "类别",
                "阵列", "病人名", "病人性别", "病人年龄", "数据", "status"]
        try:
            if os.path.exists(save_path):
                # 追加
                with pd.ExcelWriter(save_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                    new_data.to_excel(writer, sheet_name="Sheet2", startrow=writer.sheets["Sheet2"].max_row,
                                     index=False, header=False)
            else:
                # 新建
                with pd.ExcelWriter(save_path, mode="w", engine="openpyxl") as writer:
                    new_data.to_excel(writer, sheet_name="Sheet2", header=head, index=False)
            # 覆盖
            with pd.ExcelWriter(self.save_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                dataone.to_excel(writer, sheet_name="Sheet2", header=head, index=False)
        except Exception as e:
            print(e)