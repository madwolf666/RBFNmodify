import sys
import configparser
import  csv
from datetime import datetime

g_LOG_FILENAME = "rbfnmdf"
g_LOGMODE_ERROR = 1             # エラー(エラー種別)
g_LOGMODE_DISCLAIMER  = 2       # 警告(エラー種別)
g_LOGMODE_WARNING = 3           # ワーニング(エラー種別)
g_LOGMODE_INFORMATION = 4       # 情報(エラー種別)
g_LOGMODE_TRACE1 = 5            # トレース(エラー種別)
g_LOGMODE_TRACE2 = 6            # トレース(エラー種別)
g_LOG_SUCCESSFUL = "successful."

g_MeshSymbol =  "メッシュ番号"
g_AllRainfallSymbol = "全解析雨量・土壌雨量指数"                                            #"ARF"    '全降雨量
g_FindChainOccurRainfallSymbol = "一連の発生降雨の検出結果"                                 #"FCOR" '一連の降雨抽出結果
g_ChainOccurRainfallSymbol = "一連の発生降雨の抽出結果"                                     #"COR" '一連の降雨
g_FindOccurRainfallSymbol = "災害発生降雨の検出結果"                                        #'"FORF"  '発生降雨抽出結果
g_OccurRainfallSymbol = "災害発生降雨の抽出結果"                                            #"ORF"  '災害発生降雨
g_ChainOnlyOccurRainfallSymbol = "一連の発生降雨から災害発生降雨を除外した結果"           #"COO" '一連の降雨から災害発生降雨を取り除いたもの
g_NonOccurRainfallSymbol = "RBFN用非発生降雨の抽出結果"                                    #"NORF"  'RBFN非発生降雨
g_OverRainfallNumByMeshSymbol = "年毎メッシュ単位の超過数算出結果"                         #"ORBM"   'メッシュ単位の超過数
g_OverAllRainFallNumSymbol = "全超過数の算出結果"                                           #"OARN"  '全降雨超過数
g_OverNonOccurRainFallNumSymbol = "非発生降雨超過数の算出結果"                             #"ONOR"  '非発生降雨超過数
g_OverOccurRainFallNumSymbol = "発生降雨超過数の算出結果"                                  #"ORNF"  '発生降雨超過数
g_WhiffTimeMixSymbol = "空振り時間超過数の算出結果"                                        #"WFTM"  '空振り時間→2006.03.22
g_DisasterSupplementSymbol = "災害捕捉率の算出結果"                                        #"DSP"    '災害捕捉率
g_WhiffSymbol = "空振り率の算出結果"                                                       #"WHF"  '空振り率
g_WhiffFrequencySymbol = "空振り頻度の算出結果"                                            #"WFR"  '空振り頻度→2006.03.22
g_WhiffTimeSymbol = "空振り時間の算出結果"                                                 #"WFT"  '空振り時間→2006.03.22
g_AlarmAnnounceSymbol = "警報頻度の算出結果"                                               #"ALA"  '警報の頻度
g_ContourOriginSymbol = "等高線オリジナル画像"                                             #"CTO"  '等高線オリジナル
g_ContourReviseSymbol = "等高線補正画像"                                                   #"CTR"  '等高線補正
g_ContourSnakeSymbol = "スネーク曲線画像"                                                  #"CTS"  'スネーク曲線
g_ContourReviseSoilMinSymbol = "等高線補正画像(土壌雨量指数下限値)"                      #"CTR"  '等高線補正
g_ContourSnakeSoilMinSymbol = "スネーク曲線画像(土壌雨量指数下限値)"                     #"CTM"  '土壌雨量指数下限値
g_StatisticsByMeshSoilMinSymbol = "メッシュ単位の再集計結果(土壌雨量指数下限値)"        #"ORBM"   'メッシュ単位の超過数
g_OverRainfallNumByMeshSoilMinSymbol = "年毎メッシュ単位の超過数算出結果(土壌雨量指数下限値)"    #"ORBM"   'メッシュ単位の超過数
g_OverAllRainFallNumSoilMinSymbol = "全超過数の算出結果(土壌雨量指数下限値)"                      #"OARN"  '全降雨超過数
g_OverNonOccurRainFallNumSoilMinSymbol = "非発生降雨超過数の算出結果(土壌雨量指数下限値)"        #"ONOR"  '非発生降雨超過数
g_OverOccurRainFallNumSoilMinSymbol = "発生降雨超過数の算出結果(土壌雨量指数下限値)"             #""ORNF"  '発生降雨超過数
g_WhiffTimeMixSoilMinSymbol = "空振り時間超過数の算出結果(土壌雨量指数下限値)"                   #"WFTM"  '空振り時間→2006.03.22
g_DisasterSupplementSoilMinSymbol = "災害捕捉率の算出結果(土壌雨量指数下限値)"                   #"DSP"    '災害捕捉率
g_WhiffSoilMinSymbol = "空振り率の算出結果(土壌雨量指数下限値)"                                  #"WHF"  '空振り率
g_WhiffFrequencySoilMinSymbol = "空振り頻度の算出結果(土壌雨量指数下限値)"                       #"WFR"  '空振り頻度→2006.03.22
g_WhiffTimeSoilMinSymbol = "空振り時間の算出結果(土壌雨量指数下限値)"                            #"WFT"  '空振り時間→2006.03.22
g_AlarmAnnounceSoilMinSymbol = "警報頻度の算出結果(土壌雨量指数下限値)"                          #"ALA"  '警報の頻度
g_BlockStatisticsSymbol = "ブロック集計結果"                                                       #"BSTC"  'ブロック毎集計
g_BlockOriginalSymbol = "ブロックオリジナル画像"                                                   #"BORG"  'オリジナルブロック図
g_BlockOverAllRainFallNumSymbol = "ブロック全降雨超過数画像"                                      #"BOARN"  '全降雨超過数
g_BlockOverNonOccurRainFallNumSymbol = "ブロック非発生降雨超過数画像"                             #"BONOR"  '非発生降雨超過数
g_BlockOverOccurRainFallNumSymbol = "ブロック発生降雨超過数画像"                                  #"BORNF"  '発生降雨超過数
g_BlockDisasterSupplementSymbol = "ブロック災害捕捉率画像"                                        #"BDSP"    '災害捕捉率
g_BlockWhiffSymbol = "ブロック空振り率画像"                                                       #"BWHF"  '空振り率
g_BlockAlarmAnnounceSymbol = "ブロック警報頻度画像"                                               #"BALA"  '警報の頻度
g_BlockWhiffFrequencySymbol = "ブロック空振り頻度画像"                                            #"BWFR"  '空振り頻度
g_BlockWhiffTimeSymbol = "ブロック空振り時間画像"                                                 #"BWFT"  '空振り時間

