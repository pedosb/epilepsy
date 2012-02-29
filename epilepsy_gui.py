#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# This file is part of Coruja-scripts
#
# Coruja-scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Coruja-scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Coruja-scripts.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2011 Grupo Falabrasil - http://www.laps.ufpa.br/falabrasil
#
# Author 2011: Pedro Batista - pedosb@gmail.com

import sys
from PyQt4 import QtGui

class EpilepsyGui(QtGui.QMainWindow):
	def __init__(self):
		super(EpilepsyGui, self).__init__()

		self.initUI()
		self.statusBar().showMessage('Ready')

	def initUI(self):
		self.menuInit()

		label = QtGui.QLabel('TDMS File:')
		line = QtGui.QLineEdit()
		button = QtGui.QPushButton('Browse')

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(label, 0, 0)
		grid.addWidget(line, 0, 1)
		grid.addWidget(button, 0, 2)

		vbox = QtGui.QVBoxLayout()
		vbox.addItem(grid)
		vbox.addStretch(1)

		centralWidget = QtGui.QWidget()
		centralWidget.setLayout(vbox)
		self.setCentralWidget(centralWidget)

		self.setWindowTitle('Epilepsy plot')

	def menuInit(self):
		exitAction = QtGui.QAction(QtGui.QIcon('Close-2-icon.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit Application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		toolbar = self.addToolBar('Standard')
		toolbar.addAction(exitAction)

def main():
	app = QtGui.QApplication(sys.argv)
	e = EpilepsyGui()
	e.show()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()
