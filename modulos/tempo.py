#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comandos import Comandos
import config, IPlugin, random, web, funcoes

class Frases:
    nao_encontrado = {
        1: 'Poutz, não encontrei esse lugar aí­ não..', 
        2: 'Bah, não achei essa cidade aki no meu banco de dados..', 
        3: 'Essa cidade existe ? ;)',
        4: 'Não achei essa tribo/quilombo',
        5: 'Achei não fi..',
        6: 'Hahahahahaha, não achei!',
        7: 'Digitou certo esse nome?!',
        8: '%cidade... como fas~?',
        9: 'Não foi lá que Judas perdeu as botas?',
        10:'Por favor coloque o nome de uma cidade do planeta Terra.',
        11:'Err...é dentro ou fora do triângulo das bermudas?',
        12:'Vai lá fora e olha!',
        13:'Hum... %cidade... há quantos anos isso não dá no jornal, hein?!',
        14:'A mesma de sempre, lá as coisas nunca mudam mesmo!',
        15:'Então é nesse lugar que as bolas do dragão se encontram? A-há!',
        16: "O tempo parou nesse lugar."}

    sem_informacao = {
        1: 'dis q os aparêio que mede as temperatura quebrô',
        2: 'Imprevisível!',
        3: 'Não tenho idéia..',
        4: 'Já tá pedindo de mais.',
        5: 'Já ouvi falar dessa cidade, mas não sei nada dela.',
        6: 'Ah, o tempo lá está bom... ou não!',
        7: 'Então... lá é legal, né?'
    }
    
    ''' Umidade == 100% '''
    umidade_max = {
        1: 'Uii, que úmido!',
        2: 'Tá chovendo né?',
        3: 'Úmido hein...',
        4: 'Hmmm, meu sexto sentido diz que está chovendo...',
        5: 'A cidade está toda molhadinha! ;)',
        6: 'Definitivamente NÃO vai dar praia hoje!',
        7: 'Minhas 2 bolas mágicas tem um ponteiro que está indicando chuva.'
    }

    ''' Umidade > 90% '''
    umidade_alta = {
        1: 'Através de cálculos assaz complexos, conclúo que PODE chover..',
        2: 'Acho que vai chover..',
        3: 'Especialistas indicam que há risco de chuva.',
        4: 'Usando bhaskara, concluo que há possibilidades de chuva elevada.',
        5: 'Fala sério, você achou que ia fazer sol hoje?'
    }
    
    ''' Umidade <= 25% '''
    umidade_baixa = {
        1: 'Está na hora de chover.. ;)',
        2: 'É, acho que vai dar praia...',
        3: 'Credo! Existe água aí?'
    }

    ''' Temperatura <= 4 '''
    temperatura_super_baixa = {
        1: 'Caralho! Que frio!',
        2: 'Friozinho polar, hein?!'
    }
    
    ''' Temperatura < 13 '''
    temperatura_baixa = {
    }
    
    ''' Temperatura >= 28 '''
    temperatura_alta = {
        1: 'Hmmm.. HOT!',
        2: 'Frio como o inferno!'
    }
    
    varios_resultados = 'Encontrei \x02%d\x02 cidades.. Especifique \x02Cidade,UF\x02 ou use \x02.w -a cidade\x02 para todos os resultados'

    cond_comp = '\x031Condições atuais de \x02%s\x02(%s): %s, Temperatura: \x02%s\x02, Vento %s. Umidade: \x02%s\x02. IUV: \x02%s\x02. %s'
    cond_normal = '\x031Condições atuais de \x02%s\x02: %s, Temperatura: \x02%s\x02, Vento %s. Umidade: \x02%s\x02. IUV: \x02%s\x02. %s'

