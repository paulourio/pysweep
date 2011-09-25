#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin, random

tried_recover = False

frases_onkicked = ['Wanna die? --\'',
                   'Qual é a tua mano? Vai kickar a tua mãe!',
                   'Que que foi que eu fiz? :~',
                   '\x01ACTION enfurecido.\x01',
                   '\x01ACTION will kill somebody.\x01',
                   '\x01ACTION want to kill.\x01',
                   'I kill you!',
                   'GTHB. lol',
                   'Pra que essa raiva toda?']
frases_onkick = ['UAHUAHAUhuhahauhu kick\'em all :D',
                 'kkkk, i love it.',
                 'lol',
                 'quando chega a minha vez que kickar?',
                 'bem feito.',
                 'haha, foda.']

class ControlPlugin(IPlugin.Plugin):
    '''
    Plugin para controle do bot.
    A implementação dos comandos do protocolo IRC estão aqui.    
    - Atualização do nick do bot
    - Auto-identificar o nick
    - Recuperar nick (GHOST)
    - Entrar nos canais da lista autojoin
    - Responder mensagens CTCP: PING, VERSION e USERINFO
    - Controle a lista de usuários. config.usuarios == {'canal': ['usuarios']}
    - Re-entrar num canal ao ser kickado. (Acompanha com umas gracinhas)
    '''
    def __init__(self, bot=None):
        self.Descricao = 'Controle geral do bot'
        self.Autor     = 'JimmySkull'
        self.Versao    = '2.3'
        self.Bot       = bot

    def ajuda(self, nick):
        pass
        
    def carregar(self):
        ''' Cria a lista de usuários '''
        config.usuarios = {}
        
    def msg_rand(self, lista_base):
        ''' Mensagem randômica '''
        return lista_base[random.randint(1, len(lista_base)-1)]   
                
    def comandos(self):
        return {Comandos.CMD_NICK: self.OnNick,
                Comandos.CMD_PRIVMSG: self.BotInfo, 
                Comandos.RPL_NAMREPLY: self.ReceberNicks, 
                Comandos.CMD_KICK: self.OnKick,
                Comandos.CMD_JOIN: self.OnJoin, 
                Comandos.CMD_QUIT: self.OnQuit,
                Comandos.CMD_PART: self.OnPart, 
                Comandos.ERR_NOMOTD: self.EndMOTD,
                Comandos.RPL_ENDOFMOTD: self.EndMOTD, 
                Comandos.ERR_NICKNAMEINUSE: self.RecoverNick,
                Comandos.CMD_NOTICE: self.OnNotice}

    def OnNotice(self, mensagem):
        ''' Auto-identificar um nick '''
        if len(mensagem['prefix']) < 3: return
        if (config.senha == ''): return 
        if (mensagem['prefix']['nick'].lower() != 'nickserv'): return
        if ('/nickserv identify' in mensagem['params'][1].lower()):
            self.Bot.Enviar('NICKSERV IDENTIFY ' + config.senha)
        elif ('/msg nickserv identify' in mensagem['params'][1].lower()):
            self.Bot.Say('NICKSERV', 'IDENTIFY ' + config.senha)

    def OnNick(self, mensagem):
        ''' Atualizar lista de usuários e nick do bot '''
        old = mensagem['prefix']['nick']
        nick  = mensagem['params'][0]
        # Nick do bot mudou
        if self.nick() == old:
            config.mynick = nick
        # Atualizar lista de usuários
        for canal in config.usuarios:
            if config.usuarios[canal].__contains__(old):
                del config.usuarios[canal][config.usuarios[canal].index(old)]
                config.usuarios[canal].append(nick)
            
    def OnKick(self, mensagem):
        global frases_onkicked, frases_onkick
        ''' Atualizar a lista de usuários, reentrar '''
        canal = mensagem['params'][0].lower()
        nick  = mensagem['params'][1]
        if self.nick().lower() == nick.lower():
            del config.usuarios[canal]
            self.Bot.Entrar(canal)
            __import__('time').sleep(1.0)
            self.Bot.Say(canal, self.msg_rand(frases_onkicked))
            return
            
        if config.usuarios[canal].__contains__(nick): 
            del config.usuarios[canal][config.usuarios[canal].index(nick)]
        self.Bot.Say(canal, self.msg_rand(frases_onkick))
            
    def OnJoin(self, mensagem):
        ''' Atualizar a lista de usuários '''
        canal = mensagem['params'][0].lower()
        if not config.usuarios.has_key(canal): return
        if self.nick() != mensagem['prefix']['nick']:
            config.usuarios[canal].append(mensagem['prefix']['nick'])
    
    def OnQuit(self, mensagem):
        ''' Atualizar a lista de usuários '''
        nick = mensagem['prefix']['nick']
        for canal in config.usuarios:
            if config.usuarios[canal].__contains__(nick):                
                del config.usuarios[canal][config.usuarios[canal].index(nick)]
                         
    def OnPart(self, mensagem):
        ''' Atualizar a lista de usuários '''
        canal = mensagem['params'][0].lower()
        nick = mensagem['prefix']['nick']
        if not config.usuarios.has_key(canal): return
        if self.nick() == nick:
            del config.usuarios[canal]
        elif config.usuarios[canal].__contains__(nick):                
            del config.usuarios[canal][config.usuarios[canal].index(nick)]

    def BotInfo(self, mensagem):
        ''' Reponder a CTCP: PING, VERSION e USERINFO '''
        if Comandos.CTCP_VERSION in mensagem['puro']:
            self.Bot.CTCP(mensagem['prefix']['nick'], config.version_rsp)
        elif Comandos.CTCP_USERINFO in mensagem['puro']:
            self.Bot.CTCP(mensagem['prefix']['nick'], config.version_rsp)
        elif '\x01PING' in mensagem['puro']:
            analise = self.analisar(mensagem)
            self.Bot.CTCP(mensagem['prefix']['nick'], analise['valor'])
            
    def ReceberNicks(self, mensagem):
        ''' Recebe a lista de usuários de um canal '''
        nicks = []
        canal = mensagem['params'][2].lower()
        for nick in mensagem['params'][3].split():
            if nick[0] in ['+', '@', '.', '&', '%']:
                nicks += [nick[1:]]
            else:
                nicks += [nick]
        # usuarios == {'canal': ['usuarios']}
        if not config.usuarios.has_key(canal):
            config.usuarios[canal] = nicks
        else:
            config.usuarios[canal] += nicks       
            
    def EndMOTD(self, mensagem):
       ''' Entrar nos canais pré-configurados '''
       if config.canais != '':
            self.Bot.Entrar(config.canais)
            
    def RecoverNick(self, mensagem):
        '''
        Recuperar nick 
        Variável tried_recover existe para apenas uma tentativa de 
        recuperar o nick do bot (senão ele fica o tempo todo).
        '''
        global tried_recover
        if tried_recover: return
        tried_recover = True
        from time import sleep
        nick = self.nick()
        self.Bot.Enviar('NICK ' + config.second_nick)
        config.mynick = config.second_nick
        self.Bot.Mostrar('Nick %s em uso. Mudando para %s, e tentando recuperar..' % (nick, config.second_nick))
        sleep(5.0)
        self.Bot.Enviar('NICKSERV GHOST %s %s' % (nick, config.senha))
        sleep(3.0)
        self.Bot.Enviar('NICK ' + nick)
        
