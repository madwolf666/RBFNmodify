################################################################################
# 等高線の作成
################################################################################
import sys
import os
import datetime
import csv
import com_functions
import threading

class Thread_MakeAutoContourByMesh(threading.Thread):
    com = None

    def __init__(self,
                 h_ini_path,
                 h_textline_DisasterFile,
                 h_textline_CautionAnnounceFile,
                 h_textline_TemperatureFile,
                 h_textline_RainfallFile,
                 h_textline_SoilRainFile,
                 h_textline_RainfallFile1,
                 h_textline_SoilRainFile1,
                 h_year,
                 h_meshNo
                 ):
        threading.Thread.__init__(self)

        self.com = com_functions.ComFunctions()

        self.ini_path = h_ini_path
        self.com.g_textline_DisasterFile =  h_textline_DisasterFile
        self.com.g_textline_CautionAnnounceFile =  h_textline_CautionAnnounceFile
        self.com.g_textline_TemperatureFile = h_textline_TemperatureFile
        self.com.g_textline_RainfallFile = h_textline_RainfallFile
        self.com.g_textline_SoilRainFile = h_textline_SoilRainFile
        self.com.g_textline_RainfallFile1 = h_textline_RainfallFile1
        self.com.g_textline_SoilRainFile1 = h_textline_SoilRainFile1
        self.com.g_textSum_DisasterFile =  len(h_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile =  len(h_textline_CautionAnnounceFile)
        self.com.g_textSum_TemperatureFile = len(h_textline_TemperatureFile)
        self.com.g_textSum_RainfallFile = len(h_textline_RainfallFile)
        self.com.g_textSum_SoilRainFile = len(h_textline_SoilRainFile)
        self.com.g_textSum_RainfallFile1 = len(h_textline_RainfallFile1)
        self.com.g_textSum_SoilRainFile1 = len(h_textline_SoilRainFile1)
        self.year = h_year
        self.meshNo = h_meshNo

        #引数を取得
        self.com.GetEnvData(h_ini_path)

    def run(self):
        a_strErr = "ini_path=" + self.ini_path +  ",Year=" + str(self.year) + ",meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', a_strErr)

        try:
            # 既往CLの取り込み
            if (self.com.g_PastKind == 0):
                # 取り込みなし
                self.TargetPath = self.com.g_RBFNOutPath
                self.TargetFile = "surface-" + self.meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                # 取り込みあり
                self.TargetPath = self.com.g_PastRBFNOutPath
                # 既往CL対象メッシュ選択サポート
                self.TargetFile = "surface-" + self.com.GetTargetMeshNoByCL(self.com.g_TargetStartYear, self.meshNo) + "-" + str(self.com.g_PastTargetStartYear) + "-" + str(self.com.g_PastTargetEndYear) + ".csv"
                #self.meshNo = a_strTmp  '[2012.12.17]既往CL対象メッシュ選択サポート

            self.OutPath = self.com.g_OutPath

            # オリジナル等高線の作成
            self._makeAutoContourOrigin(self.meshNo)
            # 等高線の補正
            self._makeAutoContourRevise(self.meshNo)
            # スネーク曲線の作成
            self._makeAutoContourSnake(self.meshNo)

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args), a_strErr)
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")

    def _makeAutoContourOrigin(self, h_meshNo):
        a_strErr = "meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, '_makeAutoContourOrigin', a_strErr)

        try:
            a_i = 0
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args), a_strErr)
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")

    def _makeAutoContourRevise(self, h_meshNo):
        a_strErr = "meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, '_makeAutoContourOrigin', a_strErr)

        try:
            a_i = 0
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args), a_strErr)
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")

    def _makeAutoContourSnake(self, h_meshNo):
        a_strErr = "meshNo=" + h_meshNo
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, '_makeAutoContourOrigin', a_strErr)

        try:
            a_i = 0
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, str(exp.args), a_strErr)
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, sys.exc_info(), "")
