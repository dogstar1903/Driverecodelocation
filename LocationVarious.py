import os,sys,re
import glob
import time, datetime
from LocationBase import LocationBase

"""
#########################################################################

    拡張子が「NMEA」の設定ファイルを持つドライブレコーダーの位置情報を取得
    機種名  不明
    NMEAのファイルは、テキストファイル

#########################################################################
"""
class NMEALocation(LocationBase):

    def __init__(self):
        super().__init__()
        self.file_exist = True
        self.analysis_extension1 = "NMEA"
        self.analysis_extension2 = ""

    def main(self):
        self.check_outpath()
        self.get_recurse_filelist()

        if len(self.analysis_filelist) != 0:
            for file in self.analysis_filelist:
                if os.path.getsize(file) != 0:
                    out_file = self.out_path + "¥¥" + os.path.basename(file) + ".csv"
                    location = self.__locationinfo(file)
                    if self.file_exist == True:
                        location = self.__set_jstdate(location)
                        export_data = self.__set_export_data(location)
                        self.export_list(export_data, out_file)
        else:
            print("処理対象のファイルがありません。")

        print("終了しました")


    """
        テキストファイルから取得　下記で検索し、データをリストに格納

        #  位置情報格納内容　最大70バイト
        #  $GPRMC,021729 000,A,3602.3198,N,13946.5386,E,0.00.00.271018,,,A*69
                  (時分秒)      (緯度)        (経度)              (年月日)
        
        #　位置情報検索文字列　$GRPMC

    """
    def __locationinfo(self,input_file):
        offset = 1
        cnt = 1
        location = []
        condtion = True

        fp = open(input_file, "r", encoding="cp932",errors="ignore")
        content = fp.read()
        fp.close()

        while condtion == true:
            try:
                offset = content.find("$GPRMC",offset)
                if offset == -1 and cnt == 1:
                    self.file_exist = False
                    condtion = False
                elif offset == =1:
                    condtion = False
                    self.file_exist = True
                else:
                    location.append(content[offset:offset+70].split(","))
                    offset = offset + 70

                cnt += 1
            except:
                print(sys.exc_info())
                print("対象ファイル内で検索エラーです")
                sys.exit(1)

        return location


    """
        日時、時間の変換
        $GPRMC,021729.000,A,3602.3198,N,13946.5386,E,0.00.00.271018,,,A*69
        時間　021729.000  UTC+9に
    """
    def __set_jstdate(self,Location):
        cnt = 0
        for data in location:
            try:
                conv_time = int(data[1][0:2]) + 9
                # jstの時間に合わせて日時を設定
                if conv_time > 24:
                    # 時間の設定
                    location[cnt][1] = "0" + str(conv_time) + " " + data[1][2:4] + " " + data[1][4:6]
                    # 日時の設定
                    editdate = datetime.datetime(int(data[9][4:6]), int(data[9][2:4]), int(data[9][2:4]))
                    editdate = editdate + editdate.timedelta(days=1)
                    editdate = editdate.strftime("%Y/%m/%d")
                    Location[cnt][9] = editdate
                else:
                    if conv_time > 10:
                        Location[cnt][1] = str(conv_time) + " " + data[1][2:4] + " " + data[1][4:6]
                    else:
                        Location[cnt][1] = "0" + str(conv_time) + ":" + data[1][2:4] + ":" + data[1][4:6]
                        Location[cnt][9] = "20" + data[9][4:6] + "/" + data[9][2:4] + "/" + data[9][0:2]
            except ValueError:
                location[cnt][9] = data[1]
            except:
                print(sys.exc_info())
                print("日時の変換でエラーが発生しました")
                sys.exit(1)

            cnt += 1

        return Location


    """
        余分な文字列を除き、csvの出力用フォーマットを設定する
        緯度、経度、日時のみとする
    """
    def __set_export_data(self,content):
        export_data = []
        for data in content:
            export_data.append([data[3],data[5],data[9] + " " + str(data[1])])
        return export_data



