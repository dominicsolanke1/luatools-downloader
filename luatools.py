import os
import sys
import json
import time
import shutil
import locale
import re
import ctypes
import subprocess
import datetime
import urllib.request
import winreg

L = {}
millDir = ""
Name = ""
Link = ""

COLORS = {
    "Green": "\033[92m",
    "Cyan": "\033[96m",
    "Red": "\033[91m",
    "Yellow": "\033[93m",
    "Magenta": "\033[95m",
    "DarkGray": "\033[90m",
    "Reset": "\033[0m",
    "White": "\033[97m"
}

LogColors = {
    "OK": "Green",
    "INFO": "Cyan",
    "ERR": "Red",
    "WARN": "Yellow",
    "LOG": "Magenta",
    "AUX": "DarkGray"
}

def init_ansi():
    try:
        kernel32 = ctypes.windll.kernel32
        h_stdout = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(h_stdout, ctypes.byref(mode)):
            kernel32.SetConsoleMode(h_stdout, mode.value | 0x0004)
    except Exception:
        pass

init_ansi()

def write_log(log_type, message, no_newline=False):
    color = COLORS.get(LogColors.get(log_type, "Reset"), COLORS["Reset"])
    reset = COLORS["Reset"]
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    
    end_char = "" if no_newline else "\n"
    start_char = "\r" if no_newline else ""
    
    sys.stdout.write(f"{start_char}[{ts}] {color}[{log_type}] {message}{reset}{end_char}")
    sys.stdout.flush()

