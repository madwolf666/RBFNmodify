################################################################################
# 集計
################################################################################
import sys
import os
import datetime
import math
import csv
import com_functions
import threading
import gc

# 警報発表頻度を作成する
class MakeAlarmAnnounce():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeAlarmAnnounce-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverAllRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverAllRainfallFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_AlarmAnnounceSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_AlarmAnnounceSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,対象期間(年),現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            # 該当メッシュの対象期間を算出する
            a_tyear = self.com.GetTargetYearByMesh(self.com.g_TargetStartYear, self.com.g_TargetEndYear, self.com.g_OutPath, self.meshList[0])
            a_tyear = int(self.com.My_round(a_tyear, 0))
            for a_cnt1 in range(1, self.com.g_textSum_OverAllRainfallFile):
                a_split1 = self.com.g_textline_OverAllRainfallFile[a_cnt1]
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                for a_cnt2 in range(1, 10):
                    if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                        if (float(a_split1[a_cnt2]) != 0):
                            if (a_tyear > 0):
                                a_sTmp = str(self.com.My_round((float(a_split1[a_cnt2]) / a_tyear), 2))
                                #a_sTmp = '%10.2f' % ((float(a_split1[a_cnt2]) / a_tyear) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            a_sTmp = "0"
                    else:
                        a_sTmp = a_split1[a_cnt2]
                    a_writeline += "," + a_sTmp
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        a_sCL = "-,-"
                    else:
                        # 既往CL取込あり
                        if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                            a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + str(a_tyear)
                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverAllRainfallFile[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeAlarmAnnounce-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeAlarmAnnounce-run', a_strErr + "," + sys.exc_info())

# 発表頻度を作成する
class MakeCautionAnnounceFrequencyOverOccurRainFallNum():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeCautionAnnounceFrequencyOverOccurRainFallNum-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurRainFallNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurRainFallNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_CautionAnnouncOccurRainfalleFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_CautionAnnouncOccurRainfalleFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceFrequencyOverOccurRainFallNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceFrequencyOverOccurRainFallNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,警戒発表した降雨数,対象期間,発表頻度" + a_TemperatureInfo + "\n")

            # 対象期間（年）を取得
            a_tyear = self.com.GetTargetYearByMesh(self.com.g_TargetStartYear, self.com.g_TargetEndYear, self.com.g_OutPath, self.meshList[0])
            a_tyear = int(self.com.My_round(a_tyear, 0))

            for a_cnt1 in range(1, self.com.g_textSum_CautionAnnouncOccurRainfalleFile):
                a_split1 = self.com.g_textline_CautionAnnouncOccurRainfalleFile[a_cnt1]
                '''
                # 対象期間（年）を取得
                a_tyear = self.com.GetTargetYearByMesh(self.com.g_TargetStartYear, self.com.g_TargetEndYear, self.com.g_OutPath, a_split1[0])
                a_tyear = int(self.com.My_round(a_tyear, 0))
                '''
                a_writeline = a_split1[0]
                if (a_tyear > 0):
                    for a_cnt2 in range(1, 2):
                        if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                            if (float(a_split1[a_cnt2]) != 0):
                                a_writeline += "," + str(a_split1[a_cnt2])
                                a_writeline += "," + str(int(a_tyear))
                                a_writeline += "," + str(self.com.My_round((float(a_split1[a_cnt2]) / a_tyear), 2))
                                #a_writeline += "," + "%10.2f" % ((float(a_split1[a_cnt2]) / a_tyear) * 100)
                            else:
                                a_writeline += ",0"
                                a_writeline += "," + str(int(a_tyear))
                                a_writeline += ",0"
                        else:
                            a_writeline += ",0"
                            a_writeline += "," + str(int(a_tyear))
                            a_writeline += ",0"
                else:
                    a_writeline += ",0"
                    a_writeline += "," + str(int(a_tyear))
                    a_writeline += ",0"

                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_CautionAnnouncOccurRainfalleFile[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeCautionAnnounceFrequencyOverOccurRainFallNum-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeCautionAnnounceFrequencyOverOccurRainFallNum-run', a_strErr + "," + sys.exc_info())

# 災害捕捉率を作成する
class MakeCautionAnnounceRateOccurNum():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeCautionAnnounceRateOccurNum-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_CautionAnnouncOccurFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_CautionAnnouncOccurFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceRateOccurNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceRateOccurNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,警戒発表中の発生件数,発生件数,災害捕捉率" + a_TemperatureInfo + "\n")

            for a_cnt1 in range(1, self.com.g_textSum_CautionAnnouncOccurFile):
                a_split1 = self.com.g_textline_CautionAnnouncOccurFile[a_cnt1]
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_split1[0])
                a_writeline = a_split1[0]
                if (a_occurSum != 0):
                    for a_cnt2 in range(1, 2):
                        if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                            if (float(a_split1[a_cnt2]) != 0):
                                a_writeline += "," + str(a_split1[a_cnt2])
                                a_writeline += "," + str(a_occurSum)
                                a_writeline += "," + str(self.com.My_round((float(a_split1[a_cnt2]) / a_occurSum) * 100, 2))
                                #a_writeline += "," + "%3.2f" % ((float(a_split1[a_cnt2]) / a_occurSum) * 100)
                            else:
                                a_writeline += ",0"
                                a_writeline += "," + str(a_occurSum)
                                a_writeline += ",0"
                        else:
                            a_writeline += ",無し"
                            a_writeline += "," + str(a_occurSum)
                            a_writeline += ",無し"
                else:
                    a_writeline += ",無し"
                    a_writeline += "," + str(a_occurSum)
                    a_writeline += ",無し"

                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_CautionAnnouncOccurFile[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeCautionAnnounceRateOccurNum-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeCautionAnnounceRateOccurNum-run', a_strErr + "," + sys.exc_info())

# 災害捕捉率を作成する
class MakeCautionAnnounceRateOccurRainFallNum():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeCautionAnnounceRateOccurRainFallNum-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurRainFallNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurRainFallNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_CautionAnnouncOccurRainfalleFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_CautionAnnouncOccurRainfalleFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceRateOverOccurRainFallNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceRateOverOccurRainFallNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,警戒発表中の発生降雨数,発生降雨数,災害捕捉率" + a_TemperatureInfo + "\n")

            for a_cnt1 in range(1, self.com.g_textSum_CautionAnnouncOccurRainfalleFile):
                a_split1 = self.com.g_textline_CautionAnnouncOccurRainfalleFile[a_cnt1]
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_split1[0])
                a_writeline = a_split1[0]
                if (a_occurSum != 0):
                    for a_cnt2 in range(1, 2):
                        if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                            if (float(a_split1[a_cnt2]) != 0):
                                a_writeline += "," + str(a_split1[a_cnt2])
                                a_writeline += "," + str(a_occurSum)
                                a_writeline += "," + str(self.com.My_round((float(a_split1[a_cnt2]) / a_occurSum) * 100, 2))
                                #a_writeline += "," + "%3.2f" % ((float(a_split1[a_cnt2]) / a_occurSum) * 100)
                            else:
                                a_writeline += ",0"
                                a_writeline += "," + str(a_occurSum)
                                a_writeline += ",0"
                        else:
                            a_writeline += ",無し"
                            a_writeline += "," + str(a_occurSum)
                            a_writeline += ",無し"
                else:
                    a_writeline += ",無し"
                    a_writeline += "," + str(a_occurSum)
                    a_writeline += ",無し"

                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_CautionAnnouncOccurRainfalleFile[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeCautionAnnounceRateOccurRainFallNum-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeCautionAnnounceRateOccurRainFallNum-run', a_strErr + "," + sys.exc_info())

# 災害捕捉率を作成する
class MakeDisasterSupplement():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeDisasterSupplement-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverOccurRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverOccurRainfallFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_DisasterSupplementSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_DisasterSupplementSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,発生降雨数,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            for a_cnt1 in range(1, self.com.g_textSum_OverOccurRainfallFile):
                a_split1 = self.com.g_textline_OverOccurRainfallFile[a_cnt1]
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_split1[0])
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                if (a_occurSum != 0):
                    for a_cnt2 in range(1, 10):
                        if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                            if (float(a_split1[a_cnt2]) != 0):
                                a_sTmp = str(self.com.My_round((float(a_split1[a_cnt2]) / a_occurSum) * 100, 2))
                                #a_sTmp = '%3.1f' % ((float(a_split1[a_cnt2]) / a_occurSum) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            if (self.com.g_PastKind == 0):
                                # 既往CL取り込みなし
                                a_sTmp = "無し"
                            else:
                                # 既往CL取り込みあり
                                a_sTmp = a_split1[a_cnt2]
                        a_writeline += "," + a_sTmp
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL = "-,-"
                        else:
                            # 既往CL取込あり
                            if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                                a_sCL = a_sTmp + "," + a_split1[11]
                else:
                    for a_cnt2 in range(1, 10):
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sTmp = "無し"
                        else:
                            # 既往CL取込あり
                            if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                                a_sTmp = "無し"
                            else:
                                a_sTmp = a_split1[a_cnt2]
                        a_writeline += "," + a_sTmp
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL = "-,-"
                        else:
                            # 既往CL取込あり
                            if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                                a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + str(a_occurSum)
                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverOccurRainfallFile[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeDisasterSupplement-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeDisasterSupplement-run', a_strErr + "," + sys.exc_info())

# 災害捕捉率を作成する
class MakeDisasterSupplement9_1():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeDisasterSupplement9_1-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_1SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_1Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverOccurRainfall9_1File = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverOccurRainfall9_1File)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_DisasterSupplement9_1SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_DisasterSupplement9_1Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,発生降雨数,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            for a_cnt1 in range(1, self.com.g_textSum_OverOccurRainfall9_1File):
                a_split1 = self.com.g_textline_OverOccurRainfall9_1File[a_cnt1]
                # 該メッシュの災害発生件数を取得
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_split1[0])
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                if (a_occurSum != 0):
                    for a_cnt2 in range(1, 10):
                        if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                            if (float(a_split1[a_cnt2]) != 0):
                                a_sTmp = str(self.com.My_round((float(a_split1[a_cnt2]) / a_occurSum) * 100, 2))
                                #a_sTmp = '%3.2f' % ((float(a_split1[a_cnt2]) / a_occurSum) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            if (self.com.g_PastKind == 0):
                                a_strTmp = "無し"
                            else:
                                a_sTmp = a_split1[a_cnt2]
                        a_writeline += "," + a_sTmp
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL = "-,-"
                        else:
                            # 既往CL取込あり
                            if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                                a_sCL = a_sTmp + "," + a_split1[11]
                else:
                    for a_cnt2 in range(1, 10):
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sTmp = "無し"
                        else:
                            # 既往CL取込あり
                            if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                                a_sTmp = "無し"
                            else:
                                a_sTmp = a_split1[a_cnt2]
                        a_writeline += "," + a_sTmp
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL = "-,-"
                        else:
                            # 既往CL取込あり
                            if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                                a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + str(a_occurSum)
                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverOccurRainfall9_1File[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeDisasterSupplement9_1-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeDisasterSupplement9_1-run', a_strErr + "," + sys.exc_info())

# 災害捕捉率を作成する
class MakeDisasterSupplement9_2():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeDisasterSupplement9_2-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_2SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_2Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverOccurRainfall9_2File = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverOccurRainfall9_2File)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_DisasterSupplement9_2SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_DisasterSupplement9_2Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,災害発生件数,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            for a_cnt1 in range(1, self.com.g_textSum_OverOccurRainfall9_2File):
                a_split1 = self.com.g_textline_OverOccurRainfall9_2File[a_cnt1]
                # 該メッシュの災害発生件数を取得
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_split1[0])
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                if (a_occurSum != 0):
                    for a_cnt2 in range(1, 10):
                        if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                            if (float(a_split1[a_cnt2]) != 0):
                                a_sTmp = str(self.com.My_round((float(a_split1[a_cnt2]) / a_occurSum) * 100, 2))
                                #a_sTmp = '%3.2f' % ((float(a_split1[a_cnt2]) / a_occurSum) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            if (self.com.g_PastKind == 0):
                                a_strTmp = "無し"
                            else:
                                a_sTmp = a_split1[a_cnt2]
                        a_writeline += "," + a_sTmp
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL = "-,-"
                        else:
                            # 既往CL取込あり
                            if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                                a_sCL = a_sTmp + "," + a_split1[11]
                else:
                    for a_cnt2 in range(1, 10):
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sTmp = "無し"
                        else:
                            # 既往CL取込あり
                            if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                                a_sTmp = "無し"
                            else:
                                a_sTmp = a_split1[a_cnt2]
                        a_writeline += "," + a_sTmp
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL = "-,-"
                        else:
                            # 既往CL取込あり
                            if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                                a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + str(a_occurSum)
                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverOccurRainfall9_2File[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeDisasterSupplement9_2-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeDisasterSupplement9_2-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeForecastPredictive():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        #self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeForecastPredictive-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_overSum = 0
        a_overRBFNTime = []
        a_occurTime = []
        a_overRBFNVal = []

        a_prevMsno = ""
        a_msSum = 0
        a_msNo = [0]
        a_FSum = [[0]*9]
        a_PSum = [[0]*9]

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime1SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime1Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_CalcForecastTime1File = self.com.Store_DataFile(a_sFileName, self.com.g_textline_CalcForecastTime1File)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime0SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime0Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_CalcForecastTime0File = self.com.Store_DataFile(a_sFileName, self.com.g_textline_CalcForecastTime0File)

            if (self.soilMin > 0):
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastPredictiveSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastPredictiveSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')

            a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastPredictiveSymbol + "【ブロック】-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_swB = open(a_sFileName, 'w', encoding='shift_jis')

            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,CL" + a_TemperatureInfo + "\n")
            a_swB.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,CL" + a_TemperatureInfo + "\n")

            for a_cnt1 in range(1, self.com.g_textSum_CalcForecastTime1File):
                # 予測と実況の行の並びが同じである必要あり。
                a_split1 = self.com.g_textline_CalcForecastTime1File[a_cnt1]
                a_split2 = self.com.g_textline_CalcForecastTime0File[a_cnt1]

                if (a_prevMsno != ""):
                    # 既に処理中のメッシュあり
                    if (a_prevMsno != a_split1[0]):
                        # 次のメッシュ
                        if (a_msSum > 0):
                            a_msNo.append('')
                            a_FSum.append([0]*9)
                            a_PSum.append([0]*9)
                        a_msSum += 1
                        a_msNo[a_msSum -1] = a_split1[0]
                else:
                    # 最初のメッシュ
                    if (a_msSum > 0):
                        a_msNo.append('')
                        a_FSum.append([0]*9)
                        a_PSum.append([0]*9)
                    a_msSum += 1
                    a_msNo[a_msSum - 1] = a_split1[0]
                a_prevMsno = a_split1[0]

                # 予測時間と実況時間を比較
                for a_cnt2 in range(1, 10):
                    if (a_split1[a_cnt2] != ""):
                        # 予測超過数を設定
                        a_FSum[a_msSum - 1][a_cnt2 - 1] += 1
                        # 予測時刻計算
                        # 時刻は加算しなくても良い↓
                        a_tTmp = datetime.datetime.strptime(a_split1[a_cnt2], "%Y/%m/%d %H:%M")
                        if (a_split2[a_cnt2] != ""):
                            # 予測時間と実測時間を比較
                            a_tTmp2 = datetime.datetime.strptime(a_split2[a_cnt2], "%Y/%m/%d %H:%M")
                            if (a_tTmp2 > a_tTmp):
                                # 予測適中
                                a_PSum[a_msSum - 1][a_cnt2 - 1] += 1

            for a_cnt1 in range(0, a_msSum):
                # メッシュ番号
                a_writeline = a_msNo[a_cnt1]

                a_RBFN = 0
                a_soilMin = 0
                a_rainMax = -1

                if (self.com.g_PastKind != 0):
                    # 取込あり
                    a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(a_msNo[a_cnt1])    # 60分間積算雨量上限値のサポート
                    if (self.soilMin > 0) or (self.rainMax > 0):
                        a_soilMin = self.soilMin
                        a_rainMax = self.rainMax

                a_sTmp = ""
                a_sCL1 = ""
                # 予測適中率
                for a_cnt2 in range(0, 9):
                    if (a_PSum[a_cnt1][a_cnt2] > 0) and (a_FSum[a_cnt1][a_cnt2] > 0):
                        a_sTmp = str(self.com.My_round((float(a_PSum[a_cnt1][a_cnt2]) / float(a_FSum[a_cnt1][a_cnt2])) * 100, 2))
                        #a_sTmp = "%3.1f" % ((float(a_PSum[a_cnt1][a_cnt2]) / float(a_FSum[a_cnt1][a_cnt2])) * 100)
                    else:
                        a_sTmp = "0"
                    a_writeline += "," + a_sTmp
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        a_sCL1 = "-"
                    else:
                        # 既往CL取込あり
                        if (a_cnt2 == a_RBFN):
                            a_sCL1 = str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1))

                # 予測超過数
                for a_cnt2 in range(0, 9):
                    a_sTmp = str(a_FSum[a_cnt1][a_cnt2])
                    a_writeline += "," + a_sTmp

                # 適中数
                for a_cnt2 in range(0, 9):
                    a_sTmp = str(a_PSum[a_cnt1][a_cnt2])
                    a_writeline += "," + a_sTmp

                a_writeline += "," + a_sCL1
                a_sw.write(a_writeline  + "\n")
                a_swB.write(a_writeline + "\n")

            a_sw.close()
            a_swB.close()

            del self.com.g_textline_CalcForecastTime1File[:]
            del self.com.g_textline_CalcForecastTime0File[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeForecastPredictive-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeForecastPredictive-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeNIGeDaS():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfall3_2-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_overSum = 0
        a_overRBFNTime = []
        a_occurTime = []
        a_overRBFNVal = []

        a_soilIdx = 0

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0][1])

            for a_index, a_meshNo in self.meshList:
                a_RBFN = -1

                # 既往CLの取り込み
                if (self.com.g_PastKind == 0):
                    # 取込なし
                    a_surfaceFile = self.com.g_RBFNOutPath + "\\" + "surface-" + a_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    # 取込あり
                    a_surfaceFile = self.com.g_PastRBFNOutPath + "\\" + "surface-" + self.com.GetTargetMeshNoByCL(self.com.g_TargetStartYear, a_meshNo) + "-" + str(self.com.g_PastTargetStartYear) + "-" + str(self.com.g_PastTargetEndYear) + ".csv"
                    a_RBFN, a_soilMin, a_rainMax =  self.com.GetPastCLData(a_meshNo)    # 60分間積算雨量上限値のサポート
                    if (self.soilMin > 0) or (self.rainMax > 0):
                        a_soilMin = self.soilMin
                        a_rainMax = self.rainMax
                self.com.g_textSum_SurfaceFile = self.com.Store_DataFile(a_surfaceFile, self.com.g_textline_SurfaceFile)
                self.com.g_textSum_ContourReviseByMesh = self.com.Store_DataFile(self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + a_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", self.com.g_textline_ContourReviseByMesh)

                if (self.soilMin > 0):
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaSSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaSSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw = open(a_sFileName, 'w', encoding='shift_jis')
                a_sw.write("年,月,日,時,雨量,土壌雨量指数,RBFN出力値,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

                if (self.soilMin > 0):
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaS2SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaS2Symbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw2 = open(a_sFileName, 'w', encoding='shift_jis')
                a_sw2.write("年,月,日,時,雨量,土壌雨量指数,RBFN出力値,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

                for a_cnt2 in range(self.com.g_TargetStartYear, self.com.g_TargetEndYear + 1):
                    self.g_textSum_OccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_OccurRainfallSymbol + str(a_cnt2) + ".csv", self.com.g_textline_OccurRainfallFile)
                    for a_cnt3 in range(1, self.g_textSum_OccurRainfallFile):
                        a_splitO = self.com.g_textline_OccurRainfallFile[a_cnt3]
                        a_isFound = False
                        a_splitS = self.com.g_textline_SurfaceFile[0]
                        a_sCL = ""
                        for a_cnt4 in range(1, self.com.g_textSum_SurfaceFile):
                            if (float(a_splitS[a_cnt4]) >= float(a_splitO[7])):
                                a_isFound = True

                                if (a_isFound == True):
                                    a_soilIdx = a_cnt4

                                break

                        if (a_isFound == True):
                            a_isFound = False
                            for a_cnt4 in range(1, self.com.g_textSum_SurfaceFile):
                                a_splitS = self.com.g_textline_SurfaceFile[a_cnt4]
                                if (float(a_splitS[0]) >= float(a_splitO[6])):
                                    # 雨量検出
                                    # NIGeDaS
                                    a_sw.write(
                                        a_splitO[2] + "," + a_splitO[3] + "," + a_splitO[4] + "," + a_splitO[5] + "," +
                                        a_splitO[6] + "," + a_splitO[7] + "," + a_splitS[a_soilIdx] +
                                        self.com.CalcNIGeDaS(a_splitS[a_soilIdx], a_RBFN) +
                                        "\n"
                                    )
                                    # NIGeDaSⅡ
                                    a_sw2.write(
                                        a_splitO[2] + "," + a_splitO[3] + "," + a_splitO[4] + "," + a_splitO[5] + "," +
                                        a_splitO[6] + "," + a_splitO[7] + "," + a_splitS[a_soilIdx] +
                                        self.com.CalcNIGeDaS2(
                                            self.com.g_textSum_SurfaceFile,
                                            self.com.g_textline_SurfaceFile,
                                            self.com.g_textSum_ContourReviseByMesh,
                                            self.com.g_textline_ContourReviseByMesh,
                                            a_splitO[6],
                                            a_splitO[7],
                                            a_RBFN
                                        ) +
                                        "\n"
                                    )
                                    a_isFound = True
                                    break

                    del self.com.g_textline_OccurRainfallFile[:]
                    gc.collect()

                a_sw.close()
                a_sw2.close()

                del self.com.g_textline_SurfaceFile[:]
                del self.com.g_textline_ContourReviseByMesh[:]
                gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeNIGeDaS-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeNIGeDaS-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeNIGeDaS_NonOccurCalc():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeNIGeDaS_NonOccurCalc-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_overSum = 0
        a_overRBFNTime = []
        a_occurTime = []
        a_overRBFNVal = []

        a_soilIdx = 0

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0][1])

            for a_index, a_meshNo in self.meshList:
                a_RBFN = -1

                # 既往CLの取り込み
                if (self.com.g_PastKind == 0):
                    # 取込なし
                    a_surfaceFile = self.com.g_RBFNOutPath + "\\" + "surface-" + a_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    # 取込あり
                    a_surfaceFile = self.com.g_PastRBFNOutPath + "\\" + "surface-" + self.com.GetTargetMeshNoByCL(self.com.g_TargetStartYear, a_meshNo) + "-" + str(self.com.g_PastTargetStartYear) + "-" + str(self.com.g_PastTargetEndYear) + ".csv"
                    a_RBFN, a_soilMin, a_rainMax =  self.com.GetPastCLData(a_meshNo)    # 60分間積算雨量上限値のサポート
                    if (self.soilMin > 0) or (self.rainMax > 0):
                        a_soilMin = self.soilMin
                        a_rainMax = self.rainMax
                self.com.g_textSum_SurfaceFile = self.com.Store_DataFile(a_surfaceFile, self.com.g_textline_SurfaceFile)
                self.com.g_textSum_ContourReviseByMesh = self.com.Store_DataFile(self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + a_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", self.com.g_textline_ContourReviseByMesh)

                if (self.soilMin > 0):
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaSSoilMinSymbol + "【非発生降雨】-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaSSymbol + "【非発生降雨】-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw = open(a_sFileName, 'w', encoding='shift_jis')
                a_sw.write("年,月,日,時,雨量,土壌雨量指数,RBFN出力値,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

                if (self.soilMin > 0):
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaS2SoilMinSymbol + "【非発生降雨】-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "-" + self.com.g_NIGeDaS2Symbol + "【非発生降雨】-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw2 = open(a_sFileName, 'w', encoding='shift_jis')
                a_sw2.write("年,月,日,時,雨量,土壌雨量指数,RBFN出力値,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

                for a_cnt2 in range(self.com.g_TargetStartYear, self.com.g_TargetEndYear + 1):
                    self.g_textSum_ChainOccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_ChainOnlyOccurRainfallSymbol + str(a_cnt2) + ".csv", self.com.g_textline_ChainOccurRainfallFile)
                    for a_cnt3 in range(1, self.g_textSum_ChainOccurRainfallFile):
                        a_splitO = self.com.g_textline_ChainOccurRainfallFile[a_cnt3]
                        a_isFound = False
                        a_splitS = self.com.g_textline_SurfaceFile[0]
                        a_sCL = ""
                        for a_cnt4 in range(1, self.com.g_textSum_SurfaceFile):
                            if (float(a_splitS[a_cnt4]) >= float(a_splitO[7])):
                                a_isFound = True

                                if (a_isFound == True):
                                    a_soilIdx = a_cnt4

                                break

                        if (a_isFound == True):
                            a_isFound = False
                            for a_cnt4 in range(1, self.com.g_textSum_SurfaceFile):
                                a_splitS = self.com.g_textline_SurfaceFile[a_cnt4]
                                if (float(a_splitS[0]) >= float(a_splitO[6])):
                                    # 雨量検出
                                    # NIGeDaS
                                    a_sw.write(
                                        a_splitO[2] + "," + a_splitO[3] + "," + a_splitO[4] + "," + a_splitO[5] + "," +
                                        a_splitO[6] + "," + a_splitO[7] + "," + a_splitS[a_soilIdx] +
                                        self.com.CalcNIGeDaS(a_splitS[a_soilIdx], a_RBFN) +
                                        "\n"
                                    )
                                    # NIGeDaSⅡ
                                    a_sw2.write(
                                        a_splitO[2] + "," + a_splitO[3] + "," + a_splitO[4] + "," + a_splitO[5] + "," +
                                        a_splitO[6] + "," + a_splitO[7] + "," + a_splitS[a_soilIdx] +
                                        self.com.CalcNIGeDaS2(
                                            self.com.g_textSum_SurfaceFile,
                                            self.com.g_textline_SurfaceFile,
                                            self.com.g_textSum_ContourReviseByMesh,
                                            self.com.g_textline_ContourReviseByMesh,
                                            a_splitO[6],
                                            a_splitO[7],
                                            a_RBFN
                                        ) +
                                        "\n"
                                    )
                                    a_isFound = True
                                    break

                    del self.com.g_textline_ChainOccurRainfallFile[:]
                    gc.collect()

                a_sw.close()
                a_sw2.close()

                del self.com.g_textline_SurfaceFile[:]
                del self.com.g_textline_ContourReviseByMesh[:]
                gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeNIGeDaS_NonOccurCalc-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeNIGeDaS_NonOccurCalc-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeOverRainfall2():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_DisasterFile,
                 h_CautionAnnounceFile,
                 h_meshList,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        if(h_DisasterFile != None):
            del self.com.g_textline_DisasterFile[:]
            gc.collect()
            self.com.g_textline_DisasterFile = h_DisasterFile[:].split("\n")
            self.com.g_textSum_DisasterFile = len(self.com.g_textline_DisasterFile)

        if(h_CautionAnnounceFile != None):
            del self.com.g_textline_CautionAnnounceFile[:]
            gc.collect()
            self.com.g_textline_CautionAnnounceFile = h_CautionAnnounceFile[:].split("\n")
            self.com.g_textSum_CautionAnnounceFile = len(self.com.g_textline_CautionAnnounceFile)

        '''
        self.com.g_textSum_DisasterFile = self.com.Store_DataFile(self.com.g_DisasterFileName, self.com.g_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile = self.com.Store_DataFile(self.com.g_CautionAnnounceFileName, self.com.g_textline_CautionAnnounceFile)
        '''

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfall2-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0][1])
            a_RBFN = 0
            for a_index, a_meshNo in self.meshList:
                # 既往CLの取り込み
                if (self.com.g_PastKind != 0):
                    # 取込あり
                    a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(a_meshNo)    # 60分間積算雨量上限値のサポート
                    if (self.soilMin > 0) or (self.rainMax > 0):
                        a_soilMin = self.soilMin
                        a_rainMax = self.rainMax

                # 発生降雨数を取得する
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_meshNo)

                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_OverRainfallNumByMeshSoilMinSymbol2 + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_OverRainfallNumByMeshSymbol2 + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw = open(a_sFileName, 'w', encoding='shift_jis')
                #self.com.g_textSum_OverRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverRainfallFile)

                a_sw.write("メッシュNo.,any" + a_TemperatureInfo + "\n")

                a_iTmp = 0
                # ①土砂災害警戒情報の災害捕捉率
                # 土砂災害警戒情報発表中の発生降雨超過数を算出する。
                if (self.com.g_PastKind == 0):
                    # 取込みなし
                    a_iTmp = self._getCautionAnnounceOccurRainfallSum(a_meshNo, self.unReal, self.soilMin, self.rainMax)  # 60分積算雨量上限値の追加
                else:
                    # 取込あり
                    a_iTmp = self._getCautionAnnounceOccurRainfallSum(a_meshNo, self.unReal, a_soilMin, a_rainMax)
                # 土砂災害警戒情報発表中の発生降雨超過数
                a_sw.write(a_meshNo + "," + str(a_iTmp) + ",,,,,,,,\n")

                # 土砂災害警戒情報発表中の災害発生件数を算出する。
                if (self.com.g_PastKind == 0):
                    # 取込なし
                    a_iTmp = self._getCautionAnnounceOccurSum(a_meshNo, self.unReal, self.soilMin, self.rainMax) # 60分積算雨量上限値の追加
                else:
                    # 取込あり
                    a_iTmp = self._getCautionAnnounceOccurSum(a_meshNo, self.unReal, a_soilMin, a_rainMax)
                # 土砂災害警戒情報発表中の災害発生件数
                a_sw.write(a_meshNo + "," + str(a_iTmp) + ",,,,,,,,\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall2-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall2-run', a_strErr + "," + sys.exc_info())

    # 警戒発表中の発生降雨数を取得する
    def _getCautionAnnounceOccurRainfallSum(
            self,
            h_meshNo,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getCautionAnnounceOccurRainfallSum', a_strErr)

        a_iRet = 0
        a_IsExists = False
        a_OccurT = [None]*2

        try:
            for a_cntN in range(self.com.g_TargetStartYear, self.com.g_TargetEndYear + 1):
                self.g_textSum_OccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_OccurRainfallSymbol + str(a_cntN) + ".csv", self.com.g_textline_OccurRainfallFile)
                a_prevTime = ""
                for a_cntO1 in range(1, self.g_textSum_OccurRainfallFile):
                    a_split1 = self.com.g_textline_OccurRainfallFile[a_cntO1]
                    a_nowTime = a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5]
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
                    if (a_prevTime != ""):
                        if (a_prevTime != a_strTmp):
                            # 異なる一連の降雨となる
                            # 土砂災害警戒情報発表中の災害件数チェック
                            a_IsExists = False
                            for a_cnt in range(1, self.com.g_textSum_CautionAnnounceFile):
                                a_split = self.com.g_textline_CautionAnnounceFile[a_cnt].split(",")
                                if (a_split[0] == h_meshNo):
                                    # メッシュ番号が同じ
                                    a_sTime = datetime.datetime.strptime(a_split[1] + "/" + a_split[2] + "/" + a_split[3] + " " + a_split[4], '%Y/%m/%d %H:%M')
                                    a_eTime = datetime.datetime.strptime(a_split[5] + "/" + a_split[6] + "/" + a_split[7] + " " + a_split[8], '%Y/%m/%d %H:%M')
                                    for a_cntD in range(1, self.com.g_textSum_DisasterFile):
                                        a_splitD = self.com.g_textline_DisasterFile[a_cntD].split(",")
                                        if (a_splitD[0].strip() == h_meshNo):
                                            # メッシュ番号が同じ
                                            a_mTime = datetime.datetime.strptime(a_splitD[1] + "/" + a_splitD[2] + "/" + a_splitD[3] + " " + a_splitD[4], '%Y/%m/%d %H:%M')
                                            if (a_OccurT[0] != None) and (a_OccurT[1] != None):
                                                if (a_mTime >= a_OccurT[0]) and (a_mTime <= a_OccurT[1]):
                                                    # 災害が一連の降雨内である
                                                    # 警戒発表以前に災害発生
                                                    if (a_mTime < a_sTime):
                                                        a_IsExists = True
                                                        break
                                                    if (a_mTime >= a_sTime) and (a_mTime <= a_eTime):
                                                        # 年月日時が警戒発表の範囲内
                                                        a_iRet += 1
                                                        a_IsExists = True
                                                        break
                                    if (a_IsExists == True):
                                        break
                            a_OccurT[0] = datetime.datetime.strptime(a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5], '%Y/%m/%d %H:%M') # 開始
                    else:
                        a_OccurT[0] = datetime.datetime.strptime(a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5], '%Y/%m/%d %H:%M') # 開始

                    a_OccurT[1] = datetime.datetime.strptime(a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5], '%Y/%m/%d %H:%M') # 終了
                    a_prevTime = a_nowTime

                # 一連の降雨内での検出
                # 土砂災害警戒情報発表中の災害件数チェック
                a_IsExists = False
                for a_cnt in range(1, self.com.g_textSum_CautionAnnounceFile):
                    a_split = self.com.g_textline_CautionAnnounceFile[a_cnt].split(",")
                    if (a_split[0] == h_meshNo):
                        # メッシュ番号が同じ
                        a_sTime = datetime.datetime.strptime(a_split[1] + "/" + a_split[2] + "/" + a_split[3] + " " + a_split[4], '%Y/%m/%d %H:%M')
                        a_eTime = datetime.datetime.strptime(a_split[5] + "/" + a_split[6] + "/" + a_split[7] + " " + a_split[8], '%Y/%m/%d %H:%M')
                        for a_cntD in range(1, self.com.g_textSum_DisasterFile):
                            a_splitD = self.com.g_textline_DisasterFile[a_cntD].split(",")
                            if (a_splitD[0].strip() == h_meshNo):
                                # メッシュ番号が同じ
                                a_mTime = datetime.datetime.strptime(a_splitD[1] + "/" + a_splitD[2] + "/" + a_splitD[3] + " " + a_splitD[4], '%Y/%m/%d %H:%M')
                                if (a_OccurT[0] != None) and (a_OccurT[1] != None):
                                    if (a_mTime >= a_OccurT[0]) and (a_mTime <= a_OccurT[1]):
                                        # 災害が一連の降雨内である
                                        # 警戒発表以前に災害発生
                                        if (a_mTime < a_sTime):
                                            a_IsExists = True
                                            break
                                        if (a_mTime >= a_sTime) and (a_mTime <= a_eTime):
                                            # 年月日時が警戒発表の範囲内
                                            a_iRet += 1
                                            a_IsExists = True
                                            break
                        if (a_IsExists == True):
                            break

                del self.com.g_textline_OccurRainfallFile[:]
                gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getCautionAnnounceOccurRainfallSum', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getCautionAnnounceOccurRainfallSum', a_strErr + "," + sys.exc_info())

        return a_iRet

    # 警戒発表中の災害件数を取得する
    def _getCautionAnnounceOccurSum(
            self,
            h_meshNo,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getCautionAnnounceOccurSum', a_strErr)

        a_iRet = 0

        try:
            for a_cnt in range(1, self.com.g_textSum_CautionAnnounceFile):
                a_split = self.com.g_textline_CautionAnnounceFile[a_cnt].split(",")
                if (a_split[0] == h_meshNo):
                    # メッシュ番号が同じ
                    a_sTime = datetime.datetime.strptime(a_split[1] + "/" + a_split[2] + "/" + a_split[3] + " " + a_split[4], '%Y/%m/%d %H:%M')
                    a_eTime = datetime.datetime.strptime(a_split[5] + "/" + a_split[6] + "/" + a_split[7] + " " + a_split[8], '%Y/%m/%d %H:%M')
                    for a_cntD in range(1, self.com.g_textSum_DisasterFile):
                        a_splitD = self.com.g_textline_DisasterFile[a_cntD].split(",")
                        if (a_splitD[0].strip() == h_meshNo):
                            # メッシュ番号が同じ
                            a_mTime = datetime.datetime.strptime(a_splitD[1] + "/" + a_splitD[2] + "/" + a_splitD[3] + " " + a_splitD[4], '%Y/%m/%d %H:%M')
                            if (a_mTime >= a_sTime) and (a_mTime <= a_eTime):
                                # 年月日時が警戒発表の範囲内
                                a_iRet += 1

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getCautionAnnounceOccurSum', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getCautionAnnounceOccurSum', a_strErr + "," + sys.exc_info())

        return a_iRet

