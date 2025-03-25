from h2o_wave import main, app, Q, ui, on, run_on, data
from log import log, setup_logger


async def get_secao(q: Q, secao, config):
    log.info("**********************************")
    log.info(q.args)

    info_secao = config["secoes"][secao]
    q.page["meta"].dialog.items = [
        ui.progress(label="", caption=f'Processando {info_secao["titulo"]}...')
    ]

    await q.page.save()

    preprompt = get_preprompt(q)
    promt = info_secao["pergunta"]

    q.client.relatorio[secao] = q.client.chat_client.query_chat(
        preprompt + promt,
        q.client.selected_cidade,
    )

    log.info("PROMPTTTTTTTTTTTTTTTTTTTTTTTTTT")
    log.info(q.client.relatorio[secao])

    return q.client.relatorio[secao]


def get_preprompt(q):
    preprompt = f"Considerando uma Viagem para {q.client.selected_cidade}, e sabendo que o passageiro apresenta essas características: "

    caracteristicas = []

    if q.args.data_chegada:
        caracteristicas.append(f"Chegará na cidade em {q.args.data_chegada}.")

    if q.args.data_saida:
        caracteristicas.append(f"Sairá da cidade em {q.args.data_saida}.")

    if q.args.preferencia_tempo:
        caracteristicas.append(f"Prefere atividades {q.args.preferencia_tempo}.")

    if q.args.tipo_experiencia:
        caracteristicas.append(
            f"Busca uma experiência focada em {q.args.tipo_experiencia}."
        )

    if q.args.companhia_viagem:
        caracteristicas.append(f"Estará viajando {q.args.companhia_viagem}.")

    if q.args.meio_transporte:
        caracteristicas.append(
            f"Utilizará {q.args.meio_transporte} como meio de transporte principal."
        )

    if q.args.frequencia_deslocamento:
        caracteristicas.append(
            f"Prefere {q.args.frequencia_deslocamento} em relação aos deslocamentos."
        )

    preprompt += " ".join(caracteristicas) + " "

    return preprompt
