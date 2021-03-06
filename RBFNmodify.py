#import mmap
import os
import sys
import wx
import wx.lib.mixins.listctrl as listmix
#from PIL import Image
from subprocess import check_call
import multiprocessing
from multiprocessing import sharedctypes
#from multiprocessing.sharedctypes import synchronized
#from multiprocessing import Process, Value, Array  #Manager
import threading
import time
import gc
from ctypes import *
from ctypes import wintypes

import com_functions
import clsRainfall_gen as clsRainfall
#pandasの処理は遅い
#import clsRainfall_pandas as clsRainfall
import clsContour_w32 as clsContour
#import clsContour_pil as clsContour
#OpenCVの機能には制限がかなりある
#import clsContour_cv2 as clsContour
import clsFigure
import clsBlock

com = com_functions.ComFunctions()

#g_ini_path = "C:\\Users\\hal\\Documents\\CTI\\東京\\RBFN修正ツール\\2015年度\\program-source\\bin\\rbfnmdf.ini"
g_ini_path = ".\\rbfnmdf.ini"
g_System_Title = "RBFN修正ツール Ver 3.0"
g_meshSum_target = 0
g_meshSum_list = 0
g_meshList_check = 0
g_meshList_target = []
g_meshList_list = []
g_meshList_check = []

def Testing(
        h_m
):
    try:
        #a_aaa = h_DisasterFile
        print(h_m)
        #h_DisasterFile.value = 666
    except Exception as exp:
        a_strErr = " ".join(map(str, exp.args))
    except:
        a_strErr = sys.exc_info()

def SetText_ListBox(
    h_self,
    h_listBox,
    h_row,
    h_col,
    h_msg
):
    try:
        h_listBox.SetItem(h_row , h_col, h_msg)
        h_listBox.SetItemTextColour(h_row, wx.BLUE)
        h_listBox.Refresh(True)
        h_listBox.Update()
        h_self.Refresh()
        h_self.Update()
    except Exception as exp:
        a_strErr = " ".join(map(str, exp.args))
    except:
        a_strErr = sys.exc_info()