def get_default_strings(culture):
    tables = {
        "en": {
            "Title": "Luatools plugin installer | .gg/luatools",
            "SteamRegNotFound": "Steam registry key not found. Is Steam installed?",
            "SteamKilling": "Stopping Steam",
            "SteamKilled": "Steam stopped",
            "SteamtoolsFound": "Steamtools already installed",
            "SteamtoolsNotFound": "Steamtools not found",
            "SteamtoolsInstalling": "Installing Steamtools",
            "SteamtoolsInstalled": "Steamtools installed",
            "SteamtoolsRetrying": "Steamtools installation failed, retrying...",
            "SteamtoolsFailed": "Steamtools installation failed after 5 attempts",
            "MillenniumNotFound": "Millennium not found",
            "MillenniumCountdown": "Millennium will be installed in {0} second(s)... Press any key to cancel",
            "MillenniumCancelled": "Installation cancelled by user",
            "MillenniumInstalling": "Installing Millennium",
            "MillenniumInstalled": "Millennium installed",
            "MillenniumAlready": "Millennium already installed",
            "MillenniumFirstBoot": "Steam startup may be slower on first boot -- let it sit.",
            "PluginUpdating": "Plugin already installed, updating",
            "PluginDownloading": "Downloading {0}",
            "PluginDownloadFailed": "Failed to download {0}",
            "PluginExtracting": "Extracting {0}",
            "PluginExtractFailed": "Extraction failed, trying built-in Expand-Archive",
            "PluginInstalled": "{0} installed",
            "PluginEnabled": "Plugin enabled",
            "RemovingBeta": "Cleaning up beta flag",
            "RemovingCfg": "Cleaning up steam.cfg",
            "RemovingForceX86": "Cleaning up ForceX86 registry flags (32 bits)",
            "StartingSteam": "Starting Steam",
            "UpdateCheckDisabled": "Millennium auto-updates disabled to prevent startup hangs.",
            "UpdateCheckManual": "Check for Millennium updates manually if you want the latest.",
            "ErrorTitle": "Luatools installer - ERROR",
            "ErrorHeader": "AN ERROR OCCURRED",
            "ErrorBody": "The Luatools plugin installer encountered a problem and could not complete. This is often caused by your ISP blocking the download servers we use.",
            "ErrorFaq": "Visit the server (.gg/luatools) for more information & fixes.",
            "ErrorExit": "Press Enter to exit.",
            "MenuHeader": "Luatools Installation Menu",
            "MenuOptionInstall": "1. Install",
            "MenuOptionUninstall": "2. Uninstall / Delete",
            "MenuOptionLang": "3. Change Language",
            "MenuOptionExit": "4. Exit",
            "MenuPrompt": "Please choose an option (1, 2, 3, or 4): ",
            "LangPrompt": "Select language:\n1. English (en)\n2. Portuguese (pt-BR)\n3. Spanish (es)\n4. French (fr)\n5. Turkish (tr)\nChoice (1-5): ",
            "ProcessCompletePrompt": "\nProcess completed. Press Enter to return to the menu...",
            "Uninstalling": "Deleting all installed files...",
            "Uninstalled": "All Luatools, Millennium, and Steamtools files have been completely deleted!"
        },
        "pt-BR": {
            "Title": "Instalador do Luatools | .gg/luatools",
            "SteamRegNotFound": "Steam não encontrada no registro. Sua Steam ta instalada?",
            "SteamKilling": "Parando a Steam",
            "SteamKilled": "Steam Encerrada",
            "SteamtoolsFound": "Steamtools ja instalado",
            "SteamtoolsNotFound": "Steamtools não encontrado",
            "SteamtoolsInstalling": "Instalando Steamtools",
            "SteamtoolsInstalled": "Steamtools instalado",
            "SteamtoolsRetrying": "Falha ao instalar Steamtools, tentando denovo...",
            "SteamtoolsFailed": "Falha ao instalar Steamtools após 5 tentativas",
            "MillenniumNotFound": "Millennium não encontrado",
            "MillenniumCountdown": "Millennium vai ser instalado em {0} segundo(s)... Aperte qualquer tecla pra cancelar",
            "MillenniumCancelled": "Instalação cancelada pelo usuário",
            "MillenniumInstalling": "Instalando Millennium",
            "MillenniumInstalled": "Millennium instalado",
            "MillenniumAlready": "O Millennium ja está instalado",
            "MillenniumFirstBoot": "A Steam pode demorar um pouco pra abrir pela primeira vez -- deixa rolar.",
            "PluginUpdating": "Plugin já instalado, atualizando",
            "PluginDownloading": "Baixando {0}",
            "PluginDownloadFailed": "Falha ao baixar {0}",
            "PluginExtracting": "Extraindo {0}",
            "PluginExtractFailed": "Falha ao extrair, tentando via Expand-Archive",
            "PluginInstalled": "{0} instalado",
            "PluginEnabled": "Plugin habilitado",
            "RemovingBeta": "Limpando flag de beta da Steam",
            "RemovingCfg": "Apagando steam.cfg",
            "RemovingForceX86": "limpando as flags de registro do ForceX86 (32 bits)",
            "StartingSteam": "Abrindo a Steam",
            "UpdateCheckDisabled": "Atualizações automáticas do Millennium desabilitadas pra evitar travamentos ao iniciar",
            "UpdateCheckManual": "Verifique manualmente por atualizações do Millennium caso você queira a ultima versão",
            "ErrorTitle": "Instalador do Luatools - ERRO",
            "ErrorHeader": "OCORREU UM ERRO",
            "ErrorBody": "O instalador do Luatools encontrou um problema e não pôde ser concluído. Isso geralmente é causado pela tua internet bloqueando nossos servidores de Download",
            "ErrorFaq": "Visite o servidor (.gg/luatools) pra mais informações e detalhes em como consertar",
            "ErrorExit": "Aperte qualquer botão pra sair.",
            "MenuHeader": "Menu de Instalação do Luatools",
            "MenuOptionInstall": "1. Instalar",
            "MenuOptionUninstall": "2. Desinstalar / Excluir",
            "MenuOptionLang": "3. Alterar idioma",
            "MenuOptionExit": "4. Sair",
            "MenuPrompt": "Por favor, escolha uma opção (1, 2, 3 ou 4): ",
            "LangPrompt": "Selecionar idioma:\n1. English (en)\n2. Portuguese (pt-BR)\n3. Spanish (es)\n4. French (fr)\n5. Turkish (tr)\nEscolha (1-5): ",
            "ProcessCompletePrompt": "\nProcesso concluído. Pressione Enter para voltar ao menu...",
            "Uninstalling": "Excluindo todos os arquivos instalados...",
            "Uninstalled": "Todos os arquivos do Luatools, Millennium e Steamtools foram totalmente excluídos!"
        },
        "es": {
            "Title": "Instalador del plugin de Luatools | .gg/luatools",
            "SteamRegNotFound": "La clave de registro de Steam no se ha encontrado. Está Steam instalado?",
            "SteamKilling": "Deteniendo Steam",
            "SteamKilled": "Steam se ha detenido",
            "SteamtoolsFound": "Steamtools ya está instalado",
            "SteamtoolsNotFound": "Steamtools no se ha encontrado",
            "SteamtoolsInstalling": "Instalando Steamtools",
            "SteamtoolsInstalled": "Steamtools se ha instalado",
            "SteamtoolsRetrying": "La instalación de Steamtools ha fallado, reintentando...",
            "SteamtoolsFailed": "La instalación de Steamtools ha fallado despues de 5 intentos",
            "MillenniumNotFound": "Millenium no encontrado",
            "MillenniumCountdown": "Millenium sera instalado en {0} segundo(s) ... Presiona cualquier tecla para cancelar",
            "MillenniumCancelled": "Instalación cancelada por el usuario",
            "MillenniumInstalling": "Instalando Millenium",
            "MillenniumInstalled": "Millenium instalado",
            "MillenniumAlready": "Millenium ya estaba instalado",
            "MillenniumFirstBoot": "La carga de steam puede ser más lenta la primera vez para cargar las dependencias -- espera pacientemente",
            "PluginUpdating": "El plugin ya esta instalado, actualizando",
            "PluginDownloading": "Descargando {0}",
            "PluginDownloadFailed": "Error al descargar {0}",
            "PluginExtracting": "Extrayendo {0}",
            "PluginExtractFailed": "Extracción fallida, intentando descomprimir archivos",
            "PluginInstalled": "{0} instalado",
            "PluginEnabled": "Plugin establecido",
            "RemovingBeta": "Limpiando indicador beta",
            "RemovingCfg": "Limpiando steam.cfg",
            "RemovingForceX86": "Limpiando los registros de ForceX86 (32 bits)",
            "StartingSteam": "Iniciando Steam",
            "UpdateCheckDisabled": "Las auto-actualizaciones de Millenium están deshabilitadas para prevenir cuelgues al inicio",
            "UpdateCheckManual": "Comprueba las actualizaciones de Millenium manualmente si necesitas la última versión",
            "ErrorTitle": "Error con el instalador Luatools - ERROR",
            "ErrorHeader": "UN ERROR HA OCURRIDO",
            "ErrorBody": "El instalador del plugin Luatools encontró un problema y no pudo completarse. Esto suele ocurrir cuando tu proveedor de internet (ISP) bloquea los servidores de descarga que utilizamos.",
            "ErrorFaq": "Visita el servidor (.gg/luatools) para mas información o fixes.",
            "ErrorExit": "Presiona cualquier tecla para salir.",
            "MenuHeader": "Menú de Instalación de Luatools",
            "MenuOptionInstall": "1. Instalar",
            "MenuOptionUninstall": "2. Desinstalar / Eliminar",
            "MenuOptionLang": "3. Cambiar idioma",
            "MenuOptionExit": "4. Salir",
            "MenuPrompt": "Por favor, elija una opción (1, 2, 3 o 4): ",
            "LangPrompt": "Seleccionar idioma:\n1. English (en)\n2. Portuguese (pt-BR)\n3. Spanish (es)\n4. French (fr)\n5. Turkish (tr)\nSelección (1-5): ",
            "ProcessCompletePrompt": "\nProceso completado. Presione Enter para volver al menú...",
            "Uninstalling": "Eliminando todos los archivos instalados...",
            "Uninstalled": "¡Todos los archivos de Luatools, Millennium y Steamtools han sido eliminados por completo!"
        },
        "fr": {
            "Title": "Installateur du plugin Luatools | .gg/luatools",
            "SteamRegNotFound": "Clé de registre steam introuvable. Est ce que Steam est installé?",
            "SteamKilling": "Arrêt de Steam",
            "SteamKilled": "Steam arreté",
            "SteamtoolsFound": "Steamtools déjà installé",
            "SteamtoolsNotFound": "Steamtools introuvable",
            "SteamtoolsInstalling": "Installation de Steamtools",
            "SteamtoolsInstalled": "Steamtools installé",
            "SteamtoolsRetrying": "L'instalation de Steamtools a echoué, nouvelle tentative...",
            "SteamtoolsFailed": "L'installation de Steamtools a echoué apres 5 tentatives",
            "MillenniumNotFound": "Millennium introuvable",
            "MillenniumCountdown": "Millennium sera installé dans {0} seconde(s)... Appuyez sur une touche pour annuler",
            "MillenniumCancelled": "Installation annuléee par l'utilisateur",
            "MillenniumInstalling": "Installation de Millennium",
            "MillenniumInstalled": "Millennium installé",
            "MillenniumAlready": "Millennium déjà installé",
            "MillenniumFirstBoot": "Le prochain lancement de Steam sera plus long -- laisser le temps.",
            "PluginUpdating": "Plugin déjà installé, mise à jour",
            "PluginDownloading": "Installation {0}",
            "PluginDownloadFailed": "Echec de l'installation {0}",
            "PluginExtracting": "Extraction {0}",
            "PluginExtractFailed": "Extraction echouée, tentative avec la fonction native",
            "PluginInstalled": "{0} installé",
            "PluginEnabled": "Plugin activé",
            "RemovingBeta": "Nettoyage de la beta",
            "RemovingCfg": "Nettoyage de steam.cfg",
            "RemovingForceX86": "Nettoyage des registres ForceX86 (32 bits)",
            "StartingSteam": "Lancement de Steam",
            "UpdateCheckDisabled": "Les mises à jour de Millennium ont été désactivée pour éviter les blocages au demarrage.",
            "UpdateCheckManual": "Vérifiez manuellement les mises à jour de Millennium si vous souhaitez la derniere version.",
            "ErrorTitle": "Installateur Luatools - ERREUR",
            "ErrorHeader": "UNE ERREUR EST SURVENUE",
            "ErrorBody": "L'installation du plugin Luatools a rencontré un problème et n'a pas pu se terminer. Ça se produit souvent quand votre fournisseur d'internet (ISP) bloque les serveurs de téléchargement.",
            "ErrorFaq": "Allez voir le serveur (.gg/luatools) pour plus d'informations & corrections.",
            "ErrorExit": "Appuyez sur une touche pour quitter.",
            "MenuHeader": "Menu d'Installation de Luatools",
            "MenuOptionInstall": "1. Installer",
            "MenuOptionUninstall": "2. Désinstaller / Supprimer",
            "MenuOptionLang": "3. Changer de langue",
            "MenuOptionExit": "4. Quitter",
            "MenuPrompt": "Veuillez choisir une option (1, 2, 3 ou 4): ",
            "LangPrompt": "Choisir la langue:\n1. English (en)\n2. Portuguese (pt-BR)\n3. Spanish (es)\n4. French (fr)\n5. Turkish (tr)\nChoix (1-5): ",
            "ProcessCompletePrompt": "\nProcessus terminé. Appuyez sur Entrée pour revenir au menu...",
            "Uninstalling": "Suppression de tous les fichiers installés...",
            "Uninstalled": "Tous les fichiers Luatools, Millennium et Steamtools ont été complètement supprimés !"
        },
        "tr": {
            "Title": "Luatools eklenti kurucu | .gg/luatools",
            "SteamRegNotFound": "Steam kayıt defteri anahtarı bulunamadı. Steam kurulu mu?",
            "SteamKilling": "Steam durduruluyor",
            "SteamKilled": "Steam durduruldu",
            "SteamtoolsFound": "Steamtools zaten kurulu",
            "SteamtoolsNotFound": "Steamtools bulunamadı",
            "SteamtoolsInstalling": "Steamtools kuruluyor",
            "SteamtoolsInstalled": "Steamtools kuruldu",
            "SteamtoolsRetrying": "Steamtools kurulumu başarısız, tekrar deneniyor...",
            "SteamtoolsFailed": "5 denemeden sonra Steamtools kurulumu başarısız oldu",
            "MillenniumNotFound": "Millennium bulunamadı",
            "MillenniumCountdown": "Millennium {0} saniye içinde kurulacak... İptal etmek için bir tuşa basın",
            "MillenniumCancelled": "Kurulum kullanıcı tarafından iptal edildi",
            "MillenniumInstalling": "Millennium kuruluyor",
            "MillenniumInstalled": "Millennium kuruldu",
            "MillenniumAlready": "Millennium zaten kurulu",
            "MillenniumFirstBoot": "İlk açılışta Steam yavaş başlayabilir -- lütfen bekleyin.",
            "PluginUpdating": "Eklenti zaten kurulu, güncelleniyor",
            "PluginDownloading": "{0} indiriliyor",
            "PluginDownloadFailed": "{0} indirilemedi",
            "PluginExtracting": "{0} ayıklanıyor",
            "PluginExtractFailed": "Ayıklama başarısız oldu, yerleşik Expand-Archive deneniyor",
            "PluginInstalled": "{0} kuruldu",
            "PluginEnabled": "Eklenti etkinleştirildi",
            "RemovingBeta": "Beta bayrağı temizleniyor",
            "RemovingCfg": "steam.cfg temizleniyor",
            "RemovingForceX86": "ForceX86 kayıt defteri bayrakları temizleniyor (32 bit)",
            "StartingSteam": "Steam başlatılıyor",
            "UpdateCheckDisabled": "Başlangıçta donmaları önlemek için Millennium otomatik güncellemeleri devre dışı bırakıldı.",
            "UpdateCheckManual": "En son sürümü istiyorsanız Millennium güncellemelerini manuel olarak kontrol edin.",
            "ErrorTitle": "Luatools kurucu - HATA",
            "ErrorHeader": "BİR HATA OLUŞTU",
            "ErrorBody": "Luatools eklenti kurucusu bir sorunla karşılaştı ve tamamlanamadı. Bu genellikle ISS'nizin kullandığımız indirme sunucularını engellemesinden kaynaklanır.",
            "ErrorFaq": "Daha fazla bilgi ve çözüm için sunucuyu (.gg/luatools) ziyaret edin.",
            "ErrorExit": "Çıkmak için bir tuşa basın.",
            "MenuHeader": "Luatools Kurulum Menüsü",
            "MenuOptionInstall": "1. Kur",
            "MenuOptionUninstall": "2. Sil (Kaldır)",
            "MenuOptionLang": "3. Dili Değiştir",
            "MenuOptionExit": "4. Çıkış",
            "MenuPrompt": "Lütfen seçiminizi yapın (1, 2, 3 veya 4): ",
            "LangPrompt": "Dil seçin:\n1. English (en)\n2. Portuguese (pt-BR)\n3. Spanish (es)\n4. French (fr)\n5. Turkish (tr)\nSeçim (1-5): ",
            "ProcessCompletePrompt": "\nİşlem tamamlandı. Menüye dönmek için Enter'a basın...",
            "Uninstalling": "Tüm kurulu dosyalar siliniyor...",
            "Uninstalled": "Tüm Luatools, Millennium ve Steamtools dosyaları tamamen silindi!"
        }
    }
    
    keys_to_try = [culture, culture.split('-')[0], "en"]
    for k in keys_to_try:
        if k in tables:
            return tables[k]
    return tables["en"]

