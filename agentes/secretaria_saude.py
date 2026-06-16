# arquivo: agentes/secretaria_saude.py

from maspy import *

class AgenteSecretariaSaude(Agent):
    def __init__(self, agent_name, estoque_inicial):
        super().__init__(agent_name)
        self.estoque_central = estoque_inicial
        
        # Correção: Retornados os nomes originais. O MASPY realiza o roteamento automático.
        self.ubs_participantes = ["UBS_Centro", "UBS_ZonaNorte", "UBS_ZonaSul"]
        self.lances_recebidos = [] 

    @pl(gain, Goal("iniciar_distribuicao", Any))
    def disparar_cfp(self, src, quantidade):
        self.print(f"ALERTA: Iniciando protocolo Contract-Net para {quantidade} kits.")
        
        for ubs in self.ubs_participantes:
            self.send(ubs, tell, Belief("cfp", (101, quantidade)), "Canal_SUS")
            self.print(f"-> Mensagem [CFP] enviada para {ubs}")

    # Correção: Alterado para (Any, Any) para corresponder à tupla de dois elementos enviada pelas UBSs
    @pl(gain, Belief("propose", (Any, Any)))
    def receber_proposta(self, src, dados_proposta):
        id_lote, urgencia = dados_proposta
        self.print(f"Proposta recebida de {src} com urgência: {urgencia}")
        
        self.lances_recebidos.append((src, urgencia))

        if len(self.lances_recebidos) == len(self.ubs_participantes):
            self.print("Todos os lances recebidos. Iniciando avaliação...")
            self.add(Goal("avaliar_propostas", id_lote))

    @pl(gain, Goal("avaliar_propostas", Any))
    def avaliar_lances(self, src, id_lote):
        self.lances_recebidos.sort(key=lambda x: x[1], reverse=True)
        
        vencedor, maior_urgencia = self.lances_recebidos[0]
        self.print(f"*** VENCEDOR DA LICITAÇÃO: {vencedor} (Urgência: {maior_urgencia}) ***")

        for ubs, urgencia in self.lances_recebidos:
            if ubs == vencedor:
                self.send(ubs, tell, Belief("accept_proposal", id_lote), "Canal_SUS")
            else:
                self.send(ubs, tell, Belief("reject_proposal", id_lote), "Canal_SUS")
        
        self.lances_recebidos.clear()