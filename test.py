
# dest=(daniel.posicion[0] + 200, daniel.posicion[1] - 140),

# Extraer un sprite específico del sprite sheet
# sprite_sheet_agachado: pygame.Surface = pygame.image.load(
#     r"./personajes/Daniel/agachado.png"
# )

# # Definir las coordenadas del sprite (x, y, ancho, alto)
# agachado: pygame.Surface = sprite_sheet_agachado.subsurface(
#     pygame.Rect(60, 90, 950, 1315)
# ).copy()

# # Escalar el sprite
# agachado = pygame.transform.scale(
#     agachado,
#     (
#         int(agachado.get_width() * 0.2),
#         int(agachado.get_height() * 0.2),
#     ),
# )

# pygame.image.save(agachado, r"./personajes/Daniel/agachado_scaled.png")


# # Coordenadas de los sprites (x, y, ancho, alto)
# coordenadas_sprites_yo: List[Tuple[int, int, int, int]] = [
#     (0, 30, 265, 505),
#     (60, 0, 50, 60),
#     (120, 0, 50, 60),
#     (0, 70, 50, 60),
#     (60, 70, 50, 60),
#     (120, 70, 50, 60),
# ]

# # Extraer los sprites
# sprites_yo: list[pygame.Surface] = [
#     pygame.transform.scale(sprite, (int(sprite.get_width() * 0.5), int(sprite.get_height() * 0.5)))
#     for sprite in extraer_sprites_varios_tamanos(sprite_sheet_yo, coordenadas_sprites_yo)
# ]


#  pygame.image.save(
#                 daniel.movimientos.get(
#                     "posicion_normal",  # Cambiar a "posicion_normal" para la posición estándar
#                 ),  # type: ignore
#                 "./1.png",
#             )  # Guardar la imagen actual

#             pygame.image.save(
#                 daniel.movimientos.get(
#                     "ataque_inicial",  # Cambiar a "ataque_inicial" para la posición de ataque
#                 ),  # type: ignore
#                 "./2.png",
#             )  # Guardar la imagen actual

#             pygame.image.save(
#                 daniel.movimientos.get(
#                     "ataque_final",  # Cambiar a "ataque_final" para la posición de ataque
#                 ),  # type: ignore
#                 "./3.png",
#             )

    # screen.blit(
    #     source = text_surface,
    #     dest = (100, 100)
    # )


 "ataque_inicial": pygame.transform.scale(
                pygame.image.load(
                    rf"./personajes/{self.nombre}/ataque_inicial.png"
                ).convert_alpha(),
                (
                    int(
                        pygame.image.load(
                            rf"./personajes/{self.nombre}/ataque_inicial.png"
                        )
                        .convert_alpha()
                        .get_width()
                        * 1.5
                    ),
                    int(
                        pygame.image.load(
                            rf"./personajes/{self.nombre}/ataque_inicial.png"
                        )
                        .convert_alpha()
                        .get_height()
                        * 1.5
                    ),
                ),
            ),
            "ataque_final": pygame.transform.scale(
                pygame.image.load(
                    rf"./personajes/{self.nombre}/ataque_final.png"
                ).convert_alpha(),
                (
                    int(
                        pygame.image.load(
                            rf"./personajes/{self.nombre}/ataque_final.png"
                        )
                        .convert_alpha()
                        .get_width()
                        * 1.5
                    ),
                    int(
                        pygame.image.load(
                            rf"./personajes/{self.nombre}/ataque_final.png"
                        )
                        .convert_alpha()
                        .get_height()
                        * 1.5
                    ),
                ),
            ),
            "agachado": pygame.image.load(
                rf"./personajes/{self.nombre}/agachado.png"
            ).convert_alpha(),
            "defendiendose": pygame.transform.scale(
                pygame.image.load(
                    rf"./personajes/{self.nombre}/defendiendose.png"
                ).convert_alpha(),
                (
                    int(
                        pygame.image.load(
                            rf"./personajes/{self.nombre}/defendiendose.png"
                        )
                        .convert_alpha()
                        .get_width()
                        * 0.2
                    ),
                    int(
                        pygame.image.load(
                            rf"./personajes/{self.nombre}/defendiendose.png"
                        )
                        .convert_alpha()
                        .get_height()
                        * 0.2
                    ),
                ),
            ),
           
           