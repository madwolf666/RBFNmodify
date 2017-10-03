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
    prv_xlWkb = None
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

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'MakeBlockAll-run', a_strErr)

        try:
            a_retsu, a_gyo = self._EOpenEx()
            print(a_retsu, a_gyo)

            # 集計結果ファイルを読み込み、ブロック毎に集計し直す。
            # 一連の発生降雨
            self._makeRainfallByBlock()
            # 災害発生降雨
            self._makeOccurRainfallByBlock()
            # 非発生降雨
            self._makeNonOccurRainfallByBlock()
            # 一連の発生降雨
            self._makeRainfall2ByBlock()
            # 災害発生降雨
            self._makeOccurRainfall2ByBlock()
            # 空振り時間
            self._makeWiffTimeByBlock()
            # 発生降雨超過数【災害捕捉率】
            self._makeOccurRainfall9_1ByBlock()
            # 災害発生件数【災害捕捉率】
            self._makeOccurRainfall9_2ByBlock()
            # 警戒情報リードタイム
            self._makeReadTimeByBlock()
            # RBFN越リードタイム
            self._makeReadTimeByBlock()

            self._makeStatisticsByBlock()

            # ①土砂災害警戒情報の災害捕捉率、③土砂災害警戒情報の発表頻度
            self._makeStatisticsByBlock2()
            # ②土砂災害警戒情報のリードタイム
            self._makeStatisticsByBlock3_1()
            # ⑥RBFN越のリードタイム
            self._makeStatisticsByBlock3_2()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeBlockAll-run', a_strErr + str(exp.args[0]))
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeBlockAll-run', a_strErr + sys.exc_info())

    def _EOpenEx(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, '_EOpenEx-run', a_strErr)

        a_restu = 0
        a_gyo = 0

        try:
            del self.g_blockNameList[:]
            del self.g_blockNoList[:]

            self.prv_xlWkb = xlrd.open_workbook(self.com.g_BlockExcelDefine)

            a_wks1 = self.prv_xlWkb.sheet_by_name("ブロック図")

            # 列数を取得
            a_restu = a_wks1.ncols -1
            '''
            a_row = a_wks1.row_values(1, 1)
            for a_cell in a_row:
                a_restu += 1
                '''

            # 行数を取得
            a_gyo = a_wks1.nrows - 1

            a_wks1 = self.prv_xlWkb.sheet_by_name("ブロック区分")
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
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_EOpenEx', a_strErr + str(exp.args[0]))
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_EOpenEx', a_strErr + sys.exc_info())

        return a_restu, a_gyo

    # ブロック毎集計処理
    def _makeStatisticsByBlock(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, '_makeStatisticsByBlock', a_strErr)

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
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock', a_strErr + str(exp.args[0]))
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock', a_strErr + sys.exc_info())

    # ブロック毎集計処理3
    # ②土砂災害警戒情報のリードタイム
    def _makeStatisticsByBlock3_1(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, '_makeStatisticsByBlock3_1', a_strErr)

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
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_1', a_strErr + str(exp.args[0]))
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_1', a_strErr + sys.exc_info())

    # ブロック毎集計処理3
    # ⑥RBFN越のリードタイム
    def _makeStatisticsByBlock3_2(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, '_makeStatisticsByBlock3_2', a_strErr)

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
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_2', a_strErr + str(exp.args[0]))
            #self.com.Outputlog(self.com.g_LOGMODE_INFORMATION, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeStatisticsByBlock3_2', a_strErr + sys.exc_info())

