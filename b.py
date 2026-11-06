import frida
import sys
import pymem
import time
import os
import urllib.request
import json
import subprocess
import base64

# ============================================================
# CONFIGURAÇÕES DO GITHUB (Auto-Update)
# ============================================================
GITHUB_USER = "juicrwrldfabr123-gif"
GITHUB_REPO = "crw-bypass"
VERSAO_ATUAL = "1.0.0"  # Mude para "1.0.1" quando for lançar um update

# ============================================================
# INTERFACE (Cores do Terminal)
# ============================================================
class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"{C.CYAN}{C.BOLD}")
    print("  ============================================================")
    print(f"   ██████╗ ██████╗ ██╗    ██╗     ██████╗ ██╗   ██╗██████╗  █████╗ ███████╗███████╗")
    print(f"  ██╔════╝ ██╔══██╗██║    ██║     ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝")
    print(f"  ██║      ██████╔╝██║ █╗ ██║     ██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗███████╗")
    print(f"  ██║      ██╔══██╗██║███╗██║     ██╔══██╗  ╚██╔╝  ██╔═══╝ ██╔══██║╚════██║╚════██║")
    print(f"  ╚██████╗ ██║  ██║╚███╔███╔╝     ██████╔╝   ██║   ██║     ██║  ██║███████║███████║")
    print(f"   ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝      ╚═════╝    ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝")
    print(f"{C.RESET}")
    print(f"{C.GRAY}              [ Runtime Modifier ]    [ v{VERSAO_ATUAL} ]{C.RESET}")
    print(f"  ============================================================\n")

def spinner(texto, duracao=2):
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    end_time = time.time() + duracao
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{C.GRAY}[*] {texto}... {frames[i % len(frames)]}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{C.GREEN}[+] {texto}... OK      {C.RESET}\n")

