import os
from flask import Flask
from core.dao import LeaderboardDAO
from config import DevelopmentConfig, ProductionConfig
from core.utils import data_local_filter, seed_inicial

app = Flask(__name__)

if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

app.jinja_env.filters['data_local'] = data_local_filter

dao = LeaderboardDAO("leaderboard.db")
dao.criar_tabela()

seed_inicial(dao)

from core import routes