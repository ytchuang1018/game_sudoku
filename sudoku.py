# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 11:16:54 2021

@author: Skye
"""

import wx 
class sudoku_win(wx.Frame): 
            
   def __init__(self, parent, title): 
      super(sudoku_win, self).__init__(parent, title = title,size = (490,530))
		
      self.splitter = wx.SplitterWindow(self,-1)
      self.splitter_top = wx.SplitterWindow(self.splitter, -1) 
      
      self.panel1_top = wx.Panel(self.splitter_top, -1, size=(450,450),style=wx.BORDER_RAISED) 
		
      gridBox = wx.GridSizer(9,1,5,5)
      labels=['1','2','3','4','5','6','7','8','9']
    
      for label in labels:
          buttonItem = wx.Button(self.panel1_top, label=label)
          buttonItem.Disable()
          gridBox.Add(buttonItem, 1, wx.EXPAND)

      self.panel1_top.SetSizerAndFit(gridBox)
      
      self.panel2_top = wx.Panel(self.splitter_top, -1, size=(450,60),style=wx.BORDER_RAISED) 
		
      gridBox = wx.GridSizer(9,9,2,2)
        
      self.board=[
       [0,0,0,4,0,8,0,0,0],
       [9,0,6,8,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,8],
       [0,0,3,0,0,2,0,7,0],
       [0,0,9,0,3,0,7,0,0],
       [0,4,0,7,0,0,1,0,0],
       [7,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,4,0,0,6],
       [0,0,0,3,0,5,0,0,0]
       ]
      
      color_board=[
          ['1', '1', '2', '2', '2', '2', '2', '3', '3'],
          ['1', '1', '1', '4', '2', '2', '3', '3', '3'],
          ['1', '1', '4', '4', '2', '2', '3', '3', '3'],
          ['1', '4', '4', '4', '4', '5', '5', '3', '5'],
          ['1', '4', '6', '4', '5', '5', '5', '5', '5'],
          ['7', '7', '6', '6', '5', '6', '6', '8', '8'],
          ['7', '7', '7', '6', '6', '6', '6', '8', '8'],
          ['7', '7', '7', '7', '9', '8', '8', '8', '8'],
          ['9', '9', '9', '9', '9', '9', '9', '9', '8']
          ]
      
      dict = {'1': (216,206,27), '2': (26,217,207), '3': (230,0,115),
              '4':(255,119,187),'5':(183,53,232),'6':(0,0,255),
              '7':(5,224,131),'8':(255,128,192),'9':(45,186,210)}
      
      font = wx.Font(30, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, 
                     'Arial')
        
      for x in range(len(self.board)):
         for y in range(len(self.board[x])):
            Map_i_j = "self.Map_" + "%d" %x + "_" +"%d" %y
            if self.board[x][y]!=0:
                exec(Map_i_j + "=wx.TextCtrl(self.panel2_top, -1, str(self.board[x][y]),size=(50,50),style=wx.TE_READONLY|wx.ALIGN_CENTRE_HORIZONTAL)")
                exec(Map_i_j + ".SetBackgroundColour(dict[color_board[x][y]])")
                exec(Map_i_j + ".SetFont(font)")
            else:
                exec(Map_i_j + " = wx.TextCtrl(self.panel2_top,-1, '""',size=(50,50),style=wx.ALIGN_CENTRE_HORIZONTAL)")
                exec(Map_i_j + ".SetBackgroundColour(dict[color_board[x][y]])")
                exec(Map_i_j + ".SetFont(font)")
            exec("gridBox.Add(" + Map_i_j + ", 1, wx.EXPAND,border=1)")
            
      self.panel2_top.SetSizer(gridBox) 
      self.panel2_top.SetBackgroundColour('black')
      self.panel2_top.Centre()
      self.panel2_top.Fit()
      self.splitter_top.SplitVertically(self.panel2_top, self.panel1_top) 
      
      splitter_Bottom = wx.Panel(self.splitter, style=wx.SUNKEN_BORDER)
      
      b = wx.BoxSizer(wx.HORIZONTAL) 
      self.solve_Button = wx.Button(splitter_Bottom,label="solve",size=(450,40))
      self.solve_Button.SetBackgroundColour((221,72,0))
      self.solve_Button.Bind(wx.EVT_BUTTON, self.btn_onclick)
      b.Add(self.solve_Button, 1, wx.EXPAND|wx.CENTER)
      splitter_Bottom.SetSizer(b)
      
      self.splitter.SplitHorizontally(self.splitter_top, splitter_Bottom, 450)
      self.splitter_top.SplitVertically(self.panel1_top, self.panel2_top, 500)
      
      self.Centre()  
      self.Show(True)
   
   def btn_onclick(self,event):
      labels = event.GetEventObject().GetLabel()
      item = "solve close"
      if labels not in item:
          #print(event.GetEventObject())
          pass
      elif labels == "solve":
          m=sudoku(self.board)
          self.fill_solve(m)
          print("solve done!")
          self.solve_Button.SetLabel("close")
      elif labels == "close":
          self.Close()
    
   def fill_solve(self,m):
        
      self.board=m
      for x in range(len(self.board)):
         for y in range(len(self.board[x])):
            Map_i_j = "self.Map_" + "%d" %x + "_" +"%d" %y
            exec(Map_i_j + ".SetValue(str(m[x][y]))")
            
def get_next(m, x, y):
    """ 功能：获得下一个空白格在数独中的坐标。       
    """
    for next_y in range(y+1, 9):  # 下一个空白格和当前格在一行的情况
        if m[x][next_y] == 0:
            return x, next_y
    for next_x in range(x+1, 9):  # 下一个空白格和当前格不在一行的情况
        for next_y in range(0, 9):
            if m[next_x][next_y] == 0:
                return next_x, next_y
    return -1, -1               # 若不存在下一个空白格，则返回 -1，-1

def index_2d(myList, v):
    return [[x, y] for x, li in enumerate(myList) for y, val in enumerate(li) if val==v]

def value(m, x, y):
    """ 功能：返回符合"每个横排和竖排以及
              九宫格内无相同数字"这个条件的有效值。
    """ 
    ii=[[1,1,2,2,2,2,2,3,3],
    [1,1,1,4,2,2,3,3,3],
    [1,1,4,4,2,2,3,3,3],
    [1,4,4,4,4,5,5,3,5],
    [1,4,6,4,5,5,5,5,5],
    [7,7,6,6,5,6,6,8,8],
    [7,7,7,6,6,6,6,8,8],
    [7,7,7,7,9,8,8,8,8],
    [9,9,9,9,9,9,9,9,8]]
    
    a=index_2d(ii,ii[x][y])
    #i, j = x//3, y//3
    #grid = [m[i*3+r][j*3+c] for r in range(3) for c in range(3)]
    grid = [m[a[r][0]][a[r][1]] for r in range(len(a))]
    v = set([x for x in range(1,10)]) - set(grid) - set(m[x]) - \
        set(list(zip(*m))[y])    
    return list(v)


def start_pos(m):
    """ 功能：返回第一个空白格的位置坐标"""
    for x in range(9):
        for y in range(9):
            if m[x][y] == 0:
                return x, y
    return False  # 若数独已完成，则返回 False, False

def try_sudoku(m, x, y):
    """ 功能：试着填写数独 """
    for v in value(m, x, y):
        m[x][y] = v
        next_x, next_y = get_next(m, x, y)
        if next_y == -1: # 如果无下一个空白格
            return True
        else:
            end = try_sudoku(m, next_x, next_y) # 递归
            if end:
                return True
            m[x][y] = 0 # 在递归的过程中，如果数独没有解开，
                        # 则回溯到上一个空白格

def sudoku(m):        
    x, y = start_pos(m)
    try_sudoku(m, x, y)
    return m
   
if __name__ == '__main__':	
    ex = wx.App() 
    sudoku_win(None,'sudoku') 
    ex.MainLoop()
