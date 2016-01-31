from ..models import SipkdBase, SipkdDBSession
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    SmallInteger,
    Text,
    DateTime,
    Date,
    String,
    ForeignKey,
    text,
    UniqueConstraint,
    Numeric,
    ForeignKeyConstraint,
    PrimaryKeyConstraint
    
)
from sqlalchemy.orm import (
    relationship,backref    )
    
class SipkdSpm(SipkdBase):
    __tablename__  = 'antarbyr'
    __table_args__ = (PrimaryKeyConstraint('unitkey', 'nospm'),)
    unitkey = Column(String(10), nullable=False)
    nospm = Column(String(50), nullable=False)
    kdstatus = Column(String(3), nullable=False)
    keybend = Column(String(10))
    idxsko = Column(String(10), nullable=False)
    idxttd = Column(String(10))
    nospp = Column(String(50))
    kdp3 = Column(String(10), ForeignKey('daftphk3.kdp3'))
    idxkode = Column(Integer, nullable=False)
    noreg = Column(String(5))
    ketotor = Column(String(254))
    nokontrak = Column(String(1024))
    keperluan = Column(String(4096))
    penolakan = Column(String(1))
    tglvalid = Column(DateTime)
    tglspm = Column(DateTime)
    tgspp = Column(DateTime)
    kddana = Column(String(3))
    kdkabkot = Column(String(3))

class SipkdSp2d(SipkdBase):
    __tablename__  = 'sp2d'
    __table_args__ = (PrimaryKeyConstraint('unitkey', 'nosp2d'),
                      ForeignKeyConstraint(['unitkey', 'nospm'],
                                           ['antarbyr.unitkey', 'antarbyr.nospm']),)
    unitkey = Column(String(10), nullable=False)
    nosp2d = Column(String(50), nullable=False)
    kdstatus = Column(String(3), nullable=False)
    nospm = Column(String(50))
    keybend = Column(String(10), ForeignKey('bend.keybend'))
    idxsko = Column(String(10), nullable=False)
    idxttd = Column(String(10))
    kdp3 = Column(String(10), ForeignKey('daftphk3.kdp3'))
    idxkode = Column(Integer, nullable=False)
    noreg = Column(String(5))
    ketotor = Column(String(254))
    nokontrak = Column(String(2048))
    keperluan = Column(String(4096))
    penolakan = Column(String(1))
    tglvalid = Column(DateTime)
    tglsp2d = Column(DateTime)
    tglspm = Column(DateTime)
    nobbantu = Column(String(10))

class SipkdSp2d4(SipkdBase):
    __tablename__  = 'sp2ddetd'
    __table_args__ = (PrimaryKeyConstraint('mtgkey','unitkey', 'nosp2d'),
                      ForeignKeyConstraint(['unitkey', 'nosp2d'],
                                           ['sp2d.unitkey', 'sp2d.nosp2d']),)
    mtgkey = Column(String(10), nullable=False)
    unitkey = Column(String(10), nullable=False)
    nosp2d = Column(String(50), nullable=False)
    nojetra = Column(String(2), nullable=False)
    nilai = Column(Numeric)

class SipkdSp2d5(SipkdBase):
    __tablename__  = 'sp2ddetr'
    __table_args__ = (PrimaryKeyConstraint('kdkegunit','mtgkey','unitkey', 'nosp2d'),
                      ForeignKeyConstraint(['unitkey', 'nosp2d'],
                                           ['sp2d.unitkey', 'sp2d.nosp2d']),)
    kdkegunit = Column(String(10), nullable=False)
    mtgkey = Column(String(10), nullable=False)
    unitkey = Column(String(10), nullable=False)
    nosp2d = Column(String(50), nullable=False)
    nojetra = Column(String(2), nullable=False)
    kddana = Column(String(3))
    nilai = Column(Numeric)
    
class SipkdSp2d51(SipkdBase):
    __tablename__  = 'sp2ddetrtl'
    __table_args__ = (PrimaryKeyConstraint('mtgkey','unitkey', 'nosp2d'),
                      ForeignKeyConstraint(['unitkey', 'nosp2d'],
                                           ['sp2d.unitkey', 'sp2d.nosp2d']),)
    
    mtgkey = Column(String(10), nullable=False)
    unitkey = Column(String(10), nullable=False)
    nosp2d = Column(String(50), nullable=False)
    nojetra = Column(String(2), nullable=False)
    kddana = Column(String(3))
    nilai = Column(Numeric)

