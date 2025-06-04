# https://youtu.be/AY9MnQ4x3zk?t=2685
# https://arexxuru.itch.io/pixel-floor-texture-pack-ground-tile

from typing import Any, List, Tuple, Union

import pygame


class Personaje:
    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        self.nombre: str = nombre
        self.vida: int = vida
        self.ataque: int = ataque
        # La posición inicial del personaje el primer index es la posición x y el segundo índice es la posición y
        self.defensa: int = defensa
        self.__x: int = (WIDTH // 2) - 900
        self.__y: int = HEIGHT - 400
        self.posicion: Tuple[int, int] = (self.__x, self.__y)
        self.ataque_contador: int = 0  # Contador de ataques
        self.velocidad: int = 10  # Velocidad de movimiento
        self.salto_tiempo_inicio: int = 0  # Tiempo de inicio del salto

        rutas_imagenes = {
            "posicion_normal": "./personajes/daniel/default.png",
            "primer_ataque": "./personajes/daniel/primer_ataque.png",
            "segundo_ataque": "./personajes/daniel/segundo_ataque.png",
            "agachado": "./personajes/daniel/agachado.png",
            "saltando": "./personajes/daniel/saltando.png",
            "defendiendose": "./personajes/daniel/defendiendose.png",
            "defendiendose_agachado": "./personajes/daniel/defendiendose_agachado.png",
            "ataque_especial": "./personajes/daniel/ataque_especial.png",
            # todo
        }
        tamano_imagen = (300, 300)
        self.sprites = {
            nombre: pygame.transform.scale(
                pygame.image.load(ruta).convert_alpha(), tamano_imagen
            )
            for nombre, ruta in rutas_imagenes.items()
        }

    @property
    def y(self: "Personaje") -> int:
        return self.__y

    @y.setter
    def y(self: "Personaje", value: int) -> None:
        self.__y = value
        self.posicion = (self.__x, self.__y)

    # @y.deleter
    # def y(self: "Personaje") -> None:
    #     del self.__y
    #     self.posicion = (self.__x, self.__y)

    @property
    def x(self: "Personaje") -> int:
        return self.__x

    @x.setter
    def x(self: "Personaje", value: int) -> None:
        self.__x = value
        self.posicion = (self.__x, self.__y)


pygame.init()
pygame.mixer.init()

# Music
# pygame.mixer.music.load(r"./assets/music/ManifiestoUrbano.org.mp3")
# pygame.mixer.music.play(loops=-1, start=0.0)

WIDTH: int
HEIGHT: int

info: Any = pygame.display.Info()

WIDTH, HEIGHT = info.current_w, info.current_h
WINDOW_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)

screen: pygame.Surface = pygame.display.set_mode(size=WINDOW_SIZE)

pygame.display.set_caption(title="Smashito")

clock: pygame.time.Clock = pygame.time.Clock()

# (height, width)
# surface: pygame.Surface = pygame.Surface(
#     size = (100, 200)
# )

backgrounds: Tuple[str, ...] = (
    r"./assets/background/background_layer_1.png",
    r"./assets/background/background_layer_2.png",
    r"./assets/background/background_layer_3.png",
)

background_surfaces: List[pygame.Surface] = list()

i: Union[pygame.Surface, str, int]
for i in backgrounds:
    background_surfaces.append(
        pygame.transform.scale(surface=pygame.image.load(i), size=WINDOW_SIZE)
    )

font: pygame.font.Font = pygame.font.Font(
    r"./fonts/CsdegitadrawnRegularDemo-XGJqP.otf", 50
)

text_surface = font.render("Smashito Ultimate", False, "Green")


suelo_sprite: pygame.Surface = pygame.image.load(r"./assets/ground.png")
suelo_sprite = pygame.transform.scale(suelo_sprite, (110, 50))

shop_sprite: pygame.Surface = pygame.image.load(r"./assets/decorations/shop.png")
shop_sprite = pygame.transform.scale(shop_sprite, (400, 400))


