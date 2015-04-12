from five import grok
from plone import api
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from plone.app.contenttypes.interfaces import IDocument, INewsItem, IEvent
#from plone.app.multilingual.interfaces import ILanguage


grok.templatedir('views_template')


class MyPage(grok.View):
    grok.context(Interface)
    grok.name('mypage')

    def render(self):
        context = self.context
        catalog = context.portal_catalog
        response = self.response
        currentUser = api.user.get_current()
        if (not api.user.is_anonymous()) and ('Member' in api.user.get_roles()):
            profile = catalog({'Type':'Profile', 'id':currentUser.getId()})[0]
            response.redirect(profile.getURL())
        else:
            response.redirect(context.absolute_url())
        return
