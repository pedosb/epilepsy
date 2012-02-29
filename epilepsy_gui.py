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
import tdms

class EpilepsyGui(QtGui.QMainWindow):
	def __init__(self):
		super(EpilepsyGui, self).__init__()

		self.tdms_list = list()

		self.initUI()
		self.statusBar().showMessage('Ready')

	def initUI(self):
		self.menuInit()

		self.plot_amplitude_check_box = QtGui.QCheckBox('Plot amplitude')
		self.plot_fft_check_box = QtGui.QCheckBox('Plot the FFT')
		self.plot_specgram_check_box = QtGui.QCheckBox('Plot the spectrogram')

		plot_button = QtGui.QPushButton('Plot')
		plot_button.clicked.connect(lambda: self.plot(plot_button))

		plot_hbox = QtGui.QHBoxLayout()
		plot_hbox.addWidget(self.plot_amplitude_check_box)
		plot_hbox.addWidget(self.plot_fft_check_box)
		plot_hbox.addWidget(self.plot_specgram_check_box)
		plot_hbox.addStretch(1)
		plot_hbox.addWidget(plot_button)

		plot_group_box = QtGui.QGroupBox('Plot options')
		plot_group_box.setLayout(plot_hbox)

		add_tdms_button = QtGui.QPushButton('Add TDMS')
		add_tdms_button.clicked.connect(self.add_tdms)

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(add_tdms_button)

		self.grid = QtGui.QGridLayout()
		self.grid.setSpacing(10)

		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addItem(self.grid)
		self.vbox.addStretch(1)
		self.vbox.addItem(hbox)
		self.vbox.addWidget(plot_group_box)

		centralWidget = QtGui.QWidget()
		centralWidget.setLayout(self.vbox)
		self.setCentralWidget(centralWidget)
		self.add_tdms()

		self.setWindowTitle('Epilepsy plot')

	def add_tdms(self):
		label = QtGui.QLabel('TDMS File:', self.centralWidget())
		le = QtGui.QLineEdit(self.centralWidget())
		button = QtGui.QPushButton('Browse', self.centralWidget())
		line_n = self.grid.rowCount()
		self.grid.addWidget(label, line_n, 0)
		self.grid.addWidget(le, line_n, 1)
		self.grid.addWidget(button, line_n, 2)
		self.tdms_list.append(None)
		label.show()
		le.show()
		button.show()
		browse = lambda: self.browse(le)
		button.clicked.connect(browse)
		if line_n != 1:
			self.browse(le)

	def browse(self, le):
		file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open TDMS File',
				'', 'TDMS files in TXT format (*.txt)')
		if file_name != '':
			le.setText(file_name)

			l, _, _, _ = self.grid.getItemPosition(self.grid.indexOf(le))
			self.statusBar().showMessage('Loading %s' % file_name)
			self.tdms_list[l-1] = tdms.Tdms(file_name)
			self.statusBar().showMessage('Ready')

	def plot(self, button):
		plot_amp = self.plot_amplitude_check_box.isChecked()
		plot_fft = self.plot_fft_check_box.isChecked()
		plot_spec = self.plot_specgram_check_box.isChecked()
		plot_list = [i for i in self.tdms_list if i is not None]

		tdms.plot_all(plot_amp, plot_fft, plot_spec, *plot_list)

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
