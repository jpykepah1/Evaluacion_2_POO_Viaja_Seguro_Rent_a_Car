# servicio/indicador_service.py
import requests
from modelo.indicador import IndicadorEconomico
from datetime import datetime, timedelta
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class IndicadorService:
    """
    Servicio para obtener indicadores económicos (UF) de mindicador.cl.
    Implementa manejo de excepciones y búsqueda de fecha próxima.
    """
    
    BASE_URL: str = "https://mindicador.cl/api"
    
    @staticmethod
    def obtener_uf_por_fecha(fecha_str: str) -> Optional[IndicadorEconomico]:
        """
        Consulta el valor de la UF para una fecha específica.
        Si la fecha no tiene valor (ej: fin de semana), busca
        la fecha anterior más próxima disponible (Requisito ES3).
        
        Args:
            fecha_str (str): Fecha en formato YYYY-MM-DD.
        
        Returns:
            Optional[IndicadorEconomico]: Objeto IndicadorEconomico con el valor de la UF, 
                                          o None si no se pudo obtener.
        """
        
        fecha_dt: datetime
        try:
            fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d') 
        except ValueError:
            logger.error("Fecha ingresada con formato incorrecto: %s", fecha_str)
            print(f"❌ Error: Formato de fecha inválido {fecha_str}. Use YYYY-MM-DD.")
            return None

        # Intentar buscar la UF hasta 7 días hacia atrás
        max_intentos = 7 
        
        for i in range(max_intentos):
            fecha_consulta_dt = fecha_dt - timedelta(days=i)
            fecha_formato_api = fecha_consulta_dt.strftime('%d-%m-%Y')
            url = f"{IndicadorService.BASE_URL}/uf/{fecha_formato_api}"
            
            logger.info("Intentando consultar UF (Intento %d/%d): %s", i+1, max_intentos, url)
            
            try:
                # 1. Consumo de API (Requisito 3.1.2)
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Lanza HTTPError para 4xx/5xx

                # 2. Deserialización
                data_json = response.json()
                
                # 3. Creación de objeto vía deserialización (Requisito 3.1.3)
                indicador = IndicadorEconomico.from_json(data_json)

                if indicador:
                    logger.info("UF encontrada para la fecha %s: %s", 
                                fecha_consulta_dt.strftime('%Y-%m-%d'), indicador.getValor())
                    return indicador
                else:
                    # La API respondió pero la data estaba vacía
                    logger.warning("Respuesta de API vacía para %s. Intentando día anterior.", fecha_formato_api)

            # 3. Manejo de Excepciones (Requisito 3.1.2)
            except requests.exceptions.HTTPError as e:
                # 404 Not Found (Típico si la fecha no tiene indicador)
                if response.status_code == 404:
                    logger.warning("UF no encontrada para %s. Buscando fecha anterior.", fecha_formato_api)
                else:
                    logger.error("Error HTTP al consultar API: %s", str(e))
                    print(f"❌ Error de servidor: {response.status_code}")
                    return None
                    
            except requests.exceptions.ConnectionError:
                logger.error("Error de conexión al API de indicadores.")
                print("❌ Error de Conexión: No se pudo conectar con el servicio de indicadores.")
                return None
            
            except requests.exceptions.Timeout:
                logger.error("Tiempo de espera agotado al consultar API.")
                print("❌ Error de Timeout: El servicio tardó demasiado en responder.")
                return None
            
            except (ValueError, requests.exceptions.JSONDecodeError) as e:
                logger.error("Error en Deserialización o estructura JSON: %s", str(e))
                print("❌ Error: La respuesta de la API no es un JSON válido.")
                return None
                
            except Exception as e:
                logger.error("Error inesperado en servicio UF: %s", str(e))
                print(f"❌ Ocurrió un error inesperado al buscar la UF: {str(e)}")
                return None

        logger.warning("No se encontró valor de UF en los últimos %d días.", max_intentos)
        print(f"❌ Advertencia: No se encontró un valor de UF para la fecha {fecha_str} ni en los días cercanos.")
        return None