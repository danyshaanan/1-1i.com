from PIL import Image
import random, math

w, h = 200, 200

for gon in range(3, 7):
    vertices = []
    for a in [math.tau * i / gon for i in range(gon)]:
        vertices += [(w / 2 * (1 + math.cos(a - math.tau / 4)), h / 2 * (1 + math.sin(a - math.tau / 4)))]

    for iterations in [0, 1, 2, 3, 4, 6, 9]:
        rnd = random.Random(0)
        rr, choice = rnd.randrange, rnd.choice
        image = Image.new('1', (w, h), 1)
        pixel = image.load()

        for _ in range(3_000 * gon):
            x, y = rr(image.width), rr(image.height)

            if 4 * math.hypot(image.width / 2 - x, image.height / 2 - y) < image.width + image.height:
                for _ in range (iterations):
                    p = (12 - gon) / 18
                    v0, v1 = choice(vertices)
                    x = x * p + v0 * (1 - p)
                    y = y * p + v1 * (1 - p)
                pixel[x, y] = 0

        image.save(f'output/sierpinski_{gon}_{iterations}.png')


