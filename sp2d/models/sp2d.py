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
    Numeric
)
from sqlalchemy.orm import (
    relationship,backref    )
    
class Sp2dAdvice(SipkdBase):
    __tablename__  = 'advice'
    #__table_args__ = {'extend_existing':True,'autoload':True}   
    advno       = Column(String(30), nullable=False, primary_key=True)
    advtgl      = Column(DateTime, nullable=False)
    tahun       = Column(String(4), nullable=False)
    adv_notes   = Column(String(255))
    bank_nm     = Column(String(50))
    dtcreated   = Column(DateTime)
    createdby   = Column(String(50)) 
    dtupdated   = Column(DateTime)
    updateby    = Column(String(50)) 
  
class Sp2dAdviceDet(SipkdBase):
    __tablename__  = 'advicedet'
    #__table_args__ = {'extend_existing':True,'autoload':True}   
    advno       = Column(String(30), nullable=False, primary_key=True)
    sp2dno      = Column(String(30), ForeignKey('sp2d.sp2dno'), nullable=False, primary_key=True)
    keterangan  = Column(String(250))
    sp2dcurr    = Column(Numeric)
    ppn         = Column(Numeric)
    pph21       = Column(Numeric)
    pph22       = Column(Numeric)
    pph23       = Column(Numeric)
    bppn        = Column(Numeric)
    bpph21      = Column(Numeric)
    bpph22      = Column(Numeric)
    bpph23      = Column(Numeric)
    nossp       = Column(String(250)) 
    tglsetor    = Column(DateTime)
    #sp2d        = relationship("Sp2d", backref="advicedet")

class Sp2d(SipkdBase):
    __tablename__  = 'sp2ds'
    #__table_args__ = {'extend_existing':True,'autoload':True}   
    sp2dno             = Column(String(30), nullable=False, primary_key=True)
    sp2ddate           = Column(DateTime)
    isgaji             = Column(SmallInteger)
    spmno              = Column(String(30)) 
    spmdate            = Column(DateTime)
    validatespd        = Column(SmallInteger)
    spdno              = Column(String(30)) 
    spddate            = Column(DateTime)
    spdvalidate        = Column(SmallInteger)
    tahun              = Column(String(4)) 
    unitkd             = Column(String(10)) 
    bknama             = Column(String(100)) 
    bankposnm          = Column(String(50))
    bankaccount        = Column(String(25))
    sp2dtype           = Column(String(5))
    npwp               = Column(String(25))
    paymentfor         = Column(String(600)) 
    belanjatype        = Column(String(5))
    pot1no             = Column(String(15)) 
    pot1txt            = Column(String(150)) 
    pot1num            = Column(Numeric)
    pot1notes          = Column(String(50)) 
    pot2no             = Column(String(15))
    pot2txt            = Column(String(150))
    pot2num            = Column(Numeric)
    pot2notes          = Column(String(50)) 
    pot3no             = Column(String(15))
    pot3txt            = Column(String(150)) 
    pot3num            = Column(Numeric)
    pot3notes          = Column(String(50))
    pot4no             = Column(String(15))
    pot4txt            = Column(String(150)) 
    pot4num            = Column(Numeric)
    pot4notes          = Column(String(50)) 
    pot5no             = Column(String(15))
    pot5num            = Column(Numeric)
    pot5notes          = Column(String(150)) 
    isppnmanual        = Column(SmallInteger)
    ppn                = Column(Numeric)
    ppnamount          = Column(Numeric)
    ispphmanual        = Column(SmallInteger) 
    pph                = Column(Numeric)
    pphamount          = Column(Numeric)
    sp2damount         = Column(Numeric)
    sp2damounttxt      = Column(String(255)) 
    dtcreated          = Column(DateTime)
    createdby          = Column(String(50))
    dtupdated          = Column(DateTime)
    updateby           = Column(String(50))
    banksumbernm       = Column(String(50))
    banksumberaccount  = Column(String(25))
    ttdjab             = Column(String(100))
    ttdnama            = Column(String(100))
    ttdnip             = Column(String(100))
    posted             = Column(SmallInteger)
    isbud              = Column(SmallInteger)
    isrobject          = Column(SmallInteger)
    sdana              = Column(String(15))
    infix              = Column(String(15))
    pot5txt            = Column(String(50))
    sppdate            = Column(DateTime)
    sppno              = Column(String(50))
    sppamount          = Column(Numeric)
    sppamounttxt       = Column(String(255))
    isbendahara        = Column(SmallInteger)
    kegiatankdfull     = Column(String(20))
    pptknama           = Column(String(50))
    pptknip            = Column(String(30))
    pptkjab            = Column(String(50))
    perusahaanbentuk   = Column(String(3))
    uraianpekerjaan    = Column(String(800))
    waktu              = Column(String(50))
    islanjutan         = Column(SmallInteger, nullable=False)
    perusahaankontrak  = Column(String(50))
    perusahaanpemilik  = Column(String(50))
    perusahaanalamat   = Column(String(50))
    bknip              = Column(String(30))
    bknamattd          = Column(String(100))
    sppbulan           = Column(String(20))
    skup               = Column(String(50))
    tglup              = Column(DateTime)
    sptjmno            = Column(String(50))
    bapno              = Column(String(500))
    bapdate            = Column(DateTime)
    kontrakdate        = Column(DateTime)
    kontrakvalue       = Column(Numeric)
    daftar             = Column(String(50))
    bagi               = Column(String(50))
    status             = Column(Integer, nullable=False)
    sp2dnetto          = Column(Numeric)
    sp2dnettotxt       = Column(String(250))
    #posted_sap         = Column(SmallInteger)
  
  
"""class SipkdRek4(SipkdBase):
    __tablename__  = 'MATANGD'
    __table_args__ = {'extend_existing':True,'autoload':True}   
    
class SipkdUnit(SipkdBase):
    __tablename__  = 'DAFTUNIT'
    __table_args__ = {'extend_existing':True,'autoload':True}    
    
class SipkdSts(SipkdBase):
    __tablename__  = 'STS'
    __table_args__ = {'extend_existing':True,'autoload':True}    

class SipkdTbp(SipkdBase):
    __tablename__  = 'TBP'
    __table_args__ = {'extend_existing':True,'autoload':True}    
    
class SipkdTbpSts(SipkdBase):
    __tablename__  = 'TBPSTS'
    __table_args__ = {'extend_existing':True,'autoload':True}    

class SipkdTbpDetD(SipkdBase):
    __tablename__  = 'TBPDETD'
    __table_args__ = {'extend_existing':True,'autoload':True}    
    
class SipkdSkp(SipkdBase):
    __tablename__  = 'Skp'
    __table_args__ = {'extend_existing':True,'autoload':True}    
    
class SipkdMatangd(SipkdBase):
    __tablename__  = 'SKPDET'
    __table_args__ = {'extend_existing':True,'autoload':True}    

class SipkdSkpTbp(SipkdBase):
    __tablename__  = 'SKPSTS'
    __table_args__ = {'extend_existing':True,'autoload':True}    
    
class SipkdMatangd(SipkdBase):
    __tablename__  = 'SKPTBP'
    __table_args__ = {'extend_existing':True,'autoload':True}    
"""