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
git remote add origin https://github.com/rkouno/todoapps.git
git push -u origin master

--pythonanywhere first create only--
pip3.6 install --user pythonanywhere
pa_autoconfigure_django.py --python=3.6 https://github.com/rkouno/todoapps.git
python manage.py createsuperuser

--Git--
git status
git add --all
git commit -m "test"
git push

--pythonanywhere--
cd rkouno.pythonanywhere.com
git pull