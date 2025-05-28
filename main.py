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

        rutas_imagenes = {
            "posicion_normal": "./personajes/daniel/default.png",
            "primer_ataque": "./personajes/daniel/primer_ataque.png",
            "segundo_ataque": "./personajes/daniel/segundo_ataque.png",
            "agachado": "./personajes/daniel/5_agachado_defendiendose.png",
            # "segundo_ataque": "./personajes/daniel/2_segundo_ataque.png",
            # "agachado_primer_ataque": "./personajes/daniel/3_agachado_primer_ataque.png",
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


# Variables para las barras
vida_actual = 100
escudo_actual = 100
barra_extra_actual = 0
BARRA_EXTRA_MAX = 100

# Tiempos para la barra extra
tiempo_ultimo_incremento = pygame.time.get_ticks()
INCREMENTO_BARRA_EXTRA = 20
INTERVALO_BARRA_EXTRA = 10000  # 10 segundos en milisegundos


def dibujar_barras():
    # Posiciones y tamaños
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
    screen.blit(txt_vida, (x + 10, y + 2))

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
    screen.blit(txt_escudo, (x + 10, y + 2))

    # Barra extra (verde)
    y += alto + espacio
    pygame.draw.rect(screen, (60, 60, 60), (x, y, ancho, alto), border_radius=8)
    pygame.draw.rect(
        screen,
        (40, 220, 80),
        (x, y, ancho * (barra_extra_actual / BARRA_EXTRA_MAX), alto),
        border_radius=8,
    )
    txt_extra = font_barra.render(f"Extra: {barra_extra_actual}", True, (255, 255, 255))
    screen.blit(txt_extra, (x + 10, y + 2))


def actualizar_barra_extra():
    global barra_extra_actual, tiempo_ultimo_incremento
    ahora = pygame.time.get_ticks()
    if (
        barra_extra_actual < BARRA_EXTRA_MAX
        and ahora - tiempo_ultimo_incremento >= INTERVALO_BARRA_EXTRA
    ):
        barra_extra_actual = min(
            barra_extra_actual + INCREMENTO_BARRA_EXTRA, BARRA_EXTRA_MAX
        )
        tiempo_ultimo_incremento = ahora


# Agregar una variable de estado para controlar la animación
estado_personaje: str = "normal"  # Puede ser "normal", "agachado", etc.


def manejar_eventos():
    global estado_personaje
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                personaje.ataque_contador += 1
                if personaje.ataque_contador == 1:
                    estado_personaje = "primer_ataque"

                elif personaje.ataque_contador == 2:
                    estado_personaje = "segundo_ataque"
                    personaje.ataque_contador = 0

            elif event.key == pygame.K_w:
                estado_personaje = "defendiendose"

    # Movimiento continuo con teclas presionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        estado_personaje = "agachado"
    elif estado_personaje == "agachado":
        estado_personaje = "normal"

    if keys[pygame.K_RIGHT]:
        personaje.x += personaje.velocidad
    if keys[pygame.K_LEFT]:
        personaje.x -= personaje.velocidad


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
        "normal": ("posicion_normal", (personaje.x, personaje.y)),
    }

    sprite_key, pos = sprite_map.get(
        estado_personaje, ("posicion_normal", (personaje.x, personaje.y))
    )
    sprite = personaje.sprites.get(sprite_key)
    if sprite:
        screen.blit(sprite, pos)


# Alternar ataques mientras la tecla 'c' esté presionada
ataque_alternar = False
ataque_tiempo_ultimo = 0
ATAQUE_INTERVALO = 200  # milisegundos

while True:
    manejar_eventos()
    actualizar_barra_extra()

    # Alternar ataques si la tecla 'c' está presionada
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        ahora = pygame.time.get_ticks()
        if not ataque_alternar or ahora - ataque_tiempo_ultimo > ATAQUE_INTERVALO:
            ataque_alternar = True
            personaje.ataque_contador += 1
            if personaje.ataque_contador == 1:
                estado_personaje = "primer_ataque"
            elif personaje.ataque_contador == 2:
                estado_personaje = "segundo_ataque"
                personaje.ataque_contador = 0
            ataque_tiempo_ultimo = ahora
    else:
        ataque_alternar = False
        if estado_personaje in ("primer_ataque", "segundo_ataque"):
            estado_personaje = "normal"

    dibujar()
    pygame.display.update()
    clock.tick(60)