g_OverRainfallNumByMeshSoilMinSymbol2 = "年毎メッシュ単位の算出結果2(土壌雨量指数下限値)"   #メッシュ単位の数[2012.07.02]
g_OverRainfallNumByMeshSymbol2 = "年毎メッシュ単位の算出結果2"   #メッシュ単位の数[2012.07.02]
g_BlockStatisticsSymbol2 = "ブロック集計結果2"   #ブロック毎集計[2012.07.02]①土砂災害警戒情報の災害捕捉率、③土砂災害警戒情報の発表頻度
g_BlockStatisticsSymbol3_1 = "ブロック集計結果3_1"   #ブロック毎集計[2012.07.03]②土砂災害警戒情報のリードタイム
g_BlockStatisticsSymbol3_2 = "ブロック集計結果3_2"   #ブロック毎集計[2012.07.03]⑥実況雨量・予測雨量によるリードタイム

#9)実質災害捕捉率・④実質災害捕捉率【降雨数】
g_OverOccurRainFallNum9_1SoilMinSymbol = "発生降雨超過数【災害捕捉率】の算出結果(土壌雨量指数下限値)"
g_OverOccurRainFallNum9_1Symbol = "発生降雨超過数【災害捕捉率】の算出結果"
g_DisasterSupplement9_1SoilMinSymbol = "災害捕捉率【降雨数】の算出結果(土壌雨量指数下限値)" #"DSP"    '災害捕捉率
g_DisasterSupplement9_1Symbol = "災害捕捉率【降雨数】の算出結果"   #"DSP"    '災害捕捉率

#④実質災害捕捉率・④実質災害捕捉率【件数】
g_OverOccurRainFallNum9_2SoilMinSymbol = "災害発生件数【災害捕捉率】の算出結果(土壌雨量指数下限値)"
g_OverOccurRainFallNum9_2Symbol = "災害発生件数【災害捕捉率】の算出結果"
g_DisasterSupplement9_2SoilMinSymbol = "災害捕捉率【件数】の算出結果(土壌雨量指数下限値)"  #"DSP"    '災害捕捉率
g_DisasterSupplement9_2Symbol = "災害捕捉率【件数】の算出結果"    #"DSP"    '災害捕捉率

#①土砂災害警戒情報の災害捕捉率
g_FindCautionAnnounceOccurRainFallSymbol = "警戒発表中災害発生降雨数の検出結果"
g_CautionAnnounceOccurRainFallNumMixSoilMinSymbol = "警戒発表中災害発生降雨数の算出結果(土壌雨量指数下限値)"
g_CautionAnnounceOccurRainFallNumMixSymbol = "警戒発表中災害発生降雨数の算出結果"
g_CautionAnnounceOccurNumMixSoilMinSymbol = "警戒発表中災害発生件数の算出結果(土壌雨量指数下限値)"
g_CautionAnnounceOccurNumMixSymbol = "警戒発表中災害発生件数の算出結果"
g_CautionAnnounceRateOverOccurRainFallNumMixSoilMinSymbol = "警戒情報災害捕捉率【降雨数】の算出結果(土壌雨量指数下限値)"
g_CautionAnnounceRateOverOccurRainFallNumMixSymbol = "警戒情報災害捕捉率【降雨数】の算出結果"
g_CautionAnnounceRateOccurNumMixSoilMinSymbol = "警戒情報災害捕捉率【件数】の算出結果(土壌雨量指数下限値)"
g_CautionAnnounceRateOccurNumMixSymbol = "警戒情報災害捕捉率【件数】の算出結果"

#②土砂災害警戒情報のリードタイム
g_CalcCautionAnnounceReadTimeSoilMinSymbol = "警戒情報リードタイムの算出結果(土壌雨量指数下限値)"
g_CalcCautionAnnounceReadTimeSymbol = "警戒情報リードタイムの算出結果"
g_CalcCautionAnnounceReadTimeByMeshSoilMinSymbol = "年毎警戒情報リードタイムの算出結果(土壌雨量指数下限値)"   #メッシュ単位の数[2012.07.02]
g_CalcCautionAnnounceReadTimeByMeshSymbol = "年毎警戒情報リードタイムの算出結果"   #メッシュ単位の数[2012.07.02]

