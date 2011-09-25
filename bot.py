#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, config, thread, funcoes, time, funcoes
#import bd
from irc.nucleo import ClienteBase
from gerenciador import GerenciadorExtensoes
from buffer import BufferControl
from comandos import Comandos

class IrcClient(ClienteBase):
    '''
    Classe de implementação do IRCpy. Ela não implementa quase nada.
    Apenas recebe a mensagem, responde a PING, trata os erros de conexão,
    e envia a mensagem ao Gerenciador de Extensões.
    '''
    def __init__(self, fim='\r\n', Bot=None):
        ''' Inicia a classe pai, e define as funções de análise (parsers) '''
        ClienteBase.__init__(self, fim)
        self.insere_parser(Comandos.CMD_PING, self.doping)
        self.insere_parser(Comandos.CMD_PRIVMSG, self.doprivmsg)
        self.insere_parser(Comandos.CMD_ERROR, self.doerro)
        self.insere_parser(Comandos.CMD_ERRO, self.doerro) # Em redes nacionais já recebi ERRO
        self.insere_parser(Comandos.CMD_KILL, self.killed)
        self.insere_saida_padrao(self.doall)
        self.insere_controle_erro(self.erro_socket) 
        self.Bot = Bot
        
    def ProcessarMensagem(self, tipo, mensagem):
        '''
        Envia as mensagens para as extensões. Esses plugins serão chamados
        dsincronizadamente com o bot. Se um erro ocorrer no plugin, será
        chamado o evento GravarErro() da classe Bot, para gravar os dados do erro
        e continuar com as chamadas dos plugins.
        '''
        if not config.silencioso:
            msg = [funcoes.LimpaString(m) for m in mensagem['params']]
            print '<< %s %s' % (mensagem['cmd'], ' '.join(msg))
        self.Bot.Gerenciador.despachar_mensagem(tipo, mensagem)
        self.Bot.Gerenciador.despachar_mensagem(Comandos.ALL_MSG, mensagem)

    def raw(self, mensagem):
        '''
        Escreve no socket diretamente. Se for em uma sessão MSN,
        tira os tags de cores. Caso dê algum erro ao enviar, 
        será chamao erro_socket()
        '''
        if self.Bot.SessaoMSN(): mensagem = funcoes.LimpaString(mensagem)
        if not config.silencioso: print '>>',mensagem
        if not self.envia(mensagem): return
        self.Bot.Gerenciador.despachar_mensagem(Comandos.OUT_MSG, mensagem)
        
    def doprivmsg(self, mensagem):
        '''
        Recebe PRIVMSG, envia para o gerenciador de extensões para disponibilizar
        ajuda, e depois envia para ProcessarMensagem()
        '''
        self.Bot.Gerenciador.BotAjuda(mensagem)              
        self.ProcessarMensagem(Comandos.CMD_PRIVMSG, mensagem)
        
    def doping(self, mensagem):
        ''' Responde ao PING do servidor '''
        self.raw('%s %s' % (Comandos.CMD_PONG, ' '.join(mensagem['params'])) )
        self.ProcessarMensagem(Comandos.CMD_PING, mensagem)

    def doall(self, mensagem):
        '''
        Recebe todas as mensagens. Só é chamado caso não exista um parser 
        específico para o comando recebido. Ao criar um novo parser lembre-se
        de enviar a mensagem para ProcessarMensagem() despachar para as extensões
        '''
        self.ProcessarMensagem(mensagem['cmd'], mensagem)
        
    def tentar_reconectar(self):
        ''' Chamado quando a conexão cair '''
        if config.tentar_reconectar and self.Bot.PermitirReconectar:
            self.Bot.Mostrar('# Tentando reconectar em %s segundos...' % config.reconnect_delay)
            time.sleep(config.reconnect_delay)
            self.Bot.Reconectar(True)
        else: 
            self.Bot.Desconectar(force=True)
    
    def erro_socket(self, erro):
        '''
        Tratamento de exceções do socket. 
        Se for TIMEOUT, manda reconectar; Se erro ao conectar, fecha;
        Se erro de escrita, reconecta; Outro rece fecha a aplicação.
        '''
        import socket
        if type(erro) == socket.timeout:
            self.Bot.Mostrar('# Tempo de espera limite atingido (%d seg): Conexão fechada.' % config.time_out)
            self.tentar_reconectar()
        elif type(erro) in [socket.gaierror, socket.error]:
            if erro[0] == -2:
                self.Bot.Mostrar('Servidor não encontrado! Finalizando..')
                self.Bot.Desconectar(force=True)
            elif erro[0] == 32:
                self.Bot.Mostrar('Broken pipe')
                self.tentar_reconectar()
        else:
            self.Bot.GravarErro()
            self.Bot.Desconectar(force=True)
            
    def doerro(self, mensagem):
        ''' Comando ERRO (Recebido normalmente quando desconecta) '''
        self.Bot.Reconectar(True)
        
    def killed(self, mensagem):
        ''' Recebido quando é morto com o GHOST, por exemplo '''
        self.Bot.Mostrar('** KILL: %s' % ' '.join(mensagem['params']))
        self.Bot.Desconectar(force=True)
        
