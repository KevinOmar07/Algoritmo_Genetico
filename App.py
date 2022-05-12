import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import matplotlib.pyplot as plt
# from matplotlib import pyplot
import math
import random

from cv2 import sepFilter2D, sort
from numpy import fix

class algoritmo_genetico(QMainWindow) :
    
    BANDERA_PROBABILIDAD = True
    BANDERA_MAX_O_MIN = True # Si la variable es verdadera quiere decir que se busca el maximo en caso contrario se busca el minimo
    PO_TOTAL = 0
    CANTIDAD = 0
    PRESICION = 0
    BITS = 0
    PD = 0
    PMI = 0
    PMG = 0
    A = 0
    B = 0
    NUMERO_IMAGEN = 0
    LISTA_CEROS = list()
    LISTA_INDIVIDUOS_BINARIO = list()
    LISTA_NUEVOS_INDIVIDUOS = list()
    
    def __init__(self) :
        super().__init__()
        uic.loadUi ("Vista/vista.ui", self)
        self.btn_calcular.clicked.connect(self.fn_calcular)
    
    def fn_calcular(self) :
        print('------------------------comenzamos------------------------\n')
        print(self.inputPD.text())
        self.limpiar_variables_globales()
        self.iniciar_probabilidades()
        if (self.fn_calcular_cantidad()) & (self.BANDERA_PROBABILIDAD) :
            print('Todo correcto: ', self.BANDERA_PROBABILIDAD)
            self.fn_calcuar_bits()
            self.fn_generar_individuos()
            self.fn_seleccion()
            if len(self.LISTA_INDIVIDUOS_BINARIO) > 0 :
                self.fn_cruza()
                self.fn_mutacion()
                self.fn_limpieza()
                self.fn_unir_poblacion()
                self.fn_poda()
                
            else :
                print("Ninguno de los individuos tiene probabilidad de descendencia")
        else :
            print('Algo salio mal, alguno de los datos ingresados es incorrecto o esta vacio')
            
    def limpiar_variables_globales (self) :
        self.LISTA_CEROS.clear()
        self.LISTA_INDIVIDUOS_BINARIO.clear()
        self.LISTA_NUEVOS_INDIVIDUOS.clear()
        self.BANDERA_PROBABILIDAD = True
        self.BANDERA_MAX_O_MIN = True
    
    def iniciar_probabilidades (self) :
        
        try:
            pd = int(self.inputPD.text())
            pmi = int(self.inputPMI.text())
            pmg = int(self.inputPMG.text())
            
            if (pd > 0) & (pd <= 100):
                print("Entro")
                self.PD = pd / 100
            else : 
                print("El procentaje del PD es incorrecto")
                raise TypeError("El procentaje del PD es incorrecto")
                
            if (pmi > 0) & (pmi <= 100) :
                self.PMI = pmi / 100
            else : 
                print("El procentaje del PMI es incorrecto")
                raise TypeError("El procentaje del PMI es incorrecto")
                
            if (pmg > 0 ) & (pmg <= 100) :
                self.PMG = pmg / 100
            else : 
                print("El procentaje del PMG es incorrecto")
                raise TypeError("El procentaje del PMG es incorrecto")
                
        except Exception as e:
            self.BANDERA_PROBABILIDAD = False
            print("Error en los porcentajes de probabilidad: " + repr(e))
            
    def fn_calcular_cantidad(self):
        print('------------------------Calcular cantidad------------------------\n')
        aux = True
        
        try :
            intervalo_inicio = int(self.inter_inicio.text())
            intervalo_fin = int(self.inter_fin.text())
            precision = float(self.preci.text())
            
            if precision < 1 :
                self.PRESICION = precision
                if intervalo_fin > intervalo_inicio :
                    self.A = intervalo_inicio
                    self.B = intervalo_fin
                    self.CANTIDAD = int((intervalo_fin - intervalo_inicio) / precision) + 1
                else :
                    self.B = intervalo_inicio
                    self.A = intervalo_fin
                    self.CANTIDAD = int((intervalo_inicio - intervalo_fin) / precision) + 1
                
                print(f"Inicio: {intervalo_inicio} | Final: {intervalo_fin} | Presicion: {precision}")
                print(f'Cantidad: {self.CANTIDAD}')
                
                self.soluciones.setText(str(self.CANTIDAD))
            else :
                aux = False
            
            return aux
        except :
            print ("Ingrese los datos correctamente")
            return False
        
    def fn_calcuar_bits(self):
        print('------------------------Calcular bits------------------------\n')
        n = 0
        bits = 2**n
        
        while bits < self.CANTIDAD :
            n += 1
            bits = 2**n
            print("bits: ", bits)
        
        self.BITS = n
        
        print(f"Cantidad de bits: {bits}")
        self.numBits.setText(str(n))
        
    def fn_generar_individuos(self) :
        print('------------------------Generar individuos------------------------\n')
        try :
            po = int (self.pMin.text())
            contador = 0;
            self.LISTA_CEROS = self.crear_lista_ceros()
            
            print("Lista de ceros\n")
            for edad in self.LISTA_CEROS:
                print(edad)
            
            if po < 1 :
                raise ValueError("La población debe ser mayor a 0")
            
            while contador < po :
                contador += 1
                individuo = random.randint(1, self.CANTIDAD - 1)
                print(f"Individuo entero {contador} : {individuo}\n")
                binario = format(individuo, "b")
                if len(binario) < self.BITS :
                    print("Le faltan ceros")
                    binario = self.LISTA_CEROS[(self.BITS-len(binario))-1] + binario
                    
                self.LISTA_INDIVIDUOS_BINARIO.append(binario)
                print(f"Individuo binario {contador} : {binario}\n")
        except Exception as e:
            print("Error al generar los individuos: " + repr(e))
            print("La población debe ser mayor a 0")
    
    def crear_lista_ceros (self) :
        contador = 1
        aux = "0"
        lista_ceros = list()
        while contador < self.BITS :
            lista_ceros.append(aux)
            aux = aux + "0"
            contador += 1
        
        return lista_ceros
            
    def fn_seleccion (self) :
        print('------------------------Seleccion------------------------\n')
        aux = False
        
        for x in self.LISTA_INDIVIDUOS_BINARIO :
            for y in self.LISTA_INDIVIDUOS_BINARIO :
                if x != y :
                    i = x+y
                    if aux :
                        print("i: ", i)
                        aux2 = False # Bandera para saber si es el primer dato combinado
                        for z in self.LISTA_NUEVOS_INDIVIDUOS :
                            if (i == (z[0]+ z[1])) | ( i == (z[1]+z[0]) ) :
                               aux2 = True
                               p = z[1]+z[0]
                               print(f"Verdadero for. i: {i} | z: {z} | p: {p}")
                               break
                        
                        if aux2 != True :
                            print("Se agrega: ", i)
                            print("PD: ", self.PD)
                            pd = random.randint(1, 100) / 100
                            print(f"pd: {pd} | PD: {self.PD}")
                            puntoCorte = random.randint(1, self.BITS-1)
                            if pd <= self.PD:
                                self.LISTA_NUEVOS_INDIVIDUOS.append([x, y, puntoCorte])
                            else :
                                print("Se agrega pero se elimina por PD: ", i)
                        else :
                            print("No se agrega: ", i)
                    else :
                        print("Falso: ", i)
                        pd = random.randint(1, 100) / 100
                        puntoCorte = random.randint(1, self.BITS-1)
                        if pd <= self.PD:
                            self.LISTA_NUEVOS_INDIVIDUOS.append([x, y, puntoCorte])
                        aux = True
        t = len(self.LISTA_NUEVOS_INDIVIDUOS)
        print(f"Tamaño: {t}")
                    
    def fn_cruza (self) :
        print("Si hay cruza\n")
        print('------------------------Cruza------------------------\n')
        lista_aux = list()
        
        for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
            print(f"Individuo: {individuo}\n")
            # AB1
            izquierda1 = individuo[0][:individuo[2]]
            derecha1 = individuo[1][individuo[2]:]
            
            pmi = random.randint(1, 100) / 100
            
            lista_aux.append([(izquierda1+derecha1), pmi])
            
            print(f"Cruza 1: {izquierda1}{derecha1}\n")
            
            #AB2
            izquierda2 = individuo[1][:individuo[2]]
            derecha2 = individuo[0][individuo[2]:]
            
            pmi = random.randint(1, 100) / 100
            
            lista_aux.append([(izquierda2+derecha2), pmi])
            
            print(f"Cruza 2: {izquierda2}{derecha2}\n")
            
            print("-----------------------------------\n")
        
        t = len(lista_aux)
        self.LISTA_NUEVOS_INDIVIDUOS = lista_aux
        print(f"Tamaño lista: {t}")
        print(f"PMI: {self.PMI}")
        print(self.LISTA_NUEVOS_INDIVIDUOS)
            
    def fn_mutacion (self):
        print('------------------------Mutacion------------------------\n')
        for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
            if individuo[1] <= self.PMI:
                print(f"El individuo {individuo[0]} puede mutar | PMG {self.PMG}\n")
                lista_binarios = list(individuo[0])
                print(lista_binarios)
                
                lista_aux = list()
                for bit in lista_binarios:
                    aux = "0"
                    pmg = random.randint(1, 100) / 100
                    if pmg <= self.PMG :
                        if bit == "0" :
                            aux = "1"
                    else :
                        aux = bit
                    lista_aux.append(aux)
                
                mutado = "".join(lista_aux)
                print(f"Original: {individuo[0]}")
                individuo[0] = mutado
                print(f"Mutado: {individuo[0]}")
                
    def fn_limpieza (self) :
        print('\n------------------------Limpieza------------------------\n')
        
        t = len(self.LISTA_NUEVOS_INDIVIDUOS)
        print(f"Tamaño antes: {t}\n")
        
        for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
            numDecimal = int(individuo[0], 2) # Se convierte el valor binario a entero para hacer la limpieza
            if numDecimal > (self.CANTIDAD-1) :
                print(f"Se elimina: {numDecimal}")
                self.LISTA_NUEVOS_INDIVIDUOS.remove(individuo)
            else :
                print(f"No se elimina: {numDecimal}")

        t = len(self.LISTA_NUEVOS_INDIVIDUOS)
        print(f"\nTamaño antes: {t}")

    def fn_unir_poblacion (self):
        print('\n------------------------Unir poblacion------------------------\n')
        
        lista_aux = list()
        self.PO_TOTAL = len(self.LISTA_NUEVOS_INDIVIDUOS) + len(self.LISTA_INDIVIDUOS_BINARIO)
        # Primer for para agregar los individuos inciales a nueva lista
        for originales in self.LISTA_INDIVIDUOS_BINARIO :
            ppAux = random.randint(1, 100) / 100
            lista_aux.append([originales, ppAux])
                
        # Segundo for para agregar los individuos nuevos a nueva lista
        for nuevos in self.LISTA_NUEVOS_INDIVIDUOS :
            ppAux = random.randint(1, 100) / 100
            lista_aux.append([nuevos[0], ppAux])
            
        
        
        if (self.radioMax.isChecked() == True) | ((self.radioMax.isChecked() == False) & (self.radioMin.isChecked() == False)) :
            # Ordenar de mayor a menor
            lista_aux = sorted(lista_aux, key=lambda indi : indi[1], reverse=True)
            print("Maximo seleccionado\n")
        elif self.radioMin.isChecked() :
            print("Minimo seleccionado\n")
            # Ordenar de menor a mayor
            lista_aux = sorted(lista_aux, key=lambda indi : indi[1])
            self.BANDERA_MAX_O_MIN = False
            
        self.LISTA_NUEVOS_INDIVIDUOS = lista_aux
        self.fn_graficar_funcion()
            
    def fn_poda (self) :
        print('\n------------------------Poda------------------------\n')
        try :
            poMax = int(self.pMax.text())
            # poTotal = len(self.LISTA_NUEVOS_INDIVIDUOS) + len(self.LISTA_INDIVIDUOS_BINARIO)
            if poMax < 1 :
                raise TypeError("El dato de la población maxima es incorrecta")
            
            print(f"pobla total: {self.PO_TOTAL} | Max: {poMax}")
            
            if self.PO_TOTAL > poMax :
                PP = poMax / self.PO_TOTAL
                
                lista_poda = list()
                
                # For para llenar lista auxiliar
                for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
                    lista_poda.append(individuo)
                    
                #For para eliminar los que sean mayores al pp
                for individuo in lista_poda :
                    print(f"Indi: {individuo}")
                    if individuo[1] > PP :
                        print(f"-> {individuo[1]} es mayor que {PP}")
                        self.LISTA_NUEVOS_INDIVIDUOS.remove(individuo)
                
                t = len(self.LISTA_NUEVOS_INDIVIDUOS)
                print(f"Tamaño final: {t}") 
                
                if len(self.LISTA_NUEVOS_INDIVIDUOS) > poMax :
                    demas = len(self.LISTA_NUEVOS_INDIVIDUOS) - poMax
                    for x in range(demas) :
                        self.LISTA_NUEVOS_INDIVIDUOS.pop()
                
                t = len(self.LISTA_NUEVOS_INDIVIDUOS)
                print(f"Tamaño final 2: {t}\n") 
                
                for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
                    print(f"LNI - PP: {individuo}")
                    
                self.txt_poda.setText("Hubo poda")
            else :
                print("No hay poda")
                self.txt_poda.setText("No hubo poda")
            self.po_final.setText(str(len(self.LISTA_NUEVOS_INDIVIDUOS)))
                
        except Exception as e:
            print(repr(e))
            print("El dato de la población maxima es incorrecta")

    def fn_graficar_funcion (self) :
        print("\nAqui se graficara la funcion\n")
        
        x = []
        y = []
        coordenadas = []
        
        # f(x): 1.50Cos(0.25x)Sen(1.50x) + 1.50Sen(1.50x)
        
        # Para calcular X y Y
        for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
            i = self.A + (int(individuo[0], 2) * self.PRESICION)
            # individuo[1] = i
            #x.append(i)
            y_aux = ((1.50)*(math.cos(0.25*i))*(math.sin(1.50*i))) + ((1.50)*math.sin(1.50*i))
            #y.append(y_aux)
            
            coordenadas.append([i, y_aux])
            print(f"Individuo: {individuo} | x: {i} | y: {y_aux}")
         
            #x.sort(reverse=True)
            #y.sort(reverse=True)
            texto = "nose"
        if self.BANDERA_MAX_O_MIN :
            coordenadas = sorted(coordenadas, key=lambda xy : xy[1], reverse=True)
            texto = "Maximo"
        else :
            coordenadas = sorted(coordenadas, key=lambda xy : xy[1])
            texto = "Minimo"
            
        for xy in coordenadas :
            x.append(xy[0])
            y.append(xy[1])
            
        var = range(-25, 25)


        plt.plot(var,[f1(i) for i in var], label= 'f(x)')
            
        plt.scatter(x,y, label=texto, color = "green")
        plt.axhline(0, color="black")
        plt.axvline(0, color="black")
        
        plt.savefig(f"Grafica{self.NUMERO_IMAGEN}.png")
        plt.legend(loc='lower right')
        plt.show()
        self.NUMERO_IMAGEN += 1

        # Valores del eje X que toma el gráfico.
        ''' x = range(-10, 15)
        # Graficar ambas funciones.
        pyplot.plot(x, [f1(i) for i in x])
        pyplot.plot(x, [f2(i) for i in x])
        # Establecer el color de los ejes.
        pyplot.axhline(0, color="black")
        pyplot.axvline(0, color="black")
        # Limitar los valores de los ejes.
        pyplot.xlim(-10, 10)
        pyplot.ylim(-10, 10)
        # Guardar gráfico como imágen PNG.
        pyplot.savefig("output.png")
        # Mostrarlo.
        pyplot.show() '''
        
# Función cuadrática.
def f1(i):
    # return 2*(x**2) + 5*x - 2
    return ((1.50)*(math.cos(0.25*i))*(math.sin(1.50*i))) + ((1.50)*math.sin(1.50*i))
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = algoritmo_genetico()
    ventana.windowTitle = "Algoritmos Geneticos"
    ventana.show()
    sys.exit(app.exec_())