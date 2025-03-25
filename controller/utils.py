import os
from h2o_wave import main, app, Q, ui, on, run_on, data
from config import app_config


async def show_long_process_dialog(q, title, items):

    q.page["meta"].dialog = ui.dialog(title=title, items=items, blocking=True)
    await q.page.save()


async def close_long_process_dialog(q):
    q.page["meta"].dialog = None
    await q.page.save()


async def render_error_page(q: Q, err: str):
    q.page["meta"] = ui.meta_card(
        box="",
        layouts=[
            ui.layout(
                breakpoint="xs",
                zones=[
                    ui.zone("content"),
                ],
            )
        ],
    )
    q.page["content"] = ui.form_card(
        box="content",
        items=[
            ui.text_xl("Erro interno"),
            ui.message_bar(type="error", text=f"Error: {err}"),
        ],
    )
