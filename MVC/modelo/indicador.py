# modelo/indicador.py
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class IndicadorEconomico:
    """
    Clase para la Deserialización de los datos del Indicador (UF) obtenidos
    desde la API externa (mindicador.cl).
    """
    
    def __init__(self, codigo: str, fecha: str, valor: float) -> None:
        """
        Inicializa una instancia de IndicadorEconomico.
        
        Args:
            codigo (str): Código del indicador (ej: "uf")
            fecha (str): Fecha de la consulta (YYYY-MM-DDTHH:MM:SS.ZZZ)
            valor (float): Valor del indicador en la fecha consultada
        """
        self._codigo = codigo
        self._fecha = fecha
        self._valor = valor

    # Getters
    def getCodigo(self) -> str:
        return self._codigo
    
    def getFecha(self) -> str:
        """Obtiene la fecha (string completo con hora) del indicador."""
        return self._fecha

    def getValor(self) -> float:
        """Obtiene el valor numérico (float) del indicador."""
        return self._valor
    
    def getFechaCorta(self) -> str:
        """Obtiene la fecha en formato YYYY-MM-DD."""
        try:
            return self._fecha.split('T')[0]
        except Exception:
            return self._fecha

    def __str__(self) -> str:
        return f"Indicador {self._codigo} - Fecha: {self.getFechaCorta()} - Valor: ${self._valor:,.2f}"

    @classmethod
    def from_json(cls, data_json: dict) -> Optional['IndicadorEconomico']:
        """
        Método de fábrica (Deserialización) para crear la instancia
        desde el diccionario JSON de la API.
        
        Asume la estructura estándar de mindicador.cl:
        {"serie": [ {"fecha": "...", "valor": X.X} ]}
        
        Args:
            data_json (dict): Diccionario deserializado (respuesta de requests.json())
        
        Returns:
            Optional[IndicadorEconomico]: Objeto Python creado con la data.
        """
        try:
            # La API devuelve una lista 'serie'
            if 'serie' not in data_json or not data_json['serie']:
                logger.warning("Respuesta JSON no contiene 'serie' o está vacía")
                return None
                
            primer_indicador = data_json['serie'][0]
            
            return cls(
                codigo=data_json.get('codigo', 'uf'),
                fecha=primer_indicador['fecha'],
                valor=float(primer_indicador['valor'])
            )
        except (KeyError, IndexError, TypeError, ValueError) as e:
            logger.error("Error en la estructura JSON del Indicador: %s", e)
            raise ValueError(f"Error en la estructura JSON del Indicador: {e}")