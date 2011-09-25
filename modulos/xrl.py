#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comandos import Comandos
import config, IPlugin, metamark

class XrlPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.url']
        self.Palavra   = 'link'
        self.Sintaxe   = '.url <url>'
        self.Descricao = 'Cria um link menor para url mais longas (metamark.net)'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.0'
        self.Bot       = Bot

    def ajuda(self, nick):
        self.Bot.Say(nick, 'Sintaxe: ' + self.Sintaxe)
        self.Bot.Say(nick, 'Descricao: ' + self.Descricao)

    def carregar(self):
        pass
    
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}
       
    def PrivMsg(self, mensagem):
        analise = self.analisar(mensagem)
        alvo = analise['resposta']

        if not (analise['cmd'] in self.user_cmds): return
        if ('help' in analise['param']):
            self.ajuda(alvo)
            return
        if analise['valor'] == '':
            self.Bot.Say(alvo, 'Use \x02.url http://link.com\x02, ou \x02.url --help\x02 para ajuda')
            return
        link = metamark.XrlUS().getUrl(analise['valor'])
        msg = 'A nova url eh \x02%s\x02 (%s do tamanho)' % (link[0], link[1])
        self.Bot.Say(alvo, msg)
