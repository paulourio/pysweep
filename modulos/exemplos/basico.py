# -*- coding: utf-8 -*-
'''
 Arquivo de exemplo de extensão básico para o bot Sweep.
'''   
from comandos import Comandos
import config, IPlugin

# Classe da extensão
class ExemploJoinPlugin(IPlugin.Plugin):
    def __init__(self, bot=None):
        '''
        O argumento bot indica o acesso à classe de controle do
        bot. Com ela é possível acessar qualquer coisa do bot,
        como socket, classe de controle de fluxo de mensagens
        e até a classe de gerenciamento de extensões (plugins).
        '''
        self.Palavra   = 'join'          # Palavra-chave para a ajuda (help palavra).
        self.Sintaxe   = '.join <canal>' # Sintaxe para o uso da extensão
        self.Descricao = 'Entra no canal'# Descricao da funcao
        self.Bot       = bot             # Variavel para acessar a classe principal do bot.
        
    def ajuda(self, nick):
        '''
        Mostrar help para o usuario, quando ele enviar "help join"
        Para ignorar, deixe def ajuda(self, nick): pass
        '''
        self.Bot.Say(nick, 'Sintaxe: ' + self.Sintaxe)
        self.Bot.Say(nick, 'Descrição: ' + self.Descricao)
            
    def carregar(self):
        '''
        Chamado quando a extensão é carregado (ainda antes de conectar).
        É chamado somente uma vez.
        '''
        pass
    
    def comandos(self):
        '''
        Pegar lista de comandos do plugin
        É do tipo dicionário. A lista de comandos disponíveis está em comandos.py
        Exemplo:
          return {Comandos.CMD_PING: self.EventoPing, Comandos.CMD_JOIN: self.EventoJoin}
        '''
        return {Comandos.CMD_PRIVMSG: self.OnPrivMsg}
       
    def OnPrivMsg(self, mensagem):
        '''
        Quando o bot receber algum comando contido na lista de comandos(),
        o evento definido será chamado
        Nesse caso, quando PRIVMSG for recebido, será chamado o evento Join()
        Detalhes:
          mensagem é do tipo Dicionario, exemplos: 

        {'puro': 'NOTICE AUTH :*** Looking up your hostname...', 
         'prefix': {}, 
         'cmd': 'NOTICE', 
         'params': ['AUTH', '*** Looking up your hostname...']}
         
         
        {'puro': ':leguin.freenode.net 005 Doritos IRCD=dancer CAPAB CHANTYPES=# EXCEPTS INVEX CHANMODES=bdeIq,k,lfJD,cgijLmnPQrRstz CHANLIMIT=#:20 PREFIX=(ov)@+ MAXLIST=bdeI:50 MODES=4 STATUSMSG=@ KNOCK NICKLEN=16 :are supported by this server', 
         'prefix': {'host': 'leguin.freenode.net'}, 
         'cmd': '005', 
         'params': ['Doritos', 'IRCD=dancer', 'CAPAB', 'CHANTYPES=#', 'EXCEPTS', 'INVEX', 'CHANMODES=bdeIq,k,lfJD,cgijLmnPQrRstz', 'CHANLIMIT=#:20', 'PREFIX=(ov)@+', 'MAXLIST=bdeI:50', 'MODES=4', 'STATUSMSG=@', 'KNOCK', 'NICKLEN=16', 'are supported by this server']}


        {'puro': ':JimmySkull!n=ASF-1f@unaffiliated/jimmyskull PRIVMSG ##null :mensagem aqui', 
         'prefix': {'nick': 'JimmySkull', 'host': 'unaffiliated/jimmyskull', 'user': 'n=ASF-1f'}, 
         'cmd': 'PRIVMSG', 
         'params': ['##null', 'mensagem aqui']}

        '''
        analise = self.analisar(mensagem)
        if analise['cmd'] != '.join': return
        # Verifica se a pessoa não passou o argumento "-help"
        if ('-help' in analise['param']:
            self.ajuda(mensagem['prefix']['nick'])
        else: # Envia para o servidor "JOIN <canal>"
            self.Bot.Entrar(analise['valor'])
