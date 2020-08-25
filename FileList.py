import os, sys, re
import glob

"""
################################################################
    指定フォルダ内を処理
################################################################
"""
class FileList:

    def __init__(self):
        # 対象のパスを格納
        self.__path = ""
        # 対象のファイル拡張子１
        self.__extension1 = ""
        # 対象のファイル拡張子２
        self.__extension2 = ""
        # ファイルリストを格納
        self.__file_list = []
    
    # 対象パスのプロパティ
    @property
    def path(self):
        return self.__path
    
    #　対象パスの設定
    @path.setter
    def path(self,value):
        self.__path = value

    #　対象ファイルの拡張子１のプロパティ
    @property
    def extension1(self):
        return self.__extension1

    #　対象ファイルの拡張子１の設定
    @extension1.setter
    def extensin1(self,value):
        self.__extension1 = value

    #　対象ファイルの拡張子２のプロパティ
    @property
    def extension2(self):
        return self.__extension2

    #　対象ファイルの拡張子２の設定
    @extension2.setter
    def extension2(self,value):
        self.__extension2 = value

    #　パス内のファイル一覧を返す
    @property
    def file_list(self):
        return self.__file_list

    """
    ####################################################################
         指定パスから、指定の拡張子又は拡張子のないファイルの一覧を返す
    ####################################################################
    """
    def set_file_list(self):
        try:
            # 拡張子がないファイルの一覧を指定のフォルダ内のみから取得
            if self.__extension1 == "" and self.__extension2 == "":
                files = glob.glob(self.__path + "¥*")
                for filename in file:
                    # 指定したフォルダ内にあるサブフォルダ名は抽出しない
                    if os.path.isdir(filename):
                        pass
                    else:
                        # 拡張子がないファイル
                        if self.__extension1 == "" and self.__extension2 == "":
                            # 取得したファイル名から、拡張子がないファイルの一覧を作成
                            name, ext = os.path.splitext(filename)
                            if ext == "":
                                self.__file_list.append(filename)
                        #　拡張子があるファイル
                        elif self.__extension1 != "":
                            if filename.endswith(self.__extension1) or filename.endswith(self.__extension2):
                                self.__file_list.append(os.path.join(pathname,filename))
        except:
            print(sys.exc_info())
            print("指定フォルダ内で、処理対象ファイルの情報取得エラーです")
            sys.exit(1)


    """
    ####################################################################
         指定パスから、再起的に指定拡張子又は拡張子がないファイルの一覧を返す
    ####################################################################
    """
    def set_recurse_list(self):
        if self.__extension2 == "":
            self.__extension2 = self.__extension1
    
        try:
           # 拡張子が指定されている場合、指定のフォルダ以下から再帰的にファイル一覧を取得する
           for pathname, dirname, filenames in os.walk(self.__path):
                for filename in file:
                    # 指定したフォルダ内にあるサブフォルダ名は抽出しない
                    if os.path.isdir(filename):
                        pass
                    else:
                        # 拡張子がないファイル
                        if self.__extension1 == "" and self.__extension2 == "":
                            # 取得したファイル名から、拡張子がないファイルの一覧を作成
                            name, ext = os.path.splitext(filename)
                            if ext == "":
                                self.__file_list.append(filename)
                        #　拡張子があるファイル
                        elif self.__extension1 != "":
                            if filename.endswith(self.__extension1) or filename.endswith(self.__extension2):
                                self.__file_list.append(os.path.join(pathname,filename))
        except:
            print(sys.exc_info())
            print("指定フォルダ内で、処理対象ファイルの情報取得エラーです")
            sys.exit(1) 