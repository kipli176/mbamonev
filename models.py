from extensions import db
from flask_login import UserMixin

class TahunAnggaran(db.Model):
    __tablename__ = 'tahun_anggaran'
    id_tahun = db.Column(db.Integer, primary_key=True)
    nama_tahun = db.Column(db.String(9), unique=True, nullable=False)
    aktif = db.Column(db.Boolean, default=False)

class Pengguna(UserMixin, db.Model):
    __tablename__ = 'pengguna'
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    aktif = db.Column(db.Boolean, default=True)
    
    perans = db.relationship('PenggunaPeran', backref='pengguna', lazy=True)

class Peran(db.Model):
    __tablename__ = 'peran'
    id = db.Column(db.Integer, primary_key=True)
    nama_peran = db.Column(db.String(50), unique=True, nullable=False)
    deskripsi = db.Column(db.Text)

class PenggunaPeran(db.Model):
    __tablename__ = 'pengguna_peran'
    id = db.Column(db.Integer, primary_key=True)
    id_pengguna = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)
    id_peran = db.Column(db.Integer, db.ForeignKey('peran.id'), nullable=False)

class Modul(db.Model):
    __tablename__ = 'modul'
    id = db.Column(db.Integer, primary_key=True)
    nama_modul = db.Column(db.String(100), nullable=False)
    grup_modul = db.Column(db.String(50))
    path = db.Column(db.String(255))
    ikon = db.Column(db.String(10))
    urutan = db.Column(db.Integer)
    id_induk = db.Column(db.Integer, db.ForeignKey('modul.id'))
    publik = db.Column(db.Boolean, default=False)
    aktif = db.Column(db.Boolean, default=True)
    
    children = db.relationship('Modul', backref=db.backref('parent', remote_side=[id]))

class PeranModulIzin(db.Model):
    __tablename__ = 'peran_modul_izin'
    id = db.Column(db.Integer, primary_key=True)
    id_peran = db.Column(db.Integer, db.ForeignKey('peran.id'), nullable=False)
    id_modul = db.Column(db.Integer, db.ForeignKey('modul.id'), nullable=False)
    id_izin = db.Column(db.Integer, db.ForeignKey('izin.id'), nullable=False)

class Izin(db.Model):
    __tablename__ = 'izin'
    id = db.Column(db.Integer, primary_key=True)
    nama_izin = db.Column(db.String(50), unique=True, nullable=False)

from extensions import login_manager
@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))