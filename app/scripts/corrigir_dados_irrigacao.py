#scripts/corrigir_dados_irrigacao.py

import sys
import os
import numpy as np
from datetime import datetime, timedelta

sys.path.insert(0, '.')
from config import Config
from app.services.sql_db_service import SQLDatabaseService

def inserir_dados_irrigacao_diretos():
    """Insere dados de irrigação diretamente no formato correto"""
    
    print("🔧 Corrigindo dados de irrigação...")
    
    sql_db = SQLDatabaseService(Config.SQL_DATABASE_URI)
    session = sql_db.get_session()
    
    try:
        from sqlalchemy import text
        
        # Gerar 100 registros balanceados EXPLICITAMENTE
        dados = []
        base_time = datetime.now() - timedelta(days=30)
        
        # 50 casos de irrigação = 0 (não irrigar)
        for i in range(50):
            timestamp = base_time + timedelta(hours=i*12)
            
            # Condições que NÃO devem irrigar
            umidade = np.random.uniform(60, 95)  # Alta umidade
            ph = np.random.choice([
                np.random.uniform(4.0, 5.5),  # Muito ácido
                np.random.uniform(8.0, 9.5)   # Muito básico
            ])
            fosforo = np.random.choice([0, 1])
            potassio = np.random.choice([0, 1])
            irrigacao = 0  # EXPLICITAMENTE não irrigar
            
            dados.append({
                'timestamp': int(timestamp.timestamp() * 1000),
                'datetime': timestamp,
                'umidade': round(umidade, 2),
                'ph': round(ph, 2),
                'fosforo': fosforo,
                'potassio': potassio,
                'irrigacao': irrigacao
            })
        
        # 50 casos de irrigação = 1 (irrigar)
        for i in range(50):
            timestamp = base_time + timedelta(hours=i*12 + 6)  # Offset de 6h
            
            # Condições que DEVEM irrigar
            umidade = np.random.uniform(5, 35)    # Baixa umidade
            ph = np.random.uniform(6.0, 7.5)     # pH ideal
            fosforo = np.random.choice([0, 1])
            potassio = np.random.choice([0, 1])
            irrigacao = 1  # EXPLICITAMENTE irrigar
            
            dados.append({
                'timestamp': int(timestamp.timestamp() * 1000),
                'datetime': timestamp,
                'umidade': round(umidade, 2),
                'ph': round(ph, 2),
                'fosforo': fosforo,
                'potassio': potassio,
                'irrigacao': irrigacao
            })
        
        print(f"✅ Gerados {len(dados)} registros balanceados")
        
        # Verificar distribuição
        irrigacao_dist = [d['irrigacao'] for d in dados]
        print(f"📊 Distribuição irrigação: 0={irrigacao_dist.count(0)}, 1={irrigacao_dist.count(1)}")
        
        # Limpar dados antigos
        print("🧹 Limpando dados antigos...")
        session.execute(text("DELETE FROM leitura_sensor WHERE sensor_id = 1"))
        session.commit()
        
        # Inserir novos dados BALANCEADOS
        print("📝 Inserindo dados balanceados...")
        
        for record in dados:
            # Umidade
            session.execute(text("""
                INSERT INTO leitura_sensor (sensor_id, valor, unidade, data_hora) 
                VALUES (1, :valor, '%', :data_hora)
            """), {
                "valor": str(record['umidade']),
                "data_hora": record['datetime']
            })
            
            # pH
            session.execute(text("""
                INSERT INTO leitura_sensor (sensor_id, valor, unidade, data_hora) 
                VALUES (1, :valor, 'pH', :data_hora)
            """), {
                "valor": str(record['ph']),
                "data_hora": record['datetime']
            })
            
            # Nutrientes + IRRIGAÇÃO
            nutrientes_irrigacao = {
                "P": record['fosforo'], 
                "K": record['potassio'],
                "irrigacao": record['irrigacao']  # ADICIONAR IRRIGAÇÃO AQUI
            }
            session.execute(text("""
                INSERT INTO leitura_sensor (sensor_id, valor, unidade, data_hora) 
                VALUES (1, :valor, 'ppm', :data_hora)
            """), {
                "valor": str(nutrientes_irrigacao),
                "data_hora": record['datetime']
            })
        
        session.commit()
        print(f"✅ {len(dados)} registros balanceados inseridos!")
        
        # Verificar inserção
        result = session.execute(text("SELECT COUNT(*) FROM leitura_sensor WHERE sensor_id = 1"))
        total = result.fetchone()[0]
        print(f"📊 Total leituras: {total}")
        
        # Verificar se irrigação foi inserida
        result = session.execute(text("""
            SELECT valor FROM leitura_sensor 
            WHERE unidade = 'ppm' AND valor LIKE '%irrigacao%'
            LIMIT 5
        """))
        
        print("🔍 Amostra dados irrigação inseridos:")
        for row in result:
            print(f"   {row[0]}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

def main():
    print("🌱 FarmTech Solutions - Correção de Dados de Irrigação")
    print("=" * 55)
    
    try:
        inserir_dados_irrigacao_diretos()
        
        print("\n🎉 Dados corrigidos!")
        print("🚀 Execute: python app/scripts/train_model.py --days 30 --min-samples 20")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())