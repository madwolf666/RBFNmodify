################################################################################
# 等高線の作成
################################################################################
import sys
import os
import datetime
import math
import csv
from PIL import Image, ImageDraw, ImageFont
import shutil
import com_functions
import threading

# 降雨超過数を作成する
class MakeContourByMesh():
    prv_leftMargin = 53.333333333333336
    prv_topMargin = 26.666666666666668
    prv_rightMargin = 148.0
    prv_bottomMargin = 53.333333333333336

    def __init__(self,
                 h_proc_num,
                 h_ini_path,
                 h_DisasterFile,
                 h_CautionAnnounceFile,
                 h_TargetMeshFile,
                 h_meshNo,
                 h_kind,
                 h_unReal,
                 h_soilMin,
                 h_rainMax
                 ):
        '''
        def __init__(self,
                     h_proc_num,
                     h_ini_path,
                     h_meshNo,
                     h_kind,
                     h_unReal,
                     h_soilMin,
                     h_rainMax
                     ):
            '''
        #threading.Thread.__init__(self)
        #super(Thread_MakeOverRainfallByMesh, self).__init__()

        self.com = com_functions.ComFunctions()

        self.com.proc_num = h_proc_num
        self.com.ini_path = h_ini_path

        self.com.g_textline_DisasterFile = h_DisasterFile
        self.com.g_textline_CautionAnnounceFile = h_CautionAnnounceFile
        self.com.g_textline_TargetMeshFile = h_TargetMeshFile
        self.com.g_textSum_DisasterFile = len(self.com.g_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile = len(self.com.g_textline_CautionAnnounceFile)
        self.com.g_textSum_TargetMeshFile = len(self.com.g_textline_TargetMeshFile)

        self.meshNo = h_meshNo
        self.kind = h_kind
        self.unReal = h_unReal
        self.soilMin = h_soilMin
        self.rainMax = h_rainMax

        #引数を取得
        self.com.GetEnvData(h_ini_path)

        '''
        self.com.g_textSum_DisasterFile = self.com.Store_DataFile(self.com.g_DisasterFileName, self.com.g_textline_DisasterFile)
        self.com.g_textSum_CautionAnnounceFile = self.com.Store_DataFile(self.com.g_CautionAnnounceFileName, self.com.g_textline_CautionAnnounceFile)
        self.com.g_textSum_TargetMeshFile = self.com.Store_DataFile(self.com.g_TargetMeshFile, self.com.g_textline_TargetMeshFile)
        '''

        self.run()  # multiprocess

    def run(self):
        a_strErr = "ini_path=" + self.com.ini_path + ",meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', a_strErr)

        try:
            # 既往CLの取り込み
            if (self.com.g_PastKind == 0):
                # 取り込みなし
                self.TargetPath = self.com.g_RBFNOutPath
                self.TargetMeshNo = self.meshNo
                self.TargetFile = "surface-" + self.TargetMeshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                self.StartYear = self.com.g_TargetStartYear
                self.EndYear = self.com.g_TargetEndYear
            else:
                # 取り込みあり
                self.TargetPath = self.com.g_PastRBFNOutPath
                # 既往CL対象メッシュ選択サポート
                self.TargetMeshNo = self.meshNo
                #self.TargetMeshNo = self.com.GetTargetMeshNoByCL(self.com.g_TargetStartYear, self.meshNo)
                self.TargetFile = "surface-" + self.com.GetTargetMeshNoByCL(self.com.g_TargetStartYear, self.meshNo) + "-" + str(self.com.g_PastTargetStartYear) + "-" + str(self.com.g_PastTargetEndYear) + ".csv"
                #self.StartYear = self.com.g_PastTargetStartYear
                #self.EndYear = self.com.g_PastTargetEndYear
                self.StartYear = self.com.g_TargetStartYear
                self.EndYear = self.com.g_TargetEndYear

            # メッシュ番号の取得
            a_RBFNFile = self.TargetPath + "\\" + self.TargetFile
            # 全てのデータを読み込む
            self.com.g_textSum_RBFNFile = self.com.Store_DataFile(a_RBFNFile, self.com.g_textline_RBFNFile)

            # オリジナル等高線の作成
            self._makeAutoContourOrigin(self.meshNo)
            # 等高線の補正
            self._makeAutoContourRevise(self.meshNo)
            # スネーク曲線の作成
            self._makeAutoContourSnake(self.meshNo)

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeContourByMesh-run', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, 'MakeContourByMesh-run', a_strErr + "," + sys.exc_info())

    def _calcNearRBFN(
            self,
            h_soil,
            h_rain,
            h_x1,
            h_y1,
            h_z1,
            h_x2,
            h_y2,
            h_z2,
            h_x3,
            h_y3,
            h_z3,
            h_x4,
            h_y4,
            h_z4
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_calcNearRBFN', a_strErr)

        a_xn = 0
        a_yn = 0
        a_zn = 0

        try:
            # AB間の内分座標
            a_tmp1 = h_soil - h_x1
            a_tmp2 = h_x2 - h_x1
            a_m = a_tmp1 / a_tmp2
            a_n = 1 - a_m

            a_xAB = (a_n * h_x1 + a_m * h_x2) / (a_m + a_n)
            a_yAB = (a_n * h_y1 + a_m * h_y2) / (a_m + a_n)
            a_zAB = (a_n * h_z1 + a_m * h_z2) / (a_m + a_n)

            # DC間の内分座標
            a_xDC = (a_n * h_x4 + a_m * h_x3) / (a_m + a_n)
            a_yDC = (a_n * h_y4 + a_m * h_y3) / (a_m + a_n)
            a_zDC = (a_n * h_z4 + a_m * h_z3) / (a_m + a_n)

            # AD間の内分座標
            a_tmp1 = h_rain - h_y1
            a_tmp2 = h_y4 - h_y1
            a_m = a_tmp1 / a_tmp2
            a_n = 1 - a_m

            a_xAD = (a_n * h_x1 + a_m * h_x4) / (a_m + a_n)
            a_yAD = (a_n * h_y1 + a_m * h_y4) / (a_m + a_n)
            a_zAD = (a_n * h_z1 + a_m * h_z4) / (a_m + a_n)

            # BC間の内分座標
            a_xBC = (a_n * h_x2 + a_m * h_x3) / (a_m + a_n)
            a_yBC = (a_n * h_y2 + a_m * h_y3) / (a_m + a_n)
            a_zBC = (a_n * h_z2 + a_m * h_z3) / (a_m + a_n)

            # AB-DCの線とAD-BCの線の交点を求める。
            a_xa = a_xAB - a_xDC
            a_xb = a_xAD - a_xBC
            a_xc = a_xAD - a_xAB

            a_ya = a_yAB - a_yDC
            a_yb = a_yAD - a_yBC
            a_yc = a_yAD - a_yAB

            # 媒介変数
            a_s = ((a_xAB - a_xDC) * (a_yAD - a_yAB) - (a_yAB - a_yDC) * (a_xAD - a_xAB)) / ((a_yAB - a_yDC) * (a_xAD - a_xBC) - (a_yAD - a_yBC) * (a_xAB - a_xDC))
            a_t = ((a_xa * a_yc) - (a_xc * a_ya)) / ((a_xb * a_ya) - (a_xa * a_yb))

            # 交点
            a_hantei1 = a_zAB + a_t * (a_zAB - a_zDC)
            a_hantei2 = a_zAD + a_s * (a_zAD - a_xBC)

            # 四捨五入
            a_xn = self.com.My_round(a_xAB + a_t * (a_xAB - a_xDC), 8)
            a_yn = self.com.My_round(a_yAB + a_t * (a_yAB - a_yDC), 8)
            a_zn = self.com.My_round(a_zAB + a_t * (a_zAB - a_zDC), 8)
            '''
            a_xn = "%.8f" % (a_xAB + a_t * (a_xAB - a_xDC))
            a_yn = "%.8f" % (a_yAB + a_t * (a_yAB - a_yDC))
            a_zn = "%.8f" % (a_zAB + a_t * (a_zAB - a_zDC))
            '''

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_calcNearRBFN', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_calcNearRBFN', a_strErr + "," + sys.exc_info())

        return a_xn, a_yn, a_zn

    # 等高線補正処理
    def _contourRevise(self):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_contourRevise', a_strErr)

        try:
            a_textline = []
            a_textSum = self.com.Store_DataFile(self.com.g_OutPath + "\\" + self.com.g_ContourOriginSymbol + "-" + str(self.TargetMeshNo) + "-" + str(self.StartYear) + "-" + str(self.EndYear) + ".csv", a_textline)

            # Y軸の最大値の補正（2006.03.14）
            a_findIdx1 = 0
            a_findIdx2 = 0

            a_dst = 0
            a_dst1 = 0
            a_dst2 = 0
            a_dst3 = 0
            a_dsep = 0
            a_IsRevise = False

            for a_cnt1 in range(1, 10):
                a_yMax = 0
                a_findIdx1 = 0
                for a_cnt2 in range(0, a_textSum):
                    a_split1 = a_textline[a_cnt2]
                    # Y軸の最大値チェック
                    if (a_yMax < float(a_split1[a_cnt1])):
                        a_yMax = float(a_split1[a_cnt1])
                        a_findIdx1 = a_cnt2
                    else:
                        a_dmy = 0

                for a_cnt3 in range(0, a_findIdx1 + 1):
                    a_split1 = a_textline[a_cnt3]
                    a_split2 = str(a_yMax).split(".")
                    a_yMax = int(a_split2[0])
                    a_split1[a_cnt1] = str(a_yMax)
                    # 値の再配置
                    a_textline[a_cnt3] = [a_split1[0], a_split1[1], a_split1[2], a_split1[3], a_split1[4], a_split1[5], a_split1[6], a_split1[7], a_split1[8], a_split1[9]]
                    #a_textline[a_cnt3] = a_split1[0] + "," + a_split1[1] + "," + a_split1[2] + "," + a_split1[3] + "," + a_split1[4] + "," + a_split1[5] + "," + a_split1[6] + "," + a_split1[7] + "," + a_split1[8] + "," + a_split1[9]

                # 切り捨てた最大値を元に、小数点で最大値を超えるものをチェックする。(2006.03.14)
                a_findIdx2 = 0
                for a_cnt2 in range(a_findIdx1 + 1, a_textSum):
                    a_split1 = a_textline[a_cnt2]
                    # Y軸の最大値チェック
                    if (a_yMax < float(a_split1[a_cnt1])):
                        a_findIdx2 = a_cnt2
                    else:
                        a_dmy = 0

                for a_cnt3 in range(a_findIdx1 + 1, a_findIdx2 + 1):
                    a_split1 = a_textline[a_cnt3]
                    # 切捨てて格納→本当に切り捨ててよいのか？（2006.03.14）
                    a_split1[a_cnt1] = str(a_yMax)
                    # 値の再配置
                    a_textline[a_cnt3] = [a_split1[0], a_split1[1], a_split1[2], a_split1[3], a_split1[4], a_split1[5], a_split1[6], a_split1[7], a_split1[8], a_split1[9]]
                    #a_textline[a_cnt3] = a_split1[0] + "," + a_split1[1] + "," + a_split1[2] + "," + a_split1[3] + "," + a_split1[4] + "," + a_split1[5] + "," + a_split1[6] + "," + a_split1[7] + "," + a_split1[8] + "," + a_split1[9]

                ################################################################
                for a_cnt2 in range(a_textSum - 2, 0, -1):
                    # 前の値を取得
                    a_split1 = a_textline[a_cnt2 + 1]
                    a_dst1 = float(a_split1[a_cnt1])
                    # 現在の値を取得
                    a_split2 = a_textline[a_cnt2]
                    a_dst2 = float(a_split2[a_cnt1])
                    # 次の値を取得
                    a_split3 = a_textline[a_cnt2 - 1]
                    a_dst3 = float(a_split3[a_cnt1])

                    if ((a_dst1 > 0) and (a_dst2 > 0) and (a_dst3 > 0)):

                        if (a_dst1 >= a_dst3):
                            # 次の値の方が小さい
                            a_dst = a_dst1 - ((a_dst1 - a_dst3) / 2)

                            # Y座標を補正する。
                            a_split2[a_cnt1] = str(a_dst1)
                            # 値の再配置
                            a_textline[a_cnt2] = [a_split2[0], a_split2[1], a_split2[2], a_split2[3], a_split2[4], a_split2[5], a_split2[6], a_split2[7], a_split2[8], a_split2[9]]
                            #a_textline[a_cnt2] = a_split2[0] + "," + a_split2[1] + "," + a_split2[2] + "," + a_split2[3] + "," + a_split2[4] + "," + a_split2[5] + "," + a_split2[6] + "," + a_split2[7] + "," + a_split2[8] + "," + a_split2[9]

                            # Y座標を補正する。
                            a_split3[a_cnt1] = str(a_dst1)
                            # 値の再配置
                            a_textline[a_cnt2] = [a_split3[0], a_split3[1], a_split3[2], a_split3[3], a_split3[4], a_split3[5], a_split3[6], a_split3[7], a_split3[8], a_split3[9]]
                            #a_textline[a_cnt2] = a_split3[0] + "," + a_split3[1] + "," + a_split3[2] + "," + a_split3[3] + "," + a_split3[4] + "," + a_split3[5] + "," + a_split3[6] + "," + a_split3[7] + "," + a_split3[8] + "," + a_split3[9]

                            a_IsRevise = True
                        else:
                            a_dst = a_dst3 - ((a_dst3 - a_dst1) / 2)
                            if (float(a_split2[a_cnt1]) <= a_dst):
                                # Y座標を補正する。
                                a_split2[a_cnt1] = str(a_dst)
                                # 値の再配置
                                a_textline[a_cnt2] = [a_split2[0], a_split2[1], a_split2[2], a_split2[3], a_split2[4], a_split2[5], a_split2[6], a_split2[7], a_split2[8], a_split2[9]]
                                #a_textline[a_cnt2] = a_split2[0] + "," + a_split2[1] + "," + a_split2[2] + "," + a_split2[3] + "," + a_split2[4] + "," + a_split2[5] + "," + a_split2[6] + "," + a_split2[7] + "," + a_split2[8] + "," + a_split2[9]

                                a_IsRevise = True

            # 補正データの書き込み
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + str(self.TargetMeshNo) + "-" + str(self.StartYear) + "-" + str(self.EndYear) + ".csv", "w", encoding="shift_jis")
            for a_cnt1 in range(0, a_textSum):
                self.com.Write_TextLine(a_sw, a_textline[a_cnt1])
                a_sw.write("\n")
                #a_sw.write(a_textline[a_cnt1] + "\n")
            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_contourRevise', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_contourRevise', a_strErr + "," + sys.exc_info())

    # 等高線補正処理(土壌雨量指数下限値)
    def _contourSoilMin(
            self,
            soilMin,
            rainMax
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_contourSoilMin', a_strErr)

        try:
            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_ContourReviseSoilMinSymbol + "-" + str(self.TargetMeshNo) + "-" + str(self.StartYear) + "-" + str(self.EndYear) + ".csv", "w", encoding="shift_jis")

            a_prev_textline = ""
            a_IsPrint = False

            a_sr = open(self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + str(self.TargetMeshNo) + "-" + str(self.StartYear) + "-" + str(self.EndYear) + ".csv", "r", encoding="shift_jis")
            a_textline = a_sr.readline().strip("\r\n")
            while a_textline:
                a_split1 = a_textline.split(",")
                if (float(a_split1[0]) < soilMin):
                    # 下限値よりも小さい
                    a_dmy = 0
                elif (float(a_split1[0]) == soilMin):
                    # 下限値と等しい
                    a_sw.write(a_textline + "\n")
                    a_IsPrint = True
                else:
                    if (a_IsPrint == False):
                        if (a_prev_textline != ""):
                            a_split2 = a_prev_textline.split(",")
                            a_sw.write(str(soilMin) + "," + a_split2[1] + "," + a_split2[2] + "," + a_split2[3] + "," + a_split2[4] + "," + a_split2[5] + "," + a_split2[6] + "," + a_split2[7] + "," + a_split2[8] + "," + a_split2[9] + "\n")
                    a_sw.write(a_textline + "\n")
                    a_IsPrint = True

                a_prev_textline = a_textline
                a_textline = a_sr.readline().strip("\r\n")

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_contourSoilMin', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_contourSoilMin', a_strErr + "," + sys.exc_info())

    # 等高線イメージを描画
    def _drawContour(
            self,
            outkind,
            outAction,
            h_img,
            TargetCL,
            soilMin,
            rainMax,
            unReal,
            h_msno
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_drawContour', a_strErr)

        try:
            a_textline = []
            a_textSum = 0
            a_textline2 = ""
            a_textSum2 = ""
            a_split1 = []
            a_split2 = []
            a_cnt1 = 0
            a_cnt2 = 0
            a_RBFNFile = ""
            a_xMax = 0
            a_yMax = 0
            a_xLine = 0
            a_yLine = 0
            a_xSep = 0
            a_ySep = 0
            a_strTmp = ""
            a_bFlag = False
            a_drawInfo = []
            a_TargetCL = -1
            a_isDrawNonOccurRainfall = True
            a_isDrawTargetCLOnly = False
            a_TanbuX1 = -1
            a_TanbuY1 = -1
            a_TanbuX2 = -1
            a_TanbuY2 = -1
            a_splitC = []

            # 既往取込あり
            self._getGraphDrawInfo(h_msno, a_drawInfo)
            if (len(a_drawInfo) > 0):
                # 対象CL
                a_TargetCL = int(float(a_drawInfo[1]) * 10)
                # 非発生降雨描画の有無
                if (a_drawInfo[4] == "1"):
                    a_isDrawNonOccurRainfall = True
                else:
                    a_isDrawNonOccurRainfall = False

                # CLのみ描画の有無
                if (a_drawInfo[5] == "1"):
                    a_isDrawTargetCLOnly = True
                else:
                    a_isDrawTargetCLOnly = False

                if (soilMin <= 0):
                    soilMin = float(a_drawInfo[2])
                    rainMax = float(a_drawInfo[3])

            if (TargetCL > 0):
                a_TargetCL = int(TargetCL * 10)

            # 全てのデータを読み込む
            a_ySum = self.com.g_textSum_RBFNFile
            a_xSum = len(self.com.g_textline_RBFNFile[0]) #- 1

            # X軸の最大値を取得
            a_xMax = float(self.com.g_textline_RBFNFile[0][a_xSum - 1])
            # Y軸の最大値を取得
            a_yMax = float(self.com.g_textline_RBFNFile[a_ySum - 1][0])

            a_textline = []
            a_textSum = self.com.Store_DataFile(self.com.g_OutPath + "\\" + outkind + "-" + str(self.TargetMeshNo) + "-" + str(self.StartYear) + "-" + str(self.EndYear) + ".csv", a_textline)

            if (self.com.g_DrawRainfallMax > 0):
                a_yMax = self.com.g_DrawRainfallMax
            if (self.com.g_DrawSoilMax > 0):
                a_xMax = self.com.g_DrawSoilMax

            # X軸、Y軸のMAX値を補正する。
            a_xLine = int(a_xMax / self.com.g_xUnit)
            if ((a_xMax % self.com.g_xUnit) > 0):    #余り
                a_xMax = a_xLine * self.com.g_xUnit + self.com.g_xUnit
                a_xLine = a_xLine + 1
            else:
                a_xMax = a_xLine * self.com.g_xUnit
            a_yLine = int(a_yMax / self.com.g_yUnit)
            if ((a_yMax % self.com.g_yUnit) > 0):   #余り
                a_yMax = a_yLine * self.com.g_yUnit + self.com.g_yUnit
                a_yLine = a_yLine + 1
            else:
                a_yMax = a_yLine * self.com.g_yUnit

            # X軸、Y軸のセパレートを設定する。
            a_xSep = (h_img.width - (self.prv_leftMargin + self.prv_rightMargin)) / a_xMax
            a_ySep = (h_img.height - (self.prv_topMargin + self.prv_bottomMargin)) / a_yMax

            # PictureBox内容を初期化する。
            #picbox.Image = Nothing
            #h_img.width = int(self.com.g_ImageFileWidth)
            #h_img.height = int(self.com.g_ImageFileHeight)
            a_draw = ImageDraw.Draw(h_img)
            #a_draw.bitmap((0, 0), )
            #picbox.Image = New Bitmap(picbox.ClientSize.Width, picbox.ClientSize.Height)    '[2012.06.14]
            #a_g As Graphics = Graphics.FromImage(picbox.Image)
            a_pen_color = (0, 0, 0)   #黒
            a_pen_width = 1
            a_fnt_color = (0, 0, 0)   # 黒
            # MS UI Gothic
            a_fnt_font = ImageFont.truetype(
                "C:\\Windows\\Fonts\\msgothic.ttc", 9
            )

            a_CX = 0

            # 背景色を白に設定⇒呼び出し元で既に設定

            # メッシュ番号（5km/1km）の描画
            a_msno5km = ""
            a_msno1km = ""
            if (self.com.g_TargetRainMesh == 5):
                a_msno5km = h_msno
                a_msno1km = "-"
            else:
                a_msno1km = h_msno
                a_msno5km = self.com.GetParnetMeshNo(self.StartYear, a_msno1km)
            a_draw.text(
                ((h_img.width / 2 - 40), 2),
                a_msno5km,
                font=a_fnt_font,
                fill=a_fnt_color
            )
            a_draw.text(
                ((h_img.width / 2 - 40), 12),
                a_msno1km,
                font=a_fnt_font,
                fill=a_fnt_color
            )

            # 横
            for a_cnt1 in range(0, a_yLine + 1):
                a_bFlag = True
                if (a_cnt1 >= 1) and (a_cnt1 < a_yLine):
                    #a_pen.DashStyle = Drawing2D.DashStyle.Dot
                    a_pen_color = (192, 192, 192)
                else:
                    #a_pen.DashStyle = Drawing2D.DashStyle.Solid
                    a_pen_color = (0, 0, 0)

                if (a_bFlag == True):
                    a_draw.line(
                        [
                            (int(self.prv_leftMargin), int(self.prv_topMargin + (a_ySep * (self.com.g_yUnit * a_cnt1)))),
                            (int(h_img.width - self.prv_rightMargin), int(self.prv_topMargin + (a_ySep * (self.com.g_yUnit * a_cnt1))))
                             ],
                        a_pen_color,
                        a_pen_width
                    )

                a_strTmp = str(int(a_cnt1 * self.com.g_yUnit))
                if len(a_strTmp) == 1:
                    a_CX = int(self.prv_leftMargin - 12.0)
                elif len(a_strTmp) == 2:
                    a_CX = int(self.prv_leftMargin - 16.0)
                elif len(a_strTmp) == 3:
                    a_CX = int(self.prv_leftMargin - 18.666666666666668)

                a_draw.text(
                    (a_CX, int(h_img.height - self.prv_bottomMargin - (a_ySep * (self.com.g_yUnit * a_cnt1)) - 5.333333333333333)),
                    a_strTmp,
                    font=a_fnt_font,
                    fill=a_fnt_color
                )

            # 縦
            for a_cnt1 in range(0, a_xLine + 1):
                a_bFlag = True
                if (a_cnt1 >= 1) and (a_cnt1 < a_xLine):
                    #a_pen.DashStyle = Drawing2D.DashStyle.Dot
                    a_pen_color = (192, 192, 192)
                else:
                    #a_pen.DashStyle = Drawing2D.DashStyle.Solid
                    a_pen_color = (0, 0, 0)

                if (a_bFlag == True):
                    a_draw.line(
                        [
                            (int(self.prv_leftMargin + (a_xSep * (self.com.g_xUnit * a_cnt1))), int(self.prv_topMargin + (a_ySep * (self.com.g_yUnit * a_yLine)))),
                            (int(self.prv_leftMargin + (a_xSep * (self.com.g_xUnit * a_cnt1))), int(self.prv_topMargin))
                        ],
                        a_pen_color,
                        a_pen_width
                    )

                a_strTmp = str(int(a_cnt1 * self.com.g_xUnit))
                if len(a_strTmp) == 1:
                    a_CX = int(self.prv_leftMargin + (a_xSep * (self.com.g_xUnit * a_cnt1)) - 1.3333333333333333)
                elif len(a_strTmp) == 2:
                    a_CX = int(self.prv_leftMargin + (a_xSep * (self.com.g_xUnit * a_cnt1)) - 5.333333333333333)
                elif len(a_strTmp) == 3:
                    a_CX = int(self.prv_leftMargin + (a_xSep * (self.com.g_xUnit * a_cnt1)) - 8.0)

                a_draw.text(
                    (a_CX, int(h_img.height - self.prv_bottomMargin  + 2.6666666666666665)),
                    a_strTmp,
                    font=a_fnt_font,
                    fill=a_fnt_color
                )

            # 文字の設定
            a_imgSoil = Image.open(".\\images\\imgTitleSoil.gif")
            a_imgRain = Image.open(".\\images\\imgTitleRain.gif")
            h_img.paste(
                a_imgSoil,
                (
                    int(h_img.width / 2 - 46.666666666666664), int(h_img.height - (self.prv_bottomMargin / 2) - 5.333333333333333)
                )
            )
            h_img.paste(
                a_imgRain,
                (
                    int(6.666666666666667), int((h_img.height - self.prv_bottomMargin) / 2 - 100.0)
                )
            )

            # 等高線の描画
            a_setSoilMin  = False
            a_IsSet = False
            a_splitTmp = []

            for a_cnt1 in range(1, 10):
                if (a_isDrawTargetCLOnly == True):
                    if (a_cnt1 != a_TargetCL):
                        continue
                        #GoTo DRAWCONTOUR_CONTIBUE

                a_pen_width = 1

                # 色の設定
                if (len(a_drawInfo) > 0):
                    a_splitC = a_drawInfo[9 + ((9 - a_cnt1) * 3)].split("#")
                    a_pen_color = (int(a_splitC[0]), int(a_splitC[1]), int(a_splitC[2]))
                    #a_pen.DashStyle = CType(a_drawInfo(10 + +((9 - a_cnt1) * 3)), System.Drawing.Drawing2D.DashStyle)
                    a_pen_width = float(a_drawInfo[11 + +((9 - a_cnt1) * 3)])
                else:
                    if (a_cnt1 == 1):   # 0.1
                        a_pen_color = (0, 255, 0)
                    elif (a_cnt1 == 2):   # 0.2
                        a_pen_color = (0, 0, 255)
                    elif (a_cnt1 == 3):   # 0.3
                        a_pen_color = (0, 128, 0)
                    elif (a_cnt1 == 4):   # 0.4
                        a_pen_color = (128, 0, 0)
                    elif (a_cnt1 == 5):   # 0.5
                        a_pen_color = (128, 0, 128)
                    elif (a_cnt1 == 6):   # 0.6
                        a_pen_color = (0, 128, 192)
                    elif (a_cnt1 == 7):   # 0.7
                        a_pen_color = (255, 255, 0)
                    elif (a_cnt1 == 8):   # 0.8
                        a_pen_color = (255, 0, 255)
                    elif (a_cnt1 == 9):   # 0.9
                        a_pen_color = (0, 0, 128)

                # 一番最後はやらない？→2006.03.14
                a_IsSet = False

                a_split1 = None
                a_split2 = None

                for a_cnt2 in range(0, a_textSum - 1):
                    # 土壌雨量指数の下限値設定
                    a_setSoilMin = False

                    a_split1 = a_textline[a_cnt2]
                    a_split2 = a_textline[a_cnt2 + 1]

                    if (outAction == self.com.g_Action_MakeContourSoilMin):
                        # 土壌雨量指数の下限値判断
                        if (float(a_split1[0]) < soilMin):
                            a_setSoilMin = True
                        else:
                            if (a_IsSet == False):
                                if (float(a_split1[0]) == soilMin):
                                    if (a_cnt1 == a_TargetCL):
                                        a_TanbuX1 = int(self.prv_leftMargin + float(a_split1[0]) * a_xSep)
                                        a_TanbuY1 = int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))) + 10)
                                    if (a_cnt1 == 9):
                                        a_TanbuX2 = int(self.prv_leftMargin + float(a_split1[0]) * a_xSep)
                                        a_TanbuY2 = int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))))

                                    # 下限値と同じ場合は上部へ伸びる線を描画
                                    if (rainMax != -1):
                                        if (a_TargetCL < 0) or (a_cnt1 == a_TargetCL):
                                            a_draw.line(
                                                [
                                                    (int(self.prv_leftMargin + float(0) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * rainMax)))),
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * rainMax))))
                                                ],
                                                a_pen_color,
                                                a_pen_width
                                            )
                                            a_draw.line(
                                                [
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))))),
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * rainMax))))
                                                ],
                                                a_pen_color,
                                                a_pen_width
                                            )
                                    else:
                                        if (a_TargetCL < 0) or (a_cnt1 == a_TargetCL):
                                            a_draw.line(
                                                [
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))))),
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(self.prv_topMargin))
                                                ],
                                                a_pen_color,
                                                a_pen_width
                                            )
                                else:
                                    # 下限値と異なる場合は上部へ伸びる線を描画
                                    if (a_cnt2 > 0):
                                        a_splitTmp = a_textline[a_cnt2 - 1]
                                        if (rainMax != -1):
                                            a_draw.line(
                                                [
                                                    (int(self.prv_leftMargin + float(0) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * rainMax)))),
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * rainMax))))
                                                ],
                                                a_pen_color,
                                                a_pen_width
                                            )
                                            a_draw.line(
                                                [
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))))),
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * rainMax))))
                                                ],
                                                a_pen_color,
                                                a_pen_width
                                            )
                                        else:
                                            a_draw.line(
                                                [
                                                    (int(self.prv_leftMargin + float(soilMin) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_splitTmp[10 - a_cnt1]))))),
                                                    (int(self.prv_leftMargin + float(soilMin) * a_xSep), int(self.prv_topMargin))
                                                ],
                                                a_pen_color,
                                                a_pen_width
                                            )
                                            a_draw.line(
                                                [
                                                    (int(self.prv_leftMargin + float(soilMin) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_splitTmp[10 - a_cnt1]))))),
                                                    (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1])))))
                                                ],
                                                a_pen_color,
                                                a_pen_width
                                            )
                                a_IsSet = True

                    if (a_setSoilMin == False):
                        if (float(a_split1[10 - a_cnt1]) > 0):
                            if (float(a_split2[10 - a_cnt1]) > 0):
                                a_draw.line(
                                    [
                                        (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))))),
                                        (int(self.prv_leftMargin + float(a_split2[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split2[10 - a_cnt1])))))
                                    ],
                                    a_pen_color,
                                    a_pen_width
                                )
                            else:
                                # 次が0の場合、現在と同じX座標とする。
                                a_draw.line(
                                    [
                                        (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))))),
                                        (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split2[10 - a_cnt1])))))
                                    ],
                                    a_pen_color,
                                    a_pen_width
                                )
                        else:
                            if (float(a_split2[10 - a_cnt1]) > 0):
                                a_draw.line(
                                    [
                                        (int(self.prv_leftMargin + float(a_split1[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split1[10 - a_cnt1]))))),
                                        (int(self.prv_leftMargin + float(a_split2[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split2[10 - a_cnt1])))))
                                    ],
                                    a_pen_color,
                                    a_pen_width
                                )

                # Y=0に強制的に補正
                if (a_split2 != None):
                    if (float(a_split2[10 - a_cnt1]) > 0):
                        a_draw.line(
                            [
                                (int(self.prv_leftMargin + float(a_split2[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(a_split2[10 - a_cnt1]))))),
                                (int(self.prv_leftMargin + float(a_split2[0]) * a_xSep), int(h_img.height - (self.prv_bottomMargin + (a_ySep * float(0)))))
                            ],
                            a_pen_color,
                            a_pen_width
                        )
            #DRAWCONTOUR_CONTIBUE:

            # 端部描画
            if (a_TanbuX1 > 0):
                a_pen_Tanbu_color = (255, 255, 255)
                a_pen_Tanbu_width = 1
                a_draw.line(
                    [
                        (int(a_TanbuX1), int(a_TanbuY1)),
                        (int(a_TanbuX2), int(a_TanbuY2))
                    ],
                    a_pen_Tanbu_color,
                    a_pen_Tanbu_width
                )

                if (a_isDrawTargetCLOnly == False):
                    if (len(a_drawInfo) > 0):
                        a_splitC = a_drawInfo[6].split("#")
                        a_pen_Tanbu_color = (int(a_splitC[0]), int(a_splitC[1]), int(a_splitC[2]))
                        #a_pen_Tanbu.DashStyle = CType(a_drawInfo(7), System.Drawing.Drawing2D.DashStyle)
                        a_pen_Tanbu_width = float(a_drawInfo[8])
                    else:
                        a_pen_Tanbu_color = (0, 0, 128) # 0.9

                        a_draw.line(
                            [
                                (int(a_TanbuX1), int(a_TanbuY1 - 10)),
                                (int(a_TanbuX2), int(a_TanbuY2))
                            ],
                            a_pen_color,
                            a_pen_Tanbu_width
                        )
            #End If

            a_occurColor = []
            a_occurTime = []
            a_occurMark = []
            if ((outAction == self.com.g_Action_MakeContourSnake) or (outAction == self.com.g_Action_MakeContourSoilMin)):
                # 非発生降雨の描画
                if (a_isDrawNonOccurRainfall == True):
                    self._drawNonOccurRainFall(h_img, a_draw, a_xSep, a_ySep)

                # 発生降雨の描画
                self._drawOccurRainFall(h_img, a_draw, a_xSep, a_ySep, a_occurColor, a_occurTime, a_occurMark)
                # Unrealの描画
                self._drawUnreal(h_img, a_draw, a_xLine, a_yLine, a_xSep, a_ySep, unReal)

                # 災害発生のデータを考慮した描画とする。→2006.03.20
                self._drawLegendS(h_img, a_draw, a_occurColor, a_occurTime, a_occurMark, a_drawInfo)
            else:
                a_imgL = Image.open(".\\images\\imgLegendC.gif")
                h_img.paste(
                    a_imgL,
                    (
                        int(h_img.width - self.prv_rightMargin + 5.333333333333333), int(self.prv_topMargin)
                    )
                )

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawContour', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawContour', a_strErr + "," + sys.exc_info())

    def _drawLegendS(
            self,
            h_img,
            h_draw,
            occurColor,
            h_occurTime,
            h_occurMark,
            h_drawInfo
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_drawLegendS', a_strErr)

        try:
            a_fill = (255, 255, 255)
            a_fill2 = (0, 0, 0)
            a_fill3 = (0, 64, 128)
            a_pen_color = (0, 0, 0)
            a_pen_width = 1
            a_pen_color2 = (0, 0, 0)
            a_pen_width2 = 1
            a_fnt_color = (0, 0, 0)   # 黒
            # MS UI Gothic
            a_fnt_font = ImageFont.truetype(
                "C:\\Windows\\Fonts\\msgothic.ttc", 9
            )

            a_textline = []
            a_textSum = 0

            for a_cntDF in range(1, self.com.g_textSum_DisasterFile):
                a_split = self.com.g_textline_DisasterFile[a_cntDF]
                if (a_split[0].strip() == str(self.TargetMeshNo)):
                    if (int(a_split[1].strip()) >= int(self.StartYear)) and (int(a_split[1].strip()) <= int(self.EndYear)):

                        a_strTime = a_split[1].strip() + "/" + a_split[2].strip() + "/" + a_split[3].strip() + " " + a_split[4].strip() + " 災害"
                        a_isOK = True
                        # 同一時刻の災害が複数ある場合
                        if (a_textSum > 0):
                            for a_cnt in range(0, a_textSum):
                                if (a_textline[a_cnt] == a_strTime):
                                    a_isOK = False
                                    break

                        if (a_isOK == True):
                            # 同じメッシュ
                            a_textline.append(a_strTime)
                            a_textSum += 1

            # ボックス⇒[2013.04.16]widthを- 13.3333333333333から- 6.66666666666667
            h_draw.rectangle(
                [
                    (int(h_img.width - self.prv_rightMargin - 33.3333333333333), int(self.prv_topMargin + 6.66666666666667)),
                    (int(h_img.width - 6.66666666666667), int((self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * (10 + (a_textSum + 1))))))
                ],
                fill=a_fill,
                outline=a_pen_color
            )

            # 等高線の凡例
            for a_cnt1 in range(1, 10):
                # 色の設定
                if (len(h_drawInfo) > 0):
                    a_splitC = h_drawInfo[9 + ((9 - a_cnt1) * 3)].split("#")
                    a_pen_color2 = (int(a_splitC[0]), int(a_splitC[1]), int(a_splitC[2]))
                    #a_pen2.DashStyle = CType(h_drawInfo(10 + +((9 - a_cnt1) * 3)), System.Drawing.Drawing2D.DashStyle)
                    a_pen_width2 = float(h_drawInfo[11 + ((9 - a_cnt1) * 3)])
                else:
                    if (a_cnt1 == 1): # 0.1
                        a_pen_color2 = (0, 255, 0)
                    elif (a_cnt1 == 2): # 0.2
                        a_pen_color2 = (0, 0, 255)
                    elif (a_cnt1 == 3): # 0.3
                        a_pen_color2 = (0, 128, 0)
                    elif (a_cnt1 == 4): # 0.4
                        a_pen_color2 = (128, 0, 0)
                    elif (a_cnt1 == 5): # 0.5
                        a_pen_color2 = (128, 0, 128)
                    elif (a_cnt1 == 6): # 0.6
                        a_pen_color2 = (0, 128, 192)
                    elif (a_cnt1 == 7): # 0.7
                        a_pen_color2 = (255, 255, 0)
                    elif (a_cnt1 == 8): # 0.8
                        a_pen_color2 = (255, 0, 255)
                    elif (a_cnt1 == 9): # 0.9
                        a_pen_color2 = (0, 0, 128)

                h_draw.line(
                    [
                        (int((h_img.width - self.prv_rightMargin) - 20), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * a_cnt1))),
                        (int((h_img.width - self.prv_rightMargin) + 13.3333333333333), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * a_cnt1)))
                    ],
                    a_pen_color2,
                    a_pen_width2
                )
                h_draw.text(
                    (int((h_img.width - self.prv_rightMargin) + 20), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * a_cnt1) - 4)),
                    str(a_cnt1 / 10),
                    font=a_fnt_font,
                    fill=(0, 0, 0)
                )

            # 非発生降雨の凡例
            # EllipseのX,Yは左上角の位置である。
            h_draw.ellipse(
                [
                    (int(h_img.width - self.prv_rightMargin - 1), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * 10) - 1)),
                    (int(h_img.width - self.prv_rightMargin + 1), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * 10) + 1))
                ],
                fill=a_fill3,
                outline=(0, 0, 0)
            )
            h_draw.text(
                (int((h_img.width - self.prv_rightMargin) + 20), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * 10) - 4)),
                "非発生降雨",
                font=a_fnt_font,
                fill=(0, 0, 0)
            )

            # MS UI Gothic
            a_fnt_font2 = ImageFont.truetype(
                "C:\\Windows\\Fonts\\msgothic.ttc", 18
            )
            a_iCnt2 = 0
            a_x1 = 0
            a_y1 = 0
            a_x2 = 0
            a_y2 = 0
            a_x3 = 0

            for a_cnt in range(0, len(h_occurTime)):
                if (len(h_occurTime[a_cnt]) > 0):
                    a_pen_color2 = (occurColor[a_cnt][0], occurColor[a_cnt][1], occurColor[a_cnt][2])
                    a_pen_width2 = 2

                    a_strTmp = h_occurTime[a_cnt][1:]
                    a_textline = a_strTmp.split("#")

                    for a_strTmp in a_textline:
                        a_x1 = int((h_img.width - self.prv_rightMargin) - 20)
                        a_y1 = int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * (10 + a_iCnt2 + 1)))
                        a_x2 = int((h_img.width - self.prv_rightMargin) + 13.3333333333333)
                        a_y2 = int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * (10 + a_iCnt2 + 1)))
                        a_x3 = a_x1 + ((a_x2 - a_x1) / 2)
                        h_draw.line(
                            [
                                (int((h_img.width - self.prv_rightMargin) - 20), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * (10 + a_iCnt2 + 1)))),
                                (int((h_img.width - self.prv_rightMargin) + 13.3333333333333), int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * (10 + a_iCnt2 + 1))))
                            ],
                            a_pen_color2,
                            a_pen_width2
                        )
                        h_draw.text(
                            (
                                int((h_img.width - self.prv_rightMargin) + 20),
                                int(self.prv_topMargin + 6.66666666666667 + (17.3333333333333 * (10 + a_iCnt2 + 1)) - 4)
                            ),
                            a_strTmp + " 災害",
                            font=a_fnt_font,
                            fill=(0, 0, 0)
                        )

                        for a_iCnt3 in range(0, len(h_occurMark)):
                            a_textline3 = h_occurMark[a_iCnt3].split("#")
                            if (a_textline3[0] == a_strTmp):
                                a_iTmp = int(a_textline3[1])
                                if (a_iTmp == 1):   # 赤○（外側は黒線）
                                    # EllipseのX,Yは左上角の位置である。
                                    h_draw.ellipse(
                                        [
                                            (int(float(a_x3) - 6.66666666666667), int(float(a_y1) - 6.66666666666667)),
                                            (int(float(a_x3) + 6.66666666666667), int(float(a_y1) + 6.66666666666667))
                                        ],
                                        fill=(255, 0, 0),
                                        outline=(0, 0, 0)
                                    )
                                elif (a_iTmp == 2):   # 青◇（外側は黒線）
                                    h_draw.polygon(
                                        [
                                            (int(float(a_x3)), int(float(a_y1) + 6.66666666666667)),
                                            (int(float(a_x3) - 6.66666666666667), int(float(a_y1))),
                                            (int(float(a_x3)), int(float(a_y1) - 6.66666666666667)),
                                            (int(float(a_x3) + 6.66666666666667), int(float(a_y1)))
                                        ],
                                        fill=(0, 0, 255),
                                        outline=(0, 0, 0)
                                    )
                                elif (a_iTmp == 3):   # 緑△（外側は黒線）
                                    h_draw.polygon(
                                        [
                                            (int(float(a_x3) - 6.66666666666667), int(float(a_y1) + 6.66666666666667)),
                                            (int(float(a_x3)), int(float(a_y1) - 6.66666666666667)),
                                            (int(float(a_x3) + 6.66666666666667), int(float(a_y1) + 6.66666666666667))
                                        ],
                                        fill=(0, 255, 0),
                                        outline=(0, 0, 0)
                                    )
                                elif (a_iTmp == 4):   # 黄□（外側は黒線）
                                    h_draw.rectangle(
                                        [
                                            (int(float(a_x3) - 6.66666666666667), int(float(a_y1) - 6.66666666666667)),
                                            (int(float(a_x3) + 6.66666666666667), int(float(a_y1) + 6.66666666666667))
                                        ],
                                        fill=(255, 255, 0),
                                        outline=(0, 0, 0)
                                    )
                                elif (a_iTmp ==5):   # 赤×
                                    h_draw.text(
                                        (int(float(a_x3) - a_fnt_font2.size * 10), int(float(a_y1) - a_fnt_font2.size * 10)),
                                        "×",
                                        font=a_fnt_font2,
                                        fill=(255, 0, 0)
                                    )
                                elif (a_iTmp == 6):   # 青＊
                                    h_draw.text(
                                        (int(float(a_x3) - a_fnt_font2.size * 10), int(float(a_y1) - a_fnt_font2.size * 10)),
                                        "＊",
                                        font=a_fnt_font2,
                                        fill=(0, 0, 255)
                                    )
                                elif (a_iTmp == 7):   # 緑＋
                                    h_draw.text(
                                        (int(float(a_x3) - a_fnt_font2.size * 10), int(float(a_y1) - a_fnt_font2.size * 10)),
                                        "＋",
                                        font=a_fnt_font2,
                                        fill=(0, 255, 0)
                                    )
                                elif (a_iTmp == 8):   # その他
                                    # EllipseのX,Yは左上角の位置である。
                                    h_draw.ellipse(
                                        [
                                            (int(a_x3), int(a_y1)),
                                            (int(a_x3 + 13.3333333333333), int(a_y1 + 13.3333333333333))
                                        ],
                                        fill=(255, 0, 0),
                                        outline=(0, 0, 0)
                                    )

                                break

                        a_iCnt2 += 1

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawLegendS', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawLegendS', a_strErr + "," + sys.exc_info())

    def _drawNonOccurRainFall(
            self,
            h_img,
            h_draw,
            xSep,
            ySep
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_drawNonOccurRainFall', a_strErr)

        try:
            a_fill = (0, 64, 128)
            a_outline = (0, 64, 128)

            for a_cnt in range(int(self.StartYear), int(self.EndYear) + 1):
                a_textline = []
                a_textSum = self.com.Store_DataFile(self.com.g_OutPath + "\\" + str(self.TargetMeshNo) + "\\" + self.com.g_ChainOnlyOccurRainfallSymbol + str(a_cnt) + ".csv", a_textline)
                for a_cnt2 in range(1, a_textSum):
                    a_split = a_textline[a_cnt2]
                    # 非発生降雨を点で描画する
                    # EllipseのX,Yは左上角の位置である。
                    h_draw.ellipse(
                        [
                            (int(self.prv_leftMargin + (float(a_split[7]) * xSep) - 1), int(h_img.height - (self.prv_bottomMargin + (float(a_split[6]) * ySep)) - 1)),
                            (int(self.prv_leftMargin + (float(a_split[7]) * xSep) + 1), int(h_img.height - (self.prv_bottomMargin + (float(a_split[6]) * ySep)) + 1))
                        ],
                        fill=a_fill,
                        outline=a_outline
                    )

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawNonOccurRainFall', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawNonOccurRainFall', a_strErr + "," + sys.exc_info())

    def _drawOccurRainFall(
            self,
            h_img,
            h_draw,
            xSep,
            ySep,
            occurColor,
            h_occurTime,
            h_occurMark
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_drawOccurRainFall', a_strErr)

        try:
            '''
            if (self.com.g_PastKind == 0):
                # 取り込みなし
                a_surfaceFile = self.com.g_RBFNOutPath + "\\" + "surface-" + self.TargetMeshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
            else:
                # 取り込みあり
                # 既往CL対象メッシュ選択サポート
                a_surfaceFile = self.com.g_PastRBFNOutPath + "\\" + "surface-" + self.com.GetTargetMeshNoByCL(self.com.g_TargetStartYear, self.TargetMeshNo) + "-" + str(self.com.g_PastTargetStartYear) + "-" + str(self.com.g_PastTargetEndYear) + ".csv"
                a_textlineSR = []
            a_textSumSR = self.com.Store_DataFile(a_surfaceFile, a_textlineSR)
            '''

            # 災害発生情報を読み込む
            a_textline2 = []
            a_textSum2 = 0
            for a_cntDF in range(1, self.com.g_textSum_DisasterFile):
                a_strTmp = self.com.g_textline_DisasterFile[a_cntDF]
                a_split = a_strTmp
                if (a_split[0].strip() == str(self.TargetMeshNo)):
                    # 同じメッシュ番号
                    a_textline2.append(a_split[0] + "," + a_split[1]+ "," + a_split[2]+ "," + a_split[3]+ "," + a_split[4]+ "," + a_split[5])
                    a_textSum2 += 1

            a_X1 = 0
            a_Y1 = 0
            a_Z1 = 0
            a_X2 = 0
            a_Y2 = 0
            a_Z2 = 0
            a_X3 = 0
            a_Y3 = 0
            a_Z3 = 0
            a_X4 = 0
            a_Y4 = 0
            a_Z4 = 0
            a_XN = 0
            a_YN = 0
            a_ZN = 0

            a_colorRGB = [[0 for i in range(3)] for j in range(3)]
            a_lineStyle = [0]*3
            a_pen_color = (0, 0, 0)
            a_pen_width = 1
            a_fnt_color = (0, 0, 0)   # 黒
            # MS UI Gothic
            a_fnt_font = ImageFont.truetype(
                "C:\\Windows\\Fonts\\msgothic.ttc", 9
            )
            a_fnt_font2 = ImageFont.truetype(
                "C:\\Windows\\Fonts\\msgothic.ttc", 18
            )
            a_fill = (0, 0, 0)
            a_outline = (0, 0, 0)

            #災害発生ラインの色の初期設定
            a_colorRGB[0][0] = 255
            a_colorRGB[0][1] = 0
            a_colorRGB[0][2] = 0

            a_colorRGB[1][0] = -50
            a_colorRGB[1][1] = 0
            a_colorRGB[1][2] = 255

            a_colorRGB[2][0] = 0
            a_colorRGB[2][1] = 255
            a_colorRGB[2][2] = -50
            '''
            a_lineStyle[0] = Drawing2D.DashStyle.Solid
            a_lineStyle[1] = Drawing2D.DashStyle.Dot
            a_lineStyle[2] = Drawing2D.DashStyle.Dot
            '''

            a_color_minus = 55
            a_nowLine = 1
            a_nextLine = 1

            del occurColor[:]
            occurColor.append([0]*3)
            #occurColor = [[0]*3]*a_textSum2

            del h_occurTime[:]
            del h_occurMark[:]

            a_pen_style = a_lineStyle[0]
            a_pen_color = (a_colorRGB[0][0], a_colorRGB[0][1], a_colorRGB[0][2])

            occurColor[0][0] = a_colorRGB[0][0]
            occurColor[0][1] = a_colorRGB[0][1]
            occurColor[0][2] = a_colorRGB[0][2]

            a_occurCnt = 0
            a_i = 0

            for a_cnt in range(int(self.StartYear), int(self.EndYear) + 1):
                a_sw = open(self.com.g_OutPath + "\\" + str(self.TargetMeshNo) + "\\" + self.com.g_OccurRainfallRBFNNear + str(a_cnt) + ".csv", "w", encoding="shift_jis")

                a_pen_width = 2

                a_prevX = -999
                a_prevY = -999
                a_prevTime = ""
                a_IsPlot = False

                a_textline = []
                a_textSum = self.com.Store_DataFile(self.com.g_OutPath + "\\" + str(self.TargetMeshNo) + "\\" + self.com.g_OccurRainfallSymbol + str(a_cnt) + ".csv", a_textline)

                a_split = a_textline[0]
                a_sw.write(a_split[0] + "," + a_split[1] + "," + a_split[2] + "," + a_split[3] + "," + a_split[4] + "," + a_split[5] + "," + a_split[6] + "," + a_split[7] + ",RBFN近似値\n")

                for a_cnt1 in range(1, a_textSum):
                    # 災害発生線の種類を可変にする対応→2006.03.22
                    if (a_nextLine != a_nowLine):
                        a_nowLine = a_nextLine
                        if (a_nowLine > 3):
                            a_nowLine = 1
                            a_nextLine = 1
                        '''
                        if (a_lineStyle[a_nowLine - 1] = Drawing2D.DashStyle.Solid):
                            a_lineStyle[a_nowLine - 1] = Drawing2D.DashStyle.Dot
                        else:
                            a_lineStyle[a_nowLine - 1] = Drawing2D.DashStyle.Solid
                            '''

                        if (a_nowLine == 1):
                            a_i = 1
                        elif (a_nowLine == 2):
                            a_i = 0
                        elif (a_nowLine == 3):
                            a_i = 2

                        if (a_colorRGB[a_nowLine - 1][a_i] < 0):
                            a_colorRGB[a_nowLine - 1][a_i] = 0
                        else:
                            a_colorRGB[a_nowLine - 1][a_i] = a_colorRGB[a_nowLine - 1][a_i] - a_color_minus
                            if (a_colorRGB[a_nowLine - 1][a_i] < 0):
                                a_colorRGB[a_nowLine - 1][a_i] = 255

                        #a_pen_style = a_lineStyle[a_nowLine - 1]
                        a_pen_color = (a_colorRGB[a_nowLine - 1][0], a_colorRGB[a_nowLine - 1][1], a_colorRGB[a_nowLine - 1][2])

                        a_occurCnt = a_occurCnt + 1
                        h_occurTime.append("")
                        occurColor.append([0]*3)
                        occurColor[a_occurCnt][0] = a_colorRGB[a_nowLine - 1][0]
                        occurColor[a_occurCnt][1] = a_colorRGB[a_nowLine - 1][1]
                        occurColor[a_occurCnt][2] = a_colorRGB[a_nowLine - 1][2]

                    a_split = a_textline[a_cnt1]
                    # 土壌雨量指数・解析雨量かsurfaceの内容からABCDの座標を取得
                    '''
                    for a_SRCnt in range(0, a_textSumSR):
                        a_splitSR = a_textlineSR[a_SRCnt]
                        '''
                    for a_SRCnt in range(0, self.com.g_textSum_RBFNFile):
                        a_splitSR = self.com.g_textline_RBFNFile[a_SRCnt]
                        if (a_SRCnt == 0):
                            # 1行目
                            for a_SRCnt2 in range(1, len(a_splitSR) - 1):
                                if (float(a_split[7]) >= float(a_splitSR[a_SRCnt2])) and (float(a_split[7]) < float(a_splitSR[a_SRCnt2 + 1])):
                                    # 範囲内
                                    a_X1 = float(a_splitSR[a_SRCnt2])
                                    a_X2 = float(a_splitSR[a_SRCnt2 + 1])
                                    a_X3 = float(a_splitSR[a_SRCnt2 + 1])
                                    a_X4 = float(a_splitSR[a_SRCnt2])
                                    break
                        else:
                            # 2行目以降
                            if (float(a_split[6]) >= float(a_splitSR[0])):  #文字列による不当な判断
                                # 範囲内
                                a_Y1 = float(a_splitSR[0])
                                a_Y2 = float(a_splitSR[0])
                                a_Z1 = float(a_splitSR[a_SRCnt2])   #★pending
                                a_Z2 = float(a_splitSR[a_SRCnt2 + 1])   #★pending
                            else:
                                if (float(a_split[6]) < float(a_splitSR[0])):   # 文字列による不当な判断
                                    # 範囲内
                                    a_Y3 = float(a_splitSR[0])
                                    a_Y4 = float(a_splitSR[0])
                                    a_Z3 = float(a_splitSR[a_SRCnt2 + 1])   #★pending
                                    a_Z4 = float(a_splitSR[a_SRCnt2])   #★pending
                                    break

                    a_XN, a_YN, a_ZN = self._calcNearRBFN(
                        float(a_split[7]),
                        float(a_split[6]),
                        a_X1,
                        a_Y1,
                        a_Z1,
                        a_X2,
                        a_Y2,
                        a_Z2,
                        a_X3,
                        a_Y3,
                        a_Z3,
                        a_X4,
                        a_Y4,
                        a_Z4
                    )

                    a_sw.write(a_split[0] + "," + a_split[1] + "," + a_split[2] + "," + a_split[3] + "," + a_split[4] + "," + a_split[5] + "," + a_split[6] + "," + a_split[7] + "," + str(a_ZN) + "\n")
                    # 同一年で複数の災害発生に対応→2006.03.22
                    # 年月日時を取得
                    a_nowTime = a_split[2] + "/" + a_split[3] + "/" + a_split[4] + " " + a_split[5]
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
                            # 異なる災害発生降雨となる。
                            a_prevX = -999
                            a_prevY = -999
                            a_IsPlot = False
                            a_nextLine = a_nowLine + 1
                    a_prevTime = a_nowTime

                    if (float(a_split[6]) > 0):
                        if (a_prevX != -999):
                            # 発生降雨を線で描画する
                            h_draw.line(
                                [
                                    (int(self.prv_leftMargin + a_prevX * xSep), int(h_img.height - (self.prv_bottomMargin + (ySep * a_prevY)))),
                                    (int(self.prv_leftMargin + float(a_split[7]) * xSep), int(h_img.height - (self.prv_bottomMargin + (ySep * float(a_split[6])))))
                                ],
                                a_pen_color,
                                a_pen_width
                            )
                            a_IsPlot = True
                        a_prevX = float(a_split[7])
                        a_prevY = float(a_split[6])

                    # 災害発生時刻のプロット→2006.03.22
                    for a_cnt2 in range(0, a_textSum2):
                        a_split2 = a_textline2[a_cnt2].split(",")
                        if (a_split[2] == a_split2[1].strip()) and (a_split[3] == a_split2[2].strip()) and (a_split[4] == a_split2[3].strip()) and (a_split[5] == a_split2[4].strip()):
                            # 同じ年月日
                            # X,Y座標値を退避する。
                            a_textline2[a_cnt2] = \
                                a_split2[0] + "," + a_split2[1] + "," + a_split2[2] + "," + a_split2[3] + "," + a_split2[4] + "," + a_split2[5] + \
                                "," + str(self.prv_leftMargin + float(a_split[7]) * xSep) + "," + str(h_img.height - (self.prv_bottomMargin + (ySep * float(a_split[6]))))
                            if (len(h_occurTime) == 0):
                                h_occurTime.append("")
                            h_occurTime[a_occurCnt] += "#" + a_split2[1] + "/" + a_split2[2] + "/" + a_split2[3] + " " + a_split2[4]
                            break

                a_sw.close()

                if (a_IsPlot == True):
                    a_nextLine = a_nowLine + 1

            a_iMark = 0
            for a_cnt2 in range(0, a_textSum2):
                a_split2 = a_textline2[a_cnt2].split(",")
                if (len(a_split2) >= 8):
                    if (a_split2[6] != "") and (a_split2[7] != ""):
                        a_mark = int(a_split2[5])
                        a_iMark += 1
                        h_occurMark.append(a_split2[1] + "/" + a_split2[2] + "/" + a_split2[3] + " " + a_split2[4] + "#" + str(a_mark))

                        if (a_mark == 1):   # 赤○（外側は黒線）
                            # EllipseのX,Yは左上角の位置である。
                            h_draw.ellipse(
                                [
                                    (int(float(a_split2[6]) - 6.666666666666667), int(float(a_split2[7]) - 6.666666666666667)),
                                    (int(float(a_split2[6]) + 6.666666666666667), int(float(a_split2[7]) + 6.666666666666667))
                                ],
                                fill = (255, 0, 0),
                                outline = (0, 0, 0)
                            )
                        elif (a_mark == 2):   # 青◇（外側は黒線）
                            h_draw.polygon(
                                [
                                    (int(float(a_split2[6])), int(float(a_split2[7]) + 6.666666666666667)),
                                    (int(float(a_split2[6]) - 6.666666666666667), int(float(a_split2[7]))),
                                    (int(float(a_split2[6])), int(float(a_split2[7]) - 6.666666666666667)),
                                    (int(float(a_split2[6]) + 6.666666666666667), int(float(a_split2[7])))
                                ],
                                fill = (0, 0, 255),
                                outline = (0, 0, 0)
                            )
                        elif (a_mark == 3):   # 緑△（外側は黒線）
                            h_draw.polygon(
                                [
                                    (int(float(a_split2[6]) - 6.666666666666667), int(float(a_split2[7]) + 6.666666666666667)),
                                    (int(float(a_split2[6])), int(float(a_split2[7]) - 6.666666666666667)),
                                    (int(float(a_split2[6]) + 6.666666666666667), int(float(a_split2[7]) + 6.666666666666667))
                                ],
                                fill = (0, 255, 0),
                                outline = (0, 0, 0)
                            )
                        elif (a_mark == 4):   # 黄□（外側は黒線）
                            h_draw.rectangle(
                                [
                                    (int(float(a_split2[6]) - 6.666666666666667), int(float(a_split2[7]) - 6.666666666666667)),
                                    (int(float(a_split2[6]) + 6.666666666666667), int(float(a_split2[7]) + 6.666666666666667))
                                ],
                                fill = (255, 255, 0),
                                outline = (0, 0, 0)
                            )
                        elif (a_mark == 5):   # 赤×
                            h_draw.text(
                                (int(float(a_split2[6]) - a_fnt_font2.size * 10), int(float(a_split2[7]) - a_fnt_font2.size * 10)),
                                "×",
                                font=a_fnt_font2,
                                fill=(255, 0, 0)
                            )
                        elif (a_mark == 6):   # 青＊
                            h_draw.text(
                                (int(float(a_split2[6]) - a_fnt_font2.size * 10), int(float(a_split2[7]) - a_fnt_font2.size * 10)),
                                "＊",
                                font=a_fnt_font2,
                                fill=(0, 0, 255)
                            )
                        elif (a_mark == 7):   # 緑＋
                            h_draw.text(
                                (int(float(a_split2[6]) - a_fnt_font2.size * 10), int(float(a_split2[7]) - a_fnt_font2.size * 10)),
                                "＋",
                                font=a_fnt_font2,
                                fill=(0, 255, 0)
                            )
                        else:   # その他
                            # EllipseのX,Yは左上角の位置である。
                            h_draw.ellipse(
                                [
                                    (int(a_split2[6]), int(a_split2[7])),
                                    (int(a_split2[6] + 13.333333333333334), int(a_split2[7] + 13.333333333333334))
                                ],
                                fill=(255, 0, 0),
                                outline=(0, 0, 0)
                            )

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawOccurRainFall', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawOccurRainFall', a_strErr + "," + sys.exc_info())

    def _drawUnreal(
            self,
            h_img,
            h_draw,
            xLine,
            yLine,
            xSep,
            ySep,
            unReal
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_drawUnreal', a_strErr)

        try:
            if (unReal > 0):
                a_unReal = unReal
            else:
                a_unReal = self.com.g_UnrealAlpha

            a_fill = (0, 0, 0)  #(0, 64, 128)
            a_outline = (0, 0, 0)  #(0, 64, 128)

            h_draw.polygon(
                [
                    (int(self.prv_leftMargin), int(h_img.height - self.prv_bottomMargin)),
                    (int(self.prv_leftMargin), int(h_img.height - (self.prv_bottomMargin + (ySep * (self.com.g_yUnit * yLine))))),
                    (int(self.prv_leftMargin + xSep * ((self.com.g_yUnit * yLine) / a_unReal)), int(h_img.height - (self.prv_bottomMargin + (ySep * (self.com.g_yUnit * yLine)))))
                ],
                fill=a_fill,
                outline=a_outline
            )

            a_imgL = Image.open(".\\images\\imgUnreal.gif")
            h_img.paste(
                a_imgL,
                (
                    int(self.prv_leftMargin + 6.666666666666667), int(self.prv_topMargin + 33.333333333333336)
                )
            )

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawUnreal', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_drawUnreal', a_strErr + "," + sys.exc_info())

    def _getGraphDrawInfo(
            self,
            msno,
            h_drawInfo
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_getGraphDrawInfo', a_strErr)

        try:
            del h_drawInfo[:]

            a_iCnt2 = 0
            a_IsOK = False

            for a_iCnt2 in range(0, self.com.g_textSum_TargetMeshFile):
                a_split1 = self.com.g_textline_TargetMeshFile[a_iCnt2]

                if (self.com.g_TargetRainMesh == 1):
                    a_chkSum = 37
                    # 1kmメッシュ
                    if (a_split1[1] == msno):
                        a_IsOK = True
                else:
                    # 5kmメッシュ
                    a_chkSum = 36
                    if (a_split1[0] == msno):
                        a_IsOK = True

                if (a_IsOK == True):
                    # グラブ描画情報は35個あある。
                    h_drawInfo = [""]*a_chkSum
                    if (len(a_split1) >= a_chkSum):
                        for a_iCnt in range(0, a_chkSum):
                            if (self.com.g_TargetRainMesh == 1):
                                # 1kmメッシュ
                                if (a_iCnt > 0):
                                    h_drawInfo[a_iCnt - 1] = a_split1[a_iCnt]
                            else:
                                # 5kmメッシュ
                                h_drawInfo[a_iCnt] = a_split1[a_iCnt]
                    else:
                        del h_drawInfo[:]
                    break

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getGraphDrawInfo', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_getGraphDrawInfo', a_strErr + "," + sys.exc_info())

    # オリジナル等高線の作成
    def _makeAutoContourOrigin(self, h_meshNo):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeAutoContourOrigin', a_strErr)

        try:
            a_img = Image.new("RGB", (int(self.com.g_ImageFileWidth), int(self.com.g_ImageFileHeight)), (255, 255, 355))

            self._makeContourOriginEx()
            self._drawContour(self.com.g_ContourOriginSymbol, self.com.g_Action_MakeContourOrigin, a_img, -1, 0, -1, 0, h_meshNo)
            self._saveContourImage(self.com.g_ContourOriginSymbol, a_img)

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeAutoContourOrigin', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeAutoContourOrigin', a_strErr + "," + sys.exc_info())

    # 等高線の補正
    def _makeAutoContourRevise(self, h_meshNo):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeAutoContourRevise', a_strErr)

        try:
            a_img = Image.new("RGB", (int(self.com.g_ImageFileWidth), int(self.com.g_ImageFileHeight)), (255, 255, 355))

            self._contourRevise()
            self._drawContour(self.com.g_ContourReviseSymbol, self.com.g_Action_MakeContourRevise, a_img, -1, 0, -1, 0, h_meshNo)
            self._saveContourImage(self.com.g_ContourReviseSymbol, a_img)

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeAutoContourRevise', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeAutoContourRevise', a_strErr + "," + sys.exc_info())

    # スネーク曲線の作成
    def _makeAutoContourSnake(self, h_meshNo):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeAutoContourSnake', a_strErr)

        try:
            a_img = Image.new("RGB", (int(self.com.g_ImageFileWidth), int(self.com.g_ImageFileHeight)), (255, 255, 355))

            # 既往CLの取り込み
            if (self.com.g_PastKind == 0):
                # 取り込みなし
                self._drawContour(self.com.g_ContourReviseSymbol, self.com.g_Action_MakeContourSnake, a_img, -1, 0, -1, 0, h_meshNo)
                self._saveContourImage(self.com.g_ContourSnakeSymbol, a_img)
            else:
                # 取り込みあり
                a_RBFN = 0
                a_soilMin = 0
                a_rainMax = -1    # 60分間積算雨量上限値のサポート
                a_RBFN , a_soilMin, a_rainMax = self.com.GetPastCLData(h_meshNo, ) #60分間積算雨量上限値のサポート
                self._contourSoilMin(a_soilMin, a_rainMax)  # 60分間積算雨量上限値のサポート

                # 土壌雨量指数下限値のファイル名で作成されるので、コピーし直す。⇒上書き
                # 既往CL対象メッシュ選択サポート
                shutil.copyfile(
                    self.com.g_OutPath + "\\" + self.com.g_ContourReviseSoilMinSymbol + "-" + h_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv",
                    self.com.g_OutPath + "\\" + self.com.g_ContourReviseSymbol + "-" + h_meshNo + "-" + str(self.com.g_TargetStartYear) + "-" + str(self.com.g_TargetEndYear) + ".csv"
                )

                a_dRBFN = 0.9
                a_dRBFN = self.com.My_round(a_dRBFN - 0.1 * a_RBFN, 1)  # 四捨五入
                #a_dRBFN = round(a_dRBFN - 0.1 * a_RBFN, 1)  # 四捨五入

                self._drawContour(self.com.g_ContourReviseSoilMinSymbol, self.com.g_Action_MakeContourSoilMin, a_img, a_dRBFN, a_soilMin, a_rainMax, 0, h_meshNo)   # 60分間積算雨量上限値のサポート
                self._saveContourImage(self.com.g_ContourSnakeSymbol, a_img)

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeAutoContourSnake', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeAutoContourSnake', a_strErr + "," + sys.exc_info())

    def _makeContourOriginEx(self):
        a_strErr = ""
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_makeContourOriginEx', a_strErr)

        try:
            # 結果出力のパスを作成
            if (os.path.isdir(self.com.g_OutPath + "\\" +self.TargetMeshNo) == False):
                os.mkdir(self.com.g_OutPath + "\\" + self.TargetMeshNo)

            a_sw = open(self.com.g_OutPath + "\\" + self.com.g_ContourOriginSymbol + "-" + self.TargetMeshNo + "-" + str(self.StartYear) + "-" + str(self.EndYear) + ".csv", "w", encoding="shift_jis")

            # 全てのデータを読み込む
            a_ySum = self.com.g_textSum_RBFNFile
            a_xSum = len(self.com.g_textline_RBFNFile[0]) #- 1

            # 0.1～0.9まで、0.1刻みの等高線データを作成
            # ここは後で再検討要？
            a_dCnt = 0
            a_findSum = 0
            a_t0 = 0
            a_t1 = 0
            a_yTmp = 0

            #オリジナルのX値(土壌雨量指数)の行を読み込む。
            a_writeline = ""
            a_split1 = self.com.g_textline_RBFNFile[0]
            # 土壌雨量指数分、処理を繰り返す。
            for a_cnt1 in range(1, a_xSum):
                # 解析雨量数分、処理を繰り返す。
                a_findSum = 0
                a_yTmp = -1
                for a_cnt2 in range(1, a_ySum - 1):   # 最終で処理される事はない？
                    a_split2 = self.com.g_textline_RBFNFile[a_cnt2]
                    a_split3 = self.com.g_textline_RBFNFile[a_cnt2 + 1]  # 最終で処理される事はない？

                    a_t0 = float(a_split2[a_cnt1])
                    a_t1 = float(a_split3[a_cnt1])

                    if (a_yTmp == -1):
                        if ((a_cnt1 == 1) or (a_cnt1 == a_xSum - 1)):
                            # 土壌雨量指数が0もしくはMAX値の場合
                            # 最初の土壌雨量指数値を求める。
                            a_yTmp = float(a_split1[a_cnt1])
                            a_writeline = str(a_yTmp)
                        else:
                            a_yTmp = float(a_split1[a_cnt1])
                            a_writeline = str(a_yTmp)

                    a_dCnt = 0.9
                    #for a_dCnt in range(0.9, 0.1, -0.1):
                    while a_dCnt > 0:
                        if (a_t0 >= a_dCnt) and (a_t1 < a_dCnt):
                            # 境界線の近似値を検出
                            a_sTmp, a_findSum = self._setOriginContourYRevise(a_dCnt, a_findSum)
                            a_writeline += a_sTmp
                            # 解析雨量値の算出
                            a_writeline += self._setOriginContourY(float(a_split2[0]), float(a_split3[0]), a_t0, a_t1, a_dCnt)
                            a_findSum += 1
                            break
                        a_dCnt -= 0.1

                    if (a_findSum == 9):
                        # 0.1～0.9全てが検出された場合は、ループを抜ける。
                        a_sw.write(a_writeline + "\n")
                        break

            a_sw.close()

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeContourOriginEx', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_makeContourOriginEx', a_strErr + "," + sys.exc_info())

    # 等高線の保存
    def _saveContourImage(self, h_symbol, h_img):
        a_strErr = "h_symbol=" + h_symbol
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_saveContourImage', a_strErr)

        try:
            h_img.save(self.com.g_OutPath + "\\" + h_symbol + "-" + self.TargetMeshNo + "-" + str(self.StartYear) + "-" + str(self.EndYear) + ".bmp", "BMP")

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_saveContourImage', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_saveContourImage', a_strErr + "," + sys.exc_info())

    # 解析雨量等高線の値計算処理
    def _setOriginContourY(
            self,
            nowY,
            nextY,
            nowZ,
            nextZ,
            contour
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_setOriginContourY', a_strErr)

        a_sRet = ""

        try:
            a_ta = nextY - nowY
            a_tb = nowZ - nextZ
            a_tc = contour - nextZ

            a_sRet = "," + str(nowY + ((a_ta * a_tc) / a_tb))

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_setOriginContourY', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_setOriginContourY', a_strErr + "," + sys.exc_info())

        return a_sRet

    # 解析雨量等高線の補正処理
    def _setOriginContourYRevise(
            self,
            contour,
            nowSum
    ):
        a_strErr = "meshNo=" + self.meshNo
        self.com.Outputlog(self.com.g_LOGMODE_TRACE1, '_setOriginContourYRevise', a_strErr)

        a_sRet = ""
        a_nowSum = nowSum

        try:
            #a_tmp1 = int((0.9 - contour) * 10)
            # ★pythonでは、先に小数計算するとおかしくなる。
            a_tmp1 = (int(0.9*10) - int(contour*10))
            a_tmp2 = a_tmp1 - a_nowSum

            for a_cnt in range(1, a_tmp2 + 1):
                a_sRet += ",0"
                a_nowSum += 1

        except Exception as exp:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_setOriginContourYRevise', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.com.Outputlog(self.com.g_LOGMODE_ERROR, '_setOriginContourYRevise', a_strErr + "," + sys.exc_info())

        return a_sRet, a_nowSum