#③土砂災害警戒情報の発表頻度
g_CautionAnnounceFrequencyOverOccurRainFallNumMixSoilMinSymbol = "警戒情報発表頻度の算出結果(土壌雨量指数下限値)"
g_CautionAnnounceFrequencyOverOccurRainFallNumMixSymbol = "警戒情報発表頻度の算出結果"

#⑥実況・予測雨量のリードタイム
g_CalcRBFNReadTimeSoilMinSymbol = "RBFN越リードタイムの算出結果(土壌雨量指数下限値)"
g_CalcRBFNReadTimeSymbol = "RBFN越リードタイムの算出結果"
g_CalcRBFNReadTimeByMeshSoilMinSymbol2 = "年毎RBFN越リードタイムの算出結果(土壌雨量指数下限値)"    #メッシュ単位の数[2012.07.02]
g_CalcRBFNReadTimeByMeshSymbol2 = "年毎RBFN越リードタイムの算出結果"   #メッシュ単位の数[2012.07.02]

#[2012.07.26]⑧予測適中率
g_AllRainfall0Symbol = "全解析雨量・土壌雨量指数（実況雨量）" #"ARF"    '全降雨量
g_FindChainOccurRainfall0Symbol = "一連の発生降雨の検出結果（実況雨量）"  #"FCOR" '一連の降雨抽出結果
g_ChainOccurRainfall0Symbol = "一連の発生降雨の抽出結果（実況雨量）"  #"COR" '一連の降雨
g_FindOccurRainfall0Symbol = "災害発生降雨の検出結果（実況雨量）"    #"FORF"  '発生降雨抽出結果
g_OccurRainfall0Symbol = "災害発生降雨の抽出結果（実況雨量）"    #"ORF"  '災害発生降雨
g_CalcForecastTime0SoilMinSymbol = "予測適中率（実況雨量）の算出結果(土壌雨量指数下限値)"
g_CalcForecastTime0Symbol = "予測適中率（実況雨量）の算出結果"
g_CalcForecastTime0ByMeshSoilMinSymbol = "年毎予測適中率（実況雨量）の算出結果(土壌雨量指数下限値)"    #メッシュ単位の数[2012.07.02]
g_CalcForecastTime0ByMeshSymbol = "年毎予測適中率（実況雨量）の算出結果"   #メッシュ単位の数[2012.07.02]
g_CalcForecastTime1SoilMinSymbol = "予測適中率（予測雨量）の算出結果(土壌雨量指数下限値)"
g_CalcForecastTime1Symbol = "予測適中率（予測雨量）の算出結果"
g_CalcForecastTime1ByMeshSoilMinSymbol = "年毎予測適中率（予測雨量）の算出結果(土壌雨量指数下限値)"    #メッシュ単位の数[2012.07.02]
g_CalcForecastTime1ByMeshSymbol = "年毎予測適中率（予測雨量）の算出結果"   #メッシュ単位の数[2012.07.02]
g_CalcForecastPredictiveSoilMinSymbol = "予測適中率の算出結果(土壌雨量指数下限値)"
g_CalcForecastPredictiveSymbol = "予測適中率の算出結果"

#⑨NIGeDaS、NIGeDaSⅡ
g_NIGeDaSSoilMinSymbol = "NIGeDaS(土壌雨量指数下限値)"
g_NIGeDaSSymbol = "NIGeDaS"
g_NIGeDaS2SoilMinSymbol = "NIGeDaSⅡ(土壌雨量指数下限値)"
g_NIGeDaS2Symbol = "NIGeDaSⅡ"

#RBFN近似値
g_OccurRainfallRBFNNear = "災害発生降雨のRBFN近似値"  #"ORF"  '災害発生降雨
g_OccurRainfall0RBFNNear = "災害発生降雨のRBFN近似値（実況雨量）"   #"ORF"  '災害発生降雨

g_ChainOccurRainfallSymbolByBlock = "一連の発生降雨【ブロック】"
g_ChainOccurRainfall2SymbolByBlock = "一連の発生降雨2【ブロック】"
g_OccurRainfallSymbolByBlock = "災害発生降雨【ブロック】"
g_OccurRainfall2SymbolByBlock = "災害発生降雨2【ブロック】"
g_ChainOnlyOccurRainfallSymbolByBlock = "一連の発生降雨から災害発生降雨を除外【ブロック】"
g_WhiffTimeSymbolByBlock = "空振り時間【ブロック】"
g_OverOccurRainFallNum9_1TimeSymbolByBlock = "発生降雨超過数【災害捕捉率】【ブロック】"
g_OverOccurRainFallNum9_2TimeSymbolByBlock = "災害発生件数【災害捕捉率】【ブロック】"

g_CalcCautionAnnounceReadTimeSymbolByBlock = "警戒情報リードタイム【ブロック】"
g_CalcRBFNReadTimeSymbolByBlock = "RBFN越リードタイム【ブロック】"

g_CalcForecastPredictiveSymbolByBlock1 = "予測適中率（予測）【ブロック】"
g_CalcForecastPredictiveSymbolByBlock2 = "予測適中率（実況）【ブロック】"

