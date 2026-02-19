"""
Dashboard Web para SentinelAPI
Interface visual para monitoramento de endpoints em tempo real
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from threading import Thread

from flask import Flask, jsonify, render_template

from app.core.logger import setup_logger
from app.core.models import EndpointConfig
from app.monitor.health_checker import HealthChecker

logger = setup_logger(__name__)

app = Flask(__name__)

# Estado global do monitoramento
monitoring_data = {
    "results": [],
    "last_check": None,
    "stats": {
        "total_endpoints": 0,
        "healthy": 0,
        "degraded": 0,
        "down": 0
    },
    "history": []  # Histórico limitado dos últimos checks
}


def load_endpoints(file_path: str = "endpoints.json") -> list[EndpointConfig]:
    """Carrega endpoints do arquivo de configuração"""
    config_file = Path(file_path)
    
    if not config_file.exists():
        logger.warning(f"Arquivo de configuração {file_path} não encontrado")
        return []
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        endpoints = [EndpointConfig(**endpoint) for endpoint in data]
        logger.info(f"Carregados {len(endpoints)} endpoints para monitoramento")
        return endpoints
        
    except Exception as e:
        logger.error(f"Erro ao carregar endpoints: {e}")
        return []


async def monitor_loop():
    """Loop de monitoramento assíncrono"""
    endpoints = load_endpoints()
    
    if not endpoints:
        logger.error("Nenhum endpoint configurado para monitoramento")
        return
    
    while True:
        try:
            async with HealthChecker(max_retries=2) as checker:
                results = await checker.check_multiple(endpoints)
                
                # Atualizar dados globais
                monitoring_data["results"] = [
                    {
                        "name": r.endpoint,
                        "url": next((e.url for e in endpoints if e.name == r.endpoint), ""),
                        "status": r.status,
                        "response_time": round(r.response_time, 2),
                        "status_code": r.status_code,
                        "error_message": r.error_message,
                        "timestamp": datetime.now().isoformat()
                    }
                    for r in results
                ]
                
                monitoring_data["last_check"] = datetime.now().isoformat()
                
                # Calcular estatísticas
                stats = monitoring_data["stats"]
                stats["total_endpoints"] = len(results)
                stats["healthy"] = sum(1 for r in results if r.status == "healthy")
                stats["degraded"] = sum(1 for r in results if r.status == "degraded")
                stats["down"] = sum(1 for r in results if r.status == "down")
                
                # Adicionar ao histórico (manter últimos 50 registros)
                history_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "results": [
                        {
                            "name": r.endpoint,
                            "status": r.status,
                            "response_time": round(r.response_time, 2)
                        }
                        for r in results
                    ]
                }
                monitoring_data["history"].append(history_entry)
                if len(monitoring_data["history"]) > 50:
                    monitoring_data["history"].pop(0)
                
                logger.info(f"Check completo: {stats['healthy']} healthy, {stats['degraded']} degraded, {stats['down']} down")
                
        except Exception as e:
            logger.error(f"Erro no loop de monitoramento: {e}")
        
        # Aguardar antes do próximo check (30 segundos)
        await asyncio.sleep(30)


def run_monitor_thread():
    """Executar loop de monitoramento em thread separada"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor_loop())


@app.route("/")
def index():
    """Página principal do dashboard"""
    return render_template("dashboard.html")


@app.route("/api/status")
def api_status():
    """API endpoint para obter status atual"""
    return jsonify(monitoring_data)


@app.route("/api/history")
def api_history():
    """API endpoint para obter histórico"""
    return jsonify({
        "history": monitoring_data["history"][-20:]  # Últimos 20 registros
    })


def main():
    """Iniciar dashboard web"""
    # Iniciar thread de monitoramento
    monitor_thread = Thread(target=run_monitor_thread, daemon=True)
    monitor_thread.start()
    
    logger.info("=== Dashboard SentinelAPI ===")
    logger.info("Acesse: http://localhost:5000")
    logger.info("Monitoramento iniciado...")
    
    # Iniciar servidor Flask
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
