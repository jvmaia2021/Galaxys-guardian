import pygame
import random
import time
import math

# --- Configurações Iniciais ---
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Galaxy's Guardian: Full Version")

# --- Cores ---
PRETO, BRANCO = (0, 0, 0), (255, 255, 255)
VERMELHO, AZUL, AMARELO, VERDE, CIANO, ROXO = (255, 50, 50), (0, 150, 255), (255, 255, 0), (0, 255, 100), (
0, 255, 255), (150, 0, 255)
LARANJA = (255, 165, 0)
ROSA = (255, 182, 193)

# --- Fontes ---
fonte_p = pygame.font.SysFont("arial", 22, bold=True)
fonte_m = pygame.font.SysFont("arial", 35, bold=True)
fonte_g = pygame.font.SysFont("arial", 60, bold=True)

DICAS = [
    "DICA: O escudo laranja consome 20 pontos por impacto!",
    "DICA: Você fica imune enquanto recupera os sistemas.",
    "DICA: Agora você precisa de pontos para subir de fase!",
    "DICA: Os triângulos indicam a direção dos inimigos.",
    "DICA: A linha da zona de conforto aparece após 2 segundos.",
    "DICA: No nível 10, o Boss destruirá sua nave em segundos!",
    "DICA: Guarde lasers para as naves azuis rápidas.",
    "DICA: Quadrados verdes recuperam sua vida.",
    "DICA: O Boss tem um escudo, acerte o centro branco!",
    "DICA: Quadrados amarelos te dão mais pontos!",
    "Alguem realmente lê isso?",
    "DICA: Quadrados Ciano recarregam seus Lazers",
    "DICA: A Nave Roxa não é sua amiga!",
    "Vamos salvar a galáxia?",
    "Nós somos os vilões?",
    "Quem é esse tal de Mestre Yoga?",
    "Já não existe uma franquia com esse nome?",
    "DICA: É mais facil ganhar se você não bater!",
    "DICA: As naves que vêm da lateral são inimigas!",
    "DICA: A cada 50 pontos você sobre de fase!",
    "Existem gatos galáticos?",
    "DICA: Aperte espaço para atirar!",
    "Fui atingido! Alguém me ouve?",
    "DICA: Saia da Zona de Conforto",
    "DICA: A Zona de Conforto tira seus pontos!",
    "De quem foi essa maldita ideia?",
    "A Zona de Conforto não faz sentido!"
]


# --- Funções de Desenho ---
def desenhar_triangulo(surface, cor, centro, tamanho, direcao="CIMA"):
    x, y = centro
    if direcao == "CIMA":
        pts = [(x, y - tamanho), (x - tamanho, y + tamanho), (x + tamanho, y + tamanho)]
    elif direcao == "DIREITA":
        pts = [(x + tamanho, y), (x - tamanho, y - tamanho), (x - tamanho, y + tamanho)]
    elif direcao == "ESQUERDA":
        pts = [(x - tamanho, y), (x + tamanho, y - tamanho), (x + tamanho, y + tamanho)]
    pygame.draw.polygon(surface, cor, pts)


def criar_asteroide(nivel=1):
    vel_ajustada = 4 + (nivel * 0.8)
    variacao = random.randint(0, 7)
    tamanho = 30 + variacao
    return {"x": random.randint(0, LARGURA - tamanho), "y": random.randint(-600, -50),
            "vel": random.uniform(vel_ajustada, vel_ajustada + 2), "tam": tamanho}


def criar_nave_inimiga(nivel=1):
    direcao = random.choice([1, -1])
    x_inicial = -100 if direcao == 1 else LARGURA + 100
    return {"x": x_inicial, "y": random.randint(50, ALTURA - 220), "vel_x": (5 + (nivel * 0.6)) * direcao,
            "direcao": direcao}


def criar_nave_roxa(nivel=1):
    # Velocidade base de 2, mas aumenta 0.15 por nível (sempre mais lento que outros inimigos)
    vel_base = 2 + (nivel * 0.17)
    return {
        "x": random.randint(50, LARGURA - 50),
        "y": -40,
        "vel_y": vel_base,
        "vel_x": 0
    }


def criar_item(dados, emergencia_vida=False):
    # 1. Se for emergência (vidas <= 2), prioridade total para Vida
    if emergencia_vida:
        return {"x": random.randint(50, LARGURA - 50), "y": -50, "vel": 4, "tipo": "VIDA"}

    # 2. Criamos a lista de possibilidades (pool)
    pool = ["PONTOS", "TIRO"]  # Itens que sempre podem cair

    # 3. Adicionamos os outros APENAS se não estiverem lotados
    if dados["vidas"] < dados["vidas_max"]:
        pool.append("VIDA")

    if dados["escudo"] < 15:
        pool.append("ESCUDO")

    if dados["plasma_tiros"] < 10:
        pool.append("PLASMA")

    # 4. Sorteia um dos itens permitidos
    tipo = random.choice(pool)

    return {"x": random.randint(50, LARGURA - 50), "y": -50, "vel": 4, "tipo": tipo}

