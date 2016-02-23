# Script para ajustar os logins dos parlamentares autores com os logins dos parlamentares
# Para executar: bin/instance run login_parlamentar.py
# Gustavo Lepri: 30/03/2015

import transaction
import MySQLdb

# nome da instancia SAPL
SAPL = 'sapl'

# dados de acesso ao banco de dados
DB_HOST = 'localhost'
DB_NAME = 'interlegis'
DB_USER = 'root'
DB_PASS = 'interlegis'

from AccessControl.SecurityManagement import newSecurityManager
sapl = getattr(app, SAPL)
user = sapl.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(sapl.acl_users))


def login():
    print "copiando login"
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS)
    db.select_db(DB_NAME)
    cursor = db.cursor()
    parlamentares = sapl.portal_skins.sk_sapl.zsql.parlamentar_obter_zsql(ind_ativo=1, ind_excluido=0)
    for parlamentar in parlamentares:
        cod_parlamentar = parlamentar.cod_parlamentar
        autor = sapl.portal_skins.sk_sapl.zsql.autor_obter_zsql(cod_parlamentar=cod_parlamentar)
        if autor:
            login = autor[0].col_username
            if login:
                login_update = 'UPDATE parlamentar SET txt_login = "%s" WHERE cod_parlamentar = %s' % (login,
                                                                                                       cod_parlamentar)
                cursor.execute(login_update)
                sapl.portal_skins.sk_sapl.pysc.username_pysc(role='parlamentar', username=login, adicionar=True)
                transaction.commit()


if __name__ == "__main__":
    login()