#実質災害捕捉率【降雨数】による非発生降雨数
g_OverNonOccurRainFall9_1NumSoilMinSymbol = "非発生降雨超過数【災害捕捉率】の算出結果(土壌雨量指数下限値)"   #"ONOR"  '非発生降雨超過数
g_OverNonOccurRainFall9_1NumSymbol = "非発生降雨超過数【災害捕捉率】の算出結果" #"ONOR"  '非発生降雨超過数
g_WhiffNewSoilMinSymbol = "空振り率2の算出結果(土壌雨量指数下限値)"   #"WHF"  '空振り率
g_WhiffNewSymbol = "空振り率2の算出結果" #"WFT"  '空振り時間→2006.03.22
g_WhiffFrequencyNewSoilMinSymbol = "空振り頻度2の算出結果(土壌雨量指数下限値)" #"WFR"  '空振り頻度→2006.03.22
g_WhiffFrequencyNewSymbol = "空振り頻度2の算出結果"   #"WFR"  '空振り頻度→2006.03.22

g_textSum_AllRainfall = 0
g_textline_AllRainfall = []
g_textSum_CautionAnnounceFile = 0
g_textline_CautionAnnounceFile = []
g_textSum_DisasterFile = 0
g_textline_DisasterFile = []
g_textSum_FindOccurRainfall = 0
g_textline_FindOccurRainfall = []
g_textSum_RainfallFile = 0
g_textline_RainfallFile = []
g_textSum_RainfallFile1 = 0
g_textline_RainfallFile1 = []
g_textSum_SoilRainFile = 0
g_textline_SoilRainFile = []
g_textSum_SoilRainFile1 = 0
g_textline_SoilRainFile1 = []

g_strIni = ""                   # INIファイル名
g_target_year = 0               # 対象年

g_LogPath = "."                 # ログパス("TEMPパス")
g_LogEffectiveDays = 7          # ログ有効期間("7")
g_LogLevel = 0                  # ログレベル("0")
g_SystemTitle = ""              # システムのタイトル名
g_TargetMeshFile = ""           # 対象メッシュNoファイル
g_OccurSepTime = 24             # 発生降雨の前後時間範囲
g_xUnit = 50                    # X軸の単位線
g_yUnit = 10                    # Y軸の単位線
g_UnrealAlpha = 1               # Unrealの係数
g_ImageFileWidth = 320          # ファイル保存時の画像サイズ（幅）→pixel値
g_ImageFileHeight = 160         # ファイル保存時の画像サイズ（高さ）→pixel値
g_DrawRainfallMax = 0           # 60分間積算雨量の描画MAXサイズ→mm/hr
g_DrawSoilMax = 0               # 土壌雨量指数の描画MAXサイズ→mm
g_TargetPath = ""               # 気象庁元データパス
g_TargetRainMesh = 5            # 対象雨量メッシュ
g_TargetSurface = 5             # 既往CL対象メッシュ選択サポート
g_TimeKind = 2                  # 30分データ取込
g_TargetStartYear = 0           # 開始年
g_TargetEndYear = 0             # 終了年
g_OutPath = ""                  # 結果出力パス
g_RBFNOutPath = ""              # RBFN結果出力パス
g_RainfallFileSId = ""          # 解析雨量→2006.03.20
g_RainfallFileEId = ""          # 解析雨量→2006.03.20
g_SoilrainFileSId = ""          # 土壌雨量指数→2006.03.20
g_SoilrainFileEId = ""          # 土壌雨量指数→2006.03.20
g_DisasterFileName = ""         # 災害発生情報ファイル名
g_TemperatureKind = 0           # 気温の取り込み→種別（0：なし、1：平均気温、2：最高気温）
g_TemperatureMin = 0            # 気温の取り込み→最小気温
g_TemperatureMax = 0            #気温の取り込み→最高気温
g_TemperatureFileSId = ""       # 気温ファイル
g_TemperatureFileEId = ""       # 気温ファイル
g_BlockBackgroundImage = ""     # ブロック図背景→2006.04.05
g_BlockExcelDefine = ""         # ブロック定義Excel→2006.04.05
g_BlockDrawDefine = ""          # ブロック描画定義ファイル→2006.04.05
g_CautionAnnounceFileName = ""  # 警戒発表情報ファイル[2012.06.28]①土砂災害警戒情報の災害捕捉率
g_RecalcLimitFileName = ""      #下限値・上限値再集計ファイル

g_RainKind = 0                  #実況雨量・予測雨量
g_ForecastTime = 0              #
g_OutPathReal = ""              #
g_PastKind = 0                  # 既往CLの取り込み
g_PastTargetStartYear = 0       #
g_PastTargetEndYear = 0         #
g_PastRBFNOutPath = ""          #
g_PastCLFileName = ""           #
g_NIGeDaS_NonOccurCalc =0       # NIGeDaS


def _getInifile(inifile, section, name):
    try:
        return inifile.get(section, name)
    except Exception as exp:
        return "error: could not read " + name

