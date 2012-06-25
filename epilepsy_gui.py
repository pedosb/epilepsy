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
		self.joint_button_list = list()
		self.joint_le_list = list()

		self.stop_time_str = '(max %d)'
		self.stop_frequency_str = 'Stop frequency (max %d)'

		self.group_len = 3
		self.group_ini_col = 5

		self.initUI()
		self.statusBar().showMessage('Ready')

		self.output_fn = None

	def initUI(self):
		self.menuInit()

		#Plot Options group box
		self.plot_amplitude_check_box = QtGui.QCheckBox('Plot amplitude')
		self.plot_fft_check_box = QtGui.QCheckBox('Plot the PSD')
		self.plot_specgram_check_box = QtGui.QCheckBox('Plot the spectrogram')
		self.plot_freq_hist_box = QtGui.QCheckBox('Plot frequency histogram')
		self.plot_joint_psd_check_box = QtGui.QCheckBox('Plot joint PSD')

		plot_button = QtGui.QPushButton('Plot')
		plot_button.clicked.connect(self.plot)

		plot_hbox = QtGui.QHBoxLayout()
		plot_hbox.addWidget(self.plot_amplitude_check_box)
		plot_hbox.addWidget(self.plot_fft_check_box)
		plot_hbox.addWidget(self.plot_specgram_check_box)
		plot_hbox.addWidget(self.plot_freq_hist_box)
		plot_hbox.addWidget(self.plot_joint_psd_check_box)
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
		psd_group_box = QtGui.QGroupBox('Scale')
		psd_group_box.setLayout(fft_unit_vbox)

		fft_hbox = QtGui.QHBoxLayout()
		fft_hbox.addWidget(fft_label)
		fft_hbox.addWidget(self.fft_le)
		fft_hbox.addWidget(psd_group_box)
		fft_hbox.addStretch(1)
		psd_group_box = QtGui.QGroupBox('PSD Configuration')
		psd_group_box.setLayout(fft_hbox)

		#Joint PSD configuration group box
		joint_psd_group_box = QtGui.QGroupBox('Joint PSD Configuration')
		joint_psd_grid_layout = QtGui.QGridLayout(self.centralWidget())
		frequency_interval_start_label = QtGui.QLabel('Start Frequency',
				self.centralWidget())
		self.frequency_interval_start_le = QtGui.QLineEdit(self.centralWidget())
		self.frequency_interval_stop_label = QtGui.QLabel('Stop Frequency',
				self.centralWidget())
		self.frequency_interval_stop_le = QtGui.QLineEdit()
		self.joint_psb_bar_check_box = QtGui.QCheckBox("Plot bars")
		joint_psd_grid_layout.addWidget(frequency_interval_start_label, 0, 0)
		joint_psd_grid_layout.addWidget(self.frequency_interval_start_le, 0, 1)
		joint_psd_grid_layout.addWidget(self.frequency_interval_stop_label, 1, 0)
		joint_psd_grid_layout.addWidget(self.frequency_interval_stop_le, 1, 1)
		joint_psd_vbox = QtGui.QVBoxLayout()
		joint_psd_vbox.addItem(joint_psd_grid_layout)
		joint_psd_vbox.addWidget(self.joint_psb_bar_check_box)
		joint_psd_group_box.setLayout(joint_psd_vbox)

		#PSD and Joint PSD configuration HBox
		psd_and_joint_hbox = QtGui.QHBoxLayout()
		psd_and_joint_hbox.addWidget(psd_group_box)
		psd_and_joint_hbox.addWidget(joint_psd_group_box)

		#Histogram configuration group box
		freq_hist_label = QtGui.QLabel('Number of bins')
		self.freq_hist_le = QtGui.QLineEdit()
		self.freq_hist_le.setText('25')

		freq_hist_hbox = QtGui.QHBoxLayout()
		freq_hist_hbox.addWidget(freq_hist_label)
		freq_hist_hbox.addWidget(self.freq_hist_le)
		freq_hist_hbox.addStretch(1)

		freq_hist_group_box = QtGui.QGroupBox('Frequency Histogram Configuration')
		freq_hist_group_box.setLayout(freq_hist_hbox)

		#Figure options group box
		figure_size_hbox = QtGui.QHBoxLayout()
		figure_size_hbox.addWidget(QtGui.QLabel('Figure Size (in) '))
		self.figure_size_wid_le = QtGui.QLineEdit('8')
		self.figure_size_hei_le = QtGui.QLineEdit('6')
		figure_size_hbox.addWidget(self.figure_size_wid_le)
		figure_size_hbox.addWidget(QtGui.QLabel('X'))
		figure_size_hbox.addWidget(self.figure_size_hei_le)

		figure_resolution_hbox = QtGui.QHBoxLayout()
		figure_resolution_hbox.addWidget(QtGui.QLabel('Figure resolution (dpi) '))
		self.figure_resolution_le = QtGui.QLineEdit('80')
		figure_resolution_hbox.addWidget(self.figure_resolution_le)

		figure_out_hbox = QtGui.QHBoxLayout()
		figure_out_button = QtGui.QPushButton('Save Figure')
		figure_out_button.clicked.connect(self.save_figure)
		figure_out_hbox.addWidget(figure_out_button)

		figure_vbox = QtGui.QVBoxLayout()
		figure_vbox.addItem(figure_size_hbox)
		figure_vbox.addItem(figure_resolution_hbox)
		figure_vbox.addItem(figure_out_hbox)

		figure_group_box = QtGui.QGroupBox('Figure Options')
		figure_group_box.setLayout(figure_vbox)

		#Add TDMS button
		add_tdms_button = QtGui.QPushButton('Add TDMS')
		add_tdms_button.clicked.connect(self.add_tdms)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(add_tdms_button)

		#Grid layout for tdms intput files
		self.grid = QtGui.QGridLayout()
		self.grid.setSpacing(10)
		self.grid.addWidget(QtGui.QLabel('TDMS file'), 0, 0)
		self.grid.addWidget(QtGui.QLabel('Start time'), 0, 2)
		self.grid.addWidget(QtGui.QLabel('Stop time'), 0, 4)
		for i in xrange(self.group_len):
			new_le = QtGui.QLineEdit('Grupo %d' % i)
			self.joint_le_list.append(new_le)
			self.grid.addWidget(new_le, 0,
					self.group_ini_col + i)

		#Main Vertical Box
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addItem(self.grid)
		self.vbox.addStretch(1)
		self.vbox.addItem(hbox)
		self.vbox.addWidget(figure_group_box)
		self.vbox.addWidget(freq_hist_group_box)
		self.vbox.addItem(psd_and_joint_hbox)
		self.vbox.addWidget(plot_group_box)

		centralWidget = QtGui.QWidget()
		centralWidget.setLayout(self.vbox)
		self.setCentralWidget(centralWidget)
		self.add_tdms()

		self.setWindowTitle('Epilepsy plot')

	def add_tdms(self):
