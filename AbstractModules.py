from abc import ABCMeta, abstractclassmethod

"""
     一覧出力クラスの抽象クラス
"""
class ExportList(metaclass=ABCMeta):

    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def setheader(self):
        pass

    @abstractclassmethod
    def writedata(self):
        pass

    @abstractclassmethod
    def __del__(self):
        pass



"""
    ドライブレコーダー位置情報抽出の抽象クラス
"""
class DriveRecoderLocation(metaclass=ABCMeta):

    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def get_filelist(self):
        pass

    @abstractclassmethod
    def export_location(self):
        pass

    @abstractclassmethod
    def set_export_data(self):
        pass