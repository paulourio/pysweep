#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comandos import Comandos
import IPlugin, web, sys

class PegarTituloPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Palavra   = 'UrlTitulo'
        self.Descricao = 'Obtem o titulo do link'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.0'
        self.Bot       = Bot
        #self.sites = ['.com', 'http://', 'www.']
        self.ignore_channels = ['#python-br', '#archlinux.br']
        self.ignore_nicks    = ['delphix', 'hal9500']
        self.ignore_list     = ['image', 'orkut']        
        self.sites = ['youtube.com', 'dailymotion.com', 'redtube.com', 
            'pornkolt.com', 'youporn.com', 'torrent', 'forum', 'porhub.com',
            'docs', 'xrl.us', 'letras', 'lyrics', 'break.com']

    def ajuda(self, nick):
        self.Bot.Say(nick, 'Pegando titulos de %s' % ', '.join(self.sites))
        self.Bot.Say(nick, 'Descricao: ' + self.Descricao)

    def carregar(self):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}
            
    def getLink(self, msg):
        id = ['.com','http://', 'www.']
        for id_s in id:
            if id_s in msg.lower():
                i = msg.lower().find(id_s)
                inicio = msg[:i].rfind(' ')
                if inicio == -1:
                    inicio = 0
                else:
                    inicio += 1
                fim = msg[i:].find(' ')
                if fim == -1:
                    fim = len(msg)
                else:
                    fim += i
                link = msg[inicio:fim]
                if not ('://' in link):
                    # não tentar pegar link de e-mails
                    if ('@' in link):
                        return ''
                    else:
                        link = 'http://' + link
                return link

    def getTitle(self, para, msg):
        try:
            link = self.getLink(msg)
            if (link == ''):
                return
            msg = web.get(link)
            inicio = msg.lower().find('<title>')
            if inicio != -1:
                msg = '%s12%s' % (chr(3), msg[inicio+7:msg.lower().find('</title>')])
                msg = msg.replace('\n', '').replace('\r', '').replace(chr(160), ' ')
                while '&' in msg:
                    if msg.find(';') < msg.find('&'): #pog
                        break
                    msg = msg[:msg.find('&')] + msg[msg.find(';')+1:]
                if msg.strip() != '':
                    self.Bot.Say(para, msg.strip())
        except:
            pass

    def PrivMsg(self, mensagem):
        frase = mensagem['params'][1].lower()

        analise = self.analisar(mensagem)
        cmd = analise['cmd']
        param = analise['param']
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']
                
        for itm in self.ignore_list:
            if itm in frase:
                return

        for itm in self.ignore_nicks:
            if itm in nick.lower():
                return
                
        for itm in self.ignore_channels:
            if itm in alvo.lower():
                return
        
        for id_s in self.sites:
            if id_s in frase:
                self.getTitle(alvo, mensagem['params'][1])
                break
