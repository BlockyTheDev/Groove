# coding:utf-8
from common.config import config
from common.signal_bus import signalBus
from PyQt5.QtCore import QPointF, QPropertyAnimation, Qt, pyqtProperty
from PyQt5.QtGui import (QColor, QFont, QFontMetrics, QPainter, QPainterPath,
                         QPen)
from PyQt5.QtWidgets import QWidget


class LyricWidget(QWidget):
    """ Lyric widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.lyric = []
        self.duration = 0
        self.__originMaskWidth = 0
        self.__translationMaskWidth = 0
        self.__originTextX = 0
        self.__translationTextX = 0

        self.originMaskWidthAni = QPropertyAnimation(
            self, b'originMaskWidth', self)
        self.translationMaskWidthAni = QPropertyAnimation(
            self, b'translationMaskWidth', self)
        self.originTextXAni = QPropertyAnimation(
            self, b'originTextX', self)
        self.translationTextXAni = QPropertyAnimation(
            self, b'translationTextX', self)

        signalBus.desktopLyricStyleChanged.connect(self.update)

    def paintEvent(self, e):
        if not self.lyric:
            return

        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.TextAntialiasing)

        # draw original lyric
        self.__drawLyric(
            painter,
            self.originTextX,
            config.get(config.deskLyricFontSize),
            self.originMaskWidth,
            self.originFont,
            self.lyric[0]
        )

        if not self.hasTranslation():
            return

        # draw translation lyric
        self.__drawLyric(
            painter,
            self.translationTextX,
            25 + config.get(config.deskLyricFontSize)*5/3,
            self.translationMaskWidth,
            self.translationFont,
            self.lyric[1]
        )

    def __drawLyric(self, painter: QPainter, x, y, width, font: QFont, text: str):
        """ draw lyric """
        painter.setFont(font)

        # draw background text
        path = QPainterPath()
        path.addText(QPointF(x, y), font, text)
        painter.strokePath(path, QPen(
            config.get(config.deskLyricStrokeColor), config.get(config.deskLyricStrokeSize)))
        painter.fillPath(path, config.get(config.deskLyricFontColor))

        # draw foreground text
        painter.fillPath(
            self.__getMaskedLyricPath(path, width),
            config.get(config.deskLyricHighlightColor)
        )

    def __getMaskedLyricPath(self, path: QPainterPath, width: float):
        """ get the masked lyric path """
        subPath = QPainterPath()
        rect = path.boundingRect()
        rect.setWidth(width)
        subPath.addRect(rect)
        return path.intersected(subPath)

    def setLyric(self, lyric: list, duration: int, update=False):
        """ set lyric

        Parameters
        ----------
        lyric: list
            list contains original lyric and translation lyric

        duration: int
            lyric duration in milliseconds

        update: bool
            update immediately or not
        """
        self.lyric = lyric or [""]
        self.duration = max(duration, 1)
        self.__originMaskWidth = 0
        self.__translationMaskWidth = 0

        # stop running animations
        for ani in self.findChildren(QPropertyAnimation):
            if ani.state() == ani.Running:
                ani.stop()

        # start scroll animation if text is too long
        fontMetrics = QFontMetrics(self.originFont)
        w = fontMetrics.width(lyric[0])
        if w > self.width():
            x = self.width() - w
            self.__setAnimation(self.originTextXAni, 0, x)
        else:
            self.__originTextX = self.__getLyricX(w)
            self.originTextXAni.setEndValue(None)

        # start foreground color animation
        self.__setAnimation(self.originMaskWidthAni, 0, w)

        if self.hasTranslation():
            fontMetrics = QFontMetrics(self.translationFont)
            w = fontMetrics.width(lyric[1])
            if w > self.width():
                x = self.width() - w
                self.__setAnimation(self.translationTextXAni, 0, x)
            else:
                self.__translationTextX = self.__getLyricX(w)
                self.translationTextXAni.setEndValue(None)

            self.__setAnimation(self.translationMaskWidthAni, 0, w)

        if update:
            self.update()

    def __getLyricX(self, w: float):
        """ get the x coordinate of lyric """
        alignment = config.get(config.deskLyricAlignment)
        if alignment == "Right":
            return self.width() - w
        elif alignment == "Left":
            return 0

        return self.width()/2 - w/2

    def getOriginMaskWidth(self):
        return self.__originMaskWidth

    def getTranslationMaskWidth(self):
        return self.__translationMaskWidth

    def getOriginTextX(self):
        return self.__originTextX

    def getTranslationTextX(self):
        return self.__translationTextX

    def setOriginMaskWidth(self, pos: int):
        self.__originMaskWidth = pos
        self.update()

    def setTranslationMaskWidth(self, pos: int):
        self.__translationMaskWidth = pos
        self.update()

    def setOriginTextX(self, pos: int):
        self.__originTextX = pos
        self.update()

    def setTranslationTextX(self, pos):
        self.__translationTextX = pos
        self.update()

    def __setAnimation(self, ani: QPropertyAnimation, start, end):
        if ani.state() == ani.Running:
            ani.stop()

        ani.setStartValue(start)
        ani.setEndValue(end)
        ani.setDuration(self.duration)

    def setPlay(self, isPlay: bool):
        """ set the play status of lyric """
        for ani in self.findChildren(QPropertyAnimation):
            if isPlay and ani.state() != ani.Running and ani.endValue() is not None:
                ani.start()
            elif not isPlay and ani.state() == ani.Running:
                ani.pause()

    def hasTranslation(self):
        return len(self.lyric) == 2

    def minimumHeight(self) -> int:
        size = config.get(config.deskLyricFontSize)
        h = size/1.5+60 if self.hasTranslation() else 40
        return int(size+h)

    @property
    def originFont(self):
        return config.desktopLyricFont

    @property
    def translationFont(self):
        font = QFont(config.get(config.deskLyricFontFamily))
        font.setPixelSize(config.get(config.deskLyricFontSize)//1.5)
        return font

    originMaskWidth = pyqtProperty(
        float, getOriginMaskWidth, setOriginMaskWidth)
    translationMaskWidth = pyqtProperty(
        float, getTranslationMaskWidth, setTranslationMaskWidth)
    originTextX = pyqtProperty(float, getOriginTextX, setOriginTextX)
    translationTextX = pyqtProperty(
        float, getTranslationTextX, setTranslationTextX)
