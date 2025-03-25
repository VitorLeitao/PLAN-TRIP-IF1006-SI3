from datetime import datetime
from h2o_wave import main, app, Q, ui, on, run_on, data
from jinja2 import Environment, FileSystemLoader
from .informacoes_viagem_detalhada_config import config
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from ..report_service import get_secao
from log import log, setup_logger


async def get_html(q: Q):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(
        "informacoes_viagem_detalhada/informacoes_viagem_detalhada.html"
    )

    html = template.render(await get_data(q))

    return html


async def get_data(q: Q):
    data = datetime.now().strftime("%d/%m/%Y")
    return {
        "resumo": await get_secao(q, "resumo", config),
        "atrações": await get_secao(q, "atrações", config),
        "refeições": await get_secao(q, "refeições", config),
    }


def get_header_doc(doc, q):
    img_paragraph = doc.add_paragraph()
    run = img_paragraph.add_run()
    img_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return doc
