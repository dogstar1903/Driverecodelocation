import win32com.client
import os, sys, re
import glob
from Abstractmodules import ExportList

"""
#######################################################################
    csv形式で一覧化
#######################################################################
"""
class CsvList(ExportList):
    #
    #   クラス生成時にエクセルファイル名を指定
    #
    def __init__(self,filename):
        ###  インスタンス変数の初期化及び設定
        self.wfp = open(filename,"w")
        self.header = ""
        self.data = []

    #
    #  引数を可変（タプル）で受け、一覧表の見出しを設定
    #
    def setheader(self,*args):
        cnt = 1
        # 引数の数だけ一覧の見出しを設定
        for data in args:
            if cnt == 1:
                header = data
            else:
                header = header + "." + data
            cnt += 1
        
        self.wfp.writeline(header + "¥n")

    #
    #  リストデータを「,」区切りで書き込む
    #
    def writedata(self,content):
        try:
            for data in content:
                data_str = ",".join(map(str,data))
                self.wfp.writelines(data_str + "¥n")
        except:
            print("csvファイルの書き込みエラーです。")
        finally:
            self.wfp.close()

    def __del__(self):
        self.wfp.close()






"""
#######################################################################
    端末にインストールされているExcelを呼び出し使用
    入力データを一覧化し、　Excelに出力
#######################################################################
"""
class ExcelList(ExportList):

    #
    # クラス生成時にエクセルファイル名を指定
    #
    def __init__(self, filename):

        ### インスタンス変数の初期化及び設定

        # 保存するファイルの設定
        self.filename = filename
        # Excelのインスタンス
        self.xlApp = win32com.client.Dispatch("Excel.Application")
        self.xlApp.Workbooks.Add()
        self.book = self.xlApp.Workbooks(1)
        self.sheet = self.book.Sheets(1)
        self.book.Activate
        self.xlApp.Visible = 1


    #
    # 引数を可変(タプル)で受け、一覧表の見出しを設定
    #
    def setheader(self, *args):
        colnum = 1
        row=1

        # 引数分だけ、一覧の見出しを設定
        for header in args:
            self.sheet.Cells(row, colnum).value = header
            colnum = colnum + 1


	#
	# 可変の引数で渡された分の内容を書き込み
	#            rownum : 書き込む行数、
	#            *args  : 書き込むデータ(可変)
	#
	#	エラー処理を入れる	文字列によってエラーが発生する
	#
    def write(self, rownum, *args):
		#rownum=2
        colnum=1

        #try:
        for value in args:
            #print("書き込み"+value)
            self.sheet.Cells(rownum, colnum).Value = value
            colnum = colnum + 1
		#except:
		#	print("excelの書き込みエラーです。")
        #finally:
        #    self.save()


    # 
    # 一覧表の罫線等を設定
    #
    #   Excelに渡す定数は、Office環境(VBA等)で設定されている値と同一
    #
    def layout(self,cnum,recnum):

        # 出力する行数(レコード件数)にヘッダ1行分を足す
        recnum = recnum + 1
        # Excelに渡す定数の設定
        xlCenter = -4108
        xlEdgeTop = 8
        xlEdgeBottom = 9
        xlEdgeLeft = 7
        xlEdgeRight = 10
        xlContinuous = 1
        xlMedium = -4138
        xlDouble = -4119


        # 見出しの横位置を中央に設定
        self.sheet.Range(self.sheet.Cells(1, 1), self.sheet.Cells(1, cnum)).HorizontalAlignment = xlCenter
        # 列範囲に中太の罫線を設定
        borders = self.sheet.Range(self.sheet.Cells(1, 1), self.sheet.Cells(recnum, cnum)).Borders
        # セルに罫線を設定
        borders(xlEdgeTop).LineStyle = xlContinuous
        borders(xlEdgeLeft).LineStyle = xlContinuous
        borders(xlEdgeRight).LineStyle = xlContinuous
        borders(xlEdgeTop).Weight = xlMedium
        borders(xlEdgeBottom).Weight = xlMedium
        borders(xlEdgeLeft).Weight = xlMedium
        borders(xlEdgeRight).Weight = xlMedium

        #self.sheet.Borders(xlEdgeTop).LineStyle = xlContinuous
        #self.sheet.Borders(xlEdgeBottom).LineStyle = xlContinuous
        #self.sheet.Borders(xlEdgeLeft).LineStyle = xlContinuous
        #self.sheet.Borders(xlEdgeRight).LineStyle = xlContinuous
        #self.sheet.Borders(xlEdgeTop).Weight = xlMedium
        #self.sheet.Borders(xlEdgeBottom).Weight = xlMedium
        #self.sheet.Borders(xlEdgeLeft).Weight = xlMedium
        #self.sheet.Borders(xlEdgeRight).Weight = xlMedium

        # 全体に罫線を設定
        self.sheet.Range(self.sheet.Cells(1, 1), self.sheet.Cells(recnum, cnum)).Borders.LineStyle = xlContinuous

        # 見出しの下に二重線、背景色を水色にする
        self.sheet.Range(self.sheet.Cells(1, 1), self.sheet.Cells(1, cnum)).Borders(xlEdgeBottom).LineStyle = xlDouble
        self.sheet.Range(self.sheet.Cells(1, 1), self.sheet.Cells(1, cnum)).Interior.ColorIndex = 20
        # オートフィルタを表示
        self.sheet.rows("1:"+str(cnum)).AutoFilter()


    # ブックを保存
    def save(self):
        # sheet名を設定
        title = "メール一覧"
        self.sheet.Name = title
        # bookを保存
        #print(self.filename)
        self.book.SaveAs(self.filename)
        self.xlApp.Quit()




class ExcelRead:

    #
    # クラス生成時にエクセルファイル名を指定
    #
    def __init__(self, filename):
        ### インスタンス変数の初期化及び設定
        # 保存するファイルの設定
        self.filename = filename
        # Excelのインスタンス
        self.xlApp = win32com.client.Dispatch("Excel.Application")
        self.xlbook = self.xlApp.Workbooks.Open(filename)
        self.book.Activate
        self.xlApp.Visible = 0
        self.xlrange = []

    # 読み込むシートの設定
    def setSheet(self,sheetNum):
        self.xlsheet = self.xlbook.Sheets(sheetNum)

    # 値が入力されているシート範囲をリストで返す
    def getSheetValue(self):
        self.sheetRange = self.xlsheet.UsedRange
        self.xlrange = self.sheetRange.Value
        return self.xlrange

    """ 
      値が入っているシートの最終列の番号を返す
      ※値が飛び飛びに入っていると最終列番号まで取得できない場合に対応すること
      ※getSheetValueを呼び出さないとエラーになる
    """
    def getSheetEndColumnnum(self):
        # return self.xlsheet.Range("A1").End(-4161).Column
        return self.sheetRange.Columns.Count

    """ 
      シートの最終行の番号を返す
      ※値が飛び飛びに入っていると最終列番号まで取得できない場合に対応すること 
      ※getSheetValueを呼び出さないとエラーになる
    """
    def getSheetEndRownum(self):
        # return self.xlsheet.Range("A1").End(-4121).Row
        return self.sheetRange.Rows.Count
   
    # ブックを閉じる
    def close(self):
        self.xlbook.close()

    # デストラクタ
    def __del__():
        self.xlApp.Quit()
        self.xlApp = Nothing
        self.xlbook = Nothing
        self.xlsheet = Nothing

