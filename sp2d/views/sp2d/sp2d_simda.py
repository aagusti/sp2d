import os
import uuid
from ...tools import row2dict, xls_reader
from datetime import datetime
from sqlalchemy import not_, func, and_, or_
from pyramid.view import (
    view_config,
    )
from pyramid.httpexceptions import (
    HTTPFound,
    )
import colander
from deform import (
    Form,
    widget,
    ValidationFailure,
    )
from ...models import (
    SipkdDBSession,
    )
from ...models.sp2d_simda import (
    SimdaSp2d, SimdaSpm, SimdaSpmDet, SimdaSpmPot, SimdaSpmInfo
    )
    
from datatables import ColumnDT, DataTables
from ...views.base_view import BaseViews
    

SESS_ADD_FAILED = 'Tambah sp2d gagal'
SESS_EDIT_FAILED = 'Edit sp2d gagal'


def get_query():
    sub_amt = SipkdDBSession.query(SimdaSpmDet.tahun, SimdaSpmDet.no_spm, 
                                  func.sum(SimdaSpmDet.nilai).label('sp2damt')).\
                group_by(SimdaSpmDet.tahun, SimdaSpmDet.no_spm,).subquery()
                
    sub_pot = SipkdDBSession.query(SimdaSpmPot.tahun, SimdaSpmPot.no_spm, 
                                  func.sum(SimdaSpmPot.nilai).label('sp2dpot')).\
                group_by(SimdaSpmPot.tahun, SimdaSpmPot.no_spm,).subquery()

    sub_ppn = SipkdDBSession.query(SimdaSpmInfo.tahun, SimdaSpmInfo.no_spm, 
                                  func.sum(SimdaSpmInfo.nilai).label('sp2dppn')).\
                group_by(SimdaSpmInfo.tahun, SimdaSpmInfo.no_spm,).\
                filter(SimdaSpmInfo.kd_pot_rek==11).subquery()
                
    sub_pph = SipkdDBSession.query(SimdaSpmInfo.tahun, SimdaSpmInfo.no_spm, 
                                  func.sum(SimdaSpmInfo.nilai).label('sp2dpph')).\
                group_by(SimdaSpmInfo.tahun, SimdaSpmInfo.no_spm,).\
                filter(SimdaSpmInfo.kd_pot_rek<>11).subquery()
    
    q = SipkdDBSession.query(SimdaSp2d.no_sp2d, SimdaSp2d.tgl_sp2d,
                                 SimdaSpm.uraian, SimdaSpm.nm_penerima, 
                                 SimdaSpm.bank_penerima, SimdaSpm.rek_penerima, 
                                 SimdaSpm.npwp,
                                 sub_amt.c.sp2damt,
                                 sub_pot.c.sp2dpot,
                                 sub_ppn.c.sp2dppn,
                                 sub_pph.c.sp2dpph,
                                 (sub_amt.c.sp2damt- sub_pot.c.sp2dpot-
                                 sub_ppn.c.sp2dppn-sub_pph.c.sp2dpph).label('sp2dnet'),
                                 ).\
                join(SimdaSpm).\
                outerjoin(sub_amt, and_(SimdaSpm.tahun==sub_amt.c.tahun,SimdaSpm.no_spm==sub_amt.c.no_spm)).\
                outerjoin(sub_pot, and_(SimdaSpm.tahun==sub_pot.c.tahun,SimdaSpm.no_spm==sub_pot.c.no_spm)).\
                outerjoin(sub_ppn, and_(SimdaSpm.tahun==sub_ppn.c.tahun,SimdaSpm.no_spm==sub_ppn.c.no_spm)).\
                outerjoin(sub_pph, and_(SimdaSpm.tahun==sub_pph.c.tahun,SimdaSpm.no_spm==sub_pph.c.no_spm))
    return q
    
class AddSchema(colander.Schema):
    kode = colander.SchemaNode(
                    colander.String(),
                    validator=colander.Length(max=18))
                    
    nama = colander.SchemaNode(
                    colander.String())
    tahun = colander.SchemaNode(
                    colander.Integer(),
                    default = datetime.now().year,
                    missing=colander.drop)
    disabled = colander.SchemaNode(
                    colander.Boolean())

class EditSchema(AddSchema):
    id = colander.SchemaNode(colander.String(),
            missing=colander.drop,
            widget=widget.HiddenWidget(readonly=True))
            
