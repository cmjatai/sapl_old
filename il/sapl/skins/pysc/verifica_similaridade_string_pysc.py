## Script (Python) "verifica_similaridade_string_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=str1, str2
##title=
##
##
w1=str1
w2=str2
def replaceCaracteres(texto):

    autOld ="ãâáàäeêéèëiîíìïõôóòöuûúùüçÃÂÁÀÄEÊÉÈËIÎÍÌÏÕÔÓÒÖUÛÚÙÜÇ".decode("utf-8")
    autNew ="aaaaaeeeeeiiiiiooooouuuuucaaaaaeeeeeiiiiiooooouuuuuc"
    
    for o, n in zip(autOld, autNew):
        texto = texto.replace(o, n)
    
    return texto




 
def stopWords(texto):

   stops = ( '"',"'",'?','`',',','.',  '§' ) 
   
   for st in stops:
      texto = texto.replace(st, '')
   
   texto = texto.strip()
      
   stops = ('(', ')',' o ', ' e ', ' a ', 's ', 'S ', ' do ', 
            ' da ', ' - ', '-', '.º',  'º', '/' , '\r\n' , '\t'  ,
            '\r'  , '\n', '      ', '     ', '    ', '   ', '  ' )
   
   for st in stops:
      texto = texto.replace(st, ' ')
      
   return texto  




#w1 = (w1.strip()).join(' ')
#w2 = (w2.strip()).join(' ')

w1 = stopWords(w1)
w2 = stopWords(w2)
 

 
w1 = replaceCaracteres(w1)
w2 = replaceCaracteres(w2)
 


w1 = w1 + ' '*(len(w2)-len(w1))
w2 = w2 + ' '*(len(w1)-len(w2))

count = 0

#return '<hr>' + str(zip(autOld, autNew)) + '<br><br>' + str(zip(w1,w2))+ '<hr>'


#return w1 + '<br><br>' + w2

for i,j in zip(w1,w2):
   if i==j:
      count = count + 1 
         

return int((count / float(len(w1)))*100)
