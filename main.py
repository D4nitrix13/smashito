# Autor: Daniel Benjamin Perez Morales

# Recurso Para Quitar Fondo: https://www.remove.bg/upload
# https://arexxuru.itch.io/pixel-floor-texture-pack-ground-tile

from sys import argv, exit
from typing import Any, List, Tuple, Union

JUEGO_FINALIZADO = False
PERSONAJES_DISPONIBLES = ["daniel", "jeremy", "andy"]
if len(argv) < 2 or len(argv) >= 4:
    print(
        f"""
        \rAsi se usa el programa: {argv[0]} <name-personaje-1> <name-personaje-2>
    
        \rEjemplo: Asi se usa el programa: {argv[0]} daniel jeremy
    
        \rPersonajes disponibles:
        \r* Daniel
        \r* Jeremy
        \r* Andy
        """
    )
    exit(1)

argv[1] = argv[1].lower()
argv[-1] = argv[-1].lower()

personaje1_valido: bool = False
personaje2_valido: bool = False

for index, value in enumerate(iterable=argv[1 : len(argv) : 1], start=1):
    if index == 1 and value in PERSONAJES_DISPONIBLES:
        personaje1_valido = True
        continue

    if index == 2 and value in PERSONAJES_DISPONIBLES:
        personaje2_valido = True
        break
if not personaje1_valido or not personaje2_valido:
    print(
        f"""
        \rAsi se usa el programa: {argv[0]} <name-personaje-1> <name-personaje-2>
    
        \rEjemplo: Asi se usa el programa: {argv[0]} daniel jeremy
    
        \rPersonajes disponibles:
        \r* Daniel
        \r* Jeremy
        \r* Andy
        """
    )
    exit(1)

import pygame