# 降雨超過数を作成する
class MakeOverRainfall3_1():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfall3_1-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0][1])

            for a_index, a_meshNo in self.meshList:
                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcCautionAnnounceReadTimeByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcCautionAnnounceReadTimeByMeshSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw = open(a_sFileName, 'w', encoding='shift_jis')
                a_sw.write("メッシュNo.,年（警戒）,月（警戒）,日（警戒）,時（警戒）,年（災害）,月（災害）,日（災害）,時（災害）,リードタイム" + a_TemperatureInfo + "\n")

                for a_cnt in range(self.com.g_TargetStartYear, self.com.g_TargetEndYear + 1):
                    a_cnt3 = 0

                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcCautionAnnounceReadTimeSymbol + str(a_cnt)  + ".csv"
                    a_sr = open(a_sFileName, "r", encoding='shift_jis')

                    # 1行目は読み飛ばす
                    a_strTmp = a_sr.readline()
                    a_strTmp = a_sr.readline()
                    while a_strTmp:
                        a_cnt3 += 1
                        a_sw.write(a_strTmp)
                        a_strTmp = a_sr.readline()
                    a_sr.close()

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall3_1-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall3_1-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeOverRainfall3_2():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_DisasterFile,
                 h_meshList,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        if(h_DisasterFile != None):
            del self.com.g_textline_DisasterFile[:]
            gc.collect()
            self.com.g_textline_DisasterFile = h_DisasterFile[:].split("\n")
            self.com.g_textSum_DisasterFile = len(self.com.g_textline_DisasterFile)

        '''
        self.com.g_textSum_DisasterFile = self.com.Store_DataFile(self.com.g_DisasterFileName, self.com.g_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile = self.com.Store_DataFile(self.com.g_CautionAnnounceFileName, self.com.g_textline_CautionAnnounceFile)
        '''

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfall3_2-run', a_strErr)

        a_soilMin = 0
        a_rainMax = -1
        a_sFileName = ""
        a_TemperatureInfo = ""
        a_overSum = 0
        a_overRBFNTime = []
        a_occurTime = []
        a_overRBFNVal = []

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0][1])

            for a_index, a_meshNo in self.meshList:
                # 既往CLの取り込み
                if (self.com.g_PastKind != 0):
                    # 取込あり
                    a_RBFN, a_soilMin, a_rainMax =  self.com.GetPastCLData(a_meshNo)    # 60分間積算雨量上限値のサポート
                    if (self.soilMin > 0) or (self.rainMax > 0):
                        a_soilMin = self.soilMin
                        a_rainMax = self.rainMax

                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcRBFNReadTimeByMeshSoilMinSymbol2 + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcRBFNReadTimeByMeshSymbol2 + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw = open(a_sFileName, 'w', encoding='shift_jis')
                a_sw.write("メッシュNo.,年（RBFN）,月（RBFN）,日（RBFN）,時（RBFN）,年（災害）,月（災害）,日（災害）,時（災害）,リードタイム,RBFN値" + a_TemperatureInfo + "\n")

                if (self.com.g_PastKind == 0):
                    # 取込なし
                    a_overSum = self._getRBFNReadTime(a_meshNo, a_overRBFNTime, a_occurTime, a_overRBFNVal, self.unReal, self.soilMin, self.rainMax) # 60分積算雨量上限値の追加
                else:
                    # 取込あり
                    a_overSum = self._getRBFNReadTime(a_meshNo, a_overRBFNTime, a_occurTime, a_overRBFNVal, self.unReal, a_soilMin, a_rainMax)

                a_iTmp = 0
                a_sTmp = ""
                for a_cnt3 in range(0, a_overSum + 1):
                    if (a_overRBFNVal[a_cnt3] != -1):
                        a_delta = a_occurTime[a_cnt3] - a_overRBFNTime[a_cnt3]   # 実時刻対応⇒分計算
                        a_iTmp = int(a_delta.total_seconds() /60)
                        a_sTmp = str(a_iTmp)
                        a_sw.write(
                            a_meshNo + "," +
                            str(a_overRBFNTime[a_cnt3].year) + "," + str(a_overRBFNTime[a_cnt3].month) + "," + str(a_overRBFNTime[a_cnt3].day) + "," + str(a_overRBFNTime[a_cnt3].hour) + ":" + str(a_overRBFNTime[a_cnt3].minute).rjust(2, "0") + "," +
                            str(a_occurTime[a_cnt3].year) + "," + str(a_occurTime[a_cnt3].month) + "," + str(a_occurTime[a_cnt3].day) + "," + str(a_occurTime[a_cnt3].hour) + ":" + str(a_occurTime[a_cnt3].minute).rjust(2, "0") + "," +
                            a_sTmp + "," +
                            str(float(9 - a_overRBFNVal[a_cnt3]) / 10) + "\n"
                        )

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall3_2-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall3_2-run', a_strErr + "," + sys.exc_info())

    # 全降雨の超過数を取得する
    def _getRBFNReadTime(
            self,
            h_meshNo,
            h_overRBFNTime,
            h_OccurTime,
            h_overRBFNVal,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo + ",unReal=" + str(h_unReal) + ",soilMin=" + str(h_soilMin) + ",rainMax=" + str(h_rainMax)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getRBFNReadTime', a_strErr)

        h_overSum = 0

        # 既往CLの取り込み
        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = -1  # 60分間積算雨量上限値のサポート

        if (self.com.g_PastKind == 0):
            # 取り込みなし
            a_soilMin = h_soilMin # 60分積算雨量上限値の追加
            a_rainMax = h_rainMax # 60分積算雨量上限値の追加
        else:
            # 取り込みあり
            a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(h_meshNo) # 60分間積算雨量上限値のサポート
            if (h_soilMin > 0) or (h_rainMax > 0):
                a_soilMin = h_soilMin
                a_rainMax = h_rainMax

        a_unReal = 0
        a_overTime = ['']*9
        a_strStart = ""
        a_strEnd = ""

        try:
            if (h_unReal > 0):
                a_unReal = h_unReal
            else:
                a_unReal = self.com.g_UnrealAlpha

            a_sFileName = ""
            if (h_soilMin > 0) or (h_rainMax > 0):
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_ContourReviseSoilMinSymbol + "-" + h_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + h_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_ContourReviseByMesh = self.com.Store_DataFile(a_sFileName, self.com.g_textline_ContourReviseByMesh)

            a_overSum = [0]*9
            a_OccurT = [[None]*2]

            del h_overRBFNTime[:]
            del h_overRBFNVal[:]
            del h_OccurTime[:]
            h_overRBFNTime.append(None)
            h_overRBFNVal.append(-1)
            h_OccurTime.append(None)

            for a_cnt in range(int(self.com.g_TargetStartYear), int(self.com.g_TargetEndYear) + 1):
                # 一連の降雨ファイルを開く
                self.com.g_textSum_OccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_OccurRainfallSymbol + str(a_cnt) + ".csv", self.com.g_textline_OccurRainfallFile)
                #print('meshNo=' + h_meshNo + '.a_cnt=' + str(a_cnt) + ',self.com.g_textSum_ChainOccurRainfallFile=' + str(self.com.g_textSum_ChainOccurRainfallFile))
                a_IsOver = [False]*9
                a_prevTime = ""
                for a_cnt1 in range(1, self.com.g_textSum_OccurRainfallFile):
                    #print('meshNo=' + h_meshNo + '.a_cnt1=' + str(a_cnt1))
                    a_split1 = self.com.g_textline_OccurRainfallFile[a_cnt1]
                    a_nowTime = a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5]
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
                    if (a_prevTime != ""):
                        if (a_prevTime != a_strTmp):
                            a_IsOver = [False]*9
                            # 異なる一連の降雨となる
                            h_overSum += 1
                            '''
                            if (h_overSum == 0):
                                a_OccurT[0][0] = datetime.datetime.strptime(a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5], '%Y/%m/%d %H:%M')
                            else:
                            '''
                            a_OccurT.append([None]*2)
                            a_OccurT[len(a_OccurT) - 1][0] = datetime.datetime.strptime(a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5], '%Y/%m/%d %H:%M')
                            h_overRBFNTime.append(None)
                            h_overRBFNVal.append(-1)
                            h_OccurTime.append(None)
                    else:
                        #a_OccurT.append([None]*2)
                        a_OccurT[len(a_OccurT) - 1][0] = datetime.datetime.strptime(a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5], '%Y/%m/%d %H:%M')
                    a_OccurT[len(a_OccurT) - 1][1] = datetime.datetime.strptime(a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5], '%Y/%m/%d %H:%M')

                    a_prevTime = a_nowTime

                    a_rain1 = float(a_split1[6])    # 解析雨量
                    a_shisu1 = float(a_split1[7])   # 土壌雨量指数
                    # Unreal内のデータの除外
                    if ((a_rain1 > 0) and (a_shisu1 > 0)):
                        a_alpha = a_rain1 / a_shisu1
                    else:
                        if ((a_rain1 == 0) and (a_shisu1 > 0)):
                            a_alpha = a_unReal + 1
                        else:
                            a_alpha = 0
                    if (a_alpha < a_unReal):
                        # 2秒かかる
                        #self.com.Outputlog(self.com.g_LOGMODE_TRACE2, "a_alpha < a_unReal", "start")
                        for a_cnt3 in range(0, self.com.g_textSum_ContourReviseByMesh):
                            a_split3 = self.com.g_textline_ContourReviseByMesh[a_cnt3]
                            # 一部でも超えていたらカウントする。
                            a_shisu3 = float(a_split3[0])   # 土壌雨量指数
                            if (a_shisu3 > 0):
                                # 0は意味がない
                                a_IsRBFN = False
                                for a_cnt2 in range(0, 9):
                                    if (self.com.g_PastKind == 0):
                                        # 取り込みなし
                                        a_IsRBFN = True
                                    else:
                                        # 取り込みあり
                                        if (a_cnt2 == a_RBFN):
                                            a_IsRBFN = True
                                    if (a_IsRBFN == True):
                                        if (a_IsOver[a_cnt2] == False):
                                            a_rain3 = float(a_split3[a_cnt2 + 1])   # 解析雨量
                                            self.com.CheckOverRainfall(
                                                h_meshNo,
                                                self.com.g_textline_ContourReviseByMesh,
                                                self.com.g_textSum_ContourReviseByMesh,
                                                a_cnt3,
                                                a_cnt2,
                                                a_shisu1,
                                                a_rain1,
                                                a_shisu3,
                                                a_rain3,
                                                a_overSum,
                                                a_IsOver,
                                                h_soilMin,
                                                h_rainMax
                                            )   # 60分積算雨量上限値の追加

                                            if (a_IsOver[a_cnt2] == True):
                                                a_IsNew = False
                                                # RBFN越
                                                if (h_overRBFNVal[len(h_overRBFNVal) -1 ] != -1):
                                                    # 検出済の年が設定されている
                                                    # RBFN値が大きいものを優先
                                                    if (a_cnt2 < int(h_overRBFNVal[len(h_overRBFNVal) - 1])):
                                                        a_IsNew = True
                                                else:
                                                    # 検出済の年が設定されていない
                                                    a_IsNew = True

                                                if (a_IsNew == True):
                                                    h_overRBFNTime[len(h_overRBFNTime) - 1] = a_OccurT[len(a_OccurT) - 1][1]   # RBFN越時間
                                                    #h_overRBFNTime[h_overSum - 1] = a_OccurT(h_overSum - 1, 1)   # RBFN越時間
                                                    h_overRBFNVal[len(h_overRBFNVal) -1 ] = a_cnt2 # RBFN値

                                    if (self.com.g_PastKind != 0):
                                        # 取込あり
                                        if (a_IsRBFN == True):
                                            break

                del self.com.g_textline_OccurRainfallFile[:]
                gc.collect()

            a_TimeD2 = datetime.datetime.now()
            for a_cnt in range(0, h_overSum + 1):
                a_fFlagD2 = False
                for a_cntD2 in range(1, self.com.g_textSum_DisasterFile):
                    a_splitD2 = self.com.g_textline_DisasterFile[a_cntD2].split(",")
                    if (a_splitD2[0].strip() == h_meshNo):
                        # メッシュ番号が同じ
                        a_tmpTime = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                        if (a_tmpTime >= a_OccurT[a_cnt][0]) and (a_tmpTime <= a_OccurT[a_cnt][1]):
                            if (a_fFlagD2 == True):
                                if (a_tmpTime < a_TimeD2):
                                    a_TimeD2 = a_tmpTime
                                    if (len(a_splitD2) >= 10):
                                        # 実時刻あり
                                        h_OccurTime[a_cnt] = datetime.datetime.strptime(a_splitD2[6] + "/" + a_splitD2[7] + "/" + a_splitD2[8] + " " + a_splitD2[9], '%Y/%m/%d %H:%M')
                                    else:
                                        # 実時刻なし
                                        h_OccurTime[a_cnt] = a_tmpTime
                            else:
                                a_TimeD2 = a_tmpTime
                                if (len(a_splitD2) >= 10):
                                    # 実時刻あり
                                    h_OccurTime[a_cnt] = datetime.datetime.strptime(a_splitD2[6] + "/" + a_splitD2[7] + "/" + a_splitD2[8] + " " + a_splitD2[9], '%Y/%m/%d %H:%M')
                                else:
                                    # 実時刻なし
                                    h_OccurTime[a_cnt] = a_tmpTime

                            a_fFlagD2 = True

                if (a_fFlagD2 == False):
                    # 災害発生時刻が検出されなかった場合
                    h_overRBFNVal[a_cnt] = -1

            del self.com.g_textline_ContourReviseByMesh[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getRBFNReadTime', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getRBFNReadTime', a_strErr + "," + sys.exc_info())

        return h_overSum

