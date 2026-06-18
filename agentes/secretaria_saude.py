# arquivo: agentes/secretaria_saude.py
from maspy import *

class AgenteSecretariaSaude(Agent):
    def __init__(self, agent_name, estoque_inicial):
        super().__init__(agent_name)
        self.estoque_central = estoque_inicial
        self.ubs_participantes = ["UBS_Centro", "UBS_ZonaNorte", "UBS_ZonaSul"]
        self.lances_recebidos = [] 
        
        #  --- VARIÁVEIS DA FASE 2 (Nativas e simplificadas sem conflito de underscore) ---
        self.lista_frota = ["Fiorino01", "Caminhao02"]
        self.mapa_coordenadas = {
            "UBS_Centro": (15, 42),
            "UBS_ZonaNorte": (60, 80),
            "UBS_ZonaSul": (10, 5)
        }
        self.lances_transporte = []

    @pl(gain, Goal("iniciar_distribuicao", Any))
    def disparar_cfp(self, src, quantidade):
        self.print(f"ALERTA: Iniciando protocolo Contract-Net para {quantidade} kits.")
        for ubs in self.ubs_participantes:
            self.send(ubs, tell, Belief("cfp", (101, quantidade)), "Canal_SUS")
            self.print(f"-> Mensagem [CFP] enviada para {ubs}")

    @pl(gain, Belief("propose", (Any, Any)))
    def receber_proposta(self, src, dados_proposta):
        id_lote, urgencia = dados_proposta
        self.print(f"Proposta recebida de {src} com urgência: {urgencia}")
        self.lances_recebidos.append((src, urgencia))

        if len(self.lances_recebidos) == len(self.ubs_participantes):
            self.print("Todos os lances de urgência recebidos. Iniciando avaliação...")
            self.add(Goal("avaliar_propostas", id_lote))

    @pl(gain, Goal("avaliar_propostas", Any))
    def avaliar_lances(self, src, id_lote):
        self.lances_recebidos.sort(key=lambda x: x[1], reverse=True)
        vencedor, maior_urgencia = self.lances_recebidos[0]
        
        nome_ubs_vencedora = str(vencedor).split('_')[0] + "_" + str(vencedor).split('_')[1]
        self.print(f"*** VENCEDOR DA LICITAÇÃO: {nome_ubs_vencedora} (Urgência: {maior_urgencia}) ***")

        for ubs, urgencia in self.lances_recebidos:
            if ubs == vencedor:
                self.send(ubs, tell, Belief("accept_proposal", id_lote), "Canal_SUS")
            else:
                self.send(ubs, tell, Belief("reject_proposal", id_lote), "Canal_SUS")
        
        self.lances_recebidos.clear()

        dest_x, dest_y = self.mapa_coordenadas[nome_ubs_vencedora]
        self.print(f"Iniciando Fase 2: Contratação de frete autônomo para {nome_ubs_vencedora} em [{dest_x}, {dest_y}]")
        
        # Envia o CFP de transporte para os veículos cadastrados
        for veiculo in self.lista_frota:
            self.send(veiculo, tell, Belief("cfp_transporte", (id_lote, dest_x, dest_y)), "Canal_SUS")

    @pl(gain, Belief("propose_transporte", (Any, Any)))
    def receber_proposta_transporte(self, src, dados_transporte):
        id_lote, custo_estimado = dados_transporte
        self.print(f"Proposta de frete recebida de {src}: R$ {custo_estimado}")
        
        self.lances_transporte.append((src, custo_estimado))

        if len(self.lances_transporte) == len(self.lista_frota):
            self.print("Todas as propostas logísticas recebidas. Escolhendo menor custo...")
            self.add(Goal("alocar_transporte", id_lote))

    @pl(gain, Goal("alocar_transporte", Any))
    def avaliar_transporte(self, src, id_lote):
        self.lances_transporte.sort(key=lambda x: x[1])
        veiculo_vencedor, menor_custo = self.lances_transporte[0]
        
        nome_veiculo_vencedor = str(veiculo_vencedor).split('_')[0]
        self.print(f" LOGÍSTICA CONTRATADA: {nome_veiculo_vencedor} realizará a entrega por R$ {menor_custo}")
        
        self.send(veiculo_vencedor, tell, Belief("accept_transport", id_lote), "Canal_SUS")
        self.lances_transporte.clear()