#!/usr/bin/env python3
"""
termi-cheat - Herramienta ultra-optimizada de referencia rápida para comandos
Versión: 2.0 - Bajo consumo de memoria y máxima velocidad
"""

import json
import sys
import os
import mmap
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

# Configuración de rutas
CHEATS_DIR = Path(__file__).parent / "cheats"
CACHE: Dict[str, Dict] = {}  # Cache simple en memoria
CACHE_SIZE_LIMIT = 10  # Límite de archivos en cache

def load_cheat_file_cached(command: str) -> Optional[Dict]:
    """
    Carga el archivo JSON usando cache y técnicas de bajo consumo.
    
    Args:
        command: Nombre del comando a buscar
        
    Returns:
        Diccionario con los datos o None si no existe
    """
    # Verificar cache primero
    if command in CACHE:
        return CACHE[command]
    
    cheat_file = CHEATS_DIR / f"{command.lower()}.json"
    
    if not cheat_file.exists():
        return None
    
    try:
        # Técnica de bajo consumo: mapeado de memoria para archivos grandes
        with open(cheat_file, 'r', encoding='utf-8') as f:
            # Usar mmap para acceso eficiente a archivos grandes
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                # Cargar directamente desde el mapeo de memoria
                cheats = json.loads(mm.read().decode('utf-8'))
        
        # Gestión simple de cache (LRU-like)
        if len(CACHE) >= CACHE_SIZE_LIMIT:
            # Eliminar el primer elemento (approximación LRU)
            CACHE.pop(next(iter(CACHE)))
        
        CACHE[command] = cheats
        return cheats
        
    except (json.JSONDecodeError, IOError, OSError) as e:
        print(f"Error al cargar {cheat_file}: {e}", file=sys.stderr)
        return None

def filter_and_display(cheats: Dict, filter_str: Optional[str] = None) -> None:
    """
    Filtra y muestra los resultados de manera eficiente.
    
    Args:
        cheats: Diccionario con los datos del comando
        filter_str: Texto para filtrar (opcional)
    """
    found_results = False
    
    for topic, examples in cheats.items():
        # Filtrado eficiente (evitar lower() si no hay filtro)
        if filter_str and filter_str.lower() not in topic.lower():
            continue
            
        found_results = True
        print(f"🔹 {topic}")
        
        # Mostrar ejemplos (optimizado para rendimiento)
        for example in examples:
            cmd = example.get('cmd', 'N/A')
            desc = example.get('desc', 'Sin descripción')
            print(f"  - {cmd}: {desc}")
    
    if not found_results:
        print("❌ No se encontraron resultados" + 
              (f" para '{filter_str}'" if filter_str else ""))

def search_across_commands(search_term: str, max_results: int = 5) -> None:
    """
    Búsqueda eficiente a través de todos los archivos de comandos.
    
    Args:
        search_term: Término de búsqueda
        max_results: Límite de resultados por comando
    """
    print(f"🔍 Buscando '{search_term}' en todos los comandos...\n")
    
    results_found = False
    search_lower = search_term.lower()
    
    # Iterar eficientemente sobre archivos JSON
    for json_file in CHEATS_DIR.glob("*.json"):
        command_name = json_file.stem
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                cheats = json.load(f)
                
            command_has_results = False
            printed_header = False
            
            for topic, examples in cheats.items():
                topic_matches = search_lower in topic.lower()
                relevant_examples = []
                
                # Buscar en ejemplos
                for example in examples:
                    cmd_match = search_lower in example.get('cmd', '').lower()
                    desc_match = search_lower in example.get('desc', '').lower()
                    
                    if topic_matches or cmd_match or desc_match:
                        relevant_examples.append(example)
                        if len(relevant_examples) >= max_results:
                            break
                
                if relevant_examples:
                    results_found = True
                    if not printed_header:
                        print(f"📖 {command_name.upper()}:")
                        printed_header = True
                        command_has_results = True
                    
                    print(f"  🔹 {topic}")
                    for example in relevant_examples:
                        print(f"    - {example.get('cmd', 'N/A')}")
            
            if command_has_results:
                print()  # Espacio entre comandos
                
        except (json.JSONDecodeError, IOError):
            continue  # Saltar archivos corruptos
    
    if not results_found:
        print("❌ No se encontraron resultados en ningún comando")

def setup_argparse() -> argparse.ArgumentParser:
    """Configura el parser de argumentos con mejor rendimiento."""
    parser = argparse.ArgumentParser(
        description="Termi-cheat - Referencia rápida de comandos terminal",
        usage="%(prog)s [OPCIONES] <comando>"
    )
    
    parser.add_argument(
        'command', 
        nargs='?', 
        help='Nombre del comando (ej: git, docker)'
    )
    
    parser.add_argument(
        '-f', '--filter',
        metavar='TEXTO',
        help='Filtrar resultados por texto'
    )
    
    parser.add_argument(
        '-s', '--search',
        metavar='TÉRMINO',
        help='Buscar en todos los comandos'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='Listar todos los comandos disponibles'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 2.0 (optimizado)'
    )
    
    return parser

def list_available_commands() -> None:
    """Lista todos los comandos disponibles de manera eficiente."""
    print("📋 Comandos disponibles:\n")
    
    commands = []
    for json_file in CHEATS_DIR.glob("*.json"):
        commands.append(json_file.stem)
    
    # Ordenar y mostrar en columnas para mejor legibilidad
    commands.sort()
    for i, cmd in enumerate(commands, 1):
        end_char = "\n" if i % 3 == 0 else "\t\t"
        print(f"• {cmd:12}", end=end_char)
    
    if len(commands) % 3 != 0:
        print()  # Nueva línea final

def main() -> None:
    """Función principal optimizada."""
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Modo búsqueda global (--search)
    if args.search:
        search_across_commands(args.search)
        return
    
    # Modo listar comandos (--list)
    if args.list:
        list_available_commands()
        return
    
    # Modo normal: mostrar comando específico
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cheats = load_cheat_file_cached(args.command)
    if cheats is None:
        print(f"❌ No se encontró referencia para '{args.command}'")
        print("💡 Use '--list' para ver comandos disponibles")
        sys.exit(1)
    
    print(f"\n📖 {args.command.upper()} REFERENCIA RÁPIDA\n")
    filter_and_display(cheats, args.filter)

if __name__ == "__main__":
    # Ejecución directa sin overhead de funciones
    main()
