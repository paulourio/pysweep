# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin, sys

class MSNMsg:
    ''' Classe para mensagens que são recebidas do bitlbee '''
    BEM_VINDO = 'Welcome to the BitlBee gateway!'
    NICK_DESCONHECIDO = 'The nick is (probably) not regist'
    CONTA_CRIADA = 'Account successfully added'
    CONECTADO = 'Logging in: Logged in'
    DESCONECTADO = 'Signing off'
    CONFIRMACAO = 'commands to accept/reject'
    ERRO = 'Error: Someone else logged in with your account'
    
    
class MSNControl(IPlugin.Plugin):
    '''
    Classe para controle do funcionamento do bot em MSN.
    Usando a rede im.bitlbee.org, é possível usar o MSN através do IRC.
    Para ativar o plugin, deve ser passado como argumento na linha de comando "-msn"
    Para os plugins, config.MSN mostra se o plugin esta ativo.
    Se o plugin estiver ativo, outra variavel é usada: config.MSNLogado
    Ela mostra se o bot conseguiu logar no MSN. Esta variável só existe
    se o config.MSN for verdadeiro.
    
    Outras informações
        root é nick usado pela rede para enviar mensagens para o bot.
        mgroup é um MSN Group
        &chat00 são conversas em grupos
    '''
    def __init__(self, Bot=None):
        self.Argumento = '-msn'
        self.Palavra   = ''
        self.Descricao = 'Controle da conexão do MSN'
        self.Autor     = 'JimmySkull'
        self.Versao    = '0.725'
        self.central   = '&bitlbee'
        self.Bot       = Bot
   
    def __ativo(self):
        return (self.Argumento in sys.argv)
                
    def ajuda(self, nick):
        pass
        
    def comandos(self):
        if self.__ativo():
            return {Comandos.CMD_PRIVMSG: self.Controle}
        else: return {}
       
    def carregar(self):
        ''' Configurar as variáveis para a conexão do MSN '''
        config.MSNLogado = False
        config.MSN = self.__ativo()
        if self.__ativo():
            config.network  = 'im.bitlbee.org'
            config.canais   = ''
            config.nick     = config.msn_nick 
            config.msn      = config.msn_email
            config.senha    = config.msn_senha
            config.time_out = config.msn_time_out
            config.delay1   = config.msn_delay1
            config.delay2   = config.msn_delay2
            config.IsMSN    = True
            config.MSNLogado = False
            self.Bot.Mostrar('# Plugin MSN ativo')
    
    def DefinirCharSet(self, charset='utf-8'):
        self.Bot.Say(self.central, 'set charset %s' % charset)
        
    def Identificar(self, senha):
        self.Bot.Say(self.central, 'identify %s' % senha)
        
    def AdicionarConta(self, email, senha):
        self.Bot.Say(self.central, 'account add msn %s %s' % (email, senha))
        
    def AdicionarConta(self, email, senha):
        self.Bot.Say(self.central, 'account add msn %s %s' % (email, senha))
        
        
    def AtivarContas(self):
        self.Bot.Say(self.central, 'account on')
    
    def Controle(self, mensagem):
        if not self.__ativo(): return
        texto = ' '.join(mensagem['params'][1:])
        if MSNMsg.BEM_VINDO in texto:
            self.DefinirCharSet('utf-8')
            self.Identificar(config.senha)
        if MSNMsg.NICK_DESCONHECIDO in texto: self.AdicionarConta(config.msn, config.senha)
        if MSNMsg.CONTA_CRIADA in texto: self.AtivarContas()
        if MSNMsg.CONECTADO in texto: config.MSNLogado = True
        if MSNMsg.DESCONECTADO in texto: self.Bot.Desconectar()
        if MSNMsg.CONFIRMACAO in texto: self.Bot.Say(self.central, 'yes')
        
        
