################################################################################
# 全降雨データの作成
################################################################################
import os
import datetime
import csv
import com_functions
import threading
import clsRainfall
import clsFigure
from multiprocessing import Process

com = com_functions.ComFunctions()

prv_RainfallFileName = ""
prv_SoilRainFileName = ""
prv_RainfallFileName1 = ""
prv_SoilRainFileName1 = ""
prv_TemperatureFileName = ""

g_meshSum = 0
g_meshList = []
g_meshList2 = []

def _getMeshSum(h_year, h_RainfallFileName, h_meshList):
    a_strErr = "Year=" + str(h_year) + ",RainfallFileName=" + h_RainfallFileName
    com.Outputlog(com.g_LOGMODE_INFORMATION, '_getMeshSum', a_strErr)

    a_iRet = 0

    try:
        # 解析雨量ファイルを開く。
        a_sr = open(h_RainfallFileName, 'r', encoding='shift_jis')
        # メッシュファイルを開く。
        a_sw = open(com.g_OutPath + "\\" + com.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
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
        com.Outputlog(com.g_LOGMODE_ERROR, type(exp), a_strErr)

    com.Outputlog(com.g_LOGMODE_INFORMATION, 'a_iRet', str(a_iRet))
    #com.Outputlog(com.g_LOGMODE_INFORMATION, '_getMeshSum', 'end')

    return a_iRet

def _getMeshSumFromFile(h_year, h_RainfallFileName, h_meshList):
    a_strErr = "Year=" + str(h_year) + ",RainfallFileName=" + h_RainfallFileName
    com.Outputlog(com.g_LOGMODE_INFORMATION, '_getMeshSumFromFile', a_strErr)

    a_iRet = 0

    try:
        # 対象メッシュNoファイルを開く。
        a_sr = open(com.g_TargetMeshFile, 'r', encoding='shift_jis')
        # メッシュ数をカウントする。
        a_textline = a_sr.readline().rstrip('\r\n')
        while a_textline:
            a_iRet += 1
            a_textline = a_sr.readline().rstrip('\r\n')
        a_sr.close()
        # 対象メッシュNoファイルを開く。
        a_sr = open(com.g_TargetMeshFile, 'r', encoding='shift_jis')
        # メッシュファイルを開く。
        a_sw = open(com.g_OutPath + "\\" + com.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
        # メッシュ数を書込
        a_sw.write(str(a_iRet) + '\n')
        # メッシュ番号を取得する。
        a_textline = a_sr.readline().rstrip('\r\n')
        while a_textline:
            #print(a_textline)
            if (a_textline != ''):
                # メッシュ番号を書き込み
                a_split = a_textline.split(',')
                if com.g_TargetRainMesh == 1:
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
        com.Outputlog(com.g_LOGMODE_ERROR, type(exp), a_strErr)

    #com.Outputlog(com.g_LOGMODE_INFORMATION, 'a_iRet', str(a_iRet))
    #com.Outputlog(com.g_LOGMODE_INFORMATION, '_getMeshSumFromFile', 'end')

    return a_iRet

def _getMeshSumFromFile2(h_year, h_RainfallFileName, h_meshList):
    a_strErr = "Year=" + str(h_year) + ",RainfallFileName=" + h_RainfallFileName
    com.Outputlog(com.g_LOGMODE_INFORMATION, '_getMeshSumFromFile2', a_strErr)

    a_iRet = 0

    try:
        # 対象メッシュNoファイルを開く。
        a_sr = open(com.g_TargetMeshFile, 'r', encoding='shift_jis')
        # メッシュ数をカウントする。
        a_textline = a_sr.readline().rstrip('\r\n')
        while a_textline:
            a_iRet += 1
            a_textline = a_sr.readline().rstrip('\r\n')
        a_sr.close()
        # 対象メッシュNoファイルを開く。
        a_sr = open(com.g_TargetMeshFile, 'r', encoding='shift_jis')
        # メッシュファイルを開く。
        a_sw = open(com.g_OutPath + "\\" + com.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
        # メッシュ数を書込
        a_sw.write(str(a_iRet) + '\n')
        # メッシュ番号を取得する。
        a_textline = a_sr.readline().rstrip('\r\n')
        while a_textline:
            #print(a_textline)
            if (a_textline != ''):
                # メッシュ番号を書き込み
                a_split = a_textline.split(',')
                if com.g_TargetRainMesh == 1:
                    # 1kmメッシュ
                    a_sw.write(a_split[0] + "," + a_split[1] + '\n')
                    #h_meshList.append(a_split[0] + "," + a_split[1])
                    h_meshList.append(a_split[1])
                else:
                    # 5kmメッシュ
                    a_sw.write(a_split[0] + '\n')
                    h_meshList.append(a_split[0])
            a_textline = a_sr.readline().rstrip('\r\n')
        a_sw.close()
        a_sr.close()
    except Exception as exp:
        com.Outputlog(com.g_LOGMODE_ERROR, type(exp), a_strErr)

    #com.Outputlog(com.g_LOGMODE_INFORMATION, 'a_iRet', str(a_iRet))
    #com.Outputlog(com.g_LOGMODE_INFORMATION, '_getMeshSumFromFile', 'end')

    return a_iRet

def _makeAlarmAnnounce():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeAlarmAnnounce(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeAllRainfallData():
    global com
    global g_meshList

    # RBFNデータ入力

    for a_year in range(com.g_TargetStartYear, com.g_TargetEndYear + 1):
        print('***a_year=' + str(a_year))

        prv_RainfallFileName = com.g_OutPath + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
        prv_SoilRainFileName = com.g_OutPath + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId

        # 予測的中率
        prv_RainfallFileName1 = com.g_OutPathReal + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
        prv_SoilRainFileName1 = com.g_OutPathReal + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId

        prv_TemperatureFileName = com.g_OutPath + "\\" + com.g_TemperatureFileSId + str(a_year) + com.g_TemperatureFileEId
        com.g_textSum_TemperatureFile = com.Store_DataFile(prv_TemperatureFileName, com.g_textline_TemperatureFile)

        #print(prv_RainfallFileName)
        #com.Store_RainfallFile(prv_RainfallFileName)
        com.g_textSum_RainfallFile = com.Store_DataFile(prv_RainfallFileName, com.g_textline_RainfallFile)
        #com.Store_SoilRainFile(prv_SoilRainFileName)
        com.g_textSum_SoilRainFile = com.Store_DataFile(prv_SoilRainFileName, com.g_textline_SoilRainFile)
        if com.g_RainKind != 0:
            #com.Store_RainfallFile1(prv_RainfallFileName1)
            com.g_textSum_RainfallFile1 = com.Store_DataFile(prv_RainfallFileName1, com.g_textline_RainfallFile1)
            #com.Store_SoilRainFile1(prv_SoilRainFileName1)
            com.g_textSum_SoilRainFile1 = com.Store_DataFile(prv_SoilRainFileName1, com.g_textline_SoilRainFile1)

        a_meshSum = len(g_meshList)
        a_sum = 0
        while (a_sum < a_meshSum):
            a_cnt_max = (a_sum + 5)
            if (a_cnt_max > a_meshSum):
                a_cnt_max = a_meshSum

            print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
            a_procs = []
            a_proc_num = 0
            for a_cnt in range(a_sum, a_cnt_max):
                a_proc_num += 1
                #print('a_cnt=' + str(a_cnt))
                a_split = g_meshList[a_cnt].split(',')
                a_meshNo = ''
                if (com.g_TargetRainMesh == 1):
                    # 対象Surfaceが1km
                    a_meshNo = a_split[1]
                else:
                    # 対象Surfaceが5km
                    a_meshNo = a_split[0]
                print('a_meshNo=' + a_meshNo)
                a_proc = Process(target=clsRainfall.MakeAllRainfallDataByMesh,
                                 args=(
                                     a_proc_num,
                                     com.g_strIni,
                                     com.g_textline_DisasterFile,
                                     com.g_textline_CautionAnnounceFile,
                                     com.g_textline_TemperatureFile,
                                     com.g_textline_RainfallFile,
                                     com.g_textline_SoilRainFile,
                                     com.g_textline_RainfallFile1,
                                     com.g_textline_SoilRainFile1,
                                     a_year,
                                     a_cnt,
                                     g_meshList
                                 ))
                a_procs.append(a_proc)

            for a_proc in a_procs:
                a_proc.start()
            for a_proc in a_procs:
                a_proc.join()
            print('All process is ended.')

            a_sum = a_cnt_max

def _makeCautionAnnounceFrequencyOverOccurRainFallNum():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeCautionAnnounceFrequencyOverOccurRainFallNum(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeCautionAnnounceRateOccurNum(h_meshList):
    a_proc = clsFigure.MakeCautionAnnounceRateOccurNum(
        0,
        com.g_strIni,
        h_meshList,
        0,
        -1
    )

def _makeCautionAnnounceRateOccurRainFallNum():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeCautionAnnounceRateOccurRainFallNum(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeDisasterSupplement():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeDisasterSupplement(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeDisasterSupplement9_1():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeDisasterSupplement9_1(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeDisasterSupplement9_2():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeDisasterSupplement9_2(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeForecastPredictive():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeForecastPredictive(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeNIGeDaS():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeNIGeDaS(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        0,
        -1
    )

def _makeNIGeDaS_NonOccurCalc():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeNIGeDaS_NonOccurCalc(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        0,
        -1
    )

def _makeOverRainfall():
    global com
    global g_meshList

    a_meshSum = len(g_meshList)
    a_sum = 0
    while (a_sum < a_meshSum):
        a_cnt_max = (a_sum + 5)
        if (a_cnt_max > a_meshSum):
            a_cnt_max = a_meshSum

        print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
        a_procs = []
        a_proc_num = 0
        for a_cnt in range(a_sum, a_cnt_max):
            a_proc_num += 1
            #print('a_cnt=' + str(a_cnt))
            a_split = g_meshList[a_cnt].split(',')
            a_meshNo = ''
            if (com.g_TargetRainMesh == 1):
                # 対象Surfaceが1km
                a_meshNo = a_split[1]
            else:
                # 対象Surfaceが5km
                a_meshNo = a_split[0]
            print('a_meshNo=' + a_meshNo)
            a_proc = Process(target=clsFigure.MakeOverRainfallByMesh,
                             args=(
                                 a_proc_num,
                                 com.g_strIni,
                                 com.g_textline_DisasterFile,
                                 com.g_textline_CautionAnnounceFile,
                                 a_meshNo,
                                 0,
                                 0,
                                 -1
                             ))
            a_procs.append(a_proc)

        for a_proc in a_procs:
            a_proc.start()
        for a_proc in a_procs:
            a_proc.join()
        print('All process is ended.')

        a_sum = a_cnt_max

def _makeOverRainfall2():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeOverRainfall2(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        0,
        -1
    )

def _makeOverRainfall3_1():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeOverRainfall3_1(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        0,
        -1
    )

def _makeOverRainfall3_2():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeOverRainfall3_2(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        0,
        -1
    )

def _makeOverRainfall8():
    global com
    global g_meshList2

    # 予測雨量の算出
    a_proc = clsFigure.MakeOverRainfall8(
        0,
        com.g_strIni,
        1,
        g_meshList2,
        0,
        0,
        -1
    )

    # 実況雨量の算出
    a_proc = clsFigure.MakeOverRainfall8(
        0,
        com.g_strIni,
        0,
        g_meshList2,
        0,
        0,
        -1
    )

def _makeOverRainfallMix():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeOverRainfallMix(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeOverRainfallMix2():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeOverRainfallMix2(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeOverRainfallMix3_1():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeOverRainfallMix3_1(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeOverRainfallMix3_2():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeOverRainfallMix3_2(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeOverRainfallMix8():
    global com
    global g_meshList2

    # 予測雨量の算出
    a_proc = clsFigure.MakeOverRainfallMix8(
        0,
        com.g_strIni,
        1,
        g_meshList2,
        0,
        0,
        -1
    )

    # 実況雨量の算出
    a_proc = clsFigure.MakeOverRainfallMix8(
        0,
        com.g_strIni,
        0,
        g_meshList2,
        0,
        0,
        -1
    )

def _makeWiff():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeWhiff(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeWiff_New():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeWhiff_New(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeWhiffFrequency():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeWhiffFrequency(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeWhiffFrequency_New():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeWhiffFrequency_New(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

def _makeWhiffTime():
    global com
    global g_meshList2

    a_proc = clsFigure.MakeWhiffTime(
        0,
        com.g_strIni,
        g_meshList2,
        0,
        -1
    )

if __name__ == "__main__":
    global g_meshSum
    global g_meshList
    global g_meshList2

    ########################################################################
    com.GetEnvData('C:\\Users\\hal\\Documents\\CTI\\東京\\RBFN修正ツール\\2015年度\\program-source\\bin\\rbfnmdf.ini')
    #com.Store_DisasterFile()
    com.g_textSum_DisasterFile = com.Store_DataFile(com.g_DisasterFileName, com.g_textline_DisasterFile)
    #com.Store_CautionAnnounceFile()
    com.g_textSum_CautionAnnounceFile = com.Store_DataFile(com.g_CautionAnnounceFileName, com.g_textline_CautionAnnounceFile)
    # 集計
    # 解析雨量のCSVファイルからメッシュ数を取得する。
    g_meshList = []
    g_meshList2 = []
    if com.g_TargetMeshFile != "":
        g_meshSum = _getMeshSumFromFile(com.g_TargetStartYear, prv_RainfallFileName, g_meshList)
        g_meshSum = _getMeshSumFromFile2(com.g_TargetStartYear, prv_RainfallFileName, g_meshList2)
    else:
        g_meshSum = _getMeshSum(com.g_TargetStartYear, prv_RainfallFileName, g_meshList)
        g_meshSum = _getMeshSum(com.g_TargetStartYear, prv_RainfallFileName, g_meshList2)

    print(g_meshList)
    print(g_meshList2)
    ########################################################################

    #_makeAllRainfallData()


    # 全降雨の超過数
    # 非発生降雨の超過数
    # 発生降雨の超過数
    #_makeOverRainfall()
    #_makeOverRainfallMix()

    #災害捕捉率
    #_makeDisasterSupplement()

    # 空振り率
    #_makeWiff()
    # 空振り率2
    #_makeWiff_New()
    # 空振り頻度
    #_makeWhiffFrequency()
    # 空振り頻度2
    #_makeWhiffFrequency_New()
    # 空振り時間
    #_makeWhiffTime()

    # 警報発表頻度
    #_makeAlarmAnnounce()

    # 9)実質災害捕捉率
    # 災害捕捉率【降雨数】
    #_makeDisasterSupplement9_1()
    # 災害捕捉率【件数】
    #_makeDisasterSupplement9_2()

    # ④実質災害捕捉率
    # 年毎メッシュ単位の算出結果
    #_makeOverRainfall2()
    # 警戒発表中災害発生件数
    # 警戒発表中災害発生降雨数
    #_makeOverRainfallMix2()

    # 土砂災害警戒情報の災害捕捉率（降雨数）
    #_makeCautionAnnounceRateOccurRainFallNum()
    # 土砂災害警戒情報の災害捕捉率（件数）
    #_makeCautionAnnounceRateOccurNum()

    # ②土砂災害警戒情報のリードタイム
    #_makeOverRainfall3_1()
    #_makeOverRainfallMix3_1()

    # ③土砂災害警戒情報の発表頻度
    #_makeCautionAnnounceFrequencyOverOccurRainFallNum()

    # ⑥RBFN越のリードタイム
    #_makeOverRainfall3_2()
    #_makeOverRainfallMix3_2()

    # ⑧予測適中率
    if (com.g_RainKind != 0):
        _makeOverRainfall8()
        _makeOverRainfallMix8()
        _makeForecastPredictive()

    # ⑨NIGeDaS、NIGeDaSⅡ
    #_makeNIGeDaS()
    #makeNIGeDaS_NonOccurCalc()

