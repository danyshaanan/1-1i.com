from PIL import Image
import random, math

rnd = random.Random()
size = 200
points = 10000


for gon in range(3,7):
    vertices = []
    for a in [2*math.pi * i/gon for i in range(gon)]:
        x = size/2 * (1 + math.cos(a - math.pi/2))
        y = size/2 * (1 + math.sin(a - math.pi/2))
        vertices += [(x, y)]

    for iterations in [0,1,2,3,4,6,9]:
        rnd.seed(0)
        image = Image.new("L",(size,size),255)
        pixel = image.load()

        for p in range(points/3*gon):
            x = rnd.randrange(size)
            y = rnd.randrange(size)

            if (size/2-x)**2+(size/2-y)**2<(size/2)**2:
                for _ in range (iterations):
                    vertex = rnd.choice(vertices)
                    p = (12-gon)/18.
                    q = 1 - p
                    x = x*p + vertex[0]*q
                    y = y*p + vertex[1]*q
                pixel[x,y] = 0

        filename = 'sierpinski_' + str(gon) + '_' + str(iterations) + '.png'
        image.save(filename)
        print filename