# 降雨超過数を作成する
class MakeOverRainfall8():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_kind,
                 h_meshList,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.kind = h_kind
        self.meshList = h_meshList
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfall8-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0][1])
            a_RBFN = 0
            for a_index, a_meshNo in self.meshList:
                if (self.kind == 0):
                    # 実況雨量の場合、一連の発生降雨の抽出結果を予測のものと同一にする
                    for a_cnt2 in range(self.com.g_TargetStartYear, self.com.g_TargetEndYear + 1):
                        a_sw = open(self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_ChainOccurRainfall0Symbol + str(a_cnt2) + ".csv", 'w', encoding='shift_jis')
                        # 一連の発生降雨の抽出結果：予測雨量
                        self.com.g_textSum_ChainOccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_ChainOccurRainfallSymbol + str(a_cnt2) + ".csv", self.com.g_textline_ChainOccurRainfallFile)

                        self.com.Write_TextLine(a_sw, self.com.g_textline_ChainOccurRainfallFile[0])
                        a_sw.write("\n") # 1行目の書込

                        # 全解析雨量・土壌雨量指数：実況雨量
                        self.com.g_textSum_AllRainfall = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_AllRainfall0Symbol + str(a_cnt2) + ".csv", self.com.g_textline_AllRainfall)
                        for a_cntR1 in range(1, self.com.g_textSum_ChainOccurRainfallFile):
                            a_split1 = self.com.g_textline_ChainOccurRainfallFile[a_cntR1]
                            for a_cntR0 in range(a_cntR1, self.com.g_textSum_AllRainfall):
                                a_split0 = self.com.g_textline_AllRainfall[a_cntR0]
                                if (a_split0[0] == a_split1[0]):
                                    # データ番号が一致
                                    a_sw.write(a_split0[0] + "," + a_split1[1] + "," + a_split0[1] + "," + a_split0[2] + "," + a_split0[3] + "," + a_split0[4] + "," + a_split0[5] + "," + a_split0[6] + "," + a_split0[7] + "\n")
                                    break
                        a_sw.close()

                        del self.com.g_textline_ChainOccurRainfallFile[:]
                        del self.com.g_textline_AllRainfall[:]
                        gc.collect()

                a_RBFN = 0
                a_soilMin = 0
                a_rainMax = -1
                a_overTimeS = []
                a_overTimeE = []

                # 既往CLの取り込み
                if (self.com.g_PastKind != 0):
                    # 取込あり
                    a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(a_meshNo) # 60分間積算雨量上限値のサポート
                    if (self.soilMin > 0) or (self.rainMax > 0):
                        a_soilMin = self.soilMin
                        a_rainMax = self.rainMax

                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    if (self.kind == 0):
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime0ByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                    else:
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime1ByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    if (self.kind == 0):
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime0ByMeshSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                    else:
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime1ByMeshSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sw = open(a_sFileName, 'w', encoding='shift_jis')
                a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,CL" + a_TemperatureInfo + "\n")

                if (self.com.g_PastKind == 0):
                    # 取込なし
                    a_overSum = self._getForecastPredictive(self.kind, a_meshNo, a_overTimeS, a_overTimeE, self.unReal, self.soilMin, self.rainMax)   # ★60分積算雨量上限値の追加
                else:
                    # 取込あり
                    a_overSum = self._getForecastPredictive(self.kind, a_meshNo, a_overTimeS, a_overTimeE, self.unReal, a_soilMin, a_rainMax)

                a_sTmp = ""
                a_sCL1 = ""
                a_sCL2 = ""
                #print(a_overSum)
                for a_cnt3 in range(0, a_overSum):
                    a_sw.write(a_meshNo)
                    for a_cnt in range(0, 9):
                        if (a_overTimeS[a_cnt3][a_cnt] == ""):
                            a_sw.write(",")
                        else:
                            #print(a_overTimeS[a_cnt3][a_cnt])
                            a_sw.write("," + a_overTimeS[a_cnt3][a_cnt])

                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL1 = "-"
                        else:
                            # 既往CL取込あり
                            if (a_cnt == a_RBFN):
                                a_sCL1 = str(self.com.My_round(1 - ((a_cnt + 1) / 10), 1))
                                #a_sCL1 = str(1 - (a_cnt + 1) / 10)

                    a_sw.write("," + a_sCL1)
                    a_sw.write("\n")

                if (a_overSum <= 0):
                    a_sw.write(a_meshNo)
                    for a_cnt in range(0, 9):
                        a_sw.write(",")
                        if (self.com.g_PastKind == 0):
                            # 既往CL取込なし
                            a_sCL1 = "-"
                        else:
                            # 既往CL取込あり
                            if (a_cnt == a_RBFN):
                                a_sCL1 = str(self.com.My_round(1 - ((a_cnt + 1) / 10), 1))
                                #a_sCL1 = str(1 - (a_cnt + 1) / 10)

                    a_sw.write("," + a_sCL1)
                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall8-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfall8-run', a_strErr + "," + sys.exc_info())

    # 全降雨の超過数を取得する
    def _getForecastPredictive(
            self,
            h_kind,
            h_meshNo,
            h_overTimeS,
            h_overTimeE,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo + ",unReal=" + str(h_unReal) + ",soilMin=" + str(h_soilMin) + ",rainMax=" + str(h_rainMax)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getForecastPredictive', a_strErr)

        h_overSum = -1

        a_unReal = 0
        a_overTime = ['']*9
        a_strStart = ""
        a_strEnd = ""
        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = 0

        try:
            if (h_unReal > 0):
                a_unReal = h_unReal
            else:
                a_unReal = self.com.g_UnrealAlpha

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_ContourReviseSoilMinSymbol + "-" + h_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + h_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_ContourReviseByMesh = self.com.Store_DataFile(a_sFileName, self.com.g_textline_ContourReviseByMesh)

            a_overSum = [0]*9
            del h_overTimeS[:]
            del h_overTimeE[:]

            for a_cnt in range(int(self.com.g_TargetStartYear), int(self.com.g_TargetEndYear) + 1):
                if (h_kind == 0):
                    a_sFileName = self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_ChainOccurRainfall0Symbol + str(a_cnt) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_ChainOccurRainfallSymbol + str(a_cnt) + ".csv"
                self.com.g_textSum_ChainOccurRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_ChainOccurRainfallFile)

                a_IsOver = [False]*9
                a_now_DataNo = 0
                a_prev_DataNo = 0
                a_prevTime = ""
                for a_cnt1 in range(1, self.com.g_textSum_ChainOccurRainfallFile):
                    a_split1 = self.com.g_textline_ChainOccurRainfallFile[a_cnt1]
                    a_now_DataNo = int(a_split1[0])
                    a_nowTime = a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5]
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

                    if (a_prev_DataNo > 0):
                        if ((a_prev_DataNo + 1) < a_now_DataNo):
                            #print("a_prev_DataNo=" + str(a_prev_DataNo) + "a_now_DataNo=" + str(a_now_DataNo))
                            for a_cnt2 in range(0, 9):
                                a_IsOver[a_cnt2] = False
                            # ★異なる一連の降雨となる。
                            #if (h_overSum > 0):
                            h_overTimeS.append([""]*9)
                            h_overTimeE.append([""]*9)
                            h_overSum += 1
                    else:
                        #print("a_prev_DataNo=" + str(a_prev_DataNo) + "a_now_DataNo=" + str(a_now_DataNo))
                        #if (h_overSum > 0):
                        h_overTimeS.append([""]*9)
                        h_overTimeE.append([""]*9)
                        h_overSum += 1
                    a_prev_DataNo = a_now_DataNo

                    a_prevTime = a_nowTime

                    a_rain1 = float(a_split1[6])    # 解析雨量
                    a_shisu1 = float(a_split1[7])   # 土壌雨量指数
                    # Unreal内のデータの除外
                    if ((a_rain1 > 0) and (a_shisu1 > 0)):
                        a_alpha = a_rain1 / a_shisu1
                    else:
                        if ((a_rain1 == 0) and (a_shisu1 > 0)):
                            a_alpha = a_unReal + 1
                        else:
                            a_alpha = 0
                    if (a_alpha < a_unReal):
                        for a_cnt3 in range(0, self.com.g_textSum_ContourReviseByMesh):
                            a_split3 = self.com.g_textline_ContourReviseByMesh[a_cnt3]
                            # 一部でも超えていたらカウントする。
                            a_shisu3 = float(a_split3[0])   # 土壌雨量指数
                            if (a_shisu3 > 0):
                                # 0は意味がない
                                for a_cnt2 in range(0, 9):
                                    if (a_IsOver[a_cnt2] == False):
                                        a_rain3 = float(a_split3[a_cnt2 + 1])   # 解析雨量
                                        self.com.CheckOverRainfall(
                                            h_meshNo,
                                            self.com.g_textline_ContourReviseByMesh,
                                            self.com.g_textSum_ContourReviseByMesh,
                                            a_cnt3,
                                            a_cnt2,
                                            a_shisu1,
                                            a_rain1,
                                            a_shisu3,
                                            a_rain3,
                                            a_overSum,
                                            a_IsOver,
                                            h_soilMin,
                                            h_rainMax
                                        )   # 60分積算雨量上限値の追加
                                        if (a_IsOver[a_cnt2] == True):
                                            h_overTimeS[len(h_overTimeS) - 1][a_cnt2] += a_nowTime

                del self.com.g_textline_ChainOccurRainfallFile[:]
                gc.collect()

            del self.com.g_textline_ContourReviseByMesh[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getForecastPredictive', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getForecastPredictive', a_strErr + "," + sys.exc_info())

        return h_overSum

