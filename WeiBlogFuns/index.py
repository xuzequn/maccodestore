# coding:utf-8
import os

import sae
import web

from weibofunsInterface import XeibofunsInterface

urls = {
    '/', 'XeibofunsInterface'
}

app_root = os.path.dirname(__file__)
template_root = os.path.join(app_root, 'templates')
render = web.templates.render(template_root)

app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)