#!/usr/bin/env python3
"""
Programa para conectarse a servidores Linux mediante SSH
con puertos específicos permitidos (1, 2 o 15).
"""

import subprocess
import sys
import os


def get_user_input() -> tuple[str, str, list[int]]:
    """
    Solicita al usuario el nombre de usuario, servidor y puerto.
    
    Returns:
        tuple: (usuario, servidor, puertos)
    """
    # Solicitar usuario
    usuario = input("Usuario: ").strip()
    if not usuario:
        print("Error: El usuario no puede estar vacío.")
        sys.exit(1)
    
    # Solicitar servidor
    servidor = input("Servidor: ").strip()
    if not servidor:
        print("Error: El servidor no puede estar vacío.")
        sys.exit(1)
    
    # Mostrar opciones de puerto y solicitar selección
    puertos_permitidos = [1, 2, 15]
    print("\nPuertos disponibles:")
    for i, puerto in enumerate(puertos_permitidos, 1):
        print(f"  {i}. Puerto {puerto}")
    
    while True:
        try:
            seleccion = input(
                f"\nSeleccione uno o más puertos separados por coma (ej: 1,3): "
            ).strip()

            indices = [int(s.strip()) - 1 for s in seleccion.split(",") if s.strip()]
            puertos_seleccionados = []

            for indice in indices:
                if 0 <= indice < len(puertos_permitidos):
                    puertos_seleccionados.append(puertos_permitidos[indice])
                else:
                    raise ValueError

            if not puertos_seleccionados:
                raise ValueError

            return usuario, servidor, puertos_seleccionados

        except ValueError:
            print(
                f"Error: Seleccione números válidos entre 1 y {len(puertos_permitidos)}, separados por coma."
            )
        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            sys.exit(0)


def connect_ssh(usuario: str, servidor: str, puertos: list[int]):
    """
    Establece una conexión SSH con el servidor usando el comando ssh del sistema.
    
    Args:
        usuario: Nombre de usuario
        servidor: Dirección del servidor
        puertos: Lista de puertos SSH
    """
    print(f"\nConectando a {usuario}@{servidor} en múltiples puertos...")
    print("(Se le pedirá la contraseña para cada conexión)\n")

    procesos = []

    for puerto in puertos:
        print(f"Iniciando conexión en puerto {puerto}...")
        comando_ssh = [
            "ssh",
            "-p",
            str(puerto),
            f"{usuario}@{servidor}",
        ]

        try:
            # Usamos Popen para permitir múltiples sesiones simultáneas
            proceso = subprocess.Popen(comando_ssh)
            procesos.append(proceso)
        except FileNotFoundError:
            print("\nError: El comando 'ssh' no está disponible en el sistema.")
            print("Por favor, instale OpenSSH o use una alternativa.")
            sys.exit(1)

    # Esperar a que todos los procesos terminen
    try:
        for proceso in procesos:
            proceso.wait()
    except KeyboardInterrupt:
        print("\n\nConexiones canceladas.")
        for proceso in procesos:
            proceso.terminate()
        sys.exit(0)


def main():
    """Función principal del programa."""
    print("="*50)
    print("Cliente SSH - Conexión a servidor Linux")
    print("="*50)
    
    # Obtener datos del usuario
    usuario, servidor, puerto = get_user_input()
    
    # Conectar al servidor
    connect_ssh(usuario, servidor, puerto)


if __name__ == "__main__":
    main()
