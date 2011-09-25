#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comandos import Comandos
from threading import Thread
import config, IPlugin, time

lst_assinantes = []

lst_ignore = []

class SpyBufferControl(Thread):
    def __init__ (self, Bot):
        Thread.__init__(self)
        self.buffer = []
        self.Bot    = Bot

    def AddMsg(self, msg):
        self.buffer.append(msg)
        
    def clear(self):
        self.buffer = []
        
    def enviar(self, msg):
        if not self.Bot.Ativo(): return
        self.Bot.Irc.envia(msg)
 
    def run(self):
        while True:
            if len(self.buffer) > 0:
                self.enviar(self.buffer[0])
                self.buffer = self.buffer[1:]                
            time.sleep(1.2)

class SpyPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Descricao = 'Spy'
        self.Autor     = 'JimmySkull'
        self.Versao    = '0.01'
        self.Bot = Bot
        
    def Say(self, para, msg):
        config.buffer_thread.AddMsg('PRIVMSG %s :%s' % (para, msg))
        
    def ajuda(self, nick):
        lista = ['Sintaxe: spy <comando> <parâmetro>',
                 'ajuda    Mostra esse texto de ajuda',
                 'assinar  Fazer a assinatura do spy, e receber as mensagens enviadas/recebidas do bot',
                 'ignore   Ignorar texto. Todo texto que estiver na mensagem será omitido para todos os usuarios',
                 '. uso: spy ignore PRIVPVT',
                 '.          MSGPURAS   Ignora todas as mensagens não tratadas',
                 '.          PRIVMSG    Ignora todas as mensagens de conversa (canal)',
                 '.          PRIVPVT    Ignora todas as mensagens de conversa (pvt)',
                 '.          EVENTOS1   Ignora entradas e saídas de usuários em canais',
                 '.          EVENTOS2   Ignora Quit, Kick, mudança de Nick',
                 '.          BOTSAY     Ignora as mensagens enviadas pelo bot',
                 '.          <TEXTO>    Ignora o valor de <TEXTO> nas mensagens recebidas',
                 '.          -          Nada, mostra a lista de ignores',
                 'clear    Fazer limpeza de uma lista. Ex. spy clear IGNORE',
                 '.          IGNORE     Limpar lista de textos ignorados',
                 '.          BUFFER     Limpar buffer de mensagens',
                 'stop     Remover o teu nick da lista de assinantes' ]
        [self.Say(nick, item) for item in lista]

                
    def comandos(self):
        return {Comandos.ALL_MSG: self.AllMsg,
                Comandos.CMD_PRIVMSG: self.PrivMsg,
                Comandos.CMD_JOIN: self.Join,
                Comandos.CMD_KICK: self.Kick,
                Comandos.CMD_PART: self.Part,
                Comandos.CMD_QUIT: self.Quit,
                Comandos.CMD_NICK: self.Nick,
                Comandos.OUT_MSG: self.Out,
                Comandos.RPL_ENDOFMOTD: self.IniciarBuffer}
       
    def carregar(self):
        self.add_admin_cmd('spy')
        config.buffer_thread = SpyBufferControl(self.Bot)
        
    def IniciarBuffer(self, mensagem):
        config.buffer_thread.start()

    def Despachar(self, msg):
        global lst_assinantes, lst_ignore
        for ign in lst_ignore:
            if ign.lower() in msg.lower():
                return
        for nck in lst_assinantes:
            if not ((nck + chr(32) + self.nick()) in msg.lower()):
                self.Say(nck, msg)

    def __removerNick(self, nick):
        nick = nick.lower()
        if lst_assinantes.__contains__(nick):
            lst_assinantes.remove(nick)
            self.Say(nick, '\x034*\x031 Removido.')
        
    def PrivMsg(self, mensagem):
        global lst_assinantes, lst_ignore
        analise = self.analisar(mensagem)
        cmd = analise['cmd'].lower()
        palavra = analise['valor']
        param = analise['param'].lower()
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']          
        if self.isAdmin(nick) and (cmd == 'spy'):
            if (palavra in ['ajuda','']) or ('help' in param):
                self.ajuda(nick)
                return
                
            comando = palavra.split()[0]
            if (comando == 'assinar'):
                if lst_assinantes.__contains__(nick.lower()):
                    self.Say(nick, '\x034*\x031 Você já está como assinante.')
                    return                
                lst_assinantes.append(nick.lower())
                self.Say(nick, '\x034*\x031 Voce foi adicionado como assinante! Use "spy ajuda" para ajuda')
            elif (comando == 'stop'): self.__removerNick(nick)
            elif (comando == 'ignore'):
                if len(palavra.split()) != 2:
                    self.Say(nick, 'Lista atual (%d itens): %s' % (len(lst_ignore), ', '.join(lst_ignore)))
                    return                    
                lst_ignore.append(palavra.split()[1])
                self.Say(nick, '\x034*\x031 \x02%s\x02 adicionado ao ignore' % palavra.split()[1])
            elif (comando == 'clear'):
                if len(palavra.split()) != 2:
                    self.Say(nick, 'Defina qual tipo de limpeza. IGNORE ou BUFFER')
                    return                    
                clrt = palavra.split()[1].lower()
                if (clrt == 'ignore'):
                    lst_ignore = []
                    self.Say(nick, '\x034*\x031 \x02%s\x02 Lista de ignore esvaziada.')
                elif (clrt == 'buffer'):
                    config.buffer_thread.clear()
                    time.sleep(2.0)
                    self.Say(nick, '\x034*\x031 Buffer esvaziado')
                else:
                    self.Say(nick, 'Não entendi. Ou é IGNORE ou BUFFER')
        elif (not('PRIVMSG' in lst_ignore) and (mensagem['params'][0][0] == '#')) or (not('PRIVPVT' in lst_ignore) and (mensagem['params'][0][0] != '#')):
           frase = '\x032%s\x031 \x02<\x02\x0314%s\x031\x02>\x02 %s' % (mensagem['params'][0], nick, mensagem['params'][1])
           self.Despachar(frase)  
                
    def Join(self, mensagem):
        global lst_ignore
        if ('EVENTOS1' in lst_ignore): return
        frase = '\x035%s entrou em \x031%s' % (mensagem['prefix']['nick'], mensagem['params'][0])   
        self.Despachar(frase)
        
    def Kick(self, mensagem):
        global lst_ignore
        if ('EVENTOS2' in lst_ignore): return
        frase = '\x034%s foi expulso de \x031%s' % (mensagem['params'][1], mensagem['params'][0])
        self.Despachar(frase)

    def Part(self, mensagem):
        global lst_ignore
        if ('EVENTOS1' in lst_ignore): return
        frase = '\x035%s saiu de \x031%s' % (mensagem['prefix']['nick'], mensagem['params'][0])
        self.Despachar(frase)
        
    def Quit(self, mensagem):
        global lst_ignore
        if ('EVENTOS2' in lst_ignore): return
        frase = '\x034%s saiu da rede' % (mensagem['prefix']['nick'])
        self.__removerNick(mensagem['prefix']['nick'])
        self.Despachar(frase)
        
    def Nick(self, mensagem):
        global lst_ignore
        if ('EVENTOS2' in lst_ignore): return
        frase = '\x035%s mudou de nick para %s' % (mensagem['prefix']['nick'], mensagem['params'][0])
        self.__removerNick(mensagem['prefix']['nick'])
        self.Despachar(frase)
         
    def Out(self, mensagem):
        global lst_ignore
        if ('BOTSAY' in lst_ignore): return
        if ('PONG ' in mensagem): return
        frase = '\x02>>\x02 %s' % (mensagem)
        self.Despachar(frase)
        
    def AllMsg(self, mensagem):
        global lst_ignore, lst_assinantes, buffer
        if ('MSGPURAS' in lst_ignore): return
        lista = [Comandos.CMD_PRIVMSG,
                 Comandos.CMD_JOIN,
                 Comandos.CMD_KICK,
                 Comandos.CMD_PART,
                 Comandos.CMD_QUIT,
                 Comandos.CMD_NICK,
                 Comandos.RPL_MOTD,
                 Comandos.CMD_PING,
                 Comandos.CMD_PONG,
                 Comandos.RPL_NAMREPLY,
                 Comandos.RPL_AWAY  ]            
        for cmd in lista:
            if (cmd == mensagem['cmd']):
                return                
        if (mensagem['cmd'] == Comandos.RPL_WELCOME):
            lst_assinantes = [] 
            config.buffer_thread.clear()         
                
        self.Despachar(mensagem['puro'])
