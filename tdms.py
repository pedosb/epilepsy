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

import argparse
import matplotlib.pyplot as plt
import numpy as np
from os import path

def file_len(f):
	"""
	http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
	"""
	pos = f.tell()
	for i, l in enumerate(f):
		pass
	f.seek(pos)
	return i + 1

class TdmsSyntaxError(Exception):
	pass

class Tdms():
	def __init__(self, fn=None, ti=None):
		self.fn = fn
		self.load(ti)

	def load(self, ti=None):
		if ti is None:
			ti = [0, -1]
		f = open(self.fn)
		if f.readline().strip() != 'channel names:':
			raise TdmsSyntaxError("Can't find channels names")
		self.channels = f.readline().split('\t')

		if f.readline().strip() != 'start times:':
			raise TdmsSyntaxError("Can't find start times")
		self.channels = f.readline().split('\t')

		if f.readline().strip() != 'dt:':
			raise TdmsSyntaxError("Can't find dt flag")
		self.fs = 1/float(f.readline())
		self.start = ti[0] * self.fs
		self.stop = ti[1] * self.fs

		if f.readline().strip() != 'data:':
			raise TdmsSyntaxError("Can't find data flag")

		self.data = []
		self.wav = np.zeros(file_len(f))
		self.data_tell = f.tell()
		c = -1
		while True:
			line = f.readline()
			c += 1
			if c < self.start:
				continue
			if line == '' or (c > self.stop and self.stop > 0):
				break
#			self.data.append([float(n) for n in line.split('\t')])
			i, j = line.split('\t')
			self.wav[c] = float(i) - float(j)

		self.size = len(self.wav)
		if self.size < self.stop - self.start:
			c = 0
			f.seek(self.data_tell)
			while True:
				if f.readline() == '':
					break
				c += 1
			raise TdmsSyntaxError("Can't select time interval, must be between [0, %.2f]" % (c / self.fs))
		f.close()
#		if len(self.channels) == 2:
#			self.wav = [i - j for i, j in self.data]
#			del self.data

	def plot(self):
		plot(self)

	def specgram(self):
		plot_specgram(self)

	def plot_fft(self):
		plot_fft(self)

def _plot(tdms, **kargs):
	ti = kargs['ti']
	x = np.linspace(ti[0] / tdms.fs,
			ti[1] / tdms.fs,
			ti[1] - ti[0])
	plt.plot(x,
		tdms.wav[ti[0]:ti[1]])
	plt.grid()
	plt.xlabel('Tempo (segundos)')
	plt.ylabel('Amplitude')

def plot(*tdms):
	_plot_all(tdms, _plot)

def _plot_fft(tdms, **kargs):
	ti = kargs['ti']
	fft_len = kargs['fft_len']
	fft = np.fft.fft(tdms.wav.__getslice__(*ti), fft_len)[:fft_len/2]
	plt.plot(np.fft.fftfreq(fft_len, 1/tdms.fs)[:fft_len/2],
			10 * np.log10(np.abs(fft)))
	plt.grid()
	plt.xlabel(u'Frequência (Hz)')
	plt.ylabel('Amplitude (dB)')

def plot_fft(*tdms):
	_plot_all(tdms, _plot_fft)

def _plot_specgram(tdms, **kargs):
	ti = kargs['ti']
	plt.specgram(tdms.wav.__getslice__(*ti), Fs=tdms.fs)
	plt.xlabel('Tempo (segundos)')
	plt.ylabel(u'Frequência (Hz)')
	plt.grid()
	plt.colorbar()

def plot_specgram(*tdms):
	_plot_all(tdms, _plot_specgram)

def plot_amp_and_fft(*tdms):
	_plot_all(tdms, _plot_amp_and_fft, 2)

def _plot_amp_and_fft(tdms, col):
	if col == 1:
		_plot(tdms)
	elif col == 2:
		_plot_fft(tdms)

def _plot_any(tdms, col, plot_list, **kargs):
	n_col = plot_list.count(True)
	plot_func = [_plot, _plot_fft, _plot_specgram]
	plt.title(path.basename(str(tdms.fn)))
	if n_col == 1:
		plot_func[plot_list.index(True)](tdms, **kargs)
	elif n_col == 2:
		first_index = plot_list.index(True)
		if col == 1:
			plot_func[first_index](tdms, **kargs)
		else:
			plot_func[plot_list.index(True, first_index+1)](tdms, **kargs)
	elif n_col == 3:
		plot_func[col-1](tdms, **kargs)

def _plot_all(tdms, plot_func, cols=None, plot_list=None, **kargs):
	lines = len(tdms)
	c = 0
	ti_list = kargs['ti']
	del kargs['ti']
	for t, i in zip(tdms, ti_list):
		i = (int(i[0] * t.fs), int(i[1] * t.fs))
		for col in xrange(1, (cols + 1) if cols is not None else 2):
			c += 1
			plt.subplot(lines, cols, c)
			if cols is not None:
				plot_func(t, col, plot_list, ti=i, **kargs)
			else:
				plot_func(t)
	plt.show()

def plot_all(amplitude=False, fft=False,
		specgram=False, *tdms, **kargs):
	plot_list = [amplitude, fft, specgram]
	cols = plot_list.count(True)
	_plot_all(tdms, _plot_any, cols, plot_list, **kargs)

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Manipulate TDMS file')
	parser.add_argument('-f', '--input-file', required=True,
			help='The TDMS (txt) file to be used')
	parser.add_argument('-p', '--plot-wav-form', action='store_true',
			help='plot the wave form of a two channels TDMS file')
	parser.add_argument('-s', '--plot-specgram', action='store_true',
			help='plot the spetogram of a two channels TDMS file')
	parser.add_argument('-r', '--plot-fft', action='store_true',
			help='plot the fft of a two channels TDMS file')
	parser.add_argument('-t', '--time-interval', nargs=2, type=int,
			help='select the time interval to plot')
	args = parser.parse_args()
	t = Tdms(args.input_file, args.time_interval)
	if args.plot_wav_form:
		t.plot()
	if args.plot_specgram:
		t.specgram()
	if args.plot_fft:
		t.fft()
