# arquivo: agentes/frota_logistica.py
from maspy import *

class AgenteFrotaLogistica(Agent):
    def __init__(self, agent_name, x_inicial, y_inicial, custo_km):
        super().__init__(agent_name)
        self.x = x_inicial
        self.y = y_inicial
        self.custo_km = custo_km
        self.status = "Livre"

    @pl(gain, Belief("cfp_transporte", (Any, Any, Any)))
    def receber_cfp_transporte(self, src, dados_transporte):
        id_transporte, dest_x, dest_y = dados_transporte
        
        if self.status == "Livre":
            distancia = ((self.x - dest_x)**2 + (self.y - dest_y)**2)**0.5
            custo_estimado = round(distancia * self.custo_km, 2)
            
            self.print(f"Calculando frete para rota até [{dest_x}, {dest_y}]. Custo Estimado: R$ {custo_estimado}")
            self.send(src, tell, Belief("propose_transporte", (id_transporte, custo_estimado)), "Canal_SUS")

    @pl(gain, Belief("accept_transport", Any))
    def transporte_aceito(self, src, id_transporte):
        self.status = "Ocupado"
        self.print(f" PROPOSTA ACEITA! Veículo coletando carga e iniciando deslocamento do lote {id_transporte}.")