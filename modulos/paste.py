# -*- coding: utf-8 -*-
from comandos import Comandos
import config, IPlugin, random

pastebin_sites = ['phpfi.com',
                  'pastebin.ca',
                  'pastebin.com',
                  'rafb.net/paste',
                  'nopaste.com']
                  
lst = -1

class PasteBinPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.paste']
        self.Palavra   = 'paste'
        self.Bot       = Bot
   
    def ajuda(self, nick):
        self.Bot.Say(nick, 'Sintaxe: .paste [-a (Mostrar todos os sites cadastrados)]')
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}
       
    def carregar(self):
        pass
        
    def msg_rand(self, lista_base):
        global lst
        x = lst
        while (x == lst):
            x = random.randint(1, len(lista_base)-1)
        lst = x
        return lista_base[x]
    
    def PrivMsg(self, mensagem):
        global pastebin_sites
        analise = self.analisar(mensagem)
        alvo = analise['resposta']
        if not (analise['cmd'] in self.user_cmds):
            return
        if ('help' in analise['param']):
            self.ajuda(alvo)
        elif ('a' in analise['param']):
            self.Bot.Say(alvo, 'http://' + ' http://'.join(pastebin_sites))
        else:
            self.Bot.Say(alvo, 'Paste your fucking code into http://' + self.msg_rand(pastebin_sites))