def show_error_page(e):
    global L
    if 'L' not in globals() or not L:
        L = get_default_strings("en")
        
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(L.get("ErrorTitle", "Luatools installer - ERROR"))
    except Exception:
        pass
        
    os.system("cls")
    
    try:
        width = os.get_terminal_size().columns
    except Exception:
        width = 80
        
    red = COLORS["Red"]
    yellow = COLORS["Yellow"]
    cyan = COLORS["Cyan"]
    white = COLORS["White"]
    reset = COLORS["Reset"]
    gray = COLORS["DarkGray"]
    
    print(red + "=" * width + reset)
    print()
    
    header = L.get("ErrorHeader", "AN ERROR OCCURRED")
    pad = max(0, int((width - len(header)) / 2))
    print(" " * pad + red + header + reset)
    print()
    
    body = L.get("ErrorBody", "The installer encountered a problem.")
    print(white + body + reset)
    print()
    
    print(red + ">>> " + reset + gray + str(e) + reset)
    print()
    
    faq = L.get("ErrorFaq", "Visit (.gg/luatools)")
    print(cyan + faq + reset)
    print()
    
    print(red + "=" * width + reset)
    print()
    
    exit_msg = L.get("ErrorExit", "Press Enter to exit.")
    input(yellow + exit_msg + reset)
    sys.exit(1)

