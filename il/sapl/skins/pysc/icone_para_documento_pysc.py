## Script (Python) "busca_materias_normas_pysc"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=object_file
##title=
##

request = container.REQUEST
response = request.RESPONSE
session = request.SESSION

ct = object_file.content_type

if ct and ct == 'application/msword':
    return 'Em formato texto ', '<i class="fa fa-file-word-o fa-4x"></i>'
elif ct and ct == 'application/pdf':
    return 'Arquivo digitalizado em formato pdf', '<i class="fa fa-file-pdf-o fa-4x"></i>'
elif ct and ct == 'image/jpeg':
    return 'Arquivo em Formato Imagem.', '<i class="fa fa-file-image-o fa-4x"></i>'
else:
    return 'Arquivo do documento.', '<i class="fa fa-file fa-4x"></i>'


return ''
