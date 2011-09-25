#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comandos import Comandos
import config, IPlugin

class ExemploAdminPlugin(IPlugin.Plugin):
    '''
    Plugin Exemplo para comandos de administradores.
    Este plugin altera o valor dos delays do bot.
    '''
    def __init__(self, Bot=None):
        self.Descricao = 'Set Buffer Delay'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.0'
        self.Bot = Bot
        
    def ajuda(self, nick):
        lista = ['Sintaxe: delay [opcao] <segundos>',
                 'Opcoes:',
                 '-i    Informações sobre cada Delay.',
                 '-v    Mostra valores atuais',
                 '-s<N> Definir delay. N é 1 ou 2. Exemplo: delay -s1 0.1']
        [self.Bot.Say(nick, item) for item in lista]
        
    def informacoes(self, nick):
        msgs = [
        'Delays é tempo de espera usado no controle de fluxo de mensagens '
            'enviadas pelo bot. Há dois valores de delay. '
            'O cálculo de tempo de espera se baseia em dois valores, no número '
            'de itens na lista de espera, e no número de bytes.',
        'Entre cada mensagem enviada, há um tempo de espera, para a próxima. '
        'O tempo mínimo de espera é o valor do Delay 1. '
        'O valor de Delay 2 é usado para calcular o tempo necessário '
        'quando a lista tiver mais de duas mensagens esperando.',
        'Ainda assim, há um limite de bytes que podem ser enviados '
        'que se for ultrapassado, o Delay 2 é duplicado temporariamente.']
        [self.Bot.Say(nick, item) for item in msgs]
                
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}
       
    def carregar(self):
        ''' Adiciona à lista de comandos para administradores '''
        self.add_admin_cmd('delay')
        
    def PrivMsg(self, mensagem):
        analise = self.analisar(mensagem)
        valor = analise['valor']
        param = analise['param']
        alvo = analise['resposta']
        ''' Se o comando não for "delay" ou mensagem for no canal, sai '''
        if not (analise['cmd'] == 'delay') or (alvo[0] == '#'):
            return
        ''' Verifica se o usuario está como adminstrador '''
        if not self.isAdmin(mensagem['prefix']['nick']):
            return
        ''' Parâmetro -v '''
        if ('v' in param):
            self.Bot.Say(alvo, 'delay1: %f ; delay2 %f' % (config.delay1, config.delay2))
            return  
        if ('i' in param):
            self.informacoes(alvo)
            return
        ''' Parâmetro --help '''
        if (valor == '') or ('help' in param):
            self.ajuda(alvo)
            return
        ''' Parâmetro -s '''
        if ('s' in param):
            if not ('1' in param) and not ('2' in param):
                self.Bot.Say(alvo, 'Defina qual delay você quer alterar (1 ou 2). "delay --help" para ajuda')
                return
            ''' Pegar valor '''
            try:
                fvalor = float(valor)
            except:
                self.Bot.Say(alvo, 'Erro ao converter "%s" para float. (Use ponto)' % valor)
                return
            ''' Ajustar '''
            if ('1' in param):
                config.delay1 = fvalor
                self.Bot.Say(alvo, 'Delay 1 ajustado para esta sessão.')
            else:
                config.delay2 = fvalor
                self.Bot.Say(alvo, 'Delay 2 ajustado para esta sessão.')
