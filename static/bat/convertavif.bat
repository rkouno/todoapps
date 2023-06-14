@echo off

rem 
setlocal enabledelayedexpansion

rem 
cd /d %~dp0

:loop
 
rem 引数がなくなればループから出て「:confirm」へ飛ぶ
if "%~n1"=="" goto :confirm

rem フォルダ名を保存
set folder=%~n1

rem 変換できるフォルダ名に変更
rename "%folder%" convert

rem 変換
for /R "./convert"  %%a in (*.avif) do (
	avifdec.exe "%%a" "%%~dpa%%~na.jpg"
	del %%a
)

rem フォルダ名をもとに戻す
rename convert "%folder%"

rem 引数を一つずらす
shift
 
rem 「:loop」へ戻ってループを続ける
goto loop

:confirm

rem 終了
@REM exit
