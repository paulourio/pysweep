#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, optparse, sys

def LimpaString(Texto, Caracter = ''):
    '''
    Esta função para retirada dos caracteres de cor se baseia em um autômato construído
    para este propósito, utilizando-se dos conceitos da Máquina de Turing.

    Correção do código:
    Para que tudo ocorra da maneira correta, em vez de deletarmos diretamente na máquina
    empilhamos cada posição e seu relativo tamanho para, depois de finalizado o autômato,
    efetuarmos a deleção dos caracteres de cor, desempilhando-os.

    To-do: Corrigir a implementação do laço de repetição que ocasiona na não exclusão de um
    marcador de cor propositalmente escrito de maneira incorreta, no final da string.
    Corrigido: Substituído Laço For por Laço While para permitir teste de condições de parada
    da repetição

    To-do: Analizar a função para identificar possíveis falhas exploráveis como Overflow
    Underflow e outros tipos de ataques baseados em buffer
    Corrigido: Não houve necessidade de mudança no código pois a verificação de tamanho
    no laço While resolveu o problema da string vazia

    A Expressão pode ser entendida como: <#3 [num [num] [,[num [num]]]>

    Licenciado sob FAIL.
    '''
    Str = Texto[:]
    Pos = -1
    Tam = -1
    Estado = 1
    Tamanho = len(Str)
    Pilha = []

    I = 0

    while (I <= Tamanho) or (Estado <> 1):

        Char = Str[I:I+1]
       
        if Estado == 1: #Estado atual: 1; Verifica caracter #3
            if Char in ('\x03',):
                Pos = I
                Tam = 1
                Estado = 2
                I += 1
            elif Char in [chr(x) for x in range(1, 32)]:
                #Explicação: Todos os caracteres entre #1 e #31 são considerados caracteres de controle,
                #por isto estes normalmente não aparecem em mensagens e podem ser excluídos
                #sem risco à interpretação da mensagem.
                #Os caracteres de 32 à 127 e os ASCII extendidos são os caracteres de input normais.
               
                Pos = I
                Tam = 1
                I += 1
                Pilha.append({'Pos': Pos, 'Tam': Tam})
            else:
                I += 1
                
        elif Estado == 2: #Estado atual: 2; Verifica primeiro caracter <num>
            if Char in [str(x) for x in range(0, 10)]:
                Tam += 1
                Estado = 3
                I += 1
            else:
                Estado = 1                
                Pilha.append({'Pos': Pos, 'Tam': Tam})
                
        elif Estado == 3: #Estado atual: 3; Verifica caracteres <num> ou ","
            if Char in [str(x) for x in range(0, 10)]:
                Tam += 1
                Estado = 4
                I += 1
            elif Char in [',']:
                Tam += 1
                Estado = 5
                I += 1
            else:
                Estado = 1
                Pilha.append({'Pos': Pos, 'Tam': Tam})
                
        elif Estado == 4: #Estado Atual: 4; Verifica caracter ","
            if Char in [',']:
                Tam += 1
                Estado = 5
                I += 1
            else:
                Estado = 1
                Pilha.append({'Pos': Pos, 'Tam': Tam})
                
        elif Estado == 5: #Estado Atual 5; Verifica caracter <num>
            if Char in [str(x) for x in range(0, 10)]:
                Tam += 1
                Estado = 6
                I += 1
            else:
                Estado = 1
                Tam -= 1 #Se não houver número depois da virgula, significa que é uma vírgula normal
                Pilha.append({'Pos': Pos, 'Tam': Tam})
                
        elif Estado == 6: #Estado Atual 6; Verifica caracter <num>
            if Char in [str(x) for x in range(0, 10)]:
                Tam += 1
                Estado = 1
                Pilha.append({'Pos': Pos, 'Tam': Tam})
            else:
                Estado = 1
                Pilha.append({'Pos': Pos, 'Tam': Tam})

    while len(Pilha) > 0:
        Cor = Pilha.pop()
        Str = Str[:Cor['Pos']] + Str[Cor['Pos']+Cor['Tam']:]
 
    return Str


def LimparIRCTags(arquivo, arquivo_saida):
    f = open(arquivo, 'r')
    w = open(arquivo_saida, 'w')
    for line in f:
        w.write(LimpaString(line) + '\n')
    f.close()
    w.close()

def main():
    parser = optparse.OptionParser('%prog -f arquivo -o output')
    parser.add_option("-f", "--file", dest="file", help="Arquivo de leitura com tags de IRC", metavar="ARQ")
    parser.add_option("-o", "--out", dest="out", help="Arquivo de saida sem as tags", metavar="ARQ")
    (opts, args) = parser.parse_args(sys.argv)
    if (opts.file == None) or (opts.out == None):
        print 'Veja a ajuda com --help'
        return
    if not os.path.exists(opts.file):
        print 'Defina o arquivo de leitura!'
        return
    if os.path.exists(opts.out):
        print 'Defina o arquivo de saida que nao exista!'
        return
    LimparIRCTags(opts.file, opts.out)
           
if __name__ == '__main__':
    try:   
        main()
    except KeyboardInterrupt, v:
        print 'Cancelado.'