class Personaje:
    def __init__(
        self, nombre: str, vida: int, ataque: int, posicion_derrotado: Tuple[int, int]
    ):
        self.nombre: str = nombre
        self.vida: int = vida
        self.ataque: int = ataque
        self.posicion_derrotado: Tuple[int, int] = posicion_derrotado
        # La posición inicial del personaje el primer index es la posición x y el segundo índice es la posición y
        self.__x: int = (WIDTH // 2) - 900
        self.__y: int = HEIGHT - 400
        self.posicion: Tuple[int, int] = (self.__x, self.__y)
        self.ataque_contador: int = 0  # Contador de ataques
        self.velocidad: int = 10  # Velocidad de movimiento
        self.salto_tiempo_inicio: int = 0  # Tiempo de inicio del salto

        rutas_imagenes = {
            "posicion_normal": f"./personajes/{self.nombre}/default.png",
            "primer_ataque": f"./personajes/{self.nombre}/primer_ataque.png",
            "segundo_ataque": f"./personajes/{self.nombre}/segundo_ataque.png",
            "agachado": f"./personajes/{self.nombre}/agachado.png",
            "saltando": f"./personajes/{self.nombre}/saltando.png",
            "defendiendose": f"./personajes/{self.nombre}/defendiendose.png",
            "defendiendose_agachado": f"./personajes/{self.nombre}/defendiendose_agachado.png",
            "ataque_especial": f"./personajes/{self.nombre}/ataque_especial.png",
            "derrotado": f"./personajes/{self.nombre}/derrotado.png",
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
        if -45 <= value <= 1640:
            self.__x = value
            self.posicion = (self.__x, self.__y)
            self.posicion_derrotado = (self.__x, self.posicion_derrotado[1])


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


# Coordenadas por personaje
coordenadas_derrota = {
    "daniel": ((WIDTH // 2) - 900, HEIGHT - 340),
    "jeremy": ((WIDTH // 2) - 900, HEIGHT - 320),
    "andy": ((WIDTH // 2) - 900, HEIGHT - 320),
}

nombre1 = argv[1]
nombre2 = argv[-1]

posicion_derrotado_personaje1 = coordenadas_derrota.get(nombre1, (0, 0))
posicion_derrotado_personaje2 = coordenadas_derrota.get(nombre2, (0, 0))

personaje = Personaje(
    nombre=nombre1,
    vida=100,
    ataque=10,
    posicion_derrotado=posicion_derrotado_personaje1,
)

personaje2 = Personaje(
    nombre=nombre2,
    vida=100,
    ataque=10,
    posicion_derrotado=posicion_derrotado_personaje2,
)


# Añadir hitbox a los personajes
def obtener_hitbox(personaje: Personaje) -> pygame.Rect:
    # Ajusta el tamaño y posición de la hitbox según el sprite
    ancho, alto = 200, 250
    return pygame.Rect(personaje.x + 90, personaje.y + 30, ancho, alto)


# Variables para las barras del primer personaje
vida_actual = 100
escudo_actual = 100
# Barra especial (extra) del primer personaje
barra_especial_actual = 50
BARRA_EXTRA_MAX = 100

# Tiempos para la barra extra del primer personaje
tiempo_ultimo_incremento = pygame.time.get_ticks()
INCREMENTO_BARRA_EXTRA = 20
INTERVALO_BARRA_EXTRA = 3000  # 3 segundos en milisegundos
INTERVALO_BARRA_EXTRA2 = 3000  # 3 segundos en milisegundos

# Posición inicial diferente para el segundo personaje
personaje2.x = (WIDTH // 2) + 300
personaje2.y = HEIGHT - 400

# Variables para las barras del segundo personaje
vida_actual2 = 100
escudo_actual2 = 100
barra_especial_actual2 = 50
BARRA_EXTRA_MAX2 = 100

# Tiempos para la barra extra del segundo personaje
tiempo_ultimo_incremento2 = pygame.time.get_ticks()
INCREMENTO_BARRA_EXTRA2 = 20

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
    # No actualizar si algún personaje está derrotado
    if vida_actual == 0 or vida_actual2 == 0:
        return
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

    # Si algún personaje está derrotado, bloquear todos los eventos excepto salir
    if vida_actual == 0 or vida_actual2 == 0:
        # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
        sonido = pygame.mixer.Sound("./assets/sound_effects/ganador.mp3")
        # Reproduce el sonido
        sonido.play()
        # Espera un poco para escuchar el sonido antes de que termine el script
        pygame.time.delay(1500)
        sonido.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        return

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
            if (
                event.key == pygame.K_x
                and not ataque_especial_en_progreso
                and barra_especial_actual > 0  # Solo si la barra es mayor a 0
            ):
                # region Tecla P1
                sonido = pygame.mixer.Sound(
                    "./assets/sound_effects/%s.mp3" % personaje.nombre
                )
                sonido.play()
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
            if (
                event.key == pygame.K_KP9
                and not ataque_especial_en_progreso
                and barra_especial_actual2 > 0  # Solo si la barra es mayor a 0
            ):
                # region Tecla p2
                sonido = pygame.mixer.Sound(
                    "./assets/sound_effects/%s.mp3" % personaje2.nombre
                )
                sonido.play()
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

    # Si algún personaje está derrotado, bloquear movimientos
    if vida_actual == 0 or vida_actual2 == 0:
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
            # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
            sonido = pygame.mixer.Sound("./assets/sound_effects/saltando.mp3")
            # Reproduce el sonido
            sonido.play()
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
            # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
            sonido = pygame.mixer.Sound("./assets/sound_effects/saltando.mp3")
            # Reproduce el sonido
            sonido.play()
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
    # region Stop Ataque especial
    global \
        ataque_especial_en_progreso, \
        ataque_especial_direccion, \
        ataque_especial_personaje
    global estado_personaje, estado_personaje2
    global vida_actual, vida_actual2, escudo_actual, escudo_actual2
    global barra_especial_actual, barra_especial_actual2

    # Si algún personaje está derrotado, no hacer nada
    if vida_actual == 0 or vida_actual2 == 0:
        return

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
    # Si algún personaje está derrotado, mostrar sprite derrotado y texto ganador

    if vida_actual == 0 or vida_actual2 == 0:
        if vida_actual == 0:
            # personaje 1 derrotado, personaje2 gana
            sprite = personaje.sprites.get("derrotado")

            if sprite:
                if personaje.nombre == "daniel":
                    screen.blit(sprite, personaje.posicion_derrotado)
                elif personaje.nombre == "jeremy":
                    screen.blit(sprite, personaje.posicion_derrotado)
                else:
                    # Andy
                    screen.blit(sprite, personaje.posicion_derrotado)

            # Solo aplicar si el personaje es jeremy sumarle 10 al eje y
            sprite2 = personaje2.sprites.get(
                "posicion_normal"
            )  # ganador en pose normal
            if sprite2:
                if personaje2.nombre.lower() == "jeremy":
                    screen.blit(sprite2, (personaje2.x, personaje2.y + 10))
                else:
                    screen.blit(sprite2, (personaje2.x, personaje2.y))
            ganador = personaje2.nombre.title()
        else:
            # personaje 2 derrotado, personaje gana
            sprite2 = personaje2.sprites.get("derrotado")
            if sprite2:
                screen.blit(sprite2, personaje.posicion_derrotado)
            sprite = personaje.sprites.get("posicion_normal")
            if sprite:
                # Solo aplicar si el personaje es jeremy sumarle 10 al eje y
                if personaje.nombre.lower() == "jeremy":
                    screen.blit(sprite, (personaje.x, personaje.y + 10))
                else:
                    screen.blit(sprite, (personaje.x, personaje.y))
            ganador = personaje.nombre.title()

        # Mostrar texto de ganador
        fuente_ganador = pygame.font.Font(
            r"./fonts/CsdegitadrawnRegularDemo-XGJqP.otf", 90
        )
        texto_ganador = fuente_ganador.render(
            f"Ganador: {ganador}", True, (255, 215, 0)
        )
        rect = texto_ganador.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(texto_ganador, rect)
        # Detener la actualización de barras y escudo cuando alguien pierde
        pygame.display.update()
        clock.tick(60)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        return
        rect = texto_ganador.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(texto_ganador, rect)
        return

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
    # Si algún personaje está derrotado, no aplicar daño
    if vida_actual == 0 or vida_actual2 == 0:
        return

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
    # No recargar si algún personaje está derrotado
    if vida_actual == 0 or vida_actual2 == 0:
        return
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
    # Si algún personaje está derrotado, no alternar ataques
    if not ataque_especial_en_progreso and vida_actual != 0 and vida_actual2 != 0:
        if keys[pygame.K_c]:
            # Espera un poco para escuchar el sonido antes de que termine el script
            ahora = pygame.time.get_ticks()
            if not ataque_alternar or ahora - ataque_tiempo_ultimo > ATAQUE_INTERVALO:
                if not ataque_alternar:
                    personaje.ataque_contador = 0
                ataque_alternar = True
                personaje.ataque_contador += 1
                if personaje.ataque_contador == 1:
                    # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
                    sonido = pygame.mixer.Sound("./assets/sound_effects/golpe_1.mp3")
                    # Reproduce el sonido
                    sonido.play()
                    estado_personaje = "primer_ataque"
                elif personaje.ataque_contador == 2:
                    # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
                    sonido = pygame.mixer.Sound("./assets/sound_effects/golpe_2.mp3")
                    # Reproduce el sonido
                    sonido.play()
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
                    # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
                    sonido = pygame.mixer.Sound("./assets/sound_effects/golpe_1.mp3")
                    # Reproduce el sonido
                    sonido.play()
                    estado_personaje2 = "primer_ataque"
                elif personaje2.ataque_contador == 2:
                    # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
                    sonido = pygame.mixer.Sound("./assets/sound_effects/golpe_2.mp3")
                    # Reproduce el sonido
                    sonido.play()
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
            global JUEGO_FINALIZADO
            for fondo in background_surfaces:
                screen.blit(fondo, (0, 0))
            for n in range(0, WIDTH, 100):
                screen.blit(suelo_sprite, (n, HEIGHT - 110))
            dibujar_barras()

            # Si algún personaje está derrotado, mostrar sprite derrotado y texto ganador
            if vida_actual == 0 or vida_actual2 == 0:
                # Todo Corregir cordenadas sprite derrotado
                if vida_actual == 0:
                    sprite = personaje.sprites.get("derrotado")
                    if sprite:
                        # region Cordenas
                        # ? Posicion derrotado personaje 1
                        if personaje.nombre == "daniel":
                            screen.blit(sprite, personaje.posicion_derrotado)
                        elif personaje.nombre == "jeremy":
                            tmp_posicion_derrotado = (
                                personaje.posicion_derrotado[0],
                                personaje.posicion_derrotado[1] - 35,
                            )
                            screen.blit(sprite, tmp_posicion_derrotado)
                        else:
                            # Andy
                            screen.blit(sprite, personaje.posicion_derrotado)

                    sprite2 = personaje2.sprites.get("posicion_normal")
                    if sprite2:
                        # Solo aplica ala imagen de jeremy subirle ala cordenada y +10
                        if personaje2.nombre == "jeremy":
                            screen.blit(sprite2, (personaje2.x, personaje2.y + 10))
                        else:
                            screen.blit(sprite2, (personaje2.x, personaje2.y))
                    ganador = personaje2.nombre.title()
                else:
                    sprite2 = personaje2.sprites.get("derrotado")
                    if sprite2:
                        if personaje2.nombre == "daniel":
                            screen.blit(sprite2, personaje2.posicion_derrotado)
                        elif personaje2.nombre == "jeremy":
                            tmp_posicion_derrotado2 = (
                                personaje2.posicion_derrotado[0],
                                personaje2.posicion_derrotado[1] - 35,
                            )
                            screen.blit(sprite2, tmp_posicion_derrotado2)
                        else:
                            # Andy
                            screen.blit(sprite2, personaje2.posicion_derrotado)

                        # screen.blit(sprite2, (personaje2.x, personaje2.y + 60))
                    sprite = personaje.sprites.get("posicion_normal")
                    if sprite:
                        # Solo aplica ala imagen de jeremy subirle ala cordenada y +10
                        if personaje.nombre == "jeremy":
                            screen.blit(sprite, (personaje.x, personaje.y + 10))
                        else:
                            screen.blit(sprite, (personaje.x, personaje.y + 10))
                    ganador = personaje.nombre.title()
                fuente_ganador = pygame.font.Font(
                    r"./fonts/CsdegitadrawnRegularDemo-XGJqP.otf", 90
                )
                texto_ganador = fuente_ganador.render(
                    f"Ganador: {ganador}", True, (255, 215, 0)
                )
                rect = texto_ganador.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(texto_ganador, rect)
                if not JUEGO_FINALIZADO:
                    # Carga el archivo de sonido (puede ser .wav, .ogg, etc.)
                    sonido = pygame.mixer.Sound("./assets/sound_effects/perdedor.mp3")
                    # Reproduce el sonido
                    sonido.play()
                    # Espera un poco para escuchar el sonido antes de que termine el script
                    pygame.time.delay(1500)
                    sonido.stop()
                JUEGO_FINALIZADO = True
                return

            global personaje_rotacion_angulo, personaje2_rotacion_angulo

            # * Cordenadas Personajes
            # Default
            cordenada1_y = personaje.y
            cordenada2_y = personaje2.y

            cordenada1_cuando_esta_agachado_y = personaje.y
            cordenada2_cuando_esta_agachado_y = personaje2.y

            cordenada1_cuando_esta_agachado_defendiendose_y = personaje.y + 5
            cordenada2_cuando_esta_agachado_defendiendose_y = personaje2.y + 5

            cordenada1_ataque_especial = personaje.y
            cordenada2_ataque_especial = personaje2.y

            cordenada1_cuando_se_esta_defendiendo_y = personaje.y
            cordenada2_cuando_se_esta_defendiendo_y = personaje2.y

            # Para daniel
            if personaje.nombre.lower() == "daniel":
                cordenada1_cuando_esta_agachado_y = personaje.y + 5
            if personaje2.nombre.lower() == "daniel":
                cordenada2_cuando_esta_agachado_y = personaje2.y + 5

            # Para Jeremy
            if personaje.nombre.lower() == "jeremy":
                cordenada1_cuando_esta_agachado_y = personaje.y + 15
                cordenada1_y = personaje.y + 10
                cordenada1_cuando_esta_agachado_defendiendose_y = personaje.y + 10
                cordenada1_cuando_se_esta_defendiendo_y = personaje.y + 15
                cordenada1_ataque_especial = personaje.y + 25

            if personaje2.nombre.lower() == "jeremy":
                cordenada2_cuando_esta_agachado_y = personaje2.y + 15
                cordenada2_y = personaje.y + 10
                cordenada2_cuando_esta_agachado_defendiendose_y = personaje2.y + 10
                cordenada2_cuando_se_esta_defendiendo_y = personaje2.y + 15
                cordenada2_ataque_especial = personaje.y + 25

            # Para andy
            if personaje.nombre.lower() == "andy":
                cordenada1_y = personaje.y + 5
                cordenada1_cuando_esta_agachado_y = personaje.y + 5
                cordenada1_cuando_esta_agachado_defendiendose_y = personaje.y + 15
                cordenada1_ataque_especial = personaje.y + 15

            if personaje2.nombre.lower() == "andy":
                cordenada2_y = personaje2.y + 5
                cordenada2_cuando_esta_agachado_y = personaje2.y + 5
                cordenada2_cuando_esta_agachado_defendiendose_y = personaje2.y + 15
                cordenada2_ataque_especial = personaje2.y + 15

            # Personaje 1
            sprite_key, pos = {
                "agachado": (
                    "agachado",
                    (personaje.x, cordenada1_cuando_esta_agachado_y),
                ),
                "primer_ataque": ("primer_ataque", (personaje.x, personaje.y)),
                "segundo_ataque": ("segundo_ataque", (personaje.x, personaje.y)),
                "defendiendose": (
                    "defendiendose",
                    (personaje.x, cordenada1_cuando_se_esta_defendiendo_y),
                ),
                "defendiendose_agachado": (
                    "defendiendose_agachado",
                    (personaje.x, cordenada1_cuando_esta_agachado_defendiendose_y),
                ),
                "saltando": ("saltando", (personaje.x, personaje.y - 60)),
                "ataque_especial": (
                    "ataque_especial",
                    (personaje.x, cordenada1_ataque_especial),
                ),
                # ? Aqui hay que editar [personaje.y]
                "normal": ("posicion_normal", (personaje.x, cordenada1_y)),
            }.get(estado_personaje, ("posicion_normal", (personaje.x, personaje.y)))
            sprite = personaje.sprites.get(sprite_key)
            # Todo implemnentacion de detener el sonido cuando ya impacta
            if sprite:
                if (
                    estado_personaje == "ataque_especial"
                    and personaje.nombre == "daniel"
                    and ataque_especial_en_progreso
                    and ataque_especial_personaje == personaje
                ):
                    personaje_rotacion_angulo = (personaje_rotacion_angulo + 45) % 360
                    rotated, rotated_rect = rotar_sprite(
                        sprite, personaje_rotacion_angulo
                    )
                    rotated_rect.topleft = pos
                    screen.blit(rotated, rotated_rect)
                else:
                    personaje_rotacion_angulo = 0
                    screen.blit(sprite, pos)

            # Personaje 2
            sprite_key2, pos2 = {
                "agachado": (
                    "agachado",
                    (personaje2.x, cordenada2_cuando_esta_agachado_y),
                ),
                "primer_ataque": ("primer_ataque", (personaje2.x, personaje2.y)),
                "segundo_ataque": ("segundo_ataque", (personaje2.x, personaje2.y)),
                "defendiendose": (
                    "defendiendose",
                    (personaje2.x, cordenada2_cuando_se_esta_defendiendo_y),
                ),
                "defendiendose_agachado": (
                    "defendiendose_agachado",
                    (personaje2.x, cordenada2_cuando_esta_agachado_defendiendose_y),
                ),
                "saltando": ("saltando", (personaje2.x, personaje2.y - 60)),
                "ataque_especial": (
                    "ataque_especial",
                    (personaje2.x, cordenada2_ataque_especial),
                ),
                # ? Aqui hay que editar [personaje2.y]
                "normal": ("posicion_normal", (personaje2.x, cordenada2_y)),
            }.get(estado_personaje2, ("posicion_normal", (personaje2.x, personaje2.y)))
            sprite2 = personaje2.sprites.get(sprite_key2)
            if sprite2:
                if (
                    estado_personaje2 == "ataque_especial"
                    and personaje2.nombre == "daniel"
                    and ataque_especial_en_progreso
                    and ataque_especial_personaje == personaje2
                ):
                    personaje2_rotacion_angulo = (personaje2_rotacion_angulo + 45) % 360
                    rotated2, rotated_rect2 = rotar_sprite(
                        sprite2, personaje2_rotacion_angulo
                    )
                    rotated_rect2.topleft = pos2
                    screen.blit(rotated2, rotated_rect2)
                else:
                    personaje2_rotacion_angulo = 0
                    screen.blit(sprite2, pos2)

        dibujar = dibujar
