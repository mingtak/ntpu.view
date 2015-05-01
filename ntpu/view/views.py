from five import grok
from plone import api
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from plone.app.contenttypes.interfaces import IDocument, INewsItem, IEvent
#from plone.app.multilingual.interfaces import ILanguage

from zope.component import getMultiAdapter


grok.templatedir('views_template')


class ToLanguageHome(grok.View):
    grok.context(Interface)
    grok.name('to_language_home')

    def render(self):
        context = self.context.aq_inner
        response = self.response
        portal = api.portal.get()
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        current_language = portal_state.language()
        url = '%s/system/index_%s' % (portal.absolute_url(), current_language)
        response.redirect(url)
        return


class GetCurrentUseId(grok.View):
    grok.context(Interface)
    grok.name('getCurrentUserId')

    def render(self):
        if api.user.is_anonymous():
            return None
        return api.user.get_current().getId()


class IsAnonymous(grok.View):
    grok.context(Interface)
    grok.name('isAnonymous')

    def render(self):
        return api.user.is_anonymous()


class MyPage(grok.View):
    grok.context(Interface)
    grok.name('mypage')

    def render(self):
        context = self.context
        catalog = context.portal_catalog
        response = self.response
        currentUser = api.user.get_current()
        if (not api.user.is_anonymous()) and ('Member' in api.user.get_roles()):
            profile = catalog({'Type':'Profile', 'Creator':currentUser.getId()})[0]
            response.redirect(profile.getURL())
        else:
            response.redirect(context.absolute_url())
        return


class CurrentLanguage(grok.View):
    """
    Get current language code
    """

    grok.context(Interface)
    grok.name('currentLanguage')

    def render(self):
        context = self.context.aq_inner
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.current_language = portal_state.language()

        return self.current_language


class GetContentType(grok.View):
    grok.context(Interface)
    grok.name('get_contenttype')

    def render(self):
        return self.context.Type()


class IsOwner(grok.View):
    grok.context(Interface)
    grok.name('is_owner')

    def render(self):
        ownerId = self.context.owner_info()['id']
        currentUserId = api.user.get_current().getId()
        return ownerId == currentUserId


class GetRoles(grok.View):
    grok.context(Interface)
    grok.name('get_roles')

    def render(self):
        return api.user.get_roles()