class SipkdSp2d6(SipkdBase):
    __tablename__  = 'sp2ddetb'
    __table_args__ = (PrimaryKeyConstraint('mtgkey','unitkey', 'nosp2d'),
                      ForeignKeyConstraint(['unitkey', 'nosp2d'],
                                           ['sp2d.unitkey', 'sp2d.nosp2d']),)
    mtgkey = Column(String(10), nullable=False)
    unitkey = Column(String(10), nullable=False)
    nosp2d = Column(String(50), nullable=False)
    nojetra = Column(String(2), nullable=False)
    kddana = Column(String(3))
    nilai = Column(Numeric)
    
class SipkdSp2dPjk(SipkdBase):
    __tablename__  = 'sp2dpjk'
    __table_args__ = (PrimaryKeyConstraint('pjkkey','unitkey', 'nosp2d'),
                      ForeignKeyConstraint(['unitkey', 'nosp2d'],
                                           ['sp2d.unitkey', 'sp2d.nosp2d']),)
    unitkey = Column(String(10), nullable=False)
    nosp2d = Column(String(50), nullable=False)
    pjkkey = Column(String(10), ForeignKey('jpajak.pjkkey'), nullable=False)
    nilai = Column(Numeric)
    keterangan = Column(String(512))

class SipkdRek6(SipkdBase):
    __tablename__  = 'matangb'
    mtgkey = Column(String(10), primary_key=True, nullable=False)
    kdper = Column(String(30))
    nmper = Column(String(200))
    mtglevel = Column(String(2), nullable=False)
    kdkhusus = Column(String(1))
    type = Column(String(2))

class SipkdRek4(SipkdBase):
    __tablename__  = 'matangd'
    mtgkey = Column(String(10), primary_key=True, nullable=False)
    kdper = Column(String(30))
    nmper = Column(String(200))
    mtglevel = Column(String(2), nullable=False)
    kdkhusus = Column(String(1), nullable=False)
    type = Column(String(2))

class SipkdRek5(SipkdBase):
    __tablename__  = 'matangr'
    mtgkey = Column(String(10), primary_key=True, nullable=False)
    kdper = Column(String(30))
    nmper = Column(String(200))
    mtglevel = Column(String(2), nullable=False)
    kdkhusus = Column(String(1))
    type = Column(String(2))

class SipkdVendor(SipkdBase):
    __tablename__  = 'daftphk3'
    kdp3 = Column(String(10), primary_key=True, nullable=False)
    nmp3 = Column(String(100))
    nminst = Column(String(100))
    norcp3 = Column(String(50))
    nmbank = Column(String(50))
    jnsusaha = Column(String(50))
    alamat = Column(String(200))
    telepon = Column(String(20))
    npwp = Column(String(30))
    unitkey = Column(String(10))

class SipkdBend(SipkdBase):
    __tablename__  = 'bend'
    keybend = Column(String(10), primary_key=True, nullable=False)
    jns_bend = Column(String(2), nullable=False)
    nip = Column(String(30), ForeignKey('pegawai.nip'), nullable=False)
    kdbank = Column(String(2), ForeignKey('daftbank.kdbank'))
    unitkey = Column(String(10), nullable=False)
    jab_bend = Column(String(100))
    rekbend = Column(String(100))
    saldobend = Column(Numeric)
    npwpbend = Column(String(30))
    tglstopbend = Column(DateTime)
    saldobendt = Column(Numeric)

class SipkdPegawai(SipkdBase):
    __tablename__  = 'pegawai'
    nip = Column(String(30), primary_key=True, nullable=False)
    kdgol = Column(String(10))
    unitkey = Column(String(10))
    nama = Column(String(100))
    alamat = Column(String(200))
    jabatan = Column(String(200))
    pddk = Column(String(30))

class SipkdBank(SipkdBase):
    __tablename__  = 'daftbank'
    kdbank = Column(String(2), primary_key=True, nullable=False)
    nmbank = Column(String(50))
    akbank = Column(String(20))
    alamat = Column(String(200))
    telepon = Column(String(20))
    cabang = Column(String(50))

class SipkdPjk(SipkdBase):
    __tablename__  = 'jpajak'
    pjkkey = Column(String(10), primary_key=True, nullable=False)
    kdpajak = Column(String(10))
    nmpajak = Column(String(50))
    rumuspjk = Column(String(100))

