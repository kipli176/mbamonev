from flask import render_template, session, redirect, url_for, request
from main import main_bp
from extensions import db
from models import TahunAnggaran

@main_bp.route('/select-year', methods=['GET', 'POST'])
def select_year():
    if request.method == 'POST':
        session['tahun'] = request.form['tahun']
        return redirect(url_for('auth.login'))
    
    tahun_aktif = TahunAnggaran.query.filter_by(aktif=True).all()
    return render_template('select_year.html', tahun_aktif=tahun_aktif)
# @main_bp.route("/select-year")
# def select_year():
#     tahun_list = TahunAnggaran.query.order_by(TahunAnggaran.id_tahun.desc()).all()
#     return render_template("select_year.html", tahun_list=tahun_list)

# @main_bp.route("/set-year", methods=["POST"])
# def set_year():
#     session["tahun"] = request.form.get("tahun")
#     return redirect(url_for("auth.login"))
