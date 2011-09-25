#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
from funcoes import EscreverNoArquivo
import config, IPlugin
import os, sys, config, time

class LogPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Descricao = 'Gravar mensagens enviadas/recebidas'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.2'
        self.Bot = Bot

    def ajuda(self, nick):
        pass

    def ArquivoLog(self):
        diretorio = self.diretorio() + 'log/'
        rede = self.servidor()
        rede = rede[rede.find('.')+1:rede.rfind('.')]
        return diretorio + rede + '.txt'
        
    def CriarLog(self):
        # /logs/rede.txt
        diretorio = self.diretorio() + 'log/'
        if not os.path.exists(diretorio):
            self.Bot.Mostrar('# Criando diretório: %s' % diretorio)
            os.mkdir(diretorio)
        LogFile = self.ArquivoLog()
        EscreverNoArquivo(LogFile, '#@@ %s\n' % time.ctime())
        self.Bot.Mostrar('# Log de conversa: %s' % LogFile)
            
    def carregar(self):
        self.CriarLog()
        
    def comandos(self):
        return {Comandos.ALL_MSG: self.Entrada, Comandos.OUT_MSG: self.Saida}

    def Entrada(self, mensagem):
        try:
            LogFile = self.ArquivoLog()
            EscreverNoArquivo(LogFile, '%s <- %s\n' % (time.ctime(), mensagem['puro']))
        except: self.Bot.GravarErro(False)
            
    def Saida(self, mensagem):
        try:
            LogFile = self.ArquivoLog()
            EscreverNoArquivo(LogFile, '%s -> %s\n' % (time.ctime(), mensagem))
        except: self.Bot.GravarErro(False)      

