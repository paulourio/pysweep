# -*- coding: utf-8 -*-
from comandos import Comandos
import config, IPlugin, sys, random, time

class IncorporationPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Palavra   = 'Incorporation'
        self.Descricao = 'Incorporation Plugins'
        self.Bot = Bot
   
    def ajuda(self, nick):
        self.Bot.Say(nick, 'Incorporation Types: .tread .diabo .jonas')
        
    def comandos(self):
        pass
       
    def carregar(self):
        pass

nick_normal = ''

frases = {
    1: 'YARRRRRRRRRRRRRRR'
}

frases1 = {
    1: 'YARRRRRRR, Sai da frente que eu hoje vo pega a %s, e ninguem me segura!',
    2: 'hohohohohohoh, A %s que me espere!',
    3: 'Estoy em busca da %s, minha diaba!'
}

class DiaboIncorporation(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Bot       = Bot
   
    def ajuda(self, nick):
        self.Bot.Say(nick, 'Incorporation Types: .tread .diabo .jonas')
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.Controle}
       
    def carregar(self):
        pass

    def msg_rand(self, lista_base):
        ''' Mensagem randômica '''
        return lista_base[random.randint(1, len(lista_base)-1)]   
    
    def Controle(self, mensagem):
        global frases, nick_normal
        analise = self.analisar(mensagem)
        frase = analise['valor']
        param = analise['param']
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']
        if (analise['cmd'] == '.diabo'):
            if (self.nick() == '^DIABO^'):
                if frase == '':
                    self.Bot.Enviar('NICK ' + nick_normal)
                else:
                    self.Bot.Say(alvo, frase)
            else:
                nick_normal = self.nick()
                self.Bot.Enviar('NICK ^DIABO^')
                if not (frase == ''):
                    time.sleep(3.0)
                    self.Bot.Say(alvo, self.msg_rand(frases1) % frase)
                    time.sleep(3.0)
                    self.Bot.Enviar('NICK ' + nick_normal)
                
        elif ('diabo' in analise['cmd'].lower()) and (self.nick() == '^DIABO^'):
            self.Bot.Say(alvo, self.msg_rand(frases))





frases_tread = {
    1: 'kkk pala',
    2: 'kkk deixa di se noob',
    3: 'lesadu',
    4: 'kkk.. dexa eu ouvi avril em paz uahsuhsas',
    5: 'noss, se eh mto lesadu',
    6: 'Q Lixo...',
    7: 'Seu inutil..',
    8: 'pala uhsuashuah',
    9: 'Q lixo.. to aki curtindo meu novo pc.. que nem vo fala a config. pra nao te humilha kkk',
    10: 'comprei minha lcd de 32 .. mas sempre uso 400x600 .. quando vou jogar crysys aih eu coloco 8000x9756 kkk',
    11: 'Eu jogando crysis a 500fps nao ocupa nem a metade do meu quad',
    12: 'dexa di se lesadu kkk',
    13: 'noss q lixo..',
    14: 'uahsuhsa ce eh mto noob',
    15: 'uashuah nao chega aos meus pés',
    16: 'e dai? to muito feliz com meu IE6!',
    17: 'dexa di se noob.. perai que to instalando a nova versao do AVG.',
    18: 'aff, se mata auaushsauh',
    19: 'vai aprende a mecher no pc, noob shuhsusahu'
}

class TreadIncorporation(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Bot       = Bot
   
    def ajuda(self, nick):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.Controle}
       
    def carregar(self):
        pass

    def msg_rand(self, lista_base):
        ''' Mensagem randômica '''
        return lista_base[random.randint(1, len(lista_base)-1)]   
    
    def Controle(self, mensagem):
        global frases_tread, nick_normal
        analise = self.analisar(mensagem)
        frase = analise['valor']
        param = analise['param']
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']
        if (analise['cmd'] == '.tread'):
            if (self.nick() == 'TREAD'):
                if frase == '':
                    self.Bot.Enviar('NICK ' + nick_normal)
                else:
                    self.Bot.Say(alvo, frase)
            else:
                nick_normal = self.nick()
                self.Bot.Enviar('NICK TREAD')
        elif ('tread' in analise['cmd'].lower()) and (self.nick() == 'TREAD'):
            self.Bot.Say(alvo, self.msg_rand(frases_tread))
        
nomes_jonas = ['Jonas.. ',
               'JoOoOonas! ',
               'Jonas! ',
               'JONAS! ',
               'J\x02O\x02N\x02A\x02S! ',
               '\x031J\x030ã\x031o\x030o\x031n\x030a\x031a\x030s\x031s.. ',
               'Jon\x02a\x02s.. ',
               'J\x034o\x031O\x02o\x02O\x032on\x037as\x031.. '] 

frases_jonas = [
'Desde que completou a maioridade a baleia é sua casa, sua cidade',
'Dentro dela guarda suas gravatas, seus ternos de linho',
'E ele diz que se chama Jonas, e ele diz que é um santo homem',
'E ele diz que mora dentro da baleia por vontade própria',
'E ele diz que está comprometido, e ele diz que assinou papel',
'Que vai mante-lo preso na baleia até o fim da vida, até subir pro céu',
'Dentro da baleia a vida é tão mais fácil, nada incomoda o silêncio e a paz de jonas',
'Quando o tempo é mal, a tempestade fica de fora, a baleia é mais segura que um grande navio'
]

jonas_last = -1

class JonasIncorporation(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.Bot       = Bot
   
    def ajuda(self, nick):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.Controle}
       
    def carregar(self):
        pass
        
    def msg_rand(self, lista_base):
        global jonas_last
        x = jonas_last
        while (x == jonas_last):
            x = random.randint(1, len(lista_base)-1)
        jonas_last = x
        return lista_base[x]
    
    def Controle(self, mensagem):
        global frases_tread, nick_normal, frases_jonas
        analise = self.analisar(mensagem)
        frase = analise['valor']
        param = analise['param']
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']
        if (analise['cmd'] == '.jonas'):
            self.Bot.Say(alvo, 'Dentro da baleia mora mestre ' + self.msg_rand(nomes_jonas) + self.msg_rand(frases_jonas))
