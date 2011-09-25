#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, config, funcoes

class Plugin(object):
    '''
    Classe base para a criação de plugins.
    Se uma classe não for herdada desta, não será reconhecida como plugin
    e não será inicializada pelo gerenciador de extensões.
    
    Veja exemplos de plugins em  /modulos/exemplos/
    '''
    def diretorio(self):
        ''' Caminho do diretório do bot '''
        return config.diretorio
    
    def nick(self):
        ''' Nick atual do bot '''
        return config.mynick
        
    def nick_secundario(self):
        ''' Nick secundário definido '''
        return config.second_nick
        
    def servidor(self):
        ''' Em qual servidor o bot tá conectado '''
        return config.network
        
    def porta(self):
        ''' Em qual a porta do servidor está conectado '''
        return config.porta
        
    def dentro_canal(self, canal):
        ''' Retorna se está dentro do canal '''
        return config.usuarios.has_key(canal)
        
    def usuarios(self, canal=''):
        if (canal == ''):
            return config.usuarios
        elif self.dentro_canal(canal):
            return config.usuarios[canal]
        return ''
        
    '''
    O sistema para adminsitrar o bot:
    
    Não é salva lista de nicks de administradores. Apenas no arquivo de histórico
    terá uma informação sobre quem logou.
    Para logar, o administrador precisa digitar apenas a senha pro bot.
    As senhas ficam no arquivo config, com o nome "senhas_admin".
    '''
    def admins(self):
        ''' Pegar a lista de administradores logados '''
        return config.admins

    def add_admin(self, nick):
        ''' Adicionar administrador à lista '''
        config.admins.append(nick.lower())

    def rem_admin(self, nick):
        ''' Remover administrador da lista '''
        config.admins.remove(nick.lower())
    
    def isAdmin(self, nick):
        ''' Ver se um nick está na lista de administradores logados '''
        return nick.lower() in self.admins()
    
    def add_admin_cmd(self, comando):
        ''' Adicionar um comando à lista de comandos para administradores '''
        if hasattr(config, 'admin_cmds'):
            config.admin_cmds += [comando]
        else:
            config.admin_cmds = [comando]

    def TirarTags(self, mensagem):
        ''' Remover tags de cores, negrito, itálico e CTCP da mensagem '''
        mensagem['params'] = [funcoes.LimpaString(m) for m in mensagem['params']]
        return mensagem
                
    def analisar(self, mensagem, tirar_cores=True):
        '''
        Aqui é feita a análise da mensagem. Ela foi feita apenas para PRIVMSG
        retornando uma lista:
            {'resposta': 'nickcanal', 'cmd': 'comando', 'param': 'argumentos', 'valor': 'dados'}
        Se o valor mensagem['params'][0] for o nick do bot, a função pega mensagem['prefix']['nick']
        
        Exemplo:
           mensagem['params'] == ['#canal', 'Procurar -T Site do jimmy -a']
           O retorno será:
                {'resposta': '#canal', 'cmd': 'procurar', 'param': 'Ta', 'valor': 'Site do jimmy'}
        '''
        if tirar_cores: mensagem = self.TirarTags(mensagem)
        resposta = mensagem['params'][0]
        if resposta.lower() == self.nick().lower():
            resposta = mensagem['prefix']['nick']

        if len(mensagem['params']) == 1:
            return {'resposta': resposta, 'cmd': '', 'param': '', 'valor': ''}
            
        tudo = mensagem['params'][1].split()
        if len(tudo) == 0:
            return {'resposta': resposta, 'cmd': '', 'param': '', 'valor': ''}
        
        cmd  = tudo[0].lower()
        
        tudo = tudo[1:]
        parametros = ''
        valores = []
        for item in tudo:
            if (len(item) > 0) and (item[0] == '-'):
                parametros += item[1:]
            else: valores += [item]
        valor = ' '.join(valores)
        
        return {'resposta': resposta, 'cmd': cmd, 'param': parametros, 'valor': valor}
