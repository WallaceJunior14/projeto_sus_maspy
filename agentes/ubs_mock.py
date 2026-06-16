# arquivo: agentes/ubs_mock.py

from maspy import *
import random 

class AgenteUBSMock(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)

    # Correção: Estruturado como (Any, Any) para realizar o casamento de padrões com a tupla enviada pela Secretaria
    @pl(gain, Belief("cfp", (Any, Any)))
    def receber_cfp(self, src, dados_cfp):
        id_lote, quantidade = dados_cfp
        
        urgencia_mock = round(random.uniform(0.1, 0.9), 4)
        self.print(f"Calculando urgência e enviando proposta: {urgencia_mock}")
        
        self.send(src, tell, Belief("propose", (id_lote, urgencia_mock)), "Canal_SUS")

    # Como as mensagens de aceitação/rejeição passam um único valor de ID, o uso de Any isolado é válido
    @pl(gain, Belief("accept_proposal", Any))
    def venceu_licitacao(self, src, id_lote):
        self.print("SUCESSO: Minha proposta foi ACEITA. Aguardando logística de transporte.")

    @pl(gain, Belief("reject_proposal", Any))
    def perdeu_licitacao(self, src, id_lote):
        self.print("REJEITADO: Insumos alocados para uma unidade mais crítica.")