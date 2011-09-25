#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Módulo pra facilitar a implementação de módulos que usam protocolos HTTP
#
import urllib, socket

def get(uri, return_url=False): 
    u = urllib.urlopen(uri)
    bytes = u.read()
    url = u.geturl()
    u.close()
    if return_url: return [bytes, url]
    else: return bytes
   
def head(uri): 
    u = urllib.urlopen(uri)
    info = u.info()
    u.close()
    return info

def post(uri, query): 
    data = urllib.urlencode(query)
    u = urllib.urlopen(uri, data)
    bytes = u.read()
    u.close()
    return bytes
   
def criar_pedido(host, uri, referer=''):
    pedido=['GET %s HTTP/1.1\r\n'
            'Host: %s\r\n'
            'User-Agent: Mozilla/5.0 (Sweep)\r\n'
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
            'Accept-Language: pt,en-us;q=0.7,en;q=0.3\r\n'
            'Accept-Charset: utf-8;q=0.7,*;q=0.7\r\n'
            'Keep-Alive: 300\r\n'
            'Connection: keep-alive\r\n' % (uri, host)][0]
    if (referer != ''):
            pedido += 'Referer: %s\r\n' % referer
    return pedido + '\r\n'
            
def criar_post(host, uri, referer, conteudo):
    return ['POST %s HTTP/1.1\r\n'
            'Host: %s\r\n'
            'User-Agent: Mozilla/5.0 (Sweep)\r\n'
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
            'Accept-Language: pt,en-us;q=0.7,en;q=0.3\r\n'
            'Accept-Charset: utf-8;q=0.7,*;q=0.7\r\n'
            'Keep-Alive: 300\r\n'
            'Connection: keep-alive\r\n'
            'Referer: %s\r\n'
            'Content-Type: application/x-www-form-urlencoded\r\n'
            'Content-Length: %d\r\n\r\n'
            '%s' % (uri, host, referer, len(conteudo), conteudo)][0]
                           
def socket_send(host, porta=80, dados='', fim='</body>'):
    fSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        fSocket.connect((host, porta))
        msg = dados
        tamanho_msg = len(dados)
        total_enviado = 0
        # Enviar dados
        while total_enviado < tamanho_msg:
            enviado = fSocket.send(msg[total_enviado:])
            if enviado == 0: raise
            total_enviado += enviado
        resposta = ''
        # Receber dados
        while not (fim.lower() in resposta.lower()):
            bytes = fSocket.recv(128)
            if len(bytes) == 0: break
            resposta += bytes
        fSocket.close()
        return resposta
    except:
        return None
