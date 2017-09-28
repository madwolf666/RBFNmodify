import sys
import wx
from subprocess import check_call

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

    # メニュークリックイベント処理
    def _click_menu_bar(self, event):
        global g_panel_11
        global g_panel_12
        global g_panel_13
        global g_panel_21
        global g_panel_22
        global g_panel_23

        event_id = event.GetId()
        print(event_id)
        if event_id == 11:
            self._hide_Panel()
            # RBFNプログラム用入力データ
            self.lblTitle.SetLabel("■RBFNプログラム用入力データ作成\n　対象年：\n　気温情報：")
            g_panel_11.Show()
        elif event_id == 12:
            # RBFNプログラムの起動
            check_call([".\\bin\\RBFN.exe"])
        elif event_id == 13:
            self._hide_Panel()
            # RBFN出力値の抽出処理
            self.lblTitle.SetLabel("■RBFN出力値の抽出処理\n　対象年：\n　気温情報：")
            g_panel_13.Show()
        elif event_id == 21:
            self._hide_Panel()
            # RBFN補正の結果
            self.lblTitle.SetLabel("■RBFN補正の結果\n　対象年：\n　気温情報：")
            g_panel_21.Show()
        elif event_id == 22:
            self._hide_Panel()
            # 集計結果
            self.lblTitle.SetLabel("■集計結果\n　対象年：\n　気温情報：")
            g_panel_22.Show()
        elif event_id == 23:
            self._hide_Panel()
            # ブロック集計
            self.lblTitle.SetLabel("■ブロック集計\n　対象年：\n　気温情報：")
            g_panel_23.Show()

    # フレームのリサイズイベント処理
    def _get_frame(self, event):
        global g_panel_11
        global g_panel_12
        global g_panel_13
        global g_panel_21
        global g_panel_22
        global g_panel_23

        global g_button_11_1
        global g_button_11_2
        global g_listBox_11

        global g_button_13_1
        global g_button_13_2
        global g_button_13_3
        global g_button_13_4
        global g_listBox_13_1
        global g_listBox_13_2

        size = self.GetSize()

        # RBFNプログラム用入力データ
        g_panel_11.SetSize(size)
        g_button_11_1.SetPosition(wx.Point(size.width - (250 - 75), 8))
        pos = g_button_11_1.GetPosition()
        g_button_11_2.SetPosition(wx.Point(size.width - (250 - 75*2 - 4), 8))
        g_listBox_11.SetSize(size.width - 24, size.height - (50 + 60))

        # RBFN出力値の抽出処理
        g_panel_13.SetSize(size)
        g_button_13_1.SetPosition(wx.Point(size.width - (540 - 100), 8))
        g_button_13_2.SetPosition(wx.Point(size.width - (540 - 100*2 - 4), 8))
        g_button_13_3.SetPosition(wx.Point(size.width - (540 - 100*3 - 4*2), 8))
        g_button_13_4.SetPosition(wx.Point(size.width - (540 - 100*3 - 75 - 4*3), 8))
        g_listBox_13_2.SetSize(size.width - 24, 340)
        g_listBox_13_2.SetPosition(wx.Point(4, size.height - 340))
        g_listBox_13_1.SetSize(size.width - 24, size.height - (50) - 340)

        # RBFN補正の結果

        # 集計結果

        # ブロック集計

    # パネルの全非表示
    def _hide_Panel(self):
        #self.lblTitle.SetLabel("")
        global g_panel_11
        global g_panel_12
        global g_panel_13
        global g_panel_21
        global g_panel_22
        global g_panel_23

        g_panel_11.Hide()
        #g_panel_12.Hide()
        g_panel_13.Hide()
        g_panel_21.Hide()
        g_panel_22.Hide()
        g_panel_23.Hide()

    # RBFNプログラム用入力データ
    def _makePanel_11(self):
        global g_panel_11
        global g_button_11_1
        global g_button_11_2
        global g_listBox_11

        g_panel_11 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))
        #g_panel_11.SetBackgroundColour("#00FFFF")

        g_button_11_1 = wx.Button(g_panel_11, wx.ID_ANY, "処理開始", size=(73, 25))
        g_button_11_2 = wx.Button(g_panel_11, wx.ID_ANY, "条件設定", size=(73, 25))

        g_listBox_11 = wx.ListCtrl(g_panel_11, wx.ID_ANY, style=wx.LC_REPORT)
        g_listBox_11.InsertColumn(0, "処理年", width=100)
        g_listBox_11.InsertColumn(1, "メッシュ数", width=100)
        g_listBox_11.InsertColumn(2, "メッシュ番号", width=150)
        g_listBox_11.InsertColumn(3, "状態", width=500)
        g_listBox_11.SetPosition(wx.Point(4, 50))

    # RBFN出力値の抽出処理
    def _makePanel_13(self):
        global g_panel_13
        global g_button_13_1
        global g_button_13_2
        global g_button_13_3
        global g_button_13_4
        global g_listBox_13_1
        global g_listBox_13_2

        g_panel_13 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))

        g_button_13_1 = wx.Button(g_panel_13, wx.ID_ANY, "処理開始(等高線)", size=(100, 25))
        g_button_13_2 = wx.Button(g_panel_13, wx.ID_ANY, "処理開始(集計)", size=(100, 25))
        g_button_13_3 = wx.Button(g_panel_13, wx.ID_ANY, "条件設定", size=(73, 25))
        g_button_13_4 = wx.Button(g_panel_13, wx.ID_ANY, "下限値・上限値再計算", size=(130, 25))

        g_listBox_13_1 = wx.ListCtrl(g_panel_13, wx.ID_ANY, style=wx.LC_REPORT)
        g_listBox_13_1.InsertColumn(0, "対象メッシュ番号", width=150)
        g_listBox_13_1.InsertColumn(1, "開始年", width=100)
        g_listBox_13_1.InsertColumn(2, "終了年", width=100)
        g_listBox_13_1.InsertColumn(3, "状態", width=500)
        g_listBox_13_1.SetPosition(wx.Point(4, 50))

        g_listBox_13_2 = wx.ListCtrl(g_panel_13, wx.ID_ANY, style=wx.LC_REPORT)
        g_listBox_13_2.InsertColumn(0, "集計処理", width=300)
        g_listBox_13_2.InsertColumn(1, "開始年", width=100)
        g_listBox_13_2.InsertColumn(2, "終了年", width=100)
        g_listBox_13_2.InsertColumn(3, "状態", width=500)

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
            g_listBox_13_2.InsertItem(i, s[0])
            g_listBox_13_2.SetItem(i, 1, s[1])
            g_listBox_13_2.SetItem(i, 2, s[2])
            g_listBox_13_2.SetItem(i, 3, s[3])
            item = g_listBox_13_2.GetItem(i, 3)
            item.SetTextColour(wx.GREEN)
            item.SetText("chappy")
            #item.SetTextColour(wx.Colour("#00FF00"))
            #g_listBox_13_2.SetItemTextColour(item, wx.GREEN)
            i += 1

        #g_listBox_13_2.SetPosition(wx.Point(4, 50))

    # RBFN補正の結果
    def _makePanel_21(self):
        global g_panel_21

        g_panel_21 = wx.Panel(self, wx.ID_ANY)

    # 集計結果
    def _makePanel_22(self):
        global g_panel_22

        g_panel_22 = wx.Panel(self, wx.ID_ANY)

    # ブロック集計
    def _makePanel_23(self):
        global g_panel_23

        g_panel_23 = wx.Panel(self, wx.ID_ANY)

def main():
    app = wx.App()
    Main(None, wx.ID_ANY, "RBFN修正ツール Ver3.0")
    app.MainLoop()

if __name__ == "__main__":
    main()