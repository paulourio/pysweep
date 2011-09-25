#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comandos import Comandos
import config, IPlugin, web, urllib, simplejson

class GoogleSearchPlugin(IPlugin.Plugin):
    '''
    Plugin Exemplo, usando Internet para buscas.
    Uso da API do Google. Baseado no post do Vndmtrx:
    http://tocadoelfo.blogspot.com/2008/08/usando-api-de-busca-do-google-no-python.html
    '''
    def __init__(self, Bot=None):
        self.user_cmds = ['.google']
        self.Palavra   = 'google'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.0'
        self.Bot = Bot

    def ajuda(self, nick):
        self.Bot.Say(nick, 'Sintaxe: .google palavras-chave') 
            
    def carregar(self):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}
    
    def __ajax_search(self, busca):
        '''
        Monta o pedido da busca, e envia o pedido.
        '''
        query = urllib.urlencode({'q' : busca})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
        procura = web.get(url)
        json = simplejson.loads(procura)
        results = json['responseData']['results']
        return results
                
    def GoogleSearch(self, nick, busca):
        resultados = self.__ajax_search(busca)
        if resultados == []:
            self.Bot.Say(nick, 'Nada para ' + busca)
            return
        ''' Monta a resposta no formato "Titulo: link.com" '''
        resposta = []
        for i in resultados:
            i['title'] = i['title'].replace('<b>', '\x02').replace('</b>', '\x02')
            resposta += [i['title'] + ': ' + i['url']]
        self.Bot.Say(nick, ' | '.join(resposta))
       
    def PrivMsg(self, mensagem):
        analise = self.analisar(mensagem)
        palavra = analise['valor']
        alvo = analise['resposta']
        # Verifica se o comando é .google
        if not (analise['cmd'] in self.user_cmds):
            return
        # Verifica se tem algum texto além do ".google"
        if (palavra == '') and (param == ''):
            self.Bot.Say(alvo, 'Defina palavra-chave. Para ajuda: .google --help')
            return
        # Mostra ajuda
        if ('help' in analise['param']):
            self.ajuda(alvo)
            return
        # Faz a procura
        self.GoogleSearch(alvo, palavra) 
