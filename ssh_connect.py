#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import json
import socket
from typing import List, Optional

PROFILES_FILE = "ssh_profiles.json"


# ==========================================================
# Utils
# ==========================================================

def puerto_disponible(servidor: str, puerto: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((servidor, puerto), timeout=timeout):
            return True
    except Exception:
        return False


def cargar_perfil(nombre: str):
    if not os.path.exists(PROFILES_FILE):
        print("No existe archivo de perfiles.")
        sys.exit(1)

    with open(PROFILES_FILE, "r") as f:
        perfiles = json.load(f)

    if nombre not in perfiles:
        print(f"Perfil '{nombre}' no encontrado.")
        sys.exit(1)

    return perfiles[nombre]


# ==========================================================
# Core SSH
# ==========================================================

def ejecutar_conexiones(
    usuario: str,
    servidor: str,
    puertos: List[int],
    key_path: Optional[str],
    paralelo: bool,
):
    print("\n⚠️  Nota técnica:")
    print("Cada conexión SSH utiliza UN puerto TCP.")
    print("No es posible múltiples puertos en una sola sesión.\n")

    procesos = []

    for puerto in puertos:

        print(f"Verificando puerto {puerto}...")

        if not puerto_disponible(servidor, puerto):
            print(f"Puerto {puerto} no disponible. Se omite.")
            continue

        comando = ["ssh", "-p", str(puerto)]

        if key_path:
            comando.extend(["-i", key_path])

        comando.append(f"{usuario}@{servidor}")

        print(f"Conectando a {servidor}:{puerto}")

        if paralelo:
            proceso = subprocess.Popen(comando)
            procesos.append(proceso)
        else:
            subprocess.run(comando)

    if paralelo:
        try:
            for p in procesos:
                p.wait()
        except KeyboardInterrupt:
            print("\nCancelando conexiones...")
            for p in procesos:
                p.terminate()
            sys.exit(0)


# ==========================================================
# CLI
# ==========================================================

def main():
    parser = argparse.ArgumentParser(
        prog="andres-ssh",
        description="Cliente SSH avanzado multi-puerto",
    )

    parser.add_argument("--profile", help="Nombre del perfil")
    parser.add_argument("--parallel", action="store_true", help="Ejecutar en paralelo")

    parser.add_argument("--user", help="Usuario SSH")
    parser.add_argument("--host", help="Servidor")
    parser.add_argument("--ports", help="Puertos separados por coma")
    parser.add_argument("--key", help="Ruta a llave privada")

    args = parser.parse_args()

    if args.profile:
        perfil = cargar_perfil(args.profile)
        usuario = perfil["usuario"]
        servidor = perfil["servidor"]
        puertos = perfil["puertos"]
        key_path = perfil.get("key_path")
    else:
        if not all([args.user, args.host, args.ports]):
            parser.error("Debe usar --profile o especificar --user --host --ports")

        usuario = args.user
        servidor = args.host
        puertos = [int(p.strip()) for p in args.ports.split(",")]
        key_path = args.key

    ejecutar_conexiones(
        usuario,
        servidor,
        puertos,
        key_path,
        args.parallel,
    )


if __name__ == "__main__":
    main()