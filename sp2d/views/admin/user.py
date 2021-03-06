import os
import uuid
from ...tools import row2dict, xls_reader
from datetime import datetime
from email.utils import parseaddr
from sqlalchemy import not_
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
    User,
    )
from datatables import ColumnDT, DataTables


SESS_ADD_FAILED = 'user add failed'
SESS_EDIT_FAILED = 'user edit failed'

########                    
# List #
########    
@view_config(route_name='user', renderer='templates/user/list.pt',
             permission='read')
def view_list(request):
    #rows = DBSession.query(User).filter(User.id > 0).order_by('email')
    return dict(project='e-Gaji')
    
##########                    
# Action #
##########    
@view_config(route_name='user-act', renderer='json',
             permission='read')
def gaji_group_act(request):
    ses = request.session
    req = request
    params = req.params
    url_dict = req.matchdict
    
    if url_dict['act']=='grid':
        columns = []
        columns.append(ColumnDT('id'))
        columns.append(ColumnDT('email'))
        columns.append(ColumnDT('user_name'))
        columns.append(ColumnDT('status'))
        columns.append(ColumnDT('last_login_date'))
        columns.append(ColumnDT('registered_date'))
        
        query = DBSession.query(User)
        rowTable = DataTables(req, User, query, columns)
        return rowTable.output_result()
    elif url_dict['act']=='headofnama':
        term = 'term' in params and params['term'] or '' 
        rows = DBSession.query(User.id, User.user_name
                  ).filter(
                  User.user_name.ilike('%%%s%%' % term) ).all()
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
def email_validator(node, value):
    name, email = parseaddr(value)
    if not email or email.find('@') < 0:
        raise colander.Invalid(node, 'Invalid email format')

def form_validator(form, value):
    def err_email():
        raise colander.Invalid(form,
            'Email %s already used by user ID %d' % (
                value['email'], found.id))

    def err_name():
        raise colander.Invalid(form,
            'User name %s already used by ID %d' % (
                value['user_name'], found.id))
                
    if 'id' in form.request.matchdict:
        uid = form.request.matchdict['id']
        q = DBSession.query(User).filter_by(id=uid)
        user = q.first()
    else:
        user = None
    q = DBSession.query(User).filter_by(email=value['email'])
    found = q.first()
    if user:
        if found and found.id != user.id:
            err_email()
    elif found:
        err_email()
    if 'user_name' in value: # optional
        found = User.get_by_name(value['user_name'])
        if user:
            if found and found.id != user.id:
                err_name()
        elif found:
            err_name()

@colander.deferred
def deferred_status(node, kw):
    values = kw.get('daftar_status', [])
    return widget.SelectWidget(values=values)
    
STATUS = (
    (1, 'Active'),
    (0, 'Inactive'),
    )    

class AddSchema(colander.Schema):
    email = colander.SchemaNode(colander.String(),
                                validator=email_validator)
    user_name = colander.SchemaNode(
                    colander.String(),
                    missing=colander.drop)
    status = colander.SchemaNode(
                    colander.String(),
                    widget=deferred_status)
    password = colander.SchemaNode(
                    colander.String(),
                    widget=widget.PasswordWidget(),
                    missing=colander.drop)


class EditSchema(AddSchema):
    id = colander.SchemaNode(colander.String(),
            missing=colander.drop,
            widget=widget.HiddenWidget(readonly=True))
                    

def get_form(request, class_form):
    schema = class_form(validator=form_validator)
    schema = schema.bind(daftar_status=STATUS)
    schema.request = request
    return Form(schema, buttons=('save','cancel'))
    
def save(values, user, row=None):
    if not row:
        row = User()
    row.from_dict(values)
    if values['password']:
        row.password = values['password']
    DBSession.add(row)
    DBSession.flush()
    return row
    
def save_request(values, request, row=None):
    if 'id' in request.matchdict:
        values['id'] = request.matchdict['id']
    row = save(values, request.user, row)
    request.session.flash('User %s has been saved.' % row.email)
        
def route_list(request):
    return HTTPFound(location=request.route_url('user'))
    
def session_failed(request, session_name):
    r = dict(form=request.session[session_name])
    del request.session[session_name]
    return r
    
@view_config(route_name='user-add', renderer='templates/user/add.pt',
             permission='add')
def view_add(request):
    form = get_form(request, AddSchema)
    if request.POST:
        if 'save' in request.POST:
            controls = request.POST.items()
            try:
                c = form.validate(controls)
            except ValidationFailure, e:
                request.session[SESS_ADD_FAILED] = e.render()               
                return HTTPFound(location=request.route_url('user-add'))
            save_request(dict(controls), request)
        return route_list(request)
    elif SESS_ADD_FAILED in request.session:
        return session_failed(request, SESS_ADD_FAILED)
    return dict(form=form.render())

########
# Edit #
########
def query_id(request):
    return DBSession.query(User).filter_by(id=request.matchdict['id'])
    
def id_not_found(request):    
    msg = 'User ID %s not found.' % request.matchdict['id']
    request.session.flash(msg, 'error')
    return route_list(request)

@view_config(route_name='user-edit', renderer='templates/user/edit.pt',
             permission='edit')
def view_edit(request):
    row = query_id(request).first()
    if not row:
        return id_not_found(request)
    form = get_form(request, EditSchema)
    if request.POST:
        if 'save' in request.POST:
            controls = request.POST.items()
            try:
                c = form.validate(controls)
            except ValidationFailure, e:
                request.session[SESS_EDIT_FAILED] = e.render()               
                return HTTPFound(location=request.route_url('user-edit',
                                  id=row.id))
            save_request(dict(controls), request, row)
        return route_list(request)
    elif SESS_EDIT_FAILED in request.session:
        return session_failed(request, SESS_EDIT_FAILED)
    values = row.to_dict()
    return dict(form=form.render(appstruct=values))

##########
# Delete #
##########    
@view_config(route_name='user-delete', renderer='templates/user/delete.pt',
             permission='delete')
def view_delete(request):
    q = query_id(request)
    row = q.first()
    if not row:
        return id_not_found(request)
    form = Form(colander.Schema(), buttons=('delete','cancel'))
    if request.POST:
        if 'delete' in request.POST:
            msg = 'User ID %d %s has been deleted.' % (row.id, row.email)
            q.delete()
            DBSession.flush()
            request.session.flash(msg)
        return route_list(request)
    return dict(row=row,
                 form=form.render())

##########
#   CSV  #
##########    
@view_config(route_name='user-csv', renderer='csv',
             permission='read')
def export_csv(request):
    req = request
    
    query = DBSession.query(User.user_name,User.email)
                                      
    r = query.first()
    print ">>>>>>>>>>>>>>>>>>>", query
    header = r.keys()

    query = query.all()
    rows = []
    for item in query:
        rows.append(list(item))

    # override attributes of response
    filename = 'user%s.csv' % datetime.now().strftime('%Y%m%d%H%M%S')

    req.response.content_disposition = 'attachment;filename=' + filename

    return {
      'header': header,
      'rows': rows,
    }