class Tag:
    # Tags para as condições atuais ( br.weather.com )
    inicio_conteudo = '<!-- Begin Main Content Here-->'
    fim_conteudo = '<form name="Converter">'

    titulo  = '<font class="categoryTitle">'
    link_inicio    = '/weather/local/'
    link_fim = '</a><br>'

    fim_br = '<BR>'
    fim_td = '</TD>'

    cidade = '<!-- Insert City Name and Zip Code -->'
    relatorio = "Conforme relat&oacute;rio de "
    temperatura = '<TD COLSPAN="2" CLASS="obsTempText" VALIGN="TOP">&nbsp;'
    ceu = 'TD colspan="3" align="center" CLASS="obsText">'
    sensacao = 'Sensa&ccedil;&atilde;o de&nbsp;'
    vento = '<TD CLASS="currentObsText">'
    umidade = '<TD CLASS="currentObsText">'
    iuv = '<FONT CLASS="obsTempText">'
    
    # Tags para a previsão do tempo ( cptec.ineb.br )
    prev_not_found = 'Nenhuma cidade foi encontrada.'
    prev_cidades   = '<div id="cid">'
    
    prev_cidade    = '<div id="subcid">'
    prev_prox_item = '<div id="prev_ond">'
    prev_dia       = '<div id="tit">' 
    prev_icone     = '<img src="'
    prev_temp_min  = '<div id="c2">TEMP. MÍNIMA'
    prev_temp_max  = '<div id="c3">TEMP. MÁXIMA'
    prev_prob_chuva= '<div id="c4">PROB. DE CHUVA' #final </a></b>
    prev_nascer_sol= '<div id="c5">NASCER DO SOL'
    prev_por_do_sol= '<div id="c6">PÔR DO SOL'
    prev_iuv_maximo= '<div id="c7">IUV MÁXIMO'
    prev_final_div = '</div>'
    prev_final_lnk = '</a>'

