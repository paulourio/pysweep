#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin, os, time, random
from threading import Thread

frases_ignore = [
        'Eita.. que flood! Quando se acalmarem eu volto.',
        'Porra, que flood desgraçado.. flw ae',
        'Não agüento esses flooders, tchau.',
        'Quando se acalmarem eu volto.']

# Thread para controle e mensagens recebidas
class FloodControl(Thread):
    def __init__ (self, bot):
        Thread.__init__(self)
        self.buffer = []
        self.lista  = {}
        self.Bot    = bot
        self.inaction = False

    def msg_rand(self, lista_base):
        return lista_base[random.randint(1, len(lista_base)-1)]  
        
    def doAction(self, canal):
        self.inaction = True
        self.Bot.ControleFluxo.clear()
        self.Bot.Say(canal, self.msg_rand(frases_ignore))
        #time.sleep(2.0)
        self.Bot.Sair(canal)
        time.sleep(120.0)
        self.Bot.Entrar(canal)
        self.inaction = False
        
    def Add(self, canal):
        self.buffer.append(canal)

    def Incrementar(self):
        for item in self.buffer:
            # Verifica se tem o canal
            if self.lista.has_key(item):
                # Pega o valor atual
                valor = self.lista[item] + 1
                if valor == 3:
                    valor = 1
                    self.doAction(item) # Ignora
                    break
                # Atualiza a lista
                self.lista.update({item: valor})
            else:
                # Cria o canal
                self.lista.update({item: 1})
        # Limpa o buffer
        self.buffer = []
    
    def Decrementar(self):
        if self.lista == {}:
            return
        novo = {}
        for canal in self.lista.keys():
            valor = self.lista[canal] - 1
            if valor > 0:
                novo.update({canal: valor})
        self.lista = novo
        
    def run(self):
        while True:
            if not self.inaction:
                self.Incrementar()
                self.Decrementar()
            time.sleep(5.0)

class AntiFloodPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Bot = Bot
        
    def ajuda(self, nick):
        pass
                
    def carregar(self):
        config.AntiFlood = FloodControl(self.Bot)
        config.AntiFlood.start()

    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}
            
    def PrivMsg(self, mensagem):
        analise = self.analisar(mensagem)
        alvo = analise['resposta']  
        #if (alvo[0] != '#') or not self.Bot.Gerenciador.pegar_lista_comandos().__contains__(analise['cmd']):
        if len(analise['cmd']) == 0: 
            return
        if (alvo[0] != '#') or (analise['cmd'][0] != '.'):
            return
        config.AntiFlood.Add(alvo.lower())
        
        
