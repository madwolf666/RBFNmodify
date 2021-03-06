################################################################################
# 全降雨データの作成
################################################################################
import sys
import os
import datetime
import csv
import threading
import gc
from multiprocessing import Value
from ctypes import *
from ctypes import wintypes
import pandas as pd
import com_functions

#class Thread_MakeAllRainfallDataByMesh(threading.Thread):
class MakeAllRainfallDataByMesh():
    '''
     def __init__(self,
                     h_proc_num,
                     h_ini_path,
                     h_DisasterFile,
                     h_CautionAnnounceFile,
                     h_year,
                     h_meshIdx,
                     h_meshList
                     ):
                     '''
    '''
          def __init__(self,
                     h_proc_num,
                     h_ini_path,
                     h_DisasterFile,
                     h_CautionAnnounceFile,
                     h_TemperatureFile,
                     h_RainfallFile,
                     h_SoilRainFile,
                     h_RainfallFile1,
                     h_SoilRainFile1,
                     h_year,
                     h_meshIdx,
                     h_meshList
                     ):
                     '''

    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_key_Disaster,
                 h_size_Disaster,
                 h_key_CautionAnnounce,
                 h_size_CautionAnnounce,
                 h_key_Temperature,
                 h_size_Temperature,
                 h_key_Rainfall,
                 h_size_Rainfall,
                 h_key_SoilRain,
                 h_size_SoilRain,
                 h_key_Rainfall1,
                 h_size_Rainfall1,
                 h_key_SoilRain1,
                 h_size_SoilRain1,
                 h_year,
                 h_meshIdx,
                 h_meshList
                 ):
        '''
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_DisasterFile,
                 h_CautionAnnounceFile,
                 h_TemperatureFile,
                 h_RainfallFile,
                 h_SoilRainFile,
                 h_RainfallFile1,
                 h_SoilRainFile1,
                 h_year,
                 h_meshIdx,
                 h_meshList
                 ):
                 '''

        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        '''
        self.ini_path = h_ini_path
        self.year = h_year
        self.meshIdx = h_meshIdx
        '''
        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path

        '''
        self.com.g_textline_DisasterFile = h_DisasterFile
        self.com.g_textline_CautionAnnounceFile = h_CautionAnnounceFile
        '''
        '''
        self.com.g_textline_TemperatureFile = h_TemperatureFile
        self.com.g_textline_RainfallFile = h_RainfallFile
        self.com.g_textline_SoilRainFile = h_SoilRainFile
        self.com.g_textline_RainfallFile1 = h_RainfallFile1
        self.com.g_textline_SoilRainFile1 = h_SoilRainFile1
        '''

        '''
        self.com.g_textSum_DisasterFile = len(self.com.g_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile = len(self.com.g_textline_CautionAnnounceFile)
        '''
        '''
        self.com.g_textSum_TemperatureFile = len(h_TemperatureFile)
        self.com.g_textSum_RainfallFile = len(h_RainfallFile)
        self.com.g_textSum_SoilRainFile = len(h_SoilRainFile)
        self.com.g_textSum_RainfallFile1 = len(h_RainfallFile1)
        self.com.g_textSum_SoilRainFile1 = len(h_SoilRainFile1)
        '''

        self.year = h_year
        self.meshIdx = h_meshIdx
        self.meshList = h_meshList

        self.isProc = False
        if (self.meshIdx >= 0):
            #proc
            self.isProc = True

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        # 共有メモリ
        self.g_shmlib = windll.LoadLibrary(".\\bin\\rbfnshmctl.dll")
        self.PyShmMapRead = self.g_shmlib.PyShmMapRead
        self.PyShmMapRead.argtypes = [c_char_p, c_void_p]
        self.PyShmMapRead.restype = c_char_p

        try:
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  str(h_year))

            # 災害情報
            if (h_size_Disaster != None):
                #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  h_key_Disaster)
                a_cpyMem = self.PyShmMapRead(
                    c_char_p(h_key_Disaster.encode("sjis")),
                    c_void_p(h_size_Disaster)
                )
                self.com.g_textSum_DisasterFile = self.com.Store_Shm(a_cpyMem, self.com.g_textline_DisasterFile)

            # 警戒情報
            if (h_size_CautionAnnounce != None):
                #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  h_key_CautionAnnounce)
                a_cpyMem = self.PyShmMapRead(
                    c_char_p(h_key_CautionAnnounce.encode("sjis")),
                    c_void_p(h_size_CautionAnnounce)
                )
                self.com.g_textSum_CautionAnnounceFile = self.com.Store_Shm(a_cpyMem, self.com.g_textline_CautionAnnounceFile)

            # 気温
            if (h_size_Temperature != None):
                #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  h_key_Temperature)
                a_cpyMem = self.PyShmMapRead(
                    c_char_p(h_key_Temperature.encode("sjis")),
                    c_void_p(h_size_Temperature)
                )
                self.com.g_textSum_TargetMeshFile = self.com.Store_Shm(a_cpyMem, self.com.g_textline_TargetMeshFile)

            # 全降雨
            if (h_size_Rainfall != None):
                #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  h_key_Rainfall)
                a_cpyMem = self.PyShmMapRead(
                    c_char_p(h_key_Rainfall.encode("sjis")),
                    c_void_p(h_size_Rainfall)
                )
                self.com.g_textSum_RainfallFile = self.com.Store_Shm(a_cpyMem, self.com.g_textline_RainfallFile)
            if (h_size_SoilRain != None):
                #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  h_key_SoilRain)
                a_cpyMem = self.PyShmMapRead(
                    c_char_p(h_key_SoilRain.encode("sjis")),
                    c_void_p(h_size_SoilRain)
                )
                self.com.g_textSum_SoilRainFile = self.com.Store_Shm(a_cpyMem, self.com.g_textline_SoilRainFile)

            #予測適中率
            if self.com.g_RainKind != 0:
                if (h_size_Rainfall1 != None):
                    #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  h_key_Rainfall1)
                    a_cpyMem = self.PyShmMapRead(
                        c_char_p(h_key_Rainfall1.encode("sjis")),
                        c_void_p(h_size_Rainfall1)
                    )
                    self.com.g_textSum_RainfallFile1 = self.com.Store_Shm(a_cpyMem, self.com.g_textline_RainfallFile1)
                if (h_size_SoilRain1 != None):
                    #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, "MakeAllRainfallDataByMesh-init",  h_key_SoilRain1)
                    a_cpyMem = self.PyShmMapRead(
                        c_char_p(h_key_SoilRain1.encode("sjis")),
                        c_void_p(h_size_SoilRain1)
                    )
                    self.com.g_textSum_SoilRainFile1 = self.com.Store_Shm(a_cpyMem, self.com.g_textline_SoilRainFile1)

            '''
            # 災害情報
            if (h_DisasterFile != None):
                #print(h_DisasterFile.value[0])
                del self.com.g_textline_DisasterFile[:]
                gc.collect()
                self.com.g_textline_DisasterFile = h_DisasterFile[:].split("\n")
                self.com.g_textSum_DisasterFile = len(self.com.g_textline_DisasterFile)
            # 警戒情報
            if (h_CautionAnnounceFile != None):
                del self.com.g_textline_CautionAnnounceFile[:]
                gc.collect()
                self.com.g_textline_CautionAnnounceFile = h_CautionAnnounceFile[:].split("\n")
                self.com.g_textSum_CautionAnnounceFile = len(self.com.g_textline_CautionAnnounceFile)
            # 気温情報
            if (h_TemperatureFile != None):
                del self.com.g_textline_TemperatureFile[:]
                gc.collect()
                self.com.g_textline_TemperatureFile = h_TemperatureFile[:].split("\n")
                self.com.g_textSum_TemperatureFile = len(self.com.g_textline_TemperatureFile)

            # 全降雨
            if (h_RainfallFile != None):
                del self.com.g_textline_RainfallFile[:]
                gc.collect()
                self.com.g_textline_RainfallFile = h_RainfallFile[:].split("\n")
                self.com.g_textSum_RainfallFile = len(self.com.g_textline_RainfallFile)
            if (h_SoilRainFile != None):
                del self.com.g_textline_SoilRainFile[:]
                gc.collect()
                self.com.g_textline_SoilRainFile = h_SoilRainFile[:].split("\n")
                self.com.g_textSum_SoilRainFile = len(self.com.g_textline_SoilRainFile)

            if self.com.g_RainKind != 0:
                if (h_RainfallFile1 != None):
                    del self.com.g_textline_RainfallFile1[:]
                    gc.collect()
                    self.com.g_textline_RainfallFile1 = h_RainfallFile1[:].split("\n")
                    self.com.g_textSum_RainfallFile1 = len(self.com.g_textline_RainfallFile1)
                if (h_SoilRainFile1 != None):
                    del self.com.g_textline_SoilRainFile1[:]
                    gc.collect()
                    self.com.g_textline_SoilRainFile1 = h_SoilRainFile1[:].split("\n")
                    self.com.g_textSum_SoilRainFile1 = len(self.com.g_textline_SoilRainFile1)
                    '''

            '''
            self.com.g_textSum_DisasterFile = self.com.Store_DataFile(self.com.g_DisasterFileName, self.com.g_textline_DisasterFile)
            self.com.g_textSum_CautionAnnounceFile = self.com.Store_DataFile(self.com.g_CautionAnnounceFileName, self.com.g_textline_CautionAnnounceFile)
    
            self.prv_TemperatureFileName = self.com.g_OutPath + "\\" + self.com.g_TemperatureFileSId + str(self.year) +self.com. g_TemperatureFileEId
    
            self.prv_RainfallFileName = self.com.g_OutPath + "\\" + self.com.g_RainfallFileSId + str(self.year) + self.com.g_RainfallFileEId
            self.prv_SoilRainFileName = self.com.g_OutPath + "\\" + self.com.g_SoilrainFileSId + str(self.year) + self.com.g_SoilrainFileEId
            # 予測的中率
            self.prv_RainfallFileName1 = self.com.g_OutPathReal + "\\" + self.com.g_RainfallFileSId + str(self.year) + self.com.g_RainfallFileEId
            self.prv_SoilRainFileName1 = self.com.g_OutPathReal + "\\" + self.com.g_SoilrainFileSId + str(self.year) + self.com.g_SoilrainFileEId
    
            self.com.g_textSum_TemperatureFile = self.com.Store_DataFile(self.prv_TemperatureFileName, self.com.g_textline_TemperatureFile)
            '''

            '''
            if (self.isProc == False):
                self.com.g_textSum_RainfallFile = self.com.Store_DataFile(self.prv_RainfallFileName, self.com.g_textline_RainfallFile)
                self.com.g_textSum_SoilRainFile = self.com.Store_DataFile(self.prv_SoilRainFileName, self.com.g_textline_SoilRainFile)
                if self.com.g_RainKind != 0:
                    self.com.g_textSum_RainfallFile1 = self.com.Store_DataFile(self.prv_RainfallFileName1, self.com.g_textline_RainfallFile1)
                    self.com.g_textSum_SoilRainFile1 = self.com.Store_DataFile(self.prv_SoilRainFileName1, self.com.g_textline_SoilRainFile1)
                    '''

            self.textSum_Rainfall = 0
            self.textline_Rainfall = []
            self.textSum_SoilRain = 0
            self.textline_SoilRain = []

            if (self.isProc == True):
                self.run()   # multiprocess

                del self.com.g_textline_DisasterFile[:]
                del self.com.g_textline_CautionAnnounceFile[:]
                del self.com.g_textline_TargetMeshFile[:]
                del self.com.g_textline_RainfallFile[:]
                del self.com.g_textline_SoilRainFile[:]
                del self.com.g_textline_RainfallFile1[:]
                del self.com.g_textline_SoilRainFile1[:]
                gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "MakeAllRainfallDataByMesh-init",  " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "MakeAllRainfallDataByMesh-init", sys.exc_info())
        finally:
            if (self.g_shmlib != None):
                kernel32 = WinDLL("kernel32", use_last_error=True)
                kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
                kernel32.FreeLibrary(self.g_shmlib._handle)

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path +  ",Year=" + str(self.year) + ",meshIdx=" + str(self.meshIdx)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeAllRainfallDataByMesh-run', a_strErr)

        #a_meshList = []

        try:
            '''
            # 解析雨量のCSVファイルからメッシュ数を取得する。
            if self.com.g_TargetMeshFile != "":
                a_meshSum = self._getMeshSumFromFile(self.year, self.prv_RainfallFileName, a_meshList)
            else:
                a_meshSum = self._getMeshSum(self.year, self.prv_RainfallFileName, a_meshList)
            print(a_meshList)
            '''

            # メッシュ単位に全降雨データを作成する。
            # 実況雨量or予測雨量
            '''
            self._makeAllRainfallDataByMesh(self.year, 0, self.meshIdx, a_meshList)
            if self.com.g_RainKind != 0:
                # 比較対象の実況雨量データの算出
                self._makeAllRainfallDataByMesh(self.year, 1, self.meshIdx, a_meshList)
                '''
            self._makeAllRainfallDataByMesh(
                self.com.g_textSum_RainfallFile,
                self.com.g_textline_RainfallFile,
                self.com.g_textSum_SoilRainFile,
                self.com.g_textline_SoilRainFile,
                self.year,
                0,
                self.meshIdx,
                self.meshList
            )
            if self.com.g_RainKind != 0:
                # 比較対象の実況雨量データの算出
                self._makeAllRainfallDataByMesh(
                    self.com.g_textSum_RainfallFile1,
                    self.com.g_textline_RainfallFile1,
                    self.com.g_textSum_SoilRainFile1,
                    self.com.g_textline_SoilRainFile1,
                    self.year,
                    1,
                    self.meshIdx,
                    self.meshList
                )
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "MakeAllRainfallDataByMesh-run",  a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "MakeAllRainfallDataByMesh-run", a_strErr + "," + sys.exc_info())

    prv_RainfallFileName = ""
    prv_SoilRainFileName = ""
    prv_RainfallFileName1 = ""
    prv_SoilRainFileName1 = ""
    prv_TemperatureFileName = ""

    # メッシュ単位の気温情報を計算する
    def _calTemperatureByMesh(self, h_year, h_kind, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",kind=" + str(h_kind) + ",meshoNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_calTemperatureByMesh', a_strErr)

        a_cnt = 0
        a_strTmp = ""
        a_findDIndex = [[]]
        a_findDIndex2 = [[]]

        try:
            # 一連の降雨抽出結果ファイルを開く。
            a_sFileName = ""
            a_sFileName2 = ""
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindChainOccurRainfallSymbol + str(h_year) + ".csv"
                a_sFileName2 = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\_" + self.com.g_FindChainOccurRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindChainOccurRainfall0Symbol + str(h_year) + ".csv"
                a_sFileName2 = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\_" + self.com.g_FindChainOccurRainfall0Symbol + str(h_year) + ".csv"

            # 一連の降雨毎に平均気温・最高気温を算出する。
            a_prevTime = ""
            a_findDSum = 0

            '''        
                a_sr = open(a_sFileName, 'r', encoding='shift_jis')
                a_line = a_sr.readline().rstrip('\r\n') # 1行目を読み飛ばし
                a_line = a_sr.readline().rstrip('\r\n')
                while a_line:
                    a_split = a_line.split(',')
                '''
            a_csv_data = []
            a_csv_len, a_csv_data = self.com.Store_DataFile_pandas(a_sFileName)
            # 発生降雨フラグが'*'のものｗ抽出する
            for a_row in a_csv_data[a_csv_data['発生降雨フラグ'] == '*'].iterrows():
                a_split = a_row[1]
                a_nowTime = str(a_split[1]) + '/' + str(a_split[2]) + '/' + str(a_split[3]) + ' ' + str(a_split[4])
                a_dt = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')
                # 30分データ取込
                if (self.com.g_TimeKind == 1):
                    # 30分の場合
                    a_dt += datetime.timedelta(minutes=-30)
                else:
                    # 1時間の場合
                    a_dt += datetime.timedelta(hours=-1)
                #a_strTmp = a_dt.strftime('%Y/%m/%d %H:%M')
                a_strTmp = str(a_dt.year) + "/" + str(a_dt.month) + "/" + str(a_dt.day) + " " + str(a_dt.hour) + ":" + str(a_dt.minute).rjust(2, '0')

                if (a_prevTime != a_strTmp):
                    # 異なる一連の降雨となる。
                    a_findDIndex[0].append(a_cnt)
                    if (a_findDSum == 0):
                        a_findDIndex.append(a_cnt)
                        a_findDIndex.append(float(a_split[7]))
                        a_findDIndex.append(0)
                        a_findDIndex.append(float(a_split[7]))
                    else:
                        a_findDIndex[1].append(a_cnt)
                        a_findDIndex[2].append(float(a_split[7]))
                        a_findDIndex[3].append(0)
                        a_findDIndex[4].append(float(a_split[7]))
                    a_findDSum = a_findDSum + 1
                else:
                    a_findDIndex[1][a_findDSum - 1] = a_cnt
                    a_findDIndex[2][a_findDSum - 1] = float(a_findDIndex[2][a_findDSum - 1]) + float(a_split[7])
                    # 最高気温の算出
                    if (float(a_findDIndex[4][a_findDSum - 1]) < float(a_split[7])):
                        a_findDIndex[4][a_findDSum - 1] = float(a_split[7])

                a_prevTime = a_nowTime
                #a_line = a_sr.readline().rstrip('\r\n')
            #a_sr.close()

            del a_csv_data
            gc.collect()
            a_csv_obj = None

            for a_cnt in range(0, a_findDSum):
                # 平均気温の算出
                a_findDIndex[3][a_cnt] = float(a_findDIndex[2][a_cnt]) / (int(a_findDIndex[1][a_cnt]) - int(a_findDIndex[0][a_cnt]) + 1)

            a_findDSum2 = 0
            for a_cntD in range(0, a_findDSum):
                a_IsOccur = False
                # 条件設定された気温の範囲であるかチェックする。
                if (self.com.g_TemperatureKind == 1):    # 平均気温の場合
                    if ((float(a_findDIndex[3][a_cntD]) >= self.com.g_TemperatureMin) and (float(a_findDIndex[3][a_cntD]) <= self.com.g_TemperatureMax)):
                        # 対象
                        a_IsOccur = True
                elif (self.com.g_TemperatureKind == 2):  # 最高気温の場合
                    if ((float(a_findDIndex[4][a_cntD]) >= self.com.g_TemperatureMin) and (float(a_findDIndex[4][a_cntD]) <= self.com.g_TemperatureMax)):
                        # 対象
                        a_IsOccur = True

                if (a_IsOccur == True):
                    a_findDIndex2[0].append(a_cntD)
                    if (a_findDSum2 == 0):
                        a_findDIndex2.append(a_cntD)
                        a_findDIndex2.append(a_cntD)
                        a_findDIndex2.append(a_cntD)
                        a_findDIndex2.append(a_cntD)
                    else:
                        a_findDIndex2[1].append(a_cntD)
                        a_findDIndex2[2].append(a_cntD)
                        a_findDIndex2[3].append(a_cntD)
                        a_findDIndex2[4].append(a_cntD)
                    a_findDSum2 = a_findDSum2 + 1

            # 作成済みのFCORファイル名を変更する。
            if (os.path.isfile(a_sFileName) == True):
                os.remove(a_sFileName)
            os.rename(a_sFileName, a_sFileName2)

            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindChainOccurRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindChainOccurRainfall0Symbol + str(h_year) + ".csv"

            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            # 一連の降雨数を書き込んでおく。
            # 気温情報を書き込む。
            a_sw.write('データ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,発生降雨フラグ,' + str(a_findDSum2) + self.com.SetTemperatureInfo() + '\n')
            a_cnt = 0
            while (a_cnt < self.com.g_textSum_AllRainfall):
                a_split = self.com.g_textline_AllRainfall.ix[a_cnt]
                a_IsOccur = False
                # 1行分の読み込み
                for a_cntD in range(0, a_findDSum2):
                    if (int(a_findDIndex2[0][a_cntD]) == a_cnt):
                        for a_cnt2 in range(int(a_findDIndex2[0][a_cntD]), int(a_findDIndex2[1][a_cntD] + 1)):
                            self.com.Write_TextLine_pandas(a_sw, self.com.g_textline_AllRainfall.ix[a_cnt2], 8)
                            a_sw.write(',*\n')
                        a_cnt = int(a_findDIndex2[1][a_cntD])
                        a_IsOccur = True
                        break

                if (a_IsOccur == False):
                    self.com.Write_TextLine_pandas(a_sw, self.com.g_textline_AllRainfall.ix[a_cnt], 8)
                    a_sw.write(',\n')

                a_cnt += 1
            a_sw.close()

            del a_findDIndex[:]
            del a_findDIndex2[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_calTemperatureByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_calTemperatureByMesh", a_strErr + "," + sys.exc_info())

            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_calTemperatureByMesh', 'end')

    # メッシュ単位の一連の降雨データを自動検出する
    def _findChainOccurRainfallByMesh(self, h_year, h_kind, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",kind=" + str(h_kind) + ",meshoNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_findChainOccurRainfallByMesh', a_strErr)

        a_findDSum = 0
        a_findDIndex = [[]] #２次元配列

        try:
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + '\\' + str(h_meshNo) + '\\' + self.com.g_AllRainfallSymbol + str(h_year) + '.csv'
            else:
                a_sFileName = self.com.g_OutPath + '\\' + str(h_meshNo) + '\\' + self.com.g_AllRainfall0Symbol + str(h_year) + '.csv'

            # 一連の降雨のインデックスを退避する。
            a_cnt = 0
            while (a_cnt < self.com.g_textSum_AllRainfall):
                a_split = self.com.g_textline_AllRainfall.ix[a_cnt]
                if (float(a_split[5]) > 0):
                    #print('a_split[5]=' + a_split[5])
                    # 降雨がある場合
                    a_findDIndex[0].append(a_cnt)
                    if (a_findDSum == 0):
                        a_findDIndex.append([a_cnt])
                        a_findDIndex.append([a_cnt])
                    else:
                        a_findDIndex[1].append(a_cnt)
                        a_findDIndex[2].append(a_cnt)
                    # 前の24時間無降雨を検出する。
                    a_findDIndex[1][a_findDSum] = self._findPrevNonOccurByMesh(self.com.g_textSum_AllRainfall, self.com.g_textline_AllRainfall, a_findDIndex[0][a_findDSum], h_meshNo)
                    # 後の24時間無降雨を検出する。
                    a_findDIndex[2][a_findDSum] = self._findNextNonOccurByMesh(self.com.g_textSum_AllRainfall, self.com.g_textline_AllRainfall, a_findDIndex[0][a_findDSum], h_meshNo)
                    a_cnt = int(a_findDIndex[2][a_findDSum])
                    #print('②a_cnt=' + str(a_cnt))
                    a_findDSum += 1
                a_cnt += 1

            #print('a_findDSum=' + str(a_findDSum))
            # 結果出力ファイルを開く
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + '\\' + str(h_meshNo) + '\\' + self.com.g_FindChainOccurRainfallSymbol + str(h_year) + '.csv'
            else:
                a_sFileName = self.com.g_OutPath + '\\' + str(h_meshNo) + '\\' + self.com.g_FindChainOccurRainfall0Symbol + str(h_year) + '.csv'

            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            # 一連の降雨数を書き込んでおく。
            # 気温情報を書き込む。
            a_sw.write('データ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,発生降雨フラグ,' + str(a_findDSum) + self.com.SetTemperatureInfo() + '\n')
            a_cnt = 0
            while (a_cnt < self.com.g_textSum_AllRainfall):
                a_split = self.com.g_textline_AllRainfall.ix[a_cnt]
                a_IsOccur = False
                for a_cntD in range(0, a_findDSum):
                    if (int(a_findDIndex[1][a_cntD]) == a_cnt):
                        for a_cnt2 in range(int(a_findDIndex[1][a_cntD]), int(a_findDIndex[2][a_cntD] + 1)):
                            self.com.Write_TextLine_pandas(a_sw, self.com.g_textline_AllRainfall.ix[a_cnt2], 8)
                            a_sw.write(',*\n')
                        a_cnt = int(a_findDIndex[2][a_cntD])
                        a_IsOccur = True
                        break
                if (a_IsOccur == False):
                    self.com.Write_TextLine_pandas(a_sw, self.com.g_textline_AllRainfall.ix[a_cnt], 8)
                    a_sw.write(',\n')

                a_cnt += 1
            a_sw.close()

            del a_findDIndex[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findChainOccurRainfallByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findChainOccurRainfallByMesh", a_strErr + "," + sys.exc_info())

            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_findChainOccurRainfallByMesh', 'end')

    # メッシュ単位の災害発生降雨データを自動検出する
    def _findCautionAnnounceRainfallByMesh(self, h_year, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_findCautionAnnounceRainfallByMesh', a_strErr)

        try:
            # 災害発生箇所のインデックスを退避する。
            a_findDSum = 0
            a_cnt = 0
            while (a_cnt < self.com.g_textSum_FindOccurRainfall):
                a_split = self.com.g_textline_FindOccurRainfall.ix[a_cnt]
                if (a_split[8] == "*"):
                    a_sIdx = a_cnt  # 最初のindex
                    a_eIdx = a_cnt  # 最後のindex
                    a_mSTime = datetime.datetime.strptime(str(a_split[1]) + "/" + str(a_split[2]) + "/" + str(a_split[3]) + " " + str(a_split[4]), '%Y/%m/%d %H:%M')
                    a_mETime = None
                    # 次の非発生降雨まで
                    while(a_split[8] == "*"):
                        a_eIdx = a_cnt
                        a_mETime = datetime.datetime.strptime(str(a_split[1]) + "/" + str(a_split[2]) + "/" + str(a_split[3]) + " " + str(a_split[4]), '%Y/%m/%d %H:%M')
                        a_cnt += 1
                        a_split = self.com.g_textline_FindOccurRainfall.ix[a_cnt]

                    #a_cnt -= 1  # デクリメント⇒これがあるとVB.NETと異なる結果になる？
                    a_IsOccur = False
                    # 発生降雨フラグが「*」の場合
                    for a_cntD in range(1, self.com.g_textSum_CautionAnnounceFile):
                        a_splitD = self.com.g_textline_CautionAnnounceFile[a_cntD].split(',')
                        #a_splitD = self.com.g_textline_CautionAnnounceFile[a_cntD]
                        if (a_splitD[0].strip() == h_meshNo):
                            # メッシュ番号が同じ
                            a_sTime = datetime.datetime.strptime(str(a_splitD[1]) + "/" + str(a_splitD[2]) + "/" + str(a_splitD[3]) + " " + str(a_splitD[4]), '%Y/%m/%d %H:%M')
                            a_eTime = datetime.datetime.strptime(str(a_splitD[5]) + "/" + str(a_splitD[6]) + "/" + str(a_splitD[7]) + " " + str(a_splitD[8]), '%Y/%m/%d %H:%M')
                            # 解除の日時はチェックする必要なし？
                            if ((a_sTime >= a_mSTime) and (a_sTime <= a_mETime)):
                                # 年月日時が警戒発表の範囲内
                                a_findDSum += 1
                                a_IsOccur = True
                                break

                    if (a_IsOccur == False):
                        # 警戒情報が災害発生降雨の範囲外
                        for a_cntD in range(a_sIdx, a_eIdx + 1):
                            # a_cntはa_cntDの間違いでは？
                            self.com.Replace_TextLine(self.com.g_textline_FindOccurRainfall.ix[a_cntD], '*', '')
            a_cnt += 1

            # 結果出力ファイルを開く
            a_sw = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindCautionAnnounceOccurRainFallSymbol + str(h_year) + ".csv", 'w', encoding='shift_jis')
            # 気温情報を書き込む。
            a_sw.write('データ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,発生降雨フラグ,' + str(a_findDSum) + self.com.SetTemperatureInfo() + '\n')
            for a_row in self.com.g_textSum_FindOccurRainfall.iterrows():
                # 1行分の読み込み
                a_split = a_row[1]
                self.com.Write_TextLine_pandas(a_sw, a_split, 9)
                a_sw.write('\n')

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findCautionAnnounceRainfallByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findCautionAnnounceRainfallByMesh", a_strErr + "," + sys.exc_info())

    # メッシュ単位の警戒情報のリードタイムを自動検出する
    def _findCautionAnnounceReadTImeByMesh(self, h_year, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_findCautionAnnounceReadTImeByMesh', a_strErr)

        try:
            # 結果出力ファイルを開く
            a_sw = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_CalcCautionAnnounceReadTimeSymbol + str(h_year) + ".csv", 'w', encoding='shift_jis')
            a_sw.write('メッシュNo.,年（警戒）,月（警戒）,日（警戒）,時（警戒）,年（災害）,月（災害）,日（災害）,時（災害）,リードタイム' + self.com.SetTemperatureInfo() + '\n')
            # 災害発生箇所のインデックスを退避する。
            a_findDSum = 0
            a_cnt = 0
            while (a_cnt < self.com.g_textSum_FindOccurRainfall):
                a_split = self.com.g_textline_FindOccurRainfall.ix[a_cnt]
                if (a_split[8] == "*"):
                    a_sIdx = a_cnt  # 最初のindex
                    a_eIdx = a_cnt  # 最後のindex
                    a_mSTime = datetime.datetime.strptime(str(a_split[1]) + "/" + str(a_split[2]) + "/" + str(a_split[3]) + " " + str(a_split[4]), '%Y/%m/%d %H:%M')
                    a_mETime = None
                    a_fFlagD2 = False
                    a_fFlagD = False
                    # 次の非発生降雨まで
                    while(a_split[8] == "*"):
                        a_eIdx = a_cnt
                        a_mETime = datetime.datetime.strptime(str(a_split[1]) + "/" + str(a_split[2]) + "/" + str(a_split[3]) + " " + str(a_split[4]), '%Y/%m/%d %H:%M')
                        a_cnt += 1
                        a_split = self.com.g_textline_FindOccurRainfall.ix[a_cnt]

                    a_cnt -= 1  # デクリメント

                    # 災害情報データをチェック
                    a_TimeD2 = datetime.datetime.now()
                    a_OccurTime = None
                    a_fFlagD2 = False
                    # 一連の降雨で最初の災害発生日時を検出
                    for a_cntD2 in range(1, self.com.g_textSum_DisasterFile):
                        a_splitD2 = self.com.g_textline_DisasterFile[a_cntD2].split(',')
                        #a_splitD2 = self.com.g_textline_DisasterFile[a_cntD2]
                        if (a_splitD2[0].strip() == h_meshNo):
                            # メッシュ番号が同じ
                            a_tmpTime = datetime.datetime.strptime(str(a_splitD2[1]) + "/" + str(a_splitD2[2]) + "/" + str(a_splitD2[3]) + " " + str(a_splitD2[4]), '%Y/%m/%d %H:%M')
                            if (a_tmpTime >= a_mSTime) and (a_tmpTime <= a_mETime):
                                if (a_fFlagD2 == True):
                                    if (a_tmpTime < a_TimeD2):
                                        a_TimeD2 = a_tmpTime
                                        if (len(a_splitD2) >= 10):
                                            # 実時刻あり
                                            a_OccurTime = datetime.datetime.strptime(str(a_splitD2[6]) + "/" + str(a_splitD2[7]) + "/" + str(a_splitD2[8]) + " " + str(a_splitD2[9]), '%Y/%m/%d %H:%M')
                                        else:
                                            # 実時刻なし
                                            a_OccurTime = a_tmpTime
                                else:
                                    a_TimeD2 = a_tmpTime
                                    if (len(a_splitD2) >= 10):
                                        # 実時刻あり
                                        a_OccurTime = datetime.datetime.strptime(str(a_splitD2[6]) + "/" + str(a_splitD2[7]) + "/" + str(a_splitD2[8]) + " " + str(a_splitD2[9]), '%Y/%m/%d %H:%M')
                                    else:
                                        # 実時刻なし
                                        a_OccurTime = a_tmpTime
                                a_fFlagD2 = True

                    # 警戒情報データをチェック
                    a_TimeD = datetime.datetime.now()
                    a_CautionTime = None
                    a_fFlagD = False
                    # 一連の降雨で最初の警戒発表日時を検出
                    for a_cntD in range(1, self.com.g_textSum_CautionAnnounceFile):
                        a_splitD = self.com.g_textline_CautionAnnounceFile[a_cntD].split(',')
                        #a_splitD = self.com.g_textline_CautionAnnounceFile[a_cntD]
                        if (a_splitD[0].strip() == h_meshNo):
                            # メッシュ番号が同じ
                            a_tmpTime = datetime.datetime.strptime(str(a_splitD[1]) + "/" + str(a_splitD[2]) + "/" + str(a_splitD[3]) + " " + str(a_splitD[4]), '%Y/%m/%d %H:%M')
                            if (a_tmpTime >= a_mSTime) and (a_tmpTime <= a_mETime):
                                if (a_fFlagD == True):
                                    if (a_tmpTime < a_TimeD2):
                                        a_TimeD = a_tmpTime
                                        if (len(a_splitD) >= 13):
                                            # 実時刻あり
                                            a_CautionTime = datetime.datetime.strptime(str(a_splitD[9]) + "/" + str(a_splitD[10]) + "/" + str(a_splitD[11]) + " " + str(a_splitD[12]), '%Y/%m/%d %H:%M')
                                        else:
                                            # 実時刻なし
                                            a_CautionTime = a_tmpTime
                                else:
                                    a_TimeD = a_tmpTime
                                    if (len(a_splitD) >= 13):
                                        # 実時刻あり
                                        a_CautionTime = datetime.datetime.strptime(str(a_splitD[9]) + "/" + str(a_splitD[10]) + "/" + str(a_splitD[11]) + " " + str(a_splitD[12]), '%Y/%m/%d %H:%M')
                                    else:
                                        # 実時刻なし
                                        a_CautionTime = a_tmpTime
                                a_fFlagD = True


                    a_iTmp = 0
                    a_sTmp = ""
                    if (a_fFlagD2 == True) and (a_fFlagD == True):
                        a_iTmp = int((a_OccurTime - a_CautionTime).total_seconds() / 60)  # 実時刻対応⇒分計算
                        #a_iTmp = DateDiff(DateInterval.Minute, a_CautionTime, a_OccurTime) # 実時刻対応⇒分計算
                        a_sTmp = str(a_iTmp)
                        # 災害発生日時・警戒発表共に検出
                        a_sw.write(
                            h_meshNo + ","
                            + str(a_CautionTime.year) + "," + str(a_CautionTime.month) + "," + str(a_CautionTime.day) + "," + str(a_CautionTime.hour) + ":" + str(a_CautionTime.minute).rjust(2, "0") + ","
                            + str(a_OccurTime.year) + "," + str(a_OccurTime.month) + "," + str(a_OccurTime.day) + "," + str(a_OccurTime.hour) + ":" + str(a_OccurTime.minute).rjust(2, "0") + ","
                            + a_sTmp
                            + '\n'
                        )
                a_cnt += 1
            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findCautionAnnounceReadTImeByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findCautionAnnounceReadTImeByMesh", a_strErr + "," + sys.exc_info())

    def _findNextNonOccurByMesh(self, h_textSum, h_textline, h_idx, h_meshNo):
        a_strErr = "textSum=" + str(h_textSum) + ",idx=" + str(h_idx) + ",meshoNo=" + h_meshNo
        #print(a_strErr)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE2, '_findNextNonOccurByMesh', a_strErr)

        a_iRet = h_idx
        a_nextIdx = h_idx
        a_IsNonOccur = 0

        try:
            # 30分データ取込
            a_iCoe = 1
            if (self.com.g_TimeKind == 1):
                # 30分の場合
                a_iCoe = 2


            for a_cnt in range(h_idx + 1, h_textSum):
                # 1行分の読み込み
                a_split = h_textline.ix[a_cnt]
                if (float(a_split[5]) <= 0):
                    # 雨量がない場合
                    a_IsNonOccur += 1
                    #print('a_IsNonOccur=' + str(a_IsNonOccur))
                else:
                    # 雨量がある場合
                    a_IsNonOccur = 0
                    a_nextIdx = a_cnt

                if (a_IsNonOccur >= (self.com.g_OccurSepTime * a_iCoe)): # 30分データ取込bug-fixed.
                    # 範囲を超える場合は、ループを抜ける。
                    break

            #print('a_nextIdx=' + str(a_nextIdx))
            a_iRet = a_nextIdx
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findNextNonOccurByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findNextNonOccurByMesh", a_strErr + "," + sys.exc_info())

        #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_findNextNonOccurByMesh', 'end')
        #print('a_iRet=' + str(a_iRet))
        return a_iRet

    def _findOccurRainfallByMesh(self, h_year, h_kind, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",kind=" + str(h_kind) + ",meshoNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE2, '_findOccurRainfallByMesh', a_strErr)

        try:
            # 結果出力ファイルを開く。
            a_sFileName = ""
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_AllRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_AllRainfall0Symbol + str(h_year) + ".csv"

            # 災害発生箇所のインデックスを退避する。
            a_rainTime = None    # 実況雨量・予測雨量
            a_occurTime = None   # 実況雨量・予測雨量
            a_findDSum = 0
            a_findDIndex = [[]]
            a_cnt = 0
            while (a_cnt < self.com.g_textSum_AllRainfall):
                a_split = self.com.g_textline_AllRainfall.ix[a_cnt]
                a_rainTime = datetime.datetime.strptime(str(a_split[1]) + "/" + str(a_split[2]) + "/" + str(a_split[3]) + " " + str(a_split[4]), '%Y/%m/%d %H:%M')
                #print(a_rainTime)
                for a_cntD in range(1, self.com.g_textSum_DisasterFile):
                    a_splitD = self.com.g_textline_DisasterFile[a_cntD].split(',')
                    #a_splitD = self.com.g_textline_DisasterFile[a_cntD]
                    if (a_splitD[0].strip() == h_meshNo):
                        # メッシュ番号が同じ
                        # ⑧予測適中率
                        if (h_kind == 0):
                            # 実況or予測雨量
                            # 実況雨量・予測雨量の取り込み
                            if (self.com.g_RainKind == 0):
                                # 実況雨量
                                a_occurTime = datetime.datetime.strptime(str(a_splitD[1]) + "/" + str(a_splitD[2]) + "/" + str(a_splitD[3]) + " " + str(a_splitD[4]), '%Y/%m/%d %H:%M')
                            else:
                                # 予測雨量
                                a_occurTime = datetime.datetime.strptime(str(a_splitD[1]) + "/" + str(a_splitD[2]) + "/" + str(a_splitD[3]) + " " + str(a_splitD[4]), '%Y/%m/%d %H:%M')
                        else:
                            # 実況雨量
                            a_occurTime = datetime.datetime.strptime(str(a_splitD[1]) + "/" + str(a_splitD[2]) + "/" + str(a_splitD[3]) + " " + str(a_splitD[4]), '%Y/%m/%d %H:%M')
                        #print(a_occurTime)
                        # 実況雨量・予測雨量の取り込み---↓
                        if (a_rainTime == a_occurTime):
                            # 年月日時が同じ
                            a_findDIndex[0].append(a_cnt)
                            if (a_findDSum == 0):
                                a_findDIndex.append([a_cnt])
                                a_findDIndex.append([a_cnt])
                            else:
                                a_findDIndex[1].append(a_cnt)
                                a_findDIndex[2].append(a_cnt)
                            a_findDSum = a_findDSum + 1
                            break
                a_cnt += 1

            # 災害発生箇所のインデックスを元に前後24時間の無降雨を検出する。
            #print('a_findDSum=' + str(a_findDSum))
            #print(a_findDIndex)
            for a_cntD in range(0, a_findDSum):
                # 前の24時間無降雨を検出する。
                a_findDIndex[1][a_cntD] = self._findPrevNonOccurByMesh(self.com.g_textSum_AllRainfall, self.com.g_textline_AllRainfall, a_findDIndex[0][a_cntD], h_meshNo)
                # 後の24時間無降雨を検出する。
                a_findDIndex[2][a_cntD] = self._findNextNonOccurByMesh(self.com.g_textSum_AllRainfall, self.com.g_textline_AllRainfall, a_findDIndex[0][a_cntD], h_meshNo)

            # 結果出力ファイルを開く。
            # ⑧予測適中率
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindOccurRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindOccurRainfall0Symbol + str(h_year) + ".csv"

            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            # 災害発生降雨数を書き込んでおく。
            # 気温情報を書き込む。
            a_sw.write('データ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,発生降雨フラグ,' + str(a_findDSum) + self.com.SetTemperatureInfo() + '\n')
            a_cnt = 0
            while (a_cnt < self.com.g_textSum_AllRainfall):
                a_split = self.com.g_textline_AllRainfall.ix[a_cnt]
                a_IsOccur = False
                # 1行分の読み込み
                for a_cntD in range(0,a_findDSum):
                    if (a_findDIndex[1][a_cntD] == a_cnt):
                        for a_cnt2 in range(a_findDIndex[1][a_cntD], a_findDIndex[2][a_cntD] + 1):
                            self.com.Write_TextLine_pandas(a_sw, self.com.g_textline_AllRainfall.ix[a_cnt2], 8)
                            a_sw.write(",*\n")
                        a_cnt = a_findDIndex[2][a_cntD]
                        #print('②a_cnt=' + str(a_cnt))
                        a_IsOccur = True
                        break

                if (a_IsOccur == False):
                    self.com.Write_TextLine_pandas(a_sw, self.com.g_textline_AllRainfall.ix[a_cnt], 8)
                    a_sw.write(',\n')

                a_cnt += 1
            a_sw.close()

            del a_findDIndex[:]
            gc.collect()

            self.com.g_textSum_FindOccurRainfall, self.com.g_textline_FindOccurRainfall = self.com.Store_DataFile_pandas(a_sFileName)

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findOccurRainfallByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findOccurRainfallByMesh", a_strErr + "," + sys.exc_info())

    def _findPrevNonOccurByMesh(self, h_textSum, h_textline, h_idx, h_meshNo):
        a_strErr = "textSum=" + str(h_textSum) + ",idx=" + str(h_idx) + ",meshoNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE2, '_findPrevNonOccurByMesh', a_strErr)

        a_iCoe = 1
        # 30分データ取込
        if (self.com.g_TimeKind == 1):
            # 30分の場合
            a_iCoe = 2

        a_iRet = h_idx
        a_prevIdx = h_idx
        a_IsNonOccur = 0

        try:
            for a_cnt in range(h_idx - 1, 1, -1):
                # 1行分の読み込み
                #a_split = h_textline[a_cnt].split(',')
                a_split = h_textline.ix[a_cnt]
                if (float(a_split[5]) <= 0):
                    # 雨量がない場合
                    a_IsNonOccur = a_IsNonOccur + 1
                else:
                    # 雨量がある場合
                    a_IsNonOccur = 0
                    a_prevIdx = a_cnt

                if (a_IsNonOccur >= (self.com.g_OccurSepTime * a_iCoe)): # 30分データ取込bug-fixed.
                    # 範囲を超える場合は、ループを抜ける。
                    break

            a_iRet = a_prevIdx
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findPrevNonOccurByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_findPrevNonOccurByMesh", a_strErr + "," + sys.exc_info())

        #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))

        return a_iRet

    '''
    def _getMeshSum(self, h_year, h_RainfallFileName, h_meshList):
        a_strErr = "Year=" + str(h_year) + ",RainfallFileName=" + h_RainfallFileName
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getMeshSum', a_strErr)

        a_iRet = 0

        try:
            # 解析雨量ファイルを開く。
            a_sr = open(h_RainfallFileName, 'r', encoding='shift_jis')
            # メッシュファイルを開く。
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
            # 1行目をリスト変数に読み込む。
            a_textline = a_sr.readline().rstrip('\r\n')
            # 2行目をリスト変数に読み込む。
            a_textline = a_sr.readline().rstrip('\r\n')
            a_split = a_textline.split(',')
            # メッシュ数を取得する
            a_iRet = int(a_split[1])
            #print(a_iRet)
            a_sw.write(str(a_iRet) + '\n')

            # 3行目をリスト変数に読み込む。
            a_textline = a_sr.readline().rstrip('\r\n')
            # 4行目をリスト変数に読み込む。
            a_textline = a_sr.readline().rstrip('\r\n')
            a_split = a_textline.split(",")
            #print(a_split)
            for a_cnt in range(1, a_iRet + 1):
                a_sw.write(str(a_split[a_cnt]) + '\n')
                h_meshList.append(a_split[a_cnt].rstrip('\r\n'))
            # ファイルをクローズする。(Close)
            a_sr.close()
            # ファイルをクローズする。(Close)
            a_sw.close()
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args[0]), a_strErr)
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")

        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))
        #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getMeshSum', 'end')

        return a_iRet
        '''

    '''
    def _getMeshSumFromFile(self, h_year, h_RainfallFileName, h_meshList):
        a_strErr = "Year=" + str(h_year) + ",RainfallFileName=" + h_RainfallFileName
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getMeshSumFromFile', a_strErr)

        a_iRet = 0

        try:
            # 対象メッシュNoファイルを開く。
            a_sr = open(self.com.g_TargetMeshFile, 'r', encoding='shift_jis')
            # メッシュ数をカウントする。
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                a_iRet += 1
                a_textline = a_sr.readline().rstrip('\r\n')
            a_sr.close()
            # 対象メッシュNoファイルを開く。
            a_sr = open(self.com.g_TargetMeshFile, 'r', encoding='shift_jis')
            # メッシュファイルを開く。
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
            # メッシュ数を書込
            a_sw.write(str(a_iRet) + '\n')
            # メッシュ番号を取得する。
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                #print(a_textline)
                if (a_textline != ''):
                    # メッシュ番号を書き込み
                    a_split = a_textline.split(',')
                    if self.com.g_TargetRainMesh == 1:
                        # 1kmメッシュ
                        a_sw.write(a_split[0] + "," + a_split[1] + '\n')
                        h_meshList.append(a_split[0] + "," + a_split[1])
                    else:
                        # 5kmメッシュ
                        a_sw.write(a_split[0] + '\n')
                        h_meshList.append(a_split[0])
                a_textline = a_sr.readline().rstrip('\r\n')
            a_sw.close()
            a_sr.close()
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args[0]), a_strErr)
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")

        #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))
        #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getMeshSumFromFile', 'end')

        return a_iRet
        '''

    '''
    def _makeAllRainfallData(self, h_year):
        a_strErr = "Year=" + str(h_year)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeAllRainfallData', a_strErr)

        a_meshList = []

        try:
            self.prv_RainfallFileName = self.com.g_OutPath + "\\" + self.com.g_RainfallFileSId + str(h_year) + self.com.g_RainfallFileEId
            self.prv_SoilRainFileName = self.com.g_OutPath + "\\" + self.com.g_SoilrainFileSId + str(h_year) + self.com.g_SoilrainFileEId

            # 予測的中率
            self.prv_RainfallFileName1 = self.com.g_OutPathReal + "\\" + self.com.g_RainfallFileSId + str(h_year) + self.com.g_RainfallFileEId
            self.prv_SoilRainFileName1 = self.com.g_OutPathReal + "\\" + self.com.g_SoilrainFileSId + str(h_year) + self.com.g_SoilrainFileEId

            self.prv_TemperatureFileName = self.com.g_OutPath + "\\" + self.com.g_TemperatureFileSId + str(h_year) +self.com. g_TemperatureFileEId

            self.com.Store_RainfallFile(self.prv_RainfallFileName)
            self.com.Store_SoilRainFile(self.prv_SoilRainFileName)
            if self.com.g_RainKind != 0:
                self.com.Store_RainfallFile1(self.prv_RainfallFileName1)
                self.com.Store_SoilRainFile1(self.prv_SoilRainFileName1)

            # 解析雨量のCSVファイルからメッシュ数を取得する。
            if self.com.g_TargetMeshFile != "":
                a_meshSum = self._getMeshSumFromFile(h_year, self.prv_RainfallFileName, a_meshList)
            else:
                a_meshSum = self._getMeshSum(h_year, self.prv_RainfallFileName, a_meshList)
            print(a_meshList)

            # メッシュ単位に全降雨データを作成する。
            for a_cnt in range(0, a_meshSum):
                # 実況雨量or予測雨量
                self._makeAllRainfallDataByMesh(h_year, 0, a_cnt, a_meshList)
                if self.com.g_RainKind != 0:
                    # 比較対象の実況雨量データの算出
                    self._makeAllRainfallDataByMesh(h_year, 1, a_cnt, a_meshList)
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args[0]), a_strErr)
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")

            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeAllRainfallData', 'end')
            '''

    # メッシュ単位の全降雨データを作成する
    def _makeAllRainfallDataByMesh(
            self,
            h_textSum_Rainfall,
            h_textline_RainfallFile,
            h_textSum_SoilRain,
            h_textline_SoilRainFile,
            h_year,
            h_kind,
            h_idx,
            h_meshList
    ):
        a_strErr = "Year=" + str(h_year) + ",kind=" + str(h_kind) + ",idx=" + str(h_idx)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeAllRainfallDataByMesh', a_strErr)

        '''
        global prv_RainfallFileName
        global prv_RainfallFileName1
        global prv_SoilRainFileName
        global prv_SoilRainFileName1
        global prv_TemperatureFileName
        '''

        a_split1 = []
        a_PmeshNO = ""
        a_meshNo = ""
        a_rainIdx = 0
        a_soilIdx = 0

        try:
            if self.com.g_TargetRainMesh == 1:
                # 1km
                a_split1 = h_meshList[h_idx].split(',')
                a_PmeshNO = a_split1[0]
                a_meshNo = a_split1[1]
            else:
                # 5km
                a_meshNo = h_meshList[h_idx]

            # 解析雨量ファイルを開く
            a_sFileName = ""
            a_sFileNameW = ""

            # ⑧予測適中率
            if h_kind == 0:
                a_sFileName = self.prv_RainfallFileName
                '''
                if (self.isProc == False):
                    a_textSum_Rainfall = self.com.g_textSum_RainfallFile
                    a_textline_Rainfall = self.com.g_textline_RainfallFile
                    '''
            else:
                a_sFileName = self.prv_RainfallFileName1
                '''
                if (self.isProc == False):
                    a_textSum_Rainfall = self.com.g_textSum_RainfallFile1
                    a_textline_Rainfall = self.com.g_textline_RainfallFile1
                    '''
            '''
            if (self.isProc == True):
                self.textSum_Rainfall = self.com.Store_DataFile(a_sFileName, self.textline_Rainfall)
                '''

            # 土壌雨量指数ファイルを開く
            if h_kind == 0:
                a_sFileName = self.prv_SoilRainFileName
                '''
                if (self.isProc == False):
                    a_textSum_SoilRain = self.com.g_textSum_SoilRainFile
                    a_textline_SoilRain = self.com.g_textline_SoilRainFile
                    '''
            else:
                a_sFileName = self.prv_SoilRainFileName1
                '''
                if (self.isProc == False):
                    a_textSum_SoilRain = self.com.g_textSum_SoilRainFile1
                    a_textline_SoilRain = self.com.g_textline_SoilRainFile1
                    '''

            '''
            if (self.isProc == True):
                self.textSum_SoilRain = self.com.Store_DataFile(a_sFileName, self.textline_SoilRain)
                '''

            # 気温情報ファイルを開く
            '''
            if self.com.g_TemperatureKind == 1 or self.com.g_TemperatureKind == 2:
                # 平均気温、もしくは最高気温
                a_sr3 = open(self.prv_TemperatureFileName, 'r', encoding='shift_jis')
                '''

            # 4行分、読み飛ばす
            for a_cnt in range(0, h_textSum_Rainfall):
            #for a_cnt in range(0, self.com.g_textSum_RainfallFile):
                a_textline1 = h_textline_RainfallFile[a_cnt]
                a_textline2 = h_textline_SoilRainFile[a_cnt]
                #a_textline1 = self.textline_Rainfall[a_cnt]
                #a_textline2 = self.textline_SoilRain[a_cnt]
                if self.com.g_TemperatureKind == 1 or self.com.g_TemperatureKind == 2:
                    # 平均気温、もしくは最高気温
                    #a_textline3 = a_sr3.readline().rstrip('\r\n')
                    a_textline3 = self.com.g_textline_TemperatureFile[a_cnt]
                if a_cnt == 3:
                    a_split1 = a_textline1.split(',')
                    a_split2 = a_textline2.split(',')
                    #a_split1 = a_textline1
                    #a_split2 = a_textline2
                    # メッシュ番号を取得する
                    if self.com.g_TargetRainMesh == 1:
                        # 1km
                        a_split1 = h_textline_RainfallFile[a_cnt + 1].split(",")
                        #a_textline1 = self.textline_Rainfall[a_cnt + 1]
                        #a_split1 = a_textline1
                        for a_iCnt in range(1, len(a_split2)):
                            if a_split2[a_iCnt] == a_PmeshNO:
                                a_soilIdx = a_iCnt
                                break
                    else:
                        # 5km
                        for a_iCnt in range(1, len(a_split2)):
                            if a_split2[a_iCnt] == a_meshNo:
                                a_soilIdx = a_iCnt
                                break

                    for a_iCnt in range(1, len(a_split1)):
                        if a_split1[a_iCnt] == a_meshNo:
                            a_rainIdx = a_iCnt
                            break

                    # 結果出力のパスを作成
                    if os.path.isdir(self.com.g_OutPath + '\\' + str(a_meshNo)) == False:
                        os.mkdir(self.com.g_OutPath + '\\' + str(a_meshNo))
                    # 結果出力ファイルを開く。(OPen)
                    if h_kind == 0:
                        a_sFileNameW = self.com.g_OutPath + '\\' + str(a_meshNo) + '\\' + self.com.g_AllRainfallSymbol + str(h_year) + '.csv'
                    else:
                        a_sFileNameW = self.com.g_OutPath + '\\' + str(a_meshNo) + '\\' + self.com.g_AllRainfall0Symbol + str(h_year) + '.csv'

                if a_cnt >= 3:
                    break

            a_sw = open(a_sFileNameW, 'w', encoding='shift_jis')
            a_sw.write('データ番号,年,月,日,時,解析雨量,土壌雨量指数,気温' + self.com.SetTemperatureInfo() + '\n')
            # 5行目以降、データを取得する
            for a_cntRF in range(4, h_textSum_SoilRain):
                '''
                if (a_cntRF == 17523):
                    a_tmp = 1
                    '''
            #for a_cntRF in range(4, self.com.g_textSum_SoilRainFile):
                a_writeline = ''
                if self.com.g_TargetRainMesh == 1:
                    # 1km
                    a_textline1 = h_textline_RainfallFile[a_cntRF + 1]
                    #a_textline1 = self.textline_Rainfall[a_cntRF + 1]
                else:
                    # 5km
                    a_textline1 = h_textline_RainfallFile[a_cntRF]
                    #a_textline1 = self.textline_Rainfall[a_cntRF]
                a_textline2 = h_textline_SoilRainFile[a_cntRF]
                #a_textline2 = self.textline_SoilRain[a_cntRF]
                if self.com.g_TemperatureKind == 1 or self.com.g_TemperatureKind == 2:
                    # 5行目以降をリスト変数に読み込む。
                    #a_textline3 = a_sr3.readline().rstrip('\r\n')
                    a_textline3 = self.com.g_textline_TemperatureFile[a_cntRF]
                a_split1 = a_textline1.split(',')
                a_split2 = a_textline2.split(',')
                #a_split1 = a_textline1
                #a_split2 = a_textline2
                if self.com.g_TemperatureKind == 1 or self.com.g_TemperatureKind == 2:
                    # 5行目以降をリスト変数に読み込む。
                    a_split3 = a_textline3.split(',')
                    #a_split3 = a_textline3

                a_splitTime = a_split1[0].split(' ')
                a_splitDate = a_splitTime[0].split('/')

                a_uryou = a_split1[a_rainIdx]
                if self.com.Str_isfloat(a_uryou) == True:
                    if float(a_uryou) < 0:
                        a_uryou = '0'
                else:
                    a_uryou = '0'

                a_dojyou = a_split2[a_soilIdx]
                if self.com.Str_isfloat(a_dojyou) == True:
                    if float(a_dojyou) < 0:
                        a_dojyou = '0'
                else:
                    a_dojyou = '0'

                if self.com.g_TemperatureKind ==1 or self.com.g_TemperatureKind == 2:
                    a_kion = a_split3[a_soilIdx]
                    if self.com.Str_isfloat(a_kion) == False:
                        a_kion = '0'
                else:
                    a_kion = '0'

                # 気温情報を取り込む。
                a_writeline = str(a_cntRF - 3) + ',' + a_splitDate[0] + ',' + a_splitDate[1] + ',' + a_splitDate[2] + ',' + a_splitTime[1] + ',' + a_uryou + ',' + a_dojyou + ',' + a_kion
                a_sw.write(a_writeline + '\n')
            a_sw.close()

            '''
            if self.com.g_TemperatureKind == 1 or self.com.g_TemperatureKind == 2:
                # ファイルをクローズする。(Close)
                a_sr3.close()
                '''

            #del self.com.g_textline_RainfallFile[:]
            #del self.com.g_textline_SoilRainFile[:]
            '''
            if (self.isProc == True):
                del self.textline_Rainfall[:]
                del self.textline_SoilRain[:]
                gc.collect()
                '''

            self.com.g_textSum_AllRainfall, self.com.g_textline_AllRainfall = self.com.Store_DataFile_pandas(a_sFileNameW)
            # 一連の降雨の自動検出を行う
            self._findChainOccurRainfallByMesh(h_year, h_kind, a_meshNo)  #⑧予測的中率
            if self.com.g_TemperatureKind == 1 or self.com.g_TemperatureKind == 2:
                # 平均気温、もしくは最高気温
                self._calTemperatureByMesh(h_year, h_kind, a_meshNo)

            # 一連の降雨ファイルを作成する。
            self._makeChainOccurRainFallDataByMesh(h_year, h_kind, a_meshNo)  #⑧予測適中率
            # 災害発生降雨の自動検出を行う。
            self._findOccurRainfallByMesh(h_year, h_kind, a_meshNo)   #⑧予測適中率
            # 災害発生降雨ファイルを作成する。
            self._makeOccurRainFallDataByMesh(h_year, h_kind, a_meshNo)   #⑧予測適中率

            if h_kind == 0:
                # 一連の降雨から災害発生降雨を取り除く。
                self._makeChainOnlyOccurRainFallDataByMesh(h_year, a_meshNo)
                # RBFNツール用非発生降雨ファイルを作成する。
                self._makeNonOccurRainFallDataByMesh(h_year, a_meshNo)
                # RBFNツール用の入力ファイルを作成する。
                self._makeRBFNDataByMesh(h_year, a_meshNo)
                # 土砂災害警戒情報発表中の災害発生降雨の自動検出を行う。
                self._findCautionAnnounceRainfallByMesh(h_year, a_meshNo)
                # 砂災害警戒情報発表中の災害発生降雨の自動検出を行う。
                self._findCautionAnnounceReadTImeByMesh(h_year, a_meshNo)
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeAllRainfallDataByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeAllRainfallDataByMesh", a_strErr + "," + sys.exc_info())

            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeAllRainfallDataByMesh', 'end')

    # メッシュ単位の一連降雨データを自動検出する
    def _makeChainOccurRainFallDataByMesh(self, h_year, h_kind, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",kind=" + str(h_kind) + ",meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeChainOccurRainFallDataByMesh', a_strErr)

        try:
            # 結果出力ファイルを開く
            a_sFileName  = ""
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindChainOccurRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindChainOccurRainfall0Symbol + str(h_year) + ".csv"
            #a_sr = open(a_sFileName, 'r', encoding='shift_jis')
            a_csv_data = []
            a_csv_len, a_csv_data = self.com.Store_DataFile_pandas(a_sFileName)

            # 土壌雨量指数ファイルを開く。
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath  + "\\" + str(h_meshNo) + "\\" +  self.com.g_ChainOccurRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath  + "\\" + str(h_meshNo) + "\\" +  self.com.g_ChainOccurRainfall0Symbol + str(h_year) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')

            # 一連の発生降雨数を書き込んでおく。
            # 気温情報を書き込む。
            a_cnt = 0
            '''
            a_sw.write('データ番号,一連降雨のデータ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,' + str(a_split[9]) + self.com.SetTemperatureInfo() + '\n')
            # 1行目は読み飛ばす。
            a_textline = a_sr.readline().rstrip('\r\n')
            a_split = a_textline.split(',')
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                a_split = a_textline.split(',')
                '''
            a_sw.write('データ番号,一連降雨のデータ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,' + str(a_csv_data.columns[9]) + self.com.SetTemperatureInfo() + '\n')
            # 発生降雨フラグが'*'のものｗ抽出する
            for a_row in a_csv_data[
                        (a_csv_data['発生降雨フラグ'] == a_csv_data['発生降雨フラグ']) &
                        (a_csv_data['発生降雨フラグ'] == '*')].iterrows():
                a_split = a_row[1]
                a_cnt = a_cnt + 1
                # 発生降雨フラグがある場合
                a_sw.write(
                    str(a_split[0]) + "," + str(a_cnt) + "," + str(a_split[1]) + "," + str(a_split[2]) + "," + str(a_split[3]) + "," + str(a_split[4]) + "," + str(a_split[5]) + "," + str(a_split[6]) + "," + str(a_split[7]) + '\n')
                #a_textline = a_sr.readline().rstrip('\r\n')

            a_sw.close()
            #a_sr.close()

            del a_csv_data
            gc.collect()
            a_csv_obj = None

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeChainOccurRainFallDataByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeChainOccurRainFallDataByMesh", a_strErr + "," + sys.exc_info())

    # メッシュ単位の一連降雨データを自動検出する。
    def _makeChainOnlyOccurRainFallDataByMesh(self, h_year, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeChainOnlyOccurRainFallDataByMesh', a_strErr)

        try:
            # 結果出力ファイルを開く。
            # 全ての行をメモリに退避する。
            a_textSum1 = 0
            a_textline1 = []
            '''
            a_sr = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_ChainOccurRainfallSymbol + str(h_year) + ".csv", 'r', encoding='shift_jis')
            a_line = a_sr.readline().rstrip('\r\n')
            while a_line:
                a_textline1.append(a_line)
                a_textSum1 += 1
                a_line = a_sr.readline().rstrip('\r\n')
            a_sr.close()
            #print('a_textSum1=' + str(a_textSum1))
            '''
            a_csv_obj1 = csv.reader(open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_ChainOccurRainfallSymbol + str(h_year) + ".csv", 'r', encoding='shift_jis'))
            a_csv_data1 = [ v for v in a_csv_obj1]

            # 結果出力ファイルを開く。
            # 全ての行をメモリに退避する。
            a_textSum2 = 0
            a_textline2 = []
            '''
            a_sr = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_OccurRainfallSymbol + str(h_year) + ".csv", 'r', encoding='shift_jis')
            a_line = a_sr.readline().rstrip('\r\n')
            while a_line:
                a_textline2.append(a_line)
                a_textSum2 += 1
                a_line = a_sr.readline().rstrip('\r\n')
            a_sr.close()
            #print('a_textSum2=' + str(a_textSum2))
            '''
            a_csv_obj2 = csv.reader(open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_OccurRainfallSymbol + str(h_year) + ".csv", 'r', encoding='shift_jis'))
            a_csv_data2 = [ v for v in a_csv_obj2]

            # 一連の降雨のみファイルを開く
            a_sw = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_ChainOnlyOccurRainfallSymbol + str(h_year) + ".csv", 'w', encoding='shift_jis')
            '''
            # 1行目は読み飛ばす。
            a_split1 = a_textline1[0].split(',')
            a_split2 = a_textline2[0].split(',')
            '''
            a_split1 = a_csv_data1[0]
            a_split2 = a_csv_data2[0]
            # 災害発生降雨数を書き込んでおく。
            # 気温情報を書き込む。
            a_sw.write('データ番号,非発生降雨のデータ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,' + str(int(a_split1[9]) - int(a_split2[9])) + self.com.SetTemperatureInfo() + '\n')
            a_cnt1 = 1
            a_cnt_next = 1
            '''
            while (a_cnt1 < a_textSum1):   #for a_cnt1 in range(1, a_textSum1):
                a_split1 = a_textline1[a_cnt1].split(',')
                '''
            for a_cnt1 in range(1, len(a_csv_data1)):
                a_split1 = a_csv_data1[a_cnt1]
                a_IsFound = False
                '''
                for a_cnt2 in range(a_cnt_next, a_textSum2):
                    a_split2 = a_textline2[a_cnt2].split(',')
                    '''
                for a_cnt2 in range(a_cnt_next, len(a_csv_data2)):
                    a_split2 = a_csv_data2[a_cnt2]
                    #if (a_split1[2] == a_split2[2]) and (a_split1[3] == a_split2[3]) and (a_split1[4] == a_split2[4]) and (a_split1[5] == a_split2[5]):
                    if (a_split1[2:5] == a_split2[2:5]):
                        a_cnt_next = a_cnt2 + 1
                        a_IsFound = True
                        break

                if (a_IsFound == False):
                    a_sw.write(a_split1[0] + "," + str(a_cnt1) + "," + a_split1[2] + "," + a_split1[3] + "," + a_split1[4] + "," + a_split1[5] + "," + a_split1[6] + "," + a_split1[7] + "," + a_split1[8] + '\n')
                a_cnt1 += 1
            a_sw.close()
            #print('end')

            del a_csv_data1[:]
            del a_csv_data2[:]
            gc.collect()
            a_csv_obj1 = None
            a_csv_obj2 = None

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeChainOnlyOccurRainFallDataByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeChainOnlyOccurRainFallDataByMesh", a_strErr + "," + sys.exc_info())

    # メッシュ単位のRBFNツール用非発生降雨データを自動検出する
    def _makeNonOccurRainFallDataByMesh(self, h_year, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeNonOccurRainFallDataByMesh', a_strErr)

        try:
            a_sw = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_NonOccurRainfallSymbol + str(h_year) + ".csv", 'w',encoding='shift_jis')
            a_sw.write('データ番号,RBFN用非発生降雨のデータ番号,年,月,日,時,解析雨量,土壌雨量指数,気温' + self.com.SetTemperatureInfo() + '\n')
            a_cnt = 0
            # 発生降雨フラグが'*'以外のものを抽出する
            for a_row in self.com.g_textline_FindOccurRainfall[
                        (self.com.g_textline_FindOccurRainfall['発生降雨フラグ'] == self.com.g_textline_FindOccurRainfall['発生降雨フラグ']) == False
                        ].iterrows():
                a_split = a_row[1]
                a_cnt += 1
                # 発生降雨フラグがない場合
                a_sw.write(a_split[0] + "," + str(a_cnt) + "," + a_split[1] + "," + a_split[2] + "," + a_split[3] + "," + a_split[4] + "," + a_split[5] + "," + a_split[6] + "," + a_split[7] + '\n')

            a_sw.close()
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeNonOccurRainFallDataByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeNonOccurRainFallDataByMesh", a_strErr + "," + sys.exc_info())

    # メッシュ単位の発生降雨データを自動検出する
    def _makeOccurRainFallDataByMesh(self, h_year, h_kind, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",kind=" + str(h_kind) + ",meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeOccurRainFallDataByMesh', a_strErr)

        try:
            # 結果出力ファイルを開く。
            a_sFileName = ""
            # ⑧予測適中率
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindOccurRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_FindOccurRainfall0Symbol + str(h_year) + ".csv"

            # 土壌雨量指数ファイルを開く。
            # ⑧予測適中率
            if (h_kind == 0):
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_OccurRainfallSymbol + str(h_year) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_OccurRainfall0Symbol + str(h_year) + ".csv"

            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_prev_DataNo = 0
            a_cnt = 0
            a_outLine = []
            a_rainSum = 0
            #print('self.com.g_textSum_FindOccurRainfall=' + str(self.com.g_textSum_FindOccurRainfall))

            # 発生降雨フラグが'*'のものｗ抽出する
            for a_row in self.com.g_textline_FindOccurRainfall[
                        (self.com.g_textline_FindOccurRainfall['発生降雨フラグ'] == self.com.g_textline_FindOccurRainfall['発生降雨フラグ']) &
                        (self.com.g_textline_FindOccurRainfall['発生降雨フラグ'] == '*')
                        ].iterrows():
                a_split = a_row[1]
                a_now_DataNo = int(a_split[0])  # データ番号

                a_cnt += 1

                # 発生降雨フラグがある場合
                a_outLine.append(a_split[0] + "," + str(a_cnt) + "," + a_split[1] + "," + a_split[2] + "," + a_split[3] + "," + a_split[4] + "," + a_split[5] + "," + a_split[6] + "," + a_split[7])
                if (a_prev_DataNo == 0):
                    a_rainSum += 1
                else:
                    if ((a_prev_DataNo + 1) < a_now_DataNo):
                        a_rainSum += 1

                a_prev_DataNo = a_now_DataNo

            a_sw.write('データ番号,災害発生降雨のデータ番号,年,月,日,時,解析雨量,土壌雨量指数,気温,' + str(a_rainSum) + self.com.SetTemperatureInfo() + '\n')
            for a_cnt2 in range(0, a_cnt):
                a_sw.write(a_outLine[a_cnt2] + '\n')

            # ファイルをクローズする。
            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeOccurRainFallDataByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeOccurRainFallDataByMesh", a_strErr + "," + sys.exc_info())

    # メッシュ単位のRBFN入力データを自動検出する
    def _makeRBFNDataByMesh(self, h_year, h_meshNo):
        a_strErr = "Year=" + str(h_year) + ",meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeRBFNDataByMesh', a_strErr)

        try:
            a_textSum = 0
            a_textline =[]

            # 一連の降雨から災害発生降雨を除外したCOOファイルを使用する
            #a_sr = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_NonOccurRainfallSymbol + str(h_year) + ".csv", 'r', encoding='shift_jis')
            a_csv_obj = csv.reader(open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + self.com.g_NonOccurRainfallSymbol + str(h_year) + ".csv", 'r', encoding='shift_jis'))
            a_csv_data = [ v for v in a_csv_obj]

            # 土壌雨量指数ファイルを開く
            a_sw = open(self.com.g_OutPath + "\\" + str(h_meshNo) + "\\" + str(h_year) + ".txt", 'w', encoding='shift_jis')
            a_textSum = 0
            '''
            # 1行目は読み飛ばす。
            a_writeline = a_sr.readline().rstrip('\r\n')
            a_writeline = a_sr.readline().rstrip('\r\n')
            while a_writeline:
                a_textline.append(a_writeline)
                a_textSum += 1
                a_writeline = a_sr.readline().rstrip('\r\n')
            a_sw.write(str(a_textSum) + '\n')
                '''

            a_sw.write(str(len(a_csv_data) - 1) + '\n')

            '''        
            for a_cnt in range(0, a_textSum):
                a_split = a_textline[a_cnt].split(',')
                '''
            for a_cnt in range(1, len(a_csv_data)):
                a_split = a_csv_data[a_cnt]
                a_sw.write(a_split[6].rjust(5, ' ') + a_split[7].rjust(7, ' ') + '\n')

            a_sw.close()
            #a_sr.close()

            del a_csv_data[:]
            gc.collect()
            a_csv_obj = None

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeRBFNDataByMesh", a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, "_makeRBFNDataByMesh", a_strErr + "," + sys.exc_info())

