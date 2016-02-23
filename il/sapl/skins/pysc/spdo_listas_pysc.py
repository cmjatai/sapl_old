## Script (Python) "spdo_unidades_tramitacao_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=end
##title=
##

from Products.CMFCore.utils import getToolByName

st = getToolByName(context, 'portal_sapl')

end_spdo = context.sapl_documentos.props_sapl.end_spdo
end_lista = end_spdo + '/' + end

return st.get_listas_spdo(end_lista)
