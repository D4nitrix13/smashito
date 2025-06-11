# Recurso

Extraer los primeros 3 segundos:

```bash
# Ejemplo 1
ffmpeg -i input.mp3 -t 3 -c copy output.mp3

# Ejemplo 2
ffmpeg -i input.mp3 -t 1.5 -c copy output.mp3
```

También puedes recortar desde un punto intermedio, por ejemplo de 2 s a 5 s:

```bash
# Ejemplo 1
ffmpeg -ss 2 -i input.mp3 -t 3 -c copy output.mp3

# Ejemplo 2
ffmpeg -ss 7 -i input.mp3 -t 9 -c copy output.mp3
```
