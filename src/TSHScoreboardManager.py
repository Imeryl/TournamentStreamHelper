from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from loguru import logger

from .TSHScoreboardWidget import TSHScoreboardWidget
from .StateManager import StateManager

class TSHScoreboardManagerSignals(QObject):
    ScoreboardAmountChanged = Signal(int)

class TSHScoreboardManager(QDockWidget):
    instance: "TSHScoreboardManager" = None


    def __init__(self, *args):
        super().__init__(*args)
        
        StateManager.Unset("score")

        self.signals: TSHScoreboardManagerSignals = TSHScoreboardManagerSignals()
        logger.info("Scoreboard Manager - Initializing")

        self.setWindowTitle(QApplication.translate("app", "Scoreboard Manager"))
        self.setFloating(True)
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.widget = QWidget()
        self.setWidget(self.widget)
        self.widget.setLayout(QVBoxLayout())

        self.tabs = QTabWidget()
        self.widget.layout().addWidget(self.tabs)

        self.signals.ScoreboardAmountChanged.connect(
            lambda val: self.UpdateAmount(val)
        )

        self.scoreboardholder = []

    def UpdateAmount(self, amount):
        if amount > len(self.scoreboardholder):
            logger.info("Scoreboard Manager - Creating Scoreboard " + str(amount))
            
            scoreboard = QWidget()
            scoreboard.setLayout(QVBoxLayout())
            scoreboardObj = TSHScoreboardWidget(scoreboardNumber=amount)
            self.scoreboardholder.append(scoreboardObj)
            scoreboard.layout().addWidget(scoreboardObj)
            self.tabs.addTab(scoreboard
                 , QApplication.translate("app", "Scoreboard") + " " + str(amount))
        else:
            logger.info("Scoreboard Manager - Removing Scoreboard " + str(amount+1))
            self.tabs.removeTab(amount)
            self.scoreboardholder[amount].deleteLater()
            self.scoreboardholder.pop(amount)
            StateManager.Unset(f"score.{amount+1}")

    def GetScoreboard(self, number):
        if int(number)-1 < len(self.scoreboardholder):
            return self.scoreboardholder[int(number)-1]
        else:
            logger.error(f"Scoreboard Manager - Unable to retrieve scoreboard {number}, defaulting to scoreboard 1")
            return self.scoreboardholder[0]
        
    def SetTabName(self, index, name):
        if int(index)-1 < len(self.tabs):
            self.tabs.setTabText(int(index)-1, name)
        else:
            logger.error(f"Invalid Scoreboard ID provided: {index}")
            logger.error(f"Please provide an ID between 1 and {len(self.tabs)}")

    def GetTabAmount(self):
        return len(self.tabs)


TSHScoreboardManager.instance = TSHScoreboardManager()