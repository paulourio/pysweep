#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from comandos import Comandos
import config, IPlugin, sys, web
#import bd
from threading import Thread

class SedexRastreamento(object):
    def __init__(self):
        pass
    
    def __servicoFuncionando(self, pagina):
        return not ('Service Temporarily Unavailable' in pagina)
        
    def __codigoExistente(self, pagina):
        Msg1 = "txect01$.ErrorMsg" 
        Msg2 = 'nosso sistema não possui dados'
        return not ((Msg1 in pagina) or (Msg2 in pagina))
    
    def __substituir(self, codigo, de, para=''):
        while (de in codigo):
            codigo = codigo.replace(de, para)
        return codigo
        
    def __remover(self, codigo, inicio, fim, todos=True):
        ''' Remove o texto do inicio ao fim '''
        while (inicio in codigo):
            i = codigo.find(inicio)
            x = codigo[i:].find(fim)
            if x == -1: x=1
            codigo = codigo[:i] + codigo[x+i+len(fim):]
            if not todos: break
        return codigo    
        
    def __extrair(self, codigo, inicio, fim):
        ''' Extrai o texto entre inicio e fim '''
        cod = codigo.lower()
        inicio = inicio.lower()
        fim = fim.lower()
        tag1 = cod.find(inicio)
        tag2 = cod[tag1:].find(fim) + tag1
        return codigo[tag1+len(inicio):tag2]

    def __sedex(self, codigo):
        parametros = {'P_ITEMCODE': '',
                      'P_LINGUA' : '001', 
                      'P_TESTE': '',
                      'P_TIPO': '001',
                      'P_COD_UNI': codigo,
                      'Z_ACTION': 'Pesquisar'}
        uri = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList'
        return web.post(uri, parametros)
  
    def rastrear(self, codigo):
        pag = self.__sedex(codigo)
        tentativas = 1
        while not self.__servicoFuncionando(pag):
            pag = self.__sedex(codigo)
            tentativas += 1
            if tentativas == 6:
                return 0
        if not self.__codigoExistente(pag):
            return 1
        pag = '<' + self.__extrair(pag, '<td rowspan=', '</table>')
        pag = self.__substituir(pag, '</td><td>', ' | ')
        pag = self.__remover(pag, '<', '>')
        pag = self.__substituir(pag, '\n\n', chr(32))
        pag = self.__substituir(pag, chr(32)*2, chr(32))
        ''' Cada item tem que começar com um número, se o outro não
        começar com número, é adicionado ao ultimo item.. '''
        item = ''
        items = []
        for _item in pag.split('\n'):
            if len(_item) == 0: continue
            if (_item[0] in ['0', '1', '2']):
                if len(item) > 0:
                    items += [item]
                item = _item
            elif (item != ''):
                item += '\n' + _item
        if item != '': items += [item]
        items.reverse()
        return items
        
    def enfeitar(self, xitem):
        items = []
        bold = '\x02'
        for item in xitem.split('\n'):
            if not (item[0] in ['0', '1', '2']): # hora: 05 15 24
                items = items[:-1] + ['|' + ' '*18 + '| ' + item[:item.rfind('| ')+1] + bold + item[item.rfind('| ')+1:]] + items[-1:]
            else:
                items.append('| ' + item[:item.rfind('| ')+1] + bold + item[item.rfind('| ')+1:])
        items.reverse()
        return [item.replace('|', '\x034|\x031') for item in items]
        
class AssistirCodigosThread(Thread):
    def __init__(self, bot=None):
        # CREATE TABLE Rastreamento (assinante VARCHAR(40), valor VARCHAR(20), data NUMERIC(10, 6))
        Thread.__init__(self)
        self.Bot = bot

    def Inserir(self):
        x = self.bd.executar('INSERT INTO Rastreamento(assinante,valor,data) values (\'JimmySkull\', \'SX551994715BR\', %s)' % str(time.time()))
        print 'i',x
        self.bd.gravar()
            
    def Rastreamento(self, codigo, alvo):
        sedex = SedexRastreamento()

        info = sedex.rastrear(codigo)
        if not info:
            print 'nao encontrado'
            return
            
        ''' Gravar no histórico '''
        upd = 'UPDATE Rastreamento SET historico=\'%s\' WHERE Codigo = \'%s\''
        x = self.bd.executar(upd % (str(info), codigo))
        print x
        self.bd.gravar()
        
        ''' Avisar o usuario '''

        for item in info:
            print '\n'.join(sedex.enfeitar(item))
                    
    def run(self):
        #try:
            self.bd = bd.BancoDeDados('banco.bd')
            x = self.bd.executar('SELECT count(valor) from Rastreamento') 
            if (x[0] == 'ERRO'): 
                print x
                return
            self.Inserir()
            while True:
                x = self.bd.executar('SELECT count(valor) from Rastreamento')
                print x
                count = int(x[0][0])
                print 'Encontrados %d códigos..' % (count)
                if (count > 0):
                    x = self.bd.executar('SELECT valor from Rastreamento')
                    for _cod in x:
                        print 'Rastreando',_cod[0]
                        self.Rastreamento(_cod[0], '')
                time.sleep(4)#14400) # 4 horas
        #except: print 'ass'# self.Bot.GravarErro()
 
