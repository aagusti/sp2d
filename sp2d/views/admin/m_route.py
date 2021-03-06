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
    DBSession,
    
    )
from ...models import Route

from datatables import ColumnDT, DataTables
from ...views.base_view import BaseViews
    

SESS_ADD_FAILED = 'Tambah routes gagal'
SESS_EDIT_FAILED = 'Edit routes gagal'

def deferred_source_type(node, kw):
    values = kw.get('perm_choice', [])
    return widget.SelectWidget(values=values)
    
PERM_CHOICE = ((None,'None'),
      ('view', 'View'),
      ('read', 'Read'),
      ('add', 'Add'),
      ('edit', 'Edit'),
      ('delete', 'Delete'),)
                
class AddSchema(colander.Schema):
    kode = colander.SchemaNode(
                    colander.String())
                    
    nama = colander.SchemaNode(
                    colander.String())
                    
    path = colander.SchemaNode(
                    colander.String())
                    
    factory = colander.SchemaNode(
                    colander.String(),
                    missing=colander.drop)
                    
    perm_name = colander.SchemaNode(
                    colander.String(),
                    missing=colander.drop,
                    widget=widget.SelectWidget(values=PERM_CHOICE))
    disabled = colander.SchemaNode(
                    colander.Boolean())

class EditSchema(AddSchema):
    id = colander.SchemaNode(colander.String(),
            missing=colander.drop,
            widget=widget.HiddenWidget(readonly=True))
            
class view_routes(BaseViews):
    ########                    
    # List #
    ########    
    @view_config(route_name='routes', renderer='templates/routes/list.pt',
                 permission='read')
    def view_list(self):
        return dict(a={})
        
    ##########                    
    # Action #
    ##########    
    @view_config(route_name='routes-act', renderer='json',
                 permission='read')
    def gaji_routes_act(self):
        ses = self.request.session
        req = self.request
        params = req.params
        url_dict = req.matchdict
        
        if url_dict['act']=='grid':
            columns = []
            columns.append(ColumnDT('id'))
            columns.append(ColumnDT('kode'))
            columns.append(ColumnDT('nama'))
            columns.append(ColumnDT('path'))
            columns.append(ColumnDT('factory'))
            columns.append(ColumnDT('perm_name'))
            columns.append(ColumnDT('disabled'))
            
            query = DBSession.query(Route)
            rowTable = DataTables(req, Route, query, columns)
            return rowTable.output_result()
            
        elif url_dict['act']=='headof':
            term = 'term' in params and params['term'] or '' 
            rows = DBSession.query(Route.id, Route.nama
                      ).filter(
                      Route.nama.ilike('%%%s%%' % term),
                      Route.perm_name != None).\
                      order_by(Route.path).all()
            r = []
            for k in rows:
                d={}
                d['id']          = k[0]
                d['value']       = k[1]
                r.append(d)
            return r                  

                
            

    #######    
    # Add #
    #######
    def form_validator(self, form, value):
        if 'id' in form.request.matchdict:
            uid = form.request.matchdict['id']
            q = DBSession.query(Route).filter_by(id=uid)
            routes = q.first()
        else:
            routes = None
                
    def get_form(self, class_form, row=None):
        schema = class_form(validator=self.form_validator)
        schema = schema.bind(perm_choice=PERM_CHOICE)
        schema.request = self.request
        if row:
          schema.deserialize(row)
        return Form(schema, buttons=('simpan','batal'))
        
    def save(self, values, user, row=None):
        if not row:
            row = Route()
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
        self.request.session.flash('routes sudah disimpan.')
            
    def routes_list(self):
        return HTTPFound(location=self.request.route_url('routes'))
        
    def session_failed(self, session_name):
        r = dict(form=self.session[session_name])
        del self.session[session_name]
        return r
        
    @view_config(route_name='routes-add', renderer='templates/routes/add.pt',
                 permission='add')
    def view_routes_add(self):
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
                    return HTTPFound(location=req.route_url('routes-add'))
                self.save_request(dict(controls))
            return self.routes_list()
        elif SESS_ADD_FAILED in req.session:
            return self.session_failed(SESS_ADD_FAILED)
        return dict(form=form.render())

        
    ########
    # Edit #
    ########
    def query_id(self):
        return DBSession.query(Route).filter_by(id=self.request.matchdict['id'])
        
    def id_not_found(self):    
        msg = 'routes ID %s Tidak Ditemukan.' % self.request.matchdict['id']
        request.session.flash(msg, 'error')
        return routes_list()

    @view_config(route_name='routes-edit', renderer='templates/routes/edit.pt',
                 permission='edit')
    def view_routes_edit(self):
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
                    return HTTPFound(location=request.route_url('routes-edit',
                                      id=row.id))
                self.save_request(dict(controls), row)
            return self.routes_list()
        elif SESS_EDIT_FAILED in request.session:
            return self.session_failed(SESS_EDIT_FAILED)
        values = row.to_dict()
        return dict(form=form.render(appstruct=values))

    ##########
    # Delete #
    ##########    
    @view_config(route_name='routes-delete', renderer='templates/routes/delete.pt',
                 permission='delete')
    def view_routes_delete(self):
        request = self.request
        q = self.query_id()
        row = q.first()
        
        if not row:
            return self.id_not_found(request)
        form = Form(colander.Schema(), buttons=('hapus','batal'))
        if request.POST:
            if 'hapus' in request.POST:
                msg = 'routes ID %d %s sudah dihapus.' % (row.id, row.nama)
                try:
                  q.delete()
                  DBSession.flush()
                except:
                  msg = 'routes ID %d %s tidak dapat dihapus.' % (row.id, row.nama)
                request.session.flash(msg)
            return self.routes_list()
        return dict(row=row,
                     form=form.render())

    ##########                    
    # CSV #
    ##########    
        
    @view_config(route_name='routes-csv', renderer='csv',
                 permission='read')
    def export_csv(self):
        request = self.request
        
        query = DBSession.query(Route.kode, Route.nama, Route.path)
                                          
        r = query.first()
        header = r.keys()
        query = query.all()
        rows = []
        for item in query:
            rows.append(list(item))

        # override attributes of response
        filename = 'route%s.csv' % datetime.now().strftime('%Y%m%d%H%M%S')

        self.request.response.content_disposition = 'attachment;filename=' + filename

        return {
          'header': header,
          'rows': rows,
        }
