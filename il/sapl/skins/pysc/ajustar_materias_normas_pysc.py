## Script (Python) "ajustar_materias_normas_pysc"
 
request = container.REQUEST
response =  request.response 

if 1 == 0:
    objetos = context.sapl.sapl_documentos.materia.objectValues()   
    
    for o in objetos:
        obj_id = str(o.id)   
        if 'Catalog' in obj_id:
            continue   
         
        o.manage_changeProperties(content_type='application/pdf')
        o.manage_permission("View", [], 1)
        print o.id
        print o.content_type 
        
if 1 == 1:
    

    objetos = context.sapl.sapl_documentos.parecer_procuradoria.objectValues()   

    for o in objetos:
        obj_id = str(o.id)   
        if 'Catalog' in obj_id:
            continue   
           
        o.manage_changeProperties(content_type='application/msword')
        o.manage_permission("View", [], 1)
        print o.content_type

        
if 1 == 0:
    

    objetos = context.sapl.sapl_documentos.administrativo.objectValues()   

    for o in objetos:
        obj_id = str(o.id)   
        if 'Catalog' in obj_id:
            continue   
           
        o.manage_changeProperties(content_type='application/pdf')
        o.manage_permission("View", [], 1)
        print o.content_type




if 1 == 0:
    objetos = context.sapl.sapl_documentos.norma_juridica.objectValues()   
     
    for o in objetos:
        obj_id = str(o.id)   
        if 'Catalog' in obj_id:
            continue   
        
        codigo = obj_id.split('_')[0]
        
        if 'texto_html' in obj_id:
           print codigo+ ' - ' + o.content_type()
        else:
           print codigo+ ' - ' + str(o.content_type)
            
                
        
        normas = context.zsql.norma_juridica_obter_zsql(cod_norma = codigo)
        
        if len(normas) == 0:
            continue
        
        if 'texto_html' in obj_id:       
            o.manage_changeProperties(content_type='text/html')
        elif 'texto_integral' in obj_id:
            if normas[0]['sgl_tipo_norma'] == 'ATG':
                o.manage_changeProperties(content_type='application/msword')
            else:
                o.manage_changeProperties(content_type='application/pdf')
                
        print 
        o.manage_permission("View", [], 1)
                
        print  normas[0]['sgl_tipo_norma'] 
            
        
 
return printed



