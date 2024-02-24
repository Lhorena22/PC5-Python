import pandas as pd
from envio_correo import enviar_correo
import requests

def limpiar_columnas(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df = df.loc[:,~df.columns.duplicated()]
    df['dispositivo_legal'] = df['dispositivo_legal'].str.replace(',', '')
    return df

def dolarizar_montos(df):
    response = requests.get('http://api.sunat.cloud/cambio')
    if response.status_code == 200:
        data = response.json()
        tipo_cambio = data['dolar']['venta']
        df['monto_inversion_dolarizado'] = df['monto_inversion'] / tipo_cambio
        df['monto_transferencia_dolarizado'] = df['monto_transferencia'] / tipo_cambio
    return df

def asignar_estado_puntuacion(df):
    df['estado'] = df['estado'].replace({'ActosPrevios': 'Actos Previos', 'Ejecucion': 'Ejecución'})
    df['puntuacion_estado'] = df['estado'].map({'Actos Previos': 1, 'Resuelto': 0, 'Ejecución': 2, 'Concluido': 3})
    return df

def generar_reporte_por_region(df):
    regiones = df['Region'].unique()
    for region in regiones:
        region_df = df[df['Region'] == region]
        if not region_df.empty:
            reporte_df = region_df[(region_df['tipo_obra'] == 'Urbano') & (region_df['puntuacion_estado'].isin([1, 2, 3]))]
            if not reporte_df.empty:
                top5_df = reporte_df.nlargest(5, 'monto_inversion_dolarizado')
                top5_df.to_excel(f'{region}_top5_costo_inversion.xlsx', index=False)

def almacenar_ubigeos(df):
    ubigeos_df = df[['ubigeo', 'Region', 'Provincia', 'Distrito']].drop_duplicates()

if __name__ == "__main__":
    df = pd.read_excel('./data/reactiva.xlsx')
    df = limpiar_columnas(df)
    df = dolarizar_montos(df)
    df = asignar_estado_puntuacion(df)
    generar_reporte_por_region(df)
    almacenar_ubigeos(df)
    enviar_correo('destinatario@example.com', 'Reportes generados exitosamente', 'Se adjuntan los reportes solicitados')