AssistirCodigos = None

class Mensagens:
    Iniciando = '\x02\x034*\x02\x032 Iniciando rastreamento para o código \x02%s\x02...'
    NaoEncontrado = '\x034|\x031 Nada encontrado - Exemplo de código: SS123456789BR'
    Indisponivel = '\x034|\x031 Serviço indisponível no momento. You lose! Try Again.'
    GrandeDemais = '\x034|\x031 Foram encontrados muitos items. Use o parâmetro \x02-u\x02 no comando para mostrar apenas o mais recente, ou acesse o site: http://websro.correios.com.br/'
    Finalizado = '\x02\x034*\x02\x032 Fim do rastreamento.'
        
class SedexPlugin(IPlugin.Plugin):
    def __init__(self, bot=None):
        self.user_cmds = ['.rastrear', '.r']
        self.Palavra   = 'sedex'
        self.Sintaxe   = 'rastrear <Identificador do Objeto>'
        self.Descricao = 'Pega a última informação de um objeto'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.2'
        self.Bot       = bot

    def ajuda(self, nick):
        lista = ['Sintaxe:  .r [opção] <Identificador do Objeto>  | Ex: .r BR1234X',
                 'Descricao: Rastreamentro de pacotes sedex.',# Todos códigos assinados, após 20 dias serão deletados.',
                 #'-a   Assinar código. Quando houver novas informações, o bot informará. Se no MSN, ele espera você estar online, se no IRC, ele envia um MEMO',
                 #'-l   Listar códigos assinados por você.',
                 #'-c   Cancelar assinatura de código.',
                 '-u   Mostrar a status mais recente.'
                 'Nenhuma opção mostra todas as informações disponíveis']
        [self.Bot.Say(nick, item) for item in lista] 

    def carregar(self):
        pass
        #global AssistirCodigos
        #AssistirCodigos = AssistirCodigosThread(self.Bot)

    def comandos(self):
        return {Comandos.RPL_ENDOFMOTD: self.Iniciar, 
                Comandos.CMD_PRIVMSG: self.PrivMsg}   
        
    def Iniciar(self, mensagem):
        pass
        #global AssistirCodigos
        #AssistirCodigos.start()        
        
    def Rastreamento(self, codigo, alvo, ultimo):
        sedex = SedexRastreamento()

        self.Bot.Say(alvo, Mensagens.Iniciando % codigo)
        info = sedex.rastrear(codigo)
        if info == 0:
            self.Bot.Say(alvo, Mensagens.Indisponivel)
            return
        if info == 1:
            self.Bot.Say(alvo, Mensagens.NaoEncontrado)
            return
        if ultimo:
            info = [info[-1]]
        if (len(info) > 10) and not self.Bot.SessaoMSN():
            self.Bot.Say(alvo, Mensagens.GrandeDemais)
            return
        for item in info:
            for _i in sedex.enfeitar(item):
                self.Bot.Say(alvo, _i, False)
        self.Bot.Say(alvo, Mensagens.Finalizado)                 
      
    def PrivMsg(self, mensagem):        
        analise = self.analisar(mensagem)
        cmd = analise['cmd'].lower()
        codigo = analise['valor']
        param = analise['param']
        alvo = analise['resposta']
        
        if not (cmd in self.user_cmds): return
        
        if 'help' in param:
            self.ajuda(alvo)
            return
        
        if (codigo == ''): return
            
        ultimo = ('u' in param)
        
        self.Rastreamento(codigo, alvo, ultimo)
        
