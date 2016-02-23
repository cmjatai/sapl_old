## Script (Python) "data_converter_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=data
##title=
##



meses=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

if data != '':
    sData = data.split("/")
    if len(sData) == 0:
       sData = data.split("-")            
    if len(sData) == 0:
        return ''
    
    if int(sData[0]) <= 31:
        sData.reverse()
    
    mes = int(sData[1])
    return meses[int(mes-1)] + " de " + sData[0]
else:
   return ''
