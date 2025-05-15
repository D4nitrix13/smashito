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
        self.__x: int = (WIDTH // 2) - 600
        self.__y: int = HEIGHT - 510
        self.__position_initial: Tuple[int, int] = (self.__x, self.__y)
        self.posicion: Tuple[int, int] = (self.__x, self.__y)
        self.ataque_contador: int = 0  # Contador de ataques
        self.pie_actual: int = (
            0  # Pie actual (0 para pie izquierdo, 1 para pie derecho)
        )
        self.velocidad: int = 10  # Velocidad de movimiento
        self.posicion_cuando_esta_agachado: Tuple[int, int] = (self.__x, self.__y + 140)
        self.posicion_cuando_esta_defendiendose: Tuple[int, int] = (
            self.__x,
            self.__y + 120,
        )
        self.posicion_cuando_esta_caminando_pie_derecho: Tuple[int, int] = (
            self.__x,
            self.__y + 95,
        )

        # Carga la imagen original (spritesheet)
        imagen_original = pygame.image.load(
            rf"./personajes/{self.nombre}/spritesheet_ataque.png"
        )
        ancho_objetivo = 200
        alto_objetivo = 300

        # Define manualmente las coordenadas y tamaños de cada sprite (x, y, ancho, alto)
        # El primer sprite define el área principal (posición normal)
        coordenadas_sprites = [
            (0, 0, 460, 915),  # Sprite 1: posición normal (referencia)
            (
                460,
                0,
                540,
                915,
            ),  # Sprite 2: ataque inicial (a la derecha del primero, mismo alto)
            (
                690,
                0,
                230,
                915,
            ),  # Sprite 3: ataque final (a la derecha del segundo, mismo alto)
        ]

        sprites = []
        for x, y, w, h in coordenadas_sprites:
            rect = pygame.Rect(x, y, w, h)
            sprite = imagen_original.subsurface(rect).copy()
            sprite = pygame.transform.scale(sprite, (ancho_objetivo, alto_objetivo))
            sprites.append(sprite)

        self.movimientos: Dict[str, pygame.Surface] = {
            "posicion_normal": sprites[0],
            "ataque_inicial": sprites[1],
            "ataque_final": sprites[2],
        }

    # @property
    # def position_initial(self: "Personaje") -> Tuple[int, int]:
    #     return self.__position_initial

    # @position_initial.setter
    # def position_initial(self: "Personaje", value: Tuple[int, int]) -> None:
    #     self.__position_initial = value
    #     self.posicion = (self.__x, self.__y)

    @property
    def y(self: "Personaje") -> int:
        return self.__y

    @y.setter
    def y(self: "Personaje", value: int) -> None:
        self.__y = value
        self.posicion = (self.__x, self.__y)
        self.posicion_cuando_esta_agachado = (self.__x, self.__y + 140)
        self.posicion_cuando_esta_defendiendose = (self.__x, self.__y + 120)
        self.posicion_cuando_esta_caminando_pie_derecho = (self.__x, self.__y + 95)

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
        self.posicion_cuando_esta_agachado = (self.__x, self.__y + 140)
        self.posicion_cuando_esta_defendiendose = (self.__x, self.__y + 120)
        self.posicion_cuando_esta_caminando_pie_derecho = (self.__x, self.__y + 95)


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


personaje_one: Personaje = Personaje(
    nombre="Daniel",
    vida=100,
    ataque=10,
    defensa=5,
)


# Agregar una variable de estado para controlar la animación
estado_personaje: str = "normal"  # Puede ser "normal", "agachado", etc.

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                estado_personaje = "agachado"

            if event.key == pygame.K_c:
                personaje_one.ataque_contador += 1
                match personaje_one.ataque_contador:
                    case 1:
                        estado_personaje = "ataque_inicial"
                    case 2:
                        estado_personaje = "ataque_final"
                        personaje_one.ataque_contador = 0

            if event.key == pygame.K_w:
                estado_personaje = "defendiendose"

            if event.key == pygame.K_LEFT:
                match personaje_one.pie_actual:
                    case 1:
                        estado_personaje = "caminando_pie_derecho"
                    case 2:
                        estado_personaje = "caminando_pie_izquierdo"
                personaje_one.x -= personaje_one.velocidad

            if event.key == pygame.K_RIGHT:
                match personaje_one.pie_actual:
                    case 1:
                        estado_personaje = "caminando_pie_izquierdo"
                    case 2:
                        estado_personaje = "caminando_pie_derecho"
                personaje_one.x += personaje_one.velocidad

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                estado_personaje = "normal"
            if event.key == pygame.K_w:  # Manejar cuando se suelta la tecla W
                estado_personaje = "normal"

            if event.key == pygame.K_RIGHT:
                estado_personaje = "normal"

            if event.key == pygame.K_LEFT:
                estado_personaje = "normal"

            if event.key == pygame.K_c:
                estado_personaje = "normal"

    # Dibujar los fondos y otros elementos
    for i in background_surfaces:
        screen.blit(source=i, dest=(0, 0))  # Dibujar los fondos
    n = 0
    while n < WIDTH:
        screen.blit(suelo_sprite, (n, HEIGHT - 110))  # Dibujar el suelo
        n += 100

    match estado_personaje:
        case "agachado":
            screen.blit(
                source=personaje_one.movimientos.get("agachado"),  # type: ignore
                dest=personaje_one.posicion_cuando_esta_agachado,
            )

        case "ataque_inicial":
            screen.blit(
                source=personaje_one.movimientos.get("ataque_inicial"),  # type: ignore
                dest=personaje_one.posicion,
            )

        case "ataque_final":
            screen.blit(
                source=personaje_one.movimientos.get("ataque_final"),  # type: ignore
                dest=personaje_one.posicion,
            )

        case "defendiendose":
            screen.blit(
                source=personaje_one.movimientos.get("defendiendose"),  # type: ignore
                dest=personaje_one.posicion_cuando_esta_defendiendose,
            )

        # case "caminando_pie_derecho":
        #     screen.blit(
        #         source=personaje_one.movimientos.get("caminando_pie_derecho"),  # type: ignore
        #         dest=personaje_one.posicion_cuando_esta_caminando_pie_derecho,
        #     )

        # case "caminando_pie_izquierdo":
        #     screen.blit(
        #         source=personaje_one.movimientos.get("caminando_pie_izquierdo"),  # type: ignore
        #         dest=personaje_one.posicion,
        #     )

        case "normal":
            screen.blit(
                source=personaje_one.movimientos.get("ataque_inicial"),  # type: ignore
                dest=personaje_one.posicion,
            )

    pygame.display.update()
    clock.tick(60)
