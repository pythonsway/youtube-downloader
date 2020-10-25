# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['F:\\my_projects\\youtube-downloader'],
             binaries=[],
             datas=[('assets/*', 'assets')],
             hiddenimports=['pkg_resources.py2_warn', 'pkg_resources.markers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='YTDownloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , version='file_version_info.txt', icon='assets\\favicon.ico')
