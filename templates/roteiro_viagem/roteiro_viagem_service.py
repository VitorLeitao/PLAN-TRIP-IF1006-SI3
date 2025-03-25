from datetime import datetime
from h2o_wave import main, app, Q, ui, on, run_on, data
from jinja2 import Environment, FileSystemLoader
from .roteiro_viagem_config import config
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from ..report_service import get_secao
from log import log, setup_logger


async def get_html(q: Q):
    log.info(
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    )
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("roteiro_viagem/roteiro_viagem.html")

    html = template.render(await get_data(q))

    return html


async def get_data(q: Q):
    return {
        "roteiro": await get_secao(q, "roteiro", config),
    }


def get_header_doc(doc, q):
    img_paragraph = doc.add_paragraph()
    run = img_paragraph.add_run()
    img_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return doc
