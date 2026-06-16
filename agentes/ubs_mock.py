# arquivo: agentes/ubs_mock.py

from maspy import *

class AgenteUBSMock(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)

    # O uso do Any captura a tupla inteira enviada pela Secretaria
    @pl(gain, Belief("cfp", Any))
    def receber_cfp(self, src, dados_cfp):
        # Desempacotamento da tupla (101, 500) em variáveis locais
        id_lote, quantidade = dados_cfp
        
        self.print(f"Mensagem [CFP] recebida de {src}!")
        self.print(f"  -> Lote ID: {id_lote}")
        self.print(f"  -> Quantidade ofertada: {quantidade}")