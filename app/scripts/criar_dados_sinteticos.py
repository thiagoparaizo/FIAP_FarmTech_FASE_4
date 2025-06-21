# scripts/criar_dados_sinteticos.py

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adicionar path do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, BASE_DIR)

from config import Config
from app.services.sql_db_service import SQLDatabaseService

def criar_dados_sinteticos():
    """Cria dados sintéticos realísticos para treinamento ML"""
    
    print("🔧 Gerando dados sintéticos...")
    
    # Conectar ao banco
    sql_db = SQLDatabaseService(Config.SQL_DATABASE_URI)
    
    # Gerar dados sintéticos mais realísticos
    np.random.seed(42)
    n_samples = 200  # Mais amostras para melhor treinamento
    
    data = []
    base_time = datetime.now() - timedelta(days=30)
    
    for i in range(n_samples):
        timestamp = base_time + timedelta(hours=i*3)  # A cada 3 horas
        
        # Gerar dados com padrões realísticos
        # Umidade varia por tempo (ciclo diário)
        hora = timestamp.hour
        umidade_base = 50 + 20 * np.sin(hora * np.pi / 12)  # Ciclo diário
        umidade = max(5, min(95, umidade_base + np.random.normal(0, 15)))
        
        # pH varia mais lentamente
        ph_base = 6.8 + 0.5 * np.sin(i * 0.1)  # Variação lenta
        ph = max(4.5, min(9.0, ph_base + np.random.normal(0, 0.3)))
        
        # Nutrientes variam de forma realística
        fosforo = np.random.choice([0, 1], p=[0.6, 0.4])
        potassio = np.random.choice([0, 1], p=[0.7, 0.3])
        
        # Lógica de irrigação MAIS REALÍSTICA (com mais aleatoriedade)
        irrigacao_score = 0
        
        # Condições básicas (menos determinísticas)
        if umidade < 25:
            irrigacao_score += 4  # Muito seco = alta prioridade
        elif umidade < 40:
            irrigacao_score += 2  # Seco = média prioridade
        elif umidade < 60:
            irrigacao_score += 1  # Pouco seco = baixa prioridade
            
        if 6.0 <= ph <= 7.5:
            irrigacao_score += 2  # pH ideal
        elif 5.5 <= ph <= 8.0:
            irrigacao_score += 1  # pH aceitável
        else:
            irrigacao_score -= 1  # pH problemático
            
        # Horários ideais (menos peso)
        if 6 <= hora <= 10 or 16 <= hora <= 18:
            irrigacao_score += 1
        elif 11 <= hora <= 15:  # Meio-dia muito quente
            irrigacao_score -= 1
            
        # Nutrientes influenciam
        if fosforo and potassio:
            irrigacao_score += 1  # Nutrientes OK
        elif not fosforo and not potassio:
            irrigacao_score -= 1  # Sem nutrientes
            
        # IMPORTANTE: Adicionar muito mais aleatoriedade
        random_factor = np.random.normal(0, 1.5)  # Desvio padrão maior
        irrigacao_score += random_factor
        
        # Decisão final com limiar mais flexível
        irrigation_probability = 1 / (1 + np.exp(-irrigacao_score))  # Sigmoid
        irrigacao = 1 if irrigation_probability > np.random.uniform(0.3, 0.7) else 0
        
        # Adicionar 10% de decisões completamente aleatórias (simula erro humano/sensor)
        if np.random.random() < 0.1:
            irrigacao = np.random.choice([0, 1])
        
        data.append({
            'timestamp': int(timestamp.timestamp() * 1000),
            'datetime': timestamp,
            'umidade': round(umidade, 2),
            'ph': round(ph, 2),
            'fosforo': fosforo,
            'potassio': potassio,
            'irrigacao': irrigacao,
            'score': round(irrigacao_score, 2),  # Para debug
            'probability': round(irrigation_probability, 3)  # Para debug
        })
    
    print(f"✅ Gerados {len(data)} registros sintéticos")
    print(f"📊 Irrigação ativa: {sum(d['irrigacao'] for d in data)} casos ({sum(d['irrigacao'] for d in data)/len(data)*100:.1f}%)")
    print(f"🌡️ Umidade: {min(d['umidade'] for d in data):.1f}% - {max(d['umidade'] for d in data):.1f}%")
    print(f"🧪 pH: {min(d['ph'] for d in data):.2f} - {max(d['ph'] for d in data):.2f}")
    
    return data

