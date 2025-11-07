"""
Producer de Kafka - ETL Workshop 3
Este script realiza el proceso completo de ETL:
1. EXTRACCIÓN: Lee los archivos CSV originales (2015-2019)
2. TRANSFORMACIÓN: Limpia, estandariza y unifica los datos
3. CARGA: Envía cada registro a Kafka para ser procesado por el consumer
"""

import pandas as pd
import numpy as np
import json
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'happiness-data'
SEND_INTERVAL = 0.5  # Segundos entre cada mensaje (para simular streaming)

# Obtener la ruta base del proyecto (directorio padre de kafka/)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas de datos originales
DATA_FILES = {
    2015: os.path.join(BASE_DIR, 'data', '2015.csv'),
    2016: os.path.join(BASE_DIR, 'data', '2016.csv'),
    2017: os.path.join(BASE_DIR, 'data', '2017.csv'),
    2018: os.path.join(BASE_DIR, 'data', '2018.csv'),
    2019: os.path.join(BASE_DIR, 'data', '2019.csv')
}


def get_transformation_mappings():
    """
    Retorna los diccionarios de mapeo para estandarización
    (mismo proceso del notebook 2_transformation.ipynb)
    """
    # Diccionario para renombrar columnas equivalentes
    column_map = {
        # GDP per Capita
        'Economy (GDP per Capita)': 'GDP_per_Capita',
        'Economy..GDP.per.Capita.': 'GDP_per_Capita',
        'GDP per capita': 'GDP_per_Capita',
        
        # Social Support
        'Family': 'Social_Support',
        'Social support': 'Social_Support',
        
        # Healthy Life Expectancy
        'Health (Life Expectancy)': 'Healthy_Life_Expectancy',
        'Health..Life.Expectancy.': 'Healthy_Life_Expectancy',
        'Healthy life expectancy': 'Healthy_Life_Expectancy',
        
        # Freedom
        'Freedom': 'Freedom',
        'Freedom to make life choices': 'Freedom',
        
        # Generosity
        'Generosity': 'Generosity',
        
        # Perceptions of Corruption
        'Trust (Government Corruption)': 'Perceptions_of_Corruption',
        'Perceptions of corruption': 'Perceptions_of_Corruption',
        'Trust..Government.Corruption.': 'Perceptions_of_Corruption',
        
        # Happiness Score
        'Happiness Score': 'Happiness_Score',
        'Score': 'Happiness_Score',
        'Happiness.Score': 'Happiness_Score',

        # Country
        'Country': 'Country',
        'Country or region': 'Country',
        
        # Region
        'Region': 'Region',
    }
    
    # Diccionario de alias para normalizar nombres de países
    country_alias = {
        "Trinidad & Tobago": "Trinidad and Tobago",
        "Taiwan Province of China": "Taiwan",
        "Hong Kong S.A.R., China": "Hong Kong",
        "Northern Cyprus": "North Cyprus",
        "North Macedonia": "Macedonia",
        "Congo (Brazzaville)": "Congo",
        "Congo (Kinshasa)": "Democratic Republic of the Congo",
        "Ivory Coast": "Côte d'Ivoire",
        "Swaziland": "Eswatini",
        "Eswatini": "Eswatini",
        "Gambia": "Gambia",
        "Somaliland Region": "Somaliland region",
        "Somaliland region": "Somaliland region",
    }
    
    return column_map, country_alias


def create_region_map(dfs, country_alias):
    """
    Crea el diccionario maestro de regiones a partir de los datos de 2015 y 2016
    """
    region_map = {}
    
    for year in [2015, 2016]:
        df = dfs[year]
        for _, row in df.iterrows():
            country = row['Country']
            # Normalizar el nombre del país si existe un alias
            if country in country_alias:
                country = country_alias[country]
            # Guardar la región correspondiente
            if 'Region' in df.columns and not pd.isna(row['Region']):
                region_map[country] = row['Region']
    
    logger.info(f"✓ Diccionario de regiones creado: {len(region_map)} países")
    return region_map


