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
			i = line.split('\t')[-1]
			self.wav[c] = float(i)

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
	plt.xlabel('Time (s)')
	plt.ylabel('Amplitude ($mV$)')

def plot(*tdms):
	_plot_all(tdms, _plot)

def _plot_freq_hist(tdms, **kargs):
	ti = kargs['ti']
	fi = kargs['fi']
	fft_len = kargs['fft_len']
	fft_scale = kargs['fft_scale']
	n_bins = kargs['n_bins']

#	bins = list()
	s, f = plt.psd(tdms.wav.__getslice__(*ti),
			fft_len,
			tdms.fs)
	sfi = None
	ffi = None
	for v, i in zip(f, xrange(len(f))):
		if fi[0] is not None and v > fi[0]:
			if sfi is None:
				sfi = i
		if fi[1] is not None and v > fi[1]:
			ffi = i
			break
	if sfi is None:
		sfi = 0
	if ffi is None:
		ffi = len(f)
	s = s[sfi:ffi]
	plt.cla()
#	s = tdms.wav.__getslice__(*ti)
	t = sum(s)
	m = len(s) / n_bins
	r = len(s) - m * n_bins
	for i in xrange(n_bins):
		step = i * m + (i if i < r else r)
		b = step, step + m + (1 if i < r else 0)
#		bins.append(b, sum(s.__getslice__(*b)))
		plt.bar(b[0] + sfi, sum(s.__getslice__(*b))/t, b[1] - b[0])
	plt.ylabel(r'Amplitude $\frac{mV^2}{Hz}$')
	plt.xlabel(u'Frequency ($Hz$)')

def _plot_fft(tdms, **kargs):
	ti = kargs['ti']
	fft_len = kargs['fft_len']
	fft_scale = kargs['fft_scale']
	p, f = plt.psd(tdms.wav.__getslice__(*ti),
			fft_len,
			tdms.fs)
	if fft_scale == 'db':
		plt.ylabel(r'Amplitude $\frac{mV^2}{Hz}$ ($dB$)')
	elif fft_scale == 'linear':
		plt.cla()
		plt.plot(f, p)
		plt.ylabel(r'Amplitude $\frac{mV^2}{Hz}$')
	plt.xlabel(u'Frequency ($Hz$)')
	return
	fft = np.fft.fft(tdms.wav.__getslice__(*ti), fft_len)[:fft_len/2]

	if fft_unit == 'pow':
		fft = fft * fft.conjugate() / fft_len
	elif fft_unit == 'amp':
		fft = np.abs(fft / fft_len)
		plt.ylabel('Amplitude mV/Hz')

	plt.plot(np.fft.fftfreq(fft_len, 1/tdms.fs)[:fft_len/2], fft)
	plt.grid()

def plot_fft(*tdms):
	_plot_all(tdms, _plot_fft)

def _plot_specgram(tdms, **kargs):
	ti = kargs['ti']
	plt.specgram(tdms.wav.__getslice__(*ti), Fs=tdms.fs)
	plt.xlabel('Time (segundos)')
	plt.ylabel(u'Frequency (Hz)')
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
	plot_func = [_plot, _plot_fft, _plot_specgram, _plot_freq_hist]
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

	plt.figure(figsize=kargs['figure_size'], dpi=kargs['figure_resolution'])

	lines = len(tdms)
	c = 0
	ti_list = kargs['ti']
	del kargs['ti']
	for t, i in zip(tdms, ti_list):
		i = (int(round(i[0] * t.fs)), int(round(i[1] * t.fs)))
		for col in xrange(1, (cols + 1) if cols is not None else 2):
			c += 1
			plt.subplot(lines, cols, c)
			if cols is not None:
				plot_func(t, col, plot_list, ti=i, **kargs)
			else:
				plot_func(t)
	if kargs['output_fn'] is not None:
		plt.savefig(kargs['output_fn'])
	plt.show()

def plot_joint_psd(tdms_list, ti_list, fft_len=256, fft_scale='db', fi=None,
		bar=False, figure_size=(8,6), output_fn=None, figure_resolution=80):

	plt.figure(figsize=figure_size, dpi=figure_resolution)

	psd_len = fft_len / 2 + 1
#	data_list = np.zeros((len(tdms_list), psd_len))
	data_dict = dict()

	for tdms, ti, i, in zip(tdms_list, ti_list, xrange(len(tdms_list))):
		ti = (int(round(ti[0] * tdms.fs)), int(round((ti[1] * tdms.fs))))
		t = tdms.wav.__getslice__(*ti)
		data, f_list = plt.psd(t, fft_len, Fs=tdms.fs)

		if fft_scale == 'db':
			data = 10 * np.log10(data)

		if data_dict.has_key(tdms.group_id):
			data_dict[tdms.group_id] = \
					np.concatenate((data_dict[tdms.group_id], [data]))
		else:
			data_dict[tdms.group_id] = np.array([data])

	if fi != None:
		fi = (fi[0] if fi[0] is not None else 0,
				fi[1] if fi[1] is not None else tdms_list[0].fs / 2)
		f_start_idx = None
		f_stop_idx = None
		for f, i in zip(f_list, xrange(len(f_list))):
			if f_start_idx is None and f > fi[0]:
				f_start_idx = i - 1
			if f_stop_idx is None and f > fi[1]:
				f_stop_idx = i - 1
		f_list = f_list[f_start_idx:f_stop_idx]

	plt.cla()
	if fft_scale == 'db':
		plt.ylabel(r'Amplitude $\frac{mV^2}{Hz}$ ($dB$)')
	elif fft_scale == 'linear':
		plt.ylabel(r'Amplitude $\frac{mV^2}{Hz}$')
	plt.xlabel(u'Frequency ($Hz$)')

	xticks_list = ([], [])
	for key, data, i in zip(data_dict.iterkeys(), data_dict.itervalues(), xrange(len(data_dict))):
		data = data[:,f_start_idx:f_stop_idx]
		if bar:
			data_sum = data.sum(1)
			plt.bar(i+0.1, data_sum.mean(), yerr=data_sum.std(),
					error_kw=dict(linewidth=6, ecolor='green'))
			xticks_list[0].append(i+0.5)
			xticks_list[1].append(key)
		else:
			plt.errorbar(f_list, data.mean(0), data.std(0), label=str(key))
	if bar:
		plt.xlim((0, len(data_dict)))
		plt.xticks(*xticks_list)
		print xticks_list
	else:
		plt.legend()
		plt.xlim((min(f_list), max(f_list)))
	if output_fn is not None:
		plt.savefig(output_fn)
	plt.show()

def plot_all(amplitude=False, fft=False,
		specgram=False, hist=False, *tdms, **kargs):
	plot_list = [amplitude, fft, specgram, hist]
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
