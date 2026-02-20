#!/usr/bin/env python3
"""
Programa para conectarse a servidores Linux mediante SSH
con puertos específicos permitidos (1, 2 o 15).
"""

import subprocess
import sys
import os


def get_user_input() -> tuple[str, str, int]:
    """
    Solicita al usuario el nombre de usuario, servidor y puerto.
    
    Returns:
        tuple: (usuario, servidor, puerto)
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
            seleccion = input(f"\nSeleccione el puerto (1-{len(puertos_permitidos)}): ").strip()
            indice = int(seleccion) - 1
            if 0 <= indice < len(puertos_permitidos):
                puerto = puertos_permitidos[indice]
                return usuario, servidor, puerto
            else:
                print(f"Error: Por favor seleccione un número entre 1 y {len(puertos_permitidos)}.")
        except ValueError:
            print("Error: Por favor ingrese un número válido.")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            sys.exit(0)


def connect_ssh(usuario: str, servidor: str, puerto: int):
    """
    Establece una conexión SSH con el servidor usando el comando ssh del sistema.
    
    Args:
        usuario: Nombre de usuario
        servidor: Dirección del servidor
        puerto: Puerto SSH
    """
    print(f"\nConectando a {usuario}@{servidor}:{puerto}...")
    print("(Se le pedirá la contraseña cuando se establezca la conexión)\n")
    
    # Construir comando SSH
    comando_ssh = [
        'ssh',
        '-p', str(puerto),
        f'{usuario}@{servidor}'
    ]
    
    try:
        # Ejecutar SSH en modo interactivo (conecta directamente al terminal)
        # Esto permite una experiencia SSH completa y nativa
        subprocess.run(comando_ssh, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nError al conectar: El comando SSH falló con código {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: El comando 'ssh' no está disponible en el sistema.")
        print("Por favor, instale OpenSSH o use una alternativa.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nConexión cancelada.")
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
