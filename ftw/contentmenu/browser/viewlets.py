from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class ContentViewsViewlet(common.ContentViewsViewlet):
    index = ViewPageTemplateFile('contentviews.pt')
