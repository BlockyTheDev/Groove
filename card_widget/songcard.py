import sys

from PyQt5.QtCore import QEvent, QPoint, Qt
from PyQt5.QtGui import QContextMenuEvent, QIcon, QMouseEvent, QResizeEvent
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

sys.path.append('..')
from Groove.card_widget.songcard_sub_unit import SongNameCard, YearTconDurationCard
from Groove.my_widget.my_label import ClickableLabel

class SongCard(QWidget):
    """ 定义一个歌曲卡类 """

    def __init__(self, songInfo_dict:dict):
        super().__init__()

        # 设置item被点击标志位
        self.isClicked=False

        # 实例化小部件
        self.song_name_card = SongNameCard(songInfo_dict['songName'],self)
        self.songerLabel = ClickableLabel(songInfo_dict['songer'], self)
        self.albumLabel = ClickableLabel(songInfo_dict['album'][0], self)
        self.yearTconDuration = YearTconDurationCard(
            songInfo_dict['year'], songInfo_dict['tcon'], songInfo_dict['duration'],self)

        # 实例化布局
        self.all_h_layout = QHBoxLayout()
        self.right_h_layout = QHBoxLayout()

        # 初始化小部件
        self.initWidget()

        # 初始化布局
        self.initLayout()
        self.setQss()

    def initLayout(self):
        """ 初始化布局 """

        # 设置右侧的布局
        self.right_h_layout.addWidget(self.songerLabel, 0, Qt.AlignLeft)
        self.right_h_layout.addSpacing(13)
        self.right_h_layout.addWidget(self.albumLabel, 0, Qt.AlignLeft)
        self.right_h_layout.addWidget(self.yearTconDuration)

        # 设置全局布局
        self.all_h_layout.addWidget(self.song_name_card)
        self.all_h_layout.addLayout(self.right_h_layout)
        self.all_h_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.all_h_layout)

        self.resizetimes = 0

    def initWidget(self):
        """ 初始化小部件 """

        self.songerLabel.setFixedWidth(190)
        self.albumLabel.setFixedWidth(190)

        # 设置鼠标的光标
        self.songerLabel.setCursor(Qt.PointingHandCursor)
        self.albumLabel.setCursor(Qt.PointingHandCursor)

        # 分配ID
        self.songerLabel.setObjectName('songerLabel')
        self.albumLabel.setObjectName('albumLabel')
        self.setObjectName('songCard')

        # 将复选框的选中信号连接到槽函数
        self.song_name_card.songNameCheckBox.stateChanged.connect(self.checkStateChangeEvent)

        # 安装事件过滤器
        self.installEventFilter(self)

    def updateSongCard(self, songInfo_dict: dict):
        """ 更新songCard的信息 """
        self.song_name_card.songNameCheckBox.setText(songInfo_dict['songName'])
        self.songerLabel.setText(songInfo_dict['songer'])
        self.albumLabel.setText(songInfo_dict['album'][0])
        self.yearTconDuration.updateLabelText(songInfo_dict)
        self.update()

    def setQss(self):
        """ 设置初始层叠样式 """
        with open('resource\\css\\songCard.qss', 'r', encoding='utf-8') as f:
            qss = f.read()
            self.setStyleSheet(qss)

    def setClickableLabelState(self,labelState='unClicked'):
        """ 设置歌手和专辑这两个可点击标签state属性的状态 """
        self.songerLabel.setProperty('state', labelState)
        self.albumLabel.setProperty('state', labelState)

    def setLeaveStateQss(self):
        """ 设置离开且未被点击时的样式 """
        self.isClicked = False

        # 更新小部件样式
        self.song_name_card.setWidgetState()
        self.yearTconDuration.setWidgetState()
        self.setClickableLabelState()
        self.setStyle(QApplication.style())

        # 隐藏按钮
        self.song_name_card.setAllButtonHidden()
        
        # 更新按钮图标
        self.song_name_card.addToButton.setIcon(
            QIcon('resource\\images\\black_addTo_bt.png'))
        self.song_name_card.playButton.setIcon(
            QIcon('resource\\images\\black_play_bt.png'))

    def setEnterStateQss(self):
        """ 设置进入且未被点击时的样式 """
        self.isClicked = False

        # 更新小部件样式
        self.song_name_card.setWidgetState('enter and unClicked')
        self.yearTconDuration.setWidgetState()
        self.setClickableLabelState()
        self.setStyle(QApplication.style())

        # 显示按钮
        self.song_name_card.setAllButtonHidden(False)
        
        # 更新按钮图标
        self.song_name_card.addToButton.setIcon(
            QIcon('resource\\images\\black_addTo_bt.png'))
        self.song_name_card.playButton.setIcon(
            QIcon('resource\\images\\black_play_bt.png'))

    def setClickedStateQss(self):
        """ 设置选中状态时的样式 """
        self.isClicked = True
        self.song_name_card.setWidgetState('clicked', 'clicked')
        self.yearTconDuration.setWidgetState('clicked')
        self.setClickableLabelState('clicked')
        self.song_name_card.addToButton.setIcon(
            QIcon('resource\\images\\white_add_to_bt.png'))
        self.song_name_card.playButton.setIcon(
            QIcon('resource\\images\\white_play_bt.png'))
        # 更新样式
        self.setStyle(QApplication.style())

    def eventFilter(self, obj, event):
        """ 当鼠标点击歌曲卡时将文本换成白色 """
        if obj == self:
            if event.type() == QEvent.Enter and not self.song_name_card.contextMenuSelecting:
                # 如果歌曲卡没有被选中且鼠标进入歌曲卡就更新样式
                if not self.isClicked:
                    self.setEnterStateQss()
            elif event.type() == QEvent.Leave:
                # 如果歌曲卡没有被点击且鼠标移出歌曲卡就更新样式
                if not self.isClicked:
                    self.setLeaveStateQss()
            elif event.type() == QEvent.MouseButtonPress:
                if not self.isClicked:
                    self.setClickedStateQss()

        return False

    def resizeEvent(self, e: QResizeEvent):
        """ 窗口大小改变时就改变专辑和歌手名标签的长度 """
        # 初始化时会改变大小
        self.resizetimes += 1

        if self.resizetimes == 2:
            self.originalWidth = self.width()
        if self.resizetimes > 2:
            deltaWidth = self.width() - self.originalWidth
            self.originalWidth = self.width()
            # 分配多出来的宽度
            self.albumLabel.setFixedWidth(
                int(self.albumLabel.width() + 0.7*deltaWidth))
            self.songerLabel.setFixedWidth(
                int(self.songerLabel.width() + 0.2*deltaWidth))

    def checkStateChangeEvent(self):
        """ 复选框的状态改变时更改歌曲卡的样式 """
        if self.song_name_card.songNameCheckBox.isChecked():
            self.setClickedStateQss()
            # 选中复选框时隐藏所有按钮
            self.song_name_card.setAllButtonHidden()
        else:
            self.setLeaveStateQss()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SongCard('猫じゃらし', 'RADWIMPS', '泠鸢yousa、鹿乃、花丸晴琉、神楽七奈、物述有栖、白上吹雪、夏色祭',
                    'ロック', '2020', '4:02')
    demo.show()
    sys.exit(app.exec_())