# INIファイルの読み込み
def GetEnvData():
    global g_strIni
    global g_target_year

    global g_LogPath
    global g_LogEffectiveDays
    global g_LogLevel
    global g_SystemTitle
    global g_TargetMeshFile
    global g_OccurSepTime
    global g_xUnit
    global g_yUnit
    global g_UnrealAlpha
    global g_ImageFileWidth
    global g_ImageFileHeight
    global g_DrawRainfallMax
    global g_DrawSoilMax
    global g_TargetPath
    global g_TargetRainMesh
    global g_TargetSurface
    global g_TimeKind
    global g_TargetStartYear
    global g_TargetEndYear
    global g_OutPath
    global g_RBFNOutPath
    global g_RainfallFileSId
    global g_RainfallFileEId
    global g_SoilrainFileSId
    global g_SoilrainFileEId
    global g_DisasterFileName
    global g_TemperatureKind
    global g_TemperatureMin
    global g_TemperatureMax
    global g_TemperatureFileSId
    global g_TemperatureFileEId
    global g_BlockBackgroundImage
    global g_BlockExcelDefine
    global g_BlockDrawDefine
    global g_CautionAnnounceFileName
    global g_RecalcLimitFileName
    global g_RainKind
    global g_ForecastTime
    global g_OutPathReal
    global g_PastKind
    global g_PastTargetStartYear
    global g_PastTargetEndYear
    global g_PastRBFNOutPath
    global g_PastCLFileName
    global g_NIGeDaS_NonOccurCalc

    # 引数を取得
    args = sys.argv
    #g_strIni = args[1] #INIファイル名
    #g_target_year = args[2] #対象年
    g_strIni = "C:\\Users\\hal\\Documents\\CTI\\東京\\RBFN修正ツール\\2015年度\\program-source\\bin\\rbfnmdf.ini"
    #print("[g_strIni]" + g_strIni)
    g_target_year = 1999
    #print("[g_target_year]" + str(g_target_year))
    # INIファイル内容を読み込む
    a_inifile = configparser.SafeConfigParser()
    a_inifile.read(g_strIni)
    #for a_section in a_inifile.sections():
    #    print('===' + a_section + '===')

    g_SystemTitle = _getInifile(a_inifile, 'All', 'SystemTitle')
    #print('[g_SystemTitle]' + g_SystemTitle)
    g_TargetMeshFile = _getInifile(a_inifile, 'All', 'TargetMeshFile')
    #print('[g_TargetMeshFile]' + g_TargetMeshFile)
    #print('')

    g_TargetPath = _getInifile(a_inifile, 'Rainfall', 'TargetPath')
    #print('[g_TargetPath]' + g_TargetPath)
    g_TargetStartYear = int(_getInifile(a_inifile, 'Rainfall', 'TargetStartYear'))
    #print('[g_TargetStartYear]' + str(g_TargetStartYear))
    g_TargetEndYear = int(_getInifile(a_inifile, 'Rainfall', 'TargetEndYear'))
    #print('[g_TargetEndYear]' + str(g_TargetEndYear))
    g_OutPath = _getInifile(a_inifile, 'Rainfall', 'OutPath')
    #print('[g_OutPath]' + g_OutPath)
    g_RBFNOutPath = _getInifile(a_inifile, 'Rainfall', 'RBFNOutPath')
    #print('[g_RBFNOutPath]' + g_RBFNOutPath)
    g_OccurSepTime = int(_getInifile(a_inifile, 'Rainfall', 'OccurSepTime'))
    #print('[g_OccurSepTime]' + str(g_OccurSepTime))
    g_RainfallFileSId = _getInifile(a_inifile, 'Rainfall', 'RainfallFileSId')
    #print('[g_RainfallFileSId]' + g_RainfallFileSId)
    g_RainfallFileEId = _getInifile(a_inifile, 'Rainfall', 'RainfallFileEId')
    #print('[g_RainfallFileEId]' + g_RainfallFileEId)
    g_SoilrainFileSId = _getInifile(a_inifile, 'Rainfall', 'SoilrainFileSId')
    #print('[g_SoilrainFileSId]' + g_SoilrainFileSId)
    g_SoilrainFileEId = _getInifile(a_inifile, 'Rainfall', 'SoilrainFileEId')
    #print('[g_SoilrainFileEId]' + g_SoilrainFileEId)
    g_DisasterFileName = _getInifile(a_inifile, 'Rainfall', 'DisasterFileName')
    #print('[g_DisasterFileName]' + g_DisasterFileName)
    g_TemperatureKind = int(_getInifile(a_inifile, 'Rainfall', 'TemperatureKind'))
    #print('[g_TemperatureKind]' + str(g_TemperatureKind))
    g_TemperatureMin = float(_getInifile(a_inifile, 'Rainfall', 'TemperatureMin'))
    #print('[g_TemperatureMin]' + str(g_TemperatureMin))
    g_TemperatureMax = float(_getInifile(a_inifile, 'Rainfall', 'TemperatureMax'))
    #print('[g_TemperatureMax]' + str(g_TemperatureMax))
    g_TemperatureFileSId = _getInifile(a_inifile, 'Rainfall', 'TemperatureFileSId')
    #print('[g_TemperatureFileSId]' + g_TemperatureFileSId)
    g_TemperatureFileEId = _getInifile(a_inifile, 'Rainfall', 'TemperatureFileEId')
    #print('[g_TemperatureFileEId]' + g_TemperatureFileEId)
    g_CautionAnnounceFileName = _getInifile(a_inifile, 'Rainfall', 'CautionAnnounceFileName')
    #print('[g_CautionAnnounceFileName]' + g_CautionAnnounceFileName)
    g_RainKind = int(_getInifile(a_inifile, 'Rainfall', 'RainKind'))
    #print('[g_RainKind]' + str(g_RainKind))
    g_ForecastTime = int(_getInifile(a_inifile, 'Rainfall', 'ForecastTime'))
    #print('[g_ForecastTime]' + str(g_ForecastTime))
    g_OutPathReal = _getInifile(a_inifile, 'Rainfall', 'OutPathReal')
    #print('[g_OutPathReal]' + g_OutPathReal)
    g_TargetRainMesh = int(_getInifile(a_inifile, 'Rainfall', 'TargetRainMesh'))
    #print('[g_TargetRainMesh]' + str(g_TargetRainMesh))
    g_TimeKind = int(_getInifile(a_inifile, 'Rainfall', 'TimeKind'))
    #print('[g_TimeKind]' + str(g_TimeKind))
    g_RecalcLimitFileName = _getInifile(a_inifile, 'Rainfall', 'RecalcLimitFileName')
    #print('[g_RecalcLimitFileName]' + g_RecalcLimitFileName)
    #print('')

    g_xUnit = float(_getInifile(a_inifile, 'RBFN', 'XUnit'))
    #print('[g_xUnit]' + str(g_xUnit))
    g_yUnit = float(_getInifile(a_inifile, 'RBFN', 'YUnit'))
    #print('[g_yUnit]' + str(g_yUnit))
    g_UnrealAlpha = float(_getInifile(a_inifile, 'RBFN', 'UnrealAlpha'))
    #print('[g_UnrealAlpha]' + str(g_UnrealAlpha))
    g_ImageFileWidth = float(_getInifile(a_inifile, 'RBFN', 'ImageFileWidth'))
    #print('[g_ImageFileWidth]' + str(g_ImageFileWidth))
    g_ImageFileHeight = float(_getInifile(a_inifile, 'RBFN', 'ImageFileHeight'))
    #print('[g_ImageFileHeight]' + str(g_ImageFileHeight))
    g_DrawRainfallMax = float(_getInifile(a_inifile, 'RBFN', 'DrawRainfallMax'))
    #print('[g_DrawRainfallMax]' + str(g_DrawRainfallMax))
    g_DrawSoilMax = float(_getInifile(a_inifile, 'RBFN', 'DrawSoilMax'))
    #print('[g_DrawSoilMax]' + str(g_DrawSoilMax))
    g_PastKind= int(_getInifile(a_inifile, 'RBFN', 'PastKind'))
    #print('[g_PastKind]' + str(g_PastKind))
    g_PastTargetStartYear = int(_getInifile(a_inifile, 'RBFN', 'PastTargetStartYear'))
    #print('[g_PastTargetStartYear]' + str(g_PastTargetStartYear))
    g_PastTargetEndYear = int(_getInifile(a_inifile, 'RBFN', 'PastTargetEndYear'))
    #print('[g_PastTargetEndYear]' + str(g_PastTargetEndYear))
    g_PastRBFNOutPath = _getInifile(a_inifile, 'RBFN', 'PastRBFNOutPath')
    #print('[g_PastRBFNOutPath]' + g_PastRBFNOutPath)
    g_PastCLFileName = _getInifile(a_inifile, 'RBFN', 'PastCLFileName')
    #print('[g_PastCLFileName]' + g_PastCLFileName)
    g_TargetSurface = int(_getInifile(a_inifile, 'RBFN', 'TargetSurface'))
    #print('[g_TargetSurface]' + str(g_TargetSurface))
    g_NIGeDaS_NonOccurCalc = int(_getInifile(a_inifile, 'RBFN', 'NIGeDaS_NonOccurCalc'))
    #print('[g_NIGeDaS_NonOccurCalc]' + str(g_NIGeDaS_NonOccurCalc))
    #print('')

    g_BlockBackgroundImage = _getInifile(a_inifile, 'Block', 'BlockBackgroundImage')
    #print('[g_BlockBackgroundImage]' + g_BlockBackgroundImage)
    g_BlockExcelDefine = _getInifile(a_inifile, 'Block', 'BlockExcelDefine')
    #print('[g_BlockExcelDefine]' + g_BlockExcelDefine)
    g_BlockDrawDefine = _getInifile(a_inifile, 'Block', 'BlockDrawDefine')
    #print('[g_BlockDrawDefine]' + g_BlockDrawDefine)
    #print('')

    g_LogPath = _getInifile(a_inifile, 'LogInfo', 'LogPath')
    #print('[g_LogPath]' + g_LogPath)
    g_LogEffectiveDays = int(_getInifile(a_inifile, 'LogInfo', 'LogEffectiveDays'))
    #print('[g_LogEffectiveDays]' + str(g_LogEffectiveDays))
    g_LogLevel = int(_getInifile(a_inifile, 'LogInfo', 'LogLevel'))
    #print('[g_LogLevel]' + str(g_LogLevel))