class WeatherPlugin(IPlugin.Plugin):
    def __init__(self, Bot=None):
        self.user_cmds = ['.tempo', '.w', '.previsao', '.p']
        self.Palavra   = 'tempo'        
        self.Autor     = 'JimmySkull'
        self.Versao    = '1.7.1'
        self.Bot = Bot

    def ajuda(self, nick):
        lista = ['Sintaxe: \x032[\x031comando\x032] [\x031opções\x032] <\x031cidade\x032>',
                 'Comandos:',
                 '.tempo .w    = Informa as condições atuais (Fonte: br.weather.com)',
                 '.previsao .p = Mostra a  previsão do tempo (Fonte: tempo1.cptec.inpe.br)',
                 'Descricao: Pega as condições atuais de uma cidade. | Pega a previsão do tempo.',
                 'Opções:',
                 ' -a   Pegar as informações de todas as cidades com o mesmo nome.',
                 ' -d   Mostrar o link com os detalhes do local',
                 '--IUV Mostrar informações sobre o Índice de UV']
        [self.Bot.Say(nick, item) for item in lista]
            
    def carregar(self):
        pass
        
    def comandos(self):
        return {Comandos.CMD_PRIVMSG: self.ClimaTempo}
                   
    def MostrarIUV(self, nick):
        lista = ['O Índice UV apresentado é para condições de céu limpo (sem nuvens). '
                    'A presença de nuvens pode causar atenuação dos fluxos UV '
                    'que chegam à superfície. Sob condições de céu totalmente '
                    'encoberto, essa diminuição pode chegar à 70%.',
                 'Para calcular: IUV = IUVo X FM',
                 'Exemplo:  IUVo = 10 (índice UV mostrado da sua cidade) '
                    'FM = 0.2 (céu 75%-100% encoberto)',
                 'Portanto o IUV será dado por: IUV = 10 X 0.2 = 2',
                 'Índice de cobertura do céu:',
                 '\x031 Céu claro: 0%-25% = 1.0',
                 '\x031 Parc. Nublado:  25%-50% = 0.8',
                 '\x031 Nublado: 50%-75% = 0.5',
                 '\x031 Tempestade: 75%-100% = 0.2',
                 'Valores de UV:',
                 '\x021 à 2\x02: \x032Baixo\x031, Pode tentar se queimar à vontade. :)',
                 '\x023 à 7\x02: \x035Moderado a Alto(6+)\x031, Em horários próximos ao meio-dia procure '
                     'locais sombreados. Evite andar pelado por aí, e use boné. '
                     'Protetor solar é uma boa.',
                 '\x028 à 14\x02: \x034Muito Alto a Extremo(11+)\x031, Evite o sol ao meio-dia, permaneça na sombra, '
                     'use camisa, bone e protetor solar se não quiser morrer de câncer :)']
        [self.Bot.Say(nick, item) for item in lista]            

    def msg_rand(self, lista_base):
        ''' Mensagem randômica '''
        return lista_base[random.randint(1, len(lista_base)-1)]           
 
    def cortar(self, codigo, inicio='', fim=''):
        ''' Retirar o texto do codigo que não será mais utilizado. '''
        cod = codigo.lower()
        inicio = inicio.lower()
        fim = fim.lower()
        if (inicio != '') and (fim != ''):
            return codigo[cod.find(inicio)+len(inicio):cod.find(fim)]
        elif (inicio != ''): return codigo[cod.find(inicio)+len(inicio):]
        elif (fim != ''): return codigo[:cod.find(fim)]
        else: return codigo
        
    def extrair(self, codigo, inicio, fim):
        ''' Extrai o texto entre inicio e fim '''
        cod = codigo.lower()
        inicio = inicio.lower()
        fim = fim.lower()
        tag1 = cod.find(inicio)
        tag2 = cod[tag1:].find(fim) + tag1
        return codigo[tag1+len(inicio):tag2]       
    
    def remover(self, codigo, inicio, fim, todos=True):
        ''' Remove o texto do inicio ao fim '''
        while (inicio in codigo):
            i = codigo.find(inicio)
            codigo = codigo[:i] + codigo[codigo[i:].find(fim)+i+len(fim):]
            if not todos: break
        return codigo
    
    def weather(self, src, para, showlink, detalhes):
        cidade = self.extrair(src, Tag.cidade, Tag.fim_br).replace('\r\n', '  ').strip()
        conforme = self.extrair(src, Tag.relatorio, '.')
        src = self.extrair(src, Tag.inicio_conteudo, Tag.fim_conteudo)
        
        temperatura = self.extrair(src, Tag.temperatura, Tag.fim_td)
        src = self.cortar(src, Tag.temperatura)
        
        ceu = self.extrair(src, Tag.ceu, Tag.fim_br)
        src = self.cortar(src, Tag.ceu)
        
        sensacao = self.extrair(src, Tag.sensacao, Tag.fim_td)
        src = self.cortar(src, Tag.sensacao)
        if temperatura != sensacao:
            temperatura = '%s (Sensação de %s)' % (temperatura, sensacao)
            
        vento = self.extrair(src, Tag.vento, Tag.fim_td)

        src = self.cortar(src, '<B>Umidade:</B>')
        umidade = self.extrair(src, Tag.umidade, Tag.fim_td)
        src = self.cortar(src, Tag.umidade)
        
        src = self.cortar(src, '<B>&Iacute;ndice UV</B>')
        IUV = self.extrair(src, Tag.iuv, '</FONT>')
        
        # Até aqui, todos os dados foram recolhidos.
        # Agora começa o processo de brincadeirinhas :)
        if ('N/D' in temperatura) and ('N/D' in ceu) and ('N/D' in vento) and ('N/D' in umidade):
           self.Bot.Say(para, self.msg_rand(Frases.sem_informacao))
           return           
        observacao = ''
        if (umidade == '100%'):
            observacao = self.msg_rand(Frases.umidade_max)
        elif umidade[2:] == '%':
            umd = int(umidade[0:2])
            if umd > 90: observacao = self.msg_rand(Frases.umidade_alta)
            if umd <=25: observacao = self.msg_rand(Frases.umidade_baixa)

        if len(temperatura) <= 2: # certificar que não é N/D
            temp = int(temperatura)
            if temp < 13: observacao = self.msg_rand(Frases.temperatura_baixa)
            if temp <=4: observacao = self.msg_rand(Frases.temperatura_super_baixa)
            if temp >=28: observacao = self.msg_rand(Frases.temperatura_alta)
        
        cidade = funcoes.codificar(cidade)
        conforme = funcoes.codificar(conforme)
        ceu = funcoes.codificar(ceu)
        temperatura = funcoes.codificar(temperatura)
        vento = funcoes.codificar(vento)
        umidade = funcoes.codificar(umidade)
        
        if (cidade != conforme):
            texto = Frases.cond_comp % ((cidade, conforme, ceu, temperatura, vento, umidade, IUV, observacao))
        else:
            texto = Frases.cond_normal % ((cidade, ceu, temperatura, vento, umidade, IUV, observacao))

        texto = texto.replace('&deg;', '\xba')
        texto = texto.replace('N/D%', 'não tenho idéia')
        texto = texto.replace('N/DºC', 'sei lá')
        texto = texto.replace('N/D km/h', 'pra algum lugar')
        texto = texto.replace('N/D', 'Não Sei')
        texto = texto.replace('N/D', 'Lugar nenhum')
        #link do site com os detalhes
        if detalhes: texto += chr(32) + showlink
        self.Bot.Say(para, texto)

    def ShowWeather(self, local, para, nick, todos, detalhes):
        host = 'http://br.weather.com'
        uri = host + '/search/search?what=WeatherLocalUndeclared&where=' + local.replace(' ', '+').lower()
        dados = web.get(uri, True)
        src = dados[0]
        
        if Tag.inicio_conteudo in src:
            self.weather(src, para, dados[1], detalhes)
        else:
            locais = []
            if not (Tag.titulo in src):
                self.Bot.Say(para, self.msg_rand(Frases.nao_encontrado).replace('%cidade', local) )
            else:
                src = src[src.find(Tag.titulo):]
                while (Tag.link_inicio in src):
                    tag = src.find(Tag.link_fim)
                    item = src[src.find(Tag.link_inicio):tag]
                    locais.append(item[:item.find('"')])
                    src = src[tag+len(Tag.link_fim):]
                if len(locais) == 0: return
                if len(locais) == 1: todos = True
                if not todos:
                    self.Bot.Say(para, Frases.varios_resultados % len(locais))
                else:
                    for link in locais:
                        dados = web.get(host + link, True)
                        self.weather(dados[0], para, dados[1], detalhes)
    
    def tipo_tempo(self, icone_tempo):
            if ('nch.gif'   in icone_tempo): return 'Noite chuvosa'
            elif ('nci.gif' in icone_tempo): return 'Chuva à noite'
            elif ('ncl.gif' in icone_tempo): return 'Noite de céu claro'
            elif ('nnb.gif' in icone_tempo): return 'Noite nublada'
            elif ('ndi.gif' in icone_tempo): return 'NAO DISCPONIVEL'
            elif ('nnv.gif' in icone_tempo): return 'Nevoeiro'
            elif ('npc.gif' in icone_tempo): return 'Pancadas de chuva'
            elif ('npn.gif' in icone_tempo): return 'Parcialmente nublado'
            elif ('/c.gif'  in icone_tempo): return 'Chuva'
            elif ('ch.gif'  in icone_tempo): return 'Chuvoso'
            elif ('ci.gif'  in icone_tempo): return 'Chuvas Isoladas'
            elif ('cl.gif'  in icone_tempo): return 'Céu Claro'
            elif ('cm.gif'  in icone_tempo): return 'Chuva pela manhã'
            elif ('cl.gif'  in icone_tempo): return 'Chuva e Neve'
            elif ('ct.gif'  in icone_tempo): return 'Chuva à tarde'
            elif ('cv.gif'  in icone_tempo): return 'Chuvisco'
            elif ('de.gif'  in icone_tempo): return 'Descargas elétricas'
            elif ('/e.gif'  in icone_tempo): return 'Encoberto'
            elif ('ec.gif'  in icone_tempo): return 'Encoberto com chuvas isoladas'
            elif ('/g.gif'  in icone_tempo): return 'Geada'
            elif ('ge.gif'  in icone_tempo): return 'Gelado'
            elif ('in.gif'  in icone_tempo): return 'Instável'
            elif ('mn.gif'  in icone_tempo): return 'Muitas nuvens'
            elif ('/n.gif'  in icone_tempo): return 'Nublado'
            elif ('nb.gif'  in icone_tempo): return 'Bem Nublado'
            elif ('nd.gif'  in icone_tempo): return ''
            elif ('ne.gif'  in icone_tempo): return 'Neve'
            elif ('np.gif'  in icone_tempo): return 'Nublado e pancada de chuva'
            elif ('nv.gif'  in icone_tempo): return 'Nevoeiro'
            elif ('pc.gif'  in icone_tempo): return 'Pancadas de chuva'
            elif ('pm.gif'  in icone_tempo): return 'Pancadas de chuva pela manhã'
            elif ('pn.gif'  in icone_tempo): return 'Parcialmente nublado'
            elif ('pp.gif'  in icone_tempo): return 'Possibilidade de pancada de chuva'
            elif ('ps.gif'  in icone_tempo): return 'Predomínio de Sol'
            elif ('pt.gif'  in icone_tempo): return 'Pancadas de chuva à tarde'
            elif ('t.gif'   in icone_tempo): return 'Tempestade'
            else: return ''

    def MostrarCidadesEncontradas(self, src, para, busca_original):
        exatos = []
        cidades = {}
        mostrar_cidades = 17
        if self.Bot.SessaoMSN():
            mostrar_cidades = 40
        while (Tag.prev_cidades in src):
            item = self.extrair(src, Tag.prev_cidades, Tag.prev_final_div)
            _id  = self.extrair(item, '&amp;id=', '"')
            cidades[_id] = self.extrair(item, '>', '<')
            src = self.cortar(src, Tag.prev_cidades)
            # Se procurar por "Curitiba" e retornar "Curitiba-PR" ele manda buscar
            if cidades[_id][len(busca_original)] == '-':
                exatos += [_id]
        # Só manda fazer essa procura se tiver apenas um.
        if len(exatos) == 1:    
            self.PrevisaoTempo(exatos[0], para, False, True)
            return
        frase = 'Encontrei %d cidades.. Use \x02 .p -cod \x032[\x02\x031código da cidade que está entre parêntesis\x02\x032]\x02\x031 - Ex: .p -cod 227' % len(cidades)
        self.Bot.Say(para, frase)
        frase = ['%s(%s)' % (cidades[_id], _id) for _id in cidades]
        if len(frase) > mostrar_cidades: frase = frase[:mostrar_cidades]
        frase = 'Cidades: %s' % ', '.join(frase)
        self.Bot.Say(para, frase)
            
    
    def PrevisaoTempo(self, local, para, tudo, por_codigo):
        if por_codigo:
            uri = '/cidades/previsao.do?parameter=tempo&id='+ local
            po = web.criar_pedido('tempo1.cptec.inpe.br', uri, 'http://tempo1.cptec.inpe.br/')
            src = web.socket_send('tempo1.cptec.inpe.br', 80, po, '</body>')
        else:
            parametros = 'parameter=listar&name=' + local.replace(' ', '+')
            po = web.criar_post('tempo1.cptec.inpe.br', '/cidades/previsao.do', 'http://tempo1.cptec.inpe.br/', parametros)            
            src = web.socket_send('tempo1.cptec.inpe.br', 80, po, '</body>')
        charset = 'utf-8'
        if ('charset=' in src):
            charset = self.extrair(src, 'charset=', '\r\n')
        if charset.lower() != 'utf-8':
            src = src.decode(charset).encode('utf-8')
        if 'Location: http://tempo1.cptec.inpe.br/cidades/erro.jsp' in src:
            self.Bot.Say(para, 'Não achei nada.')
            return
        # Até aqui pegou o código, agora vamos tratá-lo
        
        # Parte 1: Verificar se tem algum resultado
        if (Tag.prev_not_found in src):
            self.Bot.Say(para, self.msg_rand(Frases.nao_encontrado).replace('%cidade', local) )
            return            
        # Parte 2: Pegar a lista de cidades encontradas
        if (Tag.prev_cidades in src):
            self.MostrarCidadesEncontradas(src, para, local)
            return
        
        cidade = self.extrair(src, Tag.prev_cidade, Tag.prev_final_div)
        self.Bot.Say(para, 'Previsão para \x02%s\x02' % cidade)
        while Tag.prev_prox_item in src:
            src = self.cortar(src, Tag.prev_prox_item)
            dia = self.extrair(src, Tag.prev_dia, Tag.prev_final_div)
            icone_tempo = self.extrair(src, Tag.prev_icone, '" ')
            temp_min = self.extrair(src, Tag.prev_temp_min, Tag.prev_final_div).strip()
            temp_max = self.extrair(src, Tag.prev_temp_max, Tag.prev_final_div).strip()
            chuva = self.extrair(src, Tag.prev_prob_chuva, Tag.prev_final_lnk).replace(chr(32), '')
            nascer_sol = self.extrair(src, Tag.prev_nascer_sol, Tag.prev_final_div)
            por_sol = self.extrair(src, Tag.prev_iuv_maximo, Tag.prev_final_lnk)
            prev_iuv_maximo = self.extrair(src, Tag.prev_iuv_maximo, Tag.prev_final_div)
            
            nascer_sol = self.remover(nascer_sol, '<', '>').strip()
            por_sol = self.remover(por_sol, '<', '>').strip()
            temp_min = self.remover(temp_min, '<', '>').strip()
            temp_max = self.remover(temp_max, '<', '>').strip()
            
            tempo = self.tipo_tempo(icone_tempo)            
            # Indice de UV http://tempo1.cptec.inpe.br/ind_uv.shtml
            indice_uv = self.extrair(prev_iuv_maximo, 'uv_', '.').strip()
            if indice_uv in ['1','2']: indice_uv += ' \x032Baixo'
            if indice_uv in ['3','4','5']: indice_uv += ' Moderado'
            if indice_uv in ['6','7']: indice_uv += ' \x035Alto'
            if indice_uv in ['8','9','10']: indice_uv += ' \x034Muito Alto'
            if indice_uv in ['11','12','13','14']: indice_uv += ' \x0313\x02Extremo\x02'
            indice_uv = 'IUV: %s' % indice_uv
                
            prev = []
            if (tempo != ''): prev += ['\x032%s\x031' % tempo]
            #if (temp_min != ''): prev += ['Mínima: \x02%s\x02' % temp_min]
            #if (temp_max != ''): prev += ['Máxima: \x02%s\x02' % temp_max]
            if (temp_min == ''): temp_min = '?'
            if (temp_max == ''): temp_max = '?'
            if (temp_min!='?')and(temp_max!='?'): prev += ['(%s-%s)' % (temp_min, temp_max)]            
            if (chuva != ''): prev += ['Vai Chover? \x02%s\x02' % chuva]
            if (nascer_sol != '') and tudo: prev += ['Nascer do Sol: %s' % nascer_sol]
            if (por_sol != '') and tudo: prev += ['Pôr do Sol: %s' % por_sol]
            prev += [indice_uv]
            frase = self.remover(', '.join(prev), '<', '>')
            frase = '%s: %s' % (dia.replace(' - ', chr(32)), frase)
            self.Bot.Say(para, frase)
            
    def ClimaTempo(self, mensagem):
        analise = self.analisar(mensagem)
        cmd = analise['cmd']
        palavra = analise['valor']
        param = analise['param']
        alvo = analise['resposta']
        nick = mensagem['prefix']['nick']    
    
        if not (cmd in self.user_cmds): return
        if (palavra == '') and (param == ''):
            self.Bot.Say(alvo, 'Defina a cidade. Use --help para ver a ajuda.')
            return
            
        if ('help' in param):
            self.ajuda(alvo)
            return       
        if ('IUV' in param):
            if self.Bot.SessaoMSN(): nick = alvo
            self.MostrarIUV(nick)
            return
        todos    = 'a' in param
        detalhes = 'd' in param
        por_codigo= 'cod' in param
        
        if (palavra == ''):
            self.Bot.Say(alvo, 'Defina a cidade. Use --help para ver a ajuda.')
            return        
        
        if (cmd in ['.tempo', '.w']):
            self.ShowWeather(palavra, alvo, nick, todos, detalhes)
        else:
            self.PrevisaoTempo(palavra, alvo, todos, por_codigo)
