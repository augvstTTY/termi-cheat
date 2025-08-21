#!/usr/bin/env python3
"""
CLI de Termi-Cheat - Interfaz de línea de comandos
"""

import sys
import argparse
from .core import TermiCheat

def setup_argparse() -> argparse.ArgumentParser:
    """Configurar parser de argumentos"""
    parser = argparse.ArgumentParser(
        description="Termi-cheat - Referencia rápida de comandos terminal",
        usage="%(prog)s [OPCIONES] <comando>"
    )
    
    parser.add_argument(
        'command', 
        nargs='?', 
        help='Nombre del comando (ej: git, docker, linux)'
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
        version='%(prog)s 1.0.0'
    )
    
    return parser

def main() -> None:
    """Función principal"""
    parser = setup_argparse()
    args = parser.parse_args()
    
    tc = TermiCheat()
    
    # Modo búsqueda global
    if args.search:
        tc.search_across_commands(args.search)
        return
    
    # Modo listar comandos
    if args.list:
        tc.list_available_commands()
        return
    
    # Modo normal: mostrar comando específico
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cheats = tc.load_cheat_file_cached(args.command)
    if cheats is None:
        print(f"❌ No se encontró referencia para '{args.command}'")
        print("💡 Use '--list' para ver comandos disponibles")
        sys.exit(1)
    
    print(f"\n📖 {args.command.upper()} REFERENCIA RÁPIDA\n")
    tc.filter_and_display(cheats, args.filter)

if __name__ == "__main__":
    main()