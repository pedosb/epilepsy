# Introduction

This page lists the project dependencies and instructs the download and execution of the epilepsy project on a Windows box (tested with Windows 7).

# Dependencies install

Firstly you need to download and install the following dependencies, during the install, choosing the default options should give you what we need, so just click on next, next, ... and finish.

## Download and install the following programs:

* [Python 2.7.2](http://www.python.org/ftp/python/2.7.2/python-2.7.2.msi)
* [matplotlib-1.1.0](http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.1.0/matplotlib-1.1.0.win32-py2.7.exe/download)
* [numpy-1.6.1](http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/numpy-1.6.1-win32-superpack-python2.7.exe/download)
* [scipy-0.10.1](http://sourceforge.net/projects/scipy/files/scipy/0.10.1/scipy-0.10.1-win32-superpack-python2.7.exe/download)
* PyQt4 (use the first if running a 64bit Windows and the second for a 32bit one)
** [PyQt4-4.11.1-x64](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.1/PyQt4-4.11.1-gpl-Py2.7-Qt4.8.6-x64.exe)
** [PyQt4-4.11.1-x32](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.1/PyQt4-4.11.1-gpl-Py2.7-Qt4.8.6-x32.exe)
* [Git-1.9.4](https://github.com/msysgit/msysgit/releases/download/Git-1.9.4-preview20140611/Git-1.9.4-preview20140611.exe)

# Download of epilepsy

Start the GitBash (from the Windows programs list) and type the following lines download the epilepsy project
```
cd c:
git clone https://github.com/pedosb/epilepsy
```
PS: if your default drive is not c: just change it to whatever your default drive is.

# Update epilepsy

If there are updated versions of epilepsy that you want to download just start the GitBash again and run the following commands (choosing the default drive used in the previous section)
```
cd c:\epilepsy
git pull
```

# Run epilepsy

Now whenever you want to run epilepsy just access you default drive (used in the cd command in the previous section) from the Windows explorer, choose the epilepsy folder and double click the epilepsy_gui.py program.
