from flask import render_template
from flask_login import login_required, current_user
from dashboard import dashboard_bp
from models import Modul, PeranModulIzin
from extensions import db, cache


@dashboard_bp.route('/dashboard')
@login_required
@cache.cached()
def index():
    # Ambil ID peran user
    peran_ids = [p.id_peran for p in current_user.perans]
    
    # Ambil modul yang bisa diakses
    modul_ids = db.session.query(PeranModulIzin.id_modul).filter(
        PeranModulIzin.id_peran.in_(peran_ids)
    ).distinct().subquery()
    
    # Ambil parent modul (id_induk IS NULL) yang aktif
    parent_moduls = Modul.query.filter(
        Modul.id.in_(modul_ids),
        Modul.aktif == True,
        Modul.id_induk.is_(None)
    ).order_by(Modul.urutan).all()
    
    # Buat struktur parent-child
    menu = []
    for parent in parent_moduls:
        children = Modul.query.filter(
            Modul.id_induk == parent.id,
            Modul.id.in_(modul_ids),
            Modul.aktif == True
        ).order_by(Modul.urutan).all()
        menu.append({'parent': parent, 'children': children})
    
    return render_template('dashboard.html', menu=menu)

# @dashboard_bp.route('/realisasi')
# @login_required
# def realisasi():
#     data = with_tahun(Subunit.query).all()   # otomatis filter tahun
#     return render_template('realisasi.html', data=data)

