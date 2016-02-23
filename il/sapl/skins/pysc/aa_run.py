## Script (Python) "ajustar_materias_normas_pysc"

request = container.REQUEST
response =  request.response

parl_sem_autor = context.zsql.parlamentar_nao_autor_obter_zsql()

for p in parl_sem_autor:
     context.zsql.autor_incluir_zsql(
        tip_autor=1,
        cod_parlamentar=p.cod_parlamentar,
        nom_autor=p.nom_completo,
        des_cargo='Vereador')
     print p.nom_completo
return printed
