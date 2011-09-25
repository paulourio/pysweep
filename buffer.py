#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
import time, socket, config

class BufferControl(Thread):
    '''
    Classe para o controle de fluxo de mensagens de saída do bot.
    O controle é feito para que ele não seja expulso da rede por flood.
    '''
    def __init__ (self, Bot):
        Thread.__init__(self)
        self.buffer = []
        self.Manter = True
        self.Bot    = Bot

    def AddMsg(self, msg):
        ''' Adiciona a mensagem na lista de espera '''
        self.buffer.append(msg)
        
    def stop(self):
        ''' Pára o buffer, e finaliza a classe '''
        self.Manter = False
        
    def clear(self):
        ''' Limpar a lista de espera '''
        self.buffer = []
        
    def enviar(self, msg):
        ''' Envia a mensagem. '''
        if not self.Bot.Ativo(): return
        self.Bot.Irc.raw(msg)
 
    def run(self):
        '''
        Função responsável para evitar o flood.
        Limite: 20 mensagens com 200 bytes em 10 segundos
        '''
        bytes_permitidos = 410 # Número de bytes permitidos
        # Marcadores de mensagens e bytes enviados
        mensagens_enviadas = 0 
        bytes_enviados = 0
        while self.Manter:
            # O Bot nunca caiu por flood no MSN
            if self.Bot.SessaoMSN():
                time.sleep(0.1)
            else:
                time.sleep(1)
            # A cada loop tira 50 da contagem de bytes
            if bytes_enviados > 20:
                bytes_enviados -= 20
            else:
                bytes_enviados = 0
            # A cada loop tira 1 da contagem de mensagens enviadas
            if mensagens_enviadas > 0:
                mensagens_enviadas -= 1
            if len(self.buffer) == 0:
                continue
            # Enquanto forem enviados menos bytes que o permitido,
            # e a contagem de mensagens enviadas for menor que 20
            # e houverem mensagens na lista de espera
            while (bytes_enviados < bytes_permitidos) and (len(self.buffer) > 0) and (mensagens_enviadas < 20):
                bytes_enviados += len(self.buffer[0])
                mensagens_enviadas += 1
                self.enviar(self.buffer[0])
                self.buffer = self.buffer[1:]