def get_steam_path():
    registries = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam")
    ]
    for hkey, subkey in registries:
        try:
            with winreg.OpenKey(hkey, subkey) as key:
                path, _ = winreg.QueryValueEx(key, "InstallPath")
                if path:
                    potential_exe = os.path.join(path, "steam.exe")
                    if os.path.exists(path) and os.path.exists(potential_exe):
                        return path
        except Exception:
            continue
    return None

def kill_steam():
    write_log("INFO", L["SteamKilling"])
    for _ in range(10):
        res = subprocess.run(["tasklist", "/FI", "IMAGENAME eq steam.exe"], capture_output=True, text=True)
        if "steam.exe" not in res.stdout.lower():
            break
        subprocess.run(["taskkill", "/F", "/IM", "steam.exe"], capture_output=True)
        time.sleep(0.5)

def run_ps_script(script_content, args=None, capture=False):
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".ps1")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8-sig') as f:
            f.write(script_content)
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path]
        if args:
            cmd.extend(args)
        if capture:
            return subprocess.run(cmd, capture_output=True, text=True)
        else:
            return subprocess.run(cmd)
    finally:
        try:
            os.remove(path)
        except Exception:
            pass

def test_steamtools(steam_path):
    for f in ["dwmapi.dll", "xinput1_4.dll"]:
        if os.path.exists(os.path.join(steam_path, f)):
            return True
    return False

