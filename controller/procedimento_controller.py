import os
from h2o_wave import Q, ui, on
from controller import relatorio_controller
from log import log
from config import app_config


@on("init")
async def init(q: Q) -> None:
    q.page["left_content"] = ui.form_card(box=ui.box(zone="left_content"), items=[])

    q.client.city_options = [
        "São Paulo",
        "Rio de Janeiro",
        "Belo Horizonte",
        "Salvador",
        "Brasília",
        "Curitiba",
        "Fortaleza",
        "Recife",
        "Porto Alegre",
        "Manaus",
        "Belém",
        "Goiânia",
        "Florianópolis",
        "Vitória",
        "Natal",
        "Cuiabá",
        "João Pessoa",
        "Campo Grande",
        "São Luís",
        "Teresina",
    ]

    await select_cidade(q)


@on("select_cidade")
async def select_cidade(q: Q):
    """Exibe a cidade selecionada após a escolha."""

    if q.args.select_cidade:
        q.client.selected_cidade = q.args.select_cidade

    q.page["left_content"].items = [
        ui.dropdown(
            name="select_cidade",
            label="Selecione uma cidade",
            choices=[
                ui.choice(name=cidade, label=cidade) for cidade in q.client.city_options
            ],
            required=True,
            trigger=True,
            value=q.client.selected_cidade,
        )
    ]

    if q.client.selected_tab == "relatorio":
        await relatorio_controller.relatorio_page(q)
