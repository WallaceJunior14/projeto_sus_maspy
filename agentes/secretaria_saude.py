# arquivo: agentes/secretaria_saude.py

from maspy import *

class AgenteSecretariaSaude(Agent):
    def __init__(self, agent_name, estoque_inicial):
        super().__init__(agent_name)
        self.estoque_central = estoque_inicial
        self.ubs_participantes = ["UBS_Centro", "UBS_ZonaNorte", "UBS_ZonaSul"]

    # Plano executado quando o agente ganha o Goal "iniciar_distribuicao"
    @pl(gain, Goal("iniciar_distribuicao", Any))
    def disparar_cfp(self, src, quantidade):
        self.print(f"ALERTA: Iniciando protocolo Contract-Net para {quantidade} kits.")
        
        for ubs in self.ubs_participantes:
            # Envia uma crença (tell) chamada "cfp" contendo o ID do lote e a quantidade
            self.send(ubs, tell, Belief("cfp", (101, quantidade)), "Canal_SUS")
            self.print(f"-> Mensagem [CFP] enviada para {ubs}")