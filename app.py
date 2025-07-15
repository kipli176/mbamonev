from flask import Flask, request, redirect, url_for, g, session
from sqlalchemy.event import listens_for
from config import Config
from extensions import db, login_manager, cache  
from auth import auth_bp
from main import main_bp
from dashboard import dashboard_bp
from models import TahunAnggaran

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # ✅ Konfigurasi caching (gunakan SimpleCache default)
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 3000})

    # ---------- MIDDLEWARE ----------
    @app.before_request
    def set_tahun_filter():
        if request.endpoint and request.endpoint not in [
            'main.select_year', 'auth.login', 'auth.logout', 'static'
        ]:
            tahun_id = session.get('tahun')
            if not tahun_id:
                return redirect(url_for('main.select_year'))
            g.tahun = TahunAnggaran.query.get_or_404(tahun_id)

    # ---------- SQLAlchemy EVENT (opsional) ----------
    @listens_for(db.session, "do_orm_execute")
    @listens_for(db.session, "do_orm_execute")
    def auto_filter_tahun(execute_state):
        # Pastikan ini SELECT dan punya mapper
        if (execute_state.is_select and
            execute_state.statement.is_select and  # SELECT statement
            hasattr(execute_state, 'mapper') and
            execute_state.mapper and
            hasattr(g, 'tahun') and g.tahun):

            model = execute_state.mapper.class_
            if hasattr(model, 'id_tahun'):
                execute_state.statement = execute_state.statement.where(
                    model.id_tahun == g.tahun.id_tahun
                )

    # ---------- REGISTER BLUEPRINT ----------
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    
    @app.route('/')
    def index():
        return redirect(url_for('main.select_year'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5005, debug=True)