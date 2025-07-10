# Commands to create an exe file / Příkazy pro vytvoření souboru exe

## Home

### Open a session in a given folder / Otevřít session v danné složce

```Powershell
cd "C:\Users\Home\Documents\Coding\Python\PyQt\PyQt_LineB\"
```

### Create a .spec file / Vytvoříme soubor .spec

```Powershell
& "C:\Users\Home\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\Home\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" --name=LineB --version-file=version.txt --noconfirm --onefile --noconsole --windowed --icon=resources\ico\b_line.ico main.py
```

### Edit the created .spec file / Upravíme vytvořený soubor .spec

```Text
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'login_window.py', 'szv_utils.py', 'intermediate.py', 'app_window.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    icon=['img/b_line.ico'],
)
```

### Create an .exe / Vytvoříme .exe

```Powershell
& "C:\Users\Home\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\Home\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" LineB.spec
```

## Work

### Open a session in a given folder / Otevřít session v danné složce

```Powershell
cd "C:\GitWork\Python\PyQt\PyQt_PrintPackingLine\"
```

### Vytvoříme soubor .spec

```Powershell
& "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" --name=LineB --version-file=version.txt --noconfirm --onefile --noconsole --windowed --icon=resources\ico\b_line.ico main.py
```

### Upravíme vytvořený soubor .spec

```Text
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('controllers/', 'controllers/'), ('core/', 'core/'), ('effects/', 'effects/'), ('resources/ico/', 'resources/ico/'), ('utils/', 'utils/'), ('views/', 'views/')],
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

### Vytvoříme exe

```Powershell
& "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\hradecky\AppData\Local\Programs\Python\Python313\Scripts\pyinstaller.exe" LineB.spec
```