# スレッドでは遅い為、multiprocessで対応
#class Thread_MakeOverRainfallByMesh(threading.Thread):
# 降雨超過数を作成する
class MakeOverRainfallByMesh():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_DisasterFile,
                 h_meshNo,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        '''
        self.com.g_textline_DisasterFile =  h_textline_DisasterFile
        self.com.g_textline_CautionAnnounceFile =  h_textline_CautionAnnounceFile
        '''
        '''
        self.com.g_textline_TemperatureFile = h_textline_TemperatureFile
        self.com.g_textline_RainfallFile = h_textline_RainfallFile
        self.com.g_textline_SoilRainFile = h_textline_SoilRainFile
        self.com.g_textline_RainfallFile1 = h_textline_RainfallFile1
        self.com.g_textline_SoilRainFile1 = h_textline_SoilRainFile1
        '''
        '''
        self.com.g_textSum_DisasterFile =  len(h_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile =  len(h_textline_CautionAnnounceFile)
        '''
        '''
        self.com.g_textSum_TemperatureFile = len(h_textline_TemperatureFile)
        self.com.g_textSum_RainfallFile = len(h_textline_RainfallFile)
        self.com.g_textSum_SoilRainFile = len(h_textline_SoilRainFile)
        self.com.g_textSum_RainfallFile1 = len(h_textline_RainfallFile1)
        self.com.g_textSum_SoilRainFile1 = len(h_textline_SoilRainFile1)
        self.year = h_year
        '''
        self.meshNo = h_meshNo
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        if(h_DisasterFile != None):
            del self.com.g_textline_DisasterFile[:]
            gc.collect()
            self.com.g_textline_DisasterFile = h_DisasterFile[:].split("\n")
            self.com.g_textSum_DisasterFile = len(self.com.g_textline_DisasterFile)

        '''
        self.com.g_textSum_DisasterFile = self.com.Store_DataFile(self.com.g_DisasterFileName, self.com.g_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile = self.com.Store_DataFile(self.com.g_CautionAnnounceFileName, self.com.g_textline_CautionAnnounceFile)
        '''

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path + ",meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', a_strErr)

        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = -1
        a_strTmp =""
        a_overSum1 = 9*[0]
        a_overSum2 = 9*[0]
        a_overSum9_1 = 9*[0]        # 9)実質災害捕捉率
        a_overSum9_1ByBlock = 9*[0] # ブロック集計不具合
        a_overSum9_2 = 9*[0]        # ④実質災害捕捉率
        a_timeSum = 9*[0]

        try:
            # 既往CLの取り込み
            if (self.com.g_PastKind != 0):
                # 取り込みあり
                a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(self.meshNo)   # 60分間積算雨量上限値のサポート
                if (self.soilMin > 0) or (self.rainMax > 0):
                    a_soilMin = self.soilMin
                    a_rainMax = self.rainMax

            # 発生降雨数を取得する。
            a_occurSum = self.com.GetOccurRainfallSumByMesh(self.meshNo)
            self.prv_TemperatureInfo = self.com.GetTemperatureInfo(self.meshNo)

            # 結果出力ファイルを開く
            a_sFileName = ""
            # 等高線補正画像
            if (self.soilMin > 0) or (self.rainMax > 0):    #★60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_ContourReviseSoilMinSymbol + "-" + self.meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + self.meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_ContourReviseByMesh = self.com.Store_DataFile(a_sFileName, self.com.g_textline_ContourReviseByMesh)

            if (self.soilMin > 0) or (self.rainMax > 0):    #★60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.meshNo + "\\" + self.com.g_OverRainfallNumByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.meshNo + "\\" + self.com.g_OverRainfallNumByMeshSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')

            # 気温情報を書き込む。
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + self.prv_TemperatureInfo + '\n')

            # 全降雨の超過数を算出する。
            if (self.com.g_PastKind == 0):
                # 取込なし
                self._getOverAllRainfallSum(self.meshNo, a_overSum1, self.unReal, self.soilMin, self.rainMax) # ★60分積算雨量上限値の追加
            else:
                # 取込あり
                self._getOverAllRainfallSum(self.meshNo, a_overSum1, self.unReal, a_soilMin, a_rainMax)

            # 非発生降雨の超過数を算出する。
            if (self.com.g_PastKind == 0):
                # 取込なし
                self._getOverNonOccurRainfallSum(self.meshNo, a_overSum2, a_timeSum, self.unReal, self.soilMin, self.rainMax) # ★60分積算雨量上限値の追加
            else:
                # 取込あり
                self._getOverNonOccurRainfallSum(self.meshNo, a_overSum2, a_timeSum, self.unReal, a_soilMin, a_rainMax)

            # 9)実質災害捕捉率
            if (self.com.g_PastKind == 0):
                # 取込なし
                self._getOverOccurRainfallSum9_1(self.meshNo, a_overSum9_1, self.unReal, self.soilMin, self.rainMax)  # ★60分積算雨量上限値の追加
            else:
                # 取込あり
                self._getOverOccurRainfallSum9_1(self.meshNo, a_overSum9_1, self.unReal, a_soilMin, a_rainMax)

            # ④実質災害捕捉率
            if (self.com.g_PastKind == 0):
                # 取込なし
                self._getOverOccurRainfallSum9_2(self.meshNo, a_overSum9_2, self.unReal, self.soilMin, self.rainMax)  # ★60分積算雨量上限値の追加
            else:
                # 取込あり
                self._getOverOccurRainfallSum9_2(self.meshNo, a_overSum9_2, self.unReal, a_soilMin, a_rainMax)

            # 全降雨超過数
            a_sw.write(self.meshNo + "," + str(a_overSum1[0]) + "," + str(a_overSum1[1]) + "," + str(a_overSum1[2]) + "," + str(a_overSum1[3]) + "," + str(a_overSum1[4]) + "," + str(a_overSum1[5]) + "," + str(a_overSum1[6]) + "," + str(a_overSum1[7]) + "," + str(a_overSum1[8]))
            if (self.com.g_PastKind == 0):
                # 既往CL取込なし
                a_sw.write(",-,-")
            else:
                # 既往CL取込あり
                for a_cnt2 in range(0, 9):
                    if (a_cnt2 == a_RBFN):
                        a_sw.write("," + str(a_overSum1[a_cnt2]) + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
            a_sw.write("\n")

            # 非発生降雨超過数
            a_sw.write(self.meshNo + "," + str(a_overSum2[0]) + "," + str(a_overSum2[1]) + "," + str(a_overSum2[2]) + "," + str(a_overSum2[3]) + "," + str(a_overSum2[4]) + "," + str(a_overSum2[5]) + "," + str(a_overSum2[6]) + "," + str(a_overSum2[7]) + "," + str(a_overSum2[8]))
            if (self.com.g_PastKind == 0):
                # 既往CL取込なし
                a_sw.write(",-,-")
            else:
                # 既往CL取込あり
                for a_cnt2 in range(0, 9):
                    if (a_cnt2 == a_RBFN):
                        a_sw.write("," + str(a_overSum2[a_cnt2]) + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
            a_sw.write("\n")

            # 発生降雨超過数
            if (a_occurSum != 0):
                a_sw.write(self.meshNo + "," + str(a_overSum1[0] - a_overSum2[0]) + "," + str(a_overSum1[1] - a_overSum2[1]) + "," + str(a_overSum1[2] - a_overSum2[2]) + "," + str(a_overSum1[3] - a_overSum2[3]) + "," + str(a_overSum1[4] - a_overSum2[4]) + "," + str(a_overSum1[5] - a_overSum2[5]) + "," + str(a_overSum1[6] - a_overSum2[6]) + "," + str(a_overSum1[7] - a_overSum2[7]) + "," + str(a_overSum1[8] - a_overSum2[8]))
            else:
                a_sw.write(self.meshNo + "," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し")
            if (self.com.g_PastKind == 0):
                # 既往CL取込なし
                a_sw.write(",-,-")
            else:
                # 既往CL取込あり
                for a_cnt2 in range(0, 9):
                    if (a_cnt2 == a_RBFN):
                        if (a_occurSum != 0):
                            a_sw.write("," + str(a_overSum1[a_cnt2] - a_overSum2[a_cnt2]) + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
                        else:
                            a_sw.write(",無し" + "," + str(1 - (a_cnt2 + 1) / 10))
            a_sw.write("\n")

            # 空振り時間
            a_sw.write(self.meshNo + "," + str(a_timeSum[0]) + "," + str(a_timeSum[1]) + "," + str(a_timeSum[2]) + "," + str(a_timeSum[3]) + "," + str(a_timeSum[4]) + "," + str(a_timeSum[5]) + "," + str(a_timeSum[6]) + "," + str(a_timeSum[7]) + "," + str(a_timeSum[8]))
            if (self.com.g_PastKind == 0):
                # 既往CL取込なし
                a_sw.write(",-,-")
            else:
                # 既往CL取込あり
                for a_cnt2 in range(0, 9):
                    if (a_cnt2 == a_RBFN):
                        a_sw.write("," + str(a_timeSum[a_cnt2]) + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
            a_sw.write("\n")

            # 9)実質災害捕捉率【降雨数】
            if (a_occurSum != 0):
                a_sw.write(self.meshNo + "," + str(a_overSum9_1[0]) + "," + str(a_overSum9_1[1]) + "," + str(a_overSum9_1[2]) + "," + str(a_overSum9_1[3]) + "," + str(a_overSum9_1[4]) + "," + str(a_overSum9_1[5]) + "," + str(a_overSum9_1[6]) + "," + str(a_overSum9_1[7]) + "," + str(a_overSum9_1[8]))
            else:
                a_sw.write(self.meshNo + "," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し")
            if (self.com.g_PastKind == 0):
                # 既往CL取込なし
                a_sw.write(",-,-")
            else:
                # 既往CL取込あり
                for a_cnt2 in range(0, 9):
                    if (a_cnt2 == a_RBFN):
                        if (a_occurSum != 0):
                            a_sw.write("," + str(a_overSum9_1[a_cnt2]) + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
                        else:
                            a_sw.write(",無し" + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
            a_sw.write("\n")

            # ④実質災害捕捉率【件数】
            # 該メッシュの災害発生件数を取得
            a_occurSum = self._getDisasterOccurSumByMesh(self.meshNo, a_strTmp)
            if (a_occurSum != 0):
                a_sw.write(self.meshNo + "," + str(a_overSum9_2[0]) + "," + str(a_overSum9_2[1]) + "," + str(a_overSum9_2[2]) + "," + str(a_overSum9_2[3]) + "," + str(a_overSum9_2[4]) + "," + str(a_overSum9_2[5]) + "," + str(a_overSum9_2[6]) + "," + str(a_overSum9_2[7]) + "," + str(a_overSum9_2[8]))
            else:
                a_sw.write(self.meshNo + "," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し")
            if (self.com.g_PastKind == 0):
                # 既往CL取込なし
                a_sw.write(",-,-")
            else:
                # 既往CL取込あり
                # 該メッシュの災害発生件数を取得
                #a_occurSum = self._getDisasterOccurSumByMesh(self.meshNo, a_strTmp)
                for a_cnt2 in range(0, 9):
                    if (a_cnt2 == a_RBFN):
                        if (a_occurSum != 0):
                            a_sw.write("," + str(a_overSum9_2[a_cnt2]) + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
                        else:
                            a_sw.write(",無し" + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
            a_sw.write("\n")

            # 実質災害捕捉率【降雨数】による非発生降雨数
            if (a_occurSum != 0):
                a_sw.write(self.meshNo)
                for a_cnt2 in range(0, 9):
                    a_sw.write("," + str(a_overSum1[a_cnt2] - a_overSum9_1[a_cnt2]))
            else:
                a_sw.write(self.meshNo + "," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し," + "無し")
            if (self.com.g_PastKind == 0):
                # 既往CL取込なし
                a_sw.write(",-,-")
            else:
                # 既往CL取込あり
                for a_cnt2 in range(0,9):
                    if (a_cnt2 == a_RBFN):
                        if (a_occurSum != 0):
                            a_sw.write("," + str(a_overSum1[a_cnt2] - a_overSum9_1[a_cnt2]) + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
                        else:
                            a_sw.write(",無し" + "," + str(self.com.My_round(1 - ((a_cnt2 + 1) / 10), 1)))
            a_sw.write("\n")

            del self.com.g_textline_ContourReviseByMesh[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallByMesh-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallByMesh-run', a_strErr + "," + sys.exc_info())

    # 災害発生件数を取得する
    def _getDisasterOccurSumByMesh(
            self,
            h_meshNo,
            h_tempInfo
    ):
        a_strErr = "meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getDisasterOccurSumByMesh', a_strErr)

        a_iRet = 0

        try:
            for a_cnt in range(0, self.com.g_textSum_DisasterFile):
                a_split1 = self.com.g_textline_DisasterFile[a_cnt].split(",")
                if (a_split1[0] == h_meshNo):
                    a_iRet += 1

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getDisasterOccurSumByMesh', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getDisasterOccurSumByMesh', a_strErr + "," + sys.exc_info())

        return a_iRet

    # 超過をチェックする
    '''
    def _checkOverWhiffTime(
            self,
            h_meshNo,
            h_contLine,
            h_contSum,
            h_contIdx,
            h_lineIdx,
            h_srcShisu,
            h_srcRain,
            h_dstShisu,
            h_dstRain,
            h_overSum,
            h_isOver,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_checkOverWhiffTime', a_strErr)

        a_bFlag = True

        try:
            if (h_srcShisu > h_dstShisu):
                # 土壌雨量指数が等高線を超えている。
                if (h_srcRain >= h_dstRain):
                    h_overSum[h_lineIdx] = h_overSum[h_lineIdx] + 1
                    h_isOver[h_lineIdx] = True
                else:
                    a_bFlag = False
            elif (h_srcShisu == h_dstShisu):
                # 土壌雨量指数が同じ。
                if (h_srcRain >= h_dstRain):
                    # 雨量が等高線を超えている。
                    # カウント対象とする。
                    h_overSum[h_lineIdx] = h_overSum[h_lineIdx] + 1
                    h_isOver[h_lineIdx] = True
            else:
                # 60分積算雨量上限値の追加
                if (h_srcShisu < h_soilMin) and (h_rainMax > 0):
                    # 土壌雨量指数下限値内、かつ60分積算雨量上限値越え
                    if (h_srcRain > h_rainMax):
                        # 雨量が上限値を超えている。
                        # カウント対象とする。
                        h_overSum[h_lineIdx] = h_overSum[h_lineIdx] + 1
                        h_isOver[h_lineIdx] = True

            a_x = [0]*5
            a_y = [0]*5
            if (a_bFlag == False):
                # 次の等高線があればそれとチェックする。
                if (h_contIdx < h_contSum - 1):
                    a_split4 = h_contLine[h_contIdx + 1]
                    a_shisu = float(a_split4[0])    # 土壌雨量指数
                    if (a_shisu > 0):
                        # 0は意味がない
                        a_rain = float(a_split4[h_lineIdx + 1])   # 解析雨量
                        if (a_rain < h_dstRain) and (a_shisu > h_dstShisu):
                            a_x[1] = h_dstShisu
                            a_x[2] = a_shisu
                            a_x[3] = a_shisu
                            a_x[4] = h_dstShisu
                            a_y[1] = h_dstRain
                            a_y[2] = a_rain
                            a_y[3] = h_dstRain
                            a_y[4] = h_dstRain
                            if (self._naigai(h_srcShisu, h_srcRain, a_x, a_y) == True):
                                h_overSum[h_lineIdx] = h_overSum[h_lineIdx] + 1
                                h_isOver[h_lineIdx] = True
                else:
                    if (h_srcShisu >= h_dstShisu):
                        h_overSum[h_lineIdx] = h_overSum[h_lineIdx] + 1
                        h_isOver[h_lineIdx] = True

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args[0]), a_strErr)
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")
            '''

    # 全降雨の超過数を取得する
    def _getOverAllRainfallSum(
            self,
            h_meshNo,
            h_overSum,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo + ",unReal=" + str(h_unReal) + ",soilMin=" + str(h_soilMin) + ",rainMax=" + str(h_rainMax)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getOverAllRainfallSum', a_strErr)

        for a_sum in h_overSum:
            a_sum = 0

        a_unReal = 0
        a_overTime = ['']*9
        a_strStart = ""
        a_strEnd = ""
        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = 0

        try:
            if (h_unReal > 0):
                a_unReal = h_unReal
            else:
                a_unReal = self.com.g_UnrealAlpha

            a_sw = open(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_ChainOccurRainfallSymbolByBlock + ".csv", 'w', encoding='shift_jis')
            a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1\n")
            a_sw2 = open(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_ChainOccurRainfall2SymbolByBlock + ".csv", 'w', encoding='shift_jis')
            a_sw2.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1\n")

            for a_cnt in range(int(self.com.g_TargetStartYear), int(self.com.g_TargetEndYear) + 1):
                # 一連の降雨ファイルを開く
                self.com.g_textSum_ChainOccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_ChainOccurRainfallSymbol + str(a_cnt) + ".csv", self.com.g_textline_ChainOccurRainfallFile)
                #print('meshNo=' + h_meshNo + '.a_cnt=' + str(a_cnt) + ',self.com.g_textSum_ChainOccurRainfallFile=' + str(self.com.g_textSum_ChainOccurRainfallFile))
                a_IsOver = [False]*9
                a_prevTime = ""
                for a_cnt1 in range(1, self.com.g_textSum_ChainOccurRainfallFile):
                    #print('meshNo=' + h_meshNo + '.a_cnt1=' + str(a_cnt1))
                    a_split1 = self.com.g_textline_ChainOccurRainfallFile[a_cnt1]
                    a_nowTime = a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5]
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
                    if (a_prevTime != ""):
                        if (a_prevTime != a_strTmp):
                            # 異なる一連の降雨となる
                            # 開始時刻を出力
                            self._writeChainOccurRainfall(
                                a_sw,
                                a_sw2,
                                h_meshNo,
                                a_strStart,
                                a_strEnd,
                                a_IsOver,
                                a_overTime
                            )
                            a_strStart = self.com.g_textline_ChainOccurRainfallFile[a_cnt1]
                            a_IsOver = [False]*9
                            a_overTime = [""]*9
                    else:
                        # 開始時刻を出力
                        a_strStart = self.com.g_textline_ChainOccurRainfallFile[a_cnt1]
                    a_prevTime = a_nowTime
                    a_strEnd = self.com.g_textline_ChainOccurRainfallFile[a_cnt1]   # ブロック集計変更
                    a_rain1 = float(a_split1[6])    # 解析雨量
                    a_shisu1 = float(a_split1[7])   # 土壌雨量指数
                    # Unreal内のデータの除外
                    if ((a_rain1 > 0) and (a_shisu1 > 0)):
                        a_alpha = a_rain1 / a_shisu1
                    else:
                        if ((a_rain1 == 0) and (a_shisu1 > 0)):
                            a_alpha = a_unReal + 1
                        else:
                            a_alpha = 0
                    if (a_alpha < a_unReal):
                        # 2秒かかる
                        #self.com.Outputlog(self.com.g_LOGMODE_TRACE2, "a_alpha < a_unReal", "start")
                        for a_cnt3 in range(0, self.com.g_textSum_ContourReviseByMesh):
                            a_split3 = self.com.g_textline_ContourReviseByMesh[a_cnt3]
                            # 一部でも超えていたらカウントする。
                            a_shisu3 = float(a_split3[0])   # 土壌雨量指数
                            if (a_shisu3 > 0):
                                # 0は意味がない
                                for a_cnt2 in range(0, 9):
                                    if (a_IsOver[a_cnt2] == False):
                                        a_rain3 = float(a_split3[a_cnt2 + 1])   # 解析雨量
                                        self.com.CheckOverRainfall(
                                            h_meshNo,
                                            self.com.g_textline_ContourReviseByMesh,
                                            self.com.g_textSum_ContourReviseByMesh,
                                            a_cnt3,
                                            a_cnt2,
                                            a_shisu1,
                                            a_rain1,
                                            a_shisu3,
                                            a_rain3,
                                            h_overSum,
                                            a_IsOver,
                                            h_soilMin,
                                            h_rainMax
                                        )   # 60分積算雨量上限値の追加
                                        if (a_IsOver[a_cnt2] == True):
                                            a_overTime[a_cnt2] = a_nowTime
                        #self.com.Outputlog(self.com.g_LOGMODE_TRACE2, "a_alpha < a_unReal", "end")

                # 開始・終了時刻を出力
                if (a_strStart != ""):
                    self._writeChainOccurRainfall(
                        a_sw,
                        a_sw2,
                        h_meshNo,
                        a_strStart,
                        a_strEnd,
                        a_IsOver,
                        a_overTime
                    )

                del self.com.g_textline_ChainOccurRainfallFile[:]
                gc.collect()

            a_sw2.close()
            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverAllRainfallSum', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverAllRainfallSum', a_strErr + "," + sys.exc_info())

    # 非発生降雨の超過数を取得する
    def _getOverNonOccurRainfallSum(
            self,
            h_meshNo,
            h_overSum,
            h_timeSum,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo + ",unReal=" + str(h_unReal) + ",soilMin=" + str(h_soilMin) + ",rainMax=" + str(h_rainMax)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getOverNonOccurRainfallSum', a_strErr)

        a_unReal = 0
        a_overTime = ['']*9
        a_strStart = ""
        a_strEnd = ""
        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = 0

        try:
            if (h_unReal > 0):
                a_unReal = h_unReal
            else:
                a_unReal = self.com.g_UnrealAlpha

            for a_sum in h_overSum:
                a_sum = 0
            for a_sum in h_timeSum:
                a_sum = 0

            a_sw = open(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_WhiffTimeSymbolByBlock + ".csv", 'w', encoding='shift_jis')
            a_sw.write("データ番号,年月日時\n")

            for a_cnt in range(int(self.com.g_TargetStartYear), int(self.com.g_TargetEndYear) + 1):
                # 災害発生降雨を除いた一連降雨ファイルを開く
                self.com.g_textSum_ChainOnlyOccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_ChainOnlyOccurRainfallSymbol + str(a_cnt) + ".csv", self.com.g_textline_ChainOnlyOccurRainfallFile)
                #print('meshNo=' + h_meshNo + ',self.com.g_textSum_ChainOnlyOccurRainfallFile=' + str(self.com.g_textSum_ChainOnlyOccurRainfallFile))
                #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getOverNonOccurRainfallSum', 'meshNo=' + h_meshNo + ',self.com.g_textSum_ChainOnlyOccurRainfallFile=' + str(self.com.g_textSum_ChainOnlyOccurRainfallFile))
                a_IsOver = [False]*9
                a_prevTime = ""
                for a_cnt1 in range(1, self.com.g_textSum_ChainOnlyOccurRainfallFile):
                    #print('meshNo=' + h_meshNo + ',a_cnt1=' + str(a_cnt1))
                    #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getOverNonOccurRainfallSum', 'meshNo=' + h_meshNo + ',self.com.g_textline_ChainOnlyOccurRainfallFile=' + strself.com.g_textline_ChainOnlyOccurRainfallFile[a_cnt1])
                    a_split1 = self.com.g_textline_ChainOnlyOccurRainfallFile[a_cnt1]
                    a_nowTime = a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5]
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
                    if (a_prevTime != ""):
                        if (a_prevTime != a_strTmp):
                            # 異なる一連の降雨となる
                            for a_cnt2 in range(0, 9):
                                if (a_IsOver[a_cnt2] == True):
                                    a_splitB1 = a_strStart
                                    a_splitB2 = a_strEnd
                                    # 開始・終了時刻を出力
                                    break
                            a_strStart = self.com.g_textline_ChainOnlyOccurRainfallFile[a_cnt1]
                            for a_cnt2 in range(0, 9):
                                a_IsOver[a_cnt2] = False
                                a_overTime[a_cnt2] = ""
                    else:
                        # 開始時刻を出力
                        a_strStart = self.com.g_textline_ChainOnlyOccurRainfallFile[a_cnt1]
                    a_prevTime = a_nowTime
                    a_strEnd = self.com.g_textline_ChainOnlyOccurRainfallFile[a_cnt1]   # ブロック集計変更
                    a_rain1 = float(a_split1[6])    # 解析雨量
                    a_shisu1 = float(a_split1[7])   # 土壌雨量指数
                    # Unreal内のデータの除外
                    if ((a_rain1 > 0) and (a_shisu1 > 0)):
                        a_alpha = a_rain1 / a_shisu1
                    else:
                        if ((a_rain1 == 0) and (a_shisu1 > 0)):
                            a_alpha = a_unReal + 1
                        else:
                            a_alpha = 0
                    if (a_alpha < a_unReal):
                        a_IsOverW = [0]*9
                        a_IsExists = False
                        for a_cnt3 in range(0, self.com.g_textSum_ContourReviseByMesh):
                            a_split3 = self.com.g_textline_ContourReviseByMesh[a_cnt3]
                            # 一部でも超えていたらカウントする。
                            a_shisu3 = float(a_split3[0])   # 土壌雨量指数
                            if (a_shisu3 > 0):
                                # 0は意味がない
                                for a_cnt2 in range(0, 9):
                                    if (a_IsOver[a_cnt2] == False):
                                        a_rain3 = float(a_split3[a_cnt2 + 1])   # 解析雨量
                                        self.com.CheckOverRainfall(
                                            h_meshNo,
                                            self.com.g_textline_ContourReviseByMesh,
                                            self.com.g_textSum_ContourReviseByMesh,
                                            a_cnt3,
                                            a_cnt2,
                                            a_shisu1,
                                            a_rain1,
                                            a_shisu3,
                                            a_rain3,
                                            h_overSum,
                                            a_IsOver,
                                            h_soilMin,
                                            h_rainMax
                                        )   # 60分積算雨量上限値の追加
                                        if (a_IsOver[a_cnt2] == True):
                                            a_overTime[a_cnt2] = a_nowTime
                                # 空振り時間は超過しているもの全てをカウント
                                # 一部でも超えていたらカウントする。
                                for a_cnt2 in range(0, 9):
                                    if (a_IsOverW[a_cnt2] == False):
                                        a_rain3 = float(a_split3[a_cnt2 + 1])   # 解析雨量
                                        #CheckOverWhiffTime(
                                        self.com.CheckOverRainfall(
                                            h_meshNo,
                                            self.com.g_textline_ContourReviseByMesh,
                                            self.com.g_textSum_ContourReviseByMesh,
                                            a_cnt3,
                                            a_cnt2,
                                            a_shisu1,
                                            a_rain1,
                                            a_shisu3,
                                            a_rain3,
                                            h_timeSum,
                                            a_IsOverW,
                                            h_soilMin,
                                            h_rainMax
                                        )   # 60分積算雨量上限値の追加
                                        if (a_IsOverW[a_cnt2] == True) and (a_IsExists == False):
                                            a_isOK = False
                                            if (self.com.g_PastKind == 1):
                                                a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(h_meshNo)
                                                if (a_cnt2 == a_RBFN):
                                                    a_isOK = True
                                            else:
                                                a_isOK = True
                                            if (a_isOK == True):
                                                a_sw.write(a_split1[0] + "," + a_nowTime + "," + str(self.com.My_round((9 - a_cnt2) / 10, 1)) + '\n')
                                                #a_sw.write(a_split1[0] + "," + a_nowTime + "," + str((9 - a_cnt2) / 10) + '\n')
                                                a_IsExists = True   # 既にCLを越えている。

                # 開始・終了時刻を出力
                for a_cnt2 in range(0, 9):
                    if (a_IsOver[a_cnt2] == True):
                        a_splitB1 = a_strStart.split(",")
                        a_splitB2 = a_strEnd.split(",")
                        # 開始・終了時刻を出力
                        break

                del self.com.g_textline_ChainOnlyOccurRainfallFile[:]
                gc.collect()

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverNonOccurRainfallSum', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverNonOccurRainfallSum', a_strErr + "," + sys.exc_info())

    # 全降雨の超過数を取得する
    def _getOverOccurRainfallSum9_1(
            self,
            h_meshNo,
            h_overSum,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo + ",unReal=" + str(h_unReal) + ",soilMin=" + str(h_soilMin) + ",rainMax=" + str(h_rainMax)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getOverOccurRainfallSum9_1', a_strErr)

        a_unReal = 0
        a_overTime = ['']*9
        a_strStart = ""
        a_strEnd = ""
        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = 0

        try:
            if (h_unReal > 0):
                a_unReal = h_unReal
            else:
                a_unReal = self.com.g_UnrealAlpha

            for a_sum in h_overSum:
                a_sum = 0

            if (self.com.g_PastKind != 0):
                # 既往CL取込あり
                a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(str(h_meshNo))

            a_sw = open(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_OverOccurRainFallNum9_1TimeSymbolByBlock + ".csv", 'w', encoding='shift_jis')
            a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1\n")

            for a_cnt in range(int(self.com.g_TargetStartYear), int(self.com.g_TargetEndYear) + 1):
                # 災害発生降雨を除いた一連降雨ファイルを開く
                self.com.g_textSum_OccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_OccurRainfallSymbol + str(a_cnt) + ".csv", self.com.g_textline_OccurRainfallFile)

                a_IsOver = [False]*9
                a_overTime = ['']*10
                a_startIdx = 1  # 災害発生時は一連の降雨内を全て超過チェック
                a_IsFirstOccur = True
                a_OccurT = [datetime.datetime.now()]*2
                a_prevTime = ""
                for a_cnt1 in range(1, self.com.g_textSum_OccurRainfallFile):
                    a_split1 = self.com.g_textline_OccurRainfallFile[a_cnt1]
                    a_nowTime = a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5]
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
                    if (a_prevTime != ""):
                        if (a_prevTime != a_strTmp):
                            # 異なる一連の降雨となる
                            a_IsFirstOccur = True
                            self._writeOverOccurRainfallNum9(
                                a_sw,
                                h_meshNo,
                                a_RBFN,
                                a_strStart,
                                a_strEnd,
                                a_IsOver,
                                a_overTime
                            )
                            a_strStart = self.com.g_textline_OccurRainfallFile[a_cnt1]
                            a_IsOver = [False]*9
                            a_overTime = [""]*10
                            a_IsNew = True
                            a_OccurT[0] = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')   # 開始
                            a_startIdx = a_cnt1 # 災害発生時は一連の降雨内を全て超過チェック
                    else:
                        a_IsFirstOccur = True
                        a_OccurT[0] = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')   # 開始
                        # 開始時刻を出力
                        a_strStart = self.com.g_textline_OccurRainfallFile[a_cnt1]
                    a_OccurT[1] = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')   # 終了
                    a_prevTime = a_nowTime
                    a_strEnd = self.com.g_textline_OccurRainfallFile[a_cnt1]   # ブロック集計変更

                    # 災害発生時刻の検出
                    a_IsNew = False
                    a_tmpTime = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')
                    for a_cntD2 in range(1, self.com.g_textSum_DisasterFile):
                        a_splitD2 = self.com.g_textline_DisasterFile[a_cntD2].split(",")
                        if (a_splitD2[0].strip() == h_meshNo):
                            # メッシュ番号が同じ
                            a_tmpTimeD2 = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                            if (a_tmpTimeD2 >= a_OccurT[0]) and (a_tmpTimeD2 <= a_OccurT[1]):
                                # 一連の降雨の時刻範囲内に災害発生時刻あり
                                if (a_tmpTime <= a_tmpTimeD2):  # RBFNを越えた判定はこれで良いか？
                                    a_IsExists = False
                                    for a_cnt3 in range(0, 9):
                                        if (a_overTime[a_cnt3] != ""):
                                            # 既に災害発生が設定されている場合
                                            a_IsExists = True
                                            break
                                    if (a_IsExists == False):
                                        # 災害発生時刻がRBFNを越えた後に発生。
                                        a_IsNew = True
                                    break

                    if (a_IsNew == True):
                        # 災害発生時は一連の降雨内を全て超過チェック
                        for a_cnt4 in range(a_startIdx, a_cnt1 + 1): # 一連の降雨開始から現在まで繰り返す。
                            a_split4 = self.com.g_textline_OccurRainfallFile[a_cnt4]

                            a_rain1 = float(a_split1[6])    # 解析雨量
                            a_shisu1 = float(a_split1[7])   # 土壌雨量指数
                            # Unreal内のデータの除外
                            if ((a_rain1 > 0) and (a_shisu1 > 0)):
                                a_alpha = a_rain1 / a_shisu1
                            else:
                                if ((a_rain1 == 0) and (a_shisu1 > 0)):
                                    a_alpha = a_unReal + 1
                                else:
                                    a_alpha = 0
                            if (a_alpha < a_unReal):
                                a_firstOccurTime = None
                                for a_cnt3 in range(0, self.com.g_textSum_ContourReviseByMesh):
                                    a_split3 = self.com.g_textline_ContourReviseByMesh[a_cnt3]
                                    # 一部でも超えていたらカウントする。
                                    a_shisu3 = float(a_split3[0])   # 土壌雨量指数
                                    if (a_shisu3 > 0):
                                        # 0は意味がない
                                        for a_cnt2 in range(0, 9):
                                            if (a_IsOver[a_cnt2] == False):
                                                a_rain3 = float(a_split3[a_cnt2 + 1])   # 解析雨量
                                                self.com.CheckOverRainfall(
                                                    h_meshNo,
                                                    self.com.g_textline_ContourReviseByMesh,
                                                    self.com.g_textSum_ContourReviseByMesh,
                                                    a_cnt3,
                                                    a_cnt2,
                                                    a_shisu1,
                                                    a_rain1,
                                                    a_shisu3,
                                                    a_rain3,
                                                    h_overSum,
                                                    a_IsOver,
                                                    h_soilMin,
                                                    h_rainMax
                                                )   # 60分積算雨量上限値の追加
                                                if (a_IsOver[a_cnt2] == True):
                                                    if (a_IsFirstOccur == True):
                                                        a_firstOccurTime = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                                                        a_IsFirstOccur = False
                                                        a_overTime[a_cnt2] = a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4]
                                                        a_overTime[9] = a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4]
                                                    else:
                                                        a_dtVal = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                                                        if (a_dtVal <= a_firstOccurTime):
                                                            a_overTime[a_cnt2] = a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4]

                # 開始・終了時刻を出力
                self._writeOverOccurRainfallNum9(
                    a_sw,
                    h_meshNo,
                    a_RBFN,
                    a_strStart,
                    a_strEnd,
                    a_IsOver,
                    a_overTime
                )

                del self.com.g_textline_OccurRainfallFile[:]
                gc.collect()

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverOccurRainfallSum9_1', a_strErr + "," + " ".join(map(str, exp.args)))
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverOccurRainfallSum9_1', a_strErr + "," + sys.exc_info())
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverOccurRainfallSum9_1', a_strErr + "," + sys.exc_info())

    # 全降雨の超過数を取得する
    def _getOverOccurRainfallSum9_2(
            self,
            h_meshNo,
            h_overSum,
            h_unReal,
            h_soilMin,
            h_rainMax
    ):
        a_strErr = "meshNo=" + h_meshNo + ",unReal=" + str(h_unReal) + ",soilMin=" + str(h_soilMin) + ",rainMax=" + str(h_rainMax)
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getOverOccurRainfallSum9_2', a_strErr)

        a_unReal = 0
        a_overTime = ['']*9
        a_strStart = ""
        a_strEnd = ""
        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = 0

        try:
            if (h_unReal > 0):
                a_unReal = h_unReal
            else:
                a_unReal = self.com.g_UnrealAlpha

            for a_sum in h_overSum:
                a_sum = 0

            if (self.com.g_PastKind != 0):
                # 既往CL取込あり
                a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(str(h_meshNo))

            a_sw = open(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_OverOccurRainFallNum9_2TimeSymbolByBlock + ".csv", 'w', encoding='shift_jis')
            a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1\n")

            for a_cnt in range(int(self.com.g_TargetStartYear), int(self.com.g_TargetEndYear) + 1):
                # 災害発生降雨を除いた一連降雨ファイルを開く
                self.com.g_textSum_OccurRainfallFile = self.com.Store_DataFile(self.com.g_OutPath + "\\" + h_meshNo + "\\" + self.com.g_OccurRainfallSymbol + str(a_cnt) + ".csv", self.com.g_textline_OccurRainfallFile)

                a_IsOver = [False]*9
                a_overTime = ['']*10
                a_IsOver = [False]*9
                a_startIdx = 1  # 災害発生時は一連の降雨内を全て超過チェック
                a_OccurT = [datetime.datetime.now()]*2
                a_prevTime = ""
                for a_cnt1 in range(1, self.com.g_textSum_OccurRainfallFile):
                    a_split1 = self.com.g_textline_OccurRainfallFile[a_cnt1]
                    a_nowTime = a_split1[2] + "/" + a_split1[3] + "/" + a_split1[4] + " " + a_split1[5]
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
                    if (a_prevTime != ""):
                        if (a_prevTime != a_strTmp):
                            # 異なる一連の降雨となる
                            a_IsFirstOccur = True
                            self._writeOverOccurRainfallNum9(
                                a_sw,
                                h_meshNo,
                                a_RBFN,
                                a_strStart,
                                a_strEnd,
                                a_IsOver,
                                a_overTime
                            )
                            a_strStart = self.com.g_textline_OccurRainfallFile[a_cnt1]
                            a_IsOver = [False]*9
                            a_overTime = [""]*10
                            a_OccurT[0] = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')   # 開始
                            a_startIdx = a_cnt1 # 災害発生時は一連の降雨内を全て超過チェック
                    else:
                        a_OccurT[0] = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')   # 開始
                        # 開始時刻を出力
                        a_strStart = self.com.g_textline_OccurRainfallFile[a_cnt1]
                    a_OccurT[1] = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')   # 終了
                    a_prevTime = a_nowTime
                    a_strEnd = self.com.g_textline_OccurRainfallFile[a_cnt1]   # ブロック集計変更

                    # 災害発生時刻の検出
                    a_IsNew = False
                    a_iSame = 0
                    a_tmpTime = datetime.datetime.strptime(a_nowTime, '%Y/%m/%d %H:%M')
                    for a_cntD2 in range(1, self.com.g_textSum_DisasterFile):
                        a_splitD2 = self.com.g_textline_DisasterFile[a_cntD2].split(",")
                        if (a_splitD2[0].strip() == h_meshNo):
                            # メッシュ番号が同じ
                            a_tmpTimeD2 = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                            if (a_tmpTimeD2 >= a_OccurT[0]) and (a_tmpTimeD2 <= a_OccurT[1]):
                                # 一連の降雨の時刻範囲内に災害発生時刻あり
                                if (a_tmpTime <= a_tmpTimeD2):  # RBFNを越えた判定はこれで良いか？
                                    # 災害発生時刻がRBFNを越えた後に発生。
                                    a_IsNew = True
                                    a_IsOver = [False]*9
                                    # 同時刻の災害がある複数存在する場合の対処
                                    for a_cntD2_2 in range(a_cntD2 + 1 , self.com.g_textSum_DisasterFile):
                                        a_splitD2_2 = self.com.g_textline_DisasterFile[a_cntD2_2].split(",")
                                        if (a_splitD2_2[0].strip() == h_meshNo):
                                            a_tmpTimeD2_2 = datetime.datetime.strptime(a_splitD2_2[1] + "/" + a_splitD2_2[2] + "/" + a_splitD2_2[3] + " " + a_splitD2_2[4], '%Y/%m/%d %H:%M')
                                            if (a_tmpTimeD2 == a_tmpTimeD2_2):
                                                # 同時刻の災害あり
                                                a_iSame += 1
                                    break

                    if (a_IsNew == True):
                        # 災害発生時は一連の降雨内を全て超過チェック
                        for a_cnt4 in range(a_startIdx, a_cnt1 + 1): # 一連の降雨開始から現在まで繰り返す。
                            a_split4 = self.com.g_textline_OccurRainfallFile[a_cnt4]

                            a_rain1 = float(a_split1[6])    # 解析雨量
                            a_shisu1 = float(a_split1[7])   # 土壌雨量指数
                            # Unreal内のデータの除外
                            if ((a_rain1 > 0) and (a_shisu1 > 0)):
                                a_alpha = a_rain1 / a_shisu1
                            else:
                                if ((a_rain1 == 0) and (a_shisu1 > 0)):
                                    a_alpha = a_unReal + 1
                                else:
                                    a_alpha = 0
                            if (a_alpha < a_unReal):
                                for a_cnt3 in range(0, self.com.g_textSum_ContourReviseByMesh):
                                    a_split3 = self.com.g_textline_ContourReviseByMesh[a_cnt3]
                                    # 一部でも超えていたらカウントする。
                                    a_shisu3 = float(a_split3[0])   # 土壌雨量指数
                                    if (a_shisu3 > 0):
                                        # 0は意味がない
                                        for a_cnt2 in range(0, 9):
                                            if (a_IsOver[a_cnt2] == False):
                                                a_rain3 = float(a_split3[a_cnt2 + 1])   # 解析雨量
                                                self.com.CheckOverRainfall(
                                                    h_meshNo,
                                                    self.com.g_textline_ContourReviseByMesh,
                                                    self.com.g_textSum_ContourReviseByMesh,
                                                    a_cnt3,
                                                    a_cnt2,
                                                    a_shisu1,
                                                    a_rain1,
                                                    a_shisu3,
                                                    a_rain3,
                                                    h_overSum,
                                                    a_IsOver,
                                                    h_soilMin,
                                                    h_rainMax
                                                )   # 60分積算雨量上限値の追加
                                                if (a_IsOver[a_cnt2] == True):
                                                    if (a_overTime[a_cnt2] != ""):
                                                        a_overTime[a_cnt2] += ";"

                                                    a_overTime[a_cnt2] += a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4]
                                                    # 同時刻の災害がある複数存在する場合の対処
                                                    if (a_iSame > 0):
                                                        h_overSum[a_cnt2] += a_iSame
                                                        for a_cntD2_2 in range(1, a_iSame + 1):
                                                            a_overTime[a_cnt2] += ";" + a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4]

                                                    if (a_overTime[9] != ""):
                                                        a_splitO9 = a_overTime[9].split(";")
                                                        for a_s in a_splitO9:
                                                            if (a_s != (a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4])):
                                                                a_overTime[9] += ";" + a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4]
                                                    else:
                                                        a_overTime[9] = a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4]

                # 開始・終了時刻を出力
                self._writeOverOccurRainfallNum9(
                    a_sw,
                    h_meshNo,
                    a_RBFN,
                    a_strStart,
                    a_strEnd,
                    a_IsOver,
                    a_overTime
                )

                del self.com.g_textline_OccurRainfallFile[:]
                gc.collect()

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverOccurRainfallSum9_2', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getOverOccurRainfallSum9_2', a_strErr + "," + sys.exc_info())

    def _writeChainOccurRainfall(
            self,
            h_sw,
            h_sw2,
            h_meshNo,
            h_strStart,
            h_strEnd,
            h_IsOver,
            h_overTime
    ):
        a_strErr = "meshNo=" + h_meshNo
        #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_writeChainOccurRainfall', a_strErr)

        try:
            a_RBFN = 0
            a_soilMin = 0
            a_rainMax = 0

            a_isfnoWO2 = False
            a_splitB1 = h_strStart
            a_splitB2 = h_strEnd
            # 開始・終了時刻を出力
            h_sw2.write(a_splitB1[0] + "," +
                        a_splitB1[2] + "," + a_splitB1[3] + "," + a_splitB1[4] + "," + a_splitB1[5] + "," +
                        a_splitB2[2] + "," + a_splitB2[3] + "," + a_splitB2[4] + "," + a_splitB2[5])
            for a_cnt2 in range(0, 9):
                a_isOK = False
                if (self.com.g_PastKind == 1):
                    a_RBFN, a_soilMin, a_rainMax = self.com.GetPastCLData(h_meshNo)
                    if (a_cnt2 == a_RBFN):
                        a_isOK = True
                else:
                    a_isOK = True
                if (a_isOK == True):
                    if (h_IsOver[a_cnt2] == True):
                        a_splitB1 = h_strStart
                        a_splitB2 = h_strEnd
                        # 開始・終了時刻を出力
                        h_sw.write(a_splitB1[0] + "," +
                                   a_splitB1[2] + "," + a_splitB1[3] + "," + a_splitB1[4] + "," + a_splitB1[5] + "," +
                                   a_splitB2[2] + "," + a_splitB2[3] + "," + a_splitB2[4] + "," + a_splitB2[5])
                        if (self.com.g_PastKind == 1):
                            for a_cnt3 in range(0, 9):
                                if (a_cnt3 == a_RBFN):
                                    h_sw.write("," + h_overTime[a_cnt3])
                                    h_sw2.write("," + h_overTime[a_cnt3])
                                else:
                                    h_sw.write("," + "")
                                    h_sw2.write("," + "")
                        else:
                            for a_cnt3 in range(0, 9):
                                h_sw.write("," + h_overTime[a_cnt3])
                                h_sw2.write("," + h_overTime[a_cnt3])
                        h_sw.write("\n")
                        a_isfnoWO2 = True
                        break
            if (a_isfnoWO2 == False):
                h_sw2.write(",,,,,,,,,")
            h_sw2.write("\n")

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_writeChainOccurRainfall', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_writeChainOccurRainfall', a_strErr + "," + sys.exc_info())

    def _writeOverOccurRainfallNum9(
            self,
            h_sw,
            h_meshNo,
            h_RBFN,
            h_strStart,
            h_strEnd,
            h_IsOver,
            h_overTime
    ):
        a_strErr = "meshNo=" + h_meshNo
        #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_writeOverOccurRainfallNum9_1', a_strErr)

        try:
            for a_cnt2 in range(0, 9):
                if (h_IsOver[a_cnt2] == True):
                    a_splitB1 = h_strStart
                    a_splitB2 = h_strEnd
                    # 開始・終了時刻を出力
                    h_sw.write(a_splitB1[0] + "," +
                        a_splitB1[2] + "," + a_splitB1[3] + "," + a_splitB1[4] + "," + a_splitB1[5] + "," +
                        a_splitB2[2] + "," + a_splitB2[3] + "," + a_splitB2[4] + "," + a_splitB2[5])
                    for a_cnt3 in range(0, 9):
                        h_sw.write("," + h_overTime[a_cnt3])
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        h_sw.write("," + h_overTime[9] + '\n')
                    else:
                        # 既往CL取込あり
                        h_sw.write("," + h_overTime[h_RBFN] + '\n')
                    break

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_writeOverOccurRainfallNum9', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_writeOverOccurRainfallNum9', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeOverRainfallMix():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfallMix-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw1 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw1.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw2 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw2.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw3 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw3.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffTimeMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffTimeMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw4 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw4.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_1SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_1Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw9_1 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw9_1.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_2SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverOccurRainFallNum9_2Symbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw9_2 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw9_2.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFall9_1NumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFall9_1NumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_swNOC9_1 = open(a_sFileName, 'w', encoding='shift_jis')
            a_swNOC9_1.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            for a_meshNo in self.meshList:
                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_OverRainfallNumByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_OverRainfallNumByMeshSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sr = open(a_sFileName, 'r', encoding='shift_jis')

                # 1行目は読み飛ばし
                a_textline = a_sr.readline()

                # 全降雨超過数
                a_textline = a_sr.readline()
                a_sw1.write(a_textline)

                # 非発生降雨超過数
                a_textline = a_sr.readline()
                a_sw2.write(a_textline)

                # 発生降雨超過数
                a_textline = a_sr.readline()
                a_sw3.write(a_textline)

                # 空振り時間
                a_textline = a_sr.readline()
                a_sw4.write(a_textline)

                # 9)実質災害捕捉率【降雨数】
                a_textline = a_sr.readline()
                a_sw9_1.write(a_textline)

                # ④実質災害捕捉率【件数】
                a_textline = a_sr.readline()
                a_sw9_2.write(a_textline)

                # 実質災害捕捉率【降雨数】による非発生降雨数
                a_textline = a_sr.readline()
                a_swNOC9_1.write(a_textline)

                a_sr.close()

            a_sw1.close()
            a_sw2.close()
            a_sw3.close()
            a_sw4.close()
            a_sw9_1.close()
            a_sw9_2.close()
            a_swNOC9_1.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeOverRainfallMix2():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfallMix2-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurRainFallNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurRainFallNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw5 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw5.write("メッシュNo.,発生降雨数" + a_TemperatureInfo + "\n")

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurNumMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CautionAnnounceOccurNumMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw6 = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw6.write("メッシュNo.,災害発生件数" + a_TemperatureInfo + "\n")

            for a_meshNo in self.meshList:
                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_OverRainfallNumByMeshSoilMinSymbol2 + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_OverRainfallNumByMeshSymbol2 + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
                a_sr = open(a_sFileName, 'r', encoding='shift_jis')

                # 1行目は読み飛ばし
                a_textline = a_sr.readline()

                # ①土砂災害警戒情報の災害捕捉率
                # 土砂災害警戒情報発表中の発生降雨超過数
                a_textline = a_sr.readline()
                a_sw5.write(a_textline)
                # 土砂災害警戒情報発表中の災害発生件数
                a_textline = a_sr.readline()
                a_sw6.write(a_textline)

                a_sr.close()

            a_sw5.close()
            a_sw6.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix2-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix2-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeOverRainfallMix3_1():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfallMix3_1-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcCautionAnnounceReadTimeSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcCautionAnnounceReadTimeSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,年（警戒）,月（警戒）,日（警戒）,時（警戒）,年（災害）,月（災害）,日（災害）,時（災害）,リードタイム" + a_TemperatureInfo + "\n")

            for a_meshNo in self.meshList:
                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcCautionAnnounceReadTimeByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcCautionAnnounceReadTimeByMeshSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"

                a_cnt2 = 0
                a_sr = open(a_sFileName, "r", encoding='shift_jis')
                # 1行目は読み飛ばす
                a_strTmp = a_sr.readline()
                a_strTmp = a_sr.readline()
                while a_strTmp:
                    a_cnt2 += 1
                    a_sw.write(a_strTmp)
                    a_strTmp = a_sr.readline()
                a_sr.close()

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix3_1-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix3_1-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeOverRainfallMix3_2():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfallMix3_1-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcRBFNReadTimeSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcRBFNReadTimeSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,年（RBFN）,月（RBFN）,日（RBFN）,時（RBFN）,年（災害）,月（災害）,日（災害）,時（災害）,リードタイム,RBFN値" + a_TemperatureInfo + "\n")

            for a_meshNo in self.meshList:
                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcRBFNReadTimeByMeshSoilMinSymbol2 + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcRBFNReadTimeByMeshSymbol2 + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"

                a_cnt2 = 0
                a_sr = open(a_sFileName, "r", encoding='shift_jis')
                # 1行目は読み飛ばす
                a_strTmp = a_sr.readline()
                a_strTmp = a_sr.readline()
                while a_strTmp:
                    a_cnt2 += 1
                    a_sw.write(a_strTmp)
                    a_strTmp = a_sr.readline()
                a_sr.close()

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix3_2-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix3_2-run', a_strErr + "," + sys.exc_info())

