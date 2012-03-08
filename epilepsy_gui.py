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
		self.stop_time_str = 'Stop time (max %d)'

		self.initUI()
		self.statusBar().showMessage('Ready')

	def initUI(self):
		self.menuInit()

		#Plot Options group box
		self.plot_amplitude_check_box = QtGui.QCheckBox('Plot amplitude')
		self.plot_fft_check_box = QtGui.QCheckBox('Plot the FFT')
		self.plot_specgram_check_box = QtGui.QCheckBox('Plot the spectrogram')

		plot_button = QtGui.QPushButton('Plot')
		plot_button.clicked.connect(self.plot)

		plot_hbox = QtGui.QHBoxLayout()
		plot_hbox.addWidget(self.plot_amplitude_check_box)
		plot_hbox.addWidget(self.plot_fft_check_box)
		plot_hbox.addWidget(self.plot_specgram_check_box)
		plot_hbox.addStretch(1)
		plot_hbox.addWidget(plot_button)

		plot_group_box = QtGui.QGroupBox('Plot options')
		plot_group_box.setLayout(plot_hbox)

		#FFT configuration group box
		fft_label = QtGui.QLabel('Number of points')
		self.fft_le = QtGui.QLineEdit()
		self.fft_le.returnPressed.connect(self.plot)
		self.fft_le.setText('1024')

		self.fft_scale_db = QtGui.QRadioButton('Decibel')
		self.fft_scale_db.setChecked(True)
		self.fft_scale_linear = QtGui.QRadioButton('Linear')
		fft_unit_vbox = QtGui.QVBoxLayout()
		fft_unit_vbox.addWidget(self.fft_scale_db)
		fft_unit_vbox.addWidget(self.fft_scale_linear)
		fft_group_box = QtGui.QGroupBox('Scale')
		fft_group_box.setLayout(fft_unit_vbox)

		fft_hbox = QtGui.QHBoxLayout()
		fft_hbox.addWidget(fft_label)
		fft_hbox.addWidget(self.fft_le)
		fft_hbox.addWidget(fft_group_box)
		fft_hbox.addStretch(1)
		fft_group_box = QtGui.QGroupBox('PSD Configuration')
		fft_group_box.setLayout(fft_hbox)

		#Add TDMS button
		add_tdms_button = QtGui.QPushButton('Add TDMS')
		add_tdms_button.clicked.connect(self.add_tdms)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(add_tdms_button)

		#Grid layout for tdms intput files
		self.grid = QtGui.QGridLayout()
		self.grid.setSpacing(10)

		#Main Vertical Box
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addItem(self.grid)
		self.vbox.addStretch(1)
		self.vbox.addItem(hbox)
		self.vbox.addWidget(fft_group_box)
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

		ti_ini_label = QtGui.QLabel('Start time ', self.centralWidget())
		ti_ini_le = QtGui.QLineEdit(self.centralWidget())
		ti_fi_label = QtGui.QLabel('Stop time', self.centralWidget())
		ti_fi_le = QtGui.QLineEdit(self.centralWidget())

		button.clicked.connect(
				lambda: self.browse(le, ti_fi_label))

		line_n = self.grid.rowCount()

		self.grid.addWidget(label, line_n, 0)
		self.grid.addWidget(le, line_n, 1)
		self.grid.addWidget(button, line_n, 2)
		self.grid.addWidget(ti_ini_label, line_n, 3)
		self.grid.addWidget(ti_ini_le, line_n, 4)
		self.grid.addWidget(ti_fi_label, line_n, 5)
		self.grid.addWidget(ti_fi_le, line_n, 6)

		self.tdms_list.append(None)

		label.show()
		le.show()
		button.show()
		ti_ini_label.show()
		ti_ini_le.show()
		ti_fi_label.show()
		ti_fi_le.show()

		if line_n != 1:
			self.browse(le, ti_fi_label)

	def browse(self, le, ti_fi_label):
		file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open TDMS File',
				'', 'TDMS files in TXT format (*.txt)')
		if file_name != '':
			le.setText(file_name)

			l, _, _, _ = self.grid.getItemPosition(self.grid.indexOf(le))

			self.statusBar().showMessage('Loading %s' % file_name)

			tdms_file = tdms.Tdms(file_name)
			self.tdms_list[l-1] = tdms_file
			ti_fi_label.setText(
					self.stop_time_str % (len(tdms_file.wav)/tdms_file.fs))

			self.statusBar().showMessage('Ready')

	def plot(self):
		fft_len_le = self.fft_le.text()

		plot_amp = self.plot_amplitude_check_box.isChecked()
		plot_fft = self.plot_fft_check_box.isChecked()
		plot_spec = self.plot_specgram_check_box.isChecked()

		if self.fft_scale_db.isChecked():
			fft_scale = 'db'
		elif self.fft_scale_linear.isChecked():
			fft_scale = 'linear'

#		plot_list = [i for i in self.tdms_list if i is not None]
		plot_list = list()
		ti_list = list()
		c = 0
		for t in self.tdms_list:
			if t is not None:
				plot_list.append(t)
				ini = self.grid.itemAtPosition(c+1, 4).widget().text()
				fi = self.grid.itemAtPosition(c+1, 6).widget().text()
				ti_list.append((
					int(ini) if ini != '' else 0,
					int(fi) if fi != '' else float(len(t.wav))/t.fs))
			c += 1
		############
		#ti = (int(ti_ini_le.text()), int(ti_fi_le.text()))

		tdms.plot_all(plot_amp, plot_fft, plot_spec, *plot_list,
				fft_len=int(fft_len_le), ti=ti_list, fft_scale=fft_scale)

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
