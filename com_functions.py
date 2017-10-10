import sys
import configparser
import  csv
import datetime
import math

class ComFunctions:
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

    g_Action_MakeContourOrigin = 312    # オリジナル等高線データの作成
    g_Action_MakeContourRevise = 313    # 等高線補正
    g_Action_MakeContourSnake = 314     # スネーク曲線
    g_Action_MakeContourSoilMin = 315   # 土壌雨量下限値

    def __init__(self):
        #pass

        self.proc_num = 0
        self.ini_path = ''

        self.g_startYear_TargetYearByMesh = 0
        self.g_endYear_TargetYearByMesh = 0
        self.g_msno_TargetYearByMesh = ""
        self.g_kikan_TargetYearByMesh = 0

        self.g_textSum_AllRainfall = 0
        self.g_textline_AllRainfall = []
        self.g_textSum_CalcForecastTime0File = 0
        self.g_textline_CalcForecastTime0File = []
        self.g_textSum_CalcForecastTime1File = 0
        self.g_textline_CalcForecastTime1File = []
        self.g_textSum_CautionAnnounceFile = 0
        self.g_textline_CautionAnnounceFile = []
        self.g_textSum_CautionAnnouncOccurFile = 0
        self.g_textline_CautionAnnouncOccurFile = []
        self.g_textSum_CautionAnnouncOccurRainfalleFile = 0
        self.g_textline_CautionAnnouncOccurRainfalleFile = []
        self.g_textSum_ChainOccurRainfallFile = 0
        self.g_textline_ChainOccurRainfallFile = []
        self.g_textSum_ChainOnlyOccurRainfallFile = 0
        self.g_textline_ChainOnlyOccurRainfallFile = []
        self.g_textSum_ContourReviseByMesh = 0
        self.g_textline_ContourReviseByMesh = []
        self.g_textSum_DisasterFile = 0
        self.g_textline_DisasterFile = []
        self.g_textSum_FindOccurRainfall = 0
        self.g_textline_FindOccurRainfall = []
        self.g_textSum_MeshListAll = 0
        self.g_textline_MeshListAll = []
        self.g_tyear_MeshListAll = 0
        self.g_textSum_PastCLFile = 0
        self.g_textline_PastCLFile = []
        self.g_textSum_OccurRainfallFile = 0
        self.g_textline_OccurRainfallFile = []
        self.g_textSum_OverRainfallFile = 0
        self.g_textline_OverRainfallFile = []
        self.g_textSum_OverAllRainfallFile = 0
        self.g_textline_OverAllRainfallFile = []
        self.g_textSum_OverNonOccurRainfallFile = 0
        self.g_textline_OverNonOccurRainfallFile = []
        self.g_textSum_OverNonOccurRainfall9_1File = 0
        self.g_textline_OverNonOccurRainfall9_1File = []
        self.g_textSum_OverOccurRainfallFile = 0
        self.g_textline_OverOccurRainfallFile = []
        self.g_textSum_OverOccurRainfall9_1File = 0
        self.g_textline_OverOccurRainfall9_1File = []
        self.g_textSum_OverOccurRainfall9_2File = 0
        self.g_textline_OverOccurRainfall9_2File = []
        self.g_textSum_RainfallFile = 0
        self.g_textline_RainfallFile = []
        self.g_textSum_RainfallFile1 = 0
        self.g_textline_RainfallFile1 = []
        self.g_textSum_RBFNFile = 0
        self.g_textline_RBFNFile = []
        self.g_textSum_SoilRainFile = 0
        self.g_textline_SoilRainFile = []
        self.g_textSum_SoilRainFile1 = 0
        self.g_textline_SoilRainFile1 = []
        self.g_textSum_SurfaceFile = []
        self.g_textline_SurfaceFile = []
        self.g_textSum_TargetMeshFile = 0
        self.g_textline_TargetMeshFile = []
        self.g_textSum_TemperatureFile = 0
        self.g_textline_TemperatureFile = []
        self.g_textSum_WhiffTimeFile = 0
        self.g_textline_WhiffTimeFile = []

        self.g_strIni = ""                   # INIファイル名
        self.g_target_year = 0               # 対象年
        self.g_tyear_MeshList = 0            # 対象メッシュ年

        self.g_LogPath = "."                 # ログパス("TEMPパス")
        self.g_LogEffectiveDays = 7          # ログ有効期間("7")
        self.g_LogLevel = 0                  # ログレベル("0")
        self.g_SystemTitle = ""              # システムのタイトル名
        self.g_TargetMeshFile = ""           # 対象メッシュNoファイル
        self.g_OccurSepTime = 24             # 発生降雨の前後時間範囲
        self.g_xUnit = 50                    # X軸の単位線
        self.g_yUnit = 10                    # Y軸の単位線
        self.g_UnrealAlpha = 1               # Unrealの係数
        self.g_ImageFileWidth = 320          # ファイル保存時の画像サイズ（幅）→pixel値
        self.g_ImageFileHeight = 160         # ファイル保存時の画像サイズ（高さ）→pixel値
        self.g_DrawRainfallMax = 0           # 60分間積算雨量の描画MAXサイズ→mm/hr
        self.g_DrawSoilMax = 0               # 土壌雨量指数の描画MAXサイズ→mm
        self.g_TargetPath = ""               # 気象庁元データパス
        self.g_TargetRainMesh = 5            # 対象雨量メッシュ
        self.g_TargetSurface = 5             # 既往CL対象メッシュ選択サポート
        self.g_TimeKind = 2                  # 30分データ取込
        self.g_TargetStartYear = 0           # 開始年
        self.g_TargetEndYear = 0             # 終了年
        self.g_OutPath = ""                  # 結果出力パス
        self.g_RBFNOutPath = ""              # RBFN結果出力パス
        self.g_RainfallFileSId = ""          # 解析雨量→2006.03.20
        self.g_RainfallFileEId = ""          # 解析雨量→2006.03.20
        self.g_SoilrainFileSId = ""          # 土壌雨量指数→2006.03.20
        self.g_SoilrainFileEId = ""          # 土壌雨量指数→2006.03.20
        self.g_DisasterFileName = ""         # 災害発生情報ファイル名
        self.g_TemperatureKind = 0           # 気温の取り込み→種別（0：なし、1：平均気温、2：最高気温）
        self.g_TemperatureMin = 0            # 気温の取り込み→最小気温
        self.g_TemperatureMax = 0            #気温の取り込み→最高気温
        self.g_TemperatureFileSId = ""       # 気温ファイル
        self.g_TemperatureFileEId = ""       # 気温ファイル
        self.g_BlockBackgroundImage = ""     # ブロック図背景→2006.04.05
        self.g_BlockExcelDefine = ""         # ブロック定義Excel→2006.04.05
        self.g_BlockDrawDefine = ""          # ブロック描画定義ファイル→2006.04.05
        self.g_CautionAnnounceFileName = ""  # 警戒発表情報ファイル[2012.06.28]①土砂災害警戒情報の災害捕捉率
        self.g_RecalcLimitFileName = ""      #下限値・上限値再集計ファイル

        self.g_RainKind = 0                  #実況雨量・予測雨量
        self.g_ForecastTime = 0              #
        self.g_OutPathReal = ""              #
        self.g_PastKind = 0                  # 既往CLの取り込み
        self.g_PastTargetStartYear = 0       #
        self.g_PastTargetEndYear = 0         #
        self.g_PastRBFNOutPath = ""          #
        self.g_PastCLFileName = ""           #
        self.g_NIGeDaS_NonOccurCalc =0       # NIGeDaS

    def _getInifile(self, inifile, section, name):
        try:
            return inifile.get(section, name)
        except Exception as exp:
            return "error: could not read " + name
        except:
            print(sys.exc_info())

    def CheckDate(self, h_year, h_month, h_day):
        a_strErr = str(h_year) + "/" + str(h_month) + "/" + str(h_day)
        try:
            a_newDataStr = "%04d/%02d/%02d" % (h_year,h_month,h_day)
            a_newDate=datetime.datetime.strptime(a_newDataStr, "%Y/%m/%d")
            return True
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'CheckDate', a_strErr + "," + " ".join(map(str, exp.args)))
            return False
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'CheckDate', a_strErr + "," + sys.exc_info())
            return False

    # INIファイルの読み込み
    def GetEnvData(self, h_ini_path):
        '''
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
        '''

        # 引数を取得
        args = sys.argv
        #g_strIni = args[1] #INIファイル名
        #g_target_year = args[2] #対象年
        #g_strIni = "C:\\Users\\hal\\Documents\\CTI\\東京\\RBFN修正ツール\\2015年度\\program-source\\bin\\rbfnmdf.ini"
        self.g_strIni = h_ini_path
        #print(self.g_strIni)
        #print("[g_strIni]" + g_strIni)
        self.g_target_year = 1999
        #print("[self.g_target_year]" + str(self.g_target_year))
        # INIファイル内容を読み込む
        a_inifile = configparser.SafeConfigParser()
        a_inifile.read(self.g_strIni)
        #for a_section in a_inifile.sections():
        #    print('===' + a_section + '===')

        self.g_SystemTitle = self._getInifile(a_inifile, 'All', 'SystemTitle')
        #print('[self.g_SystemTitle]' + self.g_SystemTitle)
        self.g_TargetMeshFile = self._getInifile(a_inifile, 'All', 'TargetMeshFile')
        #print('[self.g_TargetMeshFile]' + self.g_TargetMeshFile)
        #print('')

        self.g_TargetPath = self._getInifile(a_inifile, 'Rainfall', 'TargetPath')
        #print('[self.g_TargetPath]' + self.g_TargetPath)
        self.g_TargetStartYear = int(self._getInifile(a_inifile, 'Rainfall', 'TargetStartYear'))
        #print('[self.g_TargetStartYear]' + str(self.g_TargetStartYear))
        self.g_TargetEndYear = int(self._getInifile(a_inifile, 'Rainfall', 'TargetEndYear'))
        #print('[self.g_TargetEndYear]' + str(self.g_TargetEndYear))
        self.g_OutPath = self._getInifile(a_inifile, 'Rainfall', 'OutPath')
        #print('[self.g_OutPath]' + self.g_OutPath)
        self.g_RBFNOutPath = self._getInifile(a_inifile, 'Rainfall', 'RBFNOutPath')
        #print('[self.g_RBFNOutPath]' + self.g_RBFNOutPath)
        self.g_OccurSepTime = int(self._getInifile(a_inifile, 'Rainfall', 'OccurSepTime'))
        #print('[self.g_OccurSepTime]' + str(self.g_OccurSepTime))
        self.g_RainfallFileSId = self._getInifile(a_inifile, 'Rainfall', 'RainfallFileSId')
        #print('[self.g_RainfallFileSId]' + self.g_RainfallFileSId)
        self.g_RainfallFileEId = self._getInifile(a_inifile, 'Rainfall', 'RainfallFileEId')
        #print('[self.g_RainfallFileEId]' + self.g_RainfallFileEId)
        self.g_SoilrainFileSId = self._getInifile(a_inifile, 'Rainfall', 'SoilrainFileSId')
        #print('[self.g_SoilrainFileSId]' + self.g_SoilrainFileSId)
        self.g_SoilrainFileEId = self._getInifile(a_inifile, 'Rainfall', 'SoilrainFileEId')
        #print('[self.g_SoilrainFileEId]' + self.g_SoilrainFileEId)
        self.g_DisasterFileName = self._getInifile(a_inifile, 'Rainfall', 'DisasterFileName')
        #print('[self.g_DisasterFileName]' + self.g_DisasterFileName)
        self.g_TemperatureKind = int(self._getInifile(a_inifile, 'Rainfall', 'TemperatureKind'))
        #print('[self.g_TemperatureKind]' + str(self.g_TemperatureKind))
        self.g_TemperatureMin = float(self._getInifile(a_inifile, 'Rainfall', 'TemperatureMin'))
        #print('[self.g_TemperatureMin]' + str(self.g_TemperatureMin))
        self.g_TemperatureMax = float(self._getInifile(a_inifile, 'Rainfall', 'TemperatureMax'))
        #print('[self.g_TemperatureMax]' + str(self.g_TemperatureMax))
        self.g_TemperatureFileSId = self._getInifile(a_inifile, 'Rainfall', 'TemperatureFileSId')
        #print('[self.g_TemperatureFileSId]' + self.g_TemperatureFileSId)
        self.g_TemperatureFileEId = self._getInifile(a_inifile, 'Rainfall', 'TemperatureFileEId')
        #print('[self.g_TemperatureFileEId]' + self.g_TemperatureFileEId)
        self.g_CautionAnnounceFileName = self._getInifile(a_inifile, 'Rainfall', 'CautionAnnounceFileName')
        #print('[self.g_CautionAnnounceFileName]' + self.g_CautionAnnounceFileName)
        self.g_RainKind = int(self._getInifile(a_inifile, 'Rainfall', 'RainKind'))
        #print('[self.g_RainKind]' + str(self.g_RainKind))
        self.g_ForecastTime = int(self._getInifile(a_inifile, 'Rainfall', 'ForecastTime'))
        #print('[self.g_ForecastTime]' + str(self.g_ForecastTime))
        self.g_OutPathReal = self._getInifile(a_inifile, 'Rainfall', 'OutPathReal')
        #print('[self.g_OutPathReal]' + self.g_OutPathReal)
        self.g_TargetRainMesh = int(self._getInifile(a_inifile, 'Rainfall', 'TargetRainMesh'))
        #print('[self.g_TargetRainMesh]' + str(self.g_TargetRainMesh))
        self.g_TimeKind = int(self._getInifile(a_inifile, 'Rainfall', 'TimeKind'))
        #print('[self.g_TimeKind]' + str(self.g_TimeKind))
        self.g_RecalcLimitFileName = self._getInifile(a_inifile, 'Rainfall', 'RecalcLimitFileName')
        #print('[self.g_RecalcLimitFileName]' + self.g_RecalcLimitFileName)
        #print('')

        self.g_xUnit = float(self._getInifile(a_inifile, 'RBFN', 'XUnit'))
        #print('[self.g_xUnit]' + str(self.g_xUnit))
        self.g_yUnit = float(self._getInifile(a_inifile, 'RBFN', 'YUnit'))
        #print('[self.g_yUnit]' + str(self.g_yUnit))
        self.g_UnrealAlpha = float(self._getInifile(a_inifile, 'RBFN', 'UnrealAlpha'))
        #print('[self.g_UnrealAlpha]' + str(self.g_UnrealAlpha))
        self.g_ImageFileWidth = float(self._getInifile(a_inifile, 'RBFN', 'ImageFileWidth'))
        #print('[self.g_ImageFileWidth]' + str(self.g_ImageFileWidth))
        self.g_ImageFileHeight = float(self._getInifile(a_inifile, 'RBFN', 'ImageFileHeight'))
        #print('[self.g_ImageFileHeight]' + str(self.g_ImageFileHeight))
        self.g_DrawRainfallMax = float(self._getInifile(a_inifile, 'RBFN', 'DrawRainfallMax'))
        #print('[self.g_DrawRainfallMax]' + str(self.g_DrawRainfallMax))
        self.g_DrawSoilMax = float(self._getInifile(a_inifile, 'RBFN', 'DrawSoilMax'))
        #print('[self.g_DrawSoilMax]' + str(self.g_DrawSoilMax))
        self.g_PastKind= int(self._getInifile(a_inifile, 'RBFN', 'PastKind'))
        #print('[self.g_PastKind]' + str(self.g_PastKind))
        self.g_PastTargetStartYear = int(self._getInifile(a_inifile, 'RBFN', 'PastTargetStartYear'))
        #print('[self.g_PastTargetStartYear]' + str(self.g_PastTargetStartYear))
        self.g_PastTargetEndYear = int(self._getInifile(a_inifile, 'RBFN', 'PastTargetEndYear'))
        #print('[self.g_PastTargetEndYear]' + str(self.g_PastTargetEndYear))
        self.g_PastRBFNOutPath = self._getInifile(a_inifile, 'RBFN', 'PastRBFNOutPath')
        #print('[self.g_PastRBFNOutPath]' + self.g_PastRBFNOutPath)
        self.g_PastCLFileName = self._getInifile(a_inifile, 'RBFN', 'PastCLFileName')
        #print('[self.g_PastCLFileName]' + self.g_PastCLFileName)
        self.g_TargetSurface = int(self._getInifile(a_inifile, 'RBFN', 'TargetSurface'))
        #print('[self.g_TargetSurface]' + str(self.g_TargetSurface))
        self.g_NIGeDaS_NonOccurCalc = int(self._getInifile(a_inifile, 'RBFN', 'NIGeDaS_NonOccurCalc'))
        #print('[self.g_NIGeDaS_NonOccurCalc]' + str(self.g_NIGeDaS_NonOccurCalc))
        #print('')

        self.g_BlockBackgroundImage = self._getInifile(a_inifile, 'Block', 'BlockBackgroundImage')
        #print('[self.g_BlockBackgroundImage]' + self.g_BlockBackgroundImage)
        self.g_BlockExcelDefine = self._getInifile(a_inifile, 'Block', 'BlockExcelDefine')
        #print('[self.g_BlockExcelDefine]' + self.g_BlockExcelDefine)
        self.g_BlockDrawDefine = self._getInifile(a_inifile, 'Block', 'BlockDrawDefine')
        #print('[self.g_BlockDrawDefine]' + self.g_BlockDrawDefine)
        #print('')

        self.g_LogPath = self._getInifile(a_inifile, 'LogInfo', 'LogPath')
        #print('[self.g_LogPath]' + self.g_LogPath)
        self.g_LogEffectiveDays = int(self._getInifile(a_inifile, 'LogInfo', 'LogEffectiveDays'))
        #print('[self.g_LogEffectiveDays]' + str(self.g_LogEffectiveDays))
        self.g_LogLevel = int(self._getInifile(a_inifile, 'LogInfo', 'LogLevel'))
        #print('[self.g_LogLevel]' + str(self.g_LogLevel))

    def GetMeshList(self, h_tyear, h_meshList):
        a_strErr = "Year=" + str(h_tyear)
        self.Outputlog(self.g_LOGMODE_TRACE1, 'GetMeshList', a_strErr)

        a_iRet = 0

        try:
            del h_meshList[:]

            a_sr = open(self.g_OutPath + "\\" + self.g_MeshSymbol + str(h_tyear) + ".csv", 'r', encoding='shift_jis')
            # 1行目をリスト変数に読み込む。
            a_textline = a_sr.readline().rstrip('\r\n')
            a_iRet = int(a_textline)
            # 2行目をリスト変数に読み込む。
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                #print(a_textline)
                if (a_textline != ''):
                    # メッシュ番号を書き込み
                    a_split = a_textline.split(',')
                    if self.g_TargetRainMesh == 1:
                        # 1kmメッシュ
                        h_meshList.append(a_split[1])
                    else:
                        # 5kmメッシュ
                        h_meshList.append(a_split[0])
                a_textline = a_sr.readline().rstrip('\r\n')
            a_sr.close()

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, type(exp), a_strErr)

        self.Outputlog(self.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))
        #com.Outputlog(com.g_LOGMODE_TRACE1, '_getMeshSum', 'end')

        return a_iRet

    def GetMeshSum(self, h_year, h_RainfallFileName, h_meshList):
        a_strErr = "Year=" + str(h_year) + ",RainfallFileName=" + h_RainfallFileName
        self.Outputlog(self.g_LOGMODE_TRACE1, '_getMeshSum', a_strErr)

        a_iRet = 0

        try:
            del h_meshList[:]

            # 解析雨量ファイルを開く。
            a_sr = open(h_RainfallFileName, 'r', encoding='shift_jis')
            # メッシュファイルを開く。
            a_sw = open(self.g_OutPath + "\\" + self.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
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
            self.Outputlog(self.g_LOGMODE_ERROR, type(exp), a_strErr)

        self.Outputlog(self.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))
        #com.Outputlog(com.g_LOGMODE_TRACE1, '_getMeshSum', 'end')

        return a_iRet

    def GetMeshSum2(self, h_year, h_RainfallFileName, h_meshList):
        a_strErr = "Year=" + str(h_year) + ",RainfallFileName=" + h_RainfallFileName
        self.Outputlog(self.g_LOGMODE_TRACE1, '_getMeshSum2', a_strErr)

        a_iRet = 0

        try:
            del h_meshList[:]

            # 解析雨量ファイルを開く。
            a_sr = open(h_RainfallFileName, 'r', encoding='shift_jis')
            # メッシュファイルを開く。
            a_sw = open(self.g_OutPath + "\\" + self.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
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
                if self.g_TargetRainMesh == 1:
                    # 1kmメッシュ
                    a_sw.write(a_split[0] + "," + a_split[1] + '\n')
                    #h_meshList.append(a_split[0] + "," + a_split[1])
                    h_meshList.append(a_split[1])
                else:
                    # 5kmメッシュ
                    a_sw.write(a_split[0] + '\n')
                    h_meshList.append(a_split[0])

                    h_meshList.append(a_split[a_cnt].rstrip('\r\n'))
            # ファイルをクローズする。(Close)
            a_sr.close()
            # ファイルをクローズする。(Close)
            a_sw.close()
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, type(exp), a_strErr)

        self.Outputlog(self.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))
        #com.Outputlog(com.g_LOGMODE_TRACE1, '_getMeshSum', 'end')

        return a_iRet

    def GetMeshSumFromFile(self, h_year, h_meshList):
        a_strErr = "Year=" + str(h_year)
        self.Outputlog(self.g_LOGMODE_TRACE1, '_getMeshSumFromFile', a_strErr)

        a_iRet = 0

        try:
            del h_meshList[:]

            # 対象メッシュNoファイルを開く。
            a_sr = open(self.g_TargetMeshFile, 'r', encoding='shift_jis')
            # メッシュ数をカウントする。
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                a_iRet += 1
                a_textline = a_sr.readline().rstrip('\r\n')
            a_sr.close()
            # 対象メッシュNoファイルを開く。
            a_sr = open(self.g_TargetMeshFile, 'r', encoding='shift_jis')
            # メッシュファイルを開く。
            a_sw = open(self.g_OutPath + "\\" + self.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
            # メッシュ数を書込
            a_sw.write(str(a_iRet) + '\n')
            # メッシュ番号を取得する。
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                #print(a_textline)
                if (a_textline != ''):
                    # メッシュ番号を書き込み
                    a_split = a_textline.split(',')
                    if self.g_TargetRainMesh == 1:
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
            self.Outputlog(self.g_LOGMODE_ERROR, type(exp), a_strErr)

        #com.Outputlog(com.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))
        #com.Outputlog(com.g_LOGMODE_TRACE1, '_getMeshSumFromFile', 'end')

        return a_iRet

    def GetMeshSumFromFile2(self, h_year, h_meshList):
        a_strErr = "Year=" + str(h_year)
        self.Outputlog(self.g_LOGMODE_TRACE1, '_getMeshSumFromFile2', a_strErr)

        a_iRet = 0

        try:
            del h_meshList[:]

            # 対象メッシュNoファイルを開く。
            a_sr = open(self.g_TargetMeshFile, 'r', encoding='shift_jis')
            # メッシュ数をカウントする。
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                a_iRet += 1
                a_textline = a_sr.readline().rstrip('\r\n')
            a_sr.close()
            # 対象メッシュNoファイルを開く。
            a_sr = open(self.g_TargetMeshFile, 'r', encoding='shift_jis')
            # メッシュファイルを開く。
            a_sw = open(self.g_OutPath + "\\" + self.g_MeshSymbol + str(h_year) + ".csv", "w", encoding='shift_jis')
            # メッシュ数を書込
            a_sw.write(str(a_iRet) + '\n')
            # メッシュ番号を取得する。
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                #print(a_textline)
                if (a_textline != ''):
                    # メッシュ番号を書き込み
                    a_split = a_textline.split(',')
                    if self.g_TargetRainMesh == 1:
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
            self.Outputlog(self.g_LOGMODE_ERROR, type(exp), a_strErr)

        #com.Outputlog(com.g_LOGMODE_TRACE1, 'a_iRet', str(a_iRet))
        #com.Outputlog(com.g_LOGMODE_TRACE1, '_getMeshSumFromFile', 'end')

        return a_iRet

    # 全降雨の超過数を取得する。
    def GetOccurRainfallSumByMesh(self, h_meshNo):
        a_strErr = "meshNo=" + h_meshNo
        self.Outputlog(self.g_LOGMODE_TRACE1, 'GetOccurRainfallSumByMesh', a_strErr)

        a_iRet = 0

        try:
            for a_cnt in range(int(self.g_TargetStartYear), int(self.g_TargetEndYear) + 1):
                a_sr = open(self.g_OutPath + "\\" + h_meshNo + "\\" + self.g_OccurRainfallSymbol + str(a_cnt) + ".csv", "r", encoding="shift_jis")
                # 1行目から災害発生降雨数を取得する。
                a_strTmp = a_sr.readline().strip()
                a_split1 = a_strTmp.split(',')
                a_textSum1 = int(a_split1[9])
                '''
                if (a_cnt == int(self.g_TargetStartYear)):
                    # 1行目から気温情報を取得する。→2006.03.27
                    h_tempInfo = "," + a_split1[10] + "," + a_split1[11] + "," + a_split1[12]
                    '''
                a_sr.close()
                a_iRet += a_textSum1

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetOccurRainfallSumByMesh', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.Outputlog(self.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetOccurRainfallSumByMesh', a_strErr + "," + sys.exc_info())

        return a_iRet

    # 1kmメッシュのみで使用
    def GetParnetMeshNo(
            self,
            tyear,
            msno
    ):
        a_strErr = ""

        a_sRet = ""

        try:
            if (self.g_tyear_MeshList != tyear):
                self.g_textSum_MeshListAll = self.Store_DataFile(self.g_OutPath + "\\" + self.g_MeshSymbol + str(tyear) + ".csv", self.g_textline_MeshListAll)

            for a_cnt in range(1, self.g_textSum_MeshListAll):
                a_split = self.g_textline_MeshListAll[a_cnt]
                if (a_split[1] == msno):
                    a_sRet = a_split[0]
                    break

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetParnetMeshNo', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetParnetMeshNo', a_strErr + "," + sys.exc_info())

        return a_sRet

    #
    def GetPastCLData(self, h_meshNo):
        a_strErr = "meshNo=" + h_meshNo
        self.Outputlog(self.g_LOGMODE_TRACE1, 'GetPastCLData', a_strErr)

        a_RBFN = 0
        a_soilMin = 0
        a_rainMax = -1

        try:
            if (self.g_textSum_PastCLFile == 0):
                # 初回
                #self.Store_PastCLFile()
                self.g_textSum_PastCLFile = self.Store_DataFile(self.g_PastCLFileName, self.g_textline_PastCLFile)

            for a_cnt in range(1, self.g_textSum_PastCLFile):
                a_split1 = self.g_textline_PastCLFile[a_cnt]
                if (a_split1[0] == h_meshNo):
                    a_val = float(a_split1[1])
                    if (a_val == 0.9):
                        a_RBFN = 0
                    elif (a_val == 0.8):
                        a_RBFN = 1
                    elif (a_val == 0.7):
                        a_RBFN = 2
                    elif (a_val == 0.6):
                        a_RBFN = 3
                    elif (a_val == 0.5):
                        a_RBFN = 4
                    elif (a_val == 0.4):
                        a_RBFN = 5
                    elif (a_val == 0.3):
                        a_RBFN = 6
                    elif (a_val == 0.2):
                        a_RBFN = 7
                    elif (a_val == 0.1):
                        a_RBFN = 8
                    else:
                        a_RBFN = 0

                    a_soilMin = float(a_split1[2])

                    if (len(a_split1) >= 4):
                            a_rainMax = float(a_split1[3]) # 60分間積算雨量上限値のサポート
                    else:
                        a_rainMax = -1

                    break

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetPastCLData', a_strErr +  str(exp.args[0]))
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetPastCLData', a_strErr + "," + sys.exc_info())

        return a_RBFN, a_soilMin, a_rainMax

    # 既往CL取込時の対象メッシュ番号を処理する
    def GetTargetMeshNoByCL(self, h_tyear, h_msno):
        a_strErr = "year=" + str(h_tyear) + ',msno=' + h_msno
        self.Outputlog(self.g_LOGMODE_TRACE1, 'GetTargetMeshNoByCL', a_strErr)

        a_msno = ''

        try:
            if (self.g_TargetRainMesh == 1):
                # 対象雨量が1km
                if (self.g_textSum_MeshListAll == 0):
                    if (h_tyear != self.g_tyear_MeshListAll):
                        # 異なる
                        self.Store_MeshListAll(h_tyear)
                else:
                    # 初回
                    self.Store_MeshListAll(h_tyear)

                # 1行目はメッシュ数
                for a_cnt in range(1, self.g_textSum_MeshListAll):
                    #a_split = self.g_textline_MeshListAll[a_cnt].split(',')
                    a_split = self.g_textline_MeshListAll[a_cnt]
                    if (a_split[1] == h_msno):
                        if (self.g_TargetSurface == 1):
                            # 対象Surfaceが1km
                            a_msno = a_split[1]
                        else:
                            # 対象Surfaceが5km
                            a_msno = a_split[0]
                        break
            '''
            else:
                # 対象雨量が5km
                '''

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetTargetMeshNoByCL', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetTargetMeshNoByCL', a_strErr + "," + sys.exc_info())

        return a_msno

    # 対象期間を取得する
    def GetTargetYearByMesh(self, h_StartYear, h_EndYear, h_OutPath, h_meshNo):
        a_strErr = "meshNo=" + h_meshNo
        self.Outputlog(self.g_LOGMODE_TRACE1, 'GetTargetYearByMesh', a_strErr)

        a_dRet = 0

        try:
            if (h_StartYear == self.g_startYear_TargetYearByMesh) and (h_EndYear == self.g_endYear_TargetYearByMesh) and (h_meshNo == self.g_msno_TargetYearByMesh):
                # 既に退避済み
                a_dRet = self.g_kikan_TargetYearByMesh
            else:
                # 初回
                self.g_startYear_TargetYearByMesh = h_StartYear
                self.g_endYear_TargetYearByMesh = h_EndYear
                self.g_msno_TargetYearByMesh = h_meshNo
                self.g_kikan_TargetYearByMesh = 0
                for a_cnt in range(h_StartYear, h_EndYear + 1):
                    # 該当年の日数を計算する。
                    # 通常は365日、閏年は366日
                    a_bRet = self.CheckDate(a_cnt, 2, 29)
                    if (a_bRet == True):
                        a_tdays = 366
                    else:
                        a_tdays = 365
                    a_ttimes = a_tdays * 24

                    if (self.g_TimeKind == 1):
                        # 30分の場合
                        a_ttimes *= 2

                    # 結果出力ファイルを開く。(OPen)
                    self.g_textSum_AllRainfall = self.Store_DataFile(h_OutPath + "\\" + h_meshNo + "\\" + self.g_AllRainfallSymbol + str(a_cnt) + ".csv", self.g_textline_AllRainfall)
                    a_sum = self.g_textSum_AllRainfall - 1
                    if (a_sum > 0):
                        a_dRet += (a_sum / a_ttimes)
                        self.g_kikan_TargetYearByMesh = a_dRet

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetTargetYearByMesh', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetTargetYearByMesh', a_strErr + "," + sys.exc_info())

        return a_dRet

    # 気温情報を取得する。
    def GetTemperatureInfo(self, h_meshNo):
        a_strErr = "meshNo=" + h_meshNo
        self.Outputlog(self.g_LOGMODE_TRACE1, 'GetTemperatureInfo', a_strErr)

        a_sRet = ",,,"

        try:
            a_sr = open(self.g_OutPath + "\\" + h_meshNo + "\\" + self.g_OccurRainfallSymbol + str(self.g_TargetStartYear) + ".csv", "r", encoding="shift_jis")
            # 1行目から災害発生降雨数を取得する。
            a_strTmp = a_sr.readline().strip()
            a_split1 = a_strTmp.split(',')
            # 1行目から気温情報を取得する。→2006.03.27
            a_sRet = "," + a_split1[10] + "," + a_split1[11] + "," + a_split1[12]
            a_sr.close()

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetTemperatureInfo', a_strErr + "," + " ".join(map(str, exp.args)))
            #self.com.Outputlog(self.com.g_LOGMODE_TRACE1, 'run', 'end')
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'GetTemperatureInfo', a_strErr + "," + sys.exc_info())

        return a_sRet

    def My_round(self, x, d=0):
        a_strErr = ""
        a_iRet = 0

        try:
            p = 10 ** d
            a_iRet = float(math.floor((x * p) + math.copysign(0.5, x)))/p

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, '[Str_isfloat]', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'Str_isfloat', a_strErr + "," + sys.exc_info())

        return a_iRet

    def Outputlog(self, h_mode, h_Source, h_desc):
        '''
        global g_LOG_FILENAME
        global g_LOGMODE_ERROR
        global g_LOGMODE_DISCLAIMER
        global g_LOGMODE_WARNING
        global g_LOGMODE_INFORMATION
        global g_LOGMODE_TRACE1
        global g_LOGMODE_TRACE2
        global g_LOG_SUCCESSFUL
        '''

        a_strwork1 = ""
        a_exeMode = False

        try:
            # エラー種別により出力文字列を設定する。
            if h_mode == self.g_LOGMODE_ERROR:
                # エラー
                if self.g_LogLevel >= self.g_LOGMODE_ERROR :
                    a_strwork1 = "[ERROR]"
                    a_exeMode = True
            elif h_mode == self.g_LOGMODE_DISCLAIMER:
                # 警告
                if self.g_LogLevel >= self.g_LOGMODE_DISCLAIMER:
                    a_strwork1 = "[DISCLAIMER]"
                    a_exeMode = True
            elif h_mode == self.g_LOGMODE_WARNING:
                # ワーニング
                if self.g_LogLevel >= self.g_LOGMODE_WARNING:
                    a_strwork1 = "[WARNING]"
                    a_exeMode = True
            elif h_mode == self.g_LOGMODE_INFORMATION:
                # 情報
                if self.g_LogLevel >= self.g_LOGMODE_INFORMATION:
                    a_strwork1 = "[INFORMATION]"
                    a_exeMode = True
            elif h_mode == self.g_LOGMODE_TRACE1:
                # トレース
                if self.g_LogLevel >= self.g_LOGMODE_TRACE1:
                    a_strwork1 = "[TRACE1]"
                    a_exeMode = True
            elif h_mode == self.g_LOGMODE_TRACE2:
                # トレース
                if self.g_LogLevel >= self.g_LOGMODE_TRACE2:
                    a_strwork1 = "[TRACE2]"
                    a_exeMode = True

            if (a_exeMode == True):
                a_now = datetime.datetime.now()
                a_now1 = a_now.strftime("%Y%m%d")
                a_now2 = a_now.strftime("%Y/%m/%d %H:%M:%S.") + "%04d" % (a_now.microsecond // 1000)
                a_strwork2 = self.g_LogPath + "\\" + self.g_LOG_FILENAME + "_" + a_now1 + "_" + str(self.proc_num) + ".log"
                a_sw = open(a_strwork2, "a", encoding="shift_jis")
                a_sw.write(a_now2 + ',' + a_strwork1 + '(' + h_Source + '),' + h_desc + '\n')
                a_sw.close()

        except:
            print(sys.exc_info())
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), "")

    def Replace_TextLine(self, h_textline, h_srcChr, h_dstChr):
        for a_iw in range(0, len(h_textline)):
            h_textline[a_iw] = h_textline[a_iw].replace(h_srcChr, h_dstChr)

    # 気温情報を取得する
    # 返り値    : 気温情報
    #             1カラム目：気温取り込み種別（0:なし、1：平均気温、2：最高気温）
    #             2カラム目：範囲最小気温
    #             3カラム目：範囲最大気温
    #             4カラム目：計算結果の平均気温→これは、一連の降雨毎に算出する事になる。
    #             5カラム目：計算結果の最高気温→これは、一連の降雨毎に算出する事になる。
    def SetTemperatureInfo(self):
        '''
        global g_TemperatureKind
        global g_TemperatureMin
        global g_TemperatureMax
        '''

        a_sRet = ''
        a_sRet += ',' + str(self.g_TemperatureKind)
        a_sRet += ',' + str(self.g_TemperatureMin)
        a_sRet += ',' + str(self.g_TemperatureMax)

        return a_sRet

    '''
    def Store_AllRainfall(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_AllRainfall', a_strErr)

        # 全解析雨量・土壌雨量指数ファイルを開く

        try:
            self.g_textSum_AllRainfall = 0
            self.g_textline_AllRainfall = None
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_AllRainfall = [ v for v in a_csv_obj]
            self.g_textSum_AllRainfall = len(self.g_textline_AllRainfall)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)

        #Outputlog(self.g_LOGMODE_TRACE1, 'Store_AllRainfall', 'end')
        '''

    '''
    def Store_CautionAnnounceFile(self):
        a_strErr = "filename=" + self.g_CautionAnnounceFileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_CautionAnnounceFile', a_strErr)

        # 災害発生降雨の検出結果を退避（メッシュ単位）

        try:
            self.g_textSum_CautionAnnounceFile = 0
            self.g_textline_CautionAnnounceFile = []
            a_csv_obj = csv.reader(open(self.g_CautionAnnounceFileName, 'r', encoding='shift_jis'))
            self.g_textline_CautionAnnounceFile = [ v for v in a_csv_obj]
            self.g_textSum_CautionAnnounceFile = len(self.g_textline_CautionAnnounceFile)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)
            '''

    '''
    def Store_ContourReviseByMesh(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_ContourReviseByMesh', a_strErr)

        try:
            self.g_textSum_ContourReviseByMesh = 0
            self.g_textline_ContourReviseByMesh = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_ContourReviseByMesh = [ v for v in a_csv_obj]
            self.g_textSum_ContourReviseByMesh = len(self.g_textline_ContourReviseByMesh)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)
            '''

    # CSVファイル退避
    #def Store_DataFile(self, h_fileName, h_textSum, h_textLine):
    def Store_DataFile(self, h_fileName, h_textLine):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_DataFile', a_strErr)

        a_iRet = 0
        try:
            '''
            h_textSum = 0
            h_textLine = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            h_textLine = [ v for v in a_csv_obj]
            h_textSum = len(h_textLine)
            '''
            del h_textLine[:]
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            for v in a_csv_obj:
                h_textLine.append(v)
            a_iRet = len(h_textLine)
        except Exception as exp:
            #self.Outputlog(self.g_LOGMODE_ERROR, 'Store_DataFile', a_strErr + str(exp.args[0]))
            self.Outputlog(self.g_LOGMODE_ERROR, 'Store_DataFile', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'Store_DataFile', a_strErr + "," + sys.exc_info())

        return a_iRet

    '''
    def Store_DisasterFile(self):
        a_strErr = "filename=" + self.g_DisasterFileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_DisasterFile', a_strErr)

        # 災害発生降雨の検出結果を退避（メッシュ単位）

        try:
            self.g_textSum_DisasterFile = 0
            self.g_textline_DisasterFile = []
            a_csv_obj = csv.reader(open(self.g_DisasterFileName, 'r', encoding='shift_jis'))
            self.g_textline_DisasterFile = [ v for v in a_csv_obj]
            self.g_textSum_DisasterFile = len(self.g_textline_DisasterFile)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)
            '''

    '''
    def Store_FindOccurRainfall(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_FindOccurRainfall', a_strErr)

        # 災害発生降雨の検出結果を退避（メッシュ単位）

        try:
            self.g_textSum_FindOccurRainfall = 0
            self.g_textline_FindOccurRainfall = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_FindOccurRainfall = [ v for v in a_csv_obj]
            self.g_textSum_FindOccurRainfall = len(self.g_textline_FindOccurRainfall)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)
            '''

    def Store_MeshListAll(self, h_tyear):
        a_strErr = "year=" + str(h_tyear)
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_MeshListAll', a_strErr)

        try:
            self.g_textSum_MeshListAll = 0
            self.g_textline_MeshListAll = []
            g_tyear_MeshListAll = 0
            a_csv_obj = csv.reader(open(self.g_OutPath + "\\" + self.g_MeshSymbol + str(h_tyear) + ".csv", 'r', encoding='shift_jis'))
            self.g_textline_MeshListAll = [ v for v in a_csv_obj]
            self.g_textSum_MeshListAll = len(self.g_textline_MeshListAll)
            g_tyear_MeshListAll = h_tyear
            # 1行目は、メッシュ数の為、読み飛ばし

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, 'Store_MeshListAll', a_strErr + "," + " ".join(map(str, exp.args)))
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'Store_MeshListAll', a_strErr + "," + sys.exc_info())

    '''
    def Store_PastCLFile(self):
        a_strErr = ""
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_MeshListAll', a_strErr)

        try:
            self.g_textSum_PastCLFile = 0
            self.g_textline_PastCLFile = []
            a_csv_obj = csv.reader(open(self.g_PastCLFileName, 'r', encoding='shift_jis'))
            self.g_textline_PastCLFile = [ v for v in a_csv_obj]
            self.g_textSum_PastCLFile = len(self.g_textline_PastCLFile)

        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)
            '''

    '''
    def Store_RainfallFile(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_RainfallFile', a_strErr)

        # 災害発生降雨の検出結果を退避（メッシュ単位）

        try:
            self.g_textSum_RainfallFile = 0
            self.g_textline_RainfallFile = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_RainfallFile = [ v for v in a_csv_obj]
            self.g_textSum_RainfallFile = len(self.g_textline_RainfallFile)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)

        #Outputlog(self.g_LOGMODE_TRACE1, 'Store_RainfallFile', 'end')
        '''

    '''
    def Store_RainfallFile1(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_RainfallFile1', a_strErr)

        # 災害発生降雨の検出結果を退避（メッシュ単位）

        try:
            self.g_textSum_RainfallFile1 = 0
            self.g_textline_RainfallFile1 = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_RainfallFile1 = [ v for v in a_csv_obj]
            self.g_textSum_RainfallFile1 = len(self.g_textline_RainfallFile1)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)

        #Outputlog(self.g_LOGMODE_TRACE1, 'Store_RainfallFile1', 'end')
        '''

    '''
    def Store_SoilRainFile(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_SoilRainFile', a_strErr)

        # 災害発生降雨の検出結果を退避（メッシュ単位）

        try:
            self.g_textSum_SoilRainFile = 0
            self.g_textline_SoilRainFile = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_SoilRainFile = [ v for v in a_csv_obj]
            self.g_textSum_SoilRainFile = len(self.g_textline_SoilRainFile)
        except Exception as exp:
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)

        #Outputlog(self.g_LOGMODE_TRACE1, 'Store_SoilRainFile', 'end')
        '''

    '''
    def Store_SoilRainFile1(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_SoilRainFile1', a_strErr)

        # 災害発生降雨の検出結果を退避（メッシュ単位）

        try:
            self.g_textSum_SoilRainFile1 = 0
            self.g_textline_SoilRainFile1 = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_SoilRainFile1 = [ v for v in a_csv_obj]
            self.g_textSum_SoilRainFile1 = len(self.g_textline_SoilRainFile1)
        except Exception as exp:
            a_strErr = "filename=" + h_fileName
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)

        #Outputlog(self.g_LOGMODE_TRACE1, 'Store_SoilRainFile1', 'end')
        '''

    '''
    def Store_TemperatureFile(self, h_fileName):
        a_strErr = "filename=" + h_fileName
        self.Outputlog(self.g_LOGMODE_TRACE1, 'Store_TemperatureFile', a_strErr)

        # 気温情報を退避

        try:
            self.g_textSum_TemperatureFile = 0
            self.g_textline_TemperatureFile = []
            a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
            self.g_textline_TemperatureFile = [ v for v in a_csv_obj]
            self.g_textSum_TemperatureFile = len(self.g_textline_TemperatureFile)
        except Exception as exp:
            a_strErr = "filename=" + h_fileName
            self.Outputlog(self.g_LOGMODE_ERROR, str(exp.args), a_strErr)
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, sys.exc_info(), a_strErr)

            #Outputlog(self.g_LOGMODE_TRACE1, 'Store_TemperatureFile', 'end')
            '''

    def Str_isfloat(self, str):
        a_strErr = "str=" + str
        try:
            float(str)
            return True

        #except ValueError as err:
        except Exception as exp:
            #self.Outputlog(self.g_LOGMODE_ERROR, '[Str_isfloat]' + str(err), a_strErr)
            #self.Outputlog(self.g_LOGMODE_ERROR, 'Str_isfloat', a_strErr + str(exp.args[0]))
            self.Outputlog(self.g_LOGMODE_ERROR, '[Str_isfloat]', a_strErr + "," + " ".join(map(str, exp.args)))
            return False
        except:
            self.Outputlog(self.g_LOGMODE_ERROR, 'Str_isfloat', a_strErr + "," + sys.exc_info())
            return False

    def Write_TextLine(self, h_sw, h_textline):
        for a_iw in range(0, len(h_textline)):
            if (a_iw > 0):
                h_sw.write(',')
            h_sw.write(h_textline[a_iw])
