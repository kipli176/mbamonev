from flask import render_template
from flask_login import login_required, current_user
from dashboard import dashboard_bp
from models import Modul, PeranModulIzin
from extensions import db
from sqlalchemy import text

@dashboard_bp.route('/anggaran/dashboard-detail')
@login_required
def detail():
    return render_template('dashboard_detail.html')
@dashboard_bp.route('/anggaran/dashboard-global')
@login_required
def globale():
    return render_template('dashboard_globale.html')
@dashboard_bp.route('/anggaran/realisasi-univ')
@login_required
def univ():
    return render_template('realisasi_univ.html')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Ambil ID peran user
    peran_ids = [p.id_peran for p in current_user.perans]

    # Ambil modul yang bisa diakses user dari tabel izin
    modul_ids = db.session.query(PeranModulIzin.id_modul).filter(
        PeranModulIzin.id_peran.in_(peran_ids)
    ).distinct().subquery()

    # Ambil semua parent modul (tidak punya induk dan aktif)
    parent_moduls = Modul.query.filter(
        Modul.id.in_(modul_ids),
        Modul.aktif == True,
        Modul.id_induk.is_(None)
    ).order_by(Modul.urutan).all()

    # Susun menu struktur parent-child
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
from flask import render_template, g
from flask_login import login_required
from dashboard import dashboard_bp
from models import PaguRealisasi, UnitKerja
from extensions import db
from sqlalchemy import case, func


@dashboard_bp.route('/dashboard-global')
@login_required
def dashboard_global():
    tahun_id = g.tahun.id_tahun

    # Total Pagu
    total_pagu = db.session.query(func.coalesce(func.sum(PaguRealisasi.jumlah), 0)).filter(
        PaguRealisasi.id_tahun == tahun_id,
        PaguRealisasi.jenis == 'PAGU'
    ).scalar()

    # Total Realisasi
    total_realisasi = db.session.query(func.coalesce(func.sum(PaguRealisasi.jumlah), 0)).filter(
        PaguRealisasi.id_tahun == tahun_id,
        PaguRealisasi.jenis == 'REALISASI'
    ).scalar()

    capaian = round((total_realisasi / total_pagu) * 100, 2) if total_pagu > 0 else 0
    sisa = total_pagu - total_realisasi

    # Komposisi Jenis Dana
    jenis_dana_agg = db.session.query(
        PaguRealisasi.jenis_data,
        func.coalesce(func.sum(PaguRealisasi.jumlah), 0)
    ).filter(
        PaguRealisasi.id_tahun == tahun_id,
        PaguRealisasi.jenis == 'REALISASI'
    ).group_by(PaguRealisasi.jenis_data).all()

    # Grafik Pagu vs Realisasi per Unit + nama_unit
    grafik_per_unit = db.session.query(
        PaguRealisasi.kode_unit,
        UnitKerja.nama_unit,
        func.sum(case((PaguRealisasi.jenis == 'PAGU', PaguRealisasi.jumlah), else_=0)).label('pagu'),
        func.sum(case((PaguRealisasi.jenis == 'REALISASI', PaguRealisasi.jumlah), else_=0)).label('realisasi')
    ).join(UnitKerja, UnitKerja.kode_unit == PaguRealisasi.kode_unit).filter(
        PaguRealisasi.id_tahun == tahun_id
    ).group_by(PaguRealisasi.kode_unit, UnitKerja.nama_unit).order_by(UnitKerja.nama_unit).all()



    return render_template("dashboard_global.html",
        total_pagu=total_pagu,
        total_realisasi=total_realisasi,
        capaian=capaian,
        sisa=sisa,
        jenis_dana_agg=jenis_dana_agg,
        grafik_per_unit=grafik_per_unit
    )
