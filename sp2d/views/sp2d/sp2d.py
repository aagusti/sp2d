import os
import uuid
from ...tools import row2dict, xls_reader
from datetime import datetime
from sqlalchemy import not_, func
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
from ...models.sp2d import (
    Sp2dAdviceDet,
    Sp2dAdvice,
    Sp2d
    )
    
from datatables import ColumnDT, DataTables
from ...views.base_view import BaseViews
    

SESS_ADD_FAILED = 'Tambah sp2d gagal'
SESS_EDIT_FAILED = 'Edit sp2d gagal'


                
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
    @view_config(route_name='sp2d', renderer='templates/sp2d/list.pt',
                 permission='read')
    def view_list(self):
        return dict(a={})
        
    ##########                    
    # Action #
    ##########    
    @view_config(route_name='sp2d-act', renderer='json',
                 permission='read')
    def sp2d_act(self):
        ses = self.request.session
        req = self.request
        params = req.params
        url_dict = req.matchdict
        
        if url_dict['act']=='grid':
            columns = []
            columns.append(ColumnDT('sp2dno'))
            columns.append(ColumnDT('sp2dno'))
            columns.append(ColumnDT('sp2ddate',   filter = self._DT_strftime))
            columns.append(ColumnDT('paymentfor'))
            columns.append(ColumnDT('sp2damount', filter = self._DT_number_format))
            columns.append(ColumnDT('ppnamount',  filter = self._DT_number_format))
            columns.append(ColumnDT('pphamount',  filter = self._DT_number_format))
            columns.append(ColumnDT('pot1num',    filter = self._DT_number_format))
            columns.append(ColumnDT('sp2dnetto',  filter = self._DT_number_format))
            columns.append(ColumnDT('bknama'))
            columns.append(ColumnDT('bankposnm'))
            columns.append(ColumnDT('bankaccount'))
            
            query = SipkdDBSession.query(Sp2d).join(Sp2dAdviceDet).\
                                   filter(Sp2d.sp2dno==Sp2dAdviceDet.sp2dno)
            rowTable = DataTables(req, Sp2d, query, columns)
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
        return HTTPFound(location=self.request.route_url('sp2d'))
        
    def session_failed(self, session_name):
        r = dict(form=self.session[session_name])
        del self.session[session_name]
        return r
        
    @view_config(route_name='sp2d-add', renderer='templates/sp2d/add.pt',
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
                    return HTTPFound(location=req.route_url('sp2d-add'))
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

    @view_config(route_name='sp2d-edit', renderer='templates/sp2d/edit.pt',
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
                    return HTTPFound(location=request.route_url('sp2d-edit',
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
    @view_config(route_name='sp2d-delete', renderer='templates/sp2d/delete.pt',
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
        
    @view_config(route_name='sp2d-csv', renderer='csv',
                 permission='read')
    def export_csv(self):
        request = self.request
        
        query = SipkdDBSession.query(Sp2d.sp2dno, Sp2d.sp2ddate, Sp2d.paymentfor, Sp2d.sp2damount, 
                                     Sp2d.ppnamount, Sp2d.pphamount, 
                                     (Sp2d.pot1num+Sp2d.pot2num+Sp2d.pot3num+Sp2d.pot4num+Sp2d.pot5num).label("potongan"),  
                                     Sp2d.sp2dnetto, Sp2d.bknama, Sp2d.bankposnm, Sp2d.bankaccount).\
                               filter(Sp2d.sp2dno.in_(request.params['data'].split(',')))
                                          
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
