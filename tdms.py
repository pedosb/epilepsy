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

class TdmsSyntaxError():
	pass

class Tdms():
	def __init__(self, fn=None):
		self.load(fn)
	def load(self, fn):
		f = open(fn)
		if f.readline().strip() != 'channel names:':
			raise TdmsSyntaxError("Can't find channels names")
		self.channels = f.readline().split('\t')

		if f.readline().strip() != 'start times:':
			raise TdmsSyntaxError("Can't find start times")
		self.channels = f.readline().split('\t')

		if f.readline().strip() != 'dt:':
			raise TdmsSyntaxError("Can't find dt flag")
		self.fs = 1/float(f.readline())

		if f.readline().strip() != 'data:':
			raise TdmsSyntaxError("Can't find data flag")

		self.data = []
		self.wav = []
		while True:
			line = f.readline()
			if line == '':
				break
#			self.data.append([float(n) for n in line.split('\t')])
			i, j = line.split('\t')
			self.wav.append(float(i) - float(j))

		self.size = len(self.wav)
#		if len(self.channels) == 2:
#			self.wav = [i - j for i, j in self.data]
#			del self.data

	def plot(self):
		plt.plot(np.linspace(0, len(self.wav)/self.fs, len(self.wav)),
				self.wav)
		plt.grid()
		plt.xlabel('Tempo (segundos)')
		plt.ylabel('Amplitude')
		plt.show()

	def specgram(self):
		plt.specgram(self.wav, Fs=self.fs)
		plt.xlabel('Tempo (segundos)')
		plt.ylabel(u'Frequência (Hz)')
		plt.colorbar()
		plt.show()

	def fft(self):
		plt.plot(np.fft.fftfreq(1024, 1/self.fs),
				10 * np.log10(np.fft.fft(self.wav, 1024)))
		plt.grid()
		plt.xlabel(u'Frequência (Hz)')
		plt.ylabel('Amplitude (dB)')
		plt.show()

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
	args = parser.parse_args()
	t = Tdms(args.input_file)
	if args.plot_wav_form:
		t.plot()
	if args.plot_specgram:
		t.specgram()
	if args.plot_fft:
		t.fft()
