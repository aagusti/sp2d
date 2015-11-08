from pyramid.view import (
    view_config,
    )
from pyramid.httpexceptions import (
    HTTPFound,
    )
from ...models import App
########
# APP Home #
########
#@view_config(route_name='sp2d', renderer='templates/home.pt', permission='view')
#def view_app(request):
#    return dict(project='SP2D')
        