import os,sys,re
import glob
import time,datetime
from ExportList import CsvList
from FileList import FileList

"""
###################################################################
    ドライブレコーダー位置情報取得の基本機能クラス
###################################################################
"""
class LocationBase():

    def __init__(self):
        self.__analysis_path        = ""
        self.__analysis_extension1  = ""
        self.__analysis_extension2  = ""
        self.__analysis_filelist    = []
        self.__out_path             = os.getcwd() + "¥¥result"

    @property
    def analysis_path(self):
        return self.__analysis_path

    @analysis_path.setter
    def analysis_path(self,value):
        self.__analysis_path = value

    @property
    def analysis_extension1(self):
        return self.__analysis_extension1

    @analysis_extension1.setter
    def analysis_extension1(self,value):
        self.__analysis_extension1 = value

    @property
    def analysis_extension2(self):
        return self.__analysis_extension2

    @analysis_extension2.setter
    def analysis_extension2(self,value):
        self.__analysis_extension2 = value

    @property
    def analysis_filelist(self):
        return self.__analysis_filelist

    @property
    def out_path(self):
        return self.__out_path

    """
        出力フォルダの存在チェック、なければ作成
    """
    def check_outpath(self):
        if os.path.isdir(self.__out_path) == False:
            os.mkdir(self.__out_path)

    """
        指定フォルダから処理対象ファイルを取得して、位置情報をcsvに出力する
    """
    def export_location(self):
        pass

    """
        指定のパスから、指定の拡張子のファイル一覧を取得して返す
        拡張子の指定がない場合、拡張子がないファイルの一覧を返す
    """
    def get_filelist(self):
        file_list = Filelist()
        file_list.path = self.__analysis_path
        file_list.extension1 = self.__analysis_extension1
        file_list.extension2 = self.__analysis_extension2
        file_list.set_file_list()
        self.__analysis_filelist = file_list.file_list

    """
        指定のパスから、指定の拡張子のファイル一覧を取得して返す
        拡張子の指定がない場合、拡張子がないファイルの一覧を返す
    """
    def get_recurse_filelist(self):
        file_list = FileList()
        file_list.path _ self.__analysis_path
        file_list.extension1 = self.__analysis_extension1
        file_list.extension2 = self.__analysis_extension2
        file_list.set_recurse_list()
        self.__analysis_filelist = file_list.file_list

    """
         ファイルから位置情報取得
    """
    def locationinfo(self,input_file):
        pass

    """
         日付、時間の変換
    """
    def set_jstdate(self,location):
        pass

    """
        余分な文字列を除き、csvの出力用フォーマットを設定する
        緯度、経度、日時のみとする
    """
    def set_export_data(self,content):
        pass

    """
        csvファイルの出力
    """
    def export_list(self,content,out_file):
        export_data = CsvList(out_file)
        export_data.setheader("緯度","経度","日時")
        export_data.writedata(content)