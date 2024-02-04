import pygame as pg
import random

# Konstanter
WIDTH = 800  # Bredden til vinduet
HEIGHT = 600 # Høyden til vinduet

# Størrelsen til vinduet
SIZE = (WIDTH, HEIGHT)

# Frames Per Second (bilder per sekund)
FPS = 120

# Farger (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (100,40,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 180, 0)
LIGHTBLUE = (100, 100, 255)
GREY = (160, 160, 160)
LIGHTRED = (255, 100, 100)

# Karakterne sin bredde og høyde
w = 30


# Lager felles spillobjekt for alle karakterene
class SpillObject():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
            
    # Tegner spillobjektet, blir felles for alle
    def draw(self):
        pg.draw.rect(surface, self.color, [self.x, self.y, w, w])
    

# Lager en klasse for gjeteren
class Character(SpillObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)        
        self.vx = 0
        self.vy = 0
        
        self.points = 0 
        self.carry = False
        self.stop = False 
    
    def draw(self):
        super().draw()
    
    # Oppdaterer klassen
    def update(self):
        # Endrer posisjonen til rektangelet
        self.x += self.vx
        self.y += self.vy
        
        # Sjekker kollisjon med høyre side
        if self.x + w >= WIDTH:
            # Endrer retning på hastigheten
            self.vx *= -1
            self.x = WIDTH - w
        
        # Sjekker kollisjon med venstre side
        elif self.x <= 0:
            self.vx *= -1
            self.x = 0
        
        # Sjekker kollisjon med bunn
        elif self.y >= HEIGHT - w:
            self.vy *= -1
            self.y = HEIGHT - w 
        
        # Sjekker kollisjon med topp
        elif self.y <= 0:
            self.vy *= -1
            self.y = 0
        
    # Metode som håndterer tastaturinput
    def move(self):
        # sjekker om gjeteren bærer en sau
        # velger å lage en if-løkke istedenfor en ny metode
        if self.carry == True:
            self.speed = 1
        else:
            self.speed = 3
        # Nullstiller farten
        self.vy = 0
        self.vx = 0
        
        # Henter knappene fra tastaturet som trykkes på
        keys = pg.key.get_pressed()
        
        # Sjekker om pilen opp er trykket 
        if keys[pg.K_UP]:
            self.vy = -self.speed
            
        # Sjekker om pilen ned er trykket 
        if keys[pg.K_DOWN]:
            self.vy = self.speed
        
        # Sjekker om pilen mot venstre er trykket
        if keys[pg.K_LEFT]:
            self.vx = -self.speed
            
        # Sjekker om pilen mot høyre er trykket 
        if keys[pg.K_RIGHT]:
            self.vx = self.speed
    
    # Metode som sjekker om gjeteren kræsjer i hindrene
    def checkCollision(self):
        for ob in obsts:
            if pg.Rect(self.x, self.y, w, w).colliderect(pg.Rect(ob.x, ob.y, w, w)):
                # Hvis gjeteren kolliderer med et hindringsobjekt, nullstill farten hans
                self.x -= self.vx
                self.y -= self.vy

    
    # Metode for å sjekke om gjeteren treffer en sau
    def carryingSheep(self):
        # Sjekker om jeg bærer sauen
        for s in sheeps:
            if pg.Rect(self.x, self.y, w, w).colliderect(pg.Rect(s.x, s.y, w, w)):
                # Hvis gjeteren kolliderer med et saueobjekt, blir carry = True
                self.carry = True
                # Ser om gjeteren plukker opp flere sauer
                for sheep in sheeps:
                    if pg.Rect(shepherd.x, shepherd.y, w, w).colliderect(pg.Rect(sheep.x, sheep.y, w, w)) and sheep != s:
                        # ser om spillet skal stoppe
                        self.stop = True
            elif shepherd.x <= 160:
                self.carry = False

    
    # Funksjon som viser antall poeng
    def displayPoints(self):
        # Henter font til poeng
        font = pg.font.SysFont('Arial', 26)
        
        text_img = font.render(f"Antall poeng: {self.points}", True, WHITE)
        surface.blit(text_img, (10, 10))
        
shepherd = Character(60, HEIGHT/2, RED)

# Lager liste for sauene og hindrene
sheeps = []
obsts = []
ghosts = []

