@echo off

rem �x�����ϐ��ݒ�
setlocal enabledelayedexpansion

rem �J�����g�f�B���N�g���ֈړ�
cd /d %~dp0
set filepath=%1

call :convertavif %filepath%

exit /b

:convertavif

@REM �g���q�擾
set extention=%~x1

@REM ���ݓ���
set time2=%time: =0%
set datetime=%date:~0,4%%date:~5,2%%date:~8,2%%time2:~0,2%%time2:~3,2%%time2:~6,2%

set convertfile=convert%datetime%

if exist %~1\nul (
    :loop
    
    rem �������Ȃ��Ȃ�΃��[�v����o�āu:confirm�v�֔��
    if "%~n1"=="" goto :confirm

    rem �t�H���_����ۑ�
    set folder=%~1
    set file=%folder:~12%
    echo %file%�@������

    echo %folder%>>log.txt

    rem �ϊ��ł���t�H���_���ɕύX
    echo "%folder%"�@���@%convertfile%�@�Ƀ��l�[��
    echo %folder%/%convertfile%
    rename "%folder%" %convertfile%

    echo �ϊ��J�n
    rem �ϊ�
    for /R "./"%convertfile%  %%a in (*.avif) do (
     	avifdec.exe "%%a" "%%~dpa%%~na.jpg"
     	del %%a
    )
    echo �ϊ��I��

    rem ����������炷
    shift
    
    rem �u:loop�v�֖߂��ă��[�v�𑱂���
    goto loop

:confirm

)

rem �t�H���_�������Ƃɖ߂�
echo D:\download\%convertfile%�@���@"%file%"�@�Ƀ��l�[��
rename D:\download\%convertfile% "%file%"
echo �����I��

rem �I��
exit /b