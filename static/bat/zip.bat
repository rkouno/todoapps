@echo off

@REM カレントディレクトリへの移�?
cd %~dp0

@REM 引数取�?
set arg=%~1

@REM 拡張子取�?
set extention=%~x1

@REM ファイル�?
set fileName=%~nx1

echo %fileName%>>log.txt

if "%extention%"==".zip" (
    call :unzip_archive "%arg%"
    goto END
) else if "%extention%"==".rar" (
    call :unzip_archive "%arg%"
    goto END
) else if "%extention%"==".cbz" (
    call :unzip_archive "%arg%"
    goto END
) else if "%extention%"==".7z" (
    call :unzip_archive "%arg%"
    goto END
) else if "%extention%"=="" (
    call convertavif.bat "%arg%"
    goto END
)


:END

@REM ゴミファイル削除
del /s *.url

exit 0

@REM サブルーチン
:unzip_archive

@REM 解�?
"C:\Program Files\7-Zip\7zG.exe" X -y "%~1" -o*

if %errorlevel% equ 0 (
 echo delete "%arg%"
 del /Q "%arg%"
)

exit /b 0