import sys
import wx
import wx.lib.mixins.listctrl as listmix
from subprocess import check_call
from multiprocessing import Process
import com_functions
import clsRainfall
import clsFigure

com = com_functions.ComFunctions()

g_ini_path = "C:\\Users\\hal\\Documents\\CTI\\東京\\RBFN修正ツール\\2015年度\\program-source\\bin\\rbfnmdf.ini"
g_System_Title = "RBFN修正ツール Ver 3.0"
g_meshSum_targer = 0
g_meshSum_all = 0
g_meshList = []
g_meshList2 = []

class Main(wx.Frame):
    g_panel_11 = None   # RBFNプログラム用入力データ
    g_panel_12 = None   # RBFNプログラムの起動
    g_panel_13 = None   # RBFN出力値の抽出処理

    g_panel_21 = None   # RBFN補正の結果
    g_panel_22 = None   # 集計結果
    g_panel_23 = None   # ブロック集計

    g_button_11_1 = None
    g_button_11_2 = None
    g_listBox_11 = None

    g_button_13_1 = None
    g_button_13_2 = None
    g_button_13_3 = None
    g_button_13_4 = None
    g_listBox_13_1 = None
    g_listBox_13_2 = None

    def __init__(self, parent, id, title):
        """ レイアウトの作成 """
        wx.Frame.__init__(self, parent, id, title)
        self.SetBackgroundColour("#696969")
        self.lblTitle = wx.StaticText(self, wx.ID_ANY, "")
        self.lblTitle.SetForegroundColour("#FFFF00")

        self._get_environ()

        panel = wx.Panel(self, wx.ID_ANY)

        ################################################################################
        # メニューバー
        ################################################################################
        menu_bar = wx.MenuBar()

        #自動生成
        mnu_MakeAuto = wx.Menu()
        mnu_MakeAuto.Append(11, "RBFNプログラム用入力データ")
        mnu_MakeAuto.Append(12, "RBFNプログラムの起動")
        mnu_MakeAuto.Append(13, "RBFN出力値の抽出処理")
        menu_bar.Append(mnu_MakeAuto, "自動生成")
        self.SetMenuBar(menu_bar)

        #結果表示
        mnu_DispResult = wx.Menu()
        mnu_DispResult.Append(21, "RBFN補正の結果")
        mnu_DispResult.Append(22, "集計結果")
        mnu_DispResult.Append(23, "ブロック集計")
        menu_bar.Append(mnu_DispResult, "結果表示")
        self.SetMenuBar(menu_bar)

        #終了
        '''
        mnu_Exit = wx.Menu()
        menu_bar.Append(mnu_Exit, "終了")
        self.SetMenuBar(menu_bar)
        '''

        ################################################################################
        # メニュークリック時のイベント登録
        ################################################################################
        self.Bind(wx.EVT_MENU, self._click_menu_bar)

        ################################################################################
        # パネルの作成
        ################################################################################
        self._makePanel_11()
        self._makePanel_13()
        self._makePanel_21()
        self._makePanel_22()
        self._makePanel_23()
        self._hide_Panel()

        self.Bind(wx.EVT_SIZE, self._get_frame)

        self.Maximize()
        self.Show(True)

    def _click_button_11_1(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■RBFNプログラム用入力データ作成")

        if (wx.MessageBox("RBFNプログラム用の入力データを自動作成します。\nよろしいですか？", g_System_Title, wx.YES_NO) == wx.YES):
            self._makeAllRainfallData()
            wx.MessageBox("RBFNプログラム用の入力データを自動作成しました。\n引き続き、RBFNプログラムを起動し、RBFN値を算出して下さい。", g_System_Title)

    def _click_button_11_2(self, event):
        global g_System_Title


        self.g_button_13_1 = wx.Button(self.g_panel_13, wx.ID_ANY, "処理開始(等高線)", size=(100, 25))
        self.g_button_13_2 = wx.Button(self.g_panel_13, wx.ID_ANY, "処理開始(集計)", size=(100, 25))
        self.g_button_13_3 = wx.Button(self.g_panel_13, wx.ID_ANY, "条件設定", size=(73, 25))
        self.g_button_13_4 = wx.Button(self.g_panel_13, wx.ID_ANY, "下限値・上限値再計算", size=(130, 25))

    def _click_button_13_1(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■RBFN出力値の抽出処理")
        self._set_listBox_13_1_year()

        if (wx.MessageBox("RBFN出力値の抽出処理を行い、等高線データを作成します。\nよろしいですか？", g_System_Title, wx.YES_NO) == wx.YES):
            self._makeContour()
            wx.MessageBox("RBFN出力値からの等高線作成が完了しました。", g_System_Title)

    def _click_button_13_2(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■RBFN出力値の抽出処理")
        self._set_listBox_13_2_year()

        if (wx.MessageBox("RBFN出力値の抽出処理を行い、集計処理を行います。\nよろしいですか？", g_System_Title, wx.YES_NO) == wx.YES):
            self._makeFigure()
            wx.MessageBox("RBFN出力値からの集計処理が完了しました。", g_System_Title)


    def _click_button_13_3(self, event):
        global g_System_Title

    def _click_button_13_4(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■RBFN出力値の抽出処理")
        self._set_listBox_13_2_year()

        if (wx.MessageBox("ファイル内で指定された土壌雨量指数の下限値、60分積算雨量の上限値で再集計を行いますか？\n集計には時間がかかります。", g_System_Title, wx.YES_NO) == wx.YES):
            self._recalcLimit()
            wx.MessageBox("土壌雨量指数の下限値、60分積算雨量の上限値の設定による再集計が完了しました。", g_System_Title)

    # メニュークリックイベント処理
    def _click_menu_bar(self, event):

        event_id = event.GetId()
        print(event_id)
        if event_id == 11:
            self._hide_Panel()
            # RBFNプログラム用入力データ
            self._set_title("■RBFNプログラム用入力データ作成")
            self.g_panel_11.Show()
        elif event_id == 12:
            # RBFNプログラムの起動
            check_call([".\\bin\\RBFN.exe"])
        elif event_id == 13:
            self._hide_Panel()
            # RBFN出力値の抽出処理
            self._set_title("■RBFN出力値の抽出処理")
            self.g_panel_13.Show()
        elif event_id == 21:
            self._hide_Panel()
            # RBFN補正の結果
            self._set_title("■RBFN補正の結果")
            self.g_panel_21.Show()
        elif event_id == 22:
            self._hide_Panel()
            # 集計結果
            self._set_title("■集計結果")
            self.g_panel_22.Show()
        elif event_id == 23:
            self._hide_Panel()
            # ブロック集計
            self._set_title("■ブロック集計")
            self.g_panel_23.Show()

    def _get_environ(self):
        global com
        global g_ini_path
        global g_meshSum_target
        global g_meshSum_all
        global g_meshList
        global g_meshList2

        com.GetEnvData(g_ini_path)
        #com.Store_DisasterFile()
        com.g_textSum_DisasterFile = com.Store_DataFile(com.g_DisasterFileName, com.g_textline_DisasterFile)
        #com.Store_CautionAnnounceFile()
        com.g_textSum_CautionAnnounceFile = com.Store_DataFile(com.g_CautionAnnounceFileName, com.g_textline_CautionAnnounceFile)
        # 集計
        # 解析雨量のCSVファイルからメッシュ数を取得する。
        del g_meshList[:]
        del g_meshList2[:]

        if com.g_TargetMeshFile != "":
            g_meshSum_target = com.GetMeshSumFromFile(com.g_TargetStartYear, g_meshList)
            #g_meshSum = com.GetMeshSumFromFile2(com.g_TargetStartYear, g_meshList2)
        else:
            a_RainfallFileName = com.g_OutPath + "\\" + com.g_RainfallFileSId + str(com.g_TargetMeshFile) + com.g_RainfallFileEId
            g_meshSum_target = com.GetMeshSum(com.g_TargetStartYear, a_RainfallFileName, g_meshList)
            #g_meshSum = com.GetMeshSum(com.g_TargetStartYear, a_RainfallFileName, g_meshList2)
        g_meshSum_all = com.GetMeshList(com.g_TargetStartYear, g_meshList2)

        print(g_meshList)
        print(g_meshList2)

    # フレームのリサイズイベント処理
    def _get_frame(self, event):

        size = self.GetSize()

        # RBFNプログラム用入力データ
        self.g_panel_11.SetSize(size)
        self.g_button_11_1.SetPosition(wx.Point(size.width - (250 - 75), 8))
        pos = self.g_button_11_1.GetPosition()
        self.g_button_11_2.SetPosition(wx.Point(size.width - (250 - 75*2 - 4), 8))
        self.g_listBox_11.SetSize(size.width - 24, size.height - (50 + 60))

        # RBFN出力値の抽出処理
        self.g_panel_13.SetSize(size)
        self.g_button_13_1.SetPosition(wx.Point(size.width - (540 - 100), 8))
        self.g_button_13_2.SetPosition(wx.Point(size.width - (540 - 100*2 - 4), 8))
        self.g_button_13_3.SetPosition(wx.Point(size.width - (540 - 100*3 - 4*2), 8))
        self.g_button_13_4.SetPosition(wx.Point(size.width - (540 - 100*3 - 75 - 4*3), 8))
        self.g_listBox_13_2.SetSize(size.width - 24, 340)
        self.g_listBox_13_2.SetPosition(wx.Point(4, size.height - 340))
        self.g_listBox_13_1.SetSize(size.width - 24, size.height - (50) - 340)

        # RBFN補正の結果

        # 集計結果

        # ブロック集計


    # パネルの全非表示
    def _hide_Panel(self):
        #self.lblTitle.SetLabel("")

        self.g_panel_11.Hide()
        #self.g_panel_12.Hide()
        self.g_panel_13.Hide()
        self.g_panel_21.Hide()
        self.g_panel_22.Hide()
        self.g_panel_23.Hide()

    def _makeAlarmAnnounce(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeAlarmAnnounce(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeAllRainfallData(self):
        global com
        global g_meshList

        # RBFNデータ入力

        for a_year in range(com.g_TargetStartYear, com.g_TargetStartYear + 2):
        #for a_year in range(com.g_TargetStartYear, com.g_TargetEndYear + 1):
            print('***a_year=' + str(a_year))

            ''' testing...
            self.g_listBox_11.InsertItem(0, str(a_year))
            self.g_listBox_11.SetItem(0, 1, str(0 + 1) + "/" + str(1))
            self.g_listBox_11.SetItem(0, 2, '')
            self.g_listBox_11.SetItem(0, 3, "処理中......")
            self.g_listBox_11.SetItemTextColour(0, wx.RED)
            self.g_listBox_11.Update()
            '''

            a_RainfallFileName = com.g_OutPath + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
            a_SoilRainFileName = com.g_OutPath + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId

            # 予測的中率
            a_RainfallFileName1 = com.g_OutPathReal + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
            a_SoilRainFileName1 = com.g_OutPathReal + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId

            a_TemperatureFileName = com.g_OutPath + "\\" + com.g_TemperatureFileSId + str(a_year) + com.g_TemperatureFileEId
            com.g_textSum_TemperatureFile = com.Store_DataFile(a_TemperatureFileName, com.g_textline_TemperatureFile)

            #print(prv_RainfallFileName)
            #com.Store_RainfallFile(prv_RainfallFileName)
            com.g_textSum_RainfallFile = com.Store_DataFile(a_RainfallFileName, com.g_textline_RainfallFile)
            #com.Store_SoilRainFile(prv_SoilRainFileName)
            com.g_textSum_SoilRainFile = com.Store_DataFile(a_SoilRainFileName, com.g_textline_SoilRainFile)
            if com.g_RainKind != 0:
                #com.Store_RainfallFile1(prv_RainfallFileName1)
                com.g_textSum_RainfallFile1 = com.Store_DataFile(a_RainfallFileName1, com.g_textline_RainfallFile1)
                #com.Store_SoilRainFile1(prv_SoilRainFileName1)
                com.g_textSum_SoilRainFile1 = com.Store_DataFile(a_SoilRainFileName1, com.g_textline_SoilRainFile1)

            a_meshSum = len(g_meshList)

            ''' testing...
            self.g_listBox_11.SetItem(0, 3, "入力データ作成が完了しました。")
            self.g_listBox_11.Refresh(0)
            return
            '''

            a_sum = 0
            a_count = self.g_listBox_11.GetItemCount()
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + 1)
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

                    self.g_listBox_11.InsertItem(a_count + a_sum, str(a_year))
                    self.g_listBox_11.SetItem(a_count + a_sum, 1, str(a_sum + 1) + "/" + str(a_meshSum))
                    self.g_listBox_11.SetItem(a_count + a_sum, 2, a_meshNo)
                    self.g_listBox_11.SetItem(a_count + a_sum, 3, "処理中......")
                    self.g_listBox_11.SetItemTextColour(a_count + a_sum, wx.RED)
                    self.g_listBox_11.Update()

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

                for a_i in range(a_sum, a_cnt_max):
                    self.g_listBox_11.SetItem(a_count + a_sum , 3, "入力データ作成が完了しました。")
                    self.g_listBox_11.SetItemTextColour(a_count + a_sum, wx.BLUE)
                    self.g_listBox_11.Update()

                print('All process is ended.')

                a_sum = a_cnt_max

    def _makeCautionAnnounceFrequencyOverOccurRainFallNum(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeCautionAnnounceFrequencyOverOccurRainFallNum(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeCautionAnnounceRateOccurNum(self):
        global com
        global g_meshList

        a_proc = clsFigure.MakeCautionAnnounceRateOccurNum(
            0,
            com.g_strIni,
            g_meshList,
            0,
            -1
        )

    def _makeCautionAnnounceRateOccurRainFallNum(self, ):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeCautionAnnounceRateOccurRainFallNum(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeContour(self):
        print('aa')

    def _makeDisasterSupplement(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeDisasterSupplement(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeDisasterSupplement9_1(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeDisasterSupplement9_1(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeDisasterSupplement9_2(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeDisasterSupplement9_2(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeFigure(self):
        self.g_listBox_13_2.SetItem(0, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(0, wx.RED)
        self.g_listBox_13_2.Update()
        # 全降雨の超過数
        # 非発生降雨の超過数
        # 発生降雨の超過数
        #_makeOverRainfall()
        #_makeOverRainfallMix()
        self.g_listBox_13_2.SetItem(0, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(0, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(1, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(1, wx.RED)
        self.g_listBox_13_2.Update()
        #災害捕捉率
        self._makeDisasterSupplement()
        self.g_listBox_13_2.SetItem(1, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(1, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(2, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(2, wx.RED)
        self.g_listBox_13_2.Update()
        # 空振り率
        self._makeWiff()
        # 空振り率2
        self._makeWiff_New()
        self.g_listBox_13_2.SetItem(2, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(2, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(3, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(3, wx.RED)
        self.g_listBox_13_2.Update()
        # 空振り頻度
        self._makeWhiffFrequency()
        # 空振り頻度2
        self._makeWhiffFrequency_New()
        self.g_listBox_13_2.SetItem(3, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(3, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(4, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(4, wx.RED)
        self.g_listBox_13_2.Update()
        # 空振り時間
        self._makeWhiffTime()
        self.g_listBox_13_2.SetItem(4, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(4, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(5, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(5, wx.RED)
        self.g_listBox_13_2.Update()
        # 警報発表頻度
        self._makeAlarmAnnounce()
        self.g_listBox_13_2.SetItem(5, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(5, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(6, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(6, wx.RED)
        self.g_listBox_13_2.Update()
        # 9)実質災害捕捉率
        # 災害捕捉率【降雨数】
        self._makeDisasterSupplement9_1()
        # 災害捕捉率【件数】
        self._makeDisasterSupplement9_2()
        self.g_listBox_13_2.SetItem(6, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(6, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(7, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(7, wx.RED)
        self.g_listBox_13_2.Update()
        # ④実質災害捕捉率
        # 年毎メッシュ単位の算出結果
        self._makeOverRainfall2()
        # 警戒発表中災害発生件数
        # 警戒発表中災害発生降雨数
        self._makeOverRainfallMix2()

        # 土砂災害警戒情報の災害捕捉率（降雨数）
        self._makeCautionAnnounceRateOccurRainFallNum()
        # 土砂災害警戒情報の災害捕捉率（件数）
        self._makeCautionAnnounceRateOccurNum()
        self.g_listBox_13_2.SetItem(7, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(7, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(8, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(8, wx.RED)
        self.g_listBox_13_2.Update()
        # ②土砂災害警戒情報のリードタイム
        self._makeOverRainfall3_1()
        self._makeOverRainfallMix3_1()
        self.g_listBox_13_2.SetItem(8, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(8, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(9, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(9, wx.RED)
        self.g_listBox_13_2.Update()
        # ③土砂災害警戒情報の発表頻度
        self._makeCautionAnnounceFrequencyOverOccurRainFallNum()
        self.g_listBox_13_2.SetItem(9, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(9, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(10, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(10, wx.RED)
        self.g_listBox_13_2.Update()
        # ⑥RBFN越のリードタイム
        self._makeOverRainfall3_2()
        self._makeOverRainfallMix3_2()
        self.g_listBox_13_2.SetItem(10, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(10, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(11, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(11, wx.RED)
        self.g_listBox_13_2.Update()
        # ⑧予測適中率
        if (com.g_RainKind != 0):
            self._makeOverRainfall8()
            self._makeOverRainfallMix8()
            self._makeForecastPredictive()
        self.g_listBox_13_2.SetItem(11, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(11, wx.BLUE)
        self.g_listBox_13_2.Update()

        self.g_listBox_13_2.SetItem(12, 3, "処理中......")
        self.g_listBox_13_2.SetItemTextColour(12, wx.RED)
        self.g_listBox_13_2.Update()
        # ⑨NIGeDaS、NIGeDaSⅡ
        self._makeNIGeDaS()
        self._makeNIGeDaS_NonOccurCalc()
        self.g_listBox_13_2.SetItem(12, 3, "集計処理が完了しました。")
        self.g_listBox_13_2.SetItemTextColour(12, wx.BLUE)
        self.g_listBox_13_2.Update()

    def _makeForecastPredictive(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeForecastPredictive(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeNIGeDaS(self):
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

    def _makeNIGeDaS_NonOccurCalc(self):
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

    def _makeOverRainfall(self):
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

    def _makeOverRainfall2(self):
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

    def _makeOverRainfall3_1(self):
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

    def _makeOverRainfall3_2(self):
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

    def _makeOverRainfall8(self):
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

    def _makeOverRainfallMix(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeOverRainfallMix(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeOverRainfallMix2(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeOverRainfallMix2(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeOverRainfallMix3_1(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeOverRainfallMix3_1(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeOverRainfallMix3_2(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeOverRainfallMix3_2(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeOverRainfallMix8(self):
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

    def _makeWiff(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeWhiff(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeWiff_New(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeWhiff_New(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeWhiffFrequency(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeWhiffFrequency(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeWhiffFrequency_New(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeWhiffFrequency_New(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )

    def _makeWhiffTime(self):
        global com
        global g_meshList2

        a_proc = clsFigure.MakeWhiffTime(
            0,
            com.g_strIni,
            g_meshList2,
            0,
            -1
        )


    # RBFNプログラム用入力データ
    def _makePanel_11(self):

        self.g_panel_11 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))

        self.g_button_11_1 = wx.Button(self.g_panel_11, wx.ID_ANY, "処理開始", size=(73, 25))
        self.g_button_11_2 = wx.Button(self.g_panel_11, wx.ID_ANY, "条件設定", size=(73, 25))
        self.g_button_11_1.Bind(wx.EVT_BUTTON, self._click_button_11_1)
        self.g_button_11_2.Bind(wx.EVT_BUTTON, self._click_button_11_2)

        self.g_listBox_11 = wx.ListCtrl(self.g_panel_11, wx.ID_ANY, style=wx.LC_REPORT)
        #listmix.TextEditMixin(self.g_listBox_11)
        self.g_listBox_11.InsertColumn(0, "処理年", width=100)
        self.g_listBox_11.InsertColumn(1, "メッシュ数", width=100)
        self.g_listBox_11.InsertColumn(2, "メッシュ番号", width=150)
        self.g_listBox_11.InsertColumn(3, "状態", width=500)
        self.g_listBox_11.SetPosition(wx.Point(4, 50))

    # RBFN出力値の抽出処理
    def _makePanel_13(self):
        self.g_panel_13 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))

        self.g_button_13_1 = wx.Button(self.g_panel_13, wx.ID_ANY, "処理開始(等高線)", size=(100, 25))
        self.g_button_13_2 = wx.Button(self.g_panel_13, wx.ID_ANY, "処理開始(集計)", size=(100, 25))
        self.g_button_13_3 = wx.Button(self.g_panel_13, wx.ID_ANY, "条件設定", size=(73, 25))
        self.g_button_13_4 = wx.Button(self.g_panel_13, wx.ID_ANY, "下限値・上限値再計算", size=(130, 25))
        self.g_button_13_1.Bind(wx.EVT_BUTTON, self._click_button_13_1)
        self.g_button_13_2.Bind(wx.EVT_BUTTON, self._click_button_13_2)
        self.g_button_13_3.Bind(wx.EVT_BUTTON, self._click_button_13_3)
        self.g_button_13_4.Bind(wx.EVT_BUTTON, self._click_button_13_4)

        ########################################################################
        # 等高線
        ########################################################################
        self.g_listBox_13_1 = wx.ListCtrl(self.g_panel_13, wx.ID_ANY, style=wx.LC_REPORT)
        self.g_listBox_13_1.InsertColumn(0, "対象メッシュ番号", width=150)
        self.g_listBox_13_1.InsertColumn(1, "開始年", width=100)
        self.g_listBox_13_1.InsertColumn(2, "終了年", width=100)
        self.g_listBox_13_1.InsertColumn(3, "状態", width=500)
        self.g_listBox_13_1.SetPosition(wx.Point(4, 50))

        self._set_listBox_13_1_year()

        ########################################################################
        # 集計
        ########################################################################
        self.g_listBox_13_2 = wx.ListCtrl(self.g_panel_13, wx.ID_ANY, style=wx.LC_REPORT)
        self.g_listBox_13_2.InsertColumn(0, "集計処理", width=200)
        self.g_listBox_13_2.InsertColumn(1, "開始年", width=100)
        self.g_listBox_13_2.InsertColumn(2, "終了年", width=100)
        self.g_listBox_13_2.InsertColumn(3, "状態", width=500)

        statistics = [("降雨の超過数", "", "", "待機中"),
                      ("災害捕捉率", "", "", "待機中"),
                      ("空振り率", "", "", "待機中"),
                      ("空振り頻度", "", "", "待機中"),
                      ("空振り時間", "", "", "待機中"),
                      ("警報発表頻度", "", "", "待機中"),
                      ("実質災害捕捉率", "", "", "待機中"),
                      ("警戒情報の災害捕捉率", "", "", "待機中"),
                      ("警戒情報のリードタイム", "", "", "待機中"),
                      ("警戒情報の発表頻度", "", "", "待機中"),
                      ("RBFN越のリードタイム", "", "", "待機中"),
                      ("予測適中率", "", "", "待機中"),
                      ("NIGeDaS", "", "", "待機中")
                      ]
        i = 0
        for s in statistics:
            self.g_listBox_13_2.InsertItem(i, s[0])
            self.g_listBox_13_2.SetItem(i, 1, s[1])
            self.g_listBox_13_2.SetItem(i, 2, s[2])
            self.g_listBox_13_2.SetItem(i, 3, s[3])
            self.g_listBox_13_2.SetItemTextColour(i, wx.GREEN)
            i += 1

        self._set_listBox_13_2_year()

    # RBFN補正の結果
    def _makePanel_21(self):

        self.g_panel_21 = wx.Panel(self, wx.ID_ANY)

    # 集計結果
    def _makePanel_22(self):

        self.g_panel_22 = wx.Panel(self, wx.ID_ANY)

    # ブロック集計
    def _makePanel_23(self):

        self.g_panel_23 = wx.Panel(self, wx.ID_ANY)

    def _recalcLimit(self):
        Call GetRecalcLimitData(Me, a_strTmp, a_soilMin, a_rainMax)
        Call RecalcLimitByMesh(Me, Me.Picture1, Me.Picture2, a_sTFolder, a_soilMin, a_rainMax, 1, a_meshList2)

    def _set_listBox_13_1_year(self):
        global g_meshSum_all
        global g_meshList2

        if (self.g_listBox_13_1.GetItemCount() > 0):
            self.g_listBox_13_1.DeleteAllItems()

        for a_cnt in range(0, g_meshSum_all):
            self.g_listBox_13_1.InsertItem(a_cnt, g_meshList2[a_cnt])
            self.g_listBox_13_1.SetItem(a_cnt, 1, str(com.g_TargetStartYear))
            self.g_listBox_13_1.SetItem(a_cnt, 2, str(com.g_TargetEndYear))
            self.g_listBox_13_1.SetItem(a_cnt, 3, "待機中")
            self.g_listBox_13_1.SetItemTextColour(a_cnt, wx.GREEN)
        self.g_listBox_13_1.Update()

    def _set_listBox_13_2_year(self):
        a_size = self.g_listBox_13_2.GetItemCount()
        for a_i in range(0, a_size):
            self.g_listBox_13_2.SetItem(a_i, 1, str(com.g_TargetStartYear))
            self.g_listBox_13_2.SetItem(a_i, 2, str(com.g_TargetEndYear))
            self.g_listBox_13_2.SetItem(a_i, 3, "待機中")
            self.g_listBox_13_2.SetItemTextColour(a_i, wx.GREEN)
        self.g_listBox_13_2.Update()

    def _set_title(self, h_title):
        a_Temperature = ""

        if (com.g_TemperatureKind == 1):
            # 平均気温
            a_Temperature += "平均気温で算出"
        elif (com.g_TemperatureKind == 2):
            # 最高気温
            a_Temperature += "最高気温で算出"
        else:
            a_Temperature += "なし"

        if (com.g_TemperatureKind == 1) or (com.g_TemperatureKind == 2):
            # 平均気温
            a_Temperature += "　(" + str(com.g_TemperatureMin) + "℃～" + str(com.g_TemperatureMax) + ")"

        self.lblTitle.SetLabel("　" + h_title +
                               "\n　　対象年：" + str(com.g_TargetStartYear) + "年～" + str(com.g_TargetEndYear) + "年" +
                               "\n　　気温情報：" + a_Temperature)

def main():
    app = wx.App()
    Main(None, wx.ID_ANY, "RBFN修正ツール Ver3.0")
    app.MainLoop()

if __name__ == "__main__":
    main()