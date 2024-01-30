import pandas as pd

def verificarConflitos(df01,df02):
    if 'error' in df01:
        return True
    
    id_gestor = df02["id"][0]
    nova_hora_inicio = df02["hora_inicio"][0]
    nova_hora_fim = df02["hora_fim"][0]
    df = pd.DataFrame(df01)
    
    df_filtrado = df.loc[df["id_gestor"] != id_gestor]
    if df_filtrado.empty:
        return True  # Não há agendamentos para esse gestor
    lista_de_hora_inicio_ja_agendada = df_filtrado["hora_inicio"].tolist()
    lista_de_hora_fim_ja_agendada = df_filtrado["hora_fim"].tolist()

    for hora_inicio_ja_agendada, hora_fim_ja_agendada in zip(lista_de_hora_inicio_ja_agendada,lista_de_hora_fim_ja_agendada):
        if nova_hora_inicio >= hora_inicio_ja_agendada and nova_hora_inicio <= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim": hora_fim_ja_agendada}
            return horario
        elif nova_hora_fim >= hora_inicio_ja_agendada and nova_hora_fim <= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim": hora_fim_ja_agendada}
            return horario
        elif nova_hora_inicio <= hora_inicio_ja_agendada and nova_hora_fim >= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim ": hora_fim_ja_agendada}
            return horario
        else:
            return True

def verificarConflitosEntreOProprioUser(df01,df02):
    if 'error' in df01:
        return True
    
    if df02 == [] or df02 == None or df02 == '':
        return True
    

    id_gestor = df02["id"][0]
    nova_hora_inicio = df02["hora_inicio"][0]
    nova_hora_fim = df02["hora_fim"][0]
    df = pd.DataFrame(df01)

    print("Passou por aqui")
    df_filtrado = df.loc[df["id_gestor"] == id_gestor]
    if df_filtrado.empty:
        return True  # Não há agendamentos para esse gestor
    print("Aqui não")
    lista_de_hora_inicio_ja_agendada = df_filtrado["hora_inicio"].tolist()
    lista_de_hora_fim_ja_agendada = df_filtrado["hora_fim"].tolist()

    print(lista_de_hora_inicio_ja_agendada)
    print(lista_de_hora_fim_ja_agendada)

    for hora_inicio_ja_agendada, hora_fim_ja_agendada in zip(lista_de_hora_inicio_ja_agendada,lista_de_hora_fim_ja_agendada):
        if nova_hora_inicio >= hora_inicio_ja_agendada and nova_hora_inicio <= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim": hora_fim_ja_agendada}
            return horario
        elif nova_hora_fim >= hora_inicio_ja_agendada and nova_hora_fim <= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim": hora_fim_ja_agendada}
            return horario
        elif nova_hora_inicio <= hora_inicio_ja_agendada and nova_hora_fim >= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim ": hora_fim_ja_agendada}
            return horario
        else:
            return True

def verificarConflitosEntreOpropriouserParaEditar(agendamentos_ja_efetuados,novo_agendamento):
    if 'error' in agendamentos_ja_efetuados:
        return True
    
    print(f'-------------------------------------- agendamento já efetuado {agendamentos_ja_efetuados}')
    if novo_agendamento == [] or novo_agendamento == None or novo_agendamento == '':
        return True
    

    id_agendamento = novo_agendamento["id"][0]
    nova_hora_inicio = novo_agendamento["hora_inicio"][0]
    nova_hora_fim = novo_agendamento["hora_fim"][0]
    df = pd.DataFrame(agendamentos_ja_efetuados)
    print(f'Novo agendamento id:{id_agendamento}, hora_inicio:{nova_hora_inicio}, hora_fim:{nova_hora_fim}')
    print("Passou por aqui")
    df_filtrado = df.loc[df["id"] != id_agendamento]
    if df_filtrado.empty:
        return True  # Não há agendamentos para esse gestor
    print("Aqui não")
    lista_de_hora_inicio_ja_agendada = df_filtrado["hora_inicio"].tolist()
    lista_de_hora_fim_ja_agendada = df_filtrado["hora_fim"].tolist()

    print(f'--------------------------------------------------------------{lista_de_hora_inicio_ja_agendada}')
    print(f'--------------------------------------------------------------{lista_de_hora_fim_ja_agendada}')

    for hora_inicio_ja_agendada, hora_fim_ja_agendada in zip(lista_de_hora_inicio_ja_agendada,lista_de_hora_fim_ja_agendada):
        if nova_hora_inicio >= hora_inicio_ja_agendada and nova_hora_inicio <= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim": hora_fim_ja_agendada}
            return horario
        elif nova_hora_fim >= hora_inicio_ja_agendada and nova_hora_fim <= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim": hora_fim_ja_agendada}
            return horario
        elif nova_hora_inicio <= hora_inicio_ja_agendada and nova_hora_fim >= hora_fim_ja_agendada:
            horario = {"horario_inicio":hora_inicio_ja_agendada,
                       "horario_fim ": hora_fim_ja_agendada}
            return horario
        else:
            return True