#		label = QtGui.QLabel('TDMS File:', self.centralWidget())
		le = QtGui.QLineEdit(self.centralWidget())
		button = QtGui.QPushButton('Browse', self.centralWidget())

#		ti_ini_label = QtGui.QLabel('Start time ', self.centralWidget())
		ti_ini_le = QtGui.QLineEdit(self.centralWidget())
		ti_fi_label = QtGui.QLabel('', self.centralWidget())
		ti_fi_le = QtGui.QLineEdit(self.centralWidget())

		button.clicked.connect(
				lambda: self.browse(le, ti_fi_label))

		line_n = self.grid.rowCount()

#		self.grid.addWidget(label, line_n, 0)
		self.grid.addWidget(le, line_n, 0)
		self.grid.addWidget(button, line_n, 1)
#		self.grid.addWidget(ti_ini_label, line_n, 3)
		self.grid.addWidget(ti_ini_le, line_n, 2)
		self.grid.addWidget(ti_fi_label, line_n, 3)
		self.grid.addWidget(ti_fi_le, line_n, 4)

		button_group = QtGui.QButtonGroup(self.centralWidget())
		for i in xrange(self.group_len):
			new_button = QtGui.QRadioButton(self.centralWidget())
			if i == 0:
				new_button.setChecked(True)
			button_group.addButton(new_button, i)
			self.grid.addWidget(new_button, line_n, self.group_ini_col + i)
			new_button.show()

		self.tdms_list.append(None)
		self.joint_button_list.append(button_group)

#		label.show()
		le.show()
		button.show()
#		ti_ini_label.show()
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

			self.frequency_interval_stop_label.setText(self.stop_frequency_str %
					(tdms_file.fs / 2))

			self.statusBar().showMessage('Ready')

	def save_figure(self):
		file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save Figure',
				filter='Images (*.png)')
		if file_name != '':
			self.output_fn = str(file_name)
			self.plot()

	def plot(self):
		fft_len_le = int(self.fft_le.text())

		plot_amp = self.plot_amplitude_check_box.isChecked()
		plot_fft = self.plot_fft_check_box.isChecked()
		plot_freq_hist = self.plot_freq_hist_box.isChecked()
		plot_spec = self.plot_specgram_check_box.isChecked()
		plot_joint_psd = self.plot_joint_psd_check_box.isChecked()
		joint_psb_bar = self.joint_psb_bar_check_box.isChecked()
		ti_start = self.frequency_interval_start_le.text()
		ti_stop = self.frequency_interval_stop_le.text()
		frequency_interval = (float(ti_start) if ti_start != '' else None,
				float(ti_stop) if ti_stop != '' else None)

		figure_size = (float(self.figure_size_wid_le.text()),
				float(self.figure_size_hei_le.text()))
		figure_resolution = float(self.figure_resolution_le.text())

		n_bins = int(self.freq_hist_le.text())

		if self.fft_scale_db.isChecked():
			fft_scale = 'db'
		elif self.fft_scale_linear.isChecked():
			fft_scale = 'linear'

#		plot_list = [i for i in self.tdms_list if i is not None]
		plot_list = list()
		ti_list = list()
		c = 0
		for t, button_group in zip(self.tdms_list, self.joint_button_list):
			if t is not None:
				plot_list.append(t)
				t.group_id = self.joint_le_list[button_group.checkedId()].text()
				ini = self.grid.itemAtPosition(c+1, 2).widget().text()
				fi = self.grid.itemAtPosition(c+1, 4).widget().text()
				ti_list.append((
					float(ini) if ini != '' else 0,
					float(fi) if fi != '' else float(len(t.wav))/t.fs))
			c += 1

		if plot_joint_psd:
			tdms.plot_joint_psd(plot_list, ti_list, fft_len=fft_len_le,
					fft_scale=fft_scale, fi=frequency_interval,
					bar=joint_psb_bar, figure_size=figure_size,
					output_fn=self.output_fn,
					figure_resolution=figure_resolution)

		if any((plot_amp, plot_fft, plot_spec, plot_freq_hist)):
			tdms.plot_all(plot_amp, plot_fft, plot_spec, plot_freq_hist, *plot_list,
					fft_len=fft_len_le, ti=ti_list, fi=frequency_interval,
					fft_scale=fft_scale, n_bins=n_bins, figure_size=figure_size,
					output_fn=self.output_fn,
					figure_resolution=figure_resolution)

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
