## Script (Python) "dados_spdo_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=tipo=''
##title=
##

from Products.CMFCore.utils import getToolByName

st = getToolByName(context, 'portal_sapl')

if tipo == 'login':
    usuario = context.REQUEST.get('AUTHENTICATED_USER', None)
    return usuario

if tipo == 'senha':
    usuario = context.REQUEST.get('AUTHENTICATED_USER', None)
    if usuario:
        return st.get_user_password(usuario)
