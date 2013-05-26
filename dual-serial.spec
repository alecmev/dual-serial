# -*- mode: python -*-
a = Analysis(['dual-serial.py'],
             pathex=['C:\\STORAGE\\stuff\\work\\ekselcom\\2013.05.19.dual-serial'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'dual-serial.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
