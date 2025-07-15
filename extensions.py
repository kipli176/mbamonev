from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import g 
from flask_caching import Cache  # ✅ Tambahkan ini

db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()  # ✅ Inisialisasi objek cache
login_manager.login_view = 'auth.login'

def with_tahun(query):
    """Inject filter id_tahun otomatis."""
    if hasattr(g, 'tahun') and g.tahun:
        model = query.column_descriptions[0]['type']
        if hasattr(model, 'id_tahun'):
            return query.filter(model.id_tahun == g.tahun.id_tahun)
    return query