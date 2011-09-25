#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comandos import Comandos
import config, IPlugin, web, time

class ExtensionDetailsPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.ext']
        self.Palavra   = 'ext'
        self.Sintaxe   = '.ext <extensao>'
        self.Descricao = 'Mostra detalhes de uma extensao como descricao, organizacao, caracter de identificacao, etc. (site: filext.com)'
        self.Autor     = 'JimmySkull'
        self.Versao    = '0.8'
        self.Bot = Bot

    def ajuda(self, nick):
        self.Bot.Say(nick, 'Sintaxe: '+ self.Sintaxe)
        self.Bot.Say(nick, 'Descricao: ' + self.Descricao)

    def carregar(self):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}
            
    def ExtInfo(self, busca, para):
        if busca != '':
            busca = busca.strip().replace(' ', '%2B')
            get = web.criar_pedido('filext.com', '/file-extension/' + busca)
            src = web.socket_send('filext.com', dados=get, fim='</html>')
            
            if 'is not in any of the databases' in src:
                self.Bot.Say(para, 'Nada para a extensao "%s"' % busca)
            else:
                Link = 'http://filext.com/file-extension/' + busca
                self.Bot.Say(para, 'Detalhes %s' % Link)
                title = '<strong>Program and/or Extension Function'
                Loc = '<td colspan="2">'
                while title in src:
                    src = src[src.find(title)+len(title):]
                    src = src[src.find(Loc)+len(Loc):]
                    Descricao = src[:src.find('</td>')]
                    while '<' in Descricao:
                        Descricao = Descricao[:Descricao.find('<')] + Descricao[Descricao.find('>')+1:]
                    while '\r\n' in Descricao:
                        Descricao = Descricao[Descricao.find('\r\n')+2:]
                    self.Bot.Say(para, '%s: %s' % (busca, Descricao.strip()))
    
    def PrivMsg(self, mensagem):
        analise = self.analisar(mensagem)
        cmd = analise['cmd']
        param = analise['param'].lower()
                
        if (cmd != '.ext'):
            return
            
        if ('help' in param):
            self.ajuda(analise['resposta'])
        else:
            self.ExtInfo(analise['valor'], analise['resposta'])