# 降雨超過数を作成する
class MakeOverRainfallMix8():
    def __init__(
            self,
            h_proc_num,
            h_ini_path,
            h_kind,
            h_meshList,
            h_soilMin,
            h_rainMax
    ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.kind = h_kind
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeOverRainfallMix8-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                if (self.kind == 0):
                    a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime0SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime1SoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                if (self.kind == 0):
                    a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime0Symbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    a_sFileName = self.com.g_OutPath + "\\" + self.com.g_CalcForecastTime1Symbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,CL" + a_TemperatureInfo + "\n")

            for a_meshNo in self.meshList:
                if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                    if (self.kind == 0):
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime0ByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                    else:
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime1ByMeshSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                else:
                    if (self.kind == 0):
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime0ByMeshSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                    else:
                        a_sFileName = self.com.g_OutPath + "\\" + a_meshNo + "\\" + self.com.g_CalcForecastTime1ByMeshSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"

                a_cnt2 = 0
                a_sr = open(a_sFileName, "r", encoding='shift_jis')
                # 1行目は読み飛ばす
                a_strTmp = a_sr.readline()
                a_strTmp = a_sr.readline()
                while a_strTmp:
                    a_cnt2 += 1
                    a_sw.write(a_strTmp)
                    a_strTmp = a_sr.readline()
                a_sr.close()

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix8-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeOverRainfallMix8-run', a_strErr + "," + sys.exc_info())

# 空振り率を作成する
class MakeWhiff():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeWhiff-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverAllRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverAllRainfallFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverNonOccurRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverNonOccurRainfallFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            self.com.Write_TextLine(a_sw, self.com.g_textline_OverAllRainfallFile[0])
            a_sw.write("\n")

            for a_cnt1 in range(1, self.com.g_textSum_OverAllRainfallFile):
                a_split1 = self.com.g_textline_OverAllRainfallFile[a_cnt1]
                a_split2 = self.com.g_textline_OverNonOccurRainfallFile[a_cnt1]
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_split1[0])
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                for a_cnt2 in range(1, 10):
                    if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                        if (float(a_split1[a_cnt2]) != 0):
                            if (float(a_split2[a_cnt2]) != 0):
                                a_sTmp = str(self.com.My_round((float(a_split2[a_cnt2]) / float(a_split1[a_cnt2])) * 100, 2))
                                #a_sTmp = '%3.2f' % ((float(a_split2[a_cnt2]) / float(a_split1[a_cnt2])) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            a_sTmp = "未経験"
                    else:
                        if (self.com.g_PastKind == 0):
                            # 既往CL取り込みなし
                            a_sTmp = "無し"
                        else:
                            # 既往CL取り込みあり
                            a_sTmp = a_split1[a_cnt2]
                    a_writeline += "," + a_sTmp
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        a_sCL = "-,-"
                    else:
                        # 既往CL取込あり
                        if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                            a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverAllRainfallFile[:]
            del self.com.g_textline_OverNonOccurRainfallFile[:]
            gc.collect()


        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiff-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiff-run', a_strErr + "," + sys.exc_info())

