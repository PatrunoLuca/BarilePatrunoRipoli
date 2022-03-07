from .conica import Conica
import pygame

class Retta(Conica):


    def __init__(self, a, b, c):
        self.__a = float(a)
        self.__b = float(b)
        self.__c = float(c)
        self.__punti = []
        
        super().__init__(a,b,c)
        
        if (self.__a, self.__b) == (0.0, 0.0):
            raise Exception(f"{self.eq_implicita()} non è una retta")
        elif self.__b == 0.0:
            self.__asse_di_simmetria = "x"
            self.__m = 0.0
            self.__q = self.__c
        elif self.__a == 0.0:
            self.__asse_di_simmetria = "y"
            self.__m = 0.0
            self.__q = self.__c
        else:
            self.__asse_di_simmetria = "y"
            self.__m = - self.__a / self.__b
            self.__q = - self.__c / self.__a

    @property
    def simmetria(self):
        return self.__asse_di_simmetria

    @property
    def m(self):
        return self.__m
        
    @property
    def q(self):
        return self.__q

    def risolvi(self, noto=int):
        if self.__m != 0.0:
            soluzione = int((self.__m * noto) + self.__c)
        else:
            if  self.__asse_di_simmetria == "y":
                soluzione = int(self.__b)
            else:
                soluzione = int(self.__a)
        if self.__asse_di_simmetria == "y":
            self.__punti.append((noto, soluzione))
        else:
            self.__punti.append(( soluzione, noto))
        return soluzione

    def eq_implicita(self):
        segno_x = "" if self.__a >= 0 else "- "
        segno_y = "+" if self.__b >= 0 else "-"
        segno_c = "+" if self.__c >= 0 else "-"
        
        x = f"{segno_x}{self.__a}X" if self.__a != 1.0 else f"{segno_x}X"
        y = f"{segno_y} {abs(self.__b)}Y" if abs(self.__b) != 1.0 else f"{segno_y} Y"
        c = f"{segno_c} {abs(self.__c)}"
        return f"{segno_x}{x} {y} {c} = 0"

    def eq_esplicita(self):
        x_y = "Y" if self.__asse_di_simmetria == "y" else "X"
        m = f"{self.__m}X " if self.__asse_di_simmetria == "y" else f"{self.__m}Y "
        
        if self.__m == 0.0:
            segno = "" if self.__q >= 0 else "- "
            return f"{x_y} = {segno}{self.__q}"
        elif self.__q != 0.0:
            segno = "+" if self.__q >= 0 else "-"
            return f"{x_y} = {m} {segno} {abs(self.__q)}" 
        else:
            return f"{x_y} = {self.__a}" if x_y == "X" else f"{x_y} = {self.__b}" 

    
    @classmethod
    def intersezione(cls, r1, r2):
        if type(r1) != Retta or type(r2) != Retta:
            raise Exception
        elif (r1.a, r1.b, r1.c) == (r2.a, r2.b, r2.c):
            return "Coincidenti"
        elif r1.m == r2.m:
            return None
        else:
            det = (r1.a * r2.b) - (r2.a * r1.b)
            det_x = (r1.c * r2.b) - (r2.c * r1.b)
            det_y = (r1.a * r2.c) - (r2.a * r1.c)
            return (det_x / det, det_y / det)

    @classmethod
    def from_points(cls, punto1, punto2):
        assert len(punto1) == 2 
        assert len(punto2) == 2
        assert type(punto1) == tuple 
        assert type(punto2) == tuple
        
        x = (punto2[0] - punto1[0])
        y = (punto2[1] - punto1[1])
        m = y/x 
        q = punto1[-1] - (m * punto1[0])
        return cls(m, -1, q)
    
    @classmethod
    def from_coeff(cls, m, punto):
        assert len(punto) == 2
        assert type(punto) == tuple
        assert type(m) == float
        
        q = punto[-1] - (m * punto[0])
        return cls(m, -1, q)

    @classmethod
    def from_intercepts(cls, q, punto):
        assert len(punto) == 2
        assert type(punto) == tuple
        assert type(q) == float
        
        m = (punto[-1] - q) / punto[0]
        return cls(m, -1, q) 

if __name__ == "__main__":
    m = float(input("Inserisci valore di 'm' nella prima retta:    "))
    x = float(input("Inserisci valore di 'x' del punto nella prima retta:    "))
    y = float(input("Inserisci valore di 'y' del punto nella prima retta:    "))
    x1 = float(input("\nInserisci valore di 'x1' nella seconda retta:  "))
    y1 = float(input("Inserisci valore di 'y1' nella seconda retta:  "))
    x2 = float(input("Inserisci valore di 'x2' nella seconda retta:  "))
    y2 = float(input("Inserisci valore di 'y2' nella seconda retta:  "))

    retta1 = Retta.from_coeff(m, (x, y))
    retta2 = Retta.from_points((x1, y1), (x2, y2))

    retta1.coppie(1, 20)
    retta2.coppie(1, 20)
    print(f"\n\nRetta 1:\n  Implicita: {retta1.eq_implicita()}\n  Esplicita: {retta1.eq_esplicita()}\n  Punti: {retta1.coppie(1,10)}")
    print(f"\n\nRetta 2:\n  Implicita: {retta2.eq_implicita()}\n  Esplicita: {retta2.eq_esplicita()}\n  Punti: {retta2.coppie(1,10)}")
    print(f"\n\nIl punto in cui le due rette si incontrano è il punto: {Retta.intersezione(retta1, retta2)}")
    
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
        clock.tick(30)
        screen.fill("white")
        pygame.draw.polygon(screen, "blue", retta1.coppie(1, 20))
        pygame.draw.polygon(screen, "red", retta2.coppie(1, 20))
    pygame.quit()

    