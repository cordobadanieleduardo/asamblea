"# asamblea" 


…or create a new repository on the command line


echo "# asamblea" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/cordobadanieleduardo/asamblea.git
git push -u origin main



…or push an existing repository from the command line


git remote add origin https://github.com/cordobadanieleduardo/asamblea.git
git branch -M main
git push -u origin main



4. Crear Entorno Virtual
py -m venv ..\venv
..\venv\Scripts\activate.bat
pip freeze





1. Crear Directorio
mkdir djcmpfc42
cd djcmpfc42

2. Clonar Proyecto

git clone https:// app

3. Acceder al Directorio
cd app

4. Crear Entorno Virtual
py -m venv ..\venv
..\venv\Scripts\activate.bat
pip freeze

5. Actualizar pip
python.exe -m pip install --upgrade pip


6. Instalar Dependencias

pip install Django==4.2.6 psycopg[binary] Pillow reportlab django-userforeignkey djangorestframework
pip install dj-database-url gunicorn PyPDF2 pylint xhtml2pdf python-decouple whitenoise



7. Crear Base de Datos

psql -h 127.0.0.1 -p 5433 -U postgres
create database db_djfull;
\q


8. Crear archivo .env
SECRET_KEY=pzmaeg=(8-0#5yt^s#lk5+1km!h3jbg4wchu6souuv!9l#%2tc

9. En Settings.py
9.1 Configurar Nueva Base de Datos
9.2 Modificar

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEBUG = True

10. Migrar
python manage.py migrate

11. Crear Super Usuario
python manage.py createsuperuser --username test --email test@mail.com

12. Levantar Servidor
py manage.py runserver 0.0.0.0:8000


C:\Program Files\PostgreSQL\17\bin



Consejo importante: si no estás usando un entorno virtual (como venv o pipenv), el archivo incluirá
 todas las dependencias instaladas globalmente, no solo las de tu proyecto. Para evitar eso y mantener 
 tu proyecto limpio y portable, te recomiendo trabajar dentro de un entorno virtual. Por ejemplo:



pip freeze > requirements.txt


python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate     # En Windows
pip install -r requirements.txt  # Para instalar dependencias si ya tienes el archivo





pip uninstall twisted-iocpsupport
pip freeze > requirements.txt
