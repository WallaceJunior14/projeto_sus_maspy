# arquivo: agentes/ubs.py
from maspy import *

class AgenteUBS(Agent):
    def __init__(self, agent_name, populacao, casos_24h, estoque_local):
        super().__init__(agent_name)
        self.populacao = populacao
        self.casos_24h = casos_24h
        self.estoque_local = estoque_local

    def calcular_urgencia(self):
        """
        Calcula o Índice de Urgência com base na fórmula epidemiológica oficial:
        Urgência = (Casos Suspeitos / População) * (1 / (Estoque Local + 1))
        """
        if self.populacao <= 0:
            return 0.0
            
        taxa_ataque = self.casos_24h / self.populacao
        fator_escassez = 1 / (self.estoque_local + 1)
        return round(taxa_ataque * fator_escassez, 4)

    @pl(gain, Belief("cfp", (Any, Any)))
    def receber_cfp(self, src, dados_cfp):
        # Desempacota o ID do lote e a quantidade enviada pela Secretaria
        id_lote, quantidade = dados_cfp
        
        # Calcula a urgência real usando os dados do estado interno
        urgencia_real = self.calcular_urgencia()
        
        self.print(f"Calculando urgência real com base nos dados locais. Resultado: {urgencia_real}")
        
        # Responde à Secretaria com a proposta contendo a urgência calculada
        self.send(src, tell, Belief("propose", (id_lote, urgencia_real)), "Canal_SUS")

    @pl(gain, Belief("accept_proposal", Any))
    def venceu_licitacao(self, src, id_lote):
        self.print(f"SUCESSO: Minha proposta para o lote {id_lote} foi ACEITA. Aguardando logística de transporte.")

    @pl(gain, Belief("reject_proposal", Any))
    def perdeu_licitacao(self, src, id_lote):
        self.print(f"REJEITADO: Insumos do lote {id_lote} alocados para uma unidade mais crítica.")