def Outputlog(h_mode, h_Source, h_desc):
    global g_LOG_FILENAME
    global g_LOGMODE_ERROR
    global g_LOGMODE_DISCLAIMER
    global g_LOGMODE_WARNING
    global g_LOGMODE_INFORMATION
    global g_LOGMODE_TRACE1
    global g_LOGMODE_TRACE2
    global g_LOG_SUCCESSFUL

    a_strwork1 = ""
    a_exeMode = False
    # エラー種別により出力文字列を設定する。
    if h_mode == g_LOGMODE_ERROR:
        # エラー
        if g_LogLevel >= g_LOGMODE_ERROR :
            a_strwork1 = "[ERROR]"
            a_exeMode = True
    elif h_mode == g_LOGMODE_DISCLAIMER:
        # 警告
        if g_LogLevel >= g_LOGMODE_DISCLAIMER:
            a_strwork1 = "[DISCLAIMER]"
            a_exeMode = True
    elif h_mode == g_LOGMODE_WARNING:
        # ワーニング
        if g_LogLevel >= g_LOGMODE_WARNING:
            a_strwork1 = "[WARNING]"
            a_exeMode = True
    elif h_mode == g_LOGMODE_INFORMATION:
        # 情報
        if g_LogLevel >= g_LOGMODE_INFORMATION:
            a_strwork1 = "[INFORMATION]"
            a_exeMode = True
    elif h_mode == g_LOGMODE_TRACE1:
        # トレース
        if g_LogLevel >= g_LOGMODE_TRACE1:
            a_strwork1 = "[TRACE1]"
            a_exeMode = True
    elif h_mode == g_LOGMODE_TRACE2:
        # トレース
        if g_LogLevel >= g_LOGMODE_TRACE2:
            a_strwork1 = "[TRACE2]"
            a_exeMode = True

    if (a_exeMode == True):
        a_now = datetime.now()
        a_now1 = a_now.strftime("%Y%m%d")
        a_now2 = a_now.strftime("%Y/%m/%d %H:%M:%S.") + "%04d" % (a_now.microsecond // 1000)
        a_strwork2 = g_LogPath + "\\" + g_LOG_FILENAME + a_now1 + ".log"
        a_sw = open(a_strwork2, "a", encoding="shift_jis")
        a_sw.write(a_now2 + ',' + a_strwork1 + '(' + h_Source + '),' + h_desc + '\n')
        a_sw.close()

def Replace_TextLine(h_textline, h_srcChr, h_dstChr):
    for a_iw in range(0, len(h_textline)):
        h_textline[a_iw] = h_textline[a_iw].replace(h_srcChr, h_dstChr)

# 気温情報を取得する
# 返り値    : 気温情報
#             1カラム目：気温取り込み種別（0:なし、1：平均気温、2：最高気温）
#             2カラム目：範囲最小気温
#             3カラム目：範囲最大気温
#             4カラム目：計算結果の平均気温→これは、一連の降雨毎に算出する事になる。
#             5カラム目：計算結果の最高気温→これは、一連の降雨毎に算出する事になる。
def SetTemperatureInfo():
    global g_TemperatureKind
    global g_TemperatureMin
    global g_TemperatureMax

    a_sRet = ''
    a_sRet += ',' + str(g_TemperatureKind)
    a_sRet += ',' + str(g_TemperatureMin)
    a_sRet += ',' + str(g_TemperatureMax)

    return a_sRet

def Store_AllRainfall(h_fileName):
    global g_textSum_AllRainfall
    global g_textline_AllRainfall

    a_strErr = "filename=" + h_fileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_AllRainfall', a_strErr)

    # 全解析雨量・土壌雨量指数ファイルを開く

    try:
        g_textSum_AllRainfall = 0
        g_textline_AllRainfall = None
        a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
        g_textline_AllRainfall = [ v for v in a_csv_obj]
        g_textSum_AllRainfall = len(g_textline_AllRainfall)
        '''
        a_f = open(h_fileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
           g_textSum_AllRainfall +=1
           g_textline_AllRainfall.append(a_line.rstrip('\r\n'))
           a_line = a_f.readline()
        a_f.close()
        #print(g_textline_AllRainfall)
        '''
    except Exception as exp:
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

    #Outputlog(g_LOGMODE_INFORMATION, 'Store_AllRainfall', 'end')

def Store_CautionAnnounceFile():
    global g_CautionAnnounceFileName
    global g_textSum_CautionAnnounceFile
    global g_textline_CautionAnnounceFile

    a_strErr = "filename=" + g_CautionAnnounceFileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_CautionAnnounceFile', a_strErr)

    # 災害発生降雨の検出結果を退避（メッシュ単位）

    try:
        g_textSum_CautionAnnounceFile = 0
        g_textline_CautionAnnounceFile = []
        a_csv_obj = csv.reader(open(g_CautionAnnounceFileName, 'r', encoding='shift_jis'))
        g_textline_CautionAnnounceFile = [ v for v in a_csv_obj]
        g_textSum_CautionAnnounceFile = len(g_textline_CautionAnnounceFile)
        '''
        a_f = open(g_CautionAnnounceFileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
            g_textSum_CautionAnnounceFile +=1
            g_textline_CautionAnnounceFile.append(a_line.rstrip('\r\n'))
            a_line = a_f.readline()
        a_f.close()
        #print(g_textline_RainfallFile)
        '''
    except Exception as exp:
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

def Store_DisasterFile():
    global g_DisasterFileName
    global g_textSum_DisasterFile
    global g_textline_DisasterFile

    a_strErr = "filename=" + g_DisasterFileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_DisasterFile', a_strErr)

    # 災害発生降雨の検出結果を退避（メッシュ単位）

    try:
        g_textSum_DisasterFile = 0
        g_textline_DisasterFile = []
        a_csv_obj = csv.reader(open(g_DisasterFileName, 'r', encoding='shift_jis'))
        g_textline_DisasterFile = [ v for v in a_csv_obj]
        g_textSum_DisasterFile = len(g_textline_DisasterFile)
        '''
        a_f = open(g_DisasterFileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
            g_textSum_DisasterFile +=1
            g_textline_DisasterFile.append(a_line.rstrip('\r\n'))
            a_line = a_f.readline()
        a_f.close()
        #print(g_textline_RainfallFile)
        '''
    except Exception as exp:
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

def Store_FindOccurRainfall(h_fileName):
    global g_textSum_FindOccurRainfall
    global g_textline_FindOccurRainfall

    a_strErr = "filename=" + h_fileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_FindOccurRainfall', a_strErr)

    # 災害発生降雨の検出結果を退避（メッシュ単位）

    try:
        g_textSum_FindOccurRainfall = 0
        g_textline_FindOccurRainfall = []
        a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
        g_textline_FindOccurRainfall = [ v for v in a_csv_obj]
        g_textSum_FindOccurRainfall = len(g_textline_FindOccurRainfall)
        '''
        a_f = open(h_fileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
            g_textSum_FindOccurRainfall +=1
            g_textline_FindOccurRainfall.append(a_line.rstrip('\r\n'))
            a_line = a_f.readline()
        a_f.close()
        #print(g_textline_RainfallFile)
        '''
    except Exception as exp:
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

def Store_RainfallFile(h_fileName):
    global g_textSum_RainfallFile
    global g_textline_RainfallFile

    a_strErr = "filename=" + h_fileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_RainfallFile', a_strErr)

    # 災害発生降雨の検出結果を退避（メッシュ単位）

    try:
        g_textSum_RainfallFile = 0
        g_textline_RainfallFile = []
        a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
        g_textline_RainfallFile = [ v for v in a_csv_obj]
        g_textSum_RainfallFile = len(g_textline_RainfallFile)
        '''
        a_f = open(h_fileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
            g_textSum_RainfallFile +=1
            g_textline_RainfallFile.append(a_line.rstrip('\r\n'))
            a_line = a_f.readline()
        a_f.close()
        #print(g_textline_RainfallFile)
        '''
    except Exception as exp:
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

    #Outputlog(g_LOGMODE_INFORMATION, 'Store_RainfallFile', 'end')

def Store_RainfallFile1(h_fileName):
    global g_textSum_RainfallFile1
    global g_textline_RainfallFile1

    a_strErr = "filename=" + h_fileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_RainfallFile1', a_strErr)

    # 災害発生降雨の検出結果を退避（メッシュ単位）

    try:
        g_textSum_RainfallFile1 = 0
        g_textline_RainfallFile1 = []
        a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
        g_textline_RainfallFile1 = [ v for v in a_csv_obj]
        g_textSum_RainfallFile1 = len(g_textline_RainfallFile1)
        '''
        a_f = open(h_fileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
            g_textSum_RainfallFile1 += 1
            g_textline_RainfallFile1.append(a_line.rstrip('\r\n'))
            a_line = a_f.readline()
        a_f.close()
        #print(g_textline_RainfallFile1)
        '''
    except Exception as exp:
        a_strErr = "filename=" + h_fileName
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

    #Outputlog(g_LOGMODE_INFORMATION, 'Store_RainfallFile1', 'end')

def Store_SoilRainFile(h_fileName):
    global g_textSum_SoilRainFile
    global g_textline_SoilRainFile

    a_strErr = "filename=" + h_fileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_SoilRainFile', a_strErr)

    # 災害発生降雨の検出結果を退避（メッシュ単位）

    try:
        g_textSum_SoilRainFile = 0
        g_textline_SoilRainFile = []
        a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
        g_textline_SoilRainFile = [ v for v in a_csv_obj]
        g_textSum_SoilRainFile = len(g_textline_SoilRainFile)
        '''
        a_f = open(h_fileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
            g_textSum_SoilRainFile += 1
            g_textline_SoilRainFile.append(a_line.rstrip('\r\n'))
            a_line = a_f.readline()
        a_f.close()
        #print(g_textline_SoilRainFile)
        '''
    except Exception as exp:
        a_strErr = "filename=" + h_fileName
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

    #Outputlog(g_LOGMODE_INFORMATION, 'Store_SoilRainFile', 'end')

def Store_SoilRainFile1(h_fileName):
    global g_textSum_SoilRainFile1
    global g_textline_SoilRainFile1

    a_strErr = "filename=" + h_fileName
    Outputlog(g_LOGMODE_INFORMATION, 'Store_SoilRainFile1', a_strErr)

    # 災害発生降雨の検出結果を退避（メッシュ単位）

    try:
        g_textSum_SoilRainFile1 = 0
        g_textline_SoilRainFile1 = []
        a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
        g_textline_SoilRainFile1 = [ v for v in a_csv_obj]
        g_textSum_SoilRainFile1 = len(g_textline_SoilRainFile1)
        '''
        a_f = open(h_fileName, 'r', encoding='shift_jis')
        a_line = a_f.readline()
        while a_line:
            g_textSum_SoilRainFile1 += 1
            g_textline_SoilRainFile1.append(a_line.rstrip('\r\n'))
            a_line = a_f.readline()
        a_f.close()
        #print(g_textline_SoilRainFile1)
        '''
    except Exception as exp:
        a_strErr = "filename=" + h_fileName
        Outputlog(g_LOGMODE_ERROR, type(exp), a_strErr)

    #Outputlog(g_LOGMODE_INFORMATION, 'Store_SoilRainFile1', 'end')

def Str_isfloat(str):
    try:
        float(str)
        return True

    except ValueError as err:
        a_strErr = "str=" + str
        Outputlog(g_LOGMODE_ERROR, '[Str_isfloat]' + err, a_strErr)
        return False

def Write_TextLine(h_sw, h_textline):
    for a_iw in range(0, len(h_textline)):
        if (a_iw > 0):
            h_sw.write(',')
        h_sw.write(h_textline[a_iw])
