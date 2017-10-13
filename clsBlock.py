################################################################################
# ブロック集計
################################################################################
import sys
import os
import datetime
import math
import csv
import xlrd
import openpyxl as px
import com_functions
import threading

prv_xlWkb = None


class MakeBlockAll():
    #prv_xlWkb = None
    g_blockNameList = []
    g_blockNoList = []

    def __init__(self,
                 h_proc_num,
                 h_ini_path
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

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.com.g_textSum_DisasterFile = self.com.Store_DataFile(self.com.g_DisasterFileName, self.com.g_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile = self.com.Store_DataFile(self.com.g_CautionAnnounceFileName, self.com.g_textline_CautionAnnounceFile)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'MakeBlockAll-run', a_strErr)

        try:
            a_retsu, a_gyo = self._getBlockList()
            print(a_retsu, a_gyo)

            # 集計結果ファイルを読み込み、ブロック毎に集計し直す。
            # 一連の発生降雨
            #self._makeRainfallByBlock()
            # 災害発生降雨
            self._makeOccurRainfallByBlock()
            # 非発生降雨
            #self._makeNonOccurRainfallByBlock()
            # 一連の発生降雨
            #self._makeRainfall2ByBlock()
            # 災害発生降雨
            #self._makeOccurRainfall2ByBlock()
            # 空振り時間
            #self._makeWiffTimeByBlock()
            # 発生降雨超過数【災害捕捉率】
            #self._makeOccurRainfall9_1ByBlock()
            # 災害発生件数【災害捕捉率】
            #self._makeOccurRainfall9_2ByBlock()
            # 警戒情報リードタイム
            #self._makeReadTimeByBlock(self.com.g_CalcCautionAnnounceReadTimeSymbolByBlock)
            # RBFN越リードタイム
            #self._makeReadTimeByBlock(self.com.g_CalcRBFNReadTimeSymbolByBlock)

            #self._makeStatisticsByBlock()

            # ①土砂災害警戒情報の災害捕捉率、③土砂災害警戒情報の発表頻度
            #self._makeStatisticsByBlock2()
            # ②土砂災害警戒情報のリードタイム
            #self._makeStatisticsByBlock3_1()
            # ⑥RBFN越のリードタイム
            #self._makeStatisticsByBlock3_2()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeBlockAll-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeBlockAll-run', a_strErr + "," + sys.exc_info())

    def _getBlockList(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getBlockList-run', a_strErr)

        a_restu = 0
        a_gyo = 0

        a_wkb = None

        try:
            del self.g_blockNameList[:]
            del self.g_blockNoList[:]

            a_wkb = xlrd.open_workbook(self.com.g_BlockExcelDefine)

            a_wks1 = a_wkb.sheet_by_name("ブロック図")

            # 列数を取得
            a_restu = a_wks1.ncols -1
            '''
            a_row = a_wks1.row_values(1, 1)
            for a_cell in a_row:
                a_restu += 1
                '''

            # 行数を取得
            a_gyo = a_wks1.nrows - 1

            a_wks1 = a_wkb.sheet_by_name("ブロック区分")
            a_cnt = 0
            a_sum = -1
            a_strPrevName = ""
            for a_row_index in range(a_wks1.nrows):
                a_value = int(a_wks1.cell_value(a_row_index, 0))   # ブロック番号
                a_strNowName = a_wks1.cell_value(a_row_index, 1)   # ブロック名
                if (a_strPrevName != a_strNowName):
                    # ブロック名が異なる
                    self.g_blockNameList.append(str(a_strNowName))
                    self.g_blockNoList.append(str(a_value))
                    a_strPrevName = a_strNowName
                    a_sum += 1
                else:
                    self.g_blockNoList[a_sum] += "," + str(a_value)

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getBlockList', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getBlockList', a_strErr + "," + sys.exc_info())
        finally:
            if (a_wkb != None):
                a_wkb.release_resources()
                del a_wkb

        return a_restu, a_gyo

    # 空振り率を作成する
    def _makeForecastPredictiveByBlock(self, h_sw, h_meshList):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeForecastPredictiveByBlock', a_strErr)

        try:
            a_textline1 = []
            a_textSum1 = self.com.Store_DataFile(self.com.g_OutPath + "\\" + self.com.g_CalcForecastPredictiveSymbol + "【ブロック】-" + (self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", a_textline1)
            a_FSum = 0    # 予測超過メッシュ数
            a_PSum = 0    # 予測適中メッシュ数
            a_sTmp = ""
            a_iTmp = 0

            for a_cnt1 in range(1, a_textSum1):
                a_split1 = a_textline1[a_cnt1]
                for a_s in h_meshList:
                    if (a_split1[0] == a_s):
                        # 予測超過数をチェック
                        for a_cnt2 in range(10, 19):
                            if (self.com.Str_isfloat(a_split1[28]) == False):
                                # 既往CL取込なし
                                a_FSum += int(a_split1[a_cnt2])
                            else:
                                # 既往CL取込あり
                                a_iTmp = a_split1[28] * 10  # CL
                                if ((19 - a_cnt2) == a_iTmp):
                                    a_FSum += int(a_split1[a_cnt2])
                                    break

                        # 予測適中数をチェック
                        for a_cnt2 in range(19, 28):
                            if (self.com.Str_isfloat(a_split1[28]) == False):
                                # 既往CL取込なし
                                a_PSum += int(a_split1[a_cnt2])
                            else:
                                # 既往CL取込あり
                                a_iTmp = a_split1[28] * 10  # CL
                                if ((28 - a_cnt2) == a_iTmp):
                                    a_PSum += int(a_split1[a_cnt2])
                                    break
                        break

            if (a_FSum > 0) and (a_PSum > 0):
                a_sTmp = "%3,1f" % ((float(a_PSum) /float(a_FSum)) * 100) + ",予測適中メッシュ数⇒," + str(a_PSum) + ",予測超過メッシュ数⇒," + str(a_FSum)
            else:
                a_sTmp = "0"
            h_sw.write("予測適中率,", a_sTmp + "\n")

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeForecastPredictiveByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeForecastPredictiveByBlock', a_strErr + "," + sys.exc_info())

    # 非発生降雨
    def _makeNonOccurRainfallByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeNonOccurRainfallByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 一連の降雨データをメモリに退避
                a_textlineR = []
                a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", a_textlineR)
                # 災害発生降雨データをメモリに退避
                a_textlineC = []
                a_textSumC = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_OccurRainfallSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", a_textlineC)

                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOnlyOccurRainfallSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1\n")

                for a_cnt3 in range(1, a_textSumR):
                    a_splitR = a_textlineR[a_cnt3]
                    a_nowsTimeR = datetime.datetime.strptime(a_splitR[1] + "/" + a_splitR[2] + "/" + a_splitR[3] + " " + a_splitR[4], '%Y/%m/%d %H:%M')
                    a_noweTimeR = datetime.datetime.strptime(a_splitR[5] + "/" + a_splitR[6] + "/" + a_splitR[7] + " " + a_splitR[8], '%Y/%m/%d %H:%M')

                    a_IsOK = True    # 災害発生降雨がなかった場合に非発生降雨に反映されない。

                    for a_cnt2 in range(1, a_textSumC):
                        a_splitC = a_textlineC[a_cnt2]
                        a_nowsTimeC = datetime.datetime.strptime(a_splitC[1] + "/" + a_splitC[2] + "/" + a_splitC[3] + " " + a_splitC[4], '%Y/%m/%d %H:%M')
                        a_noweTimeC = datetime.datetime.strptime(a_splitC[5] + "/" + a_splitC[6] + "/" + a_splitC[7] + " " + a_splitC[8], '%Y/%m/%d %H:%M')

                        if (a_nowsTimeR == a_nowsTimeC) and (a_noweTimeR == a_noweTimeC):
                            # 一致
                            a_IsOK = False
                            break
                        else:
                            # 不一致
                            a_IsOK = True

                    if (a_IsOK == True):
                        a_sw.write(a_textlineR[a_cnt3])
                        a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeNonOccurRainfallByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeNonOccurRainfallByBlock', a_strErr + "," + sys.exc_info())

    # 災害発生降雨
    def _makeOccurRainfallByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeOccurRainfallByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 一連の降雨データをメモリに退避
                a_textlineR = []
                a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv", a_textlineR)

                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_OccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,メッシュ番号,災害発生時刻\n")

                a_index = []
                a_sTime = []
                a_eTime = []
                a_CLTime = []
                a_MeshNo = []
                a_OMeshNo = []
                a_OTime = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    for a_cnt2 in range(0, self.com.g_textSum_DisasterFile):
                        a_splitD2 = self.com.g_textline_DisasterFile[a_cnt2]
                        if (a_splitD2[0] == a_meshList[a_cnt3]):
                            # メッシュ番号が一致
                            a_tmpTime = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                            for a_cnt4 in range(1, a_textSumR):
                                a_splitR = a_textlineR[a_cnt4]
                                a_nowsTime = datetime.datetime.strptime(a_splitR[1] + "/" + a_splitR[2] + "/" + a_splitR[3] + " " + a_splitR[4], '%Y/%m/%d %H:%M')
                                a_noweTime = datetime.datetime.strptime(a_splitR[5] + "/" + a_splitR[6] + "/" + a_splitR[7] + " " + a_splitR[8], '%Y/%m/%d %H:%M')
                                if (a_tmpTime >= a_nowsTime) and (a_tmpTime <= a_noweTime):
                                    # 降雨範囲内で災害発生
                                    a_IsOK = False

                                    # 対象CLに災害時刻が設定されていない場合にエラー
                                    if (a_rSum <= 0):
                                        # 最初のレコード読込
                                        a_IsOK = True
                                    else:
                                        # ２回目以降のレコード読込
                                        for a_cnt5 in range(0, a_rSum):
                                            # 時間範囲の比較
                                            if (a_tmpTime > a_eTime[a_cnt5]) or (a_tmpTime < a_sTime[a_cnt5]):
                                                # 開始時間が終了より先の場合
                                                # 終了時間が開始より前の場合
                                                a_IsOK = True
                                            else:
                                                a_IsOK = False
                                                if (a_tmpTime < a_OTime[a_rSum - 1]):
                                                    a_OTime[a_rSum - 1] = a_tmpTime
                                                    a_OMeshNo[a_rSum - 1] = a_splitD2[0]
                                                break

                                    if (a_IsOK == True):
                                        a_index.append(a_splitR[0])
                                        a_sTime.append(a_nowsTime)
                                        a_eTime.append(a_noweTime)

                                        a_CLTime.append([None]*9)
                                        a_MeshNo.append([""]*9)

                                        for a_cnt5 in range(9, 18):
                                            if (a_splitR[a_cnt5] != ""):
                                                a_CLTime[a_rSum][a_cnt5 - 9] = datetime.datetime.strptime(a_splitR[a_cnt5], '%Y/%m/%d %H:%M')
                                                a_MeshNo[a_rSum][a_cnt5 - 9] = a_meshList[a_cnt3]

                                        a_OMeshNo.append(a_splitD2[0])
                                        a_OTime.append(a_tmpTime)
                                        a_rSum += 1

                                    break

                for a_cnt2 in range(0, a_rSum):
                    a_sw.write(a_index[a_cnt2] +
                               "," + str(a_sTime[a_cnt2].year) + "," + str(a_sTime[a_cnt2].month) + "," + str(a_sTime[a_cnt2].day) + "," + str(a_sTime[a_cnt2].hour) + ":" + str(a_sTime[a_cnt2].minute).rjust(2, "0") +
                               "," + str(a_eTime[a_cnt2].year) + "," + str(a_eTime[a_cnt2].month) + "," + str(a_eTime[a_cnt2].day) + "," + str(a_eTime[a_cnt2].hour) + ":" + str(a_eTime[a_cnt2].minute).rjust(2, "0"))

                    for a_cnt3 in range(0, 9):
                        if (a_CLTime[a_cnt2][a_cnt3] == None):
                            a_sw.write(",")
                        else:
                            a_sw.write("," + str(a_CLTime[a_cnt2][a_cnt3].year) + "/" + str(a_CLTime[a_cnt2][a_cnt3].month) + "/" + str(a_CLTime[a_cnt2][a_cnt3].day) + " " + str(a_CLTime[a_cnt2][a_cnt3].hour) + ":" + str(a_CLTime[a_cnt2][a_cnt3].minute).rjust(2, "0"))

                    for a_cnt3 in range(0, 9):
                        a_sw.write("," + a_MeshNo[a_cnt2][a_cnt3])

                    a_sw.write("," + a_OMeshNo[a_cnt2])
                    a_sw.write("," + str(a_OTime[a_cnt2].year) + "/" + str(a_OTime[a_cnt2].month) + "/" + str(a_OTime[a_cnt2].day) + " " + str(a_OTime[a_cnt2].hour) + ":" + str(a_OTime[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfallByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfallByBlock', a_strErr + "," + sys.exc_info())

    # 災害発生降雨
    def _makeOccurRainfall2ByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeOccurRainfall2ByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 一連の降雨データをメモリに退避
                a_textlineR = []
                a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", a_textlineR)

                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_OccurRainfall2SymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,メッシュ番号,災害発生時刻\n")

                a_bIsSet = [False]*a_textSumR
                a_index = []
                a_sTime = []
                a_eTime = []
                a_CLTime = []
                a_MeshNo = []
                a_OMeshNo = []
                a_OTime = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    for a_cnt2 in range(0, self.com.g_textSum_DisasterFile):
                        a_splitD2 = self.com.g_textline_DisasterFile[a_cnt2]
                        if (a_splitD2[0] == a_meshList[a_cnt3]):
                            # メッシュ番号が一致
                            a_tmpTime = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                            for a_cnt4 in range(1, a_textSumR):
                                a_splitR = a_textlineR[a_cnt4]
                                a_nowsTime = datetime.datetime.strptime(a_splitR[1] + "/" + a_splitR[2] + "/" + a_splitR[3] + " " + a_splitR[4], '%Y/%m/%d %H:%M')
                                a_noweTime = datetime.datetime.strptime(a_splitR[5] + "/" + a_splitR[6] + "/" + a_splitR[7] + " " + a_splitR[8], '%Y/%m/%d %H:%M')
                                if (a_tmpTime >= a_nowsTime) and (a_tmpTime <= a_noweTime):
                                    # 降雨範囲内で災害発生
                                    a_IsOK = False

                                    # 対象CLに災害時刻が設定されていない場合にエラー
                                    if (a_rSum <= 0):
                                        # 最初のレコード読込
                                        a_IsOK = True
                                    else:
                                        # ２回目以降のレコード読込
                                        for a_cnt5 in range(0, a_rSum):
                                            # 時間範囲の比較
                                            if (a_tmpTime > a_eTime[a_cnt5]) or (a_tmpTime < a_sTime[a_cnt5]):
                                                # 開始時間が終了より先の場合
                                                # 終了時間が開始より前の場合
                                                a_IsOK = True
                                            else:
                                                a_IsOK = False
                                                if (a_tmpTime < a_OTime[a_rSum]):
                                                    a_OTime[a_rSum] = a_tmpTime
                                                    a_OMeshNo[a_rSum] = a_splitD2[0]
                                            break

                                    if (a_IsOK == True):
                                        a_index.append(a_splitR[0])
                                        a_sTime.append(a_nowsTime)
                                        a_eTime.append(a_noweTime)

                                        a_CLTime.append([None]*9)
                                        a_MeshNo.append([""]*9)

                                        for a_cnt5 in range(9, 18):
                                            if (a_splitR[a_cnt5] != ""):
                                                a_CLTime[a_rSum][a_cnt5 - 9] = datetime.datetime.strptime(a_splitR[a_cnt5], '%Y/%m/%d %H:%M')
                                                a_MeshNo[a_rSum][a_cnt5 - 9] = a_meshList[a_cnt3]

                                        a_OMeshNo.append(a_splitD2[0])
                                        a_OTime.append(a_tmpTime)
                                        a_rSum += 1

                                    break

                for a_cnt2 in range(0, a_rSum):
                    a_sw.write(a_index[a_cnt2] +
                               "," + str(a_sTime[a_cnt2].year) + "," + str(a_sTime[a_cnt2].month) + "," + str(a_sTime[a_cnt2].day) + "," + str(a_sTime[a_cnt2].hour) + ":" + str(a_sTime[a_cnt2].minute).rjust(2, "0") +
                               "," + str(a_eTime[a_cnt2].year) + "," + str(a_eTime[a_cnt2].month) + "," + str(a_eTime[a_cnt2].day) + "," + str(a_eTime[a_cnt2].hour) + ":" + str(a_eTime[a_cnt2].minute).rjust(2, "0"))

                    for a_cnt3 in range(0, 9):
                        if (a_CLTime[a_cnt2][a_cnt3] == None):
                            a_sw.write(",")
                        else:
                            a_sw.write("," + str(a_CLTime[a_cnt2][a_cnt3].year) + "/" + str(a_CLTime[a_cnt2][a_cnt3].month) + "/" + str(a_CLTime[a_cnt2][a_cnt3].day) + " " + str(a_CLTime[a_cnt2][a_cnt3].hour) + ":" + str(a_CLTime[a_cnt2][a_cnt3].minute).rjust(2, "0"))

                    for a_cnt3 in range(0, 9):
                        a_sw.write("," + a_MeshNo[a_cnt2][a_cnt3])

                    a_sw.write("," + a_OMeshNo[a_cnt2])
                    a_sw.write("," + str(a_OTime[a_cnt2].year) + "/" + str(a_OTime[a_cnt2].month) + "/" + str(a_OTime[a_cnt2].day) + " " + str(a_OTime[a_cnt2].hour) + ":" + str(a_OTime[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfall2ByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfall2ByBlock', a_strErr + "," + sys.exc_info())

    # 発生降雨超過数【災害捕捉率】
    def _makeOccurRainfall9_1ByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeOccurRainfall9_1ByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 一連の降雨データをメモリに退避
                a_textlineR = []
                a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", a_textlineR)

                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_OverOccurRainFallNum9_1TimeSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),メッシュ番号,災害発生時刻\n")

                a_bIsSet = [False]*a_textSumR
                a_index = []
                a_sTime = []
                a_eTime = []
                a_CLTime = []
                a_MeshNo = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    if os.path.isfile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_OverOccurRainFallNum9_1TimeSymbolByBlock + ".csv") == True:
                        a_textlineD2 = []
                        a_textSumD2 = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_OverOccurRainFallNum9_1TimeSymbolByBlock + ".csv", a_textlineD2)
                        for a_cnt2 in range(1, a_textSumD2):
                            a_split1 = a_textlineD2[a_cnt2]
                            a_tmpTime1 = datetime.datetime.strptime(a_split1[1] + "/" + a_split1[2] + "/" + a_split1[3] + " " + a_split1[4], '%Y/%m/%d %H:%M')
                            a_tmpTime2 = datetime.datetime.strptime(a_split1[5] + "/" + a_split1[6] + "/" + a_split1[7] + " " + a_split1[8], '%Y/%m/%d %H:%M')
                            for a_cnt4 in range(1, a_textSumR):
                                a_splitR = a_textlineR[a_cnt4]
                                a_nowsTime = datetime.datetime.strptime(a_splitR[1] + "/" + a_splitR[2] + "/" + a_splitR[3] + " " + a_splitR[4], '%Y/%m/%d %H:%M')
                                a_noweTime = datetime.datetime.strptime(a_splitR[5] + "/" + a_splitR[6] + "/" + a_splitR[7] + " " + a_splitR[8], '%Y/%m/%d %H:%M')
                                if (a_tmpTime1 >= a_nowsTime) and (a_tmpTime1 <= a_noweTime):
                                    # 降雨範囲内で災害発生
                                    a_IsOK = False

                                    # 対象CLに災害時刻が設定されていない場合にエラー
                                    if (a_rSum <= 0):
                                        # 最初のレコード読込
                                        if (a_split1[18] != ""):
                                            a_IsOK = True
                                    else:
                                        # ２回目以降のレコード読込
                                        for a_cnt5 in range(0, a_rSum):
                                            # 時間範囲の比較
                                            if (a_tmpTime1 > a_eTime[a_cnt5]) or (a_tmpTime1 < a_sTime[a_cnt5]):
                                                # 開始時間が終了より先の場合
                                                # 終了時間が開始より前の場合
                                                if (a_split1[18] != ""):
                                                    a_IsOK = True
                                            else:
                                                a_IsOK = False
                                                break

                                        # ★重複カウント不具合
                                        if (a_IsOK == False):
                                            # 既に同一範囲内でヒットしている場合
                                            if (a_split1[18] != ""):    # 災害時刻
                                                a_tmpTime = datetime.datetime.strptime(a_split1[18], '%Y/%m/%d %H:%M')
                                                if (a_tmpTime < (a_CLTime[a_cnt5])):
                                                    a_CLTime[a_cnt5] = a_tmpTime
                                                    a_MeshNo[a_cnt5] = a_meshList[a_cnt3]

                                    if (a_IsOK == True):
                                        a_index.append(a_splitR[0])
                                        a_sTime.append(a_nowsTime)
                                        a_eTime.append(a_noweTime)
                                        a_MeshNo.append(a_meshList[a_cnt3])
                                        a_CLTime.append(datetime.datetime.strptime(a_split1[18], '%Y/%m/%d %H:%M'))   # 災害時刻
                                        #a_CLTime.append(a_split1[18])   # 災害時刻
                                        a_bIsSet[a_cnt4] = True     # ★重複カウント不具合
                                        a_rSum += 1

                                    break

                for a_cnt2 in range(0, a_rSum):
                    a_sw.write(str(a_cnt2 + 1) +
                               "," + str(a_sTime[a_cnt2].year) + "," + str(a_sTime[a_cnt2].month) + "," + str(a_sTime[a_cnt2].day) + "," + str(a_sTime[a_cnt2].hour) + ":" + str(a_sTime[a_cnt2].minute).rjust(2, "0") +
                               "," + str(a_eTime[a_cnt2].year) + "," + str(a_eTime[a_cnt2].month) + "," + str(a_eTime[a_cnt2].day) + "," + str(a_eTime[a_cnt2].hour) + ":" + str(a_eTime[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("," + a_MeshNo[a_cnt2])
                    a_sw.write("," + str(a_CLTime[a_cnt2].year) + "/" + str(a_CLTime[a_cnt2].month) + "/" + str(a_CLTime[a_cnt2].day) + " " + str(a_CLTime[a_cnt2].hour) + ":" + str(a_CLTime[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfall9_1ByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfall9_1ByBlock', a_strErr + "," + sys.exc_info())

    # 災害発生件数【災害捕捉率】
    def _makeOccurRainfall9_2ByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeOccurRainfall9_2ByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 一連の降雨データをメモリに退避
                a_textlineR = []
                a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", a_textlineR)

                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_OverOccurRainFallNum9_2TimeSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),メッシュ番号,災害発生時刻\n")

                a_bIsSet = [False]*a_textSumR
                a_index = []
                a_sTime = []
                a_eTime = []
                a_CLTime = []
                a_MeshNo = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    if os.path.isfile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_OverOccurRainFallNum9_2TimeSymbolByBlock + ".csv") == True:
                        a_textlineD2 = []
                        a_textSumD2 = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_OverOccurRainFallNum9_2TimeSymbolByBlock + ".csv", a_textlineD2)
                        for a_cnt2 in range(1, a_textSumD2):
                            a_split1 = a_textlineD2[a_cnt2]
                            a_tmpTime1 = datetime.datetime.strptime(a_split1[1] + "/" + a_split1[2] + "/" + a_split1[3] + " " + a_split1[4], '%Y/%m/%d %H:%M')
                            a_tmpTime2 = datetime.datetime.strptime(a_split1[5] + "/" + a_split1[6] + "/" + a_split1[7] + " " + a_split1[8], '%Y/%m/%d %H:%M')
                            for a_cnt4 in range(1, a_textSumR):
                                a_splitR = a_textlineR[a_cnt4]
                                a_nowsTime = datetime.datetime.strptime(a_splitR[1] + "/" + a_splitR[2] + "/" + a_splitR[3] + " " + a_splitR[4], '%Y/%m/%d %H:%M')
                                a_noweTime = datetime.datetime.strptime(a_splitR[5] + "/" + a_splitR[6] + "/" + a_splitR[7] + " " + a_splitR[8], '%Y/%m/%d %H:%M')
                                if (a_tmpTime1 >= a_nowsTime) and (a_tmpTime1 <= a_noweTime):
                                    # 降雨範囲内で災害発生
                                    a_IsOK = False

                                    # 対象CLに災害時刻が設定されていない場合にエラー
                                    if (a_split1[18] != ""):
                                        if (a_rSum <= 0):
                                            # 最初のレコード読込
                                            a_IsOK = True
                                        else:
                                            # ２回目以降のレコード読込
                                            for a_cnt5 in range(0, a_rSum):
                                                # 時間範囲の比較
                                                if (a_tmpTime1 > a_eTime[a_cnt5]) or (a_tmpTime1 < a_sTime[a_cnt5]):
                                                    # 開始時間が終了より先の場合
                                                    # 終了時間が開始より前の場合
                                                    a_IsOK = True
                                                else:
                                                    a_IsOK = False
                                                    break

                                            # ★重複カウント不具合
                                            if (a_IsOK == False) or (a_bIsSet[a_cnt4] == True):
                                                a_IsOK = False
                                                # 既に同一範囲内でヒットしている場合
                                                if (a_split1[18] != ""):    # 災害時刻
                                                    #a_split1(18)には「;」区切りで複数の災害時刻がある為、バラしてチェック
                                                    a_splitSepCL = a_CLTime[a_rSum].split(";")
                                                    a_splitSep1 = a_split1[18].split(";")
                                                    a_IsExists = False
                                                    a_AddMesh = False

                                                    a_iCntSepCL = 0
                                                    a_iCntSep1 = 0
                                                    a_IsExists = False
                                                    for a_iCntSep1 in range(0, len(a_splitSep1)):
                                                        a_tmpTime1 = datetime.datetime.strptime(a_splitSep1[a_iCntSep1], '%Y/%m/%d %H:%M')
                                                        for a_iCntSepCL in range(0, len(a_splitSepCL)):
                                                            a_tmpTime2 = datetime.datetime.strptime(a_splitSepCL[a_iCntSepCL], '%Y/%m/%d %H:%M')
                                                            if (a_tmpTime2 == a_tmpTime1):
                                                                # 同一時刻で既に災害あり
                                                                a_IsExists = False  # ★本来の仕様（同一時刻でもカウントする）
                                                                #a_IsExists = True  # ★新潟仕様（同一時刻はカウントしない）
                                                                break
                                                        if (a_IsExists == False):
                                                            # 同一時刻でない災害
                                                            a_MeshNo[a_rSum] += ";" + a_meshList[a_cnt3]
                                                            a_CLTime[a_rSum] += ";" + str(a_tmpTime1.year) + "/" + str(a_tmpTime1.month) + "/" + str(a_tmpTime1.day) + " " + str(a_tmpTime1.hour) + ":" + str(a_tmpTime1.minute).rjust(2, "0")

                                    if (a_IsOK == True):
                                        a_index.append(a_splitR[0])
                                        a_sTime.append(a_nowsTime)
                                        a_eTime.append(a_noweTime)
                                        a_CLTime.append(a_split1[18])   # 災害時刻

                                        a_splitSepCL = a_CLTime[a_rSum].aplit(";")
                                        a_splitNum = 0
                                        a_MeshNo.append("")
                                        for a_splitNum in range(0, len(a_splitSepCL)):
                                            if (a_splitNum > 0):
                                                a_MeshNo[a_rSum] += ";"
                                            a_MeshNo[a_rSum] += a_meshList[a_cnt3]

                                        a_bIsSet[a_cnt4] = True     # ★重複カウント不具合
                                        a_rSum += 1

                                    break

                for a_cnt2 in range(0, a_rSum):
                    a_sw.write(str(a_cnt2 + 1) +
                    "," + str(a_sTime[a_cnt2].year) + "," + str(a_sTime[a_cnt2].month) + "," + str(a_sTime[a_cnt2].day) + "," + str(a_sTime[a_cnt2].hour) + ":" + str(a_sTime[a_cnt2].minute).rjust(2, "0") +
                    "," + str(a_eTime[a_cnt2].year) + "," + str(a_eTime[a_cnt2].month) + "," + str(a_eTime[a_cnt2].day) + "," + str(a_eTime[a_cnt2].hour) + ":" + str(a_eTime[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("," + a_MeshNo[a_cnt2])
                    a_sw.write("," + a_CLTime[a_cnt2])

                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfall9_2ByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeOccurRainfall9_2ByBlock', a_strErr + "," + sys.exc_info())

    # 一連の発生降雨
    def _makeRainfallByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeRainfallByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,メッシュ番号(開始),メッシュ番号(終了)\n")

                a_sTime = []
                a_eTime = []
                a_CLTime = []
                a_MeshNo = []
                a_rMeshNoS = []
                a_rMeshNoE = []
                a_chkOK = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    if os.path.isfile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_ChainOccurRainfallSymbolByBlock + ".csv") == True:
                        a_textlineR = []
                        a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_ChainOccurRainfallSymbolByBlock + ".csv", a_textlineR)

                        for a_cnt in range(1, a_textSumR):
                            a_split1 = a_textlineR[a_cnt]
                            a_IsOK = False
                            a_IsChk = False

                            # 対象CLに災害時刻が設定されていない場合にエラー
                            if (a_rSum <= 0):
                                # 最初のレコード読込
                                a_IsOK = True
                            else:
                                # ２回目以降のレコード読込
                                a_nowsTime = datetime.datetime.strptime(a_split1[1] + "/" + a_split1[2] + "/" + a_split1[3] + " " + a_split1[4], '%Y/%m/%d %H:%M')
                                a_noweTime = datetime.datetime.strptime(a_split1[5] + "/" + a_split1[6] + "/" + a_split1[7] + " " + a_split1[8], '%Y/%m/%d %H:%M')
                                for a_cnt2 in range(0, a_rSum):
                                    # 時間範囲の比較
                                    if (a_nowsTime > a_eTime[a_cnt2]) or (a_noweTime < a_sTime[a_cnt2]) :
                                        # 開始時間が終了より先の場合
                                        # 終了時間が開始より前の場合
                                        a_IsOK = True
                                    else:
                                        if (a_chkOK[a_cnt2] == True):
                                            a_IsOK = False
                                            if (a_nowsTime < a_sTime[a_cnt2]):
                                                # 開始時間が開始時間より前の場合
                                                a_sTime[a_cnt2] = a_nowsTime
                                                a_rMeshNoS[a_cnt2] = a_meshList[a_cnt3]
                                            if (a_noweTime > a_eTime[a_cnt2]):
                                                # 終了時間が終了時間より先の場合
                                                a_eTime[a_cnt2] = a_noweTime
                                                a_rMeshNoE[a_cnt2] = a_meshList[a_cnt3]
                                            for a_cnt4 in range(9, 18):
                                                if (a_split1[a_cnt4] != ""):
                                                    a_tmpTime = datetime.datetime.strptime(a_split1[a_cnt4], '%Y/%m/%d %H:%M')
                                                    if (a_CLTime[a_cnt2][a_cnt4 - 9] == None):
                                                        a_CLTime[a_cnt2][a_cnt4 - 9] = a_tmpTime
                                                        a_MeshNo[a_cnt2][a_cnt4 - 9] = a_meshList[a_cnt3]
                                                    else:
                                                        if (a_tmpTime < a_CLTime[a_cnt2][a_cnt4 - 9]):
                                                            a_CLTime[a_cnt2][a_cnt4 - 9] = a_tmpTime
                                                            a_MeshNo[a_cnt2][a_cnt4 - 9] = a_meshList[a_cnt3]
                                            a_ChkIdx = a_cnt2
                                            a_IsChk = True
                                            break

                            if (a_IsOK == True):
                                a_sTime.append(datetime.datetime.strptime(a_split1[1] + "/" + a_split1[2] + "/" + a_split1[3] + " " + a_split1[4], '%Y/%m/%d %H:%M'))
                                a_eTime.append(datetime.datetime.strptime(a_split1[5] + "/" + a_split1[6] + "/" + a_split1[7] + " " + a_split1[8], '%Y/%m/%d %H:%M'))

                                a_CLTime.append([None]*9)
                                a_MeshNo.append([""]*9)
                                a_rMeshNoS.append("")
                                a_rMeshNoE.append("")
                                a_chkOK.append(True)

                                for a_cnt2 in range(9, 18):
                                    if (a_split1[a_cnt2] != ""):
                                        a_CLTime[a_rSum][a_cnt2 - 9] = datetime.datetime.strptime(a_split1[a_cnt2], '%Y/%m/%d %H:%M')
                                        a_MeshNo[a_rSum][a_cnt2 - 9] = a_meshList[a_cnt3]

                                a_rMeshNoS[a_rSum] = a_meshList[a_cnt3]
                                a_rMeshNoE[a_rSum] = a_meshList[a_cnt3]
                                a_chkOK[a_rSum] = True
                                a_rSum += 1
                            else:
                                # 異なる範囲のものが繋がる可能性があった。
                                if (a_IsChk == True):
                                    for a_cnt5 in range(0, a_rSum):
                                        if (a_cnt5 != a_ChkIdx) and (a_chkOK[a_cnt5] == True):
                                            # 時間範囲の比較
                                            if (a_sTime[a_cnt5] > a_eTime[a_ChkIdx]) or (a_eTime[a_cnt5] < a_sTime[a_ChkIdx]):
                                                # 開始時間が終了より先の場合
                                                # 終了時間が開始より前の場合
                                                a_dmy = 1
                                            else:
                                                if (a_sTime[a_cnt5] < a_sTime[a_ChkIdx]):
                                                    # 開始時間が開始時間より前の場合
                                                    a_sTime[a_ChkIdx] = a_sTime[a_cnt5]
                                                    a_rMeshNoS[a_ChkIdx] = a_rMeshNoS[a_cnt5]
                                                if (a_eTime[a_cnt5] > a_eTime[a_ChkIdx]):
                                                    # 終了時間が終了時間より先の場合
                                                    a_eTime[a_ChkIdx] = a_eTime[a_cnt5]
                                                    a_rMeshNoE[a_ChkIdx] = a_rMeshNoE[a_cnt5]
                                                for a_cnt4 in range(9, 18):
                                                    if (a_CLTime[a_cnt5][a_cnt4 - 9] != None):
                                                        a_tmpTime = a_CLTime[a_cnt5][a_cnt4 - 9]
                                                        if (a_CLTime[a_ChkIdx][a_cnt4 - 9] == None):
                                                            a_CLTime[a_ChkIdx][a_cnt4 - 9] = a_tmpTime
                                                            a_MeshNo[a_ChkIdx][a_cnt4 - 9] = a_MeshNo[a_cnt5][a_cnt4 - 9]
                                                        else:
                                                            if (a_tmpTime < a_CLTime[a_ChkIdx][a_cnt4 - 9]):
                                                                a_CLTime[a_ChkIdx][a_cnt4 - 9] = a_tmpTime
                                                                a_MeshNo[a_ChkIdx][a_cnt4 - 9] = a_MeshNo[a_cnt5][a_cnt4 - 9]
                                                a_chkOK[a_cnt5] = False

                for a_cnt2 in range(0, a_rSum):
                    if (a_chkOK[a_cnt2] == True):
                        a_sw.write(str(a_cnt2 + 1) +
                                   "," + str(a_sTime[a_cnt2].year) + "," + str(a_sTime[a_cnt2].month) + "," + str(a_sTime[a_cnt2].day) + "," + str(a_sTime[a_cnt2].hour) + ":" + str(a_sTime[a_cnt2].minute).rjust(2, "0") +
                                   "," + str(a_eTime[a_cnt2].year) + "," + str(a_eTime[a_cnt2].month) + "," + str(a_eTime[a_cnt2].day) + "," + str(a_eTime[a_cnt2].hour) + ":" + str(a_eTime[a_cnt2].minute).rjust(2, "0"))

                        for a_cnt3 in range(0, 9):
                            if (a_CLTime[a_cnt2][a_cnt3] == None):
                                a_sw.write(",")
                            else:
                                a_sw.write("," + str(a_CLTime[a_cnt2][a_cnt3].year) + "/" + str(a_CLTime[a_cnt2][a_cnt3].month) + "/" + str(a_CLTime[a_cnt2][a_cnt3].day) + " " + str(a_CLTime[a_cnt2][a_cnt3].hour) + ":" + str(a_CLTime[a_cnt2][a_cnt3].minute).rjust(2, "0"))

                        for a_cnt3 in range(0, 9):
                            a_sw.write("," + a_MeshNo[a_cnt2][a_cnt3])

                        a_sw.write("," + a_rMeshNoS[a_cnt2] + "," + a_rMeshNoE[a_cnt2])

                        a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeRainfallByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeRainfallByBlock', a_strErr + "," + sys.exc_info())

    # 一連の発生降雨
    def _makeRainfall2ByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeRainfall2ByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfall2SymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,メッシュ番号(開始),メッシュ番号(終了)\n")

                a_bIsSet = [False]*a_textSumR
                a_sTime = []
                a_eTime = []
                a_CLTime = []
                a_MeshNo = []
                a_rMeshNoS = []
                a_rMeshNoE = []
                a_chkOK = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    if os.path.isfile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_ChainOccurRainfall2SymbolByBlock + ".csv") == True:
                        a_textlineR = []
                        a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_ChainOccurRainfall2SymbolByBlock + ".csv", a_textlineR)

                        for a_cnt in range(1, a_textSumR):
                            a_split1 = a_textlineR[a_cnt]
                            a_IsOK = False
                            a_IsChk = False

                            # 対象CLに災害時刻が設定されていない場合にエラー
                            if (a_rSum <= 0):
                                # 最初のレコード読込
                                a_IsOK = True
                            else:
                                # ２回目以降のレコード読込
                                a_nowsTime = datetime.datetime.strptime(a_split1[1] + "/" + a_split1[2] + "/" + a_split1[3] + " " + a_split1[4], '%Y/%m/%d %H:%M')
                                a_noweTime = datetime.datetime.strptime(a_split1[5] + "/" + a_split1[6] + "/" + a_split1[7] + " " + a_split1[8], '%Y/%m/%d %H:%M')
                                for a_cnt2 in range(0, a_rSum):
                                    # 時間範囲の比較
                                    if (a_nowsTime > a_eTime[a_cnt2]) or (a_noweTime < a_sTime[a_cnt2]) :
                                        # 開始時間が終了より先の場合
                                        # 終了時間が開始より前の場合
                                        a_IsOK = True
                                    else:
                                        if (a_chkOK[a_cnt2] == True):
                                            a_IsOK = False
                                            if (a_nowsTime < a_sTime[a_cnt2]):
                                                # 開始時間が開始時間より前の場合
                                                a_sTime[a_cnt2] = a_nowsTime
                                                a_rMeshNoS[a_cnt2] = a_meshList[a_cnt3]
                                            if (a_noweTime > a_eTime[a_cnt2]):
                                                # 終了時間が終了時間より先の場合
                                                a_eTime[a_cnt2] = a_noweTime
                                                a_rMeshNoE[a_cnt2] = a_meshList[a_cnt3]
                                            for a_cnt4 in range(9, 18):
                                                if (a_split1[a_cnt4] != ""):
                                                    a_tmpTime = datetime.datetime.strptime(a_split1[a_cnt4], '%Y/%m/%d %H:%M')
                                                    if (a_CLTime[a_cnt2][a_cnt4 - 9] == None):
                                                        a_CLTime[a_cnt2][a_cnt4 - 9] = a_tmpTime
                                                        a_MeshNo[a_cnt2][a_cnt4 - 9] = a_meshList[a_cnt3]
                                                    else:
                                                        if (a_tmpTime < a_CLTime[a_cnt2][a_cnt4 - 9]):
                                                            a_CLTime[a_cnt2][a_cnt4 - 9] = a_tmpTime
                                                            a_MeshNo[a_cnt2][a_cnt4 - 9] = a_meshList[a_cnt3]
                                            a_ChkIdx = a_cnt2
                                            a_IsChk = True
                                            break

                            if (a_IsOK == True):
                                a_sTime.append(datetime.datetime.strptime(a_split1[1] + "/" + a_split1[2] + "/" + a_split1[3] + " " + a_split1[4], '%Y/%m/%d %H:%M'))
                                a_eTime.append(datetime.datetime.strptime(a_split1[5] + "/" + a_split1[6] + "/" + a_split1[7] + " " + a_split1[8], '%Y/%m/%d %H:%M'))

                                a_CLTime.append([None]*9)
                                a_MeshNo.append([""]*9)

                                for a_cnt2 in range(9, 18):
                                    if (a_split1[a_cnt2] != ""):
                                        a_CLTime[a_rSum][a_cnt2 - 9] = datetime.datetime.strptime(a_split1[a_cnt2])
                                        a_MeshNo[a_rSum][a_cnt2 - 9] = a_meshList[a_cnt3]

                                a_rMeshNoS[a_rSum] = a_meshList[a_cnt3]
                                a_rMeshNoE[a_rSum] = a_meshList[a_cnt3]
                                a_chkOK[a_rSum] = True
                                a_rSum += 1
                            else:
                                # 異なる範囲のものが繋がる可能性があった。
                                if (a_IsChk == True):
                                    for a_cnt5 in range(0, a_rSum):
                                        if (a_cnt5 != a_ChkIdx) and (a_chkOK[a_cnt5] == True):
                                            # 時間範囲の比較
                                            if (a_sTime[a_cnt5] > a_eTime[a_ChkIdx]) or (a_eTime[a_cnt5] < a_sTime[a_ChkIdx]):
                                                # 開始時間が終了より先の場合
                                                # 終了時間が開始より前の場合
                                                a_dmy = 1
                                            else:
                                                if (a_sTime[a_cnt5] < a_sTime[a_ChkIdx]):
                                                    # 開始時間が開始時間より前の場合
                                                    a_sTime[a_ChkIdx] = a_sTime[a_cnt5]
                                                    a_rMeshNoS[a_ChkIdx] = a_rMeshNoS[a_cnt5]
                                                if (a_eTime[a_cnt5] > a_eTime[a_ChkIdx]):
                                                    # 終了時間が終了時間より先の場合
                                                    a_eTime[a_ChkIdx] = a_eTime[a_cnt5]
                                                    a_rMeshNoE[a_ChkIdx] = a_rMeshNoE[a_cnt5]
                                                for a_cnt4 in range(9, 18):
                                                    if (a_CLTime[a_cnt5][a_cnt4 - 9] != None):
                                                        a_tmpTime = a_CLTime[a_cnt5][a_cnt4 - 9]
                                                        if (a_CLTime[a_ChkIdx][a_cnt4 - 9] == None):
                                                            a_CLTime[a_ChkIdx][a_cnt4 - 9] = a_tmpTime
                                                            a_MeshNo[a_ChkIdx][a_cnt4 - 9] = a_MeshNo[a_cnt5][a_cnt4 - 9]
                                                        else:
                                                            if (a_tmpTime < a_CLTime[a_ChkIdx][a_cnt4 - 9]):
                                                                a_CLTime[a_ChkIdx][a_cnt4 - 9] = a_tmpTime
                                                                a_MeshNo[a_ChkIdx][a_cnt4 - 9] = a_MeshNo[a_cnt5][a_cnt4 - 9]
                                                a_chkOK[a_cnt5] = False

                for a_cnt2 in range(0, a_rSum):
                    if (a_chkOK[a_cnt2] == True):
                        a_sw.write(str(a_cnt2 + 1) +
                                   "," + str(a_sTime[a_cnt2].year) + "," + str(a_sTime[a_cnt2].month) + "," + str(a_sTime[a_cnt2].day) + "," + str(a_sTime[a_cnt2].hour) + ":" + str(a_sTime[a_cnt2].minute).rjust(2, "0") +
                                   "," + str(a_eTime[a_cnt2].year) + "," + str(a_eTime[a_cnt2].month) + "," + str(a_eTime[a_cnt2].day) + "," + str(a_eTime[a_cnt2].hour) + ":" + str(a_eTime[a_cnt2].minute).rjust(2, "0"))

                    for a_cnt3 in range(0, 9):
                        if (a_CLTime[a_cnt2][a_cnt3] == None):
                            a_sw.write(",")
                        else:
                            a_sw.write("," + str(a_CLTime[a_cnt2][a_cnt3].year) + "/" + str(a_CLTime[a_cnt2][a_cnt3].month) + "/" + str(a_CLTime[a_cnt2][a_cnt3].day) + " " + str(a_CLTime[a_cnt2][a_cnt3].hour) + ":" + str(a_CLTime[a_cnt2][a_cnt3].minute).rjust(2, "0"))

                    for a_cnt3 in range(0, 9):
                        a_sw.write("," + a_MeshNo[a_cnt2][a_cnt3])

                    a_sw.write("," + a_rMeshNoS[a_cnt2] + "," + a_rMeshNoE[a_cnt2])

                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeRainfall2ByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeRainfall2ByBlock', a_strErr + "," + sys.exc_info())

    # 警戒情報リードタイム/RBFN越リードタイム
    def _makeReadTimeByBlock(self, h_sKind):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeReadTimeByBlock', a_strErr)

        try:
            # リードタイムのデータをメモリに退避
            if (h_sKind == self.com.g_CalcRBFNReadTimeSymbolByBlock):
                a_FName = self.com.g_CalcRBFNReadTimeSymbol
            else:
                a_FName = self.com.g_CalcCautionAnnounceReadTimeSymbol
            a_textlineD2 = []
            a_textSumD2 = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_FName + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", a_textlineD2)

            # 災害発生降雨
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 一連の降雨データをメモリに退避
                a_textlineR = []
                a_textSumR = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", a_textlineR)

                a_sw = open(self.com.g_OutPath + "\\block\\" + h_sKind + "-" + self.blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("データ番号,年(S),月(S),日(S),時(S),年(E),月(E),日(E),時(E),メッシュ番号,年,月,日,時,メッシュ番号,年,月,日,時,リードタイム")
                if (h_sKind == self.com.g_CalcRBFNReadTimeSymbolByBlock):
                    a_sw.write(",RBFN値")
                a_sw.write("\n")

                a_index = []
                a_sTime = []
                a_eTime = []
                a_RTimeS = []
                a_RTimeE = []
                a_RTimeV = []
                a_MeshNoS = []
                a_MeshNoE = []
                a_RBFN = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    for a_cnt2 in range(1, a_textSumD2):
                        a_splitD2 = a_textlineD2[a_cnt2]
                        if (a_splitD2[0] == a_meshList[a_cnt3]):
                            # メッシュ番号が一致
                            a_tmpTime1 = datetime.datetime.strptime(a_splitD2[1] + "/" + a_splitD2[2] + "/" + a_splitD2[3] + " " + a_splitD2[4], '%Y/%m/%d %H:%M')
                            a_tmpTime2 = datetime.datetime.strptime(a_splitD2[5] + "/" + a_splitD2[6] + "/" + a_splitD2[7] + " " + a_splitD2[8], '%Y/%m/%d %H:%M')
                            for a_cnt4 in range(1, a_textSumR):
                                a_splitR = a_textlineR[a_cnt4]
                                a_nowsTime = datetime.datetime.strptime(a_splitR[1] + "/" + a_splitR[2] + "/" + a_splitR[3] + " " + a_splitR[4], '%Y/%m/%d %H:%M')
                                a_noweTime = datetime.datetime.strptime(a_splitR[5] + "/" + a_splitR[6] + "/" + a_splitR[7] + " " + a_splitR[8], '%Y/%m/%d %H:%M')
                                if (a_tmpTime1 >= a_nowsTime) and (a_tmpTime1 <= a_noweTime):
                                    # 降雨範囲内で災害発生
                                    a_IsOK = False

                                    if (a_rSum <= 0):
                                    # 最初のレコード読込
                                        a_IsOK = True
                                    else:
                                        # ２回目以降のレコード読込
                                        for a_cnt5 in range(0, a_rSum):
                                            # 時間範囲の比較
                                            if (a_tmpTime1 > a_eTime[a_cnt5]) or (a_tmpTime1 < a_sTime[a_cnt5]):
                                                # 開始時間が終了より先の場合
                                                # 終了時間が開始より前の場合
                                                a_IsOK = True
                                            else:
                                                a_IsOK = False
                                                if (a_tmpTime1 < a_RTimeS[a_rSum]):
                                                    # リードタイムはブロック内の最速超過メッシュと最速災害発生時刻の差
                                                    a_MeshNoS[a_rSum] = a_splitD2[0]
                                                    a_RTimeS[a_rSum] = a_tmpTime1
                                                    a_RTimeV[a_rSum] = a_splitD2[9]
                                                    if (h_sKind == self.com.g_CalcRBFNReadTimeSymbolByBlock):
                                                        a_RBFN[a_rSum] = a_splitD2[10]
                                                #elif (a_tmpTime1 == a_RTimeS[a_rSum]):
                                                #    # 同じ開始時刻

                                                # リードタイムはブロック内の最速超過メッシュと最速災害発生時刻の差
                                                if (a_tmpTime2 < a_RTimeE[a_rSum]):
                                                    a_MeshNoE[a_rSum] = a_splitD2[0]
                                                    a_RTimeE[a_rSum] = a_tmpTime2

                                                a_delta = a_RTimeE[a_rSum] - a_RTimeS[a_rSum]
                                                a_RTimeV[a_rSum] = a_delta.total.minutes()
                                                break

                                    if (a_IsOK == True):
                                        a_index.append(a_splitR[0])
                                        a_sTime.append(a_nowsTime)
                                        a_eTime.append(a_noweTime)
                                        a_RTimeS.append(a_tmpTime1)
                                        a_RTimeE.append(a_tmpTime2)
                                        a_RTimeV.append(a_splitD2[9])
                                        a_MeshNoS.append(a_splitD2[0])
                                        a_MeshNoE.append(a_splitD2[0])
                                        if (h_sKind == self.com.g_CalcRBFNReadTimeSymbolByBlock):
                                            a_RBFN.append(a_splitD2[10])
                                        a_rSum += 1

                                    break

                for a_cnt2 in range(0, a_rSum):
                    a_sw.write(str(a_cnt2 + 1) +
                    "," + str(a_sTime[a_cnt2].year) + "," + str(a_sTime[a_cnt2].month) + "," + str(a_sTime[a_cnt2].day) + "," + str(a_sTime[a_cnt2].hour) + ":" + str(a_sTime[a_cnt2].minute).rjust(2, "0") +
                    "," + str(a_eTime[a_cnt2].year) + "," + str(a_eTime[a_cnt2].month) + "," + str(a_eTime[a_cnt2].day) + "," + str(a_eTime[a_cnt2].hour) + ":" + str(a_eTime[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("," + a_MeshNoS[a_cnt2])
                    a_sw.write(
                    "," + str(a_RTimeS[a_cnt2].year) + "," + str(a_RTimeS[a_cnt2].month) + "," + str(a_RTimeS[a_cnt2].day) + "," + str(a_RTimeS[a_cnt2].hour) + ":" + str(a_RTimeS[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("," + a_MeshNoE[a_cnt2])
                    a_sw.write(
                    "," + str(a_RTimeE[a_cnt2].year) + "," + str(a_RTimeE[a_cnt2].month) + "," + str(a_RTimeE[a_cnt2].day) + "," + str(a_RTimeE[a_cnt2].hour) + ":" + str(a_RTimeE[a_cnt2].minute).rjust(2, "0"))

                    a_sw.write("," + a_RTimeV[a_cnt2])

                    if (h_sKind == self.com.g_CalcRBFNReadTimeSymbolByBlock):
                        a_sw.write("," + a_RBFN[a_cnt2])

                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeReadTimeByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeReadTimeByBlock', a_strErr + "," + sys.exc_info())

    # ブロック毎集計処理
    def _makeStatisticsByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeStatisticsByBlock', a_strErr)

        try:
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_BlockStatisticsSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", "w", encoding="shift_jis")
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                a_meshNo = ""

                # 空文字もしくは、0は無効→2006.04.07
                a_split = self.g_blockNoList[a_cnt1].split(",")
                a_len = len(a_split)
                a_strTmp = ""
                a_cnt3 = 0
                for a_cnt2 in range(0, a_len):
                    if (a_split[a_cnt2].strip() != "") and (a_split[a_cnt2].strip() != "0"):
                        if (a_cnt3 > 0):
                            a_strTmp += ","
                        a_strTmp += a_split[a_cnt2].strip()
                        a_cnt3 += 1

                if (a_strTmp != ""):
                    a_split = a_strTmp.split(",")
                    a_sw.write(self.g_blockNameList[a_cnt1] + "\n")    # メッシュ番号リスト出力の廃止
                    a_sw.write(",0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1\n")

                    a_a = [0]*9
                    a_b = [0]*9
                    a_c = [0]*9

                    # 全降雨超過数
                    a_sw.write("全降雨超過数")
                    a_sr = open(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    while a_strTmp:
                        a_split = a_strTmp.split(",")
                        for a_cnt2 in range(1, 10):
                            if (a_split[a_cnt2 + 8] != ""):
                                a_a[a_cnt2 - 1] += 1
                                if (a_meshNo == ""):
                                    a_meshNo = a_split[a_cnt2 + 17].strip()
                        a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_sr.close()
                    for a_cnt2 in range(1, 10):
                        a_sw.write("," + str(a_a[a_cnt2 - 1]))
                    a_sw.write("\n")

                    # 非発生降雨超過数
                    a_sw.write("非発生降雨超過数")
                    a_sr = open(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOnlyOccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    while a_strTmp:
                        a_split = a_strTmp.split(",")
                        for a_cnt2 in range(1, 10):
                            if (a_split[a_cnt2 + 8] != ""):
                                a_b[a_cnt2 - 1] += 1
                        a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_sr.close()
                    for a_cnt2 in range(1, 10):
                        a_sw.write("," + str(a_b[a_cnt2 - 1]))
                    a_sw.write("\n")

                    # 発生降雨超過数
                    a_sw.write("発生降雨超過数")
                    a_sr = open(self.com.g_OutPath + "\\block\\" + self.com.g_OccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_cSum = 0
                    while a_strTmp:
                        a_split = a_strTmp.split(",")
                        for a_cnt2 in range(1, 10):
                            if (a_split[a_cnt2 + 8] != ""):
                                a_c[a_cnt2 - 1] += 1
                        a_cSum += 1
                        a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_sr.close()
                    for a_cnt2 in range(1, 10):
                        a_sw.write("," + str(a_c[a_cnt2 - 1]))
                    a_sw.write("\n")

                    # 災害捕捉率
                    a_sw.write("災害捕捉率")
                    for a_cnt2 in range(1, 10):
                        if a_c[a_cnt2 -1] > 0 and a_cSum > 0:
                            a_sw.write("," + str((float(a_c[a_cnt2]) / float(a_cSum)) * 100))
                        else:
                            a_sw.write(",0")
                    a_sw.write("\n")

                    a_sw.write("\n")
            a_sw.close()
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock', a_strErr + "," + sys.exc_info())

    # ブロック毎集計処理2
    def _makeStatisticsByBlock2(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeStatisticsByBlock2', a_strErr)

        try:
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_BlockStatisticsSymbol2 + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", "w", encoding="shift_jis")
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                a_9_1 = 0
                a_9_2 = 0
                a_a = 0
                a_b = 0
                a_w = 0
                a_meshNo = ""
                # 空文字もしくは、0は無効→2006.04.07
                a_split = self.g_blockNoList[a_cnt1].split(",")
                a_len = len(a_split)
                a_strTmp = ""
                a_cnt3 = 0
                for a_cnt2 in range(0, a_len):
                    if (a_split[a_cnt2].strip() != "") and (a_split[a_cnt2].strip() != "0"):
                        if (a_cnt3 > 0):
                            a_strTmp += ","
                        a_strTmp += a_split[a_cnt2].strip()
                        a_cnt3 += 1

                if (a_strTmp != ""):
                    a_splitB = a_strTmp.split(",")
                    a_meshNoCOR = a_splitB[0]   # ブロック最初のメッシュ番号
                    # ブロックの最初のメッシュがない場合エラーとなる
                    a_dKikan = 0
                    for a_cnt2 in range(0, len(a_splitB)):
                        if os.path.isfile(self.com.g_OutPath + "\\" + a_splitB[a_cnt2] + "\\" + self.com.g_AllRainfallSymbol + str(self.com.g_TargetStartYear) + ".csv") == True:
                            a_dKikan = self.com.GetTargetYearByMesh(self.com.g_TargetStartYear, self.com.g_TargetEndYear,self.com.g_OutPath, a_splitB[a_cnt2])
                            break

                    a_sw.write(self.g_blockNameList[a_cnt1])
                    a_sw.write(",any")

                    # 災害発生降雨の読込
                    a_textlineOC = []
                    a_textSumOC = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_OccurRainfall2SymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv", a_textlineOC)
                    for a_cnt3 in range(1, a_textSumOC):
                        if (a_meshNo == ""):
                            a_split = a_textlineOC[a_cnt3]
                            for a_cnt2 in range(1, 10):
                                if (a_split[a_cnt2 + 17].strip() != ""):
                                    a_meshNo = a_split[a_cnt2 + 17].strip()
                                    break
                        if (a_meshNo != ""):
                            a_meshNo = a_split[27].strip()

                    # 一連の発生降雨の読込
                    a_textlineCOR = []
                    a_a = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv", a_textlineCOR)

                    # 非発生降雨の読込
                    a_textlineNCOR = []
                    a_b = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_ChainOccurRainfallSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv", a_textlineNCOR)

                    # 災害発生件数の取得
                    a_SaigaiSum = 0
                    for a_cntD in range(1, self.com.g_textSum_DisasterFile):
                        a_splitD = self.com.g_textline_DisasterFile[a_cntD]
                        for a_cnt2 in range(0, len(a_splitB)):
                            if (a_splitD[0] == a_splitB[a_cnt2]):
                                a_SaigaiSum += 1

                    # 降雨数を取得
                    a_findDSum = 0
                    a_findKORMsno = []
                    a_findKORTime = []
                    for a_cnt in range(1, a_textSumOC):
                        a_split = a_textlineOC[a_cnt]   # 災害発生降雨【ブロック】
                        a_mSTime = datetime.datetime.strptime(a_split[1] + "/" + a_split[2] + "/" + a_split[3] + " " + a_split[4], '%Y/%m/%d %H:%M')
                        a_mETime = datetime.datetime.strptime(a_split[5] + "/" + a_split[6] + "/" + a_split[7] + " " + a_split[8], '%Y/%m/%d %H:%M')
                        a_IsOccur = False
                        for a_cntD in range(1, self.com.g_textSum_DisasterFile):
                            a_splitD = self.com.g_textline_DisasterFile[a_cntD]
                            for a_cnt2 in range(0, len(a_splitB)):
                                if (a_splitD[0].strip() == a_splitB[a_cnt2]):
                                    # メッシュ番号が同じ
                                    a_mTime = datetime.datetime.strptime(a_splitD[1] + "/" + a_splitD[2] + "/" + a_splitD[3] + " " + a_splitD[4], '%Y/%m/%d %H:%M')
                                    if (a_mTime >= a_mSTime) and (a_mTime <= a_mETime):
                                        # 災害が一連の降雨内である
                                        # 発生降雨フラグが「*」の場合
                                        for a_cntA in range(0, self.com.g_textSum_CautionAnnounceFile):
                                            a_splitA = self.com.g_textline_CautionAnnounceFile[a_cntA]  # 土砂災害警戒情報ファイル
                                            if (a_splitA[0].strip() == a_splitB[a_cnt2]):
                                                # メッシュ番号が同じ
                                                a_sTime = datetime.datetime.strptime(a_splitA[1] + "/" + a_splitA[2] + "/" + a_splitA[3] + " " + a_splitA[4], '%Y/%m/%d %H:%M')
                                                a_eTime = datetime.datetime.strptime(a_splitA[5] + "/" + a_splitA[6] + "/" + a_splitA[7] + " " + a_splitA[8], '%Y/%m/%d %H:%M')
                                                # 警戒発表以前に災害発生
                                                if (a_mTime < a_sTime):
                                                    break

                                                if (a_mTime >= a_sTime) and (a_mTime <= a_eTime):
                                                    # 年月日時が警戒発表の範囲内
                                                    if (a_IsOccur == False):
                                                        a_findDSum += 1
                                                        a_findKORMsno.append(a_splitD[0].strip())   # メッシュ番号
                                                        a_findKORTime.append(a_splitD[1] + "/" + a_splitD[2] + "/" + a_splitD[3] + " " + a_splitD[4])   # 災害時刻
                                                        a_IsOccur = True
                                                    break

                                        if (a_IsOccur == True):
                                            break

                    # 件数を取得
                    a_Sum = 0
                    a_findKOSMsno = []
                    a_findKOSTime = []
                    for a_cntD in range(1, self.com.g_textSum_DisasterFile):
                        a_splitD = self.com.g_textline_DisasterFile[a_cntD]
                        for a_cnt2 in range(0, len(a_splitB)):
                            if (a_splitD[0].strip() == a_splitB[a_cnt2]):
                                # メッシュ番号が同じ
                                a_mTime = datetime.datetime.strptime(a_splitD[1] + "/" + a_splitD[2] + "/" + a_splitD[3] + " " + a_splitD[4], '%Y/%m/%d %H:%M')
                                for a_cnt in range(0, self.com.g_textSum_CautionAnnounceFile):
                                    a_split = self.com.g_textline_CautionAnnounceFile[a_cnt]  # 土砂災害警戒情報ファイル
                                    if (a_split[0].strip() == a_splitB[a_cnt2]):
                                        # メッシュ番号が同じ
                                        a_sTime = datetime.datetime.strptime(a_split[1] + "/" + a_split[2] + "/" + a_split[3] + " " + a_split[4], '%Y/%m/%d %H:%M')
                                        a_eTime = datetime.datetime.strptime(a_split[5] + "/" + a_split[6] + "/" + a_split[7] + " " + a_split[8], '%Y/%m/%d %H:%M')
                                        if (a_mTime >= a_sTime) and (a_mTime <= a_eTime):
                                            a_Sum += 1
                                            a_findKOSMsno.append(a_splitD[0].strip())   # メッシュ番号
                                            a_findKOSTime.append(a_splitD[1] + "/" + a_splitD[2] + "/" + a_splitD[3] + " " + a_splitD[4])   # 災害時刻

                    # 警戒発表降雨数を取得
                    a_HSum = 0
                    a_KHrainS = []
                    a_KHrainE = []
                    a_KHmeshNoS = []
                    a_KHmeshNoE = []
                    for a_cnt in range(1, a_a):
                        a_split = a_textlineCOR[a_cnt]
                        a_mSTime = datetime.datetime.strptime(a_split[1] + "/" + a_split[2] + "/" + a_split[3] + " " + a_split[4], '%Y/%m/%d %H:%M')
                        a_mETime = datetime.datetime.strptime(a_split[5] + "/" + a_split[6] + "/" + a_split[7] + " " + a_split[8], '%Y/%m/%d %H:%M')
                        a_IsOccur = False
                        for a_cntD in range(0, self.com.g_textSum_CautionAnnounceFile):
                            a_splitA = self.com.g_textline_CautionAnnounceFile[a_cntD]  # 土砂災害警戒情報ファイル
                            for a_cnt2 in range(0, len(a_splitB)):
                                if (a_splitA[0].strip() == a_splitB[a_cnt2]):
                                    # メッシュ番号が同じ
                                    a_sTime = datetime.datetime.strptime(a_splitA[1] + "/" + a_splitA[2] + "/" + a_splitA[3] + " " + a_splitA[4], '%Y/%m/%d %H:%M')
                                    a_eTime = datetime.datetime.strptime(a_splitA[5] + "/" + a_splitA[6] + "/" + a_splitA[7] + " " + a_splitA[8], '%Y/%m/%d %H:%M')
                                    # 解除の日時はチェックする必要なし？
                                    if (a_sTime >= a_mSTime) and (a_sTime <= a_mETime):
                                        # 年月日時が警戒発表の範囲内
                                        if (a_IsOccur == False):
                                            a_HSum += 1
                                            a_KHrainS.append(a_split[1] + "/" + a_split[2] + "/" + a_split[3] + " " + a_split[4])
                                            a_KHrainE.append(a_split[5] + "/" + a_split[6] + "/" + a_split[7] + " " + a_split[8])
                                            a_KHmeshNoS.append(a_split[27])
                                            a_KHmeshNoE.append(a_split[28])
                                        a_IsOccur = True
                                        break

                    # ①土砂災害警戒情報の災害捕捉率
                    # 警戒情報の災害捕捉率【降雨数】
                    if (a_meshNo != ""):
                        a_sw.write("警戒情報の災害捕捉率【降雨数】" + "," + str((a_findDSum / (a_textSumOC - 1)) * 100))
                        a_sw.write(",警戒発表中災害降雨数⇒," + str(a_findDSum) + ",災害発生降雨数⇒," + str(a_textSumOC - 1))
                        a_sw.write(",災害時刻⇒")
                        for a_cntD in range(0, a_findDSum):
                            a_sw.write("," + a_findKORMsno[a_cntD] + "#" + a_findKORTime[a_cntD])
                        a_sw.write("\n")
                    else:
                        a_sw.write("警戒情報の災害捕捉率【降雨数】" + ",無し\n")

                    # 警戒情報の災害捕捉率【件数】
                    if (a_meshNo != ""):
                        a_sw.write("警戒情報の災害捕捉率【件数】" + "," + str((a_Sum / a_SaigaiSum) * 100))
                        a_sw.write(",警戒発表中の災害件数⇒," + a_Sum.ToString() + ",災害発生件数⇒," + str(a_SaigaiSum))
                        a_sw.write(",災害時刻⇒")
                        for a_cntD in range(0, a_Sum):
                            a_sw.write("," + a_findKOSMsno[a_cntD] + "#" + a_findKOSTime[a_cntD])
                        a_sw.write("\n")
                    else:
                        a_sw.write("警戒情報の災害捕捉率【件数】" + ",無し\n")

                    # ③土砂災害警戒情報の発表頻度
                    a_sw.write("警戒情報の発表頻度")
                    if a_HSum > 0 and a_dKikan > 0:
                        a_sw.write("," + str((float(a_HSum) / float(a_dKikan))) + ",警戒情報発表降雨数⇒," + str(a_HSum) + ",期間⇒," + str(a_dKikan))
                        a_sw.write(",一連降雨期間⇒")
                        for a_cntD in range(0, a_HSum):
                            a_sw.write(",開始" + a_KHmeshNoS[a_cntD] + "#" + a_KHrainS[a_cntD] + "　終了" + a_KHmeshNoE[a_cntD] + "#" + a_KHrainE[a_cntD])
                    else:
                        a_sw.write(",0,警戒情報発表降雨数⇒," + str(a_HSum) + ",期間⇒," + str(a_dKikan))
                    a_sw.write("\n")

                    # 9)実質災害捕捉率【降雨数】
                    a_sw.write("災害捕捉率【降雨数】")
                    a_9_1 = 0
                    a_9_1_Msno = []
                    a_9_1_Time = []
                    a_sr = open(self.com.g_OutPath + "\\block\\" + self.com.g_OverOccurRainFallNum9_1TimeSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    while a_strTmp:
                        a_split = a_strTmp.split(",")
                        a_9_1_Msno.append(a_split[9])   # メッシュ番号
                        a_9_1_Time.append(a_split[10])   # 災害時刻
                        a_9_1 += 1
                        a_strTmp = a_sr.readline().rstrip("\r\n")
                    if a_9_1 > 0 and a_textSumOC > 0:
                        a_sw.write("," + str((float(a_9_1) / float(a_textSumOC - 1)) * 100))
                        a_sw.write(",RBFN越降雨数⇒," + str(a_9_1) + ",災害発生降雨数⇒," + str(a_textSumOC - 1))
                        a_sw.write(",災害時刻⇒")
                        for a_cntD in range(0, a_9_1):
                            a_sw.write("," + a_9_1_Msno[a_cntD] + "#" + a_9_1_Time[a_cntD])
                    else:
                        a_sw.write(",0")
                        a_sw.write(",RBFN越降雨数⇒," + str(a_9_1) + ",災害発生降雨数⇒," + str(a_textSumOC - 1))
                    a_sw.write("\n")

                    # ④実質災害捕捉率【件数】
                    a_sw.write("災害捕捉率【件数】")
                    a_9_2 = 0
                    a_9_2_Msno = []
                    a_9_2_Time = []
                    a_sr = open(self.com.g_OutPath + "\\block\\" + self.com.g_OverOccurRainFallNum9_2TimeSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    a_strTmp = a_sr.readline().rstrip("\r\n")
                    while a_strTmp:
                        a_split = a_strTmp.split(",")
                        # 9番目：メッシュ番号
                        # 10番目：災害時刻
                        a_splitL1 = a_split[9].split(";")
                        a_splitL2 = a_split[10].split(";")
                        a_9_2 += len(a_splitL1)
                        for a_cntD in range(0, len(a_splitL1)):
                            a_9_2_Msno.append(a_splitL1[a_cntD])    # メッシュ番号
                            a_9_2_Time.append(a_splitL2[a_cntD])    # 災害時刻
                        a_strTmp = a_sr.readline().rstrip("\r\n")
                    if a_9_2 > 0 and a_SaigaiSum > 0:
                        a_sw.write("," + str((float(a_9_2) / float(a_SaigaiSum)) * 100))
                        a_sw.write(",RBFN越件数⇒," + str(a_9_2) + ",災害発生件数⇒," + str(a_SaigaiSum))
                        a_sw.write(",災害時刻⇒")
                        for a_cntD in range(0, a_9_2):
                            a_sw.write("," + a_9_2_Msno[a_cntD] + "#" + a_9_2_Time[a_cntD])
                    else:
                        a_sw.write(",0")
                        a_sw.write(",RBFN越件数⇒," + str(a_9_2) + ",災害発生件数⇒," + str(a_SaigaiSum))
                    a_sw.write("\n")

                    # 空振り率
                    a_sw.write("空振り率")
                    if a_a > 0 and a_b > 0:
                        a_sw.write("," + str((float(a_b) / float(a_a)) * 100) + ",非発生降雨の超過降雨数⇒," + str(a_b) + ",超過降雨数⇒," + str(a_a))
                        a_sw.write(",超過時刻⇒")
                        for a_cntD in range(1, a_b):
                            a_split = a_textlineNCOR[a_cntD]
                            a_IsFirst = True
                            for a_cntD2 in range(9, 18):
                                if (len(a_split[a_cntD2].strip()) > 0):
                                    a_mETime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                    if (a_IsFirst == True):
                                        a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                        a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                                        a_IsFirst = False
                                    else:
                                        if (a_mETime < a_mSTime):
                                            a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                            a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                            a_sw.write("," + a_strTmp + "#" + str(a_mSTime.year) + "/" + str(a_mSTime.month) + "/" + str(a_mSTime.day) + " " + str(a_mSTime.hour) + ":" + str(a_mSTime.minute).rjust(2, "0") + "　非発生")

                        a_iOC = a_a - a_b
                        for a_cntD in range(1, a_iOC):
                            a_split = a_textlineOC[a_cntD]
                            a_IsFirst = True
                            for a_cntD2 in range(9, 18):
                                if (len(a_split[a_cntD2].strip()) > 0):
                                    a_mETime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                    if (a_IsFirst == True):
                                        a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                        a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                                        a_IsFirst = False
                                    else:
                                        if (a_mETime < a_mSTime):
                                            a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                            a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                            a_sw.write("," + a_strTmp + "#" + str(a_mSTime.year) + "/" + str(a_mSTime.month) + "/" + str(a_mSTime.day) + " " + str(a_mSTime.hour) + ":" + str(a_mSTime.minute).rjust(2, "0") + "　発生")
                    else:
                        a_sw.write(",0,非発生降雨の超過降雨数⇒," + str(a_b) + ",超過降雨数⇒," + str(a_a))
                    a_sw.write("\n")

                    # 警報発表頻度
                    a_sw.write("CL超過頻度")
                    if a_a > 0 and a_dKikan > 0:
                        a_sw.write("," + str((float(a_a) / float(a_dKikan)) * 100) + ",CL超過降雨数⇒," + str(a_a) + ",期間⇒," + str(a_dKikan))
                        a_sw.write(",超過時刻⇒")
                        for a_cntD in range(1, a_b):
                            a_split = a_textlineNCOR[a_cntD]
                            a_IsFirst = True
                            for a_cntD2 in range(9, 18):
                                if (len(a_split[a_cntD2].strip()) > 0):
                                    a_mETime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                    if (a_IsFirst == True):
                                        a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                        a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                                        a_IsFirst = False
                                    else:
                                        if (a_mETime < a_mSTime):
                                            a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                            a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                            a_sw.write("," + a_strTmp + "#" + str(a_mSTime.year) + "/" + str(a_mSTime.month) + "/" + str(a_mSTime.day) + " " + str(a_mSTime.hour) + ":" + str(a_mSTime.minute).rjust(2, "0") + "　非発生")

                        a_iOC = a_a - a_b
                        for a_cntD in range(1, a_iOC):
                            a_split = a_textlineOC[a_cntD]
                            a_IsFirst = True
                            for a_cntD2 in range(9, 18):
                                if (len(a_split[a_cntD2].strip()) > 0):
                                    a_mETime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                    if (a_IsFirst == True):
                                        a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                        a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                                        a_IsFirst = False
                                    else:
                                        if (a_mETime < a_mSTime):
                                            a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                            a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                            a_sw.write("," + a_strTmp + "#" + str(a_mSTime.year) + "/" + str(a_mSTime.month) + "/" + str(a_mSTime.day) + " " + str(a_mSTime.hour) + ":" + str(a_mSTime.minute).rjust(2, "0") + "　発生")
                    else:
                        a_sw.write(",0,CL超過降雨数⇒," + str(a_a) + ",期間⇒," + str(a_dKikan))
                    a_sw.write("\n")

                    # 空振り頻度
                    a_sw.write("空振り頻度")
                    if a_b > 0 and a_dKikan > 0:
                        a_sw.write("," + str((float(a_b) / float(a_dKikan)) * 100) + ",非発生降雨の超過降雨数⇒," + str(a_b) + ",期間⇒," + str(a_dKikan))
                        a_sw.write(",超過時刻⇒")
                        for a_cntD in range(1, a_b):
                            a_split = a_textlineNCOR[a_cntD]
                            a_IsFirst = True
                            for a_cntD2 in range(9, 18):
                                if (len(a_split[a_cntD2].strip()) > 0):
                                    a_mETime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                    if (a_IsFirst == True):
                                        a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                        a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                                        a_IsFirst = False
                                    else:
                                        if (a_mETime < a_mSTime):
                                            a_mSTime = datetime.datetime.strptime(a_split[a_cntD2], '%Y/%m/%d %H:%M')
                                            a_strTmp = str(float((9 - (a_cntD2 - 9)) / 10)) + "#" + a_split[a_cntD2 + 9]
                            a_sw.write("," + a_strTmp + "#" + str(a_mSTime.year) + "/" + str(a_mSTime.month) + "/" + str(a_mSTime.day) + " " + str(a_mSTime.hour) + ":" + str(a_mSTime.minute).rjust(2, "0") + "　非発生")
                    else:
                        a_sw.write(",0,非発生降雨の超過降雨数⇒," + str(a_b) + ",期間⇒," + str(a_dKikan))
                    a_sw.write("\n")

                    # 空振り時間
                    a_sw.write("空振り時間")
                    a_textlineW = []
                    a_w = self.com.Store_DataFile(self.com.g_OutPath + "\\block\\" + self.com.g_WhiffTimeSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv", a_textlineW)
                    if (a_w > 0) and (a_dKikan > 0):
                        a_dw = a_w
                        if (self.com.g_TimeKind == 1):
                            # 30分単位
                            a_dw = a_dw / 2
                        a_sw.write("," + str(float(a_dw) / a_dKikan) + ",空振り時間⇒," + str(a_dw) + ",期間⇒," + str(a_dKikan))
                    else:
                        a_sw.write(",0,空振り時間⇒,0,期間⇒," + str(a_dKikan))
                    a_sw.write("\n")

                    if os.path.isfile(self.com.g_OutPath + "\\" + self.com.g_CalcForecastPredictiveSymbol + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv") == True:
                        self._makeForecastPredictiveByBlock(a_sw, a_splitB)

                    a_sw.write("\n")

            a_sw.close()
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock2', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock2', a_strErr + "," + sys.exc_info())

    # ブロック毎集計処理3
    # ②土砂災害警戒情報のリードタイム
    def _makeStatisticsByBlock3_1(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeStatisticsByBlock3_1', a_strErr)

        try:
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_BlockStatisticsSymbol3_1 + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", "w", encoding="shift_jis")
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 空文字もしくは、0は無効→2006.04.07
                a_split = self.g_blockNoList[a_cnt1].split(",")
                a_len = len(a_split)
                a_strTmp = ""
                a_cnt3 = 0
                for a_cnt2 in range(0, a_len):
                    if (a_split[a_cnt2].strip() != "") and (a_split[a_cnt2].strip() != "0"):
                        if (a_cnt3 > 0):
                            a_strTmp += ","
                        a_strTmp += a_split[a_cnt2].strip()
                        a_cnt3 += 1

                if (a_strTmp != ""):
                    a_split = a_strTmp.split(",")
                    a_sw.write(self.g_blockNameList[a_cnt1] + "\n")    # メッシュ番号リスト出力の廃止
                    a_sw.write(",メッシュNo.（警戒）,年（警戒）,月（警戒）,日（警戒）,時（警戒）,メッシュNo.（災害）,年（災害）,月（災害）,日（災害）,時（災害）,リードタイム\n")
                    # ③土砂災害警戒情報の発表頻度
                    a_sw.write("警戒情報のリードタイム")

                    a_sr = open(self.com.g_OutPath + "\\block\\" + self.com.g_CalcCautionAnnounceReadTimeSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv")
                    a_textline11 = a_sr.readline().rstrip("\r\n")
                    a_textSum11 = 0
                    a_textline11 = a_sr.readline().rstrip("\r\n")
                    while a_textline11:
                        a_split11 = a_textline11.split(",")
                        for a_cnt2 in range(9, 20):
                            a_sw.write("," + a_split11[a_cnt2])
                        a_sw.write("\n")
                        a_textSum11 += 1
                        a_textline11 = a_sr.readline().rstrip("\r\n")

                    a_sr.close()
                    if (a_textSum11 == 0):
                        a_sw.write("\n")
                a_sw.write("\n")
            a_sw.close()
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_1', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_1', a_strErr + "," + sys.exc_info())

    # ブロック毎集計処理3
    # ⑥RBFN越のリードタイム
    def _makeStatisticsByBlock3_2(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeStatisticsByBlock3_2', a_strErr)

        try:
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_BlockStatisticsSymbol3_2 + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv", "w", encoding="shift_jis")
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                # 空文字もしくは、0は無効→2006.04.07
                a_split = self.g_blockNoList[a_cnt1].split(",")
                a_len = len(a_split)
                a_strTmp = ""
                a_cnt3 = 0
                for a_cnt2 in range(0, a_len):
                    if (a_split[a_cnt2].strip() != "") and (a_split[a_cnt2].strip() != "0"):
                        if (a_cnt3 > 0):
                            a_strTmp += ","
                        a_strTmp += a_split[a_cnt2].strip()
                        a_cnt3 += 1

                if (a_strTmp != ""):
                    a_split = a_strTmp.split(",")
                    a_sw.write(self.g_blockNameList[a_cnt1] + "\n")    # メッシュ番号リスト出力の廃止
                    a_sw.write(",メッシュNo.（RBFN）,年（RBFN）,月（RBFN）,日（RBFN）,時（RBFN）,メッシュNo.（災害）,年（災害）,月（災害）,日（災害）,時（災害）,リードタイム,RBFN値\n")
                    # ⑥RBFN越のリードタイム
                    a_sw.write("RBFN越のリードタイム")

                    a_sr = open(self.com.g_OutPath + "\\block\\" + self.com.g_CalcRBFNReadTimeSymbolByBlock + "-" + self.g_blockNameList[a_cnt1] + ".csv")
                    a_textline11 = a_sr.readline().rstrip("\r\n")
                    a_textSum11 = 0
                    a_textline11 = a_sr.readline().rstrip("\r\n")
                    while a_textline11:
                        a_split11 = a_textline11.split(",")
                        for a_cnt2 in range(9, 21):
                            a_sw.write("," + a_split11[a_cnt2])
                        a_sw.write("\n")
                        a_textSum11 += 1
                        a_textline11 = a_sr.readline().rstrip("\r\n")

                    a_sr.close()
                    if (a_textSum11 == 0):
                        a_sw.write("\n")
                a_sw.write("\n")
            a_sw.close()
        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_2', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_2', a_strErr + "," + sys.exc_info())

    # 空振り時間
    def _makeWiffTimeByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeWiffTimeByBlock', a_strErr)

        try:
            a_blockSum = len(self.g_blockNameList)
            for a_cnt1 in range(0, a_blockSum):
                a_sw = open(self.com.g_OutPath + "\\block\\" + self.com.g_WhiffTimeSymbolByBlock + "-" + self.blockNameList[a_cnt1] + ".csv", "w", encoding="shift_jis")
                a_sw.write("年,月,日,時,meshNO\n")

                a_index = []
                a_wTime = []
                a_wMeshNo = []

                a_rSum = 0
                a_meshList = self.g_blockNoList[a_cnt1].split(",")
                for a_cnt3 in range(0, len(a_meshList)):
                    if os.path.isfile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_WhiffTimeSymbolByBlock + ".csv") == True:
                        a_textlineD2 = []
                        a_textSumD2 = self.com.Store_DataFile(self.com.g_OutPath + "\\" + a_meshList[a_cnt3] + "\\" + self.com.g_WhiffTimeSymbolByBlock + ".csv", a_textlineD2)
                        for a_cnt2 in range(1, a_textSumD2):
                            a_split1 = a_textlineD2[a_cnt2]
                            a_IsOK = False

                            if (a_rSum <= 0):
                                # 最初のレコード読込
                                a_IsOK = True
                            else:
                                # ２回目以降のレコード読込
                                a_tmpTime = datetime.datetime.strptime(a_split1[1], '%Y/%m/%d %H:%M')
                                for a_cnt4 in range(0, a_rSum):
                                    if (a_tmpTime == a_wTime[a_cnt4]):
                                        a_IsOK = False
                                        break
                                    else:
                                        a_IsOK = True

                            if (a_IsOK == True):
                                a_index.append(a_split1[0])
                                a_wTime.append(datetime.datetime.strptime(a_split1[1], '%Y/%m/%d %H:%M'))
                                a_wMeshNo.append(a_meshList[a_cnt3])
                                a_rSum += 1

                            break

                for a_cnt3 in range(0, a_rSum):
                    a_sw.write("," + str(a_wTime[a_cnt3].year) + "/" + str(a_wTime[a_cnt3].month) + "/" + str(a_wTime[a_cnt3].day) + " " + str(a_wTime[a_cnt3].hour) + ":" + str(a_wTime[a_cnt3].minute).rjust(2, "0"))
                    a_sw.write("," + a_wMeshNo[a_cnt3])

                    a_sw.write("\n")

                a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeWiffTimeByBlock', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeWiffTimeByBlock', a_strErr + "," + sys.exc_info())