def install_steamtools(steam_path):
    write_log("WARN", L["SteamtoolsInstalling"])
    url = "https://luatools.vercel.app/st.ps1"
    raw = ""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode('utf-8')
    except Exception:
        try:
            cmd = "curl.exe -s --doh-url https://1.1.1.1/dns-query https://luatools.vercel.app/st.ps1"
            res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
            raw = res.stdout
        except Exception:
            pass
            
    if not raw:
        raise Exception(L["SteamtoolsFailed"])

    lines = raw.split("\n")
    filtered = []
    for line in lines:
        if (not re.search(r"Start-Process.*steam", line, re.IGNORECASE) and
            not re.search(r"steam\.exe", line, re.IGNORECASE) and
            not re.search(r"Start-Sleep|Write-Host", line, re.IGNORECASE) and
            not re.search(r"cls|exit", line, re.IGNORECASE) and
            not (re.search(r"Stop-Process", line, re.IGNORECASE) and not re.search(r"Get-Process", line, re.IGNORECASE))):
            filtered.append(line)
            
    script_block = "\n".join(filtered)
    
    for attempt in range(1, 6):
        write_log("LOG", L["SteamtoolsInstalling"])
        run_ps_script(script_block, capture=True)
        if test_steamtools(steam_path):
            write_log("OK", L["SteamtoolsInstalled"])
            return
        write_log("ERR", L["SteamtoolsRetrying"])
        
    raise Exception(L["SteamtoolsFailed"])