def load_and_transform_data():
    """
    PROCESO ETL COMPLETO:
    1. Extrae los datos de los archivos CSV originales
    2. Transforma y limpia los datos
    3. Retorna el DataFrame unificado listo para enviar a Kafka
    """
    logger.info("\n" + "="*60)
    logger.info("INICIANDO PROCESO ETL")
    logger.info("="*60)
    
    # ============ EXTRACCIÓN ============
    logger.info("\n[1/3] EXTRACCIÓN - Cargando archivos CSV...")
    dfs = {}
    for year, path in DATA_FILES.items():
        try:
            dfs[year] = pd.read_csv(path)
            logger.info(f"  ✓ {year}: {len(dfs[year])} registros")
        except FileNotFoundError:
            logger.error(f"  ✗ Archivo no encontrado: {path}")
            raise
    
    total_raw_records = sum(len(df) for df in dfs.values())
    logger.info(f"  Total de registros crudos: {total_raw_records}")
    
    # ============ TRANSFORMACIÓN ============
    logger.info("\n[2/3] TRANSFORMACIÓN - Limpiando y estandarizando...")
    
    # Obtener diccionarios de mapeo
    column_map, country_alias = get_transformation_mappings()
    
    # Crear diccionario de regiones
    region_map = create_region_map(dfs, country_alias)
    
    # Columnas finales que queremos mantener
    columns_to_keep = [
        'Country', 'Region', 'Year', 'Happiness_Score',
        'GDP_per_Capita', 'Social_Support', 'Healthy_Life_Expectancy',
        'Freedom', 'Generosity', 'Perceptions_of_Corruption'
    ]
    
    # Columnas numéricas para redondeo
    numeric_columns = [
        'Happiness_Score', 'GDP_per_Capita', 'Social_Support',
        'Healthy_Life_Expectancy', 'Freedom', 'Generosity',
        'Perceptions_of_Corruption'
    ]
    
    # Procesar cada dataset
    cleaned_dfs = {}
    for year, df in dfs.items():
        # 1. Renombrar columnas
        df = df.rename(columns=column_map)
        
        # 2. Normalizar nombres de países
        df['Country'] = df['Country'].replace(country_alias)
        
        # 3. Asignar regiones faltantes
        if 'Region' not in df.columns:
            df['Region'] = df['Country'].map(region_map)
        
        # 4. Agregar columna de año
        df['Year'] = year
        
        # 5. Seleccionar solo las columnas necesarias
        available_columns = [col for col in columns_to_keep if col in df.columns]
        cleaned_df = df[available_columns]
        
        # 6. Aplicar redondeo a 3 decimales
        for col in numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].round(3)
        
        cleaned_dfs[year] = cleaned_df
        logger.info(f"  ✓ Dataset {year} procesado: {len(cleaned_df)} registros")
    
    # Concatenar todos los datasets
    happiness_all = pd.concat(cleaned_dfs.values(), ignore_index=True)
    
    # Correcciones finales
    # Completar región faltante para Gambia
    happiness_all.loc[happiness_all["Country"] == "Gambia", "Region"] = "Sub-Saharan Africa"
    
    # Imputar valores faltantes en Perceptions_of_Corruption
    missing_mask = happiness_all["Perceptions_of_Corruption"].isna()
    if missing_mask.any():
        for idx in happiness_all[missing_mask].index:
            region = happiness_all.loc[idx, "Region"]
            year = happiness_all.loc[idx, "Year"]
            mean_value = happiness_all[
                (happiness_all["Region"] == region) & 
                (happiness_all["Year"] == year)
            ]["Perceptions_of_Corruption"].mean()
            happiness_all.loc[idx, "Perceptions_of_Corruption"] = round(mean_value, 3)
    
    logger.info(f"\n  ✓ Dataset final unificado: {len(happiness_all)} registros")
    logger.info(f"  ✓ Columnas: {happiness_all.columns.tolist()}")
    logger.info(f"  ✓ Valores nulos: {happiness_all.isnull().sum().sum()}")
    logger.info(f"  ✓ Años cubiertos: {sorted(happiness_all['Year'].unique())}")
    
    # Agregar columna de train/test split (70%-30%)
    from sklearn.model_selection import train_test_split
    
    # Preparar features para el split (mismo que en el entrenamiento)
    feature_columns = [
        'GDP_per_Capita', 'Social_Support', 'Healthy_Life_Expectancy',
        'Freedom', 'Generosity', 'Perceptions_of_Corruption'
    ]
    
    X = happiness_all[feature_columns]
    y = happiness_all['Happiness_Score']
    
    # Hacer el split con la misma semilla que en el entrenamiento
    _, _, _, _, train_idx, test_idx = train_test_split(
        X, y, 
        range(len(X)),  # Índices
        test_size=0.30, 
        random_state=42
    )
    
    # Crear columna Data_Split
    happiness_all['Data_Split'] = None
    happiness_all.loc[train_idx, 'Data_Split'] = 'train'
    happiness_all.loc[test_idx, 'Data_Split'] = 'test'
    
    logger.info(f"\n  ✓ División train/test aplicada:")
    logger.info(f"    - Train: {len(train_idx)} registros ({len(train_idx)/len(happiness_all)*100:.1f}%)")
    logger.info(f"    - Test: {len(test_idx)} registros ({len(test_idx)/len(happiness_all)*100:.1f}%)")
    
    return happiness_all


