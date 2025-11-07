"""
Consumer de Kafka - ETL Workshop 3
Este script:
1. Consume mensajes desde Kafka
2. Carga el modelo de regresión entrenado
3. Realiza predicciones de felicidad
4. Almacena los resultados en MySQL
"""

import json
import joblib
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
import time
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener la ruta base del proyecto (directorio padre de kafka/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'happiness-data'
KAFKA_GROUP_ID = 'happiness-consumer-group-v2'  # Cambiado para empezar desde cero
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'happiness_regression.pkl')

# Configuración de MySQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'happiness_db',
    'user': 'root',
    'password': 'root'
}

# Columnas de características para el modelo
FEATURE_COLUMNS = [
    'GDP_per_Capita',
    'Social_Support',
    'Healthy_Life_Expectancy',
    'Freedom',
    'Generosity',
    'Perceptions_of_Corruption'
]


def load_model():
    """Carga el modelo de regresión entrenado"""
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"✓ Modelo cargado desde: {MODEL_PATH}")
        return model
    except FileNotFoundError:
        logger.error(f"✗ Modelo no encontrado en: {MODEL_PATH}")
        raise
    except Exception as e:
        logger.error(f"✗ Error al cargar modelo: {e}")
        raise


def create_consumer():
    """Crea y configura el consumidor de Kafka"""
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            group_id=KAFKA_GROUP_ID,
            auto_offset_reset='earliest',  # Leer desde el principio si no hay offset previo
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        logger.info(f"✓ Consumidor conectado a Kafka en {KAFKA_BROKER}")
        logger.info(f"  Topic: {KAFKA_TOPIC}")
        logger.info(f"  Group ID: {KAFKA_GROUP_ID}")
        return consumer
    except KafkaError as e:
        logger.error(f"✗ Error al conectar con Kafka: {e}")
        raise


def setup_database():
    """Crea la base de datos y tabla si no existen"""
    try:
        # Conectar sin especificar base de datos
        conn_config = DB_CONFIG.copy()
        db_name = conn_config.pop('database')
        
        connection = mysql.connector.connect(**conn_config)
        cursor = connection.cursor()
        
        # Crear base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        logger.info(f"✓ Base de datos '{db_name}' verificada/creada")
        
        # Usar la base de datos
        cursor.execute(f"USE {db_name}")
        
        # Crear tabla si no existe
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country VARCHAR(100) NOT NULL,
            region VARCHAR(100),
            year INT NOT NULL,
            gdp_per_capita DECIMAL(10, 3),
            social_support DECIMAL(10, 3),
            healthy_life_expectancy DECIMAL(10, 3),
            freedom DECIMAL(10, 3),
            generosity DECIMAL(10, 3),
            perceptions_of_corruption DECIMAL(10, 3),
            actual_happiness_score DECIMAL(10, 3),
            predicted_happiness_score DECIMAL(10, 3),
            prediction_error DECIMAL(10, 3),
            data_split VARCHAR(10) DEFAULT NULL COMMENT 'train o test',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_country_year (country, year),
            INDEX idx_created_at (created_at),
            INDEX idx_data_split (data_split)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(create_table_sql)
        logger.info(f"✓ Tabla 'predictions' verificada/creada")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        logger.error(f"✗ Error al configurar base de datos: {e}")
        return False


