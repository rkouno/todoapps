@echo off

@REM 環境遅延変数の宣言
setlocal enabledelayedexpansion

@REM ディレクトリ移動
cd %~dp0
set DL_DIR=D:\download

@REM ログファイル
set LOG=%~dp0\log.txt

echo ==========%date% %time% 処理開始==========>%LOG%

echo ----------------File処理開始---------------->>%LOG%
for /r %DL_DIR% %%f in (*.zip, *.rar, *.cbz, *.7z) do call :main_progress "%%f"

echo ----------------Folder処理開始---------------->>%LOG%
for /d %%f in ("%DL_DIR%\*") do call :convertavif "%%f"

echo ----------------不要ファイル削除---------------->>%LOG%
del /s %DL_DIR%\*.url>>%LOG%

echo ==========%date% %time% 処理終了==========>>%LOG%

endlocal

@REM 正常終了
exit

@REM ------------------------------
@REM メイン処理
:main_progress

set arg="%~1"
set extention=%~x1
set fileName=%~nx1
set filepath=%arg%

@REM ------------------------------
if "%extention%"==".zip" (
    call :unzip_archive %filepath%
    goto END
) else if "%extention%"==".rar" (
    call :unzip_archive %filepath%
    goto END
) else if "%extention%"==".cbz" (
    call :unzip_archive %filepath%
    goto END
) else if "%extention%"==".7z" (
    call :unzip_archive %filepath%
    goto END
) else if "%extention%"=="" (
    call :convertavif %filepath%
    goto END
)

:END
exit /b 0

@REM ------------------------------
@REM 圧縮ファイルの解凍
:unzip_archive
@REM 引数の取得
set filepath="%~1"
set fileName="%~n1"

echo 【解凍】%fileName%>>%LOG%
"C:\Program Files\CubeICE\cubeice.exe" "%~1">>%LOG%
echo          解凍しました。>>%LOG%
if %errorlevel% equ 0 (
    @REM 解凍が成功したファイルは削除
    echo 【削除】 %filepath%  >>%LOG%
    del /Q %filepath% >>%LOG%
    for /d %%f in (*) do (
        echo 【移動】 %%f>>%LOG%
        move "%%f" %DL_DIR% >>%LOG%
    ) 
)

@REM 正常終了
exit /b 0

@REM ------------------------------
@REM AVIFファイルの変換
:convertavif

@REM 変数
set folderPath=%~1
set folderName=%~nx1

@REM 変換（エスケープ）
set folderPath=%folderPath: =_%
set folderName=%folderName: =_%
set folderPath=%folderPath:!=_%
set folderName=%folderName:!=_%
rename "%~1" "%folderName%">>%LOG%

echo %folderName%>>%LOG%
for /r %folderPath%\ %%f in (*.avif) do goto :convert
goto :end

:convert

@REM 現在日時の取得
set time2=%time: =0%
set datetime=%date:~0,4%%date:~5,2%%date:~8,2%%time2:~0,2%%time2:~3,2%%time2:~6,2%

@REM 変換中フォルダ名の設定
set convertFolderName=convert%datetime%
set convertFolderPath=%DL_DIR%\%convertFolderName%

@REM フォルダ名の変換
rename "%folderPath%" %convertFolderName% >>%LOG%

echo 【変換】%folderPath%>>%LOG%
@REM サブフォルダを含むディレクトリ内のループ
for /R %convertFolderPath%/ %%a in (*.avif) do (
    avifdec.exe "%%a" "%%~dpa%%~na.jpg"
    del %%a
    echo %%a
)

@REM フォルダ名の変換
rename %convertFolderPath% "%folderName%" >>%LOG%

@REM 正常終了
:end

@REM 再変換
rename "%folderPath%" "%folderName:_= %" >>%LOG%

exit /b 0