# -*- coding: utf-8 -*-
from comandos import Comandos
import config, IPlugin, sys, random

class TreadIncorporation(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.linux']
        self.Palavra   = 'linux'
        self.Descricao = 'Ajuda em alguns comandos linux'
        self.Autor     = 'JimmySkull'
        self.Versao    = '0.1'
        self.Bot       = Bot
   
    def ajuda(self, nick):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.Controle}
       
    def carregar(self):
        pass
        
    def enviarlista(self, nick, lista):
        [self.Bot.Say(nick, item) for item in lista] 

    def chmod(self, nick):
        help = ['chmod XXX arquivo', 
                '0 = Nenhuma permissão  | 4 = Apenas leitura',
                '1 = Apenas execução    | 5 = Execução e leitura',
                '2 = Apenas gravação    | 6 = Leitura e gravação',
                '3 = Execução e gravação| 7 = Todos; leitura, gravação e execução']
        self.enviarlista(nick, help)
        
    def fstab3(self, nick):
        self.Bot.Say(nick, 'adfs, affs, autofs, coda, coherent, cramfs, devpts, efs, ext2, ext3, hfs, hpfs, iso9660, jfs, minix, msdos, ncpfs, nfs, ntfs, proc, qnx4, reiserfs, romfs, smbfs, sysv, tmpfs, udf, ufs, umsdos, vfat, xenix, xfs.')
        
    def fstab4(self, nick):
        help = ['auto, noauto - Montagem automatica no boot (default: auto)', 
                'user, nouser - Permite os usuarios montarem o disco/particao. (default: user)',
                'exec, noexec - Permite execucao de binarios (default: exec)',
                'rw - Montar como read-write, leitura e escrita',
                'ro - Montar como read-only, somente leitura',
                'sync, async - Como eh a sincronizacao de dados (I/O). sync: guarda na memoria e espera confirmacao pra escrever. (default: async)',
                'suid, nosuid - Habilita/desabilita o bit de set-user-identifier ou set-group-identifier.',
                'defaults - rw, suid, dev, exec, auto, nouser e async; para mais, man mount']
        self.enviarlista(nick, help)

    def fstab(self, nick):
        help = ['Coluna 1 - Partição/disco a ser montado.',
                'Coluna 2 - Local de montagem do disco/partição.',
                'Coluna 3 - Sistema de arquivo do disco/partição (.linux fstab 3)',
                'Coluna 4 - Opções de montagem da partição/disco (.linux fstab 4)',
                'Coluna 5 - Dump do sistema. Dump decide se o sistema deve ou não fazer backup. 0 (zero) ignora o disco/partição.',
                'Coluna 6 - fsck para a verificação dos discos/partições. Partições/discos de sistema normalmente tem valor 1, outras valor 2. Se for 0 (zero), o fsck nao faz verificacao.']
        self.enviarlista(nick, help)
        
    def topcmds(self, nick):
        self.Bot.Say(nick, "history|awk '{print $2}'|awk 'BEGIN {FS=\"|\"} {print $1}'|sort|uniq -c|sort -rn|head -10")

    def Controle(self, mensagem):
        global frases, nick_normal
        analise = self.analisar(mensagem)
        valor = analise['valor'].lower()
        param = analise['param']
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']
        if not (analise['cmd'].lower() == '.linux'):
            return
        
        if ('help' in analise['param']) or (valor == ''):
            self.Bot.Say(alvo, '.linux <palavra>  | Palavras: chmod, fstab, topcmds')
            return
            
        if valor == 'chmod':
            self.chmod(alvo)
    
        if valor == 'topcmds':
            self.topcmds(alvo)
        
        b1 = valor.split()
        if b1[0] == 'fstab':
            if len(b1) == 1:
                self.fstab(alvo)
            else:
                if b1[1] == '3':
                    self.fstab3(alvo)
                elif b1[1] == '4':
                    self.fstab4(alvo)
                else: self.Bot.Say(alvo, 'Nenhuma informacao adicional para a coluna ' + b1[1])
        
        
