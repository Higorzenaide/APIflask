import pandas as pd

def verificarConflitos(df01,df02):
    if 'error' in df01:
        return True
    
    id_gestor = df02["id"][0]
    nova_hora_inicio = df02["hora_inicio"][0]
    nova_hora_fim = df02["hora_fim"][0]
    df = pd.DataFrame(df01)
    
    df_filtrado = df.loc[df["id_gestor"] != id_gestor]
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
    
    print(df02)
    id_gestor = df02["id"][0]
    nova_hora_inicio = df02["hora_inicio"][0]
    nova_hora_fim = df02["hora_fim"][0]
    df = pd.DataFrame(df01)
    
    df_filtrado = df.loc[df["id_gestor"] == id_gestor]
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