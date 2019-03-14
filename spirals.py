import numpy as np
import cProfile

class spirala():
    def __init__(self,radius):
        self.radius = radius
        a = self._a_()
        self.tab = np.zeros((a,a), dtype=int)

    # Zwraca rozmiar tablicy
    def _a_(self):
        return self.radius * 2 - 1

    # Wypełnia całą spiralę Ulama
    def _fill_(self):
        a = self._a_()
        i = self.radius - 1
        j = self.radius - 1
        num = 1
        self.tab[i,j] = num
        r = 1

        while num < a * a:
            if num + r > a * a: # ostatnia linijka
                for _ in range(0,r-1): # idź w prawo
                    j = j + 1
                    num = num + 1
                    self.tab[i,j] = num
            else:
                for _ in range(0,r): # idź w prawo
                    j = j + 1
                    num = num + 1
                    if num == a * a:
                        break
                    self.tab[i,j] = num

                for _ in range(0,r): # idź do góry
                    i = i - 1
                    num = num + 1
                    self.tab[i,j] = num

                r = r + 1

                for _ in range(0,r): # idź w lewo
                    j = j - 1
                    num = num + 1
                    self.tab[i,j] = num

                for _ in range(0,r): # idź w dół
                    i = i + 1
                    num = num + 1
                    self.tab[i,j] = num

                r = r + 1

    # Wypełnia tylko przekątne
    def _filldiags_(self):
        a = self._a_()
        i = self.radius - 1
        j = self.radius - 1
        num = 1
        self.tab[i,j] = num
        r = 0
        diff = 0

        while num < a * a:
            r = r + 1
            diff = diff + 2

            num += diff
            self.tab[i-r,j+r] = num # prawo góra
            num += diff
            self.tab[i-r,j-r] = num # lewo góra
            num += diff
            self.tab[i+r,j-r] = num # lewo dół
            num += diff
            self.tab[i+r,j+r] = num # prawo dół
    
    # Zwraca elementy z obu przekątnych bez powtórzeń
    def _diag_(self):
        a = self._a_()
        diag = set()
        for i in range( 0, a ):
            diag.add(self.tab[i,i])
            diag.add(self.tab[i, a - i - 1])
        return diag

    # Tworzy sam zbiór elementów na przekątnych
    def _diag2_(self):
        a = self._a_()
        num = 1
        diag = set()
        diag.add(num)
        diff = 0
        
        while num < a * a:
            diff += 2
            for _ in range(4):
                num += diff
                diag.add(num)
        return diag

    # Zwraca liczby pierwsze z obu przekątnych
    def _diagprimes_(self):
        a = self._a_()
        return primes_in_set(self._diag2_(), a*a)

    # Zwraca liczbe elementow na obydwu przekątnych
    def _diagsize_(self):
        return self._a_() * 2 - 1

    # Zwraca ułamek, jaki stanowią liczby pierwsze na obu diagonalach
    def _diag_prime_ratio_(self):
        return len(self._diagprimes_()) / self._diagsize_()
        

def primes_in_set(myset,amax):
    prlist = primesfrom2to(amax)
    return myset.intersection(prlist)

def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = np.ones(n//3 + (n%6==2), dtype=np.bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0][1:]+1)|1)]

    # Zwraca kolejną czwórkę elementów z przekątnych
def nextfourdiags(num, diff):
    four = set()
    diff += 2
    for _ in range(4):
        num += diff
        four.add(num)
    return [four, num, diff]

# Zbiera kolejne czwórki dodawane do przekątnych dla następnych promieni spirali
def collectfours(radius):
    a = radius*2 - 1
    prlist = set(primesfrom2to(a*a))

    num = 1
    diff = 0
    r = 1
    primes = 0
    while num < a*a:
        r+=1
        ar = r * 2 - 1
        diagsize = ar * 2 - 1
        [four,num,diff] = nextfourdiags(num,diff)
        newprimes = len(four.intersection(prlist)) # liczba nowych liczb pierwszych
        primes += newprimes
        ratio = primes/diagsize
        print("R:", r, "N:", ar, "diagsize", diagsize, "primes:", primes, "percent:", "{:.2f}%".format(ratio * 100), (ratio<0.1))
        if ratio < 0.1:
            return ar

## Liczę liczby pierwsze
primes10000 = primesfrom2to(10000)
idx = np.argpartition(primes10000,100)
pierwsze = primes10000[idx[:100]]
print("\n100 pierwszych liczb pierwszych:\n")
print(pierwsze)
print("\nSuma:")
print(sum(pierwsze), "\n")

## Spirala R = 5
R = 5
S = spirala(R)
S._fill_()
print("Spirala Ulama, R =", R)
print(S.tab)
print("\nNiepowtarzajace sie liczby na przekatnych:")
print(S._diag_())
print("Ich suma:", sum(S._diag_()))

## Spirala R = 10
R10 = 10
S10 = spirala(R10)
S10._filldiags_()
print("\nSpirala Ulama, R =", R10)
print(S10.tab)
print("\nNiepowtarzajace sie liczby na przekatnych:")
print(S10._diag_())

diag10_primes = S10._diagprimes_()
print("W tym liczby pierwsze:")
print(diag10_primes)
print("Ich suma:", sum(diag10_primes), "\n")

## Spirala R = 20
R20 = 20
S20 = spirala(R20)
S20._filldiags_()
print("\nNiepowtarzajace sie liczby na przekatnych, R = 20:")
print(S20._diag_())
diag20_primes = S20._diagprimes_()
print("W tym liczby pierwsze:")
print(diag20_primes)
print("Liczby pierwsze stanowia", "{:.0f}".format(S20._diag_prime_ratio_() * 100), "procent wszystkich elementow na przekatnych.")

print("\nSprawdzam kolejne spirale!\n")

#ratio = 1
#Rcheck = 2
#while(ratio >= 0.5):
#    Scheck = spirala(Rcheck)
#    ratio = Scheck._diag_prime_ratio_()
#    print("R =", Rcheck, "   {:.2f}%".format(ratio * 100))
#    Rcheck = Rcheck + 1
#print("\n")

pr = cProfile.Profile()
pr.enable()

N = collectfours(15000)
print("N = ", N)

pr.disable()
print("\n")
pr.print_stats()