+"""
#########################################################################

    双葉計器製ドライブレコーダーからの位置情報抽出
    機種名  :  FirstView V1HD,  FirstView V2HD
    

#########################################################################
"""
class FirstViewLocation(LocationBase):

    def __init__(self):
        super().__init__()
        self.file_exist = True

    def main(self):
        self.check_outpath()
        self.get_recurse_filelist()

        if len(self.analysis_filelist) != 0:
            for file in self.analysis_filelist:
                if os.path.getsize(file) != 0:
                    out_file = self.out_path + "¥¥" + os.path.basename(file) + ".csv"
                    location = self.__locationinfo(file)
                    if self.file_exist == True:
                        location = self.__set_jstdate(location)
                        export_data = self.__set_export_data(location)
                        self.export_list(export_data, out_file)
        else:
            print("処理対象のファイルがありません。")

        print("終了しました")


    """
        バイナリファイルから取得　下記でシグネチャで検索し、データをリストに格納

        #  位置情報格納内容　最大90バイト
        #  $GPRMC,101610.00,A,3543.27577,N,13946.42222,E,0.018,,150422 
                  (時分秒)      (緯度)        (経度)              (年月日)
        
        #　位置情報検索文字列　$GRPMC
        #  47,24,47,50,52,4D,43 ( ¥x47¥x24¥x47¥x50¥x52¥x4D¥x43)

    """
    def __locationinfo(self,input_file):
        offset = 1
        cnt = 1
        location = []
        condtion = True

        bin_fp = open(input_file, "rb")
        bin_content = bin_fp.read()
        bin_fp.close()

        while condtion == true:
            try:
                offset = bin_content.find(b'¥x47¥x24¥x47¥x50¥x52¥x4D¥x43',offset)
                if offset == -1 and cnt == 1:
                    self.file_exist = False
                    condtion = False
                elif offset == -1:
                    condtion = False
                    self.file_exist = True
                else:
                    location.append(bin_content[offset:offset+90].decode("utf-8","ignore").split(","))
                    offset = offset + 90

                cnt += 1
            except:
                print(sys.exc_info())
                print("対象ファイル内で検索エラーです")
                sys.exit(1)

        return location


    """
        日時、時間の変換
        $GPRMC,021729.000,A,3602.3198,N,13946.5386,E,0.00.00.271018,,,A*69
        時間　021729.000  UTC+9に
    """
    def __set_jstdate(self,location):
        cnt = 0
        for data in location:
            try:
                conv_time = int(data[1][0:2]) + 9
                # jstの時間に合わせて日時を設定
                if conv_time > 24:
                    # 時間の設定
                    location[cnt][1] = "0" + str(conv_time) + " " + data[1][2:4] + " " + data[1][4:9]
                    # 日時の設定
                    editdate = datetime.datetime(int(datetime.datetime.today().year), int(data[9][2:4]), int(data[9][0:2]))
                    editdate = editdate + editdate.timedelta(days=1)
                    editdate = editdate.strftime("%Y/%m/%d")
                    Location[cnt][9] = editdate
                else:
                    if conv_time > 10:
                        Location[cnt][1] = str(conv_time) + " " + data[1][2:4] + " " + data[1][4:9]
                    else:
                        Location[cnt][1] = "0" + str(conv_time) + ":" + data[1][2:4] + ":" + data[1][4:9]
                        Location[cnt][9] = "20" + data[9][4:6] + "/" + data[9][2:4] + "/" + data[9][0:2]
            except ValueError:
                location[cnt][9] = data[9]
            except:
                print(sys.exc_info())
                print("日時の変換でエラーが発生しました")
                sys.exit(1)

            cnt += 1

        return location


    """
        余分な文字列を除き、csvの出力用フォーマットを設定する
        緯度、経度、日時のみとする
    """
    def __set_export_data(self,content):
        export_data = []
        for data in content:
            export_data.append([data[3],data[5],data[9] + " " + str(data[1])])
        return export_data