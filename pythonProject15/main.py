import pygame
import random
import time

# Configurações Iniciais
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Galaxy's Guardian: Full Version")

# Cores
PRETO, BRANCO = (0, 0, 0), (255, 255, 255)
VERMELHO, AZUL, AMARELO, VERDE, CIANO, ROXO = (255, 50, 50), (0, 150, 255), (255, 255, 0), (0, 255, 100), (
0, 255, 255), (150, 0, 255)

# Fontes
fonte_p = pygame.font.SysFont("arial", 22, bold=True)
fonte_m = pygame.font.SysFont("arial", 35, bold=True)
fonte_g = pygame.font.SysFont("arial", 60, bold=True)

DICAS = [
    "DICA: No nível 10, o Boss destruirá sua nave em segundos!",
    "DICA: Guarde lasers para as naves azuis rápidas.",
    "DICA: Quadrados verdes recuperam sua vida.",
    "DICA: O Boss tem um escudo, acerte o centro branco!"
]


def criar_asteroide(nivel=1):
    vel_ajustada = 4 + (nivel * 0.8)
    return {"x": random.randint(0, LARGURA - 30), "y": random.randint(-600, -50),
            "vel": random.uniform(vel_ajustada, vel_ajustada + 2)}


def criar_nave_inimiga(nivel=1):
    direcao = random.choice([1, -1])
    x_inicial = -100 if direcao == 1 else LARGURA + 100
    vel_x = (5 + (nivel * 0.6)) * direcao
    return {"x": x_inicial, "y": random.randint(50, ALTURA - 220), "vel_x": vel_x, "direcao": direcao}


def criar_item(emergencia_vida=False):
    tipo = "VIDA" if emergencia_vida else random.choice(["VIDA", "PONTOS", "TIRO"])
    return {"x": random.randint(50, LARGURA - 50), "y": -50, "vel": 4, "tipo": tipo}


