import pandas as pd
import pypyodbc

def fetch_data(connection_string, query):
    conn = pypyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df_pr = pd.DataFrame(rows, columns=columns)

    conn.close()
    return df_pr

def get_df_pr(server_name, database, username):
    query = (
       """ SELECT [NIRF]
      ,[hectares]
      ,[codigo_incra]
      ,[nome]
      ,[situacao]
      ,[logradouro]
      ,[distrito]
      ,[UF]
      ,[municipio]
      ,[CEP]
      ,[data_att_cadastro]
      ,[imunte_isento]
      ,[SNCR]
        FROM [Projeto CAFIR].[dbo].[CAFIR]
        WHERE [UF] = 'PR' AND [SNCR] = '1'"""
    )

    connection_string = f"""
        DRIVER={{SQL SERVER}};
        SERVER={server_name};
        DATABASE={database};
        UID={username};
        Trusted_Connection=yes;
    """

    return fetch_data(connection_string, query)

# Exemplo de uso
if __name__ == "__main__":
    server_name = r'DESKTOP-5V1VIGP\SQLEXPRESS'
    database = 'Projeto CAFIR'
    username = 'dbo'
    
    df_pr = get_df_pr(server_name, database, username)
    print(df_pr.head())
