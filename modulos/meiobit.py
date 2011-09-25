#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comandos import Comandos
from threading import Thread
from funcoes import codificar
import IPlugin, sys, time, metamark, web, config, funcoes, os

def NovoItem(titulo='', link='', descricao='', data='', autor=''):
    titulo = codificar(titulo)
    descricao = codificar(descricao)
    autor = codificar(autor)
    return {'Titulo': titulo, 'Link': link, 'Descricao': descricao, 'Data': data, 'Autor': autor}

class XMLParser:
    def getValue(self, texto, inicio, fim):
        i = texto.find(inicio) + len(inicio)
        return texto[i:texto[i:].find(fim)+i]

    def convert(self, valor):
        try:
            return int(valor)
        except: # 63 = ?
            return 63

    def Parse(self, source):
        global NovoItem
        # Atenção - Nivel de POG[0,1] = 0.73
        # Ignora o primeito <title>
        src = source[source.find('<item>') + 7:]
        titulo = self.getValue(src, '<title>', '</title>')
        link   = self.getValue(src, '<link>', '</link>')
        descr  = self.getValue(src, '<description>', '</description>')
        data   = self.getValue(src, '<pubDate>', '</pubDate>')
        autor  = self.getValue(src, '<dc:creator>', '</dc:creator>')
        # Tratar a descricao
        while descr.find('&lt;') != -1:
            i = descr.find('&lt;')
            descr = descr[:i] + descr[descr[i:].find('&gt;')+i+4:]
        x = 0
        while descr.find('&amp;#') != -1:
            i = descr.find('&amp;#')
            vlr = descr[i+6:descr[i+6:].find(';')+i+6]
            valor = self.convert(vlr) 
            descr = descr[:i] + chr(valor) + descr[i+6+len(vlr)+1:]
        descr = descr.replace('\r', '').replace('\n', ' ')
        descr = descr.replace('nbsp;', '').replace('&amp;', '')
        while '  ' in descr:
            descr = descr.replace('  ', '')
        # Até aqui o texto foi tratado, mas eu pego só o começo dele
        letras = 170
        if len(descr) > letras:
            descr = descr[:descr[letras:].find(' ')+letras] + '...'
        novo_link = metamark.XrlUS().getUrl(link)[0]
        return NovoItem(titulo, novo_link, descr, data, autor)

class FeedReader(Thread):
    def __init__(self, privmsg):
        global NovoItem
        Thread.__init__(self)
        self.PrivMsg = privmsg
        self.links_file = config.diretorio + 'meiobitlinks.txt'
        # Feeds
        self.PostsFeed = 'http://meiobit.com/index.xml'
        self.ForumFeed = 'http://meiobit.com/forum.xml'
        
    def Anunciado(self, link):
        if not os.path.exists(self.links_file):
            return False
        File = open(self.links_file, 'r')
        links = File.readlines()
        File.close()
        for line in links:
            if (line[:-1] == link):
                return True
        return False

    def Anunciar(self, info={}, adicional='', canal='#MeioBit'):
        msg = '%s(por %s) %s12%s: %s %s' % (adicional, info['Autor'], chr(3), info['Titulo'], info['Descricao'], info['Link'])
        if config.usuarios.has_key(canal.lower()):
            self.PrivMsg(canal, msg)
            if canal.lower() != '#meiobit':
                self.PrivMsg(canal, msg)                

    def Download(self, pagina):
        pag = web.get(pagina)
        if ('502 Server Error' in pag): return
        Parser = XMLParser()
        return Parser.Parse(pag)
    
    def AtualizarPost(self, acanal='#MeioBit', force=False):
        new = self.Download(self.PostsFeed)
        if (new == None) or ('div>' in [new['Descricao'], new['Link']]):
            return
        if not self.Anunciado(new['Link']) or force:
            self.Anunciar(new, adicional='[News] ', canal=acanal)
            if not force:
                funcoes.EscreverNoArquivo(self.links_file, new['Link'] + '\n')

    def AtualizarForum(self, acanal='#MeioBit', force=False):
        new = self.Download(self.ForumFeed)
        if (new == None) or ('div>' in new['Descricao']): 
            return
        if not self.Anunciado(new['Link']) or force:
            self.Anunciar(new, adicional='[Forum] ', canal=acanal)
            if not force:
                funcoes.EscreverNoArquivo(self.links_file, new['Link'] + '\n')
        
    def MostrarQuantosAnuncios(self, canal):
        if not os.path.exists(self.links_file):
            self.PrivMsg(canal, 'Arquivo de histórico não encontrado :(')
            return
        File = open(self.links_file, 'r')
        links = File.readlines()
        File.close()
        self.PrivMsg(canal, 'Anunciei %d vezes.' % len(links))        
        
    def Atualizar(self):
        self.AtualizarPost()
        self.AtualizarForum()

    def run(self):
        while True:
            #try:
                time.sleep(10)
                self.Atualizar()
                time.sleep(260)
            #except: pass

class MeioBitPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        ''' O Plugin só é ativado se for passado como parâmetro
            o valor e de self.Argumento  '''
        self.Argumento = '-meiobit'
        self.Bot = Bot
        if self.__ativo():
            self.Palavra  = 'meiobit'
            self.user_cmds = ['.meiobit']

    def __ativo(self):
        return (self.Argumento in sys.argv)

    def ajuda(self, nick):
        if not self.__ativo():
            self.Bot.Say(nick, 'O plugin não está habilitado.')
            return
        lista = ['Sintaxe: .meiobit [opção]',
                 '-n  Pega o post mais recente do site',
                 '-f  Mostra o topico mais recente no forum do site',
                 '-c  Mostra quantas noticias já foram publicadas']
        for item in lista:
            self.Bot.Say(nick, item) 
    
    def carregar(self):
        config.MeioBitFeed = None
        if self.__ativo() and (config.MeioBitFeed == None):
            config.MeioBitFeed = FeedReader(self.Bot.Say)

    def comandos(self):
        return {Comandos.RPL_ENDOFMOTD: self.Iniciar, 
                Comandos.CMD_PRIVMSG: self.PrivMsg}

    def Iniciar(self, mensagem):
        if self.__ativo():
            try:
                config.MeioBitFeed.start()
            except:
                self.Bot.GravarErro()

    def PrivMsg(self, mensagem):
        if not self.__ativo() or (config.MeioBitFeed == None):
            return
        analise = self.analisar(mensagem)
        alvo = analise['resposta']
        if not (analise['cmd'] in self.user_cmds):
            return 
        if ('help' in analise['param']):
            self.ajuda(alvo)
            return
        if (analise['param'] == ''):
            self.Bot.Say(alvo, 'What? Para ajuda, use .meiobit --help')
            return
        if ('n' in analise['param']):
            config.MeioBitFeed.AtualizarPost(alvo, True)
        if ('f' in analise['param']):
            config.MeioBitFeed.AtualizarForum(alvo, True)
        if ('c' in analise['param']):
            config.MeioBitFeed.MostrarQuantosAnuncios(alvo)
