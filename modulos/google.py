#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin, random, web

# Lista de mensagens caso nao encontre nada.
google_erros  = {
            1: "Nenhum resultado foi encontrado", 
            2: "Seja menos específico, porque eu não achei nada", 
            3: "Sem resultados :/", 
            4: "Foda... esse google não ta achando nada", 
            5: "PQP, o google não achou nada", 
            6: "O Google não achou nada, que decepção.. :(", 
            7: "Google vem perdendo moral comigo, não achou nada dessa vez",
            8: "Não achei nada.." }
            
class GooglePlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.g', '.wiki', '.dwiki']
        self.Palavra   = 'google'
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.5.2 POGued'
        self.Bot = Bot

    def ajuda(self, nick):
        lista = ['Sintaxe: <tipo-procura> [opções] <palavras-chave>',
                 'Tipos de Procura:  .g  .wiki  .dwiki',
                 'Descricao: Pesquisa Google | Se a palavra começar com '
                    '"-", será tratado como parâmetro do bot. Para ser '
                    'tratado como key-word, use "\-". Exemplo de uso com '
                    'NOT: .g linux \-free',
                 '-t   Mostrar o título antes do link',
                 '-a   Mostrar todos os resultados possiveis em uma mensagem',
                 '-s   Mostrar só a sugestao. Se nao tiver sugestao, o resultado da pesquisa eh mostrado',
                 '-c   Pegar resultado da calculadora ou de conversao. Ex: .g -c 40 reais -> dollar']
        [self.Bot.Say(nick, item) for item in lista] 
            
    def carregar(self):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.GoogleCall}
    
    def Calculadora(self, src):
        if "src=/images/calc_img.gif" in src:
            src = src[src.find('src=/images/calc_img.gif'):]
            valor = src[src.find('<b>')+3:src.find('</b>')]
            valor = valor.replace('&#215;', 'x').replace('<sup>', '^').replace('</sup>', '')
            while valor.find('<') != -1:
                valor = valor[:valor.find('<')] + valor[valor.find('>')+1:]                  
            return valor
        else:
            return 'Nenhum resultado da calculadora google'
     
    def __ajax_search(self, busca):
        query = urllib.urlencode({'q' : busca})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
        procudra = web.get(url)
        json = simplejson.loads(search_results.read())
        results = json['responseData']['results']
        return results
                
    def __socket_search(self, busca):
        URI = '/search?client=firefox-a&rls=org.mozilla%%3Apt-BR%%3Aofficial&channel=s&hl=pt-BR&q=%s&meta=&btnG=Pesquisa+Google'
        busca = busca.replace('+', '%2B').replace(' ', '+').replace('>', '%3E').strip()
        msg = web.criar_pedido('www.google.com.br', URI % busca, 'http://www.google.com.br/') 
        # Enviar pedido e receber resposta
        src = web.socket_send('www.google.com.br', 80, msg, '<script>google')
        if src == None: return
        src = src.replace('\n', '').replace('\r', '')
        return src

    def Google(self, busca, TxtOut, NotFoundMsg, parametros, para, nick):
        resultado = []
        # pega parametros
        if 'help' in parametros:
             self.ajuda(para)
             return
        titulos  = 't' in parametros
        todos    = 'a' in parametros
        sugestao = 's' in parametros
        calcular = 'c' in parametros

        # Pegar resultados
        src = self.__socket_search(busca)
            
        # Calculadora
        if calcular:
            self.Bot.Say(para, self.Calculadora(src))
            return
                
        tem_sugestao = ' quis dizer: ' in src[:src.find('<!--a-->')]
        if tem_sugestao:
            vc = src[src.lower().find('<b><i>')+6:src.lower().find('</i></b>')]
            resultado += ['Você quis dizer \x02%s\x02?' % vc]
            if sugestao:
                self.Bot.Say(para, resultado[0]) 
                return
                    
        if ' encontrou nenhum documento correspondente.' in src:
            if tem_sugestao:
                self.Bot.Say(para, 'Nada para \x02%s\x02. %s' % (busca, resultado[0]))
            else:
                self.Bot.Say(para, NotFoundMsg)
        else:
            tag = 'class=r><a href="'
            while tag in src.lower():
                src = src[src.lower().find(tag) + len(tag):]
                link = src[:src.find('" class=l')]
                if titulos:
                    titulo = src[src.find('class=l>')+8:src.find('</a></')]
                    if src.find('>') < src.find('<'): titulo = '<' + titulo #pog ;)
                    link   = '%s05%s %s01%s' % (chr(3), titulo, chr(3), link)
                        
                # Se o tamanho do resultado chegar ao máximo
                if ((len(' '.join(resultado)) + len(link)) > 410):
                    break
                        
                resultado += [link]
                   
                # Se não for pra pegar todos os links, pára.
                if not todos and (len(resultado) == 3):
                    break
                        
            result = ' | '.join(resultado)
            cnt = 0
            while result.find('<') != -1:
                result = result[:result.find('<')] + result[result.find('>')+1:]
                cnt += 1
                if cnt > 50:
                    result = 'erro'
            self.Bot.Say(para, TxtOut % result)
    
    def GoogleCall(self, mensagem):
        global google_erros
        
        analise = self.analisar(mensagem)
        cmd = analise['cmd']
        palavra = analise['valor']
        param = analise['param']
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']

        if not (cmd in self.user_cmds):
            return
        
        if (palavra == '') and (param == ''):
            self.Bot.Say(alvo, 'Uai, nada pra procurar? Para ajuda: .g --help')
            return
                
        if (cmd == '.g'):
            self.Google(palavra, 'G: %s', google_erros[random.randint(1,len(google_erros))], param, alvo, nick)
        elif (cmd == '.wiki'):
            WikiNotFound = 'Não encontrei nenhum artigo, experimente usar \x02.g %s\x02' % palavra
            self.Google(palavra + ' site%3Apt.wikipedia.org', 'Wikipedia: %s', WikiNotFound, param, alvo, nick)

        elif (cmd == '.dwiki'):
            self.Google(palavra + ' site%3Adesciclo.pedia.ws', 'Desciclopedia: %s', 'Nada para %s' % palavra, param, alvo, nick)