class CheckBoxList(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

    def OnCheckItem(self, index, flag):
        global g_meshList_check

        print(index, flag, self.GetItemText(index, 0))
        if (flag == True):
            g_meshList_check.append([index, self.GetItemText(index, 0)])
        else:
            for a_check in g_meshList_check:
                #print(a_check)
                #print(a_check[0])
                if (a_check[0] == index):
                    g_meshList_check.remove(a_check)

        #print(g_meshList_check)

class Main(wx.Frame):
    g_menu_bar = None

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

    g_bitmap = None

    def __init__(self, parent, id, title):
        """ レイアウトの作成 """
        wx.Frame.__init__(self, parent, id, title)

        self.SetSize(size=(1024, 768))
        self.g_icon = wx.Icon(".\\images\\RBFNmodify.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.g_icon)
        self.SetBackgroundColour("#696969")
        self.lblTitle = wx.StaticText(self, wx.ID_ANY, "")
        self.lblTitle.SetForegroundColour("#FFFF00")

        self._get_environ()

        panel = wx.Panel(self, wx.ID_ANY)

        ################################################################################
        # メニューバー
        ################################################################################
        self.g_menu_bar = wx.MenuBar()

        #自動生成
        mnu_MakeAuto = wx.Menu()
        mnu_MakeAuto.Append(11, "RBFNプログラム用入力データ")
        mnu_MakeAuto.Append(12, "RBFNプログラムの起動")
        mnu_MakeAuto.Append(13, "RBFN出力値の抽出処理")
        self.g_menu_bar.Append(mnu_MakeAuto, "自動生成")
        self.SetMenuBar(self.g_menu_bar)

        #結果表示
        mnu_DispResult = wx.Menu()
        mnu_DispResult.Append(21, "RBFN補正の結果")
        mnu_DispResult.Append(22, "集計結果")
        mnu_DispResult.Append(23, "ブロック集計")
        self.g_menu_bar.Append(mnu_DispResult, "結果表示")
        self.SetMenuBar(self.g_menu_bar)

        #終了
        '''
        mnu_Exit = wx.Menu()
        self.menu_bar.Append(mnu_Exit, "終了")
        self.SetMenuBar(self.menu_bar)
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

        self.Bind(wx.EVT_PAINT, self._onPaint)
        self.Bind(wx.EVT_SIZE, self._get_frame)
        self.Bind(wx.EVT_CLOSE, self._onClose)

        self.Maximize()
        self.Show(True)

        #共有メモリ
        self.g_shmlib = windll.LoadLibrary(".\\bin\\rbfnshmctl.dll")
        self.PyShmMapCreate = self.g_shmlib.PyShmMapCreate
        self.PyShmMapCreate.argtypes = [c_char_p, c_char_p, c_void_p, c_void_p, c_void_p, c_void_p]
        self.PyShmMapCreate.restype = c_int
        self.PyShmMapRead = self.g_shmlib.PyShmMapRead
        self.PyShmMapRead.argtypes = [c_char_p, c_void_p, c_void_p, c_void_p]
        self.PyShmMapRead.restype = c_char_p
        self.PyShmMapClose = self.g_shmlib.PyShmMapClose
        self.PyShmMapClose.argtypes = [c_void_p, c_void_p, c_void_p]
        self.PyShmMapClose.restype = c_int


    def _click_button_11_1(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■RBFNプログラム用入力データ作成")

        if (wx.MessageBox("RBFNプログラム用の入力データを自動作成します。\nよろしいですか？", g_System_Title, wx.YES_NO) == wx.YES):
            self._enable_MenuBar(False)
            self.g_button_11_1.Enabled = False
            self.g_button_11_2.Enabled = False
            #self._makeAllRainfallData()
            self._makeAllRainfallData_proc()
            wx.MessageBox("RBFNプログラム用の入力データを自動作成しました。\n引き続き、RBFNプログラムを起動し、RBFN値を算出して下さい。", g_System_Title)
            self._enable_MenuBar(True)
            self.g_menu_bar.Enabled = True
            self.g_button_11_1.Enabled = True
            self.g_button_11_2.Enabled = True

    def _click_button_11_2(self, event):
        global g_System_Title

        self.g_button_13_1 = wx.Button(self.g_panel_13, wx.ID_ANY, "処理開始(等高線)", size=(100, 25))
        self.g_button_13_2 = wx.Button(self.g_panel_13, wx.ID_ANY, "処理開始(集計)", size=(100, 25))
        self.g_button_13_3 = wx.Button(self.g_panel_13, wx.ID_ANY, "条件設定", size=(73, 25))
        self.g_button_13_4 = wx.Button(self.g_panel_13, wx.ID_ANY, "下限値・上限値再計算", size=(130, 25))

    def _click_button_13_1(self, event):
        global g_System_Title
        global g_meshList_check

        self._get_environ()
        self._set_title("■RBFN出力値の抽出処理")
        #self._set_listBox_13_1_year()


        a_sum = len(g_meshList_check)
        if (a_sum <=0 ):
            wx.MessageBox("メッシュ番号が一つも選択されていません！", g_System_Title)
            return

        if (wx.MessageBox("RBFN出力値の抽出処理を行い、等高線データを作成します。\nよろしいですか？", g_System_Title, wx.YES_NO) == wx.YES):
            self._enable_MenuBar(False)
            self.g_button_13_1.Enabled = False
            self.g_button_13_2.Enabled = False
            self.g_button_13_3.Enabled = False
            self.g_button_13_4.Enabled = False
            #self._makeContour()
            self._makeContour_proc()
            wx.MessageBox("RBFN出力値からの等高線作成が完了しました。", g_System_Title)
            self._enable_MenuBar(True)
            self.g_button_13_1.Enabled = True
            self.g_button_13_2.Enabled = True
            self.g_button_13_3.Enabled = True
            self.g_button_13_4.Enabled = True

    def _click_button_13_2(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■RBFN出力値の抽出処理")
        self._set_listBox_13_2_year()

        if (wx.MessageBox("RBFN出力値の抽出処理を行い、集計処理を行います。\nよろしいですか？", g_System_Title, wx.YES_NO) == wx.YES):
            self._enable_MenuBar(False)
            self.g_button_13_1.Enabled = False
            self.g_button_13_2.Enabled = False
            self.g_button_13_3.Enabled = False
            self.g_button_13_4.Enabled = False
            self._makeFigure()
            wx.MessageBox("RBFN出力値からの集計処理が完了しました。", g_System_Title)
            self._enable_MenuBar(True)
            self.g_button_13_1.Enabled = True
            self.g_button_13_2.Enabled = True
            self.g_button_13_3.Enabled = True
            self.g_button_13_4.Enabled = True

    def _click_button_13_3(self, event):
        global g_System_Title

    def _click_button_13_4(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■RBFN出力値の抽出処理")
        #self._set_listBox_13_2_year()

        if (wx.MessageBox("ファイル内で指定された土壌雨量指数の下限値、60分積算雨量の上限値で再集計を行いますか？\n集計には時間がかかります。", g_System_Title, wx.YES_NO) == wx.YES):
            self._recalcLimit()
            wx.MessageBox("土壌雨量指数の下限値、60分積算雨量の上限値の設定による再集計が完了しました。", g_System_Title)

    def _click_button_21_1(self, event):
        global g_System_Title

    def _click_button_21_2(self, event):
        global g_System_Title

    def _click_button_22_1(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　全降雨の超過数"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_OverAllRainFallNumSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 0)

    def _click_button_22_2(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　非発生降雨の超過数"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_OverNonOccurRainFallNumSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 1)

    def _click_button_22_3(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　発生降雨の超過数"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_OverOccurRainFallNumSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 2)

    def _click_button_22_4(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　災害捕捉率"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_DisasterSupplementSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 3)

    def _click_button_22_5(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　空振り率"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_WhiffSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 4)

    def _click_button_22_6(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　空振り頻度"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_AlarmAnnounceSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 5)

    def _click_button_22_7(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　空振り時間"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_WhiffTimeSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 6)

    def _click_button_22_8(self, event):
        global g_System_Title

        self._get_environ()
        self._set_title("■集計結果")
        a_label = self.lblTitle.GetLabel()
        a_label += "\n　　警報発表の頻度"
        self.lblTitle.SetLabel(a_label)
        self._dispStatistics(com.g_OutPath + "\\" + com.g_WhiffFrequencySymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 7)

    def _click_button_22_9(self, event):
        global g_System_Title

    # メニュークリックイベント処理
    def _click_menu_bar(self, event):

        event_id = event.GetId()
        print(event_id)
        if event_id == 11:
            self._hide_Panel()
            # RBFNプログラム用入力データ
            self.g_button_11_1.Enabled = True
            self.g_button_11_2.Enabled = True
            self._get_environ()
            self._set_title("■RBFNプログラム用入力データ作成")
            if (self.g_listBox_11.GetItemCount() > 0):
                self.g_listBox_11.DeleteAllItems()
            self.g_panel_11.Show()
        elif event_id == 12:
            # RBFNプログラムの起動
            check_call([".\\bin\\RBFN.exe"])
        elif event_id == 13:
            self._hide_Panel()
            # RBFN出力値の抽出処理
            self._get_environ()
            self._set_title("■RBFN出力値の抽出処理")
            self._set_listBox_13_1_year()
            self._set_listBox_13_2_year()
            self.g_panel_13.Show()
        elif event_id == 21:
            self._hide_Panel()
            # RBFN補正の結果
            self._get_environ()
            self._set_title("■RBFN補正の結果")
            self._set_listBox_21_1_year()
            self._set_listBox_21_2_year("")
            self.g_panel_21.Show()
        elif event_id == 22:
            self._hide_Panel()
            # 集計結果
            self._get_environ()
            self._set_title("■集計結果")
            self._dispStatistics("", -1)
            self.g_panel_22.Show()
        elif event_id == 23:
            self._hide_Panel()
            self._get_environ()
            self._set_title("■ブロック集計")
            if (wx.MessageBox("ブロック集計を行います。\n集計には時間がかかります。", g_System_Title, wx.YES_NO) == wx.YES):
                self._enable_MenuBar(False)
                self._makeBlockAll()
                self._enable_MenuBar(True)
                wx.MessageBox("ブロック集計が完了しました！", g_System_Title)
                # ブロック集計
                self.g_panel_23.Show()

    def _dispStatistics(self, h_fname, h_row):
        com.Outputlog(com.g_LOGMODE_TRACE1, '_dispStatistics', "start")

        try:
            if (self.g_listBox_22_1.GetItemCount() > 0):
                self.g_listBox_22_1.DeleteAllItems()
            if (self.g_listBox_22_1.GetColumnCount() > 0):
                self.g_listBox_22_1.DeleteAllColumns()

            if (h_row < 0):
                return

            self.g_listBox_22_1.InsertColumn(0, "メッシュ番号", width=100)
            if (h_row == 0) or (h_row == 1) or (h_row == 2):
                self.g_listBox_22_1.InsertColumn(1, "0.9", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(2, "0.8", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(3, "0.7", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(4, "0.6", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(5, "0.5", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(6, "0.4", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(7, "0.3", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(8, "0.2", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(9, "0.1", format=wx.LIST_FORMAT_CENTER, width=60)
            elif (h_row == 3) or (h_row == 4):
                self.g_listBox_22_1.InsertColumn(1, "0.9(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(2, "0.8(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(3, "0.7(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(4, "0.6(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(5, "0.5(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(6, "0.4(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(7, "0.3(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(8, "0.2(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                self.g_listBox_22_1.InsertColumn(9, "0.1(%)", format=wx.LIST_FORMAT_CENTER, width=60)
                if  (h_row == 3):
                    self.g_listBox_22_1.InsertColumn(10, "発生降雨数", format=wx.LIST_FORMAT_CENTER, width=100)
            elif (h_row == 5) or (h_row == 7):
                self.g_listBox_22_1.InsertColumn(1, "0.9(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(2, "0.8(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(3, "0.7(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(4, "0.6(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(5, "0.5(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(6, "0.4(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(7, "0.3(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(8, "0.2(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(9, "0.1(回/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(10, "対象期間(年)", format=wx.LIST_FORMAT_CENTER, width=100)
            elif (h_row == 6):
                self.g_listBox_22_1.InsertColumn(1, "0.9(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(2, "0.8(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(3, "0.7(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(4, "0.6(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(5, "0.5(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(6, "0.4(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(7, "0.3(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(8, "0.2(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(9, "0.1(時間/年)", format=wx.LIST_FORMAT_CENTER, width=100)
                self.g_listBox_22_1.InsertColumn(10, "対象期間(年)", format=wx.LIST_FORMAT_CENTER, width=100)


            a_sr = open(h_fname, "r", encoding="shift_jis")
            # 1行分、読み飛ばす
            a_textline = a_sr.readline().rstrip('\r\n')
            a_textline = a_sr.readline().rstrip('\r\n')
            a_i = 0
            while a_textline:
                a_split = a_textline.split(",")
                self.g_listBox_22_1.InsertItem(a_i, a_split[0])
                self.g_listBox_22_1.SetItem(a_i, 1, a_split[1])
                self.g_listBox_22_1.SetItem(a_i, 2, a_split[2])
                self.g_listBox_22_1.SetItem(a_i, 3, a_split[3])
                self.g_listBox_22_1.SetItem(a_i, 4, a_split[4])
                self.g_listBox_22_1.SetItem(a_i, 5, a_split[5])
                self.g_listBox_22_1.SetItem(a_i, 6, a_split[6])
                self.g_listBox_22_1.SetItem(a_i, 7, a_split[7])
                self.g_listBox_22_1.SetItem(a_i, 8, a_split[8])
                self.g_listBox_22_1.SetItem(a_i, 9, a_split[9])
                if (h_row == 3) or (h_row == 5) or (h_row == 6) or (h_row == 7):
                    self.g_listBox_22_1.SetItem(a_i, 10, a_split[10])

                a_textline = a_sr.readline().rstrip('\r\n')
                a_i += 1
            a_sr.close()

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_dispStatistics', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_dispStatistics', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_dispStatistics', "end")

    def _dispStatisticsByMesh(self, h_meshNo):
        com.Outputlog(com.g_LOGMODE_TRACE1, '_dispStatisticsByMesh', "start")

        try:
            a_size = self.g_listBox_21_2.GetItemCount()
            for a_i in range(0, a_size):
                self.g_listBox_21_2.SetItem(a_i, 1, "")
                self.g_listBox_21_2.SetItem(a_i, 2, "")
                self.g_listBox_21_2.SetItem(a_i, 3, "")
                self.g_listBox_21_2.SetItem(a_i, 4, "")
                self.g_listBox_21_2.SetItem(a_i, 5, "")
                self.g_listBox_21_2.SetItem(a_i, 6, "")
                self.g_listBox_21_2.SetItem(a_i, 7, "")
                self.g_listBox_21_2.SetItem(a_i, 8, "")
                self.g_listBox_21_2.SetItem(a_i, 9, "")
                self.g_listBox_21_2.SetItem(a_i, 10, "")
                self.g_listBox_21_2.SetItem(a_i, 11, "")

            # 全降雨の超過数
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_OverAllRainFallNumSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 0)
            # 非発生降雨の超過数
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_OverNonOccurRainFallNumSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 1)
            # 発生降雨の超過数
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_OverOccurRainFallNumSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 2)
            # 災害捕捉率
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_DisasterSupplementSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 3)
            # 空振り率
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_WhiffSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 4)
            # 空振り頻度
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_WhiffFrequencySymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 5)
            # 空振り時間
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_WhiffTimeSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 6)
            # 警報発表の頻度
            self._dispStatisticsByMesh_sub(h_meshNo, com.g_OutPath + "\\" + com.g_AlarmAnnounceSymbol + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".csv", 7)

            self.g_listBox_21_2.Update()

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_dispStatisticsByMesh', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_dispStatisticsByMesh', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_dispStatisticsByMesh', "end")

    def _dispStatisticsByMesh_sub(self, h_meshNo, h_fname, h_row):
        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeContour_proc', "start")

        try:
            a_sr = open(h_fname, "r", encoding="shift_jis")
            # 1行分、読み飛ばす
            a_textline = a_sr.readline().rstrip('\r\n')
            a_textline = a_sr.readline().rstrip('\r\n')
            while a_textline:
                a_split = a_textline.split(",")
                if (a_split[0] == h_meshNo):
                    self.g_listBox_21_2.SetItem(h_row, 1, a_split[1])
                    self.g_listBox_21_2.SetItem(h_row, 2, a_split[2])
                    self.g_listBox_21_2.SetItem(h_row, 3, a_split[3])
                    self.g_listBox_21_2.SetItem(h_row, 4, a_split[4])
                    self.g_listBox_21_2.SetItem(h_row, 5, a_split[5])
                    self.g_listBox_21_2.SetItem(h_row, 6, a_split[6])
                    self.g_listBox_21_2.SetItem(h_row, 7, a_split[7])
                    self.g_listBox_21_2.SetItem(h_row, 8, a_split[8])
                    self.g_listBox_21_2.SetItem(h_row, 9, a_split[9])
                    if (h_row == 3):
                        self.g_listBox_21_2.SetItem(h_row, 10, a_split[10])
                    if (h_row == 5) or (h_row == 6) or (h_row == 7):
                        self.g_listBox_21_2.SetItem(h_row, 11, a_split[10])

                a_textline = a_sr.readline().rstrip('\r\n')
            a_sr.close()

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_dispStatisticsByMesh_sub', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_dispStatisticsByMesh_sub', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_dispStatisticsByMesh_sub', "end")

    def _enable_MenuBar(self, h_enable):
        self.g_menu_bar.EnableTop(0, h_enable)
        self.g_menu_bar.EnableTop(1, h_enable)

    def _get_environ(self):
        global com
        global g_ini_path
        global g_meshSum_target
        global g_meshSum_list
        global g_meshList_target
        global g_meshList_list

        com.GetEnvData(g_ini_path)

        '''
        #com.Store_DisasterFile()
        com.g_textSum_DisasterFile = com.Store_DataFile(com.g_DisasterFileName, com.g_textline_DisasterFile)
        #com.Store_CautionAnnounceFile()
        com.g_textSum_CautionAnnounceFile = com.Store_DataFile(com.g_CautionAnnounceFileName, com.g_textline_CautionAnnounceFile)
        '''

        # 集計
        # 解析雨量のCSVファイルからメッシュ数を取得する。
        del g_meshList_target[:]
        del g_meshList_list[:]

        if com.g_TargetMeshFile != "":
            g_meshSum_target = com.GetMeshSumFromFile(com.g_TargetStartYear, g_meshList_target)
            #g_meshSum = com.GetMeshSumFromFile2(com.g_TargetStartYear, g_meshList_target)
        else:
            a_RainfallFileName = com.g_OutPath + "\\" + com.g_RainfallFileSId + str(com.g_TargetMeshFile) + com.g_RainfallFileEId
            g_meshSum_target = com.GetMeshSum(com.g_TargetStartYear, a_RainfallFileName, g_meshList_target)
            #g_meshSum = com.GetMeshSum(com.g_TargetStartYear, a_RainfallFileName, g_meshList_target)
        g_meshSum_list = com.GetMeshList(com.g_TargetStartYear, g_meshList_list)

        print(g_meshList_target)
        print(g_meshList_list)

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
        self.g_panel_21.SetSize(size)
        self.g_button_21_1.SetPosition(wx.Point(size.width - (310 - 75), 8))
        pos = self.g_button_21_1.GetPosition()
        self.g_button_21_2.SetPosition(wx.Point(size.width - (250 - 75*2 - 4), 8))
        self.g_listBox_21_1.SetSize(4 + 100, size.height - (50 + 60))
        self.g_listBox_21_2.SetSize(size.width - 24 - 100 - 4, 190)
        self.g_panel_21_sub1.SetSize(size.width - 24 - 100 - 4 - 1, size.height - (50 + 60) - 190)

        # 集計結果
        self.g_panel_22.SetSize(size)
        self.g_button_22_1.SetPosition(wx.Point(size.width - (766 - 130 - 4), 8))
        self.g_button_22_2.SetPosition(wx.Point(size.width - (766 - 130*2 - 4*2), 8))
        self.g_button_22_3.SetPosition(wx.Point(size.width - (766 - 130*3 - 4*3), 8))
        self.g_button_22_4.SetPosition(wx.Point(size.width - (766 - 130*4 - 4*4), 8))
        self.g_button_22_5.SetPosition(wx.Point(size.width - (766 - 130 - 4), 8 + 25 + 4))
        self.g_button_22_6.SetPosition(wx.Point(size.width - (766 - 130*2 - 4*2), 8 + 25 + 4))
        self.g_button_22_7.SetPosition(wx.Point(size.width - (766 - 130*3 - 4*3), 8 + 25 + 4))
        self.g_button_22_8.SetPosition(wx.Point(size.width - (766 - 130*4 - 4*4), 8 + 25 + 4))
        self.g_button_22_9.SetPosition(wx.Point(size.width - (766 - 130*5 - 4*5), 8))
        self.g_listBox_22_1.SetSize(size.width - 24, size.height - (50 + 60 + 20))

        # ブロック集計

        self.Refresh()
        self.Update()

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
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeAlarmAnnounce', "start")

        try:
            a_proc = clsFigure.MakeAlarmAnnounce(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeAlarmAnnounce', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeAlarmAnnounce', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeAlarmAnnounce', "end")

    def _makeAllRainfallData(self):
        global com
        global g_meshList_target

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeAllRainfallData', "start")

        try:
            # RBFNデータ入力

            for a_year in range(com.g_TargetStartYear, com.g_TargetEndYear + 1):
            #for a_year in range(com.g_TargetStartYear, com.g_TargetStartYear + 2):
                print('***a_year=' + str(a_year))

                self.prv_RainfallFileName = com.g_OutPath + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
                self.prv_SoilRainFileName = com.g_OutPath + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId
                # 予測的中率
                self.prv_RainfallFileName1 = com.g_OutPathReal + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
                self.prv_SoilRainFileName1 = com.g_OutPathReal + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId

                a_clsRainfall = clsRainfall.MakeAllRainfallDataByMesh(
                    1,
                    com.g_strIni,
                    a_year,
                    -1,
                    g_meshList_target
                )


                a_meshSum = len(g_meshList_target)

                # 通常
                a_clsRainfall.textSum_Rainfall = com.Store_DataFile(self.prv_RainfallFileName, a_clsRainfall.textline_Rainfall)
                a_clsRainfall.textSum_SoilRain = com.Store_DataFile(self.prv_SoilRainFileName, a_clsRainfall.textline_SoilRain)

                a_count = self.g_listBox_11.GetItemCount()
                for a_cnt in range(0, a_meshSum):
                    a_split = g_meshList_target[a_cnt].split(',')
                    a_meshNo = ''
                    if (com.g_TargetRainMesh == 1):
                        # 対象Surfaceが1km
                        a_meshNo = a_split[1]
                    else:
                        # 対象Surfaceが5km
                        a_meshNo = a_split[0]
                    print('a_meshNo=' + a_meshNo)

                    self.g_listBox_11.InsertItem(a_cnt + a_count, str(a_year))
                    self.g_listBox_11.SetItem(a_cnt + a_count, 1, str(a_cnt + 1) + "/" + str(a_meshSum))
                    self.g_listBox_11.SetItem(a_cnt + a_count, 2, a_meshNo)
                    self.g_listBox_11.SetItem(a_cnt + a_count, 3, "処理中......")
                    self.g_listBox_11.SetItemTextColour(a_cnt, wx.RED)
                    #self.g_listBox_11.Refresh()
                    self.g_listBox_11.Update()
                    #self.Refresh()
                    self.Update()

                    a_clsRainfall.meshIdx = a_cnt
                    #a_clsRainfall.run()
                    a_clsRainfall._makeAllRainfallDataByMesh(a_year, 0, a_cnt, g_meshList_target)

                    self.g_listBox_11.SetItem(a_cnt + a_count, 3, "入力データ作成が完了しました。")
                    self.g_listBox_11.SetItemTextColour(a_cnt + a_count, wx.BLUE)
                    #self.g_listBox_11.Refresh()
                    self.g_listBox_11.Update()
                    #self.Refresh()
                    self.Update()

                del a_clsRainfall.textline_Rainfall[:]
                del a_clsRainfall.textline_SoilRain[:]
                gc.collect()

                if com.g_RainKind != 0:
                    # 比較対象の実況雨量データの算出
                    a_clsRainfall.textSum_Rainfall = com.Store_DataFile(self.prv_RainfallFileName1, a_clsRainfall.textline_Rainfall)
                    a_clsRainfall.textSum_SoilRain = com.Store_DataFile(self.prv_SoilRainFileName1, a_clsRainfall.textline_SoilRain)

                    a_count = self.g_listBox_11.GetItemCount()
                    for a_cnt in range(0, a_meshSum):
                        a_split = g_meshList_target[a_cnt].split(',')
                        a_meshNo = ''
                        if (com.g_TargetRainMesh == 1):
                            # 対象Surfaceが1km
                            a_meshNo = a_split[1]
                        else:
                            # 対象Surfaceが5km
                            a_meshNo = a_split[0]
                        print('a_meshNo=' + a_meshNo)

                        self.g_listBox_11.InsertItem(a_cnt + a_count, str(a_year))
                        self.g_listBox_11.SetItem(a_cnt + a_count, 1, str(a_cnt + 1) + "/" + str(a_meshSum))
                        self.g_listBox_11.SetItem(a_cnt + a_count, 2, a_meshNo)
                        self.g_listBox_11.SetItem(a_cnt + a_count, 3, "実況雨量の処理中......")
                        self.g_listBox_11.SetItemTextColour(a_cnt + a_count, wx.RED)
                        #self.g_listBox_11.Refresh()
                        self.g_listBox_11.Update()
                        #self.Refresh()
                        self.Update()

                        a_clsRainfall.meshIdx = a_cnt
                        #a_clsRainfall.run()
                        a_clsRainfall._makeAllRainfallDataByMesh(a_year, 1, a_cnt, g_meshList_target)

                        self.g_listBox_11.SetItem(a_cnt + a_count, 3, "実況雨量の入力データ作成が完了しました。")
                        self.g_listBox_11.SetItemTextColour(a_cnt + a_count, wx.BLUE)
                        #self.g_listBox_11.Refresh()
                        self.g_listBox_11.Update()
                        #self.Refresh()
                        self.Update()

                    del a_clsRainfall.textline_Rainfall[:]
                    del a_clsRainfall.textline_SoilRain[:]
                    gc.collect()

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeAllRainfallData', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeAllRainfallData', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeAllRainfallData', "end")

    def _makeAllRainfallData_proc(self):
        global com
        global g_meshList_target

        com.Outputlog(com.g_LOGMODE_INFORMATION, '_makeAllRainfallData_proc', "start")

        a_iRet = 0

        #共有メモリ
        # 災害情報
        a_key_Disaster = "shmkey_Disaster"
        a_csv_Disaster = com.g_DisasterFileName
        a_shmKey_Disaster = c_char_p(a_key_Disaster.encode("sjis"))
        a_fName_Disaster = c_char_p(a_csv_Disaster.encode("sjis"))
        a_size_Disaster = c_void_p(0)
        a_hFile_Disaster = c_void_p(0)
        a_mapping_Disaster = c_void_p(0)
        a_pshared_Disaster = c_void_p(0)

        # 警戒情報
        a_key_CautionAnnounce = "shmkey_CautionAnnounce"
        a_csv_CautionAnnounce = com.g_CautionAnnounceFileName
        a_shmKey_CautionAnnounce = c_char_p(a_key_CautionAnnounce.encode("sjis"))
        a_fName_CautionAnnounce = c_char_p(a_csv_CautionAnnounce.encode("sjis"))
        a_size_CautionAnnounce = c_void_p(0)
        a_hFile_CautionAnnounce = c_void_p(0)
        a_mapping_CautionAnnounce = c_void_p(0)
        a_pshared_CautionAnnounce = c_void_p(0)

        # 気温
        a_key_Temperature = "shmkey_Temperature"
        a_csv_Temperature = ""
        a_shmKey_Temperature = c_char_p(a_key_Temperature.encode("sjis"))
        a_fName_Temperature = c_char_p(a_csv_Temperature.encode("sjis"))
        a_size_Temperature = c_void_p(0)
        a_hFile_Temperature = c_void_p(0)
        a_mapping_Temperature = c_void_p(0)
        a_pshared_Temperature = c_void_p(0)

        # 全降雨
        a_key_Rainfall = "shmkey_Rainfall"
        a_csv_Rainfall = ""
        a_shmKey_Rainfall = c_char_p(a_key_Rainfall.encode("sjis"))
        a_fName_Rainfall = c_char_p(a_csv_Rainfall.encode("sjis"))
        a_size_Rainfall = c_void_p(0)
        a_hFile_Rainfall = c_void_p(0)
        a_mapping_Rainfall = c_void_p(0)
        a_pshared_Rainfall = c_void_p(0)
        a_key_SoilRain = "shmkey_SoilRain"
        a_csv_SoilRain = ""
        a_shmKey_SoilRain = c_char_p(a_key_SoilRain.encode("sjis"))
        a_fName_SoilRain = c_char_p(a_csv_SoilRain.encode("sjis"))
        a_size_SoilRain = c_void_p(0)
        a_hFile_SoilRain = c_void_p(0)
        a_mapping_SoilRain = c_void_p(0)
        a_pshared_SoilRain = c_void_p(0)

        # 予測的中率
        a_key_Rainfall1 = "shmkey_Rainfall1"
        a_csv_Rainfall1 = ""
        a_shmKey_Rainfall1 = c_char_p(a_key_Rainfall1.encode("sjis"))
        a_fName_Rainfall1 = c_char_p(a_csv_Rainfall1.encode("sjis"))
        a_size_Rainfall1 = c_void_p(0)
        a_hFile_Rainfall1 = c_void_p(0)
        a_mapping_Rainfall1 = c_void_p(0)
        a_pshared_Rainfall1 = c_void_p(0)
        a_key_SoilRain1 = "shmkey_SoilRain1"
        a_csv_SoilRain1 = ""
        a_shmKey_SoilRain1 = c_char_p(a_key_SoilRain1.encode("sjis"))
        a_fName_SoilRain1 = c_char_p(a_csv_SoilRain1.encode("sjis"))
        a_size_SoilRain1 = c_void_p(0)
        a_hFile_SoilRain1 = c_void_p(0)
        a_mapping_SoilRain1 = c_void_p(0)
        a_pshared_SoilRain1 = c_void_p(0)

        try:
            # RBFNデータ入力

            # 災害情報
            a_iRet = self.PyShmMapCreate(
                a_shmKey_Disaster,
                a_fName_Disaster,
                byref(a_size_Disaster),
                byref(a_hFile_Disaster),
                byref(a_mapping_Disaster),
                byref(a_pshared_Disaster)
            )
            # 警戒情報
            a_iRet = self.PyShmMapCreate(
                a_shmKey_CautionAnnounce,
                a_fName_CautionAnnounce,
                byref(a_size_CautionAnnounce),
                byref(a_hFile_CautionAnnounce),
                byref(a_mapping_CautionAnnounce),
                byref(a_pshared_CautionAnnounce)
            )

            '''
            # 災害情報
            a_DisasterFile = None
            a_buf = com.Store_DataFile_all(com.g_DisasterFileName)
            #print(a_buf.encode("utf-8"))
            #a_DisasterFile = multiprocessing.Value("i", 1)
            #a_DisasterFile = multiprocessing.Value(c_wchar_p, a_buf)
            a_DisasterFile = multiprocessing.Array("u", a_buf)
            #print(a_DisasterFile.value)
            # 警戒情報
            a_CautionAnnounceFile = None
            a_buf = com.Store_DataFile_all(com.g_CautionAnnounceFileName)
            #a_CautionAnnounceFile = multiprocessing.Value(c_wchar_p, a_buf)
            a_CautionAnnounceFile = multiprocessing.Array("u", a_buf)
            #print(a_DisasterFile.value)
            '''

            #for a_year in range(com.g_TargetStartYear, com.g_TargetStartYear + 2):
            for a_year in range(com.g_TargetStartYear, com.g_TargetEndYear + 1):
                print('***a_year=' + str(a_year))

                #気温情報
                a_TemperatureFile = None
                a_TemperatureFileName = com.g_OutPath + "\\" + com.g_TemperatureFileSId + str(a_year) + com.g_TemperatureFileEId
                a_fName_Temperature = c_char_p(a_TemperatureFileName.encode("sjis"))
                a_iRet = self.PyShmMapCreate(
                    a_shmKey_Temperature,
                    a_fName_Temperature,
                    byref(a_size_Temperature),
                    byref(a_hFile_Temperature),
                    byref(a_mapping_Temperature),
                    byref(a_pshared_Temperature)
                )
                '''
                a_buf = com.Store_DataFile_all(a_TemperatureFileName)
                if (a_buf != None):
                    #a_TemperatureFile = multiprocessing.Value(c_wchar_p, a_buf)
                    a_TemperatureFile = multiprocessing.Array("u", a_buf)
                    '''

                # 全降雨
                a_RainfallFileName = com.g_OutPath + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
                a_SoilRainFileName = com.g_OutPath + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId
                # 予測的中率
                a_RainfallFileName1 = com.g_OutPathReal + "\\" + com.g_RainfallFileSId + str(a_year) + com.g_RainfallFileEId
                a_SoilRainFileName1 = com.g_OutPathReal + "\\" + com.g_SoilrainFileSId + str(a_year) + com.g_SoilrainFileEId

                a_fName_Rainfall = c_char_p(a_RainfallFileName.encode("sjis"))
                a_iRet = self.PyShmMapCreate(
                    a_shmKey_Rainfall,
                    a_fName_Rainfall,
                    byref(a_size_Rainfall),
                    byref(a_hFile_Rainfall),
                    byref(a_mapping_Rainfall),
                    byref(a_pshared_Rainfall)
                )
                a_fName_SoilRain = c_char_p(a_SoilRainFileName.encode("sjis"))
                a_iRet = self.PyShmMapCreate(
                    a_shmKey_SoilRain,
                    a_fName_SoilRain,
                    byref(a_size_SoilRain),
                    byref(a_hFile_SoilRain),
                    byref(a_mapping_SoilRain),
                    byref(a_pshared_SoilRain)
                )
                '''
                a_RainfallFile = None
                a_buf = com.Store_DataFile_all(a_RainfallFileName)
                #a_RainfallFile = multiprocessing.Value(c_wchar_p, a_buf)
                a_RainfallFile = multiprocessing.Array("u", a_buf)
                a_SoilRainFile = None
                a_buf = com.Store_DataFile_all(a_SoilRainFileName)
                #a_SoilRainFile = multiprocessing.Value(c_wchar_p, a_buf)
                a_SoilRainFile = multiprocessing.Array("u", a_buf)

                a_RainfallFile1 = None
                a_SoilRainFile1 = None
                '''

                if com.g_RainKind != 0:
                    a_fName_Rainfall1 = c_char_p(a_RainfallFileName1.encode("sjis"))
                    a_iRet = self.PyShmMapCreate(
                        a_shmKey_Rainfall1,
                        a_fName_Rainfall1,
                        byref(a_size_Rainfall1),
                        byref(a_hFile_Rainfall1),
                        byref(a_mapping_Rainfall1),
                        byref(a_pshared_Rainfall1)
                    )
                    a_fName_SoilRain1 = c_char_p(a_SoilRainFileName1.encode("sjis"))
                    a_iRet = self.PyShmMapCreate(
                        a_shmKey_SoilRain1,
                        a_fName_SoilRain1,
                        byref(a_size_SoilRain1),
                        byref(a_hFile_SoilRain1),
                        byref(a_mapping_SoilRain1),
                        byref(a_pshared_SoilRain1)
                    )
                    '''
                    a_buf = com.Store_DataFile_all(a_RainfallFileName1)
                    #a_RainfallFile1 = multiprocessing.Value(c_wchar_p, a_buf)
                    a_RainfallFile1 = multiprocessing.Array("u", a_buf)
                    a_buf = com.Store_DataFile_all(a_SoilRainFileName1)
                    #a_SoilRainFile1 = multiprocessing.Value(c_wchar_p, a_buf)
                    a_SoilRainFile1 = multiprocessing.Array("u", a_buf)
                    '''

                a_meshSum = len(g_meshList_target)

                ''' testing...
                self.g_listBox_11.SetItem(0, 3, "入力データ作成が完了しました。")
                self.g_listBox_11.Refresh(0)
                return
                '''

                a_sum = 0
                a_count = self.g_listBox_11.GetItemCount()
                while (a_sum < a_meshSum):
                    #a_cnt_max = (a_sum + com.g_cpu_count)
                    a_cnt_max = (a_sum + com.g_MakeAllRainfallDataExecNum)
                    if (a_cnt_max > a_meshSum):
                        a_cnt_max = a_meshSum

                    print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                    a_procs = []
                    a_proc_num = 0
                    for a_cnt in range(a_sum, a_cnt_max):
                        a_proc_num += 1
                        #print('a_cnt=' + str(a_cnt))
                        a_split = g_meshList_target[a_cnt].split(',')
                        a_meshNo = ''
                        if (com.g_TargetRainMesh == 1):
                            # 対象Surfaceが1km
                            a_meshNo = a_split[1]
                        else:
                            # 対象Surfaceが5km
                            a_meshNo = a_split[0]
                        print('a_meshNo=' + a_meshNo)

                        '''
                        a_proc = multiprocessing.Process(target=clsRainfall.MakeAllRainfallDataByMesh,
                                         args=(
                                             a_proc_num,
                                             com.g_strIni,
                                             a_DisasterFile,
                                             a_CautionAnnounceFile,
                                             a_year,
                                             a_cnt,
                                             g_meshList_target
                                         ))
                                         '''
                        '''
                        a_proc = multiprocessing.Process(target=clsRainfall.MakeAllRainfallDataByMesh,
                                         args=(
                                             a_proc_num,
                                             com.g_strIni,
                                             a_DisasterFile,
                                             a_CautionAnnounceFile,
                                             a_TemperatureFile,
                                             a_RainfallFile,
                                             a_SoilRainFile,
                                             a_RainfallFile1,
                                             a_SoilRainFile1,
                                             a_year,
                                             a_cnt,
                                             g_meshList_target
                                         ))
                                         '''
                        a_proc = multiprocessing.Process(target=clsRainfall.MakeAllRainfallDataByMesh,
                                         args=(
                                             a_proc_num,
                                             com.g_strIni,
                                             a_key_Disaster,
                                             a_size_Disaster.value,
                                             a_key_CautionAnnounce,
                                             a_size_CautionAnnounce.value,
                                             a_key_Temperature,
                                             a_size_Temperature.value,
                                             a_key_Rainfall,
                                             a_size_Rainfall.value,
                                             a_key_SoilRain,
                                             a_size_SoilRain.value,
                                             a_key_Rainfall1,
                                             a_size_Rainfall1.value,
                                             a_key_SoilRain1,
                                             a_size_SoilRain1.value,
                                             a_year,
                                             a_cnt,
                                             g_meshList_target
                                         ))
                        '''
                        a_proc = multiprocessing.Process(target=clsRainfall.MakeAllRainfallDataByMesh,
                                                         args=(
                                                             a_proc_num,
                                                             com.g_strIni,
                                                             a_DisasterFile,
                                                             a_CautionAnnounceFile,
                                                             a_TemperatureFile,
                                                             a_RainfallFile,
                                                             a_SoilRainFile,
                                                             a_RainfallFile1,
                                                             a_SoilRainFile1,
                                                             a_year,
                                                             a_cnt,
                                                             g_meshList_target
                                                         ))
                                                         '''

                        a_procs.append(a_proc)

                        #self.g_listBox_11.Append(str(a_year))
                        self.g_listBox_11.InsertItem(a_count + a_cnt, str(a_year))
                        self.g_listBox_11.SetItem(a_count + a_cnt, 1, str(a_cnt + 1) + "/" + str(a_meshSum))
                        self.g_listBox_11.SetItem(a_count + a_cnt, 2, a_meshNo)
                        self.g_listBox_11.SetItem(a_count + a_cnt, 3, "処理中......")
                        self.g_listBox_11.SetItemTextColour(a_count + a_cnt, wx.RED)
                        #self.g_listBox_11.Select(a_count + a_cnt)
                        #self.g_listBox_11.cur = a_count + a_cnt
                        self.g_listBox_11.Update()

                    self._refresh_self()

                    for a_proc in a_procs:
                        a_proc.start()
                    for a_proc in a_procs:
                        a_proc.join()
                    for a_proc in a_procs:
                        a_proc.terminate()

                    for a_i in range(a_sum, a_cnt_max):
                        self.g_listBox_11.SetItem(a_count + a_i , 3, "入力データ作成が完了しました。")
                        self.g_listBox_11.SetItemTextColour(a_count + a_i, wx.BLUE)
                        self.g_listBox_11.Update()
                        self.Update()

                    self._refresh_self()

                    print('All process is ended.')

                    a_sum = a_cnt_max

                # 気温
                a_iRet = self.PyShmMapClose(
                    a_hFile_Temperature,
                    a_mapping_Temperature,
                    a_pshared_Temperature
                )
                # 全降雨
                a_iRet = self.PyShmMapClose(
                    a_hFile_Rainfall,
                    a_mapping_Rainfall,
                    a_pshared_Rainfall
                )
                a_iRet = self.PyShmMapClose(
                    a_hFile_SoilRain,
                    a_mapping_SoilRain,
                    a_pshared_SoilRain
                )
                # 予測適中率
                if com.g_RainKind != 0:
                    a_iRet = self.PyShmMapClose(
                        a_hFile_Rainfall1,
                        a_mapping_Rainfall1,
                        a_pshared_Rainfall1
                    )
                    a_iRet = self.PyShmMapClose(
                        a_hFile_SoilRain1,
                        a_mapping_SoilRain1,
                        a_pshared_SoilRain1
                    )

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeAllRainfallData_proc', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeAllRainfallData_proc', sys.exc_info())
        finally:
            if (self.g_shmlib != None):
                # 共有メモリ
                # 災害情報
                a_iRet = self.PyShmMapClose(
                    a_hFile_Disaster,
                    a_mapping_Disaster,
                    a_pshared_Disaster
                )
                # 警戒情報
                a_iRet = self.PyShmMapClose(
                    a_hFile_CautionAnnounce,
                    a_mapping_CautionAnnounce,
                    a_pshared_CautionAnnounce
                )

        com.Outputlog(com.g_LOGMODE_INFORMATION, '_makeAllRainfallData_proc', "end")

    def _makeBlockAll(self):
        global com

        a_proc = clsBlock.MakeBlockAll(
            0,
            com.g_strIni
        )

    def _makeCautionAnnounceFrequencyOverOccurRainFallNum(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeCautionAnnounceFrequencyOverOccurRainFallNum', "start")

        try:
            a_proc = clsFigure.MakeCautionAnnounceFrequencyOverOccurRainFallNum(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeCautionAnnounceFrequencyOverOccurRainFallNum', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeCautionAnnounceFrequencyOverOccurRainFallNum', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeCautionAnnounceFrequencyOverOccurRainFallNum', "end")

    def _makeCautionAnnounceRateOccurNum(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeCautionAnnounceRateOccurNum', "start")

        try:
            a_proc = clsFigure.MakeCautionAnnounceRateOccurNum(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeCautionAnnounceRateOccurNum', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeCautionAnnounceRateOccurNum', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeCautionAnnounceRateOccurNum', "end")

    def _makeCautionAnnounceRateOccurRainFallNum(self, ):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeCautionAnnounceRateOccurRainFallNum', "start")

        try:
            a_proc = clsFigure.MakeCautionAnnounceRateOccurRainFallNum(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeCautionAnnounceRateOccurRainFallNum', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeCautionAnnounceRateOccurRainFallNum', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeCautionAnnounceRateOccurRainFallNum', "end")

    def _makeContour(self):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeContour', "start")

        try:
            '''
            # 災害情報
            com.g_textSum_DisasterFile = com.Store_DataFile(com.g_DisasterFileName, com.g_textline_DisasterFile)
            # 警戒情報
            com.g_textSum_CautionAnnounceFile = com.Store_DataFile(com.g_CautionAnnounceFileName, com.g_textline_CautionAnnounceFile)
            # 対象メッシュ情報
            com.g_textSum_TargetMeshFile = com.Store_DataFile(com.g_TargetMeshFile, com.g_textline_TargetMeshFile)
    
            a_manager = Manager()
            a_DisasterFile = a_manager.list(com.g_textline_DisasterFile)
            a_CautionAnnounceFile = a_manager.list(com.g_textline_CautionAnnounceFile)
            a_TargetMeshFile = a_manager.list(com.g_textline_TargetMeshFile)
            '''
            a_clsContour = clsContour.MakeContourByMesh(
                1,
                com.g_strIni,
                "",
                0,
                0,
                0,
                -1
            )

            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)

            for a_cnt in range(0, a_meshSum):
                a_index = g_meshList_check[a_cnt][0]   # インデックス
                a_meshNo = g_meshList_check[a_cnt][1]   # メッシュ番号
                print('a_meshNo=' + a_meshNo)
                self.g_listBox_13_1.SetItem(a_index , 3, "処理中......")
                self.g_listBox_13_1.SetItemTextColour(a_index, wx.RED)
                #self.g_listBox_13_1.Select(a_index, 1)
                #self.SetScrollPos(wx.VERTICAL, a_index)
                self.g_listBox_13_1.Update()
                self.Update()

                a_clsContour.meshNo = a_meshNo
                a_clsContour.run()

                self.g_listBox_13_1.SetItem(a_index , 3, "抽出処理が完了しました。")
                self.g_listBox_13_1.SetItemTextColour(a_index, wx.BLUE)
                self.g_listBox_13_1.Update()
                self.Update()

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeContour', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeContour', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeContour', "end")

    def _makeContour_proc(self):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_INFORMATION, '_makeContour_proc', "start")

        #共有メモリ
        # 災害情報
        a_key_Disaster = "shmkey_Disaster"
        a_csv_Disaster = com.g_DisasterFileName
        a_shmKey_Disaster = c_char_p(a_key_Disaster.encode("sjis"))
        a_fName_Disaster = c_char_p(a_csv_Disaster.encode("sjis"))
        a_size_Disaster = c_void_p(0)
        a_hFile_Disaster = c_void_p(0)
        a_mapping_Disaster = c_void_p(0)
        a_pshared_Disaster = c_void_p(0)

        # 対象メッシュ情報
        a_key_TargetMesh = "shmkey_TargetMesh"
        a_csv_TargetMesh = com.g_TargetMeshFile
        a_shmKey_TargetMesh = c_char_p(a_key_TargetMesh.encode("sjis"))
        a_fName_TargetMesh = c_char_p(a_csv_TargetMesh.encode("sjis"))
        a_size_TargetMesh = c_void_p(0)
        a_hFile_TargetMesh = c_void_p(0)
        a_mapping_TargetMesh = c_void_p(0)
        a_pshared_TargetMesh = c_void_p(0)

        try:
            # 災害情報
            a_iRet = self.PyShmMapCreate(
                a_shmKey_Disaster,
                a_fName_Disaster,
                byref(a_size_Disaster),
                byref(a_hFile_Disaster),
                byref(a_mapping_Disaster),
                byref(a_pshared_Disaster)
            )
            # 警戒情報
            a_iRet = self.PyShmMapCreate(
                a_shmKey_TargetMesh,
                a_fName_TargetMesh,
                byref(a_size_TargetMesh),
                byref(a_hFile_TargetMesh),
                byref(a_mapping_TargetMesh),
                byref(a_pshared_TargetMesh)
            )

            '''
            # 災害情報
            a_DisasterFile = None
            a_buf = com.Store_DataFile_all(com.g_DisasterFileName)
            a_DisasterFile = multiprocessing.Array("u", a_buf)
            # 対象メッシュ情報
            a_TargetMeshFile = None
            a_buf = com.Store_DataFile_all(com.g_TargetMeshFile)
            a_TargetMeshFile = multiprocessing.Array("u", a_buf)
            '''

            '''
            # 災害情報
            com.g_textSum_DisasterFile = com.Store_DataFile_all(com.g_DisasterFileName, com.g_textline_DisasterFile)
            # 警戒情報
            com.g_textSum_CautionAnnounceFile = com.Store_DataFile(com.g_CautionAnnounceFileName, com.g_textline_CautionAnnounceFile)
            # 対象メッシュ情報
            com.g_textSum_TargetMeshFile = com.Store_DataFile(com.g_TargetMeshFile, com.g_textline_TargetMeshFile)
            '''

            '''
            a_DisasterFile = a_manager.list(com.g_textline_DisasterFile)
            a_CautionAnnounceFile = a_manager.list(com.g_textline_CautionAnnounceFile)
            a_TargetMeshFile = a_manager.list(com.g_textline_TargetMeshFile)
            '''

            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                #a_cnt_max = (a_sum + com.g_cpu_count)
                a_cnt_max = (a_sum + com.g_MakeContourExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_index = g_meshList_check[a_cnt][0]   # インデックス
                    a_meshNo = g_meshList_check[a_cnt][1]   # メッシュ番号
                    '''
                    a_split = g_meshList_check[a_cnt].split(',')
                    a_meshNo = ''
                    if (com.g_TargetRainMesh == 1):
                        # 対象Surfaceが1km
                        a_meshNo = a_split[1]
                    else:
                        # 対象Surfaceが5km
                        a_meshNo = a_split[0]
                        '''
                    print('a_meshNo=' + a_meshNo)
                    self.g_listBox_13_1.SetItem(a_index , 3, "処理中......")
                    self.g_listBox_13_1.SetItemTextColour(a_index, wx.RED)
                    #self.g_listBox_13_1.Select(a_index, 1)
                    #self.SetScrollPos(wx.VERTICAL, a_index)
                    self.g_listBox_13_1.Refresh(True)
                    self.g_listBox_13_1.Update()
                    self.Refresh(True)
                    self.Update()

                    '''
                    a_proc = multiprocessing.Process(target=clsContour.MakeContourByMesh,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         a_DisasterFile,
                                         a_CautionAnnounceFile,
                                         a_TargetMeshFile,
                                         a_meshNo,
                                         0,
                                         0,
                                         0,
                                         -1
                                     ))
                                     '''
                    '''
                    a_proc = multiprocessing.Process(target=Testing,
                                     args=(
                                         com.g_strIni
                                     ))
                                     '''
                    a_proc = multiprocessing.Process(target=clsContour.MakeContourByMesh,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         a_key_Disaster,
                                         a_size_Disaster.value,
                                         a_key_TargetMesh,
                                         a_size_TargetMesh.value,
                                         a_meshNo,
                                         0,
                                         0,
                                         0,
                                         -1
                                     ))
                    '''
                    a_proc = multiprocessing.Process(target=clsContour.MakeContourByMesh,
                                                     args=(
                                                         a_proc_num,
                                                         com.g_strIni,
                                                         a_DisasterFile,
                                                         a_TargetMeshFile,
                                                         a_meshNo,
                                                         0,
                                                         0,
                                                         0,
                                                         -1
                                                     ))
                                                     '''

                    a_procs.append(a_proc)

                self._refresh_self()

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                for a_i in range(a_sum, a_cnt_max):
                    '''
                    a_th = threading.Thread(name=str(a_i), target=SetText_ListBox, args=(self, self.g_listBox_13_1, a_i, 3, "抽出処理が完了しました。"))
                    a_th.start()
                    '''
                    ''''''
                    self.g_listBox_13_1.SetItem(a_i , 3, "抽出処理が完了しました。")
                    self.g_listBox_13_1.SetItemTextColour(a_i, wx.BLUE)
                    self.g_listBox_13_1.Refresh(True)
                    self.g_listBox_13_1.Update()
                    self.Refresh(True)
                    self.Update()
                    #time.sleep(3)
                    ''''''
                self._refresh_self()

                print('All process is ended.')

                a_sum = a_cnt_max

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeContour_proc', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeContour_proc', sys.exc_info())
        finally:
            if (self.g_shmlib != None):
                # 共有メモリ
                # 災害情報
                a_iRet = self.PyShmMapClose(
                    a_hFile_Disaster,
                    a_mapping_Disaster,
                    a_pshared_Disaster
                )
                # 対象メッシュ情報
                a_iRet = self.PyShmMapClose(
                    a_hFile_TargetMesh,
                    a_mapping_TargetMesh,
                    a_pshared_TargetMesh
                )

        com.Outputlog(com.g_LOGMODE_INFORMATION, '_makeContour_proc', "end")

    def _makeDisasterSupplement(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeDisasterSupplement', "start")

        try:
            a_proc = clsFigure.MakeDisasterSupplement(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeDisasterSupplement', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeDisasterSupplement', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeDisasterSupplement', "end")

    def _makeDisasterSupplement9_1(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeDisasterSupplement9_1', "start")

        try:
            a_proc = clsFigure.MakeDisasterSupplement9_1(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeDisasterSupplement9_1', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeDisasterSupplement9_1', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeDisasterSupplement9_1', "end")

    def _makeDisasterSupplement9_2(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeDisasterSupplement9_2', "start")

        try:
            a_proc = clsFigure.MakeDisasterSupplement9_2(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeDisasterSupplement9_2', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeDisasterSupplement9_2', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeDisasterSupplement9_2', "end")

    def _makeFigure(self):
        com.Outputlog(com.g_LOGMODE_INFORMATION, '_makeFigure', "start")


        #共有メモリ
        # 災害情報
        a_key_Disaster = "shmkey_Disaster"
        a_csv_Disaster = com.g_DisasterFileName
        a_shmKey_Disaster = c_char_p(a_key_Disaster.encode("sjis"))
        a_fName_Disaster = c_char_p(a_csv_Disaster.encode("sjis"))
        a_size_Disaster = c_void_p(0)
        a_hFile_Disaster = c_void_p(0)
        a_mapping_Disaster = c_void_p(0)
        a_pshared_Disaster = c_void_p(0)

        # 警戒情報
        a_key_CautionAnnounce = "shmkey_CautionAnnounce"
        a_csv_CautionAnnounce = com.g_CautionAnnounceFileName
        a_shmKey_CautionAnnounce = c_char_p(a_key_CautionAnnounce.encode("sjis"))
        a_fName_CautionAnnounce = c_char_p(a_csv_CautionAnnounce.encode("sjis"))
        a_size_CautionAnnounce = c_void_p(0)
        a_hFile_CautionAnnounce = c_void_p(0)
        a_mapping_CautionAnnounce = c_void_p(0)
        a_pshared_CautionAnnounce = c_void_p(0)

        try:
            # 災害情報
            a_iRet = self.PyShmMapCreate(
                a_shmKey_Disaster,
                a_fName_Disaster,
                byref(a_size_Disaster),
                byref(a_hFile_Disaster),
                byref(a_mapping_Disaster),
                byref(a_pshared_Disaster)
            )
            # 警戒情報
            a_iRet = self.PyShmMapCreate(
                a_shmKey_CautionAnnounce,
                a_fName_CautionAnnounce,
                byref(a_size_CautionAnnounce),
                byref(a_hFile_CautionAnnounce),
                byref(a_mapping_CautionAnnounce),
                byref(a_pshared_CautionAnnounce)
            )

            '''
            # 災害情報
            a_DisasterFile = None
            a_buf = com.Store_DataFile_all(com.g_DisasterFileName)
            a_DisasterFile = multiprocessing.Array("u", a_buf)
            # 警戒情報
            a_CautionAnnounceFile = None
            a_buf = com.Store_DataFile_all(com.g_CautionAnnounceFileName)
            a_CautionAnnounceFile = multiprocessing.Array("u", a_buf)
            '''

            self.g_listBox_13_2.SetItem(0, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(0, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # 全降雨の超過数
            # 非発生降雨の超過数
            # 発生降雨の超過数
            self._makeOverRainfall(
                a_key_Disaster,
                a_size_Disaster.value
            )
            self._makeOverRainfallMix()
            self.g_listBox_13_2.SetItem(0, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(0, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(1, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(1, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            #災害捕捉率
            self._makeDisasterSupplement()
            self.g_listBox_13_2.SetItem(1, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(1, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(2, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(2, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # 空振り率
            self._makeWiff()
            # 空振り率2
            self._makeWiff_New()
            self.g_listBox_13_2.SetItem(2, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(2, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(3, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(3, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # 空振り頻度
            self._makeWhiffFrequency()
            # 空振り頻度2
            self._makeWhiffFrequency_New()
            self.g_listBox_13_2.SetItem(3, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(3, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(4, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(4, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # 空振り時間
            self._makeWhiffTime()
            self.g_listBox_13_2.SetItem(4, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(4, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(5, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(5, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # 警報発表頻度
            self._makeAlarmAnnounce()
            self.g_listBox_13_2.SetItem(5, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(5, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(6, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(6, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # 9)実質災害捕捉率
            # 災害捕捉率【降雨数】
            self._makeDisasterSupplement9_1()
            # 災害捕捉率【件数】
            self._makeDisasterSupplement9_2()
            self.g_listBox_13_2.SetItem(6, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(6, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(7, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(7, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # ④実質災害捕捉率
            # 年毎メッシュ単位の算出結果
            self._makeOverRainfall2(
                a_key_Disaster,
                a_size_Disaster.value,
                a_key_CautionAnnounce,
                a_size_CautionAnnounce.value
            )
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
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(8, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(8, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # ②土砂災害警戒情報のリードタイム
            self._makeOverRainfall3_1()
            self._makeOverRainfallMix3_1()
            self.g_listBox_13_2.SetItem(8, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(8, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(9, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(9, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # ③土砂災害警戒情報の発表頻度
            self._makeCautionAnnounceFrequencyOverOccurRainFallNum()
            self.g_listBox_13_2.SetItem(9, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(9, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(10, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(10, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # ⑥RBFN越のリードタイム
            self._makeOverRainfall3_2(
                a_key_Disaster,
                a_size_Disaster.value
            )
            self._makeOverRainfallMix3_2()
            self.g_listBox_13_2.SetItem(10, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(10, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(11, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(11, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # ⑧予測適中率
            if (com.g_RainKind != 0):
                self._makeOverRainfall8()
                self._makeOverRainfallMix8()
                self._makeForecastPredictive()
            self.g_listBox_13_2.SetItem(11, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(11, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

            self.g_listBox_13_2.SetItem(12, 3, "処理中......")
            self.g_listBox_13_2.SetItemTextColour(12, wx.RED)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()
            # ⑨NIGeDaS、NIGeDaSⅡ
            self._makeNIGeDaS()
            self._makeNIGeDaS_NonOccurCalc()
            self.g_listBox_13_2.SetItem(12, 3, "集計処理が完了しました。")
            self.g_listBox_13_2.SetItemTextColour(12, wx.BLUE)
            self.g_listBox_13_2.Update()
            self.Update()
            self._refresh_self()

        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeFigure', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeFigure', sys.exc_info())
        finally:
            if (self.g_shmlib != None):
                # 共有メモリ
                # 災害情報
                a_iRet = self.PyShmMapClose(
                    a_hFile_Disaster,
                    a_mapping_Disaster,
                    a_pshared_Disaster
                )
                # 警戒情報
                a_iRet = self.PyShmMapClose(
                    a_hFile_CautionAnnounce,
                    a_mapping_CautionAnnounce,
                    a_pshared_CautionAnnounce
                )

        com.Outputlog(com.g_LOGMODE_INFORMATION, '_makeFigure', "end")

    def _makeForecastPredictive(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeForecastPredictive', "start")

        try:
            a_proc = clsFigure.MakeForecastPredictive(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeForecastPredictive', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeForecastPredictive', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeForecastPredictive', "end")

    def _makeNIGeDaS(self):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeNIGeDaS', "start")

        try:
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_mlist = [[0, ""]]
                    a_mlist[0][0] = 0
                    a_mlist[0][1] = g_meshList_check[a_cnt][1]
                    print('a_meshNo=' + a_mlist[0][1])
                    # チェックされたものを処理対象
                    a_proc = multiprocessing.Process(target=clsFigure.MakeNIGeDaS,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         a_mlist,
                                         0,
                                         0,
                                         -1
                                     ))
                    a_procs.append(a_proc)

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max

                '''
                # チェックされたものを処理対象
                a_proc = clsFigure.MakeNIGeDaS(
                    0,
                    com.g_strIni,
                    g_meshList_check,
                    0,
                    0,
                    -1
                )
                '''
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeNIGeDaS', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeNIGeDaS', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeNIGeDaS', "end")

    def _makeNIGeDaS_NonOccurCalc(self):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeNIGeDaS_NonOccurCalc', "start")

        try:
            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_mlist = [[0, ""]]
                    a_mlist[0][0] = 0
                    a_mlist[0][1] = g_meshList_check[a_cnt][1]
                    print('a_meshNo=' + a_mlist[0][1])
                    a_proc = multiprocessing.Process(target=clsFigure.MakeNIGeDaS_NonOccurCalc,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         a_mlist,
                                         0,
                                         0,
                                         -1
                                     ))
                    a_procs.append(a_proc)

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max

            '''
            # チェックされたものを処理対象
            a_proc = clsFigure.MakeNIGeDaS_NonOccurCalc(
                0,
                com.g_strIni,
                g_meshList_check,
                0,
                0,
                -1
            )
            '''
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeNIGeDaS_NonOccurCalc', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeNIGeDaS_NonOccurCalc', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeNIGeDaS_NonOccurCalc', "end")

    def _makeOverRainfall(
            self,
            h_key_Disaster,
            h_size_Disaster
    ):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall', "start")

        try:
            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_meshNo = g_meshList_check[a_cnt][1]
                    '''
                    a_split = g_meshList_check[a_cnt].split(',')
                    a_meshNo = ''
                    if (com.g_TargetRainMesh == 1):
                        # 対象Surfaceが1km
                        a_meshNo = a_split[1]
                    else:
                        # 対象Surfaceが5km
                        a_meshNo = a_split[0]
                        '''
                    print('a_meshNo=' + a_meshNo)
                    a_proc = multiprocessing.Process(target=clsFigure.MakeOverRainfallByMesh,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         h_key_Disaster,
                                         h_size_Disaster,
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
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall', "end")

    def _makeOverRainfall2(
            self,
            h_key_Disaster,
            h_size_Disaster,
            h_key_CautionAnnounce,
            h_size_CautionAnnounce
    ):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall2', "start")

        try:
            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_mlist = [[0, ""]]
                    a_mlist[0][0] = 0
                    a_mlist[0][1] = g_meshList_check[a_cnt][1]
                    print('a_meshNo=' + a_mlist[0][1])
                    a_proc = multiprocessing.Process(target=clsFigure.MakeOverRainfall2,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         h_key_Disaster,
                                         h_size_Disaster,
                                         h_key_CautionAnnounce,
                                         h_size_CautionAnnounce,
                                         a_mlist,
                                         0,
                                         0,
                                         -1
                                     ))
                    a_procs.append(a_proc)

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max

            '''
            # チェックされたものを処理対象
            a_proc = clsFigure.MakeOverRainfall2(
                0,
                com.g_strIni,
                g_meshList_check,
                0,
                0,
                -1
            )
            '''
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall2', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall2', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall2', "end")

    def _makeOverRainfall3_1(self):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall3_1', "start")

        try:
            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_mlist = [[0, ""]]
                    a_mlist[0][0] = 0
                    a_mlist[0][1] = g_meshList_check[a_cnt][1]
                    print('a_meshNo=' + a_mlist[0][1])
                    a_proc = multiprocessing.Process(target=clsFigure.MakeOverRainfall3_1,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         a_mlist,
                                         0,
                                         0,
                                         -1
                                     ))
                    a_procs.append(a_proc)

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max

            '''
            # チェックされたものを処理対象
            a_proc = clsFigure.MakeOverRainfall3_1(
                0,
                com.g_strIni,
                g_meshList_check,
                0,
                0,
                -1
            )
            '''
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall3_1', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall3_1', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall3_1', "end")

    def _makeOverRainfall3_2(
            self,
            h_key_Disaster,
            h_size_Disaster
    ):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall3_2', "start")

        try:
            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_mlist = [[0, ""]]
                    a_mlist[0][0] = 0
                    a_mlist[0][1] = g_meshList_check[a_cnt][1]
                    print('a_meshNo=' + a_mlist[0][1])
                    a_proc = multiprocessing.Process(target=clsFigure.MakeOverRainfall3_2,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         h_key_Disaster,
                                         h_size_Disaster,
                                         a_mlist,
                                         0,
                                         0,
                                         -1
                                     ))
                    a_procs.append(a_proc)

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max

            '''
            # チェックされたものを処理対象
            a_proc = clsFigure.MakeOverRainfall3_2(
                0,
                com.g_strIni,
                g_meshList_check,
                0,
                0,
                -1
            )
            '''
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall3_2', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall3_2', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall3_2', "end")

    def _makeOverRainfall8(self):
        global com
        global g_meshList_check

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall8', "start")

        try:
            # チェックされたものを処理対象
            a_meshSum = len(g_meshList_check)
            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_mlist = [[0, ""]]
                    a_mlist[0][0] = 0
                    a_mlist[0][1] = g_meshList_check[a_cnt][1]
                    print('a_meshNo=' + a_mlist[0][1])
                    # 予測雨量の算出
                    a_proc = multiprocessing.Process(target=clsFigure.MakeOverRainfall8,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         1,
                                         a_mlist,
                                         0,
                                         0,
                                         -1
                                     ))
                    a_procs.append(a_proc)

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max

            a_sum = 0
            while (a_sum < a_meshSum):
                a_cnt_max = (a_sum + com.g_MakeOverRainfallExecNum)
                if (a_cnt_max > a_meshSum):
                    a_cnt_max = a_meshSum

                print('***a_sum=' + str(a_sum) + ',a_cnt_max=' + str(a_cnt_max))
                a_procs = []
                a_proc_num = 0
                for a_cnt in range(a_sum, a_cnt_max):
                    a_proc_num += 1
                    #print('a_cnt=' + str(a_cnt))
                    a_mlist = [[0, ""]]
                    a_mlist[0][0] = 0
                    a_mlist[0][1] = g_meshList_check[a_cnt][1]
                    print('a_meshNo=' + a_mlist[0][1])
                    # 実況雨量の算出
                    a_proc = multiprocessing.Process(target=clsFigure.MakeOverRainfall8,
                                     args=(
                                         a_proc_num,
                                         com.g_strIni,
                                         0,
                                         a_mlist,
                                         0,
                                         0,
                                         -1
                                     ))
                    a_procs.append(a_proc)

                for a_proc in a_procs:
                    a_proc.start()
                for a_proc in a_procs:
                    a_proc.join()
                for a_proc in a_procs:
                    a_proc.terminate()

                print('All process is ended.')

                a_sum = a_cnt_max

            '''
            # チェックされたものを処理対象
            # 予測雨量の算出
            a_proc = clsFigure.MakeOverRainfall8(
                0,
                com.g_strIni,
                1,
                g_meshList_check,
                0,
                0,
                -1
            )
    
            # 実況雨量の算出
            a_proc = clsFigure.MakeOverRainfall8(
                0,
                com.g_strIni,
                0,
                g_meshList_check,
                0,
                0,
                -1
            )
            '''
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall8', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfall8', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfall8', "end")

    def _makeOverRainfallMix(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix', "start")

        try:
            a_proc = clsFigure.MakeOverRainfallMix(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix', "end")

    def _makeOverRainfallMix2(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix2', "start")

        try:
            a_proc = clsFigure.MakeOverRainfallMix2(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix2', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix2', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix2', "end")

    def _makeOverRainfallMix3_1(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix3_1', "start")

        try:
            a_proc = clsFigure.MakeOverRainfallMix3_1(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix3_1', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix3_1', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix3_1', "end")

    def _makeOverRainfallMix3_2(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix3_2', "start")

        try:
            a_proc = clsFigure.MakeOverRainfallMix3_2(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix3_2', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix3_2', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix3_2', "end")

    def _makeOverRainfallMix8(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix8', "start")

        try:
            # 予測雨量の算出
            a_proc = clsFigure.MakeOverRainfallMix8(
                0,
                com.g_strIni,
                1,
                g_meshList_list,
                0,
                -1
            )

            # 実況雨量の算出
            a_proc = clsFigure.MakeOverRainfallMix8(
                0,
                com.g_strIni,
                0,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix8', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeOverRainfallMix8', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeOverRainfallMix8', "end")

    def _makeWiff(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWiff', "start")

        try:
            a_proc = clsFigure.MakeWhiff(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWiff', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWiff', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWiff', "end")

    def _makeWiff_New(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWiff_New', "start")

        try:
            a_proc = clsFigure.MakeWhiff_New(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWiff_New', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWiff_New', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWiff_New', "end")

    def _makeWhiffFrequency(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWhiffFrequency', "start")

        try:
            a_proc = clsFigure.MakeWhiffFrequency(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWhiffFrequency', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWhiffFrequency', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWhiffFrequency', "end")

    def _makeWhiffFrequency_New(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWhiffFrequency_New', "start")

        try:
            a_proc = clsFigure.MakeWhiffFrequency_New(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWhiffFrequency_New', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWhiffFrequency_New', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWhiffFrequency_New', "end")

    def _makeWhiffTime(self):
        global com
        global g_meshList_list

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWhiffTime', "start")

        try:
            a_proc = clsFigure.MakeWhiffTime(
                0,
                com.g_strIni,
                g_meshList_list,
                0,
                -1
            )
        except Exception as exp:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWhiffTime', " ".join(map(str, exp.args)))
        except:
            com.Outputlog(com.g_LOGMODE_ERROR, '_makeWhiffTime', sys.exc_info())

        com.Outputlog(com.g_LOGMODE_TRACE1, '_makeWhiffTime', "end")


    # RBFNプログラム用入力データ
    def _makePanel_11(self):

        self.g_panel_11 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))

        self.g_button_11_1 = wx.Button(self.g_panel_11, wx.ID_ANY, "処理開始", size=(73, 25))
        self.g_button_11_2 = wx.Button(self.g_panel_11, wx.ID_ANY, "条件設定", size=(73, 25))
        self.g_button_11_1.Bind(wx.EVT_BUTTON, self._click_button_11_1)
        self.g_button_11_2.Bind(wx.EVT_BUTTON, self._click_button_11_2)

        self.g_listBox_11 = wx.ListCtrl(self.g_panel_11, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        #listmix.TextEditMixin(self.g_listBox_11)
        self.g_listBox_11.InsertColumn(0, "処理年", width=100)
        self.g_listBox_11.InsertColumn(1, "メッシュ数", width=100)
        self.g_listBox_11.InsertColumn(2, "メッシュ番号", width=150)
        self.g_listBox_11.InsertColumn(3, "状態", width=500)
        self.g_listBox_11.SetPosition(wx.Point(4, 50))
        #self.g_listBox_11.Bind(wx.EVT_LIST_ITEM_SELECTED, self._onSelect_listBox_11)

    # RBFN出力値の抽出処理
    def _makePanel_13(self):
        self.g_panel_13 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))

        self.g_button_13_1 = wx.Button(self.g_panel_13, wx.ID_ANY, "処理開始(抽出)", size=(100, 25))
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
        self.g_listBox_13_1 = CheckBoxList(self.g_panel_13, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        #self.g_listBox_13_1 = wx.ListCtrl(self.g_panel_13, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.g_listBox_13_1.InsertColumn(0, "対象メッシュ番号", width=100)
        self.g_listBox_13_1.InsertColumn(1, "開始年", width=100)
        self.g_listBox_13_1.InsertColumn(2, "終了年", width=100)
        self.g_listBox_13_1.InsertColumn(3, "状態", width=500)
        self.g_listBox_13_1.SetPosition(wx.Point(4, 50))

        self._set_listBox_13_1_year()

        ########################################################################
        # 集計
        ########################################################################
        self.g_listBox_13_2 = wx.ListCtrl(self.g_panel_13, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
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

        self.g_panel_21 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))

        self.g_button_21_1 = wx.Button(self.g_panel_21, wx.ID_ANY, "下限値・上限値再計算", size=(130, 25))
        self.g_button_21_2 = wx.Button(self.g_panel_21, wx.ID_ANY, "条件設定", size=(73, 25))
        self.g_button_21_1.Bind(wx.EVT_BUTTON, self._click_button_21_1)
        self.g_button_21_2.Bind(wx.EVT_BUTTON, self._click_button_21_2)

        self.g_listBox_21_1 = wx.ListCtrl(self.g_panel_21, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.g_listBox_21_1.InsertColumn(0, "メッシュ番号", width=100)
        self.g_listBox_21_1.SetPosition(wx.Point(4, 50))

        self.g_listBox_21_1.Bind(wx.EVT_LIST_ITEM_SELECTED, self._select_listBox_21_1)

        self.g_listBox_21_2 = wx.ListCtrl(self.g_panel_21, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.g_listBox_21_2.InsertColumn(0, "集計", format=wx.LIST_FORMAT_CENTER, width=150)
        self.g_listBox_21_2.InsertColumn(1, "0.9", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(2, "0.8", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(3, "0.7", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(4, "0.6", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(5, "0.5", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(6, "0.4", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(7, "0.3", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(8, "0.2", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(9, "0.1", format=wx.LIST_FORMAT_CENTER, width=60)
        self.g_listBox_21_2.InsertColumn(10, "発生降雨数", format=wx.LIST_FORMAT_CENTER, width=80)
        self.g_listBox_21_2.InsertColumn(11, "対象期間(年)", format=wx.LIST_FORMAT_CENTER, width=80)
        self.g_listBox_21_2.SetPosition(wx.Point(4 + 100 + 4, 50))

        statistics = [("全降雨の超過数", "", "", "", "", "", "", "", "", "", "", ""),
                      ("非発生降雨の超過数", "", "", "", "", "", "", "", "", "", "", ""),
                      ("発生降雨の超過数", "", "", "", "", "", "", "", "", "", "", ""),
                      ("災害捕捉率(%)", "", "", "", "", "", "", "", "", "", "", ""),
                      ("空振り率(%)", "", "", "", "", "", "", "", "", "", "", ""),
                      ("空振り頻度(回/年)", "", "", "", "", "", "", "", "", "", "", ""),
                      ("空振り時間(時間/年)", "", "", "", "", "", "", "", "", "", "", ""),
                      ("警報発表頻度(回/年)", "", "", "", "", "", "", "", "", "", "", ""),
                      ]
        i = 0
        for s in statistics:
            self.g_listBox_21_2.InsertItem(i, s[0])
            self.g_listBox_21_2.SetItem(i, 1, s[1])
            self.g_listBox_21_2.SetItem(i, 2, s[2])
            self.g_listBox_21_2.SetItem(i, 3, s[3])
            self.g_listBox_21_2.SetItem(i, 4, s[3])
            self.g_listBox_21_2.SetItem(i, 5, s[3])
            self.g_listBox_21_2.SetItem(i, 6, s[3])
            self.g_listBox_21_2.SetItem(i, 7, s[3])
            self.g_listBox_21_2.SetItem(i, 8, s[3])
            self.g_listBox_21_2.SetItem(i, 9, s[3])
            self.g_listBox_21_2.SetItem(i, 10, s[3])
            self.g_listBox_21_2.SetItem(i, 11, s[3])
            i += 1

        self.g_panel_21_sub1 = wx.Panel(self.g_panel_21, wx.ID_ANY, pos=(4 + 100 + 4, 50 + 190))
        self.g_panel_21_sub1.SetBackgroundColour(wx.WHITE)

# 集計結果
    def _makePanel_22(self):

        self.g_panel_22 = wx.Panel(self, wx.ID_ANY, pos=(0, 0))

        self.g_button_22_1 = wx.Button(self.g_panel_22, wx.ID_ANY, "全降雨の超過数", size=(130, 25))
        self.g_button_22_2 = wx.Button(self.g_panel_22, wx.ID_ANY, "非発生降雨の超過数", size=(130, 25))
        self.g_button_22_3 = wx.Button(self.g_panel_22, wx.ID_ANY, "発生降雨の超過数", size=(130, 25))
        self.g_button_22_4 = wx.Button(self.g_panel_22, wx.ID_ANY, "災害捕捉率", size=(130, 25))
        self.g_button_22_5 = wx.Button(self.g_panel_22, wx.ID_ANY, "空振り率", size=(130, 25))
        self.g_button_22_6 = wx.Button(self.g_panel_22, wx.ID_ANY, "空振り頻度", size=(130, 25))
        self.g_button_22_7 = wx.Button(self.g_panel_22, wx.ID_ANY, "空振り時間", size=(130, 25))
        self.g_button_22_8 = wx.Button(self.g_panel_22, wx.ID_ANY, "警報発表の頻度", size=(130, 25))
        self.g_button_22_9 = wx.Button(self.g_panel_22, wx.ID_ANY, "条件設定", size=(73, 25))
        self.g_button_22_1.Bind(wx.EVT_BUTTON, self._click_button_22_1)
        self.g_button_22_2.Bind(wx.EVT_BUTTON, self._click_button_22_2)
        self.g_button_22_3.Bind(wx.EVT_BUTTON, self._click_button_22_3)
        self.g_button_22_4.Bind(wx.EVT_BUTTON, self._click_button_22_4)
        self.g_button_22_5.Bind(wx.EVT_BUTTON, self._click_button_22_5)
        self.g_button_22_6.Bind(wx.EVT_BUTTON, self._click_button_22_6)
        self.g_button_22_7.Bind(wx.EVT_BUTTON, self._click_button_22_7)
        self.g_button_22_8.Bind(wx.EVT_BUTTON, self._click_button_22_8)
        self.g_button_22_9.Bind(wx.EVT_BUTTON, self._click_button_22_9)

        self.g_listBox_22_1 = wx.ListCtrl(self.g_panel_22, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.g_listBox_22_1.SetPosition(wx.Point(4, 50 + 20))

    # ブロック集計
    def _makePanel_23(self):

        self.g_panel_23 = wx.Panel(self, wx.ID_ANY)

    def _onClose(self, event):
        a_iRet = 0
        if (wx.MessageBox("プログラムを終了します。\nよろしいですか？", g_System_Title, wx.YES_NO) == wx.YES):
            if (self.g_shmlib != None):
                # 共有メモリ
                kernel32 = WinDLL("kernel32", use_last_error=True)
                kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
                kernel32.FreeLibrary(self.g_shmlib._handle)

            self.Destroy()

    def _onPaint(self, event):
        #dc = wx.PaintDC(self)
        #dc.DrawBitmap(self., 0, 0, True)
        self.Refresh(True)
        self.Update()
        #com.Outputlog(com.g_LOGMODE_INFORMATION, '_onPaint', "completed.")


    def _onSelect_listBox_11(self, event):
        self.g_listBox_11.SetFocusFromKbd()
        self.g_listBox_11.SetFocus()
        #self.g_listBox_11.SetScrollPos(wx.VERTICAL, self.g_listBox_11.GetItemCount() - 1, True)

    '''
    def _recalcLimit(self):
        Call GetRecalcLimitData(Me, a_strTmp, a_soilMin, a_rainMax)
        Call RecalcLimitByMesh(Me, Me.Picture1, Me.Picture2, a_sTFolder, a_soilMin, a_rainMax, 1, a_meshList2)
        '''

    def _refresh_self(self):
        '''
        a_size_src = self.GetSize()
        self.SetSize(a_size_src.width - 1, a_size_src.height - 1)
        self.SetSize(a_size_src.width, a_size_src.height)
        '''

        self.Iconize(True)
        self.Iconize(False)
        '''
        if (self.IsMaximized() == True):
            self.Maximize(False)
            self.Maximize(True)
        else:
            self.Maximize(True)
            self.Maximize(False)
            '''

    def _select_listBox_21_1(self, event):
        global g_meshSum_list
        global g_meshList_list

        print(event.Item.Text)
        self._set_listBox_21_2_year(event.Item.Text)

    def _set_listBox_13_1_year(self):
        global g_meshSum_list
        global g_meshList_list
        global g_meshList_check

        del g_meshList_check[:]

        if (self.g_listBox_13_1.GetItemCount() > 0):
            self.g_listBox_13_1.DeleteAllItems()

        for a_cnt in range(0, g_meshSum_list):
            self.g_listBox_13_1.InsertItem(a_cnt, g_meshList_list[a_cnt])
            self.g_listBox_13_1.SetItem(a_cnt, 1, str(com.g_TargetStartYear))
            self.g_listBox_13_1.SetItem(a_cnt, 2, str(com.g_TargetEndYear))
            self.g_listBox_13_1.SetItem(a_cnt, 3, "待機中")
            self.g_listBox_13_1.SetItemTextColour(a_cnt, wx.BLACK)
            #self.g_listBox_13_1.SetItemTextColour(a_cnt, wx.GREEN)
            self.g_listBox_13_1.CheckItem(a_cnt, True)
        self.g_listBox_13_1.Update()

    def _set_listBox_13_2_year(self):
        a_size = self.g_listBox_13_2.GetItemCount()
        for a_i in range(0, a_size):
            self.g_listBox_13_2.SetItem(a_i, 1, str(com.g_TargetStartYear))
            self.g_listBox_13_2.SetItem(a_i, 2, str(com.g_TargetEndYear))
            self.g_listBox_13_2.SetItem(a_i, 3, "待機中")
            self.g_listBox_13_2.SetItemTextColour(a_i, wx.BLACK)
        self.g_listBox_13_2.Update()

    def _set_listBox_21_1_year(self):
        global g_meshSum_list
        global g_meshList_list

        if (self.g_listBox_21_1.GetItemCount() > 0):
            self.g_listBox_21_1.DeleteAllItems()

        for a_cnt in range(0, g_meshSum_list):
            self.g_listBox_21_1.InsertItem(a_cnt, g_meshList_list[a_cnt])
        self.g_listBox_21_1.Update()

    def _set_listBox_21_2_year(self, h_meshNo):

        if (h_meshNo == ""):
            self._dispStatisticsByMesh("")
            if (self.g_bitmap != None):
                # 画像の消去ができない：pending
                self.g_bitmap.Destroy()
                self.g_panel_21_sub1.Destroy()
                self.g_panel_21_sub1 = wx.Panel(self.g_panel_21, wx.ID_ANY, pos=(4 + 100 + 4, 50 + 190))
                self.g_panel_21_sub1.SetBackgroundColour(wx.WHITE)
                size = self.GetSize()
                self.g_panel_21_sub1.SetSize(size.width - 24 - 100 - 4 - 1, size.height - (50 + 60) - 190)
                #self.Refresh()
            self.g_bitmap = None
            self.g_panel_21_sub1.Refresh()
            return

        if (os.path.exists(com.g_OutPath + "\\" + com.g_ContourSnakeSymbol + "-" + h_meshNo + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".bmp") == False):
            wx.MessageBox("該当メッシュ【" + h_meshNo + "】は、RBFN出力値の抽出処理が行われていません！", g_System_Title)
            return

        self._dispStatisticsByMesh(h_meshNo)

        a_image = wx.Image(com.g_OutPath + "\\" + com.g_ContourSnakeSymbol + "-" + h_meshNo + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".bmp")
        self.g_bitmap = a_image.ConvertToBitmap()
        wx.StaticBitmap(self.g_panel_21_sub1, -1, self.g_bitmap, (4, 4), a_image.GetSize())
        self.g_panel_21_sub1.Refresh()
        #wx.StaticBitmap(self, -1, self.bitmap, (4 + 100, 190), self.GetClientSize())
        #self.SetSize(a_image.GetSize())

        #img = Image.open(com.g_OutPath + "\\" + com.g_ContourSnakeSymbol + "-" + h_meshNo + "-" + str(com.g_TargetStartYear) + "-" + str(com.g_TargetEndYear) + ".bmp")
        #img.show()

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