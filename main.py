# https://youtu.be/AY9MnQ4x3zk?t=2685
# https://arexxuru.itch.io/pixel-floor-texture-pack-ground-tile

from typing import Any, Dict, List, Tuple, Union

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


def get_image(
    imagen: pygame.Surface,
    width: int,
    height: int,
    cordenada_x_img: int,
    cordenada_y_img: int,
) -> pygame.Surface:
    img: pygame.Surface = pygame.Surface(size=(width, height)).convert_alpha()

    img.blit(
        source=imagen,
        dest=(0, 0),
        # Explicacion sobre code: area( value1, value2, value3, value4 )
        # value1: Coordenada X en la imagen de origen
        # value2: Coordenada Y en la imagen de origen
        # value2: Ancho del sprite que se va a extraer
        # value3: Alto del sprite que se va a extraer
        area=(cordenada_x_img, cordenada_y_img, width, height),
    )
    return img


imagen_sprites: pygame.Surface = pygame.transform.scale(
    surface=pygame.image.load(r"./assets/oak_woods_tileset.png"), size=WINDOW_SIZE
)

# sprites: Dict[str, pygame.Surface] = {
#     "suelo_superior": get_image(
#         imagen=imagen_sprites,
#         width=190,
#         height=45,
#         cordenada_x_img=330,
#         cordenada_y_img=465,
#     ),
# }

sprites: Dict[str, pygame.Surface] = {
    "suelo_superior": get_image(
        imagen=imagen_sprites,
        width=190,
        height=45,
        cordenada_x_img=590,
        cordenada_y_img=465,
    ),
}

suelo_sprite: pygame.Surface = pygame.image.load(r"./assets/ground.png")

suelo_sprite = pygame.transform.scale(suelo_sprite, (110, 50))

# Cargar la imagen de la tienda
shop_sprite: pygame.Surface = pygame.image.load(r"./assets/decorations/shop.png")

# Escalar la imagen de la tienda si es necesario
shop_sprite = pygame.transform.scale(shop_sprite, (200, 200))  # Ajusta el tamaño según sea necesario

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for i in background_surfaces:
        screen.blit(source=i, dest=(0, 0))

    # Dibujar el suelo en la parte inferior de la pantalla
    n = 0
    while n < WIDTH:
        screen.blit(suelo_sprite, (n, HEIGHT - 110))  # Ajusta la posición Y según sea necesario
        n += 100  # Avanza horizontalmente según el ancho del sprite
    
    # Dibujar la tienda en una posición específica    
    #                                x                   y
    screen.blit(shop_sprite, (WIDTH // 2 - 300, HEIGHT - 310))  # Centra la tienda horizontalmente y ajusta la posición vertical

    # Posicionamos el sprite del suelo en la coordenada Y = 670.
    # Comenzamos en X = 1170 y restamos 180 en cada iteración para moverlo hacia la izquierda.
    # n: int = 1170
    # for i in range(0, 8, 1):
    #     screen.blit(source=sprites["suelo_superior"], dest=(n, 670))
    #     n -= 180

    # screen.blit(
    #     source = text_surface,
    #     dest = (100, 100)
    # )

    pygame.display.update()

    clock.tick(60)
