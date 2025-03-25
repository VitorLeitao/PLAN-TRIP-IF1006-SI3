import importlib
import uuid
from h2o_wave import Q, ui, on, run_on
from templates.word_template import WordTemplate
from .utils import show_long_process_dialog, close_long_process_dialog
from log import log
from config import app_config


@on("relatorio_page")
@on("#relatorio_page")
async def relatorio_page(q: Q):

    log.info("************************************")
    log.info(q.client.selected_cidade)

    q.client.selected_tab = "relatorio"
    q.client.selected_relatorio = "informacoes_viagem_detalhada"

    if not q.client.selected_cidade:
        # Exibo a msg Por favor, selecione um procedimento.
        q.page["right_content"] = ui.markdown_card(
            box=ui.box(zone="right_content", size="100%"),
            title="",
            data=q.client.relatorio,
            content="Por favor, selecione uma cidade.",
        )

        return
    # Pego os possiveis tipos de relatorios a serem gerados
    tipos_relatorio = []
    for relatorio in app_config["relatorios"].split(","):
        log.info("**********************")
        log.info(relatorio)
        module = importlib.import_module(f"templates.{relatorio}.{relatorio}_config")
        tipos_relatorio.append(ui.choice(name=relatorio, label=module.config["titulo"]))

    q.page["right_content"] = ui.form_card(
        box=ui.box(zone="right_content", size="100%"),
        items=[
            ui.dropdown(
                name="selected_relatorio",
                label="Selecione o Relatório a ser gerado",
                choices=tipos_relatorio,
                required=True,
                width="50%",
                value=tipos_relatorio[0].name,
            ),
            ui.button(name="form", label="Avançar"),
        ],
    )


@on("form")
async def simple_side_bar(q: Q):

    q.client.selected_relatorio = q.args.selected_relatorio

    items = []

    items.append(
        ui.inline(
            items=[
                ui.date_picker(name="data_chegada", label="Data de Chegada"),
                ui.date_picker(name="data_saida", label="Data de Saída"),
            ]
        )
    )

    items.append(
        ui.choice_group(
            name="preferencia_tempo",
            label="Você prefere atividades Noturnas ou Diurnas?",
            inline=True,
            choices=[
                ui.choice("noturnas", "Noturnas"),
                ui.choice("diurnas", "Diurnas"),
                ui.choice("todos os tipos", "Todos os tipos"),
            ],
        )
    )

    items.append(
        ui.choice_group(
            name="tipo_experiencia",
            label="Que tipo de experiência você procura?",
            inline=True,
            choices=[
                ui.choice("aventura", "Aventura"),
                ui.choice("cultural", "Cultural"),
                ui.choice("relaxamento", "Relaxamento"),
                ui.choice("festa", "Festa"),
            ],
        )
    )

    items.append(
        ui.choice_group(
            name="companhia_viagem",
            label="Com quem você estará viajando?",
            inline=True,
            choices=[
                ui.choice("sozinho", "Sozinho"),
                ui.choice("casal", "Casal"),
                ui.choice("familia", "Família"),
                ui.choice("amigos", "Amigos"),
            ],
        )
    )

    items.append(
        ui.choice_group(
            name="meio_transporte",
            label="Qual será seu meio de transporte principal no destino?",
            inline=True,
            choices=[
                ui.choice("a_pe", "A pé"),
                ui.choice("transporte_publico", "Transporte público"),
                ui.choice("carro_alugado", "Carro alugado"),
                ui.choice("bike", "Bicicleta"),
                ui.choice("outro", "Outro"),
            ],
        )
    )

    items.append(
        ui.choice_group(
            name="frequencia_deslocamento",
            label="Prefere explorar uma única região ou conhecer vários pontos diferentes?",
            inline=True,
            choices=[
                ui.choice("fixo", "Ficar em uma região fixa e explorar com calma"),
                ui.choice("diversos", "Conhecer o máximo de lugares possível"),
            ],
        )
    )

    items.append(ui.button(name="gerar_relatorio", label="Confirmar"))

    q.page["meta"].side_panel = ui.side_panel(
        title="Escolha suas preferências:",
        name="painel_formulario",
        closable=True,
        events=["dismissed"],
        items=items,
    )


@on("gerar_relatorio")
async def gerar_relatorio(q: Q):
    q.page["meta"].side_panel = None

    await show_long_process_dialog(
        q,
        "Gerando relatório",
        [ui.progress(label="", caption="Perguntando à LLM...")],
    )

    content = await importlib.import_module(
        f"templates.{q.client.selected_relatorio}.{q.client.selected_relatorio}_service"
    ).get_html(q)

    await close_long_process_dialog(q)

    log.info("Save word template.")
    word_template = WordTemplate()
    word_doc = await word_template.convert(q, content)
    docx_uuid = str(uuid.uuid4().int)[:10]
    docx_path = f"{app_config['storage_dir']}/downloads/.docx"
    word_doc.save(docx_path)

    (download_path,) = await q.site.upload([docx_path])

    q.client.relatorio_card = ui.form_card(
        box=ui.box(zone="right_content"),
        items=[
            ui.inline(
                items=[
                    ui.button(name="relatorio_page", label="Voltar"),
                    ui.link(
                        label="Baixar relatório",
                        path=download_path,
                        download=True,
                        button=True,
                    ),
                ]
            ),
            ui.text(content),
        ],
    )

    q.page["right_content"] = q.client.relatorio_card
    await q.page.save()
