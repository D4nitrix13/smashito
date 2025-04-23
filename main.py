# https://youtu.be/AY9MnQ4x3zk?t=2685
# https://arexxuru.itch.io/pixel-floor-texture-pack-ground-tile

from typing import Any, List, Tuple, Union

import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(r"./assets/music/ManifiestoUrbano.org.mp3")
pygame.mixer.music.play(loops=-1, start=0.0)

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



def extraer_sprites(imagen: pygame.Surface, columnas: int, ancho: int, alto: int) -> list[pygame.Surface]:
    sprites: list[pygame.Surface] = []
    for i in range(columnas):
        rect = pygame.Rect(i * ancho, 0, ancho, alto)
        sprite = imagen.subsurface(rect).copy()
        sprites.append(sprite)
    return sprites

# Carga la imagen animada
sprite_sheet: pygame.Surface = pygame.image.load("./assets/decorations/shop_anim.png").convert_alpha()

# Extraer los 6 sprites (cada uno de 118x128)
sprites_shop: list[pygame.Surface] = extraer_sprites(sprite_sheet, columnas=6, ancho=118, alto=128)

sprites_shop = [pygame.transform.scale(sprite, (500, 500)) for sprite in sprites_shop]

# Ahora puedes usarlos en tu juego como:


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Dibujar la tienda en una posición específica
    #                              x          y
    # Animar la tienda iterando sobre los sprites
    for sprite in sprites_shop:
        for i in background_surfaces:
            screen.blit(source=i, dest=(0, 0))  # Redibujar los fondos
        n = 0
        while n < WIDTH:
            screen.blit(
                suelo_sprite, (n, HEIGHT - 110)
            )  # Redibujar el suelo
            n += 100
        screen.blit(sprite, (WIDTH // 2 - (-440), HEIGHT - 610))  # Dibujar la tienda animada
        pygame.display.update()
        pygame.time.delay(100)  # Controla la velocidad de la animación


    # screen.blit(
    #     source = text_surface,
    #     dest = (100, 100)
    # )

    clock.tick(60)