def extraer_sprites(
    imagen: pygame.Surface, columnas: int, ancho: int, alto: int
) -> list[pygame.Surface]:
    sprites: list[pygame.Surface] = []
    for i in range(columnas):
        rect = pygame.Rect(i * ancho, 0, ancho, alto)
        sprite = imagen.subsurface(rect).copy()
        sprites.append(sprite)
    return sprites


# Carga la imagen animada
sprite_sheet: pygame.Surface = pygame.image.load(
    "./assets/decorations/shop_anim.png"
).convert_alpha()

# Extraer los 6 sprites (cada uno de 118x128)
sprites_shop: list[pygame.Surface] = extraer_sprites(
    sprite_sheet, columnas=6, ancho=118, alto=128
)

sprites_shop = [pygame.transform.scale(sprite, (500, 500)) for sprite in sprites_shop]


def extraer_sprites_varios_tamanos(
    imagen: pygame.Surface, coordenadas: List[Tuple[int, int, int, int]]
) -> list[pygame.Surface]:
    sprites: list[pygame.Surface] = []
    for x, y, ancho, alto in coordenadas:
        rect = pygame.Rect(x, y, ancho, alto)
        sprite = imagen.subsurface(rect).copy()
        sprites.append(sprite)
    return sprites


personaje: Personaje = Personaje(
    nombre="daniel",
    vida=100,
    ataque=10,
    defensa=5,
)


# Añadir hitbox a los personajes
def obtener_hitbox(personaje: Personaje) -> pygame.Rect:
    # Ajusta el tamaño y posición de la hitbox según el sprite
    ancho, alto = 200, 250
    return pygame.Rect(personaje.x + 90, personaje.y + 30, ancho, alto)


# Variables para las barras del primer personaje
vida_actual = 100
escudo_actual = 100
barra_especial_actual = 30
BARRA_EXTRA_MAX = 100

# Tiempos para la barra extra del primer personaje
tiempo_ultimo_incremento = pygame.time.get_ticks()
INCREMENTO_BARRA_EXTRA = 20
INTERVALO_BARRA_EXTRA = 10000  # 10 segundos en milisegundos

