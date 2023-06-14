@echo off

echo Content-Type: text/html
echo.

rem Torrentディレクトリへの移動
cd C:\Torrent\

@REM ディレクトリ取得
for /d %%a in (C:\Torrent\*) do (
    @REM avifファイル変換
    call D:\todoapps\static\bat\convertavif.bat "%%a"
)
@REM zip
for %%a in ("C:\Torrent\*.zip") do (
    @REM 解凍
    call :unzip_archive "%%a"
    @REM 削除
    del "%%a"
)
@REM rar
for %%a in ("C:\Torrent\*.rar") do (
    @REM 解凍
    call :unzip_archive "%%a"
    @REM 削除
    del "%%a"
)
@REM 7z
for %%a in ("C:\Torrent\*.7z") do (
    @REM 解凍
    call :unzip_archive "%%a"
    @REM 削除
    del "%%a"
)

@REM 終了
exit 0

@REM rem サブルーチン
:unzip_archive

"C:\Program Files\7-Zip\7zG.exe" X -y "%~1" -o"C:\Torrent"

@REM サブルーチン終了
exit /b 0