# ============================================================
# SISTEMA DE AUTO-UPDATE
# ============================================================
def verificar_update():
    banner()
    print(f"{C.GRAY}[*] Verificando atualizações no repositorio GitHub...{C.RESET}")
    
    try:
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
        req = urllib.request.Request(url, headers={'User-Agent': 'CRW-Bypass'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            ultima_versao = data.get("tag_name", "").replace("v", "")
            
            if ultima_versao and ultima_versao != VERSAO_ATUAL:
                print(f"\n{C.YELLOW}{C.BOLD}[!] NOVA ATUALIZAÇÃO DISPONÍVEL!{C.RESET}")
                print(f"    Versão atual: {C.RED}{VERSAO_ATUAL}{C.RESET}")
                print(f"    Nova versão:  {C.GREEN}{ultima_versao}{C.RESET}")
                
                opcao = input(f"\n{C.CYAN}[?] Deseja baixar e atualizar agora? (S/N): {C.RESET}").strip().lower()
                
                if opcao == 's':
                    print(f"\n{C.GRAY}[*] Baixando atualização...{C.RESET}")
                    assets = data.get("assets", [])
                    download_url = None
                    
                    # Procura o arquivo .py anexado na Release
                    for asset in assets:
                        if asset["name"].endswith(".py"):
                            download_url = asset["browser_download_url"]
                            break
                    
                    if download_url:
                        urllib.request.urlretrieve(download_url, "crw_bypass_new.py")
                        print(f"{C.GREEN}[+] Download concluído!{C.RESET}")
                        print(f"{C.YELLOW}[*] Reiniciando o script com a nova versão...{C.RESET}")
                        time.sleep(1)
                        subprocess.Popen([sys.executable, "crw_bypass_new.py"])
                        sys.exit(0)
                    else:
                        print(f"{C.RED}[-] Arquivo .py não encontrado na release do GitHub.{C.RESET}")
                        time.sleep(2)
            else:
                print(f"{C.GREEN}[+] Você está na versão mais recente ({VERSAO_ATUAL}).{C.RESET}")
                time.sleep(1)
                
    except Exception as e:
        print(f"{C.GRAY}[~] Nao foi possivel verificar atualizacoes (Offline ou sem Release).{C.RESET}")
        time.sleep(1)

# ============================================================
# SCRIPT PRINCIPAL
# ============================================================
def main():
    verificar_update() # <--- CHECA UPDATE ANTES DE TUDO
    
    banner()
    RESPOSTA = "VALID|9999-12-31 23:59:59|free"
    PROCESSO = "HD-Player.exe"

    # 1. PROCURA O PROCESSO
    print(f"{C.GRAY}[*] Procurando processo: {PROCESSO}...{C.RESET}")
    while True:
        try:
            pm = pymem.Pymem(PROCESSO)
            break
        except:
            time.sleep(1)
            sys.stdout.write(f"\r{C.YELLOW}[~] Aguardando emulador iniciar...{C.RESET}")
            sys.stdout.flush()

    PID = pm.process_id
    print(f"\n{C.GREEN}[+] Processo encontrado (PID: {PID}){C.RESET}")
    spinner("Anexando contexto ao processo", 1.5)

    # 2. SCRIPT FRIDA
    script_code = f"""
    var RESPOSTA = {repr(RESPOSTA)};
    
    function log(m) {{ console.log(m); }}

    try {{
        var winhttp = Process.getModuleByName("winhttp.dll");
        var wRead = winhttp.getExportByName("WinHttpReadData");

        Interceptor.attach(wRead, {{
            onEnter: function(a) {{
                this.buf = a[1];
                this.readPtr = a[3];
            }},
            onLeave: function(r) {{
                try {{
                    var lidos = this.readPtr.readU32();
                    if (lidos !== 11) return;

                    for (var i = 0; i < RESPOSTA.length; i++) {{
                        this.buf.add(i).writeU8(RESPOSTA.charCodeAt(i));
                    }}
                    this.readPtr.writeU32(RESPOSTA.length);
                    log("Hook interceptado: INVALID_KEY -> LIFETIME");
                }} catch (e) {{ log("Falha no hook: " + e); }}
            }}
        }});
        log("Modulo WinHttpReadData inicializado.");
    }} catch (e) {{
        log("Falha: winhttp.dll nao encontrada no processo.");
    }}
    """

    try:
        session = frida.attach(PID)
        script = session.create_script(script_code)
        script.on("message", lambda m, d: print(f"{C.GRAY}    > {m.get('payload', m)}{C.RESET}"))
        script.load()
    except Exception as e:
        print(f"{C.RED}[-] Erro ao injetar: {e}{C.RESET}")
        sys.exit(1)

    # 3. PAINEL DE STATUS
    clear()
    banner()
    
    print(f"  {C.CYAN}───────────────────────────────────────────────────────────────{C.RESET}")
    print(f"  {C.GREEN}{C.BOLD} [+] SISTEMA INJETADO E OPERANTE{C.RESET}")
    print(f"  {C.CYAN}───────────────────────────────────────────────────────────────{C.RESET}")
    print(f"   {C.GRAY}• Target:{C.RESET}     HD-Player.exe")
    print(f"   {C.GRAY}• Protocolo:{C.RESET}  WinHTTP Intercept")
    print(f"   {C.GRAY}• Expiração:{C.RESET}  9999-12-31 (Lifetime)")
    print(f"   {C.GRAY}• Licença:{C.RESET}    Bypass Ativado")
    print(f"  {C.CYAN}───────────────────────────────────────────────────────────────{C.RESET}")
    print(f"\n  {C.YELLOW}>> Insira qualquer key no launcher para autenticar.{C.RESET}")
    print(f"  {C.GRAY}>> Pressione Ctrl+C para encerrar o processo.{C.RESET}\n")

    # 4. LOOP INFINITO
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{C.RED}[!] Desconectando e finalizando...{C.RESET}")
        session.detach()
        sys.exit(0)

if __name__ == "__main__":
    if os.name == 'nt':
        os.system('color')
    main()
