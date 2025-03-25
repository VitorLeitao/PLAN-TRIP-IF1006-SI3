import traceback
import os
from h2o_wave import main, app, Q, ui, on, run_on
from controller import relatorio_controller, procedimento_controller
from controller.utils import (
    close_long_process_dialog,
    render_error_page,
    show_long_process_dialog,
)
from log import log, setup_logger
from config import app_config
from gpt_mock_client import GPTMockClient
from gpt_client import GPTClient


async def init_layout(q: Q) -> None:

    layouts = [
        ui.layout(
            breakpoint="xs",
            zones=[
                ui.zone("header", size="14%"),
                ui.zone(
                    "content",
                    direction=ui.ZoneDirection.ROW,
                    size="79%",
                    zones=[
                        ui.zone("left_content", size="40%"),
                        ui.zone("right_content", size="60%"),
                    ],
                ),
                ui.zone(name="footer", size="7%"),
            ],
        ),
        ui.layout(
            breakpoint="1500px",
            zones=[
                ui.zone("header", size="10%"),
                ui.zone(
                    "content",
                    direction=ui.ZoneDirection.ROW,
                    size="80%",
                    zones=[
                        ui.zone("left_content", size="40%"),
                        ui.zone("right_content", size="60%"),
                    ],
                ),
                ui.zone(name="footer", size="10%"),
            ],
        ),
    ]

    # CSS para fazer com que a div pai do componente ui.frame ocupe 100% da altura disponível, necessário para fazer com que o ui.frame ocupe tamém 100% do espaço
    q.page["meta"] = ui.meta_card(
        box="",
        layouts=layouts,
        stylesheet=ui.inline_stylesheet(
            """
.f1ux2gcm > .flgu8z7 > div:nth-of-type(4) {
  height: 100%;
}
"""
        ),
    )

    q.page["header"] = ui.header_card(
        box="header",
        icon="Suitcase",
        title="PLAN_TRIP",
        subtitle="IA PARA AUTOMAÇÃO DE VIAGENS",
        secondary_items=(
            [
                ui.tabs(
                    name="tabs",
                    value="#relatorio_page",
                    link=True,
                    items=[
                        ui.tab(name="#relatorio_page", label="Relatório"),
                    ],
                ),
            ]
            if app_config["chat_config"]["enabled"]
            else []
        ),
    )

    q.page["footer"] = ui.footer_card(
        box="footer",
        caption="2025 - IF1006",
    )

    # Script Js para traduzir os botões de um componente específico do wave
    q.page["meta"].script = ui.inline_script(
        """
        function updateButtons() {
            const buttons = document.querySelectorAll(".ms-Link.root-214");
            if (buttons.length >= 2) {
                [buttons[0].textContent, buttons[1].textContent] = ["Marcar Todos", "Desmarcar Todos"];
            }
        }

        const observer = new MutationObserver(updateButtons);
        observer.observe(document.body, { childList: true, subtree: true });

        updateButtons(); 
        """
    )

    await q.page.save()


def on_startup():
    setup_logger()
    log.info("================================================App started!")


def on_shutdown():
    log.info("================================================On Shutdown!")

    log.info("================================================Shutdown Completed!")


@app("/", on_startup=on_startup, on_shutdown=on_shutdown, mode="unicast")
async def serve(q: Q):
    """
    Handle user interactions such as arriving at the app for the first time or clicking a button
    """
    try:
        log.info(
            "========================== Start Serve Function ==============================="
        )
        log.debug(f"q.args: {q.args}")
        log.debug(f"q.client: {q.client}")
        log.debug(f"q.user: {q.user}")
        log.debug(f"q.events: {q.events}")
        log.debug(f"q.app: {q.app}")

        if not q.client.initialized:

            """Initialize the Application"""
            log.info("init application")
            log.info(f"using chat_client: {app_config['chat_client']}")

            # q.client.chat_client = GPTMockClient()
            q.client.chat_client = GPTClient()
            await init_layout(q)

            await show_long_process_dialog(
                q,
                "Iniciando aplicação",
                [ui.progress(label="", caption="Iniciando sessão...")],
            )

            q.client.relatorio = {}

            await show_long_process_dialog(
                q,
                "Iniciando aplicação",
                [ui.progress(label="", caption="Lendo perguntas sugeridas...")],
            )
            q.client.suggested_questions = (
                q.client.chat_client.get_suggested_questions()
            )

            await close_long_process_dialog(q)

            await procedimento_controller.init(q)
            q.client.initialized = True
            log.info("end init application")

        if q.events.painel_formulario:
            if q.events.painel_formulario.dismissed:
                q.page["meta"].side_panel = None

        # Handle routing.
        log.debug("Main. Before handle_on")
        await run_on(q)
        log.debug("Main. After handle_on")
        await q.page.save()
        log.debug("Page state saved")
    except Exception as err:
        log.error(f"Unhandled Application Error: {str(err)}")
        log.error(traceback.format_exc())
        await render_error_page(q, str(err))
        await q.page.save()
