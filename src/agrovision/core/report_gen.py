import json
import os
from datetime import datetime

from fpdf import FPDF

# Single source of truth for the output filename.
# VRA.py uses this constant to build the download path so both sides
# stay in sync even if the name changes in the future.
PDF_FILENAME = "Relatorio_AgroVision.pdf"


class AgroReport(FPDF):
    def header(self):
        # Barra Verde de Topo
        self.set_fill_color(46, 125, 50)  # Verde Floresta
        self.rect(0, 0, 210, 30, "F")

        # Título Brando no Topo
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "RELATÓRIO TÉCNICO DE PRESCRIÇÃO VRA", 0, 0, "C")
        self.ln(7)
        self.set_font("Arial", "", 10)
        self.cell(
            0,
            10,
            f"AgroVision AI - Inteligência Geográfica | {datetime.now().strftime('%d/%m/%Y')}",
            0,
            0,
            "C",
        )
        self.ln(20)

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        # Linha de separação
        self.line(10, 280, 200, 280)
        self.cell(
            0,
            10,
            f"Página {self.page_no()} | Gerado por AgroVision - Tecnologia YOLOv12",
            0,
            0,
            "L",
        )
        self.cell(0, 10, "Contato: agrovision.ai@suporte.com", 0, 0, "R")


def create_pdf_report(report_dir: str, client_name: str = "Cliente Especial") -> str:
    """Generates the professional PDF report and returns its absolute path.

    Args:
        report_dir:  Directory that contains metrics.json and the chart PNGs
                     produced by generate_report_material(). Created here if
                     it does not exist yet (defensive guard).
        client_name: Client name printed in the identification block.
    """
    os.makedirs(report_dir, exist_ok=True)

    metrics_path = os.path.join(report_dir, "metrics.json")
    with open(metrics_path) as f:
        metrics = json.load(f)

    # Configuração do Documento
    pdf = AgroReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- BLOCO 1: IDENTIFICAÇÃO ---
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"CLIENTE: {client_name.upper()}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, "Área Analisada: Fazenda Santo Antônio (Processamento Big Data)", ln=True)
    pdf.ln(5)

    # --- BLOCO 2: DASHBOARD DE MÉTRICAS (CARDS) ---
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, 55, 190, 35, "F")  # Fundo cinza claro para o dashboard

    pdf.set_y(60)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(63, 5, "ÁREA TOTAL", 0, 0, "C")
    pdf.cell(63, 5, "ÁREA APLICADA", 0, 0, "C")
    pdf.cell(63, 5, "ECONOMIA REAL", 0, 1, "C")

    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(33, 33, 33)
    pdf.cell(63, 15, f"{metrics['total_ha']:.2f} ha", 0, 0, "C")
    pdf.set_text_color(183, 28, 28)  # Vermelho
    pdf.cell(63, 15, f"{metrics['sprayed_ha']:.2f} ha", 0, 0, "C")
    pdf.set_text_color(46, 125, 50)  # Verde
    pdf.cell(63, 15, f"{metrics['economy_pct']:.1f}%", 0, 1, "C")

    pdf.ln(15)

    # --- BLOCO 3: MAPA DE PRESCRIÇÃO ---
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. MAPA DE PRESCRIÇÃO VRA (GRELHA)", ln=True)

    map_path = os.path.join(report_dir, "mapa_estatico_prescricao.png")
    if os.path.exists(map_path):
        # Tenta centralizar o mapa
        pdf.image(map_path, x=15, y=None, w=180)

    pdf.add_page()

    # --- BLOCO 4: IMPACTO FINANCEIRO ---
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. IMPACTO ECONÔMICO ESTIMADO", ln=True)

    # Gráfico de Pizza
    econ_path = os.path.join(report_dir, "grafico_economia.png")
    if os.path.exists(econ_path):
        pdf.image(econ_path, x=55, y=None, w=100)

    pdf.ln(5)
    pdf.set_font("Arial", "", 11)

    # Cálculo Simulado de ROI (Exemplo: R$ 150,00 por hectare de produto)
    custo_ha = 150.00
    total_gasto_convencional = metrics["total_ha"] * custo_ha
    total_gasto_agrovision = metrics["sprayed_ha"] * custo_ha
    poupanca = total_gasto_convencional - total_gasto_agrovision

    pdf.set_fill_color(232, 245, 233)
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(
        0,
        10,
        f"ESTIMATIVA DE ECONOMIA: Com base no custo médio de R$ {custo_ha:.2f}/ha, esta operação gerou uma poupança estimada de R$ {poupanca:.2f} para o produtor.",
        border=1,
        align="C",
        fill=True,
    )

    # --- BLOCO 5: ISENÇÃO ---
    pdf.set_y(-50)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0,
        5,
        "AVISO: Este relatório é baseado em processamento de imagens via IA. A eficácia da aplicação depende da calibração do equipamento (drone/trator) e das condições meteorológicas no momento da pulverização. Georreferenciamento verificado via Metadados Nativos.",
    )

    output_pdf = os.path.join(report_dir, PDF_FILENAME)
    pdf.output(output_pdf)
    return output_pdf
