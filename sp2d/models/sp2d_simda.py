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
 
class SimdaBank(SipkdBase):
    __tablename__  = 'ref_bank'
    kd_bank = Column(Integer, nullable=False, primary_key=True)
    nm_bank = Column(String(50), nullable=False)
    no_rekening = Column(String(50))
    kd_rek_1 = Column(Integer, nullable=False)
    kd_rek_2 = Column(Integer, nullable=False)
    kd_rek_3 = Column(Integer, nullable=False)
    kd_rek_4 = Column(Integer, nullable=False)
    kd_rek_5 = Column(Integer, nullable=False)

class SimdaSpm(SipkdBase):
    __tablename__  = 'ta_spm'
    __table_args__ = (PrimaryKeyConstraint('tahun', 'no_spm'),)
    tahun = Column(Integer, nullable=False)
    no_spm = Column(String(50), nullable=False)
    kd_urusan = Column(Integer, nullable=False)
    kd_bidang = Column(Integer, nullable=False)
    kd_unit = Column(Integer, nullable=False)
    kd_sub = Column(Integer, nullable=False)
    no_spp = Column(String(50))
    jn_spm = Column(Integer, nullable=False)
    tgl_spm = Column(DateTime, nullable=False)
    uraian = Column(String(255))
    nm_penerima = Column(String(100))
    bank_penerima = Column(String(50))
    rek_penerima = Column(String(50))
    npwp = Column(String(20))
    bank_pembayar = Column(Integer)
    nm_verifikator = Column(String(50))
    nm_penandatangan = Column(String(50))
    nip_penandatangan = Column(String(21))
    jbt_penandatangan = Column(String(75))
    kd_edit = Column(Integer)
    
    
class SimdaSpmDet(SipkdBase):
    __tablename__  = 'ta_spm_rinc'
    __table_args__ = (PrimaryKeyConstraint('tahun', 'no_spm', 'no_id'),
                      ForeignKeyConstraint(['tahun', 'no_spm'], ['ta_spm.tahun', 'ta_spm.no_spm']),)
    tahun = Column(Integer, nullable=False)
    no_spm = Column(String(50), nullable=False)
    no_id = Column(Integer, nullable=False)
    kd_urusan = Column(Integer, nullable=False)
    kd_bidang = Column(Integer, nullable=False)
    kd_unit = Column(Integer, nullable=False)
    kd_sub = Column(Integer, nullable=False)
    kd_prog = Column(Integer, nullable=False)
    id_prog = Column(Integer, nullable=False)
    kd_keg = Column(Integer, nullable=False)
    kd_rek_1 = Column(Integer, nullable=False)
    kd_rek_2 = Column(Integer, nullable=False)
    kd_rek_3 = Column(Integer, nullable=False)
    kd_rek_4 = Column(Integer, nullable=False)
    kd_rek_5 = Column(Integer, nullable=False)
    nilai = Column(Numeric, nullable=False)

class SimdaSpmInfo(SipkdBase):
    __tablename__  = 'ta_spm_info'
    __table_args__ = (PrimaryKeyConstraint('tahun', 'no_spm', 'kd_pot_rek'),
                      ForeignKeyConstraint(['tahun', 'no_spm'], ['ta_spm.tahun', 'ta_spm.no_spm']),)    
    tahun = Column(Integer, nullable=False)
    no_spm = Column(String(50), nullable=False)
    kd_pot_rek = Column(Integer, ForeignKey("ref_pot_spm.kd_pot"), nullable=False)
    nilai = Column(Numeric, nullable=False)
    
class SimdaSpmPot(SipkdBase):
    __tablename__  = 'ta_spm_pot'
    __table_args__ = (PrimaryKeyConstraint('tahun', 'no_spm', 'kd_pot_rek'),
                      ForeignKeyConstraint(['tahun', 'no_spm'], ['ta_spm.tahun', 'ta_spm.no_spm']),)        
    tahun = Column(Integer, nullable=False)
    no_spm = Column(String(50), nullable=False)
    kd_pot_rek = Column(Integer, ForeignKey("ref_pot_spm.kd_pot"), nullable=False)
    nilai = Column(Numeric, nullable=False)

class SimdaRefSpmPot(SipkdBase):
    __tablename__  = 'ref_pot_spm'
    kd_pot = Column(Integer, nullable=False, primary_key=True)
    nm_pot = Column(String(50), nullable=False)
    kd_map = Column(String(6))

class SimdaSp2d(SipkdBase):
    __tablename__  = 'ta_sp2d'
    __table_args__ = (ForeignKeyConstraint(['tahun', 'no_spm'], ['ta_spm.tahun', 'ta_spm.no_spm']),)
    
    tahun = Column(Integer, nullable=False, primary_key=True)
    no_sp2d = Column(String(50), nullable=False, primary_key=True)
    no_spm = Column(String(50), nullable=False)
    tgl_sp2d = Column(DateTime, nullable=False)
    kd_bank = Column(Integer, nullable=False)
    no_bku = Column(Integer, nullable=False)
    nm_penandatangan = Column(String(50))
    nip_penandatangan = Column(String(21))
    jbt_penandatangan = Column(String(75))
    keterangan = Column(String(255), nullable=False)
    
    spm = relationship(SimdaSpm, foreign_keys=[tahun, no_spm])