class Bot():
    ''' Classe principal do bot. '''
    def __init__(self):
        self.Manter = True
        self.Irc = None
        self.Gerenciador = None
        self.ControleFluxo = None
        self.Reconnect = True
        self.PermitirReconectar = True

    def Ativo(self):
        '''
        Retorna se o loop do bot está ativo.
        É para uso próprio da classe.
        '''
        return self.Manter
        
    def SessaoMSN(self):
        '''
        Retorna se o plugin msn.py está habilitado
        (Para habilitar precisar ter o argumento -msn na linha de comando)
        '''
        return config.MSN == True
        
    def GravarErro(self, reiniciar=False):
        '''
        Grava o erro no arquivo de histórico,
        logo em seguida, reinicia a conexão.
        Caso ocorra um erro pra salvar o erro (lol)
        o bot é finalizado.
        '''
        try:
            import traceback
            trace = traceback.format_exc()
            lines = list(reversed(trace.splitlines()))
            if not config.silencioso:
                print trace
            funcoes.AdicionarHistorico(trace)
            if reiniciar: self.Reconectar(True)
        except: 
            if reiniciar: self.Desconectar(True)

    def Mostrar(self, texto):
        '''
        Mostra no terminal se o parâmetro -debug for passado
        e adiciona no histórico. Evite usar print,
        para facilitar a análise de eventuais bugs.
        '''
        if not config.silencioso:
            print texto
        funcoes.AdicionarHistorico(texto)
            
    def Desconectar(self, mensagem=None, force=False):
        '''
        Desconecta do servidor, e finaliza o bot.
        Com o parâmetro force==True não é enviado o QUIT.
        '''
        self.PermitirReconectar = False
        self.ControleFluxo.clear()  
        self.ControleFluxo.stop()
        if not force:
            if mensagem == None:
                mensagem = config.quit_msg
            self.Enviar('QUIT :%s\r\n' % mensagem, 1)
            time.sleep(1)
            self.Irc.desconecta()
            self.PermitirReconectar = True
        self.Mostrar('Desconectado.')
        self.Manter = False
        self.Reconnect = False

    def Reconectar(self, force=False):
        '''
        Desconecta do servidor, e sai da classe principal,
        voltando pro loop inicial (módulo sweep), aí
        a classe Bot() é reiniciada.
        Com o parâmetro force==True não é enviado o QUIT.
        '''
        if not self.PermitirReconectar: return
        self.ControleFluxo.clear()  
        self.ControleFluxo.stop()
        if not force:
            self.Irc.envia('QUIT :%s\r\n' % config.quit_msg)
            self.Mostrar('# Reconectando...')
            time.sleep(5)
            self.Irc.desconecta()        
        else:
            self.Mostrar('# Reconectando...')
        self.Manter = False
        self.Reconnect = True
    
    def Enviar(self, mensagem, prioridade=0, codificar=True):
        '''
        Enviar mensagem.
        Valor para prioridade:
           0 = baixa: adiciona a mensagem à lista do buffer, que controla o fluxo
           1 = alta: escreve diretamente no socket, pulando todos os items da lista.
        '''
        msg = mensagem
        if codificar:
            try:
                msg = ' '.join([funcoes.codificar(pal, 'utf-8') for pal in msg.split()])
            except Exception, e: pass
        if prioridade == 0: 
            self.ControleFluxo.AddMsg(msg)
        else:
            self.Irc.raw(msg)
        
    def NOTICE(self, destino, mensagem):
        ''' Enviar um NOTICE '''
        self.Enviar('NOTICE %s :%s' % (destino, mensagem))
    
    def CTCP(self, destino, mensagem):
        ''' Enviar um notice CTCP '''
        self.NOTICE(destino, '\x01%s\x01' % mensagem)
    
    def Say(self, destino, mensagem, codificar=True):
        ''' Enviar uma mensagem (PRIVMSG) '''
        length = 430
        msg = mensagem
        while len(msg) > 0:
            pos = msg[length:].find(' ')
            if (pos > 20):
                pos = 0
            self.Enviar('PRIVMSG %s :%s' % (destino, msg[:pos+length].strip()), 0, codificar)
            msg = msg[pos+length:]
    
    def Action(self, destino, mensagem):
        ''' Enviar uma mensagem ACTION (Comando "/me" de clientes) '''
        self.Say(destino, '\x01ACTION %s\x01' % mensagem)
        
    def Entrar(self, canal):
        ''' Entrar em um canal '''
        self.Enviar('JOIN %s' % canal)
        
    def Sair(self, canal):
        ''' Sair de um canal '''
        self.Enviar('PART %s' % canal)
        
    def Iniciar(self):
        '''
        Coração do bot.
        Primeiro é iniciado a classe de IRC, o Controle de Fluxo de 
        mensagens, o gerenciador de extensões. Depois é criado o log
        da sessão e então o bot conecta à rede.
        '''
        # Parte 1: Iniciar Classes           
        self.Irc = IrcClient(Bot=self)
        self.ControleFluxo = BufferControl(self)
        #self.bd = bd.BancoDeDados(config.diretorio + 'banco.bd', self)
        self.Gerenciador = GerenciadorExtensoes(self)
        self.Gerenciador.carregar_extensoes()
        self.Gerenciador.mostrar_info()
        
        # Parte 2: Cria cabeçalho para o arquivo de histórico
        if config.silencioso:
            self.Mostrar("# Modo output silencioso")
        elif hasattr(config, 'log_file'): print '# Log: ' + config.log_file
        self.Mostrar("# Rede: %s - Porta: %s - TimeOut: %s" % (config.network, config.porta, config.time_out))
        self.Mostrar("# Nick: %s - NickAlt: %s" % (config.mynick, config.second_nick))
        self.Mostrar("# Canais: %s" % config.canais)
        if len(self.Gerenciador.ModulosIgnorados) > 0:
            self.Mostrar('# Extensões ignoradas: ' + str(self.Gerenciador.ModulosIgnorados) )
        
        # Parte 3: Conectar
        try:            
            self.Mostrar("Conectando...")
            if not self.Irc.conecta(config.network, config.porta, config.time_out):
                return
            self.Mostrar("Conectado, enviando informacoes..")
            self.Enviar(Comandos.CMD_NICK + chr(32) + config.mynick, 1)
            self.Enviar('USER %s %s %s :%s' % (config.user, config.user, config.network, config.real_name), 1)
            self.ControleFluxo.start()
            self.Irc.start()
            while self.Ativo():
                time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit), v:
            self.Desconectar()
        except:
            self.GravarErro(False)
        #self.bd.fechar()
        return self.Manter or self.Reconnect