def inserir_no_banco(data):
    """Insere os dados no banco de dados"""
    
    print("\n💾 Inserindo dados no banco...")
    
    sql_db = SQLDatabaseService(Config.SQL_DATABASE_URI)
    session = sql_db.get_session()
    
    try:
        # Criar sensor se não existir
        sensor_id = 1
        
        # Verificar se sensor existe
        from sqlalchemy import text
        result = session.execute(text("SELECT COUNT(*) FROM sensor WHERE id = :id"), {"id": sensor_id})
        sensor_exists = result.fetchone()[0] > 0
        
        if not sensor_exists:
            print("🔧 Criando sensor de teste...")
            # Criar sensor
            session.execute(text("""
                INSERT INTO sensor (id, tipo, modelo, ativo) 
                VALUES (:id, :tipo, :modelo, :ativo)
            """), {
                "id": sensor_id,
                "tipo": "MultiSensor",
                "modelo": "Sintético para ML",
                "ativo": True
            })
            session.commit()
            print("✅ Sensor criado")
        
        # Limpar dados antigos (opcional)
        print("🧹 Limpando dados antigos...")
        session.execute(text("DELETE FROM leitura_sensor WHERE sensor_id = :id"), {"id": sensor_id})
        session.commit()
        
        # Inserir leituras
        print("📝 Inserindo leituras...")
        
        for i, record in enumerate(data):
            # Inserir leitura de umidade
            session.execute(text("""
                INSERT INTO leitura_sensor (sensor_id, valor, unidade, data_hora) 
                VALUES (:sensor_id, :valor, :unidade, :data_hora)
            """), {
                "sensor_id": sensor_id,
                "valor": str(record['umidade']),
                "unidade": "%",
                "data_hora": record['datetime']
            })
            
            # Inserir leitura de pH
            session.execute(text("""
                INSERT INTO leitura_sensor (sensor_id, valor, unidade, data_hora) 
                VALUES (:sensor_id, :valor, :unidade, :data_hora)
            """), {
                "sensor_id": sensor_id,
                "valor": str(record['ph']),
                "unidade": "pH",
                "data_hora": record['datetime']
            })
            
            # Inserir leitura de nutrientes
            nutrientes = {"P": record['fosforo'], "K": record['potassio']}
            session.execute(text("""
                INSERT INTO leitura_sensor (sensor_id, valor, unidade, data_hora) 
                VALUES (:sensor_id, :valor, :unidade, :data_hora)
            """), {
                "sensor_id": sensor_id,
                "valor": str(nutrientes),
                "unidade": "ppm",
                "data_hora": record['datetime']
            })
            
            if (i + 1) % 50 == 0:
                print(f"   📊 Inseridos {i + 1}/{len(data)} registros...")
        
        session.commit()
        print(f"✅ Todos os {len(data)} registros inseridos com sucesso!")
        
        # Verificar inserção
        result = session.execute(text("SELECT COUNT(*) FROM leitura_sensor WHERE sensor_id = :id"), {"id": sensor_id})
        total_leituras = result.fetchone()[0]
        print(f"📊 Total de leituras no banco: {total_leituras}")
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

def main():
    """Função principal"""
    print("🌱 FarmTech Solutions - Gerador de Dados Sintéticos")
    print("=" * 50)
    
    try:
        # Gerar dados
        data = criar_dados_sinteticos()
        
        # Inserir no banco
        inserir_no_banco(data)
        
        print("\n🎉 Processo concluído com sucesso!")
        print("\n🚀 Agora você pode executar o treinamento:")
        print("   python app/scripts/train_model.py --days 30 --min-samples 20")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())