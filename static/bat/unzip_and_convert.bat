@echo off

@REM ���x���ϐ��̐錾
setlocal enabledelayedexpansion

@REM �f�B���N�g���ړ�
cd %~dp0
set DL_DIR=D:\download

@REM ���O�t�@�C��
set LOG=%~dp0\log.txt

echo ==========%date% %time% �����J�n==========>%LOG%

echo ----------------File�����J�n---------------->>%LOG%
for /r %DL_DIR% %%f in (*.zip, *.rar, *.cbz, *.7z) do call :main_progress "%%f"

echo ----------------Folder�����J�n---------------->>%LOG%
for /d %%f in ("%DL_DIR%\*") do call :convertavif "%%f"

echo ----------------�s�v�t�@�C���폜---------------->>%LOG%
del /s %DL_DIR%\*.url>>%LOG%

echo ==========%date% %time% �����I��==========>>%LOG%

endlocal

@REM ����I��
exit

@REM ------------------------------
@REM ���C������
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
@REM ���k�t�@�C���̉�
:unzip_archive
@REM �����̎擾
set filepath="%~1"
set fileName="%~n1"

echo �y�𓀁z%fileName%>>%LOG%
"C:\Program Files\CubeICE\cubeice.exe" "%~1">>%LOG%
echo          �𓀂��܂����B>>%LOG%
if %errorlevel% equ 0 (
    @REM �𓀂����������t�@�C���͍폜
    echo �y�폜�z %filepath%  >>%LOG%
    del /Q %filepath% >>%LOG%
    for /d %%f in (*) do (
        echo �y�ړ��z %%f>>%LOG%
        move "%%f" %DL_DIR% >>%LOG%
    ) 
)

@REM ����I��
exit /b 0

@REM ------------------------------
@REM AVIF�t�@�C���̕ϊ�
:convertavif

@REM �ϐ�
set folderPath=%~1
set folderName=%~nx1

@REM �ϊ��i�G�X�P�[�v�j
set folderPath=%folderPath: =_%
set folderName=%folderName: =_%
set folderPath=%folderPath:!=_%
set folderName=%folderName:!=_%
rename "%~1" "%folderName%">>%LOG%

echo %folderName%>>%LOG%
for /r %folderPath%\ %%f in (*.avif) do goto :convert
goto :end

:convert

@REM ���ݓ����̎擾
set time2=%time: =0%
set datetime=%date:~0,4%%date:~5,2%%date:~8,2%%time2:~0,2%%time2:~3,2%%time2:~6,2%

@REM �ϊ����t�H���_���̐ݒ�
set convertFolderName=convert%datetime%
set convertFolderPath=%DL_DIR%\%convertFolderName%

@REM �t�H���_���̕ϊ�
rename "%folderPath%" %convertFolderName% >>%LOG%

echo �y�ϊ��z%folderPath%>>%LOG%
@REM �T�u�t�H���_���܂ރf�B���N�g�����̃��[�v
for /R %convertFolderPath%/ %%a in (*.avif) do (
    avifdec.exe "%%a" "%%~dpa%%~na.jpg"
    del %%a
    echo %%a
)

@REM �t�H���_���̕ϊ�
rename %convertFolderPath% "%folderName%" >>%LOG%

@REM ����I��
:end

@REM �ĕϊ�
rename "%folderPath%" "%folderName:_= %" >>%LOG%

exit /b 0