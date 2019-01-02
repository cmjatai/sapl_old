## Script (Python)
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_materia
##title=
##

request = container.REQUEST
response = request.RESPONSE


if str(request['AUTHENTICATED_USER']) != 'leandro':
    raise  Exception("Acesso não Autorizado")

codigo=int(cod_materia)
try:
    context.zsql.materia_check_zsql(cod_materia=codigo)
except Exception as e:
    return str(e)
return "ok"
