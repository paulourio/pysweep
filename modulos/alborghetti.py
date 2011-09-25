#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin, os, time, random
from threading import Thread

class AlborghettiSpam(Thread):
    def __init__ (self, bot):
        Thread.__init__(self)
        self.anuncio = ['tá passando o programa cadeia sem censura (Alborghetti).. www.fusaotv.com',
                    'começou o programa do Alborghetti www.fusaotv.com',
                    'o alborga vai começa a fala agora! :) www.fusaotv.com' ]
        self.canais = ['#buteco_irc', '#delphix', '##null']
        self.Bot    = bot

    def msg_rand(self, lista_base):
        return lista_base[random.randint(1, len(lista_base)-1)]  
        
    def run(self):
        ''' Da um tempo pra entrar nos canais '''
        time.sleep(20)
        while not hasattr(config, 'usuarios'):
            time.sleep(2)
        while True:
            ''' So anuncia em dias uteis '''
            if not (time.strftime('%A') in ['Sunday', 'Saturday']):
                ''' Espera até as 17 hrs '''
                while (time.strftime('%A') != '17'):
                    time.sleep(60)
                for canal in self.canais:
                    if config.usuarios.__contains__(canal):
                        self.Bot.Say(canal, self.msg_rand(self.anuncio))
            time.sleep(82800) # 23 horas

class AlborghettiPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Bot = Bot
        
    def ajuda(self, nick):
        pass
                
    def carregar(self):
        pass

    def comandos(self):
        return {Comandos.RPL_ENDOFMOTD: self.IniciarThread}
        
    def IniciarThread(self, mensagem):
        ''' Inicia a thread ''' 
        config.AlborghettiSpam = AlborghettiSpam(self.Bot)
        config.AlborghettiSpam.start()
