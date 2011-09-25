#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin, random, web, sys

tipo_laura = True
ia_habilitada = False
ia_pvt = True

class IAPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Argumento = '-ia'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.0'
        self.Bot = Bot

    def ajuda(self, nick):
        self.Bot.Say(nick, 'Ajuda: .ia 000 | <Ativo><PVT><Tipo> :: A:1/0; P:1/0; T:1/2; | Ex: .ia 102')
            
    def carregar(self):
        global ia_habilitada
        ia_habilitada = (self.Argumento in sys.argv)
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.IACall}
    
    def FixMsg(self, msg):
        id = "var resp = ''"
        new = msg[msg.find(id)+len(id)+2:msg.find('\\r\\n')]
        new = new.replace('\r', '').replace('\n', '').replace('<br>', '')
        new = new.replace('\\', '').replace('; )', ';)').replace('oitenta e sete', '69')
        new = new.replace('sete', 'Laura').replace('zoom', 'Fogosa').replace('fotografia', 'putaria')
        new = new.replace('Sete', 'Laura').replace('Zoom', 'Fogosa').replace('SE7E', 'L4UR4')
        new = new.replace('fotógrafa', 'puta').replace('Closeup', 'zona').replace('Cinema', 'putaria')
        new = new.replace('Abigail', 'minha cafetona').replace('organismo', 'sexo anal brutal')
        new = new.replace('fotos', 'putaria').replace('fotógrafa', 'puta').replace('flash da máquina', 'vibrador')
        new = new.replace('Xis!', 'Aii que tesão!!!').replace(' Bi ', ' SylviaSaint ').replace('fotografar', 'sexo')
        new = new.replace('te dei motivos para dizer isso.', 'to nem ai, sou sim, e com orgulho!').replace('Fotografia', 'Putaria')
        while '<' in new:
            new = new[:new.find('<')] + new[new.find('>')+1:]
        while " var " in new:
            new = new[:new.find(' var ')] + new[new.rfind(');')+1:]
        return new
        
    def LauraMsg(self, msg):
        global tipo_laura
        try:
            msg_ = msg.replace(' ', '+').replace(chr(160), '+')
            if tipo_laura: #Laura
                url = 'http://www.inbot.com.br/cgi-bin/bot_gateway.cgi?server=127.0.0.1:8088&js=1&&msg='
            else: # EdBot
                url = 'http://www.inbot.com.br/cgi-bin/bot_gateway.cgi?server=bot.insite.com.br:8085&js=1&&msg='
            msg_rd = self.FixMsg(web.get(url + msg_))
            if ('o dispon' in msg_rd) and ('vel no momento.' in msg_rd):
                return 'nao quero fala contigo'
            try
				return msg_rd.decode('iso-8859-1').encode('utf-8')
			except
				return msg_rd
        except:
            return 'nao quero fala contigo'
         
    def LauraMsgIRC(self, para, nick, msg):
        resp = '%s, %s' % (nick, self.LauraMsg(msg))
        self.Bot.Say(para, resp, False)
                      
    def CutWord(self, palavra, msg):
        msg_ = msg
        if msg.lower() == palavra.lower():
            return ''
        while palavra.lower() in msg_.lower():
            i = msg_.lower().find(palavra.lower())
            x = msg_[i:].find(' ')
            if x < i:
                x = len(palavra)-1
            msg_ = msg_[:i] + msg_[i+x+1:]
        return msg_

    def IACall(self, mensagem):
        global ia_habilitada, tipo_laura, ia_pvt
        analise = self.analisar(mensagem)
        cmd = analise['cmd'].lower()
        valor = analise['valor'].lower()
        param = analise['param']
        alvo = analise['resposta']
        if (cmd == '.ia'):
            new_config = ['IA:']
            if (len(valor) != 3) or ('help' in param):
                self.ajuda(alvo)
                return
            try:
                tmp = int(valor)
            except:
                self.ajuda(alvo)
                return
            # Ativo
            if (valor[0] == '1'):
                ia_habilitada = True
                new_config += ['Ativo com ']
            elif (valor[0] == '0'):
                new_config += ['Inativo com ']
                ia_habilitada = False
            else:
                self.ajuda(alvo)
                return
            # PVT
            if (valor[1] == '1'):
                new_config += ['PVT habilitado ']
                ia_pvt = True
            elif (valor[1] == '0'):
                new_config += ['PVT desabilitado ']
                ia_pvt = False
            else:
                self.ajuda(alvo)
                return
            # Tipo
            if (valor[2] == '1'):
                new_config += ['no modo laura.']
                tipo_laura = True
            elif (valor[2] == '2'):
                new_config += ['no modo ed.']
                tipo_laura = False
            else:
                self.ajuda(alvo)
                return
            self.Bot.Say(alvo, ' '.join(new_config))
        ''' Ignora mensagens que começarem com . '''
        if (len(cmd) > 0) and (cmd[0] == '.'):
            return            

        if not ia_habilitada:
            return
            
        OK = (self.nick().lower() in mensagem['params'][1].lower())
        if ia_pvt and (alvo[0] != '#'):
            OK = True
        if OK:
            msg = self.CutWord(self.nick(), mensagem['params'][1])
            self.LauraMsgIRC(analise['resposta'], mensagem['prefix']['nick'], msg)
