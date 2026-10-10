import json, time, threading, sys, traceback, webbrowser, socket
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
ROOT=Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
CFG=Path.home()/".corrida_tiktok_vgzeratv.json"
config={"usuario":"@vgzeratv","presente_lula":"Rose","presente_bolsonaro":"Finger Heart","pontos_por_presente":5,"meta":100}
if CFG.exists():
    try: config.update(json.loads(CFG.read_text(encoding="utf-8")))
    except Exception: pass
state={"lula":0,"bolsonaro":0,"vencedor":None,"status":"Iniciando","ultimo":"Aguardando presentes","rodada":1}
lock=threading.RLock()
app=Flask(__name__)
def snapshot():
    with lock: return {"estado":dict(state),"config":dict(config)}
def progress(team,qty=1,viewer="Teste",gift="Presente"):
    with lock:
        if state["vencedor"]: return
        qty=max(1,min(int(qty),10000))
        state[team]=min(int(config["meta"]),state[team]+qty*int(config["pontos_por_presente"]))
        state["ultimo"]=f"{viewer}: {qty}x {gift} => {team.upper()}"
        if state[team]>=int(config["meta"]): state["vencedor"]=team
@app.get("/")
def game(): return send_from_directory(ROOT,"jogo.html")
@app.get("/controle")
def controls(): return send_from_directory(ROOT,"controle.html")
@app.get("/api/state")
def current(): return jsonify(snapshot())
@app.post("/api/reset")
def reset():
    with lock:
        state.update(lula=0,bolsonaro=0,vencedor=None,ultimo="Nova rodada",rodada=state["rodada"]+1)
    return jsonify(snapshot())
@app.post("/api/simular")
def simulate():
    team=(request.get_json(silent=True) or {}).get("equipe")
    if team not in ("lula","bolsonaro"): return jsonify(error="Equipe invalida"),400
    progress(team,1,"SIMULACAO",config["presente_"+team])
    return jsonify(snapshot())
@app.post("/api/config")
def change():
    data=request.get_json(silent=True) or {}
    with lock:
        for k in ("usuario","presente_lula","presente_bolsonaro"):
            if k in data: config[k]=str(data[k]).strip()[:80]
        for k in ("meta","pontos_por_presente"):
            if k in data:
                try: config[k]=max(1,min(100000,int(data[k])))
                except (TypeError,ValueError): pass
        CFG.write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding="utf-8")
        state["ultimo"]="Configuracao salva; reinicie apos mudar o @"
    return jsonify(snapshot())
def live_worker():
    try:
        from TikTokLive import TikTokLiveClient
        from TikTokLive.events import GiftEvent,ConnectEvent,DisconnectEvent
    except Exception as e:
        with lock: state["status"]="Biblioteca indisponivel: "+str(e)[:100]
        return
    while True:
        user=config["usuario"].strip().lstrip("@")
        if not user:
            with lock: state["status"]="Configure seu @ no painel"
            time.sleep(10);continue
        client=TikTokLiveClient(unique_id="@"+user)
        @client.on(ConnectEvent)
        async def on_connect(event):
            with lock: state["status"]="Conectado a @"+user
        @client.on(DisconnectEvent)
        async def on_disconnect(event):
            with lock: state["status"]="Desconectado; tentando reconectar"
        @client.on(GiftEvent)
        async def on_gift(event):
            try:
                gift=event.gift
                if gift is None:return
                if getattr(gift,"streakable",False) and getattr(event,"streaking",False):return
                name=str(getattr(gift,"name","") or "")
                qty=int(getattr(event,"repeat_count",1) or 1)
                viewer=str(getattr(event.user,"nickname","Espectador") or "Espectador")[:50]
                with lock:
                    team=next((t for t in ("lula","bolsonaro") if config["presente_"+t].casefold()==name.casefold()),None)
                if team:progress(team,qty,viewer,name)
            except Exception as e:print("Presente:",e,flush=True)
        try:
            with lock:state["status"]="Conectando a @"+user
            client.run()
        except Exception as e:
            with lock:state["status"]="Offline/erro: "+str(e)[:120]
        time.sleep(12)
def main():
    print("="*55, flush=True)
    print("CORRIDA TIKTOK VGZERATV - VERSAO DE DIAGNOSTICO", flush=True)
    print("Arquivos do jogo: " + str(ROOT), flush=True)
    for fname in ("jogo.html","controle.html"):
        if not (ROOT/fname).is_file():
            raise FileNotFoundError("Arquivo obrigatorio ausente: " + str(ROOT/fname))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as check:
        if check.connect_ex(("127.0.0.1",8765)) == 0:
            print("ATENCAO: porta 8765 ja em uso. Feche a instancia anterior.", flush=True)
            webbrowser.open("http://127.0.0.1:8765/controle")
            return
    threading.Thread(target=live_worker,daemon=True).start()
    def open_panel():
        for _ in range(30):
            time.sleep(0.5)
            try:
                with socket.create_connection(("127.0.0.1",8765),timeout=1):
                    webbrowser.open("http://127.0.0.1:8765/controle")
                    return
            except OSError: pass
        print("ERRO: servidor nao respondeu em 15 segundos",flush=True)
    threading.Thread(target=open_panel,daemon=True).start()
    print("Painel: http://127.0.0.1:8765/controle", flush=True)
    print("Deixe esta janela aberta durante a live.", flush=True)
    app.run(host="127.0.0.1",port=8765,debug=False,threaded=True,use_reloader=False)
if __name__=="__main__":
    try: main()
    except Exception:
        msg=traceback.format_exc()
        print("ERRO AO INICIAR:\\n"+msg,flush=True)
        log=Path.home()/"Desktop"/"erro_corrida_tiktok.txt"
        try: log.write_text(msg,encoding="utf-8")
        except Exception: log=Path.home()/"erro_corrida_tiktok.txt"; log.write_text(msg,encoding="utf-8")
        print("Relatorio salvo em: "+str(log),flush=True)
        input("Pressione ENTER para encerrar...")

