# -*- coding: UTF-8 -*- 
class Lz77:
    def __init__(self, inputStr):
        self.inputStr = inputStr#输入流
        self.searchBuffer = 5    #搜索缓冲区(已编码区)大小
        self.lookaheadBuffer = 3     #lookAhead缓冲区（待编码区）大小
        self.windSpiltIndex = 0 #lookHead缓冲区开始的索引
        self.move = 0
        self.notFind = -1   #没有找到匹配字符串
 
    #得到滑动窗口的末端索引
    def getWinEndIndex(self):
        return self.windSpiltIndex + self.lookaheadBuffer
 
    #得到滑动窗口的始端索引
    def getWinStartIndex(self):
        return self.windSpiltIndex - self.searchBuffer
 
    #判断lookHead缓冲区是否为空
    def isLookHeadEmpty(self):
        return True if self.windSpiltIndex + self.move> len(self.inputStr) - 1   else False
 
    def encoding(self):
        step = 1
        j = 0
        m = 0
        List = [[0,0,0]]
        print("Step   Position   Match   Output")
        while not self.isLookHeadEmpty():
            #1.滑动窗口
            self.winMove()
            #2. 得到最大匹配串的偏移值和长度
            (offset, matchLen) = self.findMaxMatch()
            #3.设置窗口下一步需要滑动的距离
            self.setMoveSteps(matchLen)
            if matchLen == 0:
                #匹配为0，说明无字符串匹配，输出下一个需要编码的字母
                nextChar = self.inputStr[self.windSpiltIndex]
                result = (step, self.windSpiltIndex, '-',  '(0,0)' + nextChar)
                list = [0,0,nextChar]
                List.append(list)
            else:
                result = (step, self.windSpiltIndex, self.inputStr[self.windSpiltIndex - offset: self.windSpiltIndex - offset + matchLen], '(' + str(offset) + ',' + str(matchLen) + ')')
                list = [str(offset),str(matchLen),self.inputStr[self.windSpiltIndex - offset: self.windSpiltIndex - offset + matchLen]]
                List.append(list)
            #4.输出结果
            self.output(result)  
            step = step + 1        #仅用来设置第几步
	print List
	for tmp in List:
		open('test.txt','w').write(tmp).close()
	
    #滑动窗口(移动分界点)
    def winMove(self):
        self.windSpiltIndex = self.windSpiltIndex + self.move
 
    #寻找最大匹配字符并返回相对于窗口分界点的偏移值和匹配长度
    def findMaxMatch(self):
        matchLen = 0
        offset = 0
        minEdge = self.minEdge() + 1  #得到编码区域的右边界
        #遍历待编码区，寻找最大匹配串
        for i in range(self.windSpiltIndex + 1, minEdge):
            #print("i: %d" %i)
            offsetTemp = self.searchBufferOffest(i)
            if offsetTemp == self.notFind:
                return (offset, matchLen)
            offset = offsetTemp #偏移值
 
            matchLen = matchLen + 1  #每找到一个匹配串，加1
 
        return (offset, matchLen)
 
    #入参字符串是否存在于搜索缓冲区，如果存在，返回匹配字符串的起始索引
    def searchBufferOffest(self, i):
        searchStart = self.getWinStartIndex()
        searchEnd = self.windSpiltIndex
        #下面几个if是处理开始时的特殊情况
        if searchEnd < 1:
            return self.notFind
        if searchStart < 0:
            searchStart = 0
            if searchEnd == 0:
                searchEnd = 1
        searchStr = self.inputStr[searchStart : searchEnd]  #搜索区字符串
        findIndex = searchStr.find(self.inputStr[self.windSpiltIndex : i])
        if findIndex == -1:
            return -1
        return len(searchStr) - findIndex
 
    #设置下一次窗口需要滑动的步数
    def setMoveSteps(self, matchLen):
        if matchLen == 0:
            self.move = 1
        else:
            self.move = matchLen
 
    def minEdge(self):
        return len(self.inputStr)  if len(self.inputStr) - 1 < self.getWinEndIndex() else self.getWinEndIndex() + 1
 
    def output(self, touple):#输出到文件
		print("%d      %d           %s     %s" % touple)
		

import lz77_inputStr#导入文件
 
if __name__ == "__main__":
    lz77 = Lz77(lz77_inputStr.fileStr)
    lz77.encoding()
