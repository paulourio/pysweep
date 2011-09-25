#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""Módulo de conexão à rede IRC

Módulo: Ident
Autor: Vindemiatrix Almuredin
Blog: tocadoelfo.blogspot.com

Descrição: Módulo que implementa um servidor de Ident Completo, segundo a RFC 1413

BNF do Protocolo (RFC 1413)

### Em Desenvolvimento ###

"""

import socket, time, string
from threading import Thread

class Ident(Thread):
    pass

class IdentClient(Thread):
    def __init__(self, socket, resposta='user', sistema='UNIX', ):
        Thread.__init__(self)
        self.sock = socket
        self.resposta = resposta
        self.sistema = sistema

    def run(self):
        req = self.sock.recv(1024)
        if req.find('\r'):
            req = req[:req.find('\r')]
        elif req.find('\n'):
            req = req[:req.find('\n')]
        self.sock.sendall('%s : USERID : %s : %s\n' % (req, self.sistema, self.resposta))
        self.sock.shutdown(2)
        self.sock.close()