class view_sp2d(BaseViews):
    ########                    
    # List #
    ########    
    @view_config(route_name='sp2d-simda', renderer='templates/sp2d-simda/list.pt',
                 permission='read')
    def view_list(self):
        return dict(a={})
        
    ##########                    
    # Action #
    ##########    
    @view_config(route_name='sp2d-simda-act', renderer='json',
                 permission='read')
    def sp2d_act(self):
        ses = self.request.session
        req = self.request
        params = req.params
        url_dict = req.matchdict
        
        if url_dict['act']=='grid':
            columns = []
            columns.append(ColumnDT('no_sp2d'))
            columns.append(ColumnDT('no_sp2d'))
            columns.append(ColumnDT('tgl_sp2d',   filter = self._DT_strftime))
            columns.append(ColumnDT('uraian'))
            columns.append(ColumnDT('sp2damt',  filter = self._DT_number_format))
            columns.append(ColumnDT('sp2dppn',  filter = self._DT_number_format))
            columns.append(ColumnDT('sp2dpph',  filter = self._DT_number_format))
            columns.append(ColumnDT('sp2dpot',  filter = self._DT_number_format))
            columns.append(ColumnDT('sp2dnet',  filter = self._DT_number_format))
            columns.append(ColumnDT('nm_penerima'))
            columns.append(ColumnDT('bank_penerima'))
            columns.append(ColumnDT('rek_penerima'))
            columns.append(ColumnDT('npwp'))
            
            query = get_query()
            
            rowTable = DataTables(req, SimdaSp2d, query, columns)
            return rowTable.output_result()
            
        elif url_dict['act']=='csv':
             
            return
    #######    
    # Add #
    #######
    def form_validator(self, form, value):
        if 'id' in form.request.matchdict:
            uid = form.request.matchdict['id']
            q = DBSession.query(sp2d).filter_by(id=uid)
            sp2d = q.first()
        else:
            sp2d = None
                
    def get_form(self, class_form, row=None):
        schema = class_form(validator=self.form_validator)
        schema = schema.bind()
        schema.request = self.request
        if row:
          schema.deserialize(row)
        return Form(schema, buttons=('simpan','batal'))
        
    def save(self, values, user, row=None):
        if not row:
            row = sp2d()
            row.created = datetime.now()
            row.create_uid = user.id
        row.from_dict(values)
        row.updated = datetime.now()
        row.update_uid = user.id
        row.disabled = 'disabled' in values and values['disabled'] and 1 or 0
        DBSession.add(row)
        DBSession.flush()
        return row
        
    def save_request(self, values, row=None):
        if 'id' in self.request.matchdict:
            values['id'] = self.request.matchdict['id']
        row = self.save(values, self.request.user, row)
        self.request.session.flash('sp2d sudah disimpan.')
            
    def route_list(self):
        return HTTPFound(location=self.request.route_url('sp2d-simda'))
        
    def session_failed(self, session_name):
        r = dict(form=self.session[session_name])
        del self.session[session_name]
        return r
        
    @view_config(route_name='sp2d-simda-add', renderer='templates/sp2d-simda/add.pt',
                 permission='add')
    def view_sp2d_add(self):
        req = self.request
        ses = self.session
        form = self.get_form(AddSchema)
        if req.POST:
            if 'simpan' in req.POST:
                controls = req.POST.items()
                try:
                    c = form.validate(controls)
                except ValidationFailure, e:
                    req.session[SESS_ADD_FAILED] = e.render()               
                    return HTTPFound(location=req.route_url('sp2d-simda-add'))
                self.save_request(dict(controls))
            return self.route_list()
        elif SESS_ADD_FAILED in req.session:
            return self.session_failed(SESS_ADD_FAILED)
        return dict(form=form.render())

        
    ########
    # Edit #
    ########
    def query_id(self):
        return DBSession.query(sp2d).filter_by(id=self.request.matchdict['id'])
        
    def id_not_found(self):    
        msg = 'sp2d ID %s Tidak Ditemukan.' % self.request.matchdict['id']
        request.session.flash(msg, 'error')
        return route_list()

    @view_config(route_name='sp2d-simda-edit', renderer='templates/sp2d-simda/edit.pt',
                 permission='edit')
    def view_sp2d_edit(self):
        request = self.request
        row = self.query_id().first()
        if not row:
            return id_not_found(request)
        form = self.get_form(EditSchema)
        if request.POST:
            if 'simpan' in request.POST:
                controls = request.POST.items()
                print controls
                try:
                    c = form.validate(controls)
                except ValidationFailure, e:
                    request.session[SESS_EDIT_FAILED] = e.render()               
                    return HTTPFound(location=request.route_url('sp2d-simda-edit',
                                      id=row.id))
                self.save_request(dict(controls), row)
            return self.route_list()
        elif SESS_EDIT_FAILED in request.session:
            return self.session_failed(SESS_EDIT_FAILED)
        values = row.to_dict()
        for value in values:
            if not values[value]:
                values[value] = colander.null
        
        return dict(form=form.render(sp2dstruct=values))

    ##########
    # Delete #
    ##########    
    @view_config(route_name='sp2d-simda-delete', renderer='templates/sp2d-simda/delete.pt',
                 permission='delete')
    def view_sp2d_delete(self):
        request = self.request
        q = self.query_id()
        row = q.first()
        
        if not row:
            return self.id_not_found(request)
        form = Form(colander.Schema(), buttons=('hapus','batal'))
        if request.POST:
            if 'hapus' in request.POST:
                msg = 'sp2d ID %d %s sudah dihapus.' % (row.id, row.nama)
                try:
                  q.delete()
                  DBSession.flush()
                except:
                  msg = 'sp2d ID %d %s tidak dapat dihapus.' % (row.id, row.nama)
                request.session.flash(msg)
            return self.route_list()
        return dict(row=row,
                     form=form.render())

    ##########                    
    # CSV #
    ##########    
        
    @view_config(route_name='sp2d-simda-csv', renderer='csv',
                 permission='read')
    def export_csv(self):
        request = self.request
        query = get_query().filter(SimdaSp2d.no_sp2d.in_(request.params['data'].split(',')))
                                          
        r = query.first()
        header = r.keys()
        query = query.all()
        rows = []
        for item in query:
            rows.append(list(item))

        # override attributes of response
        filename = 'sp2d%s.csv' % datetime.now().strftime('%Y%m%d%H%M%S')

        self.request.response.content_disposition = 'attachment;filename=' + filename

        return {
          'header': header,
          'rows': rows,
        }