def create_producer():
    """Crea y configura el productor de Kafka"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3,
            max_in_flight_requests_per_connection=1
        )
        logger.info(f"\n✓ Productor conectado a Kafka en {KAFKA_BROKER}")
        return producer
    except KafkaError as e:
        logger.error(f"✗ Error al conectar con Kafka: {e}")
        raise


def send_data(producer, df):
    """
    Envía cada registro del DataFrame a Kafka
    
    Args:
        producer: Instancia del productor de Kafka
        df: DataFrame con los datos a enviar
    """
    total_records = len(df)
    success_count = 0
    error_count = 0
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Iniciando envío de {total_records} registros a Kafka")
    logger.info(f"{'='*60}\n")
    
    for idx, row in df.iterrows():
        try:
            # Convertir la fila a diccionario y manejar valores NaN
            record = row.to_dict()
            
            # Convertir valores NaN a None (null en JSON)
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
            
            # Enviar el mensaje a Kafka
            future = producer.send(KAFKA_TOPIC, value=record)
            
            # Esperar confirmación (opcional, para asegurar envío)
            result = future.get(timeout=10)
            
            success_count += 1
            
            # Log cada 50 registros
            if (idx + 1) % 50 == 0:
                logger.info(f"  Progreso: {idx + 1}/{total_records} registros enviados")
            
            # Log detallado del primer registro para verificación
            if idx == 0:
                logger.info(f"\n  Ejemplo de registro enviado:")
                logger.info(f"  {json.dumps(record, indent=2)}\n")
            
            # Pequeña pausa para simular streaming en tiempo real
            time.sleep(SEND_INTERVAL)
            
        except Exception as e:
            error_count += 1
            logger.error(f"✗ Error al enviar registro {idx}: {e}")
            continue
    
    # Asegurar que todos los mensajes se envíen
    producer.flush()
    
    # Resumen final
    logger.info(f"\n{'='*60}")
    logger.info(f"RESUMEN DEL ENVÍO")
    logger.info(f"{'='*60}")
    logger.info(f"✓ Registros enviados exitosamente: {success_count}")
    if error_count > 0:
        logger.info(f"✗ Registros con error: {error_count}")
    logger.info(f"  Total procesado: {success_count + error_count}/{total_records}")
    logger.info(f"{'='*60}\n")


def main():
    """Función principal del productor"""
    try:
        logger.info("="*60)
        logger.info("KAFKA PRODUCER - ETL Workshop 3")
        logger.info("="*60)
        
        # Ejecutar proceso ETL completo
        df = load_and_transform_data()
        
        # Crear productor
        logger.info("\n[3/3] CARGA - Enviando datos a Kafka...")
        producer = create_producer()
        
        # Enviar datos a Kafka
        send_data(producer, df)
        
        # Cerrar productor
        producer.close()
        logger.info("\n✓ Productor cerrado correctamente")
        
    except KeyboardInterrupt:
        logger.info("\n✗ Proceso interrumpido por el usuario")
    except Exception as e:
        logger.error(f"✗ Error general: {e}")
        raise
    finally:
        logger.info("\n" + "="*60)
        logger.info("PROCESO ETL FINALIZADO")
        logger.info("="*60)


if __name__ == "__main__":
    main()
