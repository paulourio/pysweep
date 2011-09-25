# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin

class AdminControlPlugin(IPlugin.Plugin):
    ''' Plugin para administradores controlares o bot. '''    
    def __init__(self, Bot=None):
        self.Descricao = 'Controle de administradores'
        self.Autor     = 'JimmySkull'
        self.Versao    = '0.4'
        self.Bot       = Bot
        
    def ajuda(self, nick):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg,
                Comandos.CMD_NICK: self.OnNick,
                Comandos.CMD_QUIT: self.OnQuit}
       
    def carregar(self):
        lista = ['quit', 'admins', 'raw', 'clear (limpar buffer)', 
                 'reconectar', 'msg <canal> <msg>', 'action <canal> <msg>', 
                 'modulos <comando>', 
                 'canais (listar canais e usuarios)' ]
        config.admins = []
        for item in lista:
            self.add_admin_cmd(item)
       
    def listar_modulos(self, nick):
        erros = len(self.Bot.Gerenciador.ModulosErros)
        ignorados = len(config.modulos_ignorados)        
        x = 'Carregados: %s' % (', '.join(self.Bot.Gerenciador.PluginList))
        self.Bot.Say(nick, x)
        if erros > 0:
           x = 'Plugins com erro ao inicializar: %s' % (', '.join(self.Bot.Gerenciador.ModulosErros))
           self.Bot.Say(nick, x)
        if (ignorados > 0):
           self.Bot.Say(nick, 'Lista de plugins para ignorar: %s' % ', '.join(config.modulos_ignorados))
        
    def recarregar_modulos(self, nick):
        try:
            copiaadmins = config.admins
            if self.Bot.Gerenciador.recarregar_extensoes():
                config.admins = copiaadmins
                self.Bot.Say(nick, 'Módulos recarregados! :)')
            else:
                self.Bot.Say(nick, 'Erro ao recarregar. :/')
        except:
            try:
                import traceback
                trace = traceback.format_exc()
                lines = list(reversed(trace.splitlines()))
                for x in trace:
                    self.Bot.Say(nick, x)
            finally: 
                self.Bot.GravarErro()
                        
    def ignorar_modulo(self, nick, params):
        if len(params) == 1:
            self.Bot.Say(nick, 'Defina o plugin para ignorar durante esta sessao ("modulos ignore plugin.py")')
        else:
            config.modulos_ignorados += [params[1]]
            self.Bot.Say(nick, params[1] + ' adicionada para a lista de extensoes ignoradas. Recarregando plugins...')
            self.recarregar_modulos(nick)

    def designorar_modulo(self, nick, params): 
        if len(params) == 1:
            self.Bot.Say(nick, 'Defina o plugin para designorar durante esta sessao ("modulos unignore plugin.py")')
        else:
            if config.modulos_ignorados.__contains__(params[1]):
                config.modulos_ignorados.remove(params[1])
                self.Bot.Say(nick, params[1] + ' removido da lista de extensoes ignoradas. Recarregando plugins...')
                self.recarregar_modulos(nick)
            else:
                self.Bot.Say(nick, params[1] + ' não encontrado na lista de extensoes ignoradas. (Lembrete: case-sensitive)')

    def status_modulos(self, nick):
        modulos = len(self.Bot.Gerenciador.modulos)
        plugins = self.Bot.Gerenciador.quantidade_extensoes()
        erros = len(self.Bot.Gerenciador.ModulosErros)
        ignorados = len(config.modulos_ignorados)
        status = 'Status: %d módulos (%s plugins), Erros: %d, Ignorados: %d módulos (%d plugins).' % (modulos, plugins, erros, ignorados, len(self.Bot.Gerenciador.ModulosIgnorados))
        self.Bot.Say(nick, status)
        
    def modulos_config(self, nick, palavra):
        if ('-help' in palavra) or (palavra == ''):
            self.Bot.Say(nick, 'modulos <comando> <parametros>')
            self.Bot.Say(nick, 'Comandos:')
            self.Bot.Say(nick, '\x02reload\x02 Recarregar gerenciador de plugins.')
            self.Bot.Say(nick, '\x02list\x02 Lista nome dos plugins carregados.')
            self.Bot.Say(nick, '\x02status\x02 Mostra quantidade de plugins carregados/com.erros/ignorados.')
            self.Bot.Say(nick, '\x02ignore plugin.py\x02 Ignora o plugin.py')
            self.Bot.Say(nick, '\x02unignore plugin.py\x02 Remove plugin.py da lista de ignorados')
            return
        parse = palavra.split()
        if (palavra  == 'reload'): self.recarregar_modulos(nick)
        if (palavra  == 'status'): self.status_modulos(nick)
        if (palavra  == 'list'):   self.listar_modulos(nick)
        if (parse[0] == 'ignore'): self.ignorar_modulo(nick, parse)            
        if (parse[0] == 'unignore'): self.designorar_modulo(nick, parse)
        if (palavra == 'init'): self.Bot.Say(nick, str(self.Bot.Gerenciador.classes_inicializadas))
         
    def doAction(self, nick, valorsplitted, mensagem):
        if len(valorsplitted) == 0:
            self.Bot.Say(nick, 'Porra, a sintaxe é action #canal mensagem bla bla')
            return        
        self.Bot.Action(valorsplitted[0], mensagem)
        
    def doSay(self, nick, valorsplitted, mensagem):
        if len(valorsplitted) == 0:
            self.Bot.Say(nick, 'Porra, a sintaxe é msg #canal mensagem bla bla')
            return        
        self.Bot.Say(valorsplitted[0], mensagem)
    
    def MostrarCanais(self, nick, canal, param):
        if not hasattr(config, 'usuarios'):
            self.Bot.Say(nick, 'ERRO: Lista não encontrada!!')
        if ('help' in param):
            self.Bot.Say(nick, 'canais [#canal || -c #canal || -f nick]')
            self.Bot.Say(nick, 'Nenhum parâmetro mostra em quais canais estou.')
            self.Bot.Say(nick, '#canal     Mostra os users de um canal.')
            self.Bot.Say(nick, '-c #canal  Mostra os quantos users tem em um canal.')
            self.Bot.Say(nick, '-f nick    Mostra em quais canais eu vejo NICK.')
            return
        if ('c' in param):
            if not config.usuarios.__contains__(canal):
                self.Bot.Say(nick, 'Canal nao encontrado. Atuais: ' + ', '.join(config.usuarios))
            else:
                self.Bot.Say(nick, '%s tem %d users' % (canal, len(config.usuarios[canal])))
            return
        if ('f' in param):
            canais = []
            for Cn in config.usuarios:
                for nck in config.usuarios[Cn]:
                    if nck.lower() == canal:
                        canais += [Cn]
                        break
            if len(canais) == 0:
                self.Bot.Say(nick, 'Não encontrei o %s nos meus canais.' % canal)
            else:
                self.Bot.Say(nick, 'Encontrei em ' + ', '.join(canais))
            return      
        if (canal == ''):
            self.Bot.Say(nick, ', '.join(config.usuarios))
        elif not config.usuarios.__contains__(canal):
            self.Bot.Say(nick, 'Canal nao encontrado. Atuais: ' + ', '.join(config.usuarios))
        else:
            self.Bot.Say(nick, '%d users: %s' % (len(config.usuarios[canal]), ', '.join(config.usuarios[canal])))
        
    def FecharBot(self, nick, quit_msg):
        self.Bot.Mostrar('** Finalizado por ' + nick)
        self.Bot.Desconectar(quit_msg)

    def PrivMsg(self, mensagem):
        analise = self.analisar(mensagem)
        cmd = analise['cmd']
        palavra = analise['valor']
        nick = mensagem['prefix']['nick']
        
        raw_msg = ''
        if palavra != '':
            raw_msg = ' '.join(mensagem['puro'].split()[2:][1:]) 
                
        # Comandos dos administradores
        if nick.lower() in self.admins():
            if cmd == 'admins': self.Bot.Say(nick, 'Administradores logados: %s' % ', '.join(self.admins()))
            if cmd == 'clear': self.Bot.ControleFluxo.clear()
            if cmd == 'raw': self.Bot.Enviar(raw_msg)
            if cmd == 'msg': self.doSay(nick, palavra.split(), ' '.join(raw_msg.split()[2:]))
            if cmd == 'action': self.doAction(nick, palavra.split(), ' '.join(raw_msg.split()[2:]))
            if cmd == 'reconectar': self.Bot.Reconectar()
            if cmd == 'canais': self.MostrarCanais(nick, palavra.lower(), analise['param'])
            if cmd == 'modulos': self.modulos_config(nick, palavra.lower())
            if cmd == 'quit': self.FecharBot(nick, palavra)

        # Verificar senha
        if mensagem['params'][1] in config.senhas_admin:
            if self.isAdmin(nick):
                self.Bot.Say(nick, 'Você já está logado.. D\'oh!')
            else:
                self.add_admin(nick)
                self.Bot.Say(nick, 'Seja bem vindo! :)')
            comandos_admin = '\x031, \x032'.join(config.admin_cmds)
            comandos_admin = comandos_admin.replace('<', '\x034<\x031').replace('>', '\x034>\x032')
            comandos_admin = comandos_admin.replace('(', '\x035(\x037').replace(')', '\x035)\x032').replace('.', '\x02\x031.\x02\x032')
            self.Bot.Say(nick, 'Comandos atuais: \x032%s' % comandos_admin)

    def OnNick(self, mensagem):
        if self.isAdmin(mensagem['prefix']['nick']):
            self.rem_admin(mensagem['prefix']['nick'])
            self.Bot.Say(mensagem['params'][0], 'Logout.') 
    
    def OnQuit(self, mensagem):
        if self.isAdmin(mensagem['prefix']['nick']):
            self.rem_admin(mensagem['prefix']['nick'])
