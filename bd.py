#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Dependências:
    sqlite3
    python-pysqlite
'''
from pysqlite2 import dbapi2 as sqlite
import os

'''
Dicionário com os  comandos de criação de tabelas.
Formato: {'NomeTabela': 'comando sql de criação'}
'''
Tabelas = {
'Quote': 'CREATE TABLE Quote (autor VARCHAR(25), id VARCHAR(20), frase VARCHAR(450) , data NUMERIC(10, 6))',
'Rastreamento': 'CREATE TABLE Rastreamento (assinante VARCHAR(40), valor VARCHAR(20), historico VARCHAR(10000), data NUMERIC(10, 6))'
}

class BancoDeDados(object):
    def __init__(self, arquivo, bot=None):
        if bot != None:
            self.fMostrar = bot.Mostrar
        if not os.path.exists(arquivo):
            self.__CriarBancoDeDados(arquivo)
        self.conexao = sqlite.connect(arquivo)
        self.cursor = self.conexao.cursor()

    def fechar(self):        
        self.cursor.close()
        self.conexao.close()

    def executar(self, comando, fetch=0):
        ''' fetch == 0  é fetchall() '''
        try:
            self.cursor.execute(comando)
            if   (fetch == 0): return self.cursor.fetchall()
            elif (fetch == 1): return self.cursor.fetchone()
            else: return self.cursor.fetchmany(fetch)
        except Exception, e: return ['ERRO', e]
        
    def gravar(self):
        self.conexao.commit()
        
    def cancelar(self):
        self.rollback()

    def Mostrar(self, msg):
        self..Bot.Mostrar(msg)
        
    def __CriarBancoDeDados(self, arquivo):
        global Tabelas
        con = sqlite.connect(arquivo)
        cur = con.cursor()
        self.Mostrar('# Criando banco de dados: %s' % arquivo)
        for tabela in Tabelas:
            texto = '# Criando tabela %s... ' % tabela
            try:
                cur.execute(Tabelas[tabela])
                texto += 'OK'                
            except Exception, e:
                texto += 'ERRO -> ' + str(e)
            self.Mostrar(texto)
        con.commit()
        cur.close()
        con.close()
