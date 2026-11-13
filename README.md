## Implementando um placar de exemplo usando Flask

Projeto inicial

Lembre-se de ativar o venv, instalar o flask e executar o projeto com python main.py

 python -m venv .venv

  .\.venv\Scripts\activate

  pip install -r requirements.txt

  python main.py

ou

  gunicorn --workers 1 --bind 0.0.0.0:$PORT main:app