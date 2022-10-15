--新規アプリ作成系--
1 python manage.py startapp アプリケーション名
2 urls.py作成
3 config urls.pyにurl追加

--起動--
& c:/Users/KRyo/todoapps/todovenv/Scripts/Activate.ps1

--DB系--
python manage.py makemigrations book
python manage.py migrate book

--Shell--
python manage.py shell
from apps.anime.models import Anime 

--git first create only--
 git init
 git config --global user.name rkouno
 git config ==global user.email rkouni@odp.co.jp

--Git--
git status
git add --all
git commit -m "test"
git push

--pythonanywhere--
cd rkouno.pythonanywhere.com
git pull