# Lager en klasse for sauene
class Sheep(SpillObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

        self.carry = False

        # Sjekker om saueobjektene er oppå hverandre
        overlapping = False
        for sh in sheeps:
            if pg.Rect(sh.x, sh.y, w, w).colliderect(pg.Rect(x, y, w, w)):
                overlapping = True
                break
        if overlapping != True and len(sheeps) < 3:
            sheeps.append(self)

    def draw(self):
        super().draw()
    
    # metode for å få sauobjektet til å følge gjeteren 
    def carried(self):
        for sheep in sheeps:
            if pg.Rect(sheep.x, sheep.y, w, w).colliderect(pg.Rect(shepherd.x, shepherd.y, w, w)):
                # Hvis gjeteren kolliderer med et saueobjekt, blir carry = True
                self.carry = True
                sheep.x = shepherd.x + 10
                sheep.y = shepherd.y
    
    def removeSheep(self):
        sheeps.remove(s)
        
        
# Legger til saueobjektene i listen og sjekker om de er oppå hverandre
for i in range(3):
    x = random.randint(WIDTH-160, WIDTH - w)
    y = random.randint(0, HEIGHT-w)
    # Sjekker om det nye saueobjektet overlapper med de eksisterende saueobjektene 
    overlapping = False
    for sh in sheeps:
        if pg.Rect(sh.x, sh.y, w, w).colliderect(pg.Rect(x, y, w, w)):
            overlapping = True
            break
    if overlapping != True:
        # Generer et nytt objekt
        sheep = Sheep(x, y, WHITE)

# Lager en klasse for hindrene 
class Object(SpillObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        
        # Sjekker om hindrene er oppå hverandre
        overlapping = False
        for ob in obsts:
            if pg.Rect(ob.x, ob.y, w, w).colliderect(pg.Rect(x, y, w, w)):
                overlapping = True
                break
        if overlapping != True and len(obsts) < 3:
            obsts.append(self)
        
    def draw(self):
        pg.draw.rect(surface, self.color, [self.x, self.y, w, w])

# Legger til saueobjektene i listen og sjekker om de er oppå hverandre
for i in range(3):
    x = random.randint(160, WIDTH - (160+w))
    y = random.randint(0, HEIGHT-w)
    # Sjekker om det nye hindrene overlapper med de eksisterende hindrene 
    overlapping = False
    for ob in obsts:
        if pg.Rect(ob.x, ob.y, w, w).colliderect(pg.Rect(x, y, w, w)):
            overlapping = True
            break
    if overlapping != True:
        # Generer et nytt objekt
        obst = Object(x, y, BROWN)

  
# Lager en klasse for spøkelsene   
class Ghost(SpillObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.vx = 2
        self.vy = 2
        ghosts.append(self)
    
    def draw(self):
        super().draw()
    
    # Beveger spøkelsene
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
    # Sjekker kollisjon med topp
        if self.y <= 0:
            self.vy *= -1
            self.y = 0
            
        # Sjekker kollisjon med bunn
        if self.y + w >= HEIGHT:
            self.vy *= -1
            self.y = HEIGHT - w

        # sjekker kollisjon med venstre vegg
        if self.x <= 160:
            self.vx *= -1
            self.x = 160 
          
        # sjekker kollisjon med høyre vegg
        if self.x + w >= WIDTH-160:
            self.vx *=-1
            self.x = WIDTH - (160 + w)


ghost = Ghost(random.randint(160, WIDTH-(160+w)), random.randint(0, HEIGHT-w), GREEN)


# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()


# Variabel som styrer om spillet skal kjøres
run = True

# Spill-løkken
while run:
    # Sørger for at løkken kjører i korrekt hastighet
    clock.tick(FPS)
    
    surface.fill(LIGHTBLUE)
    pg.draw.rect(surface, DARKGREEN, [0, 0, 160, HEIGHT])
    pg.draw.rect(surface, DARKGREEN, [WIDTH - 160, 0, 160, HEIGHT])
    
    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes
    
    
    for s in sheeps:
        s.draw()
        s.carried()
        
        # Ser om sauen er fraktet over til den andre siden
        if s.x <= 160:
            # Fjerner sauen
            s.removeSheep()
            
            # Generer et nytt hindringsobjekt
            o_x = random.randint(160, WIDTH-(160+w))
            o_y = random.randint(0, HEIGHT-w)
            block = Object(o_x, o_y, BROWN)
            
            # Lager et nytt saueobjekt
            s_x = random.randint(WIDTH-160, WIDTH - w)
            s_y = random.randint(0, HEIGHT - w)
            sheep = Sheep(s_x, s_y, WHITE)
            
            # Genererer et nytt spøkelse 
            ghost = Ghost(random.randint(160, WIDTH-(160+w)), random.randint(0, HEIGHT-w), GREEN)
        
            # Gir poeng
            shepherd.points += 1
        if shepherd.stop == True:
            run = False
            print("Du tapte!")
            print("Du kan bare plukke opp en sau om gangen!")
            print(f"Du fikk {shepherd.points} poeng!")
    
    for o in obsts:
        o.draw()

    shepherd.move()
    shepherd.update()
    shepherd.checkCollision()
    shepherd.carryingSheep()
    shepherd.displayPoints()
    shepherd.draw()

    
    for g in ghosts:
        g.draw()
        g.update()
        if g.x-w <= shepherd.x <= g.x+w and g.y-w <= shepherd.y <= g.y+w:
            run = False
            print("Du døde!")
            print(f"Du fikk {shepherd.points} poeng!")
    
    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()

# Avslutter pygame
pg.quit()