# 空振り率を作成する
class MakeWhiff_New():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeWhiff_New-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverAllRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverAllRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverAllRainfallFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFall9_1NumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFall9_1NumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverNonOccurRainfall9_1File = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverNonOccurRainfall9_1File)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffNewSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffNewSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            self.com.Write_TextLine(a_sw, self.com.g_textline_OverAllRainfallFile[0])
            a_sw.write("\n")

            for a_cnt1 in range(1, self.com.g_textSum_OverAllRainfallFile):
                a_split1 = self.com.g_textline_OverAllRainfallFile[a_cnt1]
                a_split2 = self.com.g_textline_OverNonOccurRainfall9_1File[a_cnt1]
                a_occurSum = self.com.GetOccurRainfallSumByMesh(a_split1[0])
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                for a_cnt2 in range(1, 10):
                    if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                        if (float(a_split1[a_cnt2]) != 0):
                            if (self.com.Str_isfloat(a_split2[a_cnt2]) == True):
                                if (float(a_split2[a_cnt2]) != 0):
                                    a_sTmp = str(self.com.My_round((float(a_split2[a_cnt2]) / float(a_split1[a_cnt2])) * 100, 2))
                                    #a_sTmp = '%3.1f' % ((float(a_split2[a_cnt2]) / float(a_split1[a_cnt2])) * 100)
                                else:
                                    a_sTmp = "0"
                            else:
                                a_sTmp = "未経験"
                        else:
                            a_sTmp = "未経験"
                    else:
                        if (self.com.g_PastKind == 0):
                            # 既往CL取り込みなし
                            a_sTmp = "無し"
                        else:
                            # 既往CL取り込みあり
                            a_sTmp = a_split1[a_cnt2]
                    a_writeline += "," + a_sTmp
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        a_sCL = "-,-"
                    else:
                        # 既往CL取込あり
                        if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                            a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverAllRainfallFile[:]
            del self.com.g_textline_OverNonOccurRainfall9_1File[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiff_New-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiff_New-run', a_strErr + "," + sys.exc_info())

# 空振り頻度を作成する
class MakeWhiffFrequency():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeWhiffFrequency-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFallNumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFallNumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverNonOccurRainfallFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverNonOccurRainfallFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffFrequencySoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffFrequencySymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,対象期間(年),現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            # 該当メッシュの対象期間を算出する
            a_tyear = self.com.GetTargetYearByMesh(self.com.g_TargetStartYear, self.com.g_TargetEndYear, self.com.g_OutPath, self.meshList[0])
            a_tyear = int(self.com.My_round(a_tyear, 0))
            for a_cnt1 in range(1, self.com.g_textSum_OverNonOccurRainfallFile):
                a_split1 = self.com.g_textline_OverNonOccurRainfallFile[a_cnt1]
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                for a_cnt2 in range(1, 10):
                    if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                        if (float(a_split1[a_cnt2]) != 0):
                            if (a_tyear > 0):
                                a_sTmp = str(self.com.My_round((float(a_split1[a_cnt2]) / a_tyear) * 100, 2))
                                #a_sTmp = '%10.2f' % ((float(a_split1[a_cnt2]) / a_tyear) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            a_sTmp = "0"
                    else:
                        a_sTmp = a_split1[a_cnt2]
                    a_writeline += "," + a_sTmp
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        a_sCL = "-,-"
                    else:
                        # 既往CL取込あり
                        if (str(1 - (a_cnt2) / 10) == a_split1[11]):
                            a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + str(a_tyear)
                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverNonOccurRainfallFile[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiffFrequency-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiffFrequency-run', a_strErr + "," + sys.exc_info())

# 空振り頻度を作成する
class MakeWhiffFrequency_New():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeWhiffFrequency_New-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFall9_1NumSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_OverNonOccurRainFall9_1NumSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_OverNonOccurRainfall9_1File = self.com.Store_DataFile(a_sFileName, self.com.g_textline_OverNonOccurRainfall9_1File)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffFrequencyNewSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffFrequencyNewSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,対象期間(年),現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            # 該当メッシュの対象期間を算出する
            a_tyear = self.com.GetTargetYearByMesh(self.com.g_TargetStartYear, self.com.g_TargetEndYear, self.com.g_OutPath, self.meshList[0])
            a_tyear = int(self.com.My_round(a_tyear, 0))
            for a_cnt1 in range(1, self.com.g_textSum_OverNonOccurRainfall9_1File):
                a_split1 = self.com.g_textline_OverNonOccurRainfall9_1File[a_cnt1]
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                for a_cnt2 in range(1, 10):
                    if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                        if (float(a_split1[a_cnt2]) != 0):
                            if (a_tyear > 0):
                                a_sTmp = str(self.com.My_round((float(a_split1[a_cnt2]) / a_tyear), 2))
                                #a_sTmp = '%10.2f' % ((float(a_split1[a_cnt2]) / a_tyear) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            a_sTmp = "0"
                    else:
                        a_sTmp = a_split1[a_cnt2]
                    a_writeline += "," + a_sTmp
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        a_sCL = "-,-"
                    else:
                        # 既往CL取込あり
                        if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                            a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + str(a_tyear)
                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_OverNonOccurRainfall9_1File[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiffFrequency_New-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiffFrequency_New-run', a_strErr + "," + sys.exc_info())

# 空振り時間を作成する
class MakeWhiffTime():
    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_meshList,
                 h_soilMin,
                 h_rainMax
                 ):
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path
        self.meshList = h_meshList
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeWhiffTime-run', a_strErr)

        a_sFileName = ""
        a_TemperatureInfo = ""
        a_strTmp = ""

        try:
            a_TemperatureInfo = self.com.GetTemperatureInfo(self.meshList[0])

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffTimeMixSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffTimeMixSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            self.com.g_textSum_WhiffTimeFile = self.com.Store_DataFile(a_sFileName, self.com.g_textline_WhiffTimeFile)

            if (self.soilMin > 0) or (self.rainMax > 0):    # 60分積算雨量上限値の追加
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffTimeSoilMinSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                a_sFileName = self.com.g_OutPath + "\\" + self.com.g_WhiffTimeSymbol + "-" + str(self.com.g_TargetStartYear)  + "-" + str(self.com.g_TargetEndYear) + ".csv"
            a_sw = open(a_sFileName, 'w', encoding='shift_jis')
            a_sw.write("メッシュNo.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,対象期間(年),現CLの等RBFN値出力値,結果" + a_TemperatureInfo + "\n")

            # 該当メッシュの対象期間を算出する
            a_tyear = self.com.GetTargetYearByMesh(self.com.g_TargetStartYear, self.com.g_TargetEndYear, self.com.g_OutPath, self.meshList[0])
            a_tyear = int(self.com.My_round(a_tyear, 0))
            for a_cnt1 in range(1, self.com.g_textSum_WhiffTimeFile):
                a_split1 = self.com.g_textline_WhiffTimeFile[a_cnt1]
                a_writeline = a_split1[0]
                a_sTmp = ""
                a_sCL = ""
                for a_cnt2 in range(1, 10):
                    if (self.com.Str_isfloat(a_split1[a_cnt2]) == True):
                        if (float(a_split1[a_cnt2]) != 0):
                            if (a_tyear > 0):
                                a_sTmp = str(self.com.My_round((float(a_split1[a_cnt2]) / a_tyear), 2))
                                #a_sTmp = '%10.2f' % ((float(a_split1[a_cnt2]) / a_tyear) * 100)
                            else:
                                a_sTmp = "0"
                        else:
                            a_sTmp = "0"
                    else:
                        a_sTmp = a_split1[a_cnt2]
                    a_writeline += "," + a_sTmp
                    if (self.com.g_PastKind == 0):
                        # 既往CL取込なし
                        a_sCL = "-,-"
                    else:
                        # 既往CL取込あり
                        if (str(self.com.My_round(1 - (a_cnt2) / 10, 1)) == a_split1[11]):
                            a_sCL = a_sTmp + "," + a_split1[11]

                a_writeline += "," + str(a_tyear)
                a_writeline += "," + a_sCL
                a_sw.write(a_writeline + "\n")

            a_sw.close()

            del self.com.g_textline_WhiffTimeFile[:]
            gc.collect()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiffTime-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeWhiffTime-run', a_strErr + "," + sys.exc_info())
