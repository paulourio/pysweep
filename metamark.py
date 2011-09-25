#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web

class XrlUS():        
    ''' Criar links curtos para economizar espaço. '''
    def __init__(self):
        pass
        
    def doPost(self, longURL):
    	return web.post('http://metamark.net/add', {'long_url': longURL})
                
    def getUrl(self, longUrl):
        codigo = self.doPost(longUrl)
        # Se der algum erro, retorna a url original
        if (' ERROR: ' in codigo):
            return [longUrl, '100%']
        # Pega o resultado
        codigo = codigo[:codigo.find('of the original length')]
        codigo = codigo[codigo.rfind('">')+2:]
        # Extrai link e porcentagem
        link   = codigo[:codigo.find('</a> (')]
        percent= codigo[codigo.find('a>')+4:].strip()
        return [link, percent]