def test_millennium(steam_path):
    has_bootstrap = os.path.exists(os.path.join(steam_path, "wsock32.dll")) or os.path.exists(os.path.join(steam_path, "millennium.dll"))
    has_lib = os.path.exists(os.path.join(steam_path, "python311.dll")) or os.path.exists(os.path.join(steam_path, "millennium", "lib", "millennium.dll"))
    return has_bootstrap and has_lib

def install_millennium(steam_path):
    write_log("INFO", L["MillenniumInstalling"])
    url = "https://clemdotla.github.io/millennium-installer-ps1/millennium.ps1"
    ms_code = ""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            ms_code = response.read().decode('utf-8')
    except Exception:
        pass
        
    if not ms_code:
        raise Exception(L["MillenniumNotFound"])
        
    run_ps_script(ms_code, args=["-NoLog", "-DontStart", "-SteamPath", steam_path], capture=False)
    
    if test_millennium(steam_path):
        write_log("OK", L["MillenniumInstalled"])
    else:
        raise Exception("Millennium installation failed validation checks")

def install_plugin(steam_path, name, link):
    plugins_dir = os.path.join(steam_path, "millennium", "plugins")
    os.makedirs(plugins_dir, exist_ok=True)
    
    target_dir = os.path.join(plugins_dir, name)
    
    for d in os.listdir(plugins_dir):
        d_path = os.path.join(plugins_dir, d)
        if os.path.isdir(d_path):
            plugin_json = os.path.join(d_path, "plugin.json")
            if os.path.exists(plugin_json):
                try:
                    with open(plugin_json, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    if meta.get("name") == name:
                        write_log("INFO", L["PluginUpdating"])
                        target_dir = d_path
                        break
                except Exception:
                    pass
                    
    temp_dir = os.environ.get("TEMP", os.environ.get("TMP", os.environ.get("USERPROFILE")))
    zip_path = os.path.join(temp_dir, f"{name}.zip")
    
    write_log("LOG", L["PluginDownloading"].format(name))
    
    try:
        req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Luatools Installer)'})
        with urllib.request.urlopen(req, timeout=60) as response, open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        raise Exception(L["PluginDownloadFailed"].format(name))
        
    if not os.path.exists(zip_path):
        raise Exception(L["PluginDownloadFailed"].format(name))
        
    write_log("LOG", L["PluginExtracting"].format(name))
    
    import zipfile
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for info in zip_ref.infolist():
                if info.filename.endswith('/') or info.filename.endswith('\\'):
                    continue
                dest = os.path.join(target_dir, info.filename)
                dest_dir = os.path.dirname(dest)
                
                rel_path = os.path.relpath(dest_dir, target_dir)
                if rel_path != ".":
                    parts = rel_path.split(os.sep)
                    curr = target_dir
                    for part in parts:
                        curr = os.path.join(curr, part)
                        if os.path.exists(curr) and not os.path.isdir(curr):
                            os.remove(curr)
                            
                os.makedirs(dest_dir, exist_ok=True)
                with zip_ref.open(info) as source, open(dest, "wb") as target:
                    shutil.copyfileobj(source, target)
    except Exception:
        write_log("WARN", L["PluginExtractFailed"])
        subprocess.run(["powershell", "-Command", f"Expand-Archive -Path '{zip_path}' -DestinationPath '{target_dir}' -Force"], capture_output=True)
        
    if os.path.exists(zip_path):
        try:
            os.remove(zip_path)
        except Exception:
            pass
            
    display_name = name[0].upper() + name[1:].lower()
    write_log("OK", L["PluginInstalled"].format(display_name))

