# https://youtu.be/AY9MnQ4x3zk?t=2685
# https://arexxuru.itch.io/pixel-floor-texture-pack-ground-tile

from typing import Any, Dict, List, Tuple, Union

import pygame


class Personaje:
    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        self.nombre: str = nombre
        self.vida: int = vida
        self.ataque: int = ataque
        # La posición inicial del personaje el primer index es la posición x y el segundo índice es la posición y
        self.defensa: int = defensa
        self.posicion: Tuple[int, int] = ((WIDTH // 2) - 600, HEIGHT - 370)
        self.ataque_contador: int = 0  # Contador de ataques
        self.velocidad: int = 10  # Velocidad de movimiento

        # sprite_sheet_yo: pygame.Surface = pygame.image.load(
        #     "./spritesheet.png"
        # ).convert_alpha()

        # # Coordenadas de los sprites (x, y, ancho, alto)
        # coordenadas_sprites_yo: Dict[str, Tuple[int, int, int, int]] = {
        #     "posicion_normal": (55, 30, 365, 980),  # posicion normal
        #     "ataque_inicial": (475, 30, 525, 990),  # ataque inicial
        #     "ataque_final": (950, 30, 560, 900),  # ataque final
        # }

        # # Extraer los sprites y mapearlos a un diccionario
        # sprites_yo: Dict[str, pygame.Surface] = {
        #     nombre: pygame.transform.scale(
        #         sprite, (int(sprite.get_width() * 0.3), int(sprite.get_height() * 0.3))
        #     )
        #     for nombre, coordenadas in coordenadas_sprites_yo.items()
        #     for sprite in extraer_sprites_varios_tamanos(sprite_sheet_yo, [coordenadas])
        # }

        # self.movimientos: Dict[str, pygame.Surface] = {
        #     "posicion_normal": sprites_yo["posicion_normal"],
        #     "ataque_inicial": sprites_yo["ataque_inicial"],
        #     "ataque_final": sprites_yo["ataque_final"],
        # }

        self.movimientos: Dict[str, pygame.Surface] = {
            "posicion_normal": pygame.image.load(fr"./personajes/{self.nombre}/posicion_normal.png").convert_alpha(),
            "ataque_inicial": pygame.image.load(fr"./personajes/{self.nombre}/ataque_inicial.png").convert_alpha(),
            "ataque_final": pygame.image.load(fr"./personajes/{self.nombre}/ataque_final.png").convert_alpha()
        }



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


daniel: Personaje = Personaje(
    nombre="Daniel",
    vida=100,
    ataque=10,
    defensa=5,
)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for sprite in sprites_shop:
        for i in background_surfaces:
            screen.blit(source=i, dest=(0, 0))  # Dibujar los fondos
        n = 0
        while n < WIDTH:
            screen.blit(suelo_sprite, (n, HEIGHT - 110))  # Dibujar el suelo
            n += 100
        screen.blit(
            sprite, (WIDTH // 2 - (-440), HEIGHT - 610)
        )  # Dibujar la tienda animada

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                daniel.ataque_contador += 1

                match daniel.ataque_contador:
                    case 1:
                        screen.blit(
                            source=daniel.movimientos.get(
                                "ataque_inicial",
                            ),  # type: ignore
                            dest=daniel.posicion,
                        )
                        pygame.display.update()
                        break


                    case 2:
                        screen.blit(
                            source=daniel.movimientos.get(
                                "ataque_final",
                            ),  # type: ignore
                            dest=daniel.posicion,
                        )
                        # Reiniciar el contador después del ataque final
                        daniel.ataque_contador = 0
                        pygame.display.update()
                        break

        else:
            screen.blit(
                source=daniel.movimientos.get(
                    "posicion_normal",  # Cambiar a "posicion_normal" para la posición estándar
                ),  # type: ignore
                dest=daniel.posicion,
            )

        pygame.display.update()
        pygame.time.delay(100)  # Controla la velocidad de la animación

    clock.tick(60)