def connect_db():
    """Establece conexión con MySQL"""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                logger.info(f"✓ Conectado a MySQL: {DB_CONFIG['database']}")
                return connection
        except Error as e:
            if attempt < max_retries - 1:
                logger.warning(f"Intento {attempt + 1}/{max_retries} - Reintentando en {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                logger.error(f"✗ Error al conectar con MySQL: {e}")
                raise
    return None


def insert_prediction(connection, record, predicted_score):
    """
    Inserta la predicción en la base de datos
    
    Args:
        connection: Conexión a MySQL
        record: Diccionario con los datos del registro
        predicted_score: Valor predicho de felicidad
    """
    try:
        cursor = connection.cursor()
        
        # Extraer valores del registro
        actual_score = record.get('Happiness_Score')
        prediction_error = None
        if actual_score is not None:
            prediction_error = abs(actual_score - predicted_score)
        
        # Query de inserción
        insert_query = """
        INSERT INTO predictions (
            country, region, year,
            gdp_per_capita, social_support, healthy_life_expectancy,
            freedom, generosity, perceptions_of_corruption,
            actual_happiness_score, predicted_happiness_score, prediction_error,
            data_split
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            record.get('Country'),
            record.get('Region'),
            record.get('Year'),
            record.get('GDP_per_Capita'),
            record.get('Social_Support'),
            record.get('Healthy_Life_Expectancy'),
            record.get('Freedom'),
            record.get('Generosity'),
            record.get('Perceptions_of_Corruption'),
            actual_score,
            float(predicted_score),
            float(prediction_error) if prediction_error is not None else None,
            record.get('Data_Split')  # Nueva columna
        )
        
        cursor.execute(insert_query, values)
        connection.commit()
        cursor.close()
        
        return True
        
    except Error as e:
        logger.error(f"✗ Error al insertar en DB: {e}")
        return False


def predict_and_store(model, connection, record):
    """
    Realiza la predicción y almacena en la base de datos
    
    Args:
        model: Modelo de regresión cargado
        connection: Conexión a MySQL
        record: Diccionario con los datos del registro
    """
    try:
        # Extraer características para predicción en un diccionario
        features_dict = {}
        for col in FEATURE_COLUMNS:
            value = record.get(col)
            if value is None:
                logger.warning(f"⚠ Valor faltante en {col} para {record.get('Country')}")
                # Usar 0 como valor por defecto (puedes cambiar esta estrategia)
                value = 0.0
            features_dict[col] = float(value)
        
        # Convertir a DataFrame con nombres de columnas (para evitar el warning de sklearn)
        X = pd.DataFrame([features_dict])
        predicted_score = model.predict(X)[0]
        
        # Insertar en base de datos
        success = insert_prediction(connection, record, predicted_score)
        
        if success:
            return predicted_score
        else:
            return None
            
    except Exception as e:
        logger.error(f"✗ Error en predicción: {e}")
        return None


def main():
    """Función principal del consumidor"""
    logger.info("="*60)
    logger.info("KAFKA CONSUMER - ETL Workshop 3")
    logger.info("="*60)
    
    model = None
    consumer = None
    connection = None
    
    try:
        # Cargar modelo
        model = load_model()
        
        # Configurar base de datos (crear si no existe)
        logger.info("\nConfigurando base de datos...")
        if not setup_database():
            logger.error("✗ No se pudo configurar la base de datos")
            return
        
        # Conectar a base de datos
        connection = connect_db()
        
        # Crear consumidor
        consumer = create_consumer()
        
        logger.info(f"\n{'='*60}")
        logger.info("ESPERANDO MENSAJES...")
        logger.info(f"{'='*60}\n")
        
        processed_count = 0
        error_count = 0
        
        # Consumir mensajes
        for message in consumer:
            try:
                record = message.value
                country = record.get('Country', 'Unknown')
                year = record.get('Year', 'N/A')
                
                # Realizar predicción y almacenar
                predicted_score = predict_and_store(model, connection, record)
                
                if predicted_score is not None:
                    processed_count += 1
                    actual_score = record.get('Happiness_Score', 'N/A')
                    
                    # Log cada 50 registros procesados
                    if processed_count % 50 == 0:
                        logger.info(f"  Procesados: {processed_count} registros")
                    
                    # Log detallado del primer registro
                    if processed_count == 1:
                        logger.info(f"\n  Ejemplo de predicción:")
                        logger.info(f"  País: {country} ({year})")
                        logger.info(f"  Score real: {actual_score}")
                        logger.info(f"  Score predicho: {predicted_score:.3f}")
                        if actual_score != 'N/A':
                            error = abs(actual_score - predicted_score)
                            logger.info(f"  Error absoluto: {error:.3f}\n")
                else:
                    error_count += 1
                    
            except Exception as e:
                error_count += 1
                logger.error(f"✗ Error al procesar mensaje: {e}")
                continue
                
    except KeyboardInterrupt:
        logger.info("\n✗ Consumidor interrumpido por el usuario")
        logger.info(f"\nRESUMEN:")
        logger.info(f"  ✓ Registros procesados: {processed_count}")
        if error_count > 0:
            logger.info(f"  ✗ Registros con error: {error_count}")
    except Exception as e:
        logger.error(f"✗ Error general: {e}")
    finally:
        # Cerrar conexiones
        if consumer:
            consumer.close()
            logger.info("✓ Consumidor cerrado")
        if connection and connection.is_connected():
            connection.close()
            logger.info("✓ Conexión a MySQL cerrada")
        
        logger.info("\n" + "="*60)
        logger.info("FIN DEL PROCESO")
        logger.info("="*60)


if __name__ == "__main__":
    main()
