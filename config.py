#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Arquivo de configuração do bot sweep           
#    
# Para efetuar algumas mudancas eh necessário
# reiniciar o bot. 
#                                
# Variáveis de plugins tambem ficam neste     
# arquivo.                                    
#                                                

bot_version = '1.4.5'

# Os valores "mynick", "user", "real_name" se 
# encaixam nesta sintaxe:
#       mynick!n=user@host real_name

# Nick do bot
#      Nick para o bot usar.
# Obs: Se o plugin recover.py estiver ativo
#      e o mynick esteja on, o bot envia
#      "NickServ GHOST <mynick> <senha>" 
#      para tentar derrubar e recupera-lo.
# Exemplo:
#      mynick = 'Sweep'
mynick = 'spp-dev'

# Nick secundário
#      Este nick eh usado apenas pelo recover.py
#      que utiliza este nick caso o mynick esteja 
#      em uso. Se ele nao conseguir recupera-lo 
#      permanecera com o nick secundario.
#      (Nao ha suporte de senha para o nick secundario)
# Exemplo:
#      second_nick = 'Sweep2'
second_nick = 'spp-dev-2'

# User 
#       Não pode ter espaços
# Exemplo:
#       user = 'user'
user = 'FAIL'

# Nome real 
#       Pode ter espacos
# Exemplo:
#       real_name = 'Nome Real'
real_name = 'Quer ajuda? Envie /msg %s help' % mynick

# VERSION
#       Texto para responder ao comando CTCP Version
# Exemplo:
#       version_rsp = 'Sweep Bot v1.0'
version_rsp = 'Sweep Pythons Project Bot v%s escrito por JimmySkull. Sweep esta sob a Lincenca FAIL: http://rthorstein.co.cc/fail/FAIL.txt' % bot_version

# Senha do NickServ
# Exemplo:
#       senha = 'senha_do_nick'
senha = 'passwrd'

# Mensagem de saída do bot
quit_msg = 'Bye Bye'

# Senhas de admins
#       Tipo: list
#       Para mais senhas separe cada senha com virgula. 
# Exemplo:
#       senhas_admin = ['senha1','senha2','senha3']
senhas_admin = ['g9hq5_0;56@'] 

# Canais para entrar
#       Para mais de um canal, separe-os com virgula
# Exemplo:
#       canais = '#help,#linux'
canais = '##x'

# Rede IRC para conectar
# Exemplo:
#       network = 'irc.freenode.net'
network = 'irc.freenode.net'

# Porta de conexao
# Exemplo:
#       port = 2727
porta = 6667

# Time Out do Socket
# Exemplo:
#     time out de 6 minutos
#       time_out = 360
time_out = 260

# Arquivo de histórico
# Só deixe habilitado o log_file se o valor
# não estiver vazio.
# log_file = 'historico.txt'

# Tentar reconectar caso de erro de socket
# Use True (para verdadeiro) ou False (para falso)
# Exemplo:
#       tentar_reconectar = True
tentar_reconectar = True

# Tempo de espera entre cada tentativa
# De um valor inteiro, o delay eh em segundos
# Exemplo:
#       reconnect_delay = 60
reconnect_delay = 60

# Configuração para o plugin de MSN
#
# Estas configurações serão aplicadas se o parâmetro "-msn"
# seja passado na linha de comando.
msn_nick     = 'Doritos'
msn_email    = 'sweep@msn.com'
msn_senha    = ''
msn_time_out = 500
msn_delay1   = 0.1
msn_delay2   = 0
            
#eof
