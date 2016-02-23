## Script (Python) "protocolo_proximo_obter_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=opcao
##title=
##

#Script para a verificação do número de protocolo e inclusão de um novo
# Faz a inclusão de sequencial por ano ou sequencial único do nr de protocolo
#-----------------------------correção num_protocolo em 2014 -------------------------
total2014=0
total2014=context.zsql.protocolo_2014total_obter_zsql(ano=2014)[0].total
if int(total2014) > 0:
   context.zsql.protocolo_2014update_zsql()

# Obtém o proximo "num_protocolo" por ano ou sequencial único ----- 10/11/2014
#
# opção=1 - numeração por ano, =2 - numeração única

# Busca o último número
num_protocolo = 0
op = int(opcao)
if op == 1:
    ano_corrente= DateTime().year()
else:
    ano_corrente=""
try:
    num_protocolo=context.zsql.protocolo_ultimo_obter_zsql(ano=ano_corrente)[0].num_protocolo
except:
    pass

# retorna próximo número de protocolo

return num_protocolo + 1

