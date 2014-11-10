# coding: UTF-8
"""
Paquete: Normalizador de Direcciones AMBA

Incluye todos los modulos necesarios para el uso del Normalizador de Direcciones del Gran Buenos Aires.
"""
from NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA as NDAMBA

NormalizadorAMBA = NDAMBA
"""Alias de la clase NormalizadorDireccionesAMBA provisto por conveniencia"""

VERSION = '1.0.0'
"""Versión de la aplicación"""
    
if __name__=='__main__':
    print VERSION
