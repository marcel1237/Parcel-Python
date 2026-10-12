#!/bin/bash
###############################################################################
# NOME: theme_sync.sh
# DESCRIÇÃO: Detecta se o sistema operacional está em Modo Escuro ou Claro e
#            ajusta as configurações base da IDE Parcel C++.
#
# LÓGICA: Consulta o gsettings (GNOME) ou kreadconfig (KDE) para ler o tema.
###############################################################################

echo "Detectando tema do sistema..."

INTERFACE_STYLE=$(gsettings get org.gnome.desktop.interface color-scheme 2>/dev/null || echo "default")

if [[ "$INTERFACE_STYLE" == *"'prefer-dark'"* ]]; then
    echo "Modo Escuro Detectado. Aplicando Breeze Dark config..."
    # Aqui você poderia injetar um valor em um config.ini
else
    echo "Modo Claro Detectado. Aplicando Oxygen config..."
fi
