import subprocess
import sys
import os
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()

if len(sys.argv) < 3:
    console.print("[red][!] Uso: python3 scanner.py <opcion> <target>[/red]")
    sys.exit()

opcion = sys.argv[1]
target = sys.argv[2]

comandos = {
    "1": ["nmap", "-F", target],
    "2": ["nmap", "-sV", target],
    "3": ["nmap", "-A", target],
    "4": ["nmap", "-sn", target],
}

nombres = {
    "1": "Escaneo rápido",
    "2": "Detección de versiones",
    "3": "Escaneo agresivo",
    "4": "Descubrimiento de hosts",
}

if opcion not in comandos:
    console.print("[red][!] Opción inválida[/red]")
    sys.exit()

console.print(
    Panel.fit(
        f"[bold cyan]Target:[/bold cyan] {target}\n"
        f"[bold cyan]Modo:[/bold cyan] {nombres[opcion]}",
        title="[bold red]Bayer Scan[/bold red]"
    )
)

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    console=console,
) as progress:

    task = progress.add_task(
        f"[cyan]Escaneando {target}...[/cyan]",
        total=None
    )

    resultado = subprocess.run(
        comandos[opcion],
        capture_output=True,
        text=True
    )

    progress.update(task, completed=True)

console.print("\n[bold green][+] Escaneo finalizado[/bold green]\n")

console.print(
    Panel(
        resultado.stdout,
        title="[bold green]Resultado Nmap[/bold green]",
        border_style="green"
    )
)

# Crear carpeta logs
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

# Fecha
fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Limpiar target
target_limpio = target.replace("/", "_").replace(":", "_")

# Nombre log
archivo_log = os.path.join(
    log_dir,
    f"{fecha}_{target_limpio}.txt"
)

# Guardar log
with open(archivo_log, "w") as archivo:
    archivo.write(resultado.stdout)

ruta_completa = os.path.abspath(archivo_log)

console.print(f"\n[bold green][+] Log guardado:[/bold green]")
console.print(f"[cyan]{ruta_completa}[/cyan]")

# Abrir automáticamente
subprocess.run(["xdg-open", ruta_completa])
