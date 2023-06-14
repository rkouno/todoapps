@echo off

echo Content-Type: text/html
echo.

rem Torrentディレクトリへの移動
cd C:\Torrent\

@REM 動画ファイルの移動
move C:\Torrent\*.mp4 D:\todoapps\static\media\unwatch\video

echo ^</PRE^>
exit