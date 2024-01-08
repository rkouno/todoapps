@echo off

rem 遅延環境変数設定
setlocal enabledelayedexpansion

rem カレントディレクトリへ移動
cd /d %~dp0
set filepath=%1

call :convertavif %filepath%

exit /b

:convertavif

@REM 拡張子取得
set extention=%~x1

@REM 現在日時
set time2=%time: =0%
set datetime=%date:~0,4%%date:~5,2%%date:~8,2%%time2:~0,2%%time2:~3,2%%time2:~6,2%

set convertfile=convert%datetime%

if exist %~1\nul (
    :loop
    
    rem 引数がなくなればループから出て「:confirm」へ飛ぶ
    if "%~n1"=="" goto :confirm

    rem フォルダ名を保存
    set folder=%~1
    set file=%folder:~12%
    echo %file%　を処理

    echo %folder%>>log.txt

    rem 変換できるフォルダ名に変更
    echo "%folder%"　を　%convertfile%　にリネーム
    echo %folder%/%convertfile%
    rename "%folder%" %convertfile%

    echo 変換開始
    rem 変換
    for /R "./"%convertfile%  %%a in (*.avif) do (
     	avifdec.exe "%%a" "%%~dpa%%~na.jpg"
     	del %%a
    )
    echo 変換終了

    rem 引数を一つずらす
    shift
    
    rem 「:loop」へ戻ってループを続ける
    goto loop

:confirm

)

rem フォルダ名をもとに戻す
echo D:\download\%convertfile%　を　"%file%"　にリネーム
rename D:\download\%convertfile% "%file%"
echo 処理終了

rem 終了
exit /b