def enable_plugin(steam_path, name):
    config_dir = os.path.join(steam_path, "millennium", "config")
    config_path = os.path.join(config_dir, "config.json")
    
    if not os.path.exists(config_path):
        os.makedirs(config_dir, exist_ok=True)
        config = {
            "plugins": {
                "enabledPlugins": [name]
            }
        }
    else:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            config = {}
            
        if "plugins" not in config:
            config["plugins"] = {}
        if "enabledPlugins" not in config["plugins"] or not isinstance(config["plugins"]["enabledPlugins"], list):
            config["plugins"]["enabledPlugins"] = []
            
        if name not in config["plugins"]["enabledPlugins"]:
            config["plugins"]["enabledPlugins"].append(name)
            
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        
    write_log("OK", L["PluginEnabled"])

def remove_beta_flag(steam_path):
    beta = os.path.join(steam_path, "package", "beta")
    if os.path.exists(beta):
        write_log("AUX", L["RemovingBeta"])
        try:
            if os.path.isdir(beta):
                shutil.rmtree(beta)
            else:
                os.remove(beta)
        except Exception:
            pass

def remove_steam_cfg(steam_path):
    cfg = os.path.join(steam_path, "steam.cfg")
    if os.path.exists(cfg):
        write_log("AUX", L["RemovingCfg"])
        try:
            os.remove(cfg)
        except Exception:
            pass

def remove_force_x86_flags():
    write_log("AUX", L["RemovingForceX86"])
    registries = [
        (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
    ]
    for hkey, subkey in registries:
        try:
            with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, "SteamCmdForceX86")
        except Exception:
            continue

def install_all(steam_path):
    global L, millDir
    
    millDir = os.path.join(steam_path, "millennium")
    if not os.path.exists(millDir):
        os.makedirs(millDir, exist_ok=True)
        
    kill_steam()
    
    if test_steamtools(steam_path):
        write_log("INFO", L["SteamtoolsFound"])
    else:
        write_log("ERR", L["SteamtoolsNotFound"])
        install_steamtools(steam_path)
        
    millennium_was_installed = test_millennium(steam_path)
    install_millennium(steam_path)
    
    install_plugin(steam_path, Name, Link)
    
    remove_beta_flag(steam_path)
    remove_steam_cfg(steam_path)
    remove_force_x86_flags()
    
    enable_plugin(steam_path, Name)
    
    print()
    if not millennium_was_installed:
        write_log("WARN", L["MillenniumFirstBoot"])
        
    write_log("INFO", L["StartingSteam"])
    steam_exe = os.path.join(steam_path, "steam.exe")
    subprocess.Popen([steam_exe, "-clearbeta"])

