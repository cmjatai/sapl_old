## Script (Python) "verifica_similaridade_string_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=texto
##title=
##


stops = ('?', '`', ',', 'º')

for st in stops:
    texto = texto.replace(st, '')

stops = ('(', ')', ' o ', ' a ', ' e ',
    's ', 'S ', ' do ', ' da ', ' de ',
    ' - ', '-', '.º',  'º', '/',
    '\r\n', '\t', '\r', '\n', '      ', '     ', '    ', '   ', '  ', '     ', '    ', '   ', '  ')

for st in stops:
    if texto == st.strip():
        return ''
    texto = texto.replace(st, ' ')




return texto
