## Script (Python) "dispositivo_tipos_in_session_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##  

request = container.REQUEST
RESPONSE =  request.RESPONSE

session = request.SESSION 
 
td = None #session.get('tiposDisp')

if td != None: 
    return td

result = {}

listaTipos = context.zsql.dispositivo_tipos_obter_zsql()


dict = listaTipos.dictionaries() 
 
for item in dict:
    
    ir = {}
    for key in item: 
        ir[key] = item[key]
        
    result['id_'+str(item['tip_dispositivo'])] = ir




session.set('tiposDisp', result)    

return result
#print repr(result).replace("'", '"').replace('u"', '"').replace('\\', ' ')
#return printed