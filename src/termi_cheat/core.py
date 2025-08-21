"""
Módulo core de Termi-Cheat - Lógica principal
"""

import json
import mmap
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class TermiCheat:
    """Clase principal de Termi-Cheat"""
    
    def __init__(self):
        self.cheats_dir = Path(__file__).parent / "cheats"
        self.cache: Dict[str, Dict] = {}
        self.cache_size_limit = 10
    
    def load_cheat_file_cached(self, command: str) -> Optional[Dict]:
        """Cargar archivo JSON usando cache"""
        if command in self.cache:
            return self.cache[command]
        
        cheat_file = self.cheats_dir / f"{command.lower()}.json"
        
        if not cheat_file.exists():
            return None
        
        try:
            with open(cheat_file, 'r', encoding='utf-8') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    cheats = json.loads(mm.read().decode('utf-8'))
            
            # Gestión simple de cache
            if len(self.cache) >= self.cache_size_limit:
                self.cache.pop(next(iter(self.cache)))
            
            self.cache[command] = cheats
            return cheats
            
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Error al cargar {cheat_file}: {e}", file=sys.stderr)
            return None
    
    def filter_and_display(self, cheats: Dict, filter_str: Optional[str] = None) -> None:
        """Filtrar y mostrar resultados"""
        found_results = False
        
        for topic, examples in cheats.items():
            if filter_str and filter_str.lower() not in topic.lower():
                continue
                
            found_results = True
            print(f"🔹 {topic}")
            
            for example in examples:
                cmd = example.get('cmd', 'N/A')
                desc = example.get('desc', 'Sin descripción')
                print(f"  - {cmd}: {desc}")
        
        if not found_results:
            msg = "❌ No se encontraron resultados"
            if filter_str:
                msg += f" para '{filter_str}'"
            print(msg)
    
    def search_across_commands(self, search_term: str, max_results: int = 5) -> None:
        """Búsqueda a través de todos los comandos"""
        print(f"🔍 Buscando '{search_term}' en todos los comandos...\n")
        
        results_found = False
        search_lower = search_term.lower()
        
        for json_file in self.cheats_dir.glob("*.json"):
            command_name = json_file.stem
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    cheats = json.load(f)
                    
                command_has_results = False
                printed_header = False
                
                for topic, examples in cheats.items():
                    topic_matches = search_lower in topic.lower()
                    relevant_examples = []
                    
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
                    print()
                    
            except (json.JSONDecodeError, IOError):
                continue
        
        if not results_found:
            print("❌ No se encontraron resultados en ningún comando")
    
    def list_available_commands(self) -> None:
        """Listar comandos disponibles"""
        print("📋 Comandos disponibles:\n")
        
        commands = []
        for json_file in self.cheats_dir.glob("*.json"):
            commands.append(json_file.stem)
        
        commands.sort()
        for i, cmd in enumerate(commands, 1):
            end_char = "\n" if i % 3 == 0 else "\t\t"
            print(f"• {cmd:12}", end=end_char)
        
        if len(commands) % 3 != 0:
            print()