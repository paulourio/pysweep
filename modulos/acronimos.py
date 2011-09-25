#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from comandos import Comandos
import config, IPlugin, os, funcoes, random, time

class FloodControl(Thread):
    def __init__ (self, Bot):
        Thread.__init__(self)
        self.buffer = []
        self.Bot    = Bot

    def AddMsg(self, msg):
        self.buffer.append(msg)
        
    def clear(self):
        self.buffer = []
        
    def run(self):
        while True:
            if len(self.buffer) > 0:
                self.Bot.Enviar(self.buffer[0])
                self.buffer = self.buffer[1:]  
            else:
                break
            if not self.Bot.SessaoMSN():
                time.sleep(1.5)
            
class AcronimosPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.acr', '.acronimo']
        self.Palavra   = 'acronimo'        
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.0'
        self.acr_file = config.diretorio + 'acronimos.txt'
        self.Bot = Bot

    def adminajuda(self, nick):
        self.Bot.Say(nick, ' -d   Deletar acronimo: .acr -d WTF  |  .acr -de WTF: Wut That Fak')
        self.Bot.Say(nick, ' -f <NICK> <TEMPO> Floodar nick com X acronimos aleatorios. Ex: .acr -f Hunter 100')
    
    def ajuda(self, nick):
        lista = ['Sintaxe: .acr WTF | .acronimo WTF',
                 'Descricao: Lista de acronimos com o valor dela.',
                 ' -a     Adicionar acronimo: .acr -a WTF: What That Fuck',
                 ' -e     Procurar pelo acronimo exato.',
                 ' -w     Procurar por definição',
                 ' -c     Mostrar quantidade de acronimos conhecidos',
                 ' -p<N>  Página de acrônimos. Ex: .acr -ep1 w | .acr -p90 w']
        [self.Bot.Say(nick, item) for item in lista]
        if self.isAdmin(nick):
            self.adminajuda(nick)
            
    def carregar(self):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.Acronimos}
    
    def retirarRepetidos(self, lista):
        out = []
        i = 0
        while i < len(lista):
            if (lista[i] in out):
                i += 1
                continue
            out += [lista[i]]
            i += 1
        return out
        
    def getAcronimo(self, acronimo, alvo, exato, busca_definicao, pagina):
        if not os.path.exists('acronimos.txt'):
            self.Bot.Say(alvo, 'Arquivo de acronimos nao encontrado')
            return
        results = []
        resultsAC = []
        f = open(self.acr_file, 'r')
        lacronym = acronimo.lower().strip()
        for ln in f:
            if (':' in ln):
                # Pega o acronimo ou definicao
                if busca_definicao:
                    tmpstring = ln[ln.find(':'):].lower().strip()
                else:
                    tmpstring = ln[:ln.find(':')].lower()
                # Compara string exato ou não
                if exato:
                    ok = lacronym == tmpstring
                else:
                    ok = lacronym in tmpstring
                # Adiciona resultado
                if ok:
                    results += [ln]
                    resultsAC += [ln[:ln.find(':')].upper()]
                    
        resultsAC = self.retirarRepetidos(resultsAC)
        if len(resultsAC) == 1:
            resultsAC = []
                    
        if len(results) == 0:
            self.Bot.Say(alvo, 'Nada para %s' % acronimo)
            return
            
        if (pagina == 0):
            x_range = random.randint(0, len(results))
            y_range = x_range + random.randint(7, 11)
            paginas = (len(results) / 5)
            if (len(results) % 5) != 0:
                paginas += 1
            if len(results) > 40:
                if exato: resultsAC = []
                self.Bot.Say(alvo, 'Caralho! Encontrei %d com "%s" (%d paginas). Seja mais especifico, ou use -p1.. %s' % (len(results), acronimo.upper(), paginas, ', '.join(resultsAC[x_range:y_range])))
            elif len(results) > 20:
                if exato: resultsAC = []
                self.Bot.Say(alvo, 'Encontrei %d com "%s" (%d paginas). Especifique mais, ou use -p1... %s' % (len(results), acronimo.upper(), paginas, ', '.join(resultsAC[x_range:y_range])))
            elif len(results) > 7:
                if exato: resultsAC = []
                self.Bot.Say(alvo, 'Foram encontrados %d com "%s" (%d paginas). %s' % (len(results), acronimo.upper(), paginas, ', '.join(resultsAC)))

        # Parametro "-p"
        if (len(results) > 7) and (pagina == 0):
            return
        elif (pagina != 0):
            pagina = pagina - 1
            i = pagina * 5
            results = results[i:i+5]

        if (len(results) == 0) and (pagina > 0):
            self.Bot.Say(alvo, 'Hm, não tem nada nessa página.')
            
        for x in results:
            self.Bot.Say(alvo, x)
     
    def AcronimoExistente(self, acronimo):
        if not os.path.exists(self.acr_file):
            return False
        File = open(self.acr_file, 'r')
        lista = File.readlines()
        File.close()
        for line in lista:
            if (line[:-1] == acronimo):
                return True
        return False
    
    def addacronimo(self, acronimo, nick):
        if (len(acronimo.split()) < 2) or not (': ' in acronimo):
            self.Bot.Say(nick, 'Defina o acrônimo e o seu valor (WTF: What That Fuck). Use --help para ver a ajuda.')
            return 
        if self.AcronimoExistente(acronimo):
            self.Bot.Say(nick, 'Já tenho esse acrônimo. Uh, e com essa mesma descrição.')
            return
        acronym = acronimo[:acronimo.find(':')].upper()
        acronimo = acronym + acronimo[len(acronym):]
        funcoes.EscreverNoArquivo(self.acr_file, acronimo + '\n')
        self.Bot.Say(nick, 'Acrônimo adicionado. Total: %d' % self.getAcronimoCount())
        
    def delacronimo(self, acronimo, nick, exato):
        delcnt = 0
        File = open(self.acr_file, 'r')
        lista = File.readlines()
        File.close()
        File = open(self.acr_file, 'w')
        acronimo = acronimo.lower()
        for ln in lista:
            if not (':' in ln):
                File.write(ln)
                continue
            ls = ln[:-1].lower()
            if not exato:
                if not (acronimo in ls):
                    File.write(ln)
                else:
                    self.Bot.Say(nick, 'Deletado: ' + ln[:-1])
                    delcnt += 1
            else:
                if not (acronimo.strip() == ls.strip()):
                    File.write(ln)
                else:
                    self.Bot.Say(nick, 'Deletado: ' + ln[:-1])                    
                    delcnt += 1
        File.close()
        if delcnt == 0:
            self.Bot.Say(nick, 'Nenhum deletado.')
        else:
            self.Bot.Say(nick, '%d deletado(s).' % delcnt)
            
    def getAcronimoCount(self):
        validos = 0
        File = open(self.acr_file, 'r')
        lista = File.readlines()
        File.close()
        for ln in lista:
            if (':' in ln):
                validos += 1
        return validos
                
    def showAcronimoCount(self, acronimo, nick):
        self.Bot.Say(nick, 'Uhul, eu tenho %d acrônimos salvos!' % self.getAcronimoCount())
     
    def FLOOD(self, mandante, nick, quantidade):
        config.floodthread = FloodControl(self.Bot)
        
        if 5000 < quantidade:
            self.Bot.Say(mandante, 'Denied.')
            return        
        validos = []
        f = open(self.acr_file, 'r')
        for ln in f:
            if (': ' in ln):
                validos += [ln[:-1]]
        f.close()
        # Montar frases e calcular bytes
        # PRIVMSG <NICK> :<FRASE>
        prefixo = 10 + len(nick)
        bytes = 0
        
        frases = []
        total = len(validos)
        formato = '%%.%dd: %%s' % (len(str(quantidade)))
        for i in range(1,quantidade+1):
            frase = str(formato % (i, validos[random.randint(1,total-1)]))
            frases += [frase]
            bytes += prefixo + len(frase)
        tempo = len(frases) + (len(frases) - 20)
        if quantidade <= 20:
            tempo = quantidade + 1 
        comp = 'segundos'
        if tempo > 60:
            tempo = tempo / 60
            comp = 'minutos'
        if tempo > 60:
            tempo = tempo / 60
            comp = 'horas'
        info = '(%d msgs;%d bytes;%d %s)' % (quantidade, bytes, tempo, comp)
        self.Bot.Say(mandante, 'Floodando %s com %d acrônimos aleatórios %s...' % (nick, quantidade, info))
        if (comp in ['anos', 'dias']):
            self.Bot.Say(mandante, 'Hmm, %s? Hahaha, tchau.' % comp)
            return        
        for msg in frases:
            config.floodthread.AddMsg('%s %s :%s' % (Comandos.CMD_PRIVMSG, nick, msg))
        config.floodthread.AddMsg('%s %s :Terminei de floodar o %s com os %s acrônimos.' % (Comandos.CMD_PRIVMSG, mandante, nick, quantidade))
        config.floodthread.start()
                            
    def Acronimos(self, mensagem):
        analise = self.analisar(mensagem)
        cmd = analise['cmd']
        palavra = analise['valor']
        param = analise['param']
        alvo = analise['resposta']  
        nick = mensagem['prefix']['nick']
            
        if not (cmd in self.user_cmds):
            return
            
        if ('help' in param):
            self.ajuda(alvo)
            return 
                        
        if (palavra == '') and (param == ''):
            self.Bot.Say(alvo, 'Defina o acrônimo. Use --help para ver a ajuda.')
            return
  
        quantos = 0
        if ('f' in param):
            if not self.isAdmin(nick):
                self.Bot.Say(alvo, 'hahahahaha, sai daki manézão, vai lá toma toddy pirralho!')
                return
            if len(palavra.split()) < 2:
                if (palavra == 'stop') and hasattr(config, 'floodthread'):
                    config.floodthread.clear()
                    del(config.floodthread)
                    self.Bot.Say(alvo, 'Stopped.')
                    return
                self.Bot.Say(alvo, '.acr -f nick tempo  | .acr -f stop')
                return                
            nick_alvo = palavra.split()[0]
            try:
                quantos = int(palavra.split()[1])
            except:
                self.Bot.Say(alvo, 'Erro ao converter "%s" para inteiro. Use --help para ver a ajuda.' % palavra)
                return
            self.FLOOD(alvo, nick_alvo, quantos)
            return

            
        if ('c' in param):
            self.showAcronimoCount(palavra, alvo)
            return  
            
        if (palavra == ''):
            self.Bot.Say(alvo, 'Defina o acrônimo. Use --help para ver a ajuda.')
            return  
          
        if ('a' in param):
            self.addacronimo(palavra, alvo)
            return
            
        pagina = 0
        if ('p' in param):
            valor = param[param.find('p')+1:]
            if valor in ['', '0']:
                self.Bot.Say(alvo, 'Defina qual página você quer ver, começando por 1. Use --help para ver a ajuda.')
                return
            try:
                pagina = int(valor)
            except:
                self.Bot.Say(alvo, 'Erro ao converter "%s" para inteiro. Use --help para ver a ajuda.' % valor)
                return
                
        if ('d' in param):
            if not (nick.lower() in self.admins()):
                self.Bot.Say(alvo, 'Denied.')
                return
            self.delacronimo(palavra.lower(), alvo, ('e' in param))
            return
            
        if ('e' in param):
            self.getAcronimo(palavra, alvo, True, ('w' in param), pagina)
            return    
                
        #if (param != ''):
        #    self.Bot.Say(alvo, 'Nao entendi :( Use --help para ver a ajuda.')
        #    return 
            
        self.getAcronimo(palavra, alvo, False, ('w' in param),  pagina)