def tela_loading():
    estrelas_loading = [
        {"x": random.randint(0, LARGURA), "y": random.randint(0, ALTURA), "vel": random.randint(1, 3)}
        for _ in range(40)
    ]
    dica = random.choice(DICAS)  # INICIALIZAR AQUI
    ultimo_troca_dica = time.time()  # INICIALIZAR AQUI
    progresso = 0
    esperando = True
    while esperando:
        tempo_atual = time.time()  # MOVER PARA DENTRO DO LOOP
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); exit()
            if progresso >= 100 and evento.type == pygame.KEYDOWN: esperando = False

        tela.fill(PRETO)
        if estado_jogo in ['START', 'LOADING']: gerenciar_fundo_organico()
        larg_b, alt_b = 300, 20
        x_b, y_b = LARGURA // 2 - larg_b // 2, ALTURA // 2
        pygame.draw.rect(tela, BRANCO, (x_b, y_b, larg_b, alt_b), 2)
        pygame.draw.rect(tela, VERDE, (x_b + 2, y_b + 2, min(progresso, 100) * 2.96, alt_b - 4))

        for e in estrelas_loading:
            e["y"] += e["vel"]
            if e["y"] > ALTURA:
                e["y"] = 0
                e["x"] = random.randint(0, LARGURA)
            pygame.draw.circle(tela, BRANCO, (e["x"], e["y"]), 1)

        if progresso < 100:
            txt = fonte_m.render("RECALIBRANDO SISTEMAS...", True, BRANCO)
            progresso += 0.8
        else:
            txt = fonte_m.render("DECOLAGEM AUTORIZADA!", True, VERDE)
            txt_k = fonte_p.render("PRESSIONE QUALQUER TECLA", True, BRANCO)
            tela.blit(txt_k, (LARGURA // 2 - txt_k.get_width() // 2, y_b + 80))
            # Trocar dica a cada 5 segundos após carregar
            if tempo_atual - ultimo_troca_dica >= 3:
                dica = random.choice(DICAS)
                ultimo_troca_dica = tempo_atual

        tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, y_b - 50))
        txt_d = fonte_p.render(dica, True, AMARELO)
        tela.blit(txt_d, (LARGURA // 2 - txt_d.get_width() // 2, y_b + 40))
        pygame.display.flip()
        time.sleep(0.01)


def reset_jogo():
    return {
        "nave_x": LARGURA // 2, "nave_y": ALTURA // 2,
        "vidas": 5, "pontos": 0, "nivel": 1, "tiros": 10, "escudo": 1,
        "vidas_max": 5,
        "boss": {
            "x": LARGURA // 2 - 50,
            "y": -150,
            "vida": 100,
            "vida_max": 100,
            "ativo": False,
            "vel_x": 5,
            "derrotado": False,
            "nucleo_quebrado": False,
            "regenerou": False,  # Controle de regeneração única
            "pulsando": False,
            "pulso_timer": 0
        },
        "lista_ast": [criar_asteroide(1) for _ in range(4)],
        "lista_nav": [], "lista_itens": [], "lista_lasers": [], "lista_atk_boss": [], "particulas": [],
        "zona_timer": 0,
        "fora_zona_timer": 0,
        "estado": "NORMAL",
        "zona_y_limite": ALTURA - 80,
        "lista_nav_roxas": [],
        "plasma_tiros": 0,
        "msg_timer": 0,
        "msg_texto": "",
        "msg_cor": ROSA,

    }

dados_fundo = {"naves": [], "proximo_spawn": time.time() + 5}
dados = reset_jogo()
dados["fim_timer"] = 0
lista_estrelas = [{"x": random.randint(0, LARGURA), "y": random.randint(0, ALTURA), "vel": random.randint(1, 3)} for _
                  in range(50)]
relogio = pygame.time.Clock()
estado_jogo = 'START'

TIMER_ITEM = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_ITEM, 10000)
TIMER_ATAQUE_BOSS = pygame.USEREVENT + 2

def gerenciar_fundo_organico():
    agora = time.time()
    # Spawn controlado: chance baixa e respeitando tempo
    if agora > dados_fundo["proximo_spawn"] and len(dados_fundo["naves"]) == 0:
        if random.random() < 0.05:
            # Cria a branca (líder)
            lider = {"x": -50, "y": random.randint(100, 500), "ang": random.uniform(-0.5, 0.5), "cor": BRANCO, "vel": 3}
            dados_fundo["naves"].append(lider)
            # Cria 1 ou 2 azuis seguindo
            for i in range(random.randint(1, 2)):
                dados_fundo["naves"].append({"x": -80 - (i*30), "y": lider["y"], "ang": lider["ang"], "cor": AZUL, "vel": 3, "atraso": True})
            dados_fundo["proximo_spawn"] = agora + random.randint(10, 20) # Demora para aparecer de novo

    for n in dados_fundo["naves"][:]:
        # Movimento com leve curva (ajuste de rota)
        n["ang"] += random.uniform(-0.02, 0.02)
        n["x"] += math.cos(n["ang"]) * n["vel"]
        n["y"] += math.sin(n["ang"]) * n["vel"]

        # Desenho com rotação (usando math.degrees para converter o ângulo)
        # Como o seu desenhar_triangulo é fixo, podemos usar uma versão simples aqui:
        pontos = [
            (n["x"] + math.cos(n["ang"]) * 10, n["y"] + math.sin(n["ang"]) * 10),
            (n["x"] + math.cos(n["ang"] + 2.5) * 7, n["y"] + math.sin(n["ang"] + 2.5) * 7),
            (n["x"] + math.cos(n["ang"] - 2.5) * 7, n["y"] + math.sin(n["ang"] - 2.5) * 7)
        ]
        pygame.draw.polygon(tela, n["cor"], pontos)

        # Remove apenas se sair muito da tela
        if n["x"] > LARGURA + 200 or n["x"] < -200 or n["y"] > ALTURA + 200 or n["y"] < -200:
            dados_fundo["naves"].remove(n)

# --- LOOP PRINCIPAL ---
while True:
    agora = time.time()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: pygame.quit(); exit()
        if estado_jogo in ['PLAYING', 'WIN_DELAY', 'GAMEOVER_DELAY']:

            if estado_jogo == 'PLAYING':
                # Naves Roxas (Raras, inclusive no Boss)
                chance_roxa = 0.05 if dados["boss"]["ativo"] else 0.003
                if random.random() < chance_roxa:
                    dados["lista_nav_roxas"].append(criar_nave_roxa(dados["nivel"]))
                    dados["msg_texto"] = "CUIDADO: SENTINELA DETECTADA!"
                    dados["msg_cor"] = ROXO
                    dados["msg_timer"] = 2

            if evento.type == TIMER_ITEM and estado_jogo == 'PLAYING':
                # Passamos o dicionário completo e a verificação de emergência
                novo_item = criar_item(dados, emergencia_vida=(dados["vidas"] <= 2))
                dados["lista_itens"].append(novo_item)

            if evento.type == TIMER_ATAQUE_BOSS and dados["boss"]["ativo"] and estado_jogo == 'PLAYING':
                for i in range(-2, 3):
                    dados["lista_atk_boss"].append(
                        {"x": dados["boss"]["x"] + 50, "y": dados["boss"]["y"] + 100, "vel_y": 7, "vel_x": i * 2})
            if evento.type == pygame.KEYDOWN and estado_jogo == 'PLAYING':
                if evento.key == pygame.K_SPACE and dados["tiros"] > 0 and dados["estado"] != "PENALIZADO":
                    dados["lista_lasers"].append({
                        "x": dados["nave_x"],
                        "y": dados["nave_y"] - 20,
                        "vel": 14,
                        "plasma": dados["plasma_tiros"] > 0
                    })

                    dados["tiros"] -= 1
                    if dados["plasma_tiros"] > 0:
                        dados["plasma_tiros"] -= 1

        elif evento.type == pygame.KEYDOWN:
            if estado_jogo == 'START' and evento.key == pygame.K_SPACE:
                tela_loading();
                dados = reset_jogo();
                estado_jogo = 'PLAYING'
            elif estado_jogo in ['GAMEOVER', 'WIN'] and evento.type == pygame.KEYDOWN:
                estado_jogo = 'START'

    if estado_jogo in ['PLAYING', 'WIN_DELAY', 'GAMEOVER_DELAY']:
        # desenha tudo normalmente
        # --- LÓGICA DE MOVIMENTO E JOGO ---
        if estado_jogo == 'PLAYING':  # <--- ESTA É A TRAVA
            teclas = pygame.key.get_pressed()
            v = 8
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:  dados["nave_x"] -= v
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: dados["nave_x"] += v
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:    dados["nave_y"] -= v
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:  dados["nave_y"] += v

            # Mantenha o limite da tela e a lógica da zona de conforto aqui dentro também!
            dados["nave_x"] = max(20, min(LARGURA - 20, dados["nave_x"]))
            dados["nave_y"] = max(20, min(ALTURA - 20, dados["nave_y"]))

        # Lógica da Zona de Conforto
        dt = relogio.get_time() / 1000

        if dados["nave_y"] > dados["zona_y_limite"]:
            dados["zona_timer"] += dt
            dados["fora_zona_timer"] = 0

            if dados["zona_timer"] >= 6:
                dados["estado"] = "PENALIZADO"
                dados["pontos"] = max(0, dados["pontos"] - 0.2)

        else:
            if dados["zona_timer"] > 0:
                dados["fora_zona_timer"] += dt

                # Caso 1: saiu antes da penalidade
                if dados["estado"] == "NORMAL" and dados["fora_zona_timer"] >= 1:
                    dados["zona_timer"] = 0
                    dados["fora_zona_timer"] = 0

                # Caso 2: estava penalizado → reativação correta
                elif dados["estado"] == "PENALIZADO" and dados["fora_zona_timer"] >= 3:
                    dados["estado"] = "NORMAL"
                    dados["zona_timer"] = 0
                    dados["fora_zona_timer"] = 0

        # Progressão por Pontos
        if dados["nivel"] < 10 and dados["pontos"] >= dados["nivel"] * 50:
            dados["nivel"] += 1
            if dados["nivel"] == 10:
                dados["boss"]["ativo"] = True
                pygame.time.set_timer(TIMER_ATAQUE_BOSS, 1000)
                dados["lista_ast"].clear()  # Asteroides param no Boss

        rect_p = pygame.Rect(dados["nave_x"] - 12, dados["nave_y"] - 12, 24, 24)

        # Asteroides (Só aparecem antes do Boss)
        if not dados["boss"]["ativo"]:
            for ast in dados["lista_ast"]:
                ast["y"] += ast["vel"]
                if ast["y"] > ALTURA: ast.update(criar_asteroide(dados["nivel"])); dados["pontos"] += 1
                if rect_p.colliderect(pygame.Rect(ast["x"], ast["y"], ast["tam"], ast["tam"])):
                    if dados["estado"] == "NORMAL":
                        if dados["escudo"] > 0:
                            dados["escudo"] -= 1;
                            dados["pontos"] = max(0, dados["pontos"] - 20)
                        else:
                            dados["vidas"] -= 1
                    ast.update(criar_asteroide(dados["nivel"]))

        # Naves Azuis (Com IA de perseguição original)
        if dados["nivel"] >= 2 and not dados["boss"]["ativo"] and len(dados["lista_nav"]) < 3:
            if random.random() < 0.01: dados["lista_nav"].append(criar_nave_inimiga(dados["nivel"]))

        for n in dados["lista_nav"][:]:
            n["x"] += n["vel_x"]
            diff_y = dados["nave_y"] - n["y"]
            if abs(diff_y) > 5: n["y"] += (1.5 + (dados["nivel"] * 0.2)) if diff_y > 0 else -(
                    1.5 + (dados["nivel"] * 0.2))
            if rect_p.colliderect(pygame.Rect(n["x"] - 15, n["y"] - 15, 30, 30)):
                if dados["estado"] == "NORMAL":
                    if dados["escudo"] > 0:
                        dados["escudo"] -= 1;
                        dados["pontos"] = max(0, dados["pontos"] - 20)
                    else:
                        dados["vidas"] -= 1
                dados["lista_nav"].remove(n)
            elif n["x"] > LARGURA + 150 or n["x"] < -150:
                dados["lista_nav"].remove(n)

        # Naves Roxas
        for r in dados["lista_nav_roxas"][:]:
            dx = 0
            dy = r["vel_y"]

            # Movimento descendente
            r["y"] += dy

            # Perseguição horizontal suave
            diff_x = dados["nave_x"] - r["x"]
            if abs(diff_x) > 5:
                dx = 1 if diff_x > 0 else -1
                r["x"] += dx

            # Guarda a direção para o desenho
            r["dx"] = dx
            r["dy"] = dy

            # Colisão com o jogador
            if rect_p.colliderect(pygame.Rect(r["x"] - 12, r["y"] - 12, 24, 24)):
                dados["tiros"] = max(0, dados["tiros"] - 15)
                dados["lista_nav_roxas"].remove(r)

            # Saiu da tela
            elif r["y"] > ALTURA + 40:
                dados["lista_nav_roxas"].remove(r)

        # Boss e Partículas
        if dados["boss"]["ativo"]:
            if dados["boss"]["y"] < 60:
                dados["boss"]["y"] += 1
            else:
                dados["boss"]["x"] += dados["boss"]["vel_x"]
                if dados["boss"]["x"] <= 0 or dados["boss"]["x"] >= LARGURA - 100:
                    dados["boss"]["vel_x"] *= -1

                # Regeneração única do boss
                if (dados["boss"]["vida"] <= 15 and
                        not dados["boss"]["regenerou"] and
                        random.random() < 0.3):  # 30% de chance

                    regen = random.randint(10, 30)
                    dados["boss"]["vida"] = min(dados["boss"]["vida_max"], dados["boss"]["vida"] + regen)
                    dados["boss"]["regenerou"] = True
                    dados["boss"]["pulsando"] = True
                    dados["boss"]["pulso_timer"] = 2.0

                    dados["msg_texto"] = "A Nave-mãe parece estar se recuperando..."
                    dados["msg_cor"] = VERDE
                    dados["msg_timer"] = 2.5

                # Atualizar pulso
                if dados["boss"]["pulsando"]:
                    dados["boss"]["pulso_timer"] -= dt
                    if dados["boss"]["pulso_timer"] <= 0:
                        dados["boss"]["pulsando"] = False

            for atk in dados["lista_atk_boss"][:]:
                atk["y"] += atk["vel_y"];
                atk["x"] += atk["vel_x"]
                if rect_p.colliderect(pygame.Rect(atk["x"], atk["y"], 15, 15)):
                    if dados["estado"] == "NORMAL":
                        if dados["escudo"] > 0:
                            dados["escudo"] -= 1;
                            dados["pontos"] = max(0, dados["pontos"] - 20)
                        else:
                            dados["vidas"] -= 1
                    dados["lista_atk_boss"].remove(atk)
                elif atk["y"] > ALTURA:
                    dados["lista_atk_boss"].remove(atk)

        # --- LASERS E COLISÕES (SUBSTITUIR AQUI) ---
        for l in dados["lista_lasers"][:]:
            l["y"] -= l["vel"]
            rl = pygame.Rect(l["x"] - 2, l["y"], 4, 15)
            hit = False

            # 1. Colisão com o Boss
            if dados["boss"]["ativo"] and rl.colliderect(
                    pygame.Rect(dados["boss"]["x"], dados["boss"]["y"], 100, 100)):
                dano = 3 if l.get("plasma", False) else 1
                dados["boss"]["vida"] -= dano

                if dados["boss"]["vida"] <= dados["boss"]["vida_max"] / 2 and not dados["boss"]["nucleo_quebrado"]:
                    dados["boss"]["nucleo_quebrado"] = True
                    num_powerups = random.randint(3, 6)
                    espacamento = 35
                    inicio_x = dados["boss"]["x"] + 50 - (num_powerups * espacamento) // 2
                    for i in range(num_powerups):
                        tipo = random.choice(["VIDA", "TIRO", "ESCUDO", "PONTOS"])
                        dados["lista_itens"].append({
                            "x": inicio_x + (i * espacamento) + random.randint(-5, 5),
                            "y": dados["boss"]["y"] + 50 + random.randint(-10, 10),
                            "vel": 4, "tipo": tipo
                        })
                    dados["msg_texto"] = "NÚCLEO DA NAVE-MÃE DESTRUÍDO!"
                    dados["msg_cor"] = BRANCO
                    dados["msg_timer"] = 2

                dados["pontos"] += 2
                hit = True
                for _ in range(3):
                    dados["particulas"].append(
                        {"x": l["x"], "y": l["y"], "vx": random.uniform(-2, 2), "vy": random.uniform(-2, 2),
                         "t": 30})

                if dados["boss"]["vida"] <= 0:
                    estado_jogo = 'WIN_DELAY'
                    dados["fim_timer"] = 2.5
                    dados["particulas"].clear()
                    for _ in range(70):
                        dados["particulas"].append({"x": dados["boss"]["x"] + 50, "y": dados["boss"]["y"] + 50,
                                                    "vx": random.uniform(-3, 3), "vy": random.uniform(-3, 3),
                                                    "t": random.randint(30, 60), "cor": ROXO})

            # 2. Colisão com Naves Roxas (Sentinelas)
            if not hit:
                for r in dados["lista_nav_roxas"][:]:
                    if rl.colliderect(pygame.Rect(r["x"] - 12, r["y"] - 12, 24, 24)):
                        if l.get("plasma", False):
                            dados["lista_nav_roxas"].remove(r)
                            dados["pontos"] += 50
                            hit = True
                        else:
                            hit = True  # Laser comum não mata, mas some
                        break

            # 3. Colisão com Naves Azuis
            if not hit:
                for n in dados["lista_nav"][:]:
                    if rl.colliderect(pygame.Rect(n["x"] - 15, n["y"] - 15, 30, 30)):
                        dados["lista_nav"].remove(n)
                        dados["pontos"] += 40 if l.get("plasma", False) else 20
                        hit = True
                        break

            # 4. Colisão com Asteroides
            if not hit and not dados["boss"]["ativo"]:
                for ast in dados["lista_ast"]:
                    if rl.colliderect(pygame.Rect(ast["x"], ast["y"], ast["tam"], ast["tam"])):
                        ast.update(criar_asteroide(dados["nivel"]))
                        dados["pontos"] += 10 if l.get("plasma", False) else 5
                        hit = True
                        break

            # Remove o laser se ele bater em algo ou sair da tela
            if l["y"] < -20 or hit:
                if l in dados["lista_lasers"]:
                    dados["lista_lasers"].remove(l)

        # Itens
        for it in dados["lista_itens"][:]:
            it["y"] += 4
            if rect_p.colliderect(pygame.Rect(it["x"], it["y"], 20, 20)):
                if it["tipo"] == "VIDA":
                    dados["vidas"] = min(dados["vidas_max"], dados["vidas"] + 1)
                elif it["tipo"] == "TIRO":
                    dados["tiros"] += 15
                elif it["tipo"] == "PONTOS":
                    dados["pontos"] += 80
                elif it["tipo"] == "ESCUDO":
                    dados["escudo"] = min(15, dados["escudo"] + 5)
                elif it["tipo"] == "PLASMA":
                    dados["plasma_tiros"] = 10
                    dados["msg_texto"] = "AMPLIFICADOR DE PLASMA ATIVADO!"
                    dados["msg_cor"] = ROSA
                    dados["msg_timer"] = 2.5

                dados["lista_itens"].remove(it)

        for p in dados["particulas"][:]:
            p["x"] += p["vx"];
            p["y"] += p["vy"];
            p["t"] -= 1

            pygame.draw.circle(tela, p.get("cor", BRANCO), (int(p["x"]), int(p["y"])), 2)

            if p["t"] <= 0:
                dados["particulas"].remove(p)

        if dados["vidas"] <= 0 and estado_jogo == 'PLAYING':
            estado_jogo = 'GAMEOVER_DELAY'
            dados["fim_timer"] = 2.0

            dados["particulas"].clear()
            for _ in range(50):
                dados["particulas"].append({
                    "x": dados["nave_x"],
                    "y": dados["nave_y"],
                    "vx": random.uniform(-4, 4),
                    "vy": random.uniform(-4, 4),
                    "t": random.randint(30, 50),
                    "cor": BRANCO
                })

    # --- DESENHO ---
    tela.fill(PRETO)

    # 1. Estrelas (Fundo)
    for e in lista_estrelas:
        e["y"] += e["vel"]
        if e["y"] > ALTURA: e["y"] = 0
        pygame.draw.circle(tela, BRANCO, (e["x"], e["y"]), 1)

    # 2. SISTEMA DE PARTÍCULAS (Mova para cá para aparecerem no Delay!)
    for p in dados["particulas"][:]:
        p["x"] += p.get("vx", 0)
        p["y"] += p.get("vy", 0)
        p["t"] -= 1
        pygame.draw.circle(tela, p.get("cor", BRANCO), (int(p["x"]), int(p["y"])), 2)
        if p["t"] <= 0:
            dados["particulas"].remove(p)

    # 3. LÓGICA DO DELAY (CORRIGIDA)
    if estado_jogo in ['WIN_DELAY', 'GAMEOVER_DELAY']:
        dt = relogio.get_time() / 1000
        dados["fim_timer"] -= dt  # SUBTRAI APENAS UMA VEZ!

        if estado_jogo == 'GAMEOVER_DELAY':
            # Cria partículas brancas na nave
            for _ in range(3):
                dados["particulas"].append({
                    "x": dados["nave_x"], "y": dados["nave_y"],
                    "vx": random.uniform(-3, 3), "vy": random.uniform(-3, 3),
                    "t": 30, "cor": BRANCO
                })
            # Desenha a nave parada explodindo
            desenhar_triangulo(tela, BRANCO, (dados["nave_x"], dados["nave_y"]), 14, "CIMA")

        elif estado_jogo == 'WIN_DELAY':
            # Cria partículas roxas no Boss
            for _ in range(3):
                dados["particulas"].append({
                    "x": dados["boss"]["x"] + 50, "y": dados["boss"]["y"] + 50,
                    "vx": random.uniform(-5, 5), "vy": random.uniform(-5, 5),
                    "t": 40, "cor": ROXO
                })
            # Desenha o Boss parado explodindo
            pygame.draw.rect(tela, ROXO, (dados["boss"]["x"], dados["boss"]["y"], 100, 100))

        # Muda de estado apenas quando o timer realmente zerar
        if dados["fim_timer"] <= 0:
            estado_jogo = 'WIN' if estado_jogo == 'WIN_DELAY' else 'GAMEOVER'

    if estado_jogo == 'PLAYING':
        # UI Prioritária
        msg, cor_m = None, BRANCO
        if dados["vidas"] <= 2:
            msg, cor_m = "! PRIORIDADE: ESTADO CRÍTICO DE VIDA !", VERDE
        elif dados["estado"] == "PENALIZADO":
            msg, cor_m = "!!! SISTEMAS DE ARMAS DESATIVADOS !!!", VERMELHO
        elif dados["estado"] == "REATIVANDO":
            msg, cor_m = "REATIVANDO SISTEMAS...", CIANO
        elif dados["nivel"] >= 9:
            msg, cor_m = "ALERTA: RASTRO DA NAVE MÃE DETECTADO!", VERMELHO
        elif dados["zona_timer"] >= 2:
            msg, cor_m = "AVISO: VOCÊ ESTÁ NA ZONA DE CONFORTO!", AMARELO
            alpha = int(80 + 60 * math.sin(time.time() * 3))
            s = pygame.Surface((LARGURA, 2));
            s.set_alpha(abs(alpha));
            s.fill(AMARELO)
            tela.blit(s, (0, dados["zona_y_limite"]))
        if msg:
            txt = fonte_p.render(msg, True, cor_m)
            tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, 25))
        if dados["msg_timer"] > 0:
            dados["msg_timer"] -= dt
            txt = fonte_p.render(dados["msg_texto"], True, dados["msg_cor"])
            tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, 55))

        # Linha da Zona de Conforto (independente de avisos)
        if dados["zona_timer"] >= 2:
            alpha = int(80 + 60 * math.sin(time.time() * 3))
            s = pygame.Surface((LARGURA, 2))
            s.set_alpha(alpha)
            s.fill(AMARELO)
            tela.blit(s, (0, dados["zona_y_limite"]))

        # Jogador (Triângulo Centralizado + Auras)
        # Jogador (visível em PLAYING e GAMEOVER_DELAY)
        if estado_jogo == 'PLAYING' or estado_jogo == 'GAMEOVER_DELAY':
            cor_n = BRANCO
        if dados["estado"] != "NORMAL" and (int(agora * 10) % 2 == 0): cor_n = AMARELO
        if dados["escudo"] > 0:
            pygame.draw.circle(tela, LARANJA, (int(dados["nave_x"]), int(dados["nave_y"])), 32, 2)

        if dados["tiros"] > 0:
            aura_cor = ROSA if dados["plasma_tiros"] > 0 else CIANO
            pygame.draw.circle(tela, aura_cor, (int(dados["nave_x"]), int(dados["nave_y"])), 28, 2)

        desenhar_triangulo(
            tela,
            cor_n,
            (dados["nave_x"], dados["nave_y"]),
            14,
            "CIMA"
        )

        # Inimigos e Itens
        for ast in dados["lista_ast"]:
            pygame.draw.rect(tela, VERMELHO, (ast["x"], ast["y"], ast["tam"], ast["tam"]))
            pygame.draw.rect(tela, BRANCO, (ast["x"], ast["y"], ast["tam"], ast["tam"]), 1)
        for n in dados["lista_nav"]:
            desenhar_triangulo(tela, AZUL, (n["x"], n["y"]), 15, "DIREITA" if n["direcao"] == 1 else "ESQUERDA")
        for r in dados["lista_nav_roxas"]:
            # Decide a direção visual com base no movimento
            if abs(r.get("dx", 0)) > abs(r.get("dy", 1)):
                direcao = "DIREITA" if r.get("dx", 0) > 0 else "ESQUERDA"
            else:
                direcao = "CIMA"
            desenhar_triangulo(
                tela,
                ROXO,
                (int(r["x"]), int(r["y"])),
                12,
                direcao
            )
        for it in dados["lista_itens"]:
            if it["tipo"] == "VIDA":
                c = VERDE
            elif it["tipo"] == "PONTOS":
                c = AMARELO
            elif it["tipo"] == "ESCUDO":
                c = LARANJA
            elif it["tipo"] == "TIRO":
                c = CIANO
            elif it["tipo"] == "PLASMA":
                c = ROSA
            pygame.draw.rect(tela, c, (it["x"], it["y"], 20, 20))
            # Núcleo branco central (identidade visual clássica)
            pygame.draw.rect(
                tela,
                BRANCO,
                (it["x"] + 4, it["y"] + 4, 12, 12)
            )
        for p in dados["particulas"]: pygame.draw.circle(tela, ROXO, (int(p["x"]), int(p["y"])), 3)
        # Boss (visível em PLAYING e WIN_DELAY)
        if dados["boss"]["ativo"] and (estado_jogo == 'PLAYING' or estado_jogo == 'WIN_DELAY'):
            # Efeito de pulso (regeneração)
            alpha_boss = 255
            if dados["boss"]["pulsando"]:
                alpha_boss = int(200 + 55 * math.sin(time.time() * 8))

            boss_surface = pygame.Surface((100, 100))
            boss_surface.set_alpha(alpha_boss)
            boss_surface.fill(ROXO)
            tela.blit(boss_surface, (dados["boss"]["x"], dados["boss"]["y"]))

            if not dados["boss"]["nucleo_quebrado"]:
                pygame.draw.rect(
                    tela,
                    BRANCO,
                    (dados["boss"]["x"] + 20, dados["boss"]["y"] + 20, 60, 60),
                    3
                )
            barra_x = LARGURA // 2 - 100
            barra_y = 10
            largura_total = 200

            # Vida perdida (fundo vermelho)
            pygame.draw.rect(tela, VERMELHO, (barra_x, barra_y, largura_total, 8))

            # Vida restante (verde)
            pygame.draw.rect(
                tela,
                VERDE,
                (barra_x, barra_y, largura_total * (dados["boss"]["vida"] / dados["boss"]["vida_max"]), 8)
            )
            for a in dados["lista_atk_boss"]: pygame.draw.circle(tela, VERMELHO, (int(a["x"]), int(a["y"])), 7)
        for l in dados["lista_lasers"]:
            cor_laser = ROSA if l.get("plasma", False) else CIANO
            pygame.draw.rect(tela, cor_laser, (l["x"] - 2, l["y"], 4, 15))

        # HUD
        tela.blit(fonte_p.render(f"PONTOS: {int(dados['pontos'])}", True, AMARELO), (15, 15))
        tela.blit(fonte_p.render(f"VIDAS: {dados['vidas']}", True, VERDE), (15, 45))
        tela.blit(fonte_p.render(f"LASER: {dados['tiros']}", True, CIANO), (15, 75))
        if dados["escudo"] > 0: tela.blit(fonte_p.render(f"ESCUDO: {dados['escudo']}", True, LARANJA), (15, 105))
        tela.blit(fonte_p.render(f"FASE: {dados['nivel']}", True, BRANCO), (LARGURA - 110, 15))

    elif estado_jogo == 'START':
        t1 = fonte_g.render("GALAXY'S GUARDIAN", True, BRANCO)
        tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 220))
        t2 = fonte_p.render("PRESSIONE ESPAÇO PARA INICIAR", True, AMARELO)
        tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 320))


    elif estado_jogo == 'WIN':
        t1 = fonte_g.render("VITÓRIA!", True, VERDE)
        tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 130))
        t2 = fonte_m.render(
            "Você derrotou os invasores da galáxia!",
            True, BRANCO
        )
        tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 210))
        t3 = fonte_p.render(
            "Após uma longa jornada, a nave-mãe foi destruída.",
            True, AMARELO
        )
        tela.blit(t3, (LARGURA // 2 - t3.get_width() // 2, 250))
        t4 = fonte_p.render(
            "Os povos celebram... mas será este o fim?",
            True, AMARELO
        )
        tela.blit(t4, (LARGURA // 2 - t4.get_width() // 2, 280))
        t_s = fonte_p.render(f"SCORE FINAL: {int(dados['pontos'])}", True, BRANCO)
        tela.blit(t_s, (LARGURA // 2 - t_s.get_width() // 2, 330))
        t_r = fonte_p.render("PRESSIONE QUALQUER TECLA PARA VOLTAR AO INÍCIO", True, CIANO)
        tela.blit(t_r, (LARGURA // 2 - t_r.get_width() // 2, 390))


    elif estado_jogo == 'GAMEOVER':
        t1 = fonte_g.render("MISSÃO FRACASSADA", True, VERMELHO)
        tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 150))
        t2 = fonte_m.render("Hoje não foi um bom dia para os", True, BRANCO)
        tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 230))
        t3 = fonte_m.render("Guardiões da Galáxia.", True, BRANCO)
        tela.blit(t3, (LARGURA // 2 - t3.get_width() // 2, 270))
        t4 = fonte_p.render("Mas não desista. Retorne à sua nave", True, BRANCO)
        tela.blit(t4, (LARGURA // 2 - t4.get_width() // 2, 320))
        t5 = fonte_p.render("e tente novamente.", True, BRANCO)
        tela.blit(t5, (LARGURA // 2 - t5.get_width() // 2, 350))
        t_s = fonte_p.render(f"SCORE FINAL: {int(dados['pontos'])}", True, VERMELHO)
        tela.blit(t_s, (LARGURA // 2 - t_s.get_width() // 2, 400))
        t_r = fonte_p.render("PRESSIONE QUALQUER TECLA PARA RECOMEÇAR", True, AMARELO)
        tela.blit(t_r, (LARGURA // 2 - t_r.get_width() // 2, 450))

        # Atualiza e desenha TODAS as partículas ativas no sistema
        for p in dados["particulas"][:]:
            p["x"] += p.get("vx", 0)
            p["y"] += p.get("vy", 0)
            p["t"] -= 1
            # Pega a cor da partícula ou usa BRANCO como padrão
            cor_p = p.get("cor", BRANCO)
            pygame.draw.circle(tela, cor_p, (int(p["x"]), int(p["y"])), 2)

            if p["t"] <= 0:
                dados["particulas"].remove(p)

    pygame.display.flip()
    relogio.tick(60)
