#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
import IPlugin, web, random, funcoes

class DicionarioPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.dic']
        self.Palavra   = 'dicionario'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.3'
        self.Bot       = Bot

    def ajuda(self, nick):
        lista = ['Sintaxe: .dic <tipo> <palavra>',
                 'Descricao: Pega definicao de palavras',
                 ' -ip  Sinônimos em português da palavra em inglês no freedict.com',
                 ' -pi  Sinônimos da inglês palavra em português no freedict.com',
                 ' -c   Não mostrar abreviaturas.',
                 ' -p   Procura definição pt-pt no site priberam.pt (Busca Padrão)', 
                 ' -i   Procura definição en-en no site thefreedictionary.com']
        for item in lista:
            self.Bot.Say(nick, item) 

    def carregar(self):
        pass

    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.PrivMsg}

    def DicionarioPtPt(self, procura, para, completo):
        uri = 'http://www.priberam.pt/dlpo/definir_resultados.aspx'
        pag = web.post(uri, {'h_texto_pesquisa': procura})
        if pag.find('lblNaoEncontrou') == -1: 
            pag = pag[pag.find('<span id="lblDlpoPesqPalavra">'):pag.find('<!-- fim TEXTO CONTEUDOS -->')]
            pag = pag.replace('<br />', '\r\n')
            while pag.find('<') != -1:
                pag = pag[:pag.find('<')] + pag[pag.find('>')+1:]
            pag = pag.replace('\r\n', ',').replace('\t', ' ')

            while pag.find('  ') != -1:
                pag = pag.replace('  ', ' ').replace(', ', ' ').replace(',,', ' | ').replace(';,', ';')
            pag = pag.replace(';-', ' |').replace(' -:', ':').strip('| ').replace(' ,', ' ')
            pag = funcoes.codificar(pag, 'utf-8', de='iso-8859-1')
            pag = pag.replace('|', '\x02|\x02').replace(';', '; ')
            # tirar abreviaturas
            if completo:
                pag = pag.replace('2 gén.', '2 gêneros').replace    ('2 núm.', '2 números (singular e plural)')
                pag = pag.replace('adj.',   'adjectivo').replace    ('adv.',   'advérbio; adverbial')
                pag = pag.replace('art.',   'artigo').replace       ('card.',  'cardinal').replace('Lat.', 'Latim')
                pag = pag.replace('comp.',  'comparativo').replace  ('conj.',  'conjunção; conjuncional')
                pag = pag.replace('def.',   'definido').replace     ('dem.',   'demonstrativo').replace('f.', 'feminino ')
                pag = pag.replace('indef.', 'indefinido').replace   ('interj.','interjeição')
                pag = pag.replace('interr.','interrogativo').replace('int.',   'intransitivo')
                pag = pag.replace('loc.',   'locução').replace      ('m.',     'masculino ').replace('mult.',   'multiplicativo')
                pag = pag.replace('num.',   'numeral').replace      ('ord.',   'ordinal').replace  (' part.','particípio')
                pag = pag.replace('pass.',  'passado').replace      ('pess.',  'pessoa').replace  ('plu.',   'plural')
                pag = pag.replace('poss.',  'possessivo').replace   ('pref.', 'prefixo')
                pag = pag.replace('prep.',  'preposição').replace   ('pron.',  'pronome; pronominal')
                pag = pag.replace('refl.',  'reflexo').replace      ('rel.',   'relativo').replace  ('s.',   'substantivo')
                pag = pag.replace('sing.',  'singular').replace     ('suf.',   'sufixo').replace    ('sup.', 'superioridade')
                pag = pag.replace('superl.','superlativo').replace  ('tr.',    'transitivo').replace('v.',   'verbo')
            self.Bot.Say(para, pag)
        else:
            f = 'javascript:SeleccionaEntrada(&quot;'
            x = 'A palavra não foi encontrada. Algumas sugestões: '
            while pag.find(f) > -1:
                pag = pag[pag.find(f)+len(f):]
                x = x + '\x02' + pag[:pag.find('&')] + '\x02, '
            self.Bot.Say(para, x.strip(', '))
    
    
    def FreeDict(self, tipo, palavra, palavra_exata, resultados):
        parametros = {'search': palavra,
                      'exact' : palavra_exata, 
                      'max': resultados}
        if tipo == 'enpt':
            parametros['from'] = 'English'
            parametros['to']   = 'Portugese'
            parametros['fname']= 'eng2por1'
        else:
            parametros['to']   = 'English'
            parametros['from'] = 'Portugese'
            parametros['fname']= 'eng2por2'
        parametros['back'] = 'por.html'
        return web.post('http://www.freedict.com/onldict/onldict.php', parametros)

    def Dicionario(self, tipo, palavra, para):
        token = '<td class="result-l-blue">'
        token2= '<td class="result-r-blue"><strong>'
        pag = self.FreeDict(tipo, palavra, 'true', '1')
        if pag.find('No matches found') != -1:
            pag = self.FreeDict(tipo, palavra, 'false', '10')
            if pag.find('No matches found') == -1:
                res = 'Hey! Ao inves de "%s", você quiz dizer algo como ' % palavra
                lista = []
                while pag.find(token) != -1:
                    pag = pag[pag.find(token) + len(token):]
                    lista += ['\x02%s\x02' % pag[:pag.find('</td>')]]
                self.Bot.Say(para, res + ' ou '.join(lista) + '?')
            else:
                self.Bot.Say(para, 'Nada para "%s"' % palavra)
        else:
            pag = pag[pag.find(token) + len(token):] 
            res = pag[:pag.find('</td>')] + ' = '
            pag = pag[pag.find(token2) + len(token2):]
            res = pag[:pag.find('</strong></td>')]
            self.Bot.Say(para, palavra + ' = ' + res)
           
    def remover(self, codigo, inicio, fim, substituir_por='', todos=True):
        ''' Remove o texto do inicio ao fim '''
        while (inicio in codigo):
            i = codigo.find(inicio)
            codigo = codigo[:i] + substituir_por + codigo[codigo[i:].find(fim)+i+len(fim):]
            if not todos: break
        return codigo
        
    def msg_rand(self, lista_base):
        ''' Mensagem randômica '''
        return lista_base[random.randint(1, len(lista_base)-1)] 
                
    def TheFreeDictionary(self, palavra, para):
        found = ['Yeah, encontrei: %s', '%s', 'Aqui: %s', ':) achei.. %s', '--> %s', 'Quem pediu? Tá aki: %s']
        not_found = 'Word not found in the Dictionary and Encyclopedia.'
        sugestoes = not_found + 'Did you mean:'
        sugestoes_end = 'Can\'t find what you are looking for?'
        # Aqui começa
        palavra = palavra.split()[0].lower()
        uri = 'http://www.thefreedictionary.com/' + palavra
        pag = web.get(uri)
        if (sugestoes in pag):
            resp = self.remover(pag[pag.find(sugestoes)+len(sugestoes):pag.find(sugestoes_end)], '<', '>', ' ')
            self.Bot.Say(para, 'Você quis dizer: %s?' % ', '.join(resp.split()))
        elif (not_found in pag):
            self.Bot.Say(para, 'Nada encontrado para "%s"' % palavra)
        else:
            self.Bot.Say(para, self.msg_rand(found) % uri)
        
    def PrivMsg(self, mensagem):        
        analise = self.analisar(mensagem)
        cmd = analise['cmd']
        palavra = analise['valor']
        param = analise['param'].lower()
        alvo = analise['resposta']
        
        if not (cmd in self.user_cmds):
            return
        
        if ('help' in param):
            self.ajuda(alvo)
            return
        
        if (palavra == ''):
            self.Bot.Say(alvo, 'Defina a palavra. Para ajuda digite .dic --help')
            return

        if (param in ['ip', 'pi']):
            self.Dicionario(param, palavra, alvo)
            return
        
        if ('i' in param):
            self.TheFreeDictionary(palavra, alvo)
            return

        self.DicionarioPtPt(palavra, alvo, ('c' in param))
