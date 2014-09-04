# coding: UTF-8
"""
Paquete: Normalizador de Direcciones GBA

Incluye todos los modulos necesarios para el uso del Normalizador de Direcciones del Gran Buenos Aires.
"""
from NormalizadorDireccionesGBA import NormalizadorDireccionesGBA as NDGBA

NormalizadorGBA = NDGBA
"""Alias de la clase NormalizadorDireccionesGBA provisto por conveniencia"""

VERSION = '1.0.0'
"""Versión de la aplicación"""
    
if __name__=='__main__':
    print VERSION
