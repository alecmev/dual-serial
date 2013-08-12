@ECHO OFF

python pyinstaller\utils\Build.py dual-serial.spec

RD /S /Q build
DEL *.log
DEL *.pyc
