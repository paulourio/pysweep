#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, config, funcoes
import IPlugin, thread

class GerenciadorExtensoes:
    '''
    Gerenciador de Módulos
    Classe para o gerenciamento de extensões (plugins).
    Responsável por despachar as mensagens recebidas do servidor,
    e também disponibilizar ajuda para o usuário.
    A classe base para um Plugin está no módulo IPlugin.py
    '''
    def __init__(self, Bot):
        ''' 
        Ignorados e Erros são contadores de erros ao inicializar
        os plugins. Não há contador para erros durante uma execução.
        ModulosErros ficam o nome do módulo, e será verificado no
        despachar_mensagem()
        '''
        self.Bot = Bot
        self.init_info()

    def init_info(self):
        '''
        Função para iniciar as variáveis. Ela está separada do 
        __init__(), pois é usada ao recarregar as extensões.
        '''
        self.PluginList = []
        self.modulos = []
        self.ModulosErros = []
        self.ModulosIgnorados = []
        self.plugin_dir = ''
        config.user_cmds = []
        config.admin_cmds = []
        config.admins = []     
        
    def plugin_ativo(self, plugin):
        '''
        Quando é feito o recarregamento de extensões, nas extensões
        antigas são adicionadas um valor marcando-a como desabilitada.
        Então, as funções verificam se a extensão tem este valor, antes
        de usar. Isto é necessário porque é pego as sub-classes da
        classe genérica de plugins (IPlugin.Plugin), e em Python, não
        tem como descarregá-las.
        '''
        return not hasattr(plugin, '__tag__desabilitado__')
        
    def recarregar_extensoes(self):
        '''
        Recarregar extensões. Primeiro são deletadas as atuais,
        E depois vai ser como um reinício da classe, valores iniciais
        e carregamento de plugins,
        '''
        try:
            self.ModulosIgnorados = []
            for ext in self.extensoes():
                ext.__tag__desabilitado__ = True
                self.ModulosIgnorados += [ext.__module__]
            for mod in self.modulos:
                reload(mod)
            #self.init_info()
            #self.carregar_extensoes()
            self.Bot.Mostrar('# Plugins Recarregados')
            self.mostrar_info()
            return True
        except:
            self.Bot.GravarErro()
            return False
        
    def __despachar_mensagem(self, comando, parametros):
        '''
        Despachar mensagens para os plugins. Cada plugin tem uma função
        comandos() que retorna a lista de comandos que o plugin aceita.
        Caso de um erro no plugin, o erro é gravado sem reiniciar o bot.
        '''
        modulo = None
        try:
            for extensao in self.extensao_pelo_cmd(comando):
                modulo = extensao
                plug = extensao(self.Bot)
                if not (plug.__module__ in self.extensoes_ignoradas()):
                    plug.comandos()[comando](parametros)
        except:
            self.ModulosErros += [modulo.__name__ + '.py']
            self.Bot.GravarErro()

    def despachar_mensagem(self, comando, parametros):
        ''' 
        As mensagens são enviadas para os plugins em uma thread
        diferente, assim o bot não "trava" se houverem plugins que
        precisam de tempo para serem executados.
        '''
        thread.start_new_thread(self.__despachar_mensagem, (comando, parametros))
        
    def carregar_extensoes(self):
        '''
        Varre o diretório modulos e importa os módulos com a
        terminação ".py". Um plugin é uma classe herdada de IPlugin.Plugin
        '''
        self.plugin_dir = funcoes.tratar_diretorio(config.diretorio + 'modulos')
        for fname in os.listdir(self.plugin_dir):
            if not fname.endswith('py') or (fname[:2] == '__'):
                continue
            modulo = 'modulos.' + fname[:fname.rfind('.')]
            if self.extensoes_ignoradas().__contains__(fname) or self.PluginList.__contains__(fname):
                self.ModulosIgnorados += [fname]
                continue
            self.modulos += [__import__(modulo, None, None, [''])]
            self.PluginList += [fname]
        # Inicializar classes do modulo
        for pl in self.extensoes():
            if not self.plugin_ativo(pl):
                continue
            plug = pl(self.Bot)
            try:
                plug.carregar()
            except:
                config.modulos_ignorados += [plug.__module__]
                self.ModulosIgnorados += [plug.__module__]
                self.ModulosErros += [plug.__module__]
                self.Bot.Mostrar('# ** Erro ao carregar extensao %s em %s.. Ignorando módulo' % (pl.__name__, pl.__module__))
                self.Bot.GravarErro(False)
                    
    def quantidade_extensoes(self):
        ''' Retorna quantidade de extensões carregadas '''
        return len(self.extensoes())
    
    def extensoes_ignoradas(self):
        '''
        Retorna a lista passada pela linha de comando, isso inclui 
        os módulos não encontrados. e não encontradas.
        '''
        return config.modulos_ignorados

    def extensao_pelo_cmd(self, comando):
        ''' Retorna lista de plugins de um comando específico '''
        result = []
        for pl in self.extensoes():
            cmds = pl().comandos()
            if (type(cmds) != dict):
                continue
            if cmds.has_key(comando) and self.plugin_ativo(pl):
                result.append(pl)
        return result
    
    def extensoes(self):
        ''' Retorna todos os plugins carregados '''
        return IPlugin.Plugin.__subclasses__()

    def mostrar_info(self):
        ''' Grava no log de sessão números de extensões '''
        self.Bot.Mostrar("# %d módulos (%s plugins, %d erros, %d ignorados)." % 
                (len(self.modulos), self.quantidade_extensoes(), len(self.ModulosErros), len(self.ModulosIgnorados)))
        
    def plugins_com_ajuda(self):
        '''
        Lista de extensões que disponibilizam ajuda para o
        usuário (variável Palavra e função ajuda())
        '''
        result = []
        for pl in self.extensoes():
            plug = pl(self.Bot)
            if hasattr(plug, 'Palavra') and self.plugin_ativo(plug):
                if (plug.Palavra != '') and hasattr(plug, 'ajuda'):
                    result.append(plug.Palavra)
        return result
     
    def pegar_lista_comandos(self):
        '''
        Lista de extensões que disponibilizam ajuda para o
        usuário (variável Palavra e função ajuda())
        '''
        result = []
        for pl in self.extensoes():
            plug = pl(self.Bot)
            if hasattr(plug, 'user_cmds') and self.plugin_ativo(pl):
                result = result + plug.user_cmds
        return result
                     
    def mostrar_ajuda_por_indice(self, nick, palavra):
        '''
        Chama a função ajuda() de extensões em que extensão.Palavra
        forem iguais.
        '''
        result = False
        for pl in self.extensoes():
            plug = pl(self.Bot)
            if hasattr(plug, 'Palavra') and (plug.Palavra.lower() == palavra) and self.plugin_ativo(plug):
                result = True
                plug.ajuda(nick)
        if not result:
            self.Bot.Say(nick, 'Ahn?')

    def help_tipo(self):
        '''
        Mostra o comando de ajuda para usuário. Como o bot atua
        em MSN e IRC e os comandos são diferentes, é feita a distinguição.
        '''
        if self.Bot.SessaoMSN():
            return 'Use ajuda <palavra do indice>'
        else:
            return 'Use /msg %s ajuda <palavra do indice>' % config.mynick            
           
    def pegar_comandos(self):
        ''' Retorna todos os comandos incluindo os do gerenciador '''
        return ['.help', '.ajuda', '.comandos'] + self.pegar_lista_comandos()
        
    def BotAjuda(self, mensagem):
        ''' Procedimento para fornecer ajuda ao usuário '''
        user_cmds = ['.help', '.ajuda']
        nick = mensagem['prefix']['nick']
        palavra = mensagem['params'][0].lower()
        texto = ''
        # Se for em MSN, o alvo é o nick de quem mandou (nunca o canal)
        if self.Bot.SessaoMSN() and (mensagem['params'][0][0] in ['#', '&']):
            nick = mensagem['params'][0]
        
        if len(mensagem['params']) > 1:
            pal = ' '.join(mensagem['params'][1:]).split()
            if len(pal) > 0:
                palavra = pal[0]
            if len(pal) > 1:
                texto = ' '.join(pal[1:]).lower()
                
        if (palavra in user_cmds) or ((palavra in ['help', 'ajuda']) and not (mensagem['params'][0][0] in ['#', '&'])):
            if texto == '':
                self.Bot.Say(nick, 'Oi, eu sou um Bot desenvolvido em Python por JimmySkull (ricardothorstein [at] gmail [dot] com). Eu estou licenciado sob FAIL ( http://rthorstein.co.cc/fail/FAIL.txt ).')
                self.Bot.Say(nick, self.help_tipo())
                self.Bot.Say(nick, 'Indice: ' + ', '.join(self.plugins_com_ajuda()))
            else:
                self.mostrar_ajuda_por_indice(nick, texto.lower())
        # Mostra os comandos atuais registrados
        comandos = self.pegar_comandos()                
        if (palavra == '.comandos') or ((palavra in user_cmds) and (mensagem['params'][0][0] == '#')):
            self.Bot.Say(mensagem['params'][0], 'Os plugins mostram ajuda com o parâmetro "--help" | Comandos: %s' % ' '.join(comandos))