def tela_loading():
    dica = random.choice(DICAS)
    progresso = 0
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); exit()
            if progresso >= 100 and evento.type == pygame.KEYDOWN: esperando = False
        tela.fill(PRETO)
        pygame.draw.rect(tela, BRANCO, (LARGURA // 2 - 150, ALTURA // 2, 300, 20), 2)
        pygame.draw.rect(tela, VERDE, (LARGURA // 2 - 148, ALTURA // 2 + 2, min(progresso, 100) * 2.96, 16))
        if progresso < 100:
            txt_l = fonte_m.render("RECALIBRANDO SISTEMAS...", True, BRANCO)
            progresso += 0.7
        else:
            txt_l = fonte_m.render("SISTEMAS ONLINE!", True, VERDE)
            txt_key = fonte_p.render("PRESSIONE QUALQUER TECLA", True, BRANCO)
            tela.blit(txt_key, (LARGURA // 2 - 130, ALTURA // 2 + 80))
        tela.blit(txt_l, (LARGURA // 2 - 180, ALTURA // 2 - 50))
        txt_d = fonte_p.render(dica, True, AMARELO)
        tela.blit(txt_d, (LARGURA // 2 - txt_d.get_width() // 2, ALTURA // 2 + 40))
        pygame.display.flip()
        time.sleep(0.01)


def reset_jogo():
    return {
        "nave_x": LARGURA // 2, "nave_y": ALTURA // 2,
        "vidas": 5, "pontos": 0, "nivel": 1, "tiros": 10,
        "boss": {"x": LARGURA // 2 - 50, "y": -150, "vida": 80, "ativo": False, "vel_x": 5, "derrotado": False},
        "lista_ast": [criar_asteroide(1) for _ in range(4)],
        "lista_nav": [], "lista_itens": [], "lista_lasers": [], "lista_atk_boss": []
    }


dados = reset_jogo()
lista_estrelas = [{"x": random.randint(0, LARGURA), "y": random.randint(0, ALTURA), "vel": random.randint(1, 3)} for _
                  in range(50)]
relogio = pygame.time.Clock()
estado = 'START'

TIMER_ITEM = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_ITEM, 10000)
TIMER_ATAQUE_BOSS = pygame.USEREVENT + 2
TIMER_RECARGA_BOSS = pygame.USEREVENT + 3

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: pygame.quit(); exit()
        if estado == 'PLAYING':
            if evento.type == TIMER_ITEM: dados["lista_itens"].append(criar_item(dados["vidas"] <= 2))
            if evento.type == TIMER_RECARGA_BOSS and dados["boss"]["ativo"]: dados["tiros"] += 1
            if evento.type == TIMER_ATAQUE_BOSS and dados["boss"]["ativo"]:
                for i in range(-2, 3):
                    dados["lista_atk_boss"].append(
                        {"x": dados["boss"]["x"] + 50, "y": dados["boss"]["y"] + 100, "vel_y": 8, "vel_x": i * 2})

        if evento.type == pygame.KEYDOWN:
            if estado == 'START' and evento.key == pygame.K_SPACE:
                tela_loading()
                dados = reset_jogo()
                estado = 'PLAYING'
            elif estado == 'PLAYING' and evento.key == pygame.K_SPACE and dados["tiros"] > 0:
                dados["lista_lasers"].append({"x": dados["nave_x"] - 2, "y": dados["nave_y"] - 20, "vel": 14})
                dados["tiros"] -= 1
            elif estado in ['GAMEOVER', 'WIN'] and evento.key == pygame.K_r:
                estado = 'START'

    if estado == 'PLAYING':
        teclas = pygame.key.get_pressed()
        vel_p = 8
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:  dados["nave_x"] -= vel_p
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: dados["nave_x"] += vel_p
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:    dados["nave_y"] -= vel_p
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:  dados["nave_y"] += vel_p

        dados["nave_x"] = max(18, min(LARGURA - 18, dados["nave_x"]))
        dados["nave_y"] = max(18, min(ALTURA - 18, dados["nave_y"]))
        rect_player = pygame.Rect(dados["nave_x"] - 18, dados["nave_y"] - 18, 36, 36)

        if dados["nivel"] < 10:
            novo_nivel = (dados["pontos"] // 50) + 1
            if novo_nivel > dados["nivel"]:
                dados["nivel"] = novo_nivel
                if dados["nivel"] >= 2 and len(dados["lista_nav"]) < 3:
                    dados["lista_nav"].append(criar_nave_inimiga(dados["nivel"]))

        if dados["nivel"] >= 10 and not dados["boss"]["ativo"] and not dados["boss"]["derrotado"]:
            dados["boss"]["ativo"] = True
            pygame.time.set_timer(TIMER_ATAQUE_BOSS, 1000)
            pygame.time.set_timer(TIMER_RECARGA_BOSS, 4000)
            dados["lista_ast"].clear();
            dados["lista_nav"].clear()

        for ast in dados["lista_ast"]:
            ast["y"] += ast["vel"]
            if ast["y"] > ALTURA: ast["y"], ast["x"] = -50, random.randint(0, LARGURA - 30); dados["pontos"] += 1
            if rect_player.colliderect(pygame.Rect(ast["x"], ast["y"], 30, 30)): dados["vidas"] -= 1; ast["y"] = -200

        for n in dados["lista_nav"]:
            n["x"] += n["vel_x"]
            diff_y = dados["nave_y"] - n["y"]
            if abs(diff_y) > 5:
                n["y"] += (1 + (dados["nivel"] * 0.1)) if diff_y > 0 else -(1.2 + (dados["nivel"] * 0.2))
            if n["x"] > LARGURA + 100 or n["x"] < -100: n.update(criar_nave_inimiga(dados["nivel"]))
            if rect_player.colliderect(pygame.Rect(n["x"], n["y"], 25, 25)): dados["vidas"] -= 1; n.update(
                criar_nave_inimiga(dados["nivel"]))

        if dados["boss"]["ativo"]:
            if dados["boss"]["y"] < 60:
                dados["boss"]["y"] += 2
            else:
                dados["boss"]["x"] += dados["boss"]["vel_x"]
                if dados["boss"]["x"] <= 0 or dados["boss"]["x"] >= LARGURA - 100: dados["boss"]["vel_x"] *= -1
            for atk in dados["lista_atk_boss"][:]:
                atk["y"] += atk["vel_y"];
                atk["x"] += atk["vel_x"]
                if rect_player.colliderect(pygame.Rect(atk["x"], atk["y"], 15, 15)):
                    dados["vidas"] -= 1;
                    dados["lista_atk_boss"].remove(atk)
                elif atk["y"] > ALTURA:
                    dados["lista_atk_boss"].remove(atk)

        for laser in dados["lista_lasers"][:]:
            laser["y"] -= laser["vel"]
            rl = pygame.Rect(laser["x"], laser["y"], 4, 15)
            if dados["boss"]["ativo"] and rl.colliderect(pygame.Rect(dados["boss"]["x"], dados["boss"]["y"], 100, 100)):
                dados["boss"]["vida"] -= 1;
                dados["pontos"] += 10;
                dados["lista_lasers"].remove(laser)
                if dados["boss"]["vida"] <= 0: estado = 'WIN'
            for ast in dados["lista_ast"]:
                if rl.colliderect(pygame.Rect(ast["x"], ast["y"], 30, 30)):
                    ast["y"] = -200;
                    dados["pontos"] += 5;
                    dados["lista_lasers"].remove(laser)
            for n in dados["lista_nav"]:
                if rl.colliderect(pygame.Rect(n["x"], n["y"], 25, 25)):
                    n.update(criar_nave_inimiga(dados["nivel"]));
                    dados["pontos"] += 10;
                    dados["lista_lasers"].remove(laser)
            if laser["y"] < -20 and laser in dados["lista_lasers"]: dados["lista_lasers"].remove(laser)

        for it in dados["lista_itens"][:]:
            it["y"] += 4
            if rect_player.colliderect(pygame.Rect(it["x"], it["y"], 20, 20)):
                if it["tipo"] == "VIDA":
                    dados["vidas"] = min(5, dados["vidas"] + 1)
                elif it["tipo"] == "TIRO":
                    dados["tiros"] += 15
                else:
                    dados["pontos"] += 50
                dados["lista_itens"].remove(it)
        for e in lista_estrelas:
            e["y"] += e["vel"]
            if e["y"] > ALTURA: e["y"] = 0
        if dados["vidas"] <= 0: estado = 'GAMEOVER'

    # --- DESENHO ---
    tela.fill(PRETO)
    for e in lista_estrelas: pygame.draw.circle(tela, BRANCO, (e["x"], e["y"]), 1)

    if estado == 'PLAYING':
        if dados["boss"]["ativo"]:
            pygame.draw.rect(tela, ROXO, (dados["boss"]["x"], dados["boss"]["y"], 100, 100))
            pygame.draw.rect(tela, BRANCO, (dados["boss"]["x"] + 8, dados["boss"]["y"] + 8, 84, 84), 2)
            pygame.draw.rect(tela, VERDE, (LARGURA // 2 - 160, 30, dados["boss"]["vida"] * 4, 10))
            for a in dados["lista_atk_boss"]: pygame.draw.rect(tela, VERMELHO, (a["x"], a["y"], 15, 15))

        # JOGADOR E AURA CIANO
        if dados["tiros"] > 0: pygame.draw.circle(tela, CIANO, (int(dados["nave_x"]), int(dados["nave_y"])), 23, 2)
        pygame.draw.circle(tela, BRANCO, (int(dados["nave_x"]), int(dados["nave_y"])), 18)

        for l in dados["lista_lasers"]: pygame.draw.rect(tela, CIANO, (l["x"], l["y"], 4, 15))
        for ast in dados["lista_ast"]: pygame.draw.rect(tela, VERMELHO, (ast["x"], ast["y"], 30, 30))
        for n in dados["lista_nav"]: pygame.draw.rect(tela, AZUL, (n["x"], n["y"], 25, 25))

        # ITENS COM DETALHE BRANCO
        for it in dados["lista_itens"]:
            c = VERDE if it["tipo"] == "VIDA" else AMARELO if it["tipo"] == "PONTOS" else CIANO
            pygame.draw.rect(tela, c, (it["x"], it["y"], 20, 20))
            pygame.draw.rect(tela, BRANCO, (it["x"] + 6, it["y"] + 6, 8, 8))

        # HUD E AVISOS
        if dados["vidas"] <= 2:
            tela.blit(fonte_p.render("! PRIORIDADE: VIDA !", True, VERDE), (LARGURA // 2 - 80, 10))
        elif 8 <= dados["nivel"] < 10:
            tela.blit(fonte_p.render("ALERTA: BOSS SE APROXIMANDO!", True, VERMELHO), (LARGURA // 2 - 130, 10))

        tela.blit(fonte_p.render(f"PONTOS: {dados['pontos']}", True, AMARELO), (15, 15))
        tela.blit(fonte_p.render(f"VIDAS: {dados['vidas']}", True, VERDE), (15, 45))
        tela.blit(fonte_p.render(f"CARGAS LASER: {dados['tiros']}", True, CIANO), (15, 75))
        tela.blit(fonte_p.render(f"FASE: {dados['nivel']}", True, BRANCO), (LARGURA - 110, 15))

    elif estado == 'START':
        tela.blit(fonte_g.render("GALAXY'S GUARDIAN", True, BRANCO), (140, 220))
        tela.blit(fonte_p.render("PRESSIONE ESPAÇO PARA INICIAR", True, AMARELO), (235, 320))
    elif estado in ['GAMEOVER', 'WIN']:
        txt = "VITÓRIA!" if estado == 'WIN' else "FIM DE JOGO"
        cor = VERDE if estado == 'WIN' else VERMELHO
        tela.blit(fonte_g.render(txt, True, cor), (LARGURA // 2 - 120, 150))
        tela.blit(fonte_m.render(f"SCORE FINAL: {dados['pontos']} | FASE: {dados['nivel']}", True, BRANCO), (180, 250))
        tela.blit(fonte_p.render("Pressione 'R' para o Menu", True, AMARELO), (280, 400))

    pygame.display.flip()
    relogio.tick(60)