def uninstall_all(steam_path):
    global L
    
    kill_steam()
    
    write_log("LOG", L["Uninstalling"])
    
    files_to_delete = [
        "millennium.dll",
        "python311.dll",
        "python3.dll",
        "dwmapi.dll",
        "xinput1_4.dll",
        "user32.dll",
        "version.dll",
        "wsock32.dll",
        "dwmapi.dll.old",
        "xinput1_4.dll.old",
        "wsock32.dll.old"
    ]
    
    for f in files_to_delete:
        path = os.path.join(steam_path, f)
        if os.path.exists(path):
            try:
                os.remove(path)
                write_log("AUX", f"Deleted: {f}")
            except Exception:
                pass
                
    mill_dir = os.path.join(steam_path, "millennium")
    if os.path.exists(mill_dir):
        try:
            shutil.rmtree(mill_dir)
            write_log("AUX", "Deleted directory: millennium")
        except Exception:
            pass
            
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steamtools")
        write_log("AUX", "Deleted registry key: Steamtools")
    except Exception:
        pass
        
    write_log("OK", L["Uninstalled"])
    
    write_log("INFO", L["StartingSteam"])
    steam_exe = os.path.join(steam_path, "steam.exe")
    subprocess.Popen([steam_exe])

def main():
    global L, Name, Link
    
    DownloadLink = os.environ.get("LT_DOWNLOAD_LINK", None)
    PluginName = os.environ.get("LT_PLUGIN_NAME", None)
    try:
        Branch = int(os.environ.get("LT_BRANCH", "1"))
    except ValueError:
        Branch = 1
    Culture = os.environ.get("LT_CULTURE", None)
    
    if not Culture:
        try:
            loc = locale.getdefaultlocale()[0]
            if loc:
                Culture = loc
        except Exception:
            pass
            
    if not Culture:
        Culture = "en"
        
    L = get_default_strings(Culture)
    
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(L["Title"])
    except Exception:
        pass
        
    Name = "luatools"
    Link = "https://github.com/piqseu/ltsteamplugin/releases/latest/download/ltsteamplugin.zip"
    
    if Branch == 2:
        Name = "steamtools-collection"
        Link = "https://github.com/clemdotla/steamtools-collection/releases/download/Latest/steamtools-collection.zip"
        
    if DownloadLink:
        Link = DownloadLink
    if PluginName:
        Name = PluginName
        
    steam_path = get_steam_path()
    if not steam_path:
        raise Exception(L["SteamRegNotFound"])
        
    while True:
        os.system("cls")
        cyan = COLORS["Cyan"]
        white = COLORS["White"]
        green = COLORS["Green"]
        red = COLORS["Red"]
        reset = COLORS["Reset"]
        
        ascii_art = """
 ██████╗██╗  ██╗███████╗ █████╗ ████████╗ ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     
██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     
██║     ███████║█████╗  ███████║   ██║   ██║  ███╗██║     ██║   ██║██████╔╝███████║██║     
██║     ██╔══██║██╔══╝  ██╔══██║   ██║   ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     
╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
"""
        print(green + ascii_art + reset)
        print(green + "                                   author dominicsolanke\n" + reset)
        
        print(cyan + "========================================" + reset)
        print(white + f"       {L['MenuHeader']}" + reset)
        print(cyan + "========================================" + reset)
        print(green + f"  {L['MenuOptionInstall']}" + reset)
        print(red + f"  {L['MenuOptionUninstall']}" + reset)
        print(cyan + f"  {L['MenuOptionLang']}" + reset)
        print(red + f"  {L['MenuOptionExit']}" + reset)
        print(cyan + "========================================" + reset)
        print()
        
        choice = input(L["MenuPrompt"]).strip()
        
        if choice == "1":
            install_all(steam_path)
            input(L["ProcessCompletePrompt"])
        elif choice == "2":
            uninstall_all(steam_path)
            input(L["ProcessCompletePrompt"])
        elif choice == "3":
            os.system("cls")
            print(cyan + "========================================" + reset)
            print(white + L["LangPrompt"] + reset, end="")
            lang_choice = input().strip()
            if lang_choice == "1":
                Culture = "en"
            elif lang_choice == "2":
                Culture = "pt-BR"
            elif lang_choice == "3":
                Culture = "es"
            elif lang_choice == "4":
                Culture = "fr"
            elif lang_choice == "5":
                Culture = "tr"
            L = get_default_strings(Culture)
            try:
                ctypes.windll.kernel32.SetConsoleTitleW(L["Title"])
            except Exception:
                pass
        elif choice == "4":
            sys.exit(0)
        else:
            write_log("ERR", L["MenuInvalid"])
            time.sleep(2)
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_error_page(e)
