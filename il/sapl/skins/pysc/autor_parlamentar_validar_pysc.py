## Script (Python) "autor_parlamentar_validar_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=txt_dat_apresentacao, cod_parlamentar
##title=
##
"""
  Função: validar se o parlamentar pode ou não ser autor de materia legislativa na data da apresentação indicada

  Argumentos: txt_dat_apresentacao e cod_parlamentar  --> retorna 1-verdadeiro ou 0-falso.

"""
codigo = str(cod_parlamentar)

num_ultima_legislatura = context.zsql.legislatura_ultima_obter_zsql()[0]

legislatura = context.zsql.legislatura_obter_zsql(num_legislatura=num_ultima_legislatura.num_legislatura)[0]

dat_apresentacao = DateTime(context.pysc.iso_to_port_pysc(txt_dat_apresentacao))

if legislatura.dat_inicio <= dat_apresentacao <= legislatura.dat_fim:
    autores = context.zsql.autores_obter_zsql(txt_dat_apresentacao=txt_dat_apresentacao) or []
else:
    autores = context.zsql.autores_obter_zsql(txt_dat_apresentacao=txt_dat_apresentacao, ind_ativo = 0 ) or []

for p in autores:
    s = str(p.cod_parlamentar)
    if s == codigo:
        return 1 # pode ser parlamentar na data da apresentação indicada
return 0
