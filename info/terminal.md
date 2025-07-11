# Commands to create an exe file

## Home

### 1. Open a session in a given folder

```Powershell
cd "C:\Users\Home\Documents\Coding\Python\PyQt\PyQt_LineB\"
```

### 2. Create a .spec file

```Powershell
& "C:\Users\Home\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\Home\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" --name=LineB --version-file=version.txt --noconfirm --onefile --noconsole --windowed --icon=resources\ico\b_line.ico main.py
```

### 3. Edit the created .spec file

```Text
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('controllers/', 'controllers/'), ('core/', 'core/'), ('effects/', 'effects/'), ('log/', 'log/'), ('resources/ico/', 'resources/ico/'), ('setup/', 'setup/'), ('utils/', 'utils/'), ('views/', 'views/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LineB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon=['resources/ico/b_line.ico'],
)
```

### 4. Create an .exe

```Powershell
& "C:\Users\Home\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\Home\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" LineB.spec
```

## Work

### 1. Open a session in a given folder

```Powershell
cd "C:\GitWork\Python\PyQt\PyQt_PrintPackingLine\"
```

### 2. Create a .spec file

```Powershell
& "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" --name=LineB --version-file=version.txt --noconfirm --onefile --noconsole --windowed --icon=resources\ico\b_line.ico main.py
```

### 3. Edit the created .spec file

```Text
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('controllers/', 'controllers/'), ('core/', 'core/'), ('effects/', 'effects/'), ('log/', 'log/'), ('resources/ico/', 'resources/ico/'), ('setup/', 'setup/'), ('utils/', 'utils/'), ('views/', 'views/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LineB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon=['resources/ico/b_line.ico'],
)
```

### 4. Create an .exe

```Powershell
& "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" LineB.spec
```
