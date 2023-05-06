pip install django
pip install requests
pip install beautifulsoup4
pip install wfastcgi
pip install psycopg2
pip install img2pdf

--新規アプリ作成系--
1 python manage.py startapp apps.アプリケーション名
2 urls.py作成
3 config urls.pyにurl追加

--起動--
& c:/Users/KRyo/todoapps/todovenv/Scripts/Activate.ps1

--DB系--
python manage.py makemigrations book
python manage.py migrate book

python manage.py makemigrations anime
python manage.py migrate anime

--Shell--
python manage.py shell
from apps.anime.models import Anime 

--git first create only--
git init
git config --global user.name rkouno
git config --global user.email rkouno@odp.co.jp
git remote add origin https://github.com/rkouno/todoapps.git
git push -u origin master

--pythonanywhere first create only--
pip3.6 install --user pythonanywhere
pa_autoconfigure_django.py --python=3.6 https://github.com/rkouno/todoapps.git
python manage.py createsuperuser

--再インストール--
pa_autoconfigure_django.py --nuke --python=3.6 https://github.com/rkouno/todoapps.git

--静的ファイルの適用 pythonanywhere--
workon rkouno.pythonanywhere.com
~$ python manage.py collectstatic

--Git--
git status
git add --all .
git commit -m "isort change"
git push

--pythonanywhere--
cd rkouno.pythonanywhere.com
git pull

--IIS--
%windir%\system32\inetsrv\appcmd unlock config -section:system.webServer/handlers


--開発メモ--
url.py:URLの引数
str	
    パスセパレータ '/'を除く、空でない文字列に一致します。 コンバータが式に含まれていない場合の既定値です。
int	
    ゼロまたは任意の正の整数に一致します。 intを返します。
slug	
    ASCII文字または数字、およびハイフンおよびアンダースコア文字で構成されるスラッグ文字列に一致します。 例えば、building-your-1st-django-siteのようにします。
uuid	
    フォーマットされたUUIDと一致します。 複数のURLが同じページにマッピングされないようにするには、ダッシュを含め、文字を小文字にする必要があります。 たとえば、075194d3-6885-417e-a8a8-6c931e272f00となります。 UUIDインスタンスを返します。
path	
    パスセパレータ '/'を含む、空でない文字列に一致します。 これにより、strのようなURLパスのセグメントではなく、完全なURLパスと照合することができます。