# Crear un segundo personaje
personaje2: Personaje = Personaje(
    nombre="daniel2",
    vida=100,
    ataque=10,
    defensa=5,
)
# Posición inicial diferente para el segundo personaje
personaje2.x = (WIDTH // 2) + 300
personaje2.y = HEIGHT - 400

# Variables para las barras del segundo personaje
vida_actual2 = 100
escudo_actual2 = 100
barra_especial_actual2 = 0
BARRA_EXTRA_MAX2 = 100

# Tiempos para la barra extra del segundo personaje
tiempo_ultimo_incremento2 = pygame.time.get_ticks()
INCREMENTO_BARRA_EXTRA2 = 20
INTERVALO_BARRA_EXTRA2 = 10000  # 10 segundos en milisegundos

# Estado para el segundo personaje
estado_personaje2: str = "normal"


def dibujar_barras():
    x = 30
    y = 30
    ancho = 300
    alto = 30
    espacio = 15

    # Vida (rojo)
    pygame.draw.rect(screen, (60, 60, 60), (x, y, ancho, alto), border_radius=8)
    pygame.draw.rect(
        screen,
        (220, 40, 40),
        (x, y, ancho * (vida_actual / 100), alto),
        border_radius=8,
    )
    font_barra = pygame.font.SysFont(None, 28)
    txt_vida = font_barra.render(f"Vida: {vida_actual}", True, (255, 255, 255))
    screen.blit(txt_vida, (x + 10, y + 5))

    # Escudo (azul)
    y += alto + espacio
    pygame.draw.rect(screen, (60, 60, 60), (x, y, ancho, alto), border_radius=8)
    pygame.draw.rect(
        screen,
        (40, 100, 220),
        (x, y, ancho * (escudo_actual / 100), alto),
        border_radius=8,
    )
    txt_escudo = font_barra.render(f"Escudo: {escudo_actual}", True, (255, 255, 255))
    screen.blit(txt_escudo, (x + 10, y + 5))

    # Barra extra (verde)
    y += alto + espacio
    pygame.draw.rect(screen, (60, 60, 60), (x, y, ancho, alto), border_radius=8)
    pygame.draw.rect(
        screen,
        (40, 220, 80),
        (x, y, ancho * (barra_especial_actual / BARRA_EXTRA_MAX), alto),
        border_radius=8,
    )
    txt_extra = font_barra.render(
        f"Especial: {barra_especial_actual}", True, (255, 255, 255)
    )
    screen.blit(txt_extra, (x + 10, y + 5))

    # Barras del segundo personaje (derecha)
    x2 = WIDTH - ancho - 30
    y2 = 30

    pygame.draw.rect(screen, (60, 60, 60), (x2, y2, ancho, alto), border_radius=8)
    pygame.draw.rect(
        screen,
        (220, 40, 40),
        (x2, y2, ancho * (vida_actual2 / 100), alto),
        border_radius=8,
    )
    txt_vida2 = font_barra.render(f"Vida: {vida_actual2}", True, (255, 255, 255))
    screen.blit(txt_vida2, (x2 + 10, y2 + 5))

    y2 += alto + espacio
    pygame.draw.rect(screen, (60, 60, 60), (x2, y2, ancho, alto), border_radius=8)
    pygame.draw.rect(
        screen,
        (40, 100, 220),
        (x2, y2, ancho * (escudo_actual2 / 100), alto),
        border_radius=8,
    )
    txt_escudo2 = font_barra.render(f"Escudo: {escudo_actual2}", True, (255, 255, 255))
    screen.blit(txt_escudo2, (x2 + 10, y2 + 5))

    y2 += alto + espacio
    pygame.draw.rect(screen, (60, 60, 60), (x2, y2, ancho, alto), border_radius=8)
    pygame.draw.rect(
        screen,
        (40, 220, 80),
        (x2, y2, ancho * (barra_especial_actual2 / BARRA_EXTRA_MAX2), alto),
        border_radius=8,
    )
    txt_extra2 = font_barra.render(
        f"Especial: {barra_especial_actual2}", True, (255, 255, 255)
    )
    screen.blit(txt_extra2, (x2 + 10, y2 + 5))


def actualizar_barra_extra():
    global barra_especial_actual, tiempo_ultimo_incremento
    global barra_especial_actual2, tiempo_ultimo_incremento2
    ahora = pygame.time.get_ticks()
    if (
        barra_especial_actual < BARRA_EXTRA_MAX
        and ahora - tiempo_ultimo_incremento >= INTERVALO_BARRA_EXTRA
    ):
        barra_especial_actual = min(
            barra_especial_actual + INCREMENTO_BARRA_EXTRA, BARRA_EXTRA_MAX
        )
        tiempo_ultimo_incremento = ahora

    if (
        barra_especial_actual2 < BARRA_EXTRA_MAX2
        and ahora - tiempo_ultimo_incremento2 >= INTERVALO_BARRA_EXTRA2
    ):
        barra_especial_actual2 = min(
            barra_especial_actual2 + INCREMENTO_BARRA_EXTRA2, BARRA_EXTRA_MAX2
        )
        tiempo_ultimo_incremento2 = ahora


# Agregar una variable de estado para controlar la animación
estado_personaje: str = "normal"  # Puede ser "normal", "agachado", etc.

# Variables para controlar el desplazamiento durante el ataque especial
ataque_especial_en_progreso = False
ataque_especial_direccion = 0  # -1 para izquierda, 1 para derecha
ataque_especial_personaje = None  # Puede ser personaje o personaje2


def manejar_eventos():
    global estado_personaje, estado_personaje2
    global \
        ataque_especial_en_progreso, \
        ataque_especial_direccion, \
        ataque_especial_personaje

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # Controles para personaje 1
            if event.key == pygame.K_c:
                personaje.ataque_contador += 1
                if personaje.ataque_contador == 1:
                    estado_personaje = "primer_ataque"
                elif personaje.ataque_contador == 2:
                    estado_personaje = "segundo_ataque"
                    personaje.ataque_contador = 0
            # Ataque especial personaje 1 (tecla X)
            if event.key == pygame.K_x and not ataque_especial_en_progreso:
                estado_personaje = "ataque_especial"
                ataque_especial_en_progreso = True
                ataque_especial_personaje = personaje
                # Determinar dirección hacia personaje2
                if personaje.x < personaje2.x:
                    ataque_especial_direccion = 1
                else:
                    ataque_especial_direccion = -1
            # Controles para personaje 2
            if event.key == pygame.K_KP0:  # Numpad 0 para atacar
                personaje2.ataque_contador += 1
                if personaje2.ataque_contador == 1:
                    estado_personaje2 = "primer_ataque"
                elif personaje2.ataque_contador == 2:
                    estado_personaje2 = "segundo_ataque"
                    personaje2.ataque_contador = 0
            # Ataque especial personaje 2 (tecla Numpad 9)
            if event.key == pygame.K_KP9 and not ataque_especial_en_progreso:
                estado_personaje2 = "ataque_especial"
                ataque_especial_en_progreso = True
                ataque_especial_personaje = personaje2
                # Determinar dirección hacia personaje1
                if personaje2.x < personaje.x:
                    ataque_especial_direccion = 1
                else:
                    ataque_especial_direccion = -1
            elif event.key == pygame.K_KP7:  # Numpad 7 para defenderse
                estado_personaje2 = "defendiendose"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_KP7 and estado_personaje2 == "defendiendose":
                estado_personaje2 = "normal"
            # Volver a estado normal al soltar ataque especial
            if (
                event.key == pygame.K_x
                and estado_personaje == "ataque_especial"
                and not ataque_especial_en_progreso
            ):
                estado_personaje = "normal"
            if (
                event.key == pygame.K_KP9
                and estado_personaje2 == "ataque_especial"
                and not ataque_especial_en_progreso
            ):
                estado_personaje2 = "normal"

    # Movimiento continuo con teclas presionadas
    keys = pygame.key.get_pressed()
    # Si hay ataque especial en progreso, bloquear movimientos normales
    if ataque_especial_en_progreso:
        return

    # Personaje 1
    if keys[pygame.K_DOWN] and keys[pygame.K_w]:
        estado_personaje = "defendiendose_agachado"
    elif keys[pygame.K_w]:
        estado_personaje = "defendiendose"
    elif keys[pygame.K_DOWN]:
        estado_personaje = "agachado"
    elif keys[pygame.K_UP]:
        # Saltar solo si no está ya saltando
        if estado_personaje != "saltando":
            estado_personaje = "saltando"
            personaje.salto_tiempo_inicio = pygame.time.get_ticks()
    elif estado_personaje == "saltando":
        # Si se presiona abajo, cancelar salto
        if keys[pygame.K_DOWN]:
            estado_personaje = "normal"
        else:
            # Si se mantiene arriba, no mantener en el aire
            if not keys[pygame.K_UP]:
                tiempo_en_aire = pygame.time.get_ticks() - getattr(
                    personaje, "salto_tiempo_inicio", 0
                )
                if tiempo_en_aire >= 250:
                    estado_personaje = "normal"
    elif estado_personaje in (
        "agachado",
        "defendiendose",
        "defendiendose_agachado",
        "saltando",
    ):
        estado_personaje = "normal"
    if keys[pygame.K_RIGHT]:
        personaje.x += personaje.velocidad
    if keys[pygame.K_LEFT]:
        personaje.x -= personaje.velocidad
    # Personaje 2 (Numpad: 4, 6, 2 para izq, der, agacharse, 8 para saltar)
    if keys[pygame.K_KP2] and keys[pygame.K_KP7]:
        estado_personaje2 = "defendiendose_agachado"
    elif keys[pygame.K_KP7]:
        estado_personaje2 = "defendiendose"
    elif keys[pygame.K_KP2]:
        estado_personaje2 = "agachado"
    elif keys[pygame.K_KP8]:
        # Saltar solo si no está ya saltando
        if estado_personaje2 != "saltando":
            estado_personaje2 = "saltando"
            personaje2.salto_tiempo_inicio = pygame.time.get_ticks()
    elif estado_personaje2 == "saltando":
        # Si se presiona abajo, cancelar salto
        if keys[pygame.K_KP2]:
            estado_personaje2 = "normal"
        else:
            # Si se mantiene arriba, no mantener en el aire
            if not keys[pygame.K_KP8]:
                tiempo_en_aire2 = pygame.time.get_ticks() - getattr(
                    personaje2, "salto_tiempo_inicio", 0
                )
                if tiempo_en_aire2 >= 250:
                    estado_personaje2 = "normal"
    elif estado_personaje2 in (
        "agachado",
        "defendiendose",
        "defendiendose_agachado",
        "saltando",
    ):
        estado_personaje2 = "normal"
    if keys[pygame.K_KP6]:
        personaje2.x += personaje2.velocidad
    if keys[pygame.K_KP4]:
        personaje2.x -= personaje2.velocidad


def actualizar_ataque_especial():
    global \
        ataque_especial_en_progreso, \
        ataque_especial_direccion, \
        ataque_especial_personaje
    global estado_personaje, estado_personaje2
    global vida_actual, vida_actual2, escudo_actual, escudo_actual2
    global barra_especial_actual, barra_especial_actual2

    if not ataque_especial_en_progreso or ataque_especial_personaje is None:
        return

    # Determinar objetivo y estado
    if ataque_especial_personaje == personaje:
        objetivo = personaje2
        estado = "ataque_especial"
        barra_valor = barra_especial_actual
        objetivo_escudo = "escudo_actual2"
        objetivo_vida = "vida_actual2"
        objetivo_estado = estado_personaje2
    else:
        objetivo = personaje
        estado = "ataque_especial"
        barra_valor = barra_especial_actual2
        objetivo_escudo = "escudo_actual"
        objetivo_vida = "vida_actual"
        objetivo_estado = estado_personaje

    # Mover el personaje hacia el objetivo
    # Velocidad del ataque especial
    velocidad_especial = ataque_especial_personaje.velocidad * 5
    if ataque_especial_personaje.x < objetivo.x:
        ataque_especial_personaje.x = min(
            ataque_especial_personaje.x + velocidad_especial, objetivo.x
        )
    else:
        ataque_especial_personaje.x = max(
            ataque_especial_personaje.x - velocidad_especial, objetivo.x
        )

    # El objetivo no puede moverse (su estado se mantiene)
    # Cuando las hitboxes se tocan, termina el ataque especial y aplica daño
    hitbox_atacante = obtener_hitbox(ataque_especial_personaje)
    hitbox_objetivo = obtener_hitbox(objetivo)
    if hitbox_atacante.colliderect(hitbox_objetivo):
        # Calcular daño especial según barra especial
        def calcular_dano_especial(barra_valor):
            return int(10 + (barra_valor / 100) * 30)

        dano = calcular_dano_especial(barra_valor)
        # Si el objetivo está defendiendo y tiene escudo, dañar escudo
        if (
            ataque_especial_personaje == personaje
            and estado_personaje2 in ("defendiendose", "defendiendose_agachado")
            and escudo_actual2 > 0
        ):
            escudo_actual2 = max(escudo_actual2 - dano, 0)
        elif (
            ataque_especial_personaje == personaje2
            and estado_personaje in ("defendiendose", "defendiendose_agachado")
            and escudo_actual > 0
        ):
            escudo_actual = max(escudo_actual - dano, 0)
        else:
            if ataque_especial_personaje == personaje:
                vida_actual2 = max(vida_actual2 - dano, 0)
            else:
                vida_actual = max(vida_actual - dano, 0)
        # Reiniciar barra especial después de usar el ataque especial
        if ataque_especial_personaje == personaje:
            barra_especial_actual = 0
        else:
            barra_especial_actual2 = 0
        ataque_especial_en_progreso = False
        ataque_especial_personaje = None
        # Volver a estado normal después del ataque especial
        if estado == "ataque_especial":
            if objetivo == personaje2:
                estado_personaje = "normal"
            else:
                estado_personaje2 = "normal"


def dibujar():
    for fondo in background_surfaces:
        screen.blit(fondo, (0, 0))
    for n in range(0, WIDTH, 100):
        screen.blit(suelo_sprite, (n, HEIGHT - 110))

    dibujar_barras()
    sprite_map = {
        "agachado": ("agachado", (personaje.x, personaje.y)),
        "primer_ataque": ("primer_ataque", (personaje.x, personaje.y)),
        "segundo_ataque": ("segundo_ataque", (personaje.x, personaje.y)),
        "defendiendose": ("defendiendose", (personaje.x, personaje.y)),
        "defendiendose_agachado": (
            "defendiendose_agachado",
            (personaje.x, personaje.y + 5),
        ),
        "saltando": ("saltando", (personaje.x, personaje.y - 60)),
        "ataque_especial": ("ataque_especial", (personaje.x, personaje.y)),
        "normal": ("posicion_normal", (personaje.x, personaje.y)),
    }
    sprite_map2 = {
        "agachado": ("agachado", (personaje2.x, personaje2.y)),
        "primer_ataque": ("primer_ataque", (personaje2.x, personaje2.y)),
        "segundo_ataque": ("segundo_ataque", (personaje2.x, personaje2.y)),
        "defendiendose": ("defendiendose", (personaje2.x, personaje2.y)),
        "defendiendose_agachado": (
            "defendiendose_agachado",
            (personaje2.x, personaje2.y + 5),
        ),
        "saltando": ("saltando", (personaje2.x, personaje2.y - 60)),
        "ataque_especial": ("ataque_especial", (personaje2.x, personaje2.y)),
        "normal": ("posicion_normal", (personaje2.x, personaje2.y)),
    }

    sprite_key, pos = sprite_map.get(
        estado_personaje, ("posicion_normal", (personaje.x, personaje.y))
    )
    sprite = personaje.sprites.get(sprite_key)
    if sprite:
        screen.blit(sprite, pos)

    sprite_key2, pos2 = sprite_map2.get(
        estado_personaje2, ("posicion_normal", (personaje2.x, personaje2.y))
    )
    sprite2 = personaje2.sprites.get(sprite_key2)
    if sprite2:
        screen.blit(sprite2, pos2)

    # Dibujar hitboxes (opcional, para depuración)
    # pygame.draw.rect(screen, (255, 0, 0), obtener_hitbox(personaje), 2)
    # pygame.draw.rect(screen, (0, 0, 255), obtener_hitbox(personaje2), 2)


def detectar_colision_y_aplicar_dano():
    global vida_actual, vida_actual2, escudo_actual, escudo_actual2
    hitbox1 = obtener_hitbox(personaje)
    hitbox2 = obtener_hitbox(personaje2)

    # Calcular daño especial según barra especial
    def calcular_dano_especial(barra_valor):
        # Mínimo 10, máximo 40 (puedes ajustar estos valores)
        return int(10 + (barra_valor / 100) * 30)

    # Personaje 1 ataca a personaje 2
    if estado_personaje in ("primer_ataque", "segundo_ataque", "ataque_especial"):
        if hitbox1.colliderect(hitbox2):
            if (
                estado_personaje2 in ("defendiendose", "defendiendose_agachado")
                and escudo_actual2 > 0
            ):
                if estado_personaje == "ataque_especial":
                    dano = calcular_dano_especial(barra_especial_actual)
                    escudo_actual2 = max(escudo_actual2 - dano, 0)
                else:
                    escudo_actual2 = max(escudo_actual2 - 5, 0)
            else:
                if estado_personaje == "ataque_especial":
                    dano = calcular_dano_especial(barra_especial_actual)
                    vida_actual2 = max(vida_actual2 - dano, 0)
                else:
                    vida_actual2 = max(vida_actual2 - 5, 0)
    # Personaje 2 ataca a personaje 1
    if estado_personaje2 in ("primer_ataque", "segundo_ataque", "ataque_especial"):
        if hitbox2.colliderect(hitbox1):
            if (
                estado_personaje in ("defendiendose", "defendiendose_agachado")
                and escudo_actual > 0
            ):
                if estado_personaje2 == "ataque_especial":
                    dano = calcular_dano_especial(barra_especial_actual2)
                    escudo_actual = max(escudo_actual - dano, 0)
                else:
                    escudo_actual = max(escudo_actual - 5, 0)
            else:
                if estado_personaje2 == "ataque_especial":
                    dano = calcular_dano_especial(barra_especial_actual2)
                    vida_actual = max(vida_actual - dano, 0)
                else:
                    vida_actual = max(vida_actual - 5, 0)


# Recarga de escudo cada 5 segundos
ESCUDO_RECARGA_INTERVALO = 5000  # milisegundos
ultimo_recarga_escudo = pygame.time.get_ticks()
ultimo_recarga_escudo2 = pygame.time.get_ticks()


def recargar_escudos():
    global escudo_actual, escudo_actual2, ultimo_recarga_escudo, ultimo_recarga_escudo2
    ahora = pygame.time.get_ticks()
    if (
        escudo_actual < 100
        and ahora - ultimo_recarga_escudo >= ESCUDO_RECARGA_INTERVALO
    ):
        escudo_actual = min(escudo_actual + 5, 100)
        ultimo_recarga_escudo = ahora
    if (
        escudo_actual2 < 100
        and ahora - ultimo_recarga_escudo2 >= ESCUDO_RECARGA_INTERVALO
    ):
        escudo_actual2 = min(escudo_actual2 + 5, 100)
        ultimo_recarga_escudo2 = ahora


# Alternar ataques mientras la tecla 'c' esté presionada
ataque_alternar = False
ataque_tiempo_ultimo = 0
ATAQUE_INTERVALO = 200  # milisegundos

# Alternar ataques para personaje 2
ataque_alternar2 = False
ataque_tiempo_ultimo2 = 0
ATAQUE_INTERVALO2 = 200

while True:
    manejar_eventos()
    actualizar_barra_extra()
    actualizar_ataque_especial()

    # Alternar ataques si la tecla 'c' está presionada (personaje 1)
    keys = pygame.key.get_pressed()
    if not ataque_especial_en_progreso:
        if keys[pygame.K_c]:
            ahora = pygame.time.get_ticks()
            if not ataque_alternar or ahora - ataque_tiempo_ultimo > ATAQUE_INTERVALO:
                if not ataque_alternar:
                    personaje.ataque_contador = 0
                ataque_alternar = True
                personaje.ataque_contador += 1
                if personaje.ataque_contador == 1:
                    estado_personaje = "primer_ataque"
                elif personaje.ataque_contador == 2:
                    estado_personaje = "segundo_ataque"
                    personaje.ataque_contador = 0
                ataque_tiempo_ultimo = ahora
        else:
            if ataque_alternar:
                personaje.ataque_contador = 0
            ataque_alternar = False
            if estado_personaje in ("primer_ataque", "segundo_ataque"):
                estado_personaje = "normal"

        # Alternar ataques para personaje 2 (Numpad 0)
        if keys[pygame.K_KP0]:
            ahora2 = pygame.time.get_ticks()
            if (
                not ataque_alternar2
                or ahora2 - ataque_tiempo_ultimo2 > ATAQUE_INTERVALO2
            ):
                if not ataque_alternar2:
                    personaje2.ataque_contador = 0
                ataque_alternar2 = True
                personaje2.ataque_contador += 1
                if personaje2.ataque_contador == 1:
                    estado_personaje2 = "primer_ataque"
                elif personaje2.ataque_contador == 2:
                    estado_personaje2 = "segundo_ataque"
                    personaje2.ataque_contador = 0
                ataque_tiempo_ultimo2 = ahora2
        else:
            if ataque_alternar2:
                personaje2.ataque_contador = 0
            ataque_alternar2 = False
            if estado_personaje2 in ("primer_ataque", "segundo_ataque"):
                estado_personaje2 = "normal"

    detectar_colision_y_aplicar_dano()
    dibujar()
    recargar_escudos()
    pygame.display.update()
    clock.tick(60)
    # Voltear la imagen del personaje 2 para que mire hacia la derecha (solo una vez)
    if not hasattr(personaje2, "sprites_flipped"):
        for key in personaje2.sprites:
            personaje2.sprites[key] = pygame.transform.flip(
                personaje2.sprites[key], True, False
            )
        personaje2.sprites_flipped = True  # type: ignore

        # Rotación para ataque especial de "daniel"
        personaje_rotacion_angulo = 0
        personaje2_rotacion_angulo = 0

        def rotar_sprite(sprite, angulo):
            rect = sprite.get_rect()
            rotated = pygame.transform.rotate(sprite, angulo)
            rotated_rect = rotated.get_rect(center=rect.center)
            return rotated, rotated_rect

        # Sobrescribe dibujar para rotar si ataque especial y nombre es "daniel"
        _original_dibujar = dibujar
        def dibujar():
            for fondo in background_surfaces:
                screen.blit(fondo, (0, 0))
            for n in range(0, WIDTH, 100):
                screen.blit(suelo_sprite, (n, HEIGHT - 110))
            dibujar_barras()

            global personaje_rotacion_angulo, personaje2_rotacion_angulo

            # Personaje 1
            sprite_key, pos = {
                "agachado": ("agachado", (personaje.x, personaje.y)),
                "primer_ataque": ("primer_ataque", (personaje.x, personaje.y)),
                "segundo_ataque": ("segundo_ataque", (personaje.x, personaje.y)),
                "defendiendose": ("defendiendose", (personaje.x, personaje.y)),
                "defendiendose_agachado": ("defendiendose_agachado", (personaje.x, personaje.y + 5)),
                "saltando": ("saltando", (personaje.x, personaje.y - 60)),
                "ataque_especial": ("ataque_especial", (personaje.x, personaje.y)),
                "normal": ("posicion_normal", (personaje.x, personaje.y)),
            }.get(estado_personaje, ("posicion_normal", (personaje.x, personaje.y)))
            sprite = personaje.sprites.get(sprite_key)
            if sprite:
                if estado_personaje == "ataque_especial" and personaje.nombre == "daniel" and ataque_especial_en_progreso and ataque_especial_personaje == personaje:
                    personaje_rotacion_angulo = (personaje_rotacion_angulo + 45) % 360
                    rotated, rotated_rect = rotar_sprite(sprite, personaje_rotacion_angulo)
                    rotated_rect.topleft = pos
                    screen.blit(rotated, rotated_rect)
                else:
                    personaje_rotacion_angulo = 0
                    screen.blit(sprite, pos)

            # Personaje 2
            sprite_key2, pos2 = {
                "agachado": ("agachado", (personaje2.x, personaje2.y)),
                "primer_ataque": ("primer_ataque", (personaje2.x, personaje2.y)),
                "segundo_ataque": ("segundo_ataque", (personaje2.x, personaje2.y)),
                "defendiendose": ("defendiendose", (personaje2.x, personaje2.y)),
                "defendiendose_agachado": ("defendiendose_agachado", (personaje2.x, personaje2.y + 5)),
                "saltando": ("saltando", (personaje2.x, personaje2.y - 60)),
                "ataque_especial": ("ataque_especial", (personaje2.x, personaje2.y)),
                "normal": ("posicion_normal", (personaje2.x, personaje2.y)),
            }.get(estado_personaje2, ("posicion_normal", (personaje2.x, personaje2.y)))
            sprite2 = personaje2.sprites.get(sprite_key2)
            if sprite2:
                if estado_personaje2 == "ataque_especial" and personaje2.nombre == "daniel" and ataque_especial_en_progreso and ataque_especial_personaje == personaje2:
                    personaje2_rotacion_angulo = (personaje2_rotacion_angulo + 45) % 360
                    rotated2, rotated_rect2 = rotar_sprite(sprite2, personaje2_rotacion_angulo)
                    rotated_rect2.topleft = pos2
                    screen.blit(rotated2, rotated_rect2)
                else:
                    personaje2_rotacion_angulo = 0
                    screen.blit(sprite2, pos2)
        dibujar = dibujar
