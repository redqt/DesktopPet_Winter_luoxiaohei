import json
import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
# 导入QT,其中包含一些常量，例如颜色等
from PyQt5.QtCore import Qt
# 导入常用组件
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from threading import Thread
# 使用调色板等
from PyQt5.QtGui import QIcon, QMovie
import time
import webbrowser
import os
import random
import subprocess


class DemoWin(QMainWindow):
    def __init__(self):
        super(DemoWin, self).__init__()
        self.initUI()
        # 初始化，不规则窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 是否跟随鼠标
        self.is_follow_mouse = False
        self.move(1650, 20)

        # 设置托盘选项
        iconpath = "./mypetico.ico"
        # 右键菜单
        quit_action = QAction(u'退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(iconpath))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(iconpath))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        # 窗口透明程度
        self.setWindowOpacity(1)

        # 每隔一段时间做个动作
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(5000)
        self.condition = 0
        self.talk_condition = 0

        self.pet1 = []
        for i in os.listdir("pet"):
            self.pet1.append("pet/" + i)
        self.pet1.remove("pet/init")

    def initUI(self):
        # 将窗口设置为动图大小
        self.resize(400, 400)
        self.label1 = QLabel("", self)
        self.label1.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")  # 设置边框
        # 使用label来显示动画
        self.label = QLabel("", self)
        # label大小设置为动画大小
        self.label.setFixedSize(200, 200)
        self.Action("./pet/init/start.gif")
        self.setWindowTitle("myPet")

    '''鼠标左键按下时, 宠物将和鼠标位置绑定'''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            self.Action("./pet/init/move.gif")

    '''鼠标移动, 则宠物也移动'''
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    '''鼠标释放时, 取消绑定'''
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            return
        self.Action("./pet/init/stay.gif")
        self.is_follow_mouse = False
        self.setCursor(Qt.OpenHandCursor)

    def enterEvent(self, event):  # 鼠标移进时调用
        # print('鼠标移入')
        self.setCursor(Qt.OpenHandCursor)

    def execute_action(self, action_config):
        print(action_config)
        if action_config['type'] == 'subprocess.run':
            subprocess.run(action_config['params'], shell=True)
        elif action_config['type'] == 'webbrowser':
            webbrowser.open(action_config['params'])
        elif action_config['type'] == 'subprocess.Popen':
            subprocess.Popen(action_config['params'], creationflags=subprocess.CREATE_NEW_CONSOLE)

    def contextMenuEvent(self, event):
        menus = []
        actions = []
        action_configs = []
        # 读取配置文件
        try:
            with open("./config/menu_config.json", "r", encoding="utf-8") as config:
                menu_config = json.load(config)
        except Exception as e:
            print(e)
            return

        # 获取子菜单项
        for menu in menu_config:
            # print(menu)
            menus.append(QMenu(str(menu), self))
            # 获取action
            for action_config in menu_config[menu]:
                # print(action_config)
                action_configs.append(action_config)
                actions.append(menus[-1].addAction(action_config["name"]))

        for i, menu in enumerate(menus):
            if i == 0:
                continue
            menus[0].addMenu(menu)

        quitAction = menus[0].addAction("退出")
        action = menus[0].exec_(self.mapToGlobal(event.pos()))

        if action in actions:
            self.execute_action(action_configs[actions.index(action)])

        if action == quitAction:
            qApp.quit()

    '''退出程序'''
    def quit(self):
        self.close()
        sys.exit()

    def Action(self, action):
        # 设置动画路径
        self.movie = QMovie(action)
        # 宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.label.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()

    '''随机做一个动作'''
    def randomAct(self):
        if not self.condition:
            print("状态变更")
            print(random.choice(self.pet1))
            self.Action(random.choice(self.pet1))
            self.condition = 1
        else:
            print("状态还原")
            self.Action("pet/init/stay.gif")
            self.condition = 0
        self.timer.start(random.randint(10, 30) * 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("1.jpg"))
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())
