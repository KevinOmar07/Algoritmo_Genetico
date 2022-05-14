import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import matplotlib.pyplot as plt
import cv2  
import math
import random

class algoritmo_genetico(QMainWindow) :
    
    BANDERA_PROBABILIDAD = True # Si la variable es verdadera quiere decir que hay individuos con probabilidad de desendencia
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
    NUMERO_IMAGEN = 1
    NUM_GENRACION = 1
    LISTA_CEROS = list()
    LISTA_INDIVIDUOS_BINARIO = list()
    LISTA_NUEVOS_INDIVIDUOS = list()
    LISTA_ME_PRO_PE = list()
    
    def __init__(self) :
        super().__init__()
        uic.loadUi ("Vista/vista.ui", self)
        self.btn_calcular.clicked.connect(self.fn_calcular)
    
    def fn_calcular(self) :
        print('------------------------comenzamos------------------------\n')
        print(self.inputPD.text())
        print(type(self.generaciones.value()))
        self.msj_error.setText("")
        for generacion in range(self.generaciones.value()) :
            print(f"Generaaaaa: {generacion}")
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
                    self.msj_error.setText("Error, ninguno de los individuos tiene probabilidad de descendencia")
                    print("Ninguno de los individuos tiene probabilidad de descendencia")
            else :
                self.msj_error.setText("Algo salio mal, alguno de los datos ingresados es incorrecto o esta vacio")
                print('Algo salio mal, alguno de los datos ingresados es incorrecto o esta vacio')
                break
            
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
                self.msj_error.setText("Error, El procentaje del PD es incorrecto")
                raise TypeError("El procentaje del PD es incorrecto")
                
            if (pmi > 0) & (pmi <= 100) :
                self.PMI = pmi / 100
            else : 
                self.msj_error.setText("Error, El procentaje del PMI es incorrecto")
                print("El procentaje del PMI es incorrecto")
                raise TypeError("El procentaje del PMI es incorrecto")
                
            if (pmg > 0 ) & (pmg <= 100) :
                self.PMG = pmg / 100
            else :
                self.msj_error.setText("Error, El procentaje del PMG es incorrecto")
                print("El procentaje del PMG es incorrecto")
                raise TypeError("El procentaje del PMG es incorrecto")
                
        except Exception as e:
            self.BANDERA_PROBABILIDAD = False
            self.msj_error.setText("Error en los porcentajes de probabilidad")
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
            self.msj_error.setText("Error, Ingrese los datos del intervalo y/o precision correctamente")
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
            self.msj_error.setText("Error al generar los individuos, solo ingresar datos enteros: " + repr(e))
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
            
        self.LISTA_NUEVOS_INDIVIDUOS = lista_aux
        self.fn_obtener_mejores_peores_promedio()
        self.fn_graficar_funcion(1)
            
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
                
                ''' if len(self.LISTA_NUEVOS_INDIVIDUOS) > poMax :
                    demas = len(self.LISTA_NUEVOS_INDIVIDUOS) - poMax
                    for x in range(demas) :
                        self.LISTA_NUEVOS_INDIVIDUOS.pop() '''
                
                t = len(self.LISTA_NUEVOS_INDIVIDUOS)
                print(f"Tamaño final 2: {t}\n") 
                
                for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
                    print(f"LNI - PP: {individuo}")
                    
                self.txt_poda.setText("Hubo poda")
            else :
                print("No hay poda")
                self.txt_poda.setText("No hubo poda")
                
            lista_max_o_min = list()
            for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
                lista_max_o_min.append(self.fn_encontrar_xy(individuo[0]))
            
            
            if (self.radioMax.isChecked() == True) | ((self.radioMax.isChecked() == False) & (self.radioMin.isChecked() == False)) :
                # Ordenar para maximo
                lista_max_o_min = sorted(lista_max_o_min, key=lambda index : index[1], reverse=True) 
                print("Maximo seleccionado\n")
            elif self.radioMin.isChecked() :
                print("Minimo seleccionado\n")
                # Ordenar para minimo
                lista_max_o_min = sorted(lista_max_o_min, key=lambda index : index[1])
                self.BANDERA_MAX_O_MIN = False
            
            for individuo in lista_max_o_min :
                print(f"LNM - PP: {individuo}")
            
            if len(lista_max_o_min) > poMax :
                print("Es mayor")
                demas = len(lista_max_o_min) - poMax
                for x in range(demas) :
                    lista_max_o_min.pop()
            else :
                print("Es menor")
            
            self.LISTA_NUEVOS_INDIVIDUOS = lista_max_o_min
            
            for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
                print(f"LNI2 - PP: {individuo}")
            
            self.fn_graficar_funcion(2)
            
            self.po_final.setText(str(len(self.LISTA_NUEVOS_INDIVIDUOS)))
                
        except Exception as e:
            print(repr(e))
            self.msj_error.setText("El dato de la población maxima es incorrecta")
            print("El dato de la población maxima es incorrecta")

    def fn_encontrar_xy (self, individuo) :
        i = self.A + (int(individuo, 2) * self.PRESICION)
        y = ((1.50)*(math.cos(0.25*i))*(math.sin(1.50*i))) + ((1.50)*math.sin(1.50*i))
        return [i,y]

    def fn_obtener_mejores_peores_promedio (self):
        
        xy = list()
        
        for individuo in self.LISTA_NUEVOS_INDIVIDUOS :
            print(f"iniiiii: {individuo}")
            xy.append([self.NUM_GENRACION, self.fn_encontrar_xy(individuo[0])[1]])
        
        xy.sort(reverse=True)
        
        for ind in xy :
            print(f"histo: {ind}")
        
        xy_mejor = xy[0]
        ultimo = len(xy) - 1
        xy_peor = xy[ultimo]
        y_aux = ( xy_mejor[1] + xy_peor[1]) / (2)
        xy_promedio = [self.NUM_GENRACION, y_aux]
        
        self.LISTA_ME_PRO_PE.append([xy_mejor,xy_peor,xy_promedio])
    
    def fn_graficar_funcion (self, tipo) :
        print("\nAqui se graficara la funcion\n")
        
        v = self.generaciones.value()
        print(f"Valor: {v}")
        
        x = []
        y = []
        
        # si tipo == 1 se grafican los mejores, peores y promedio, si tipo == 2 se grafican los individuos por generaciones
        
        print(f"Numero de generacion: {self.NUM_GENRACION}")
        
        if tipo == 2 :
                        
            for x_y in self.LISTA_NUEVOS_INDIVIDUOS :
                x.append(x_y[0])
                y.append(x_y[1])
            
            
            fig = plt.figure(figsize=(12,7))
            fig.tight_layout()
            plt.subplot(1, 1, 1)
            plt.scatter(x, y)
            
            titulo = 'Generacion ' + str(self.NUMERO_IMAGEN) + " | " + str(len(self.LISTA_NUEVOS_INDIVIDUOS)) + " Individuos"
            
            plt.xlim(-2, 15)
            plt.ylim(-5, 10)
            # self.generaciones.value()+2
            # plt.legend(loc='lower right')
            plt.title(titulo)
            plt.savefig(f"Imagenes/Generacion{self.NUMERO_IMAGEN}.png")
            plt.close()
            
            if self.NUMERO_IMAGEN < self.generaciones.value() :
                self.NUMERO_IMAGEN += 1
            else :
                if self.BANDERA_MAX_O_MIN :
                    self.fn_generar_video("Individuos_Maximos")
                else :
                    self.fn_generar_video("Individuos_Minimos")
                self.NUMERO_IMAGEN == 1
                    
        if (self.NUM_GENRACION == self.generaciones.value()) & (tipo == 1) :        
            contador = 0
            fig = plt.figure(figsize=(12,7))
            fig.tight_layout()
            plt.subplot(1, 1, 1)
            
            atributos = [["Mejor", "green"], ["Peor", "orange"], ["Promedio", "blue"]]
            
            while contador < 3 :
                for xy in self.LISTA_ME_PRO_PE :
                   # print(f"xy: {xy[0][0]} | {xy[1][0]} | {xy[2][0]}")
                   print(f"{atributos[contador][0]}: x: {xy[contador][0]} | y: {xy[contador][1]} ")
                   x.append(xy[contador][0])
                   y.append(xy[contador][1])
                y.sort()
                plt.plot(x, y, label= atributos[contador][0], color = atributos[contador][1])
                x.clear()
                y.clear()
                contador += 1                
            
            print("--------------historico---------\n")
            
            for x_y in self.LISTA_ME_PRO_PE :
                print(x_y)
            
            plt.savefig(f"Imagenes/Historico.png")
            plt.legend(loc='lower right')
            plt.show()
            
            self.NUM_GENRACION = 1
            self.LISTA_ME_PRO_PE.clear()
        elif tipo == 1 :
            self.NUM_GENRACION += 1 
   
    def fn_generar_video(self, nombre) :
        lista_imagenes = list()
        for imagen in range(self.generaciones.value()) :
            imagen_nombre = "Imagenes/Generacion" + str(imagen+1) + ".png"
            openCv = cv2.imread(imagen_nombre)
            lista_imagenes.append(openCv)
        img = lista_imagenes[-1]
        
        alto, ancho = img.shape[:2]
        ruta = "Videos/" + nombre + ".mp4"
        video = cv2.VideoWriter(ruta, cv2.VideoWriter_fourcc(*"mp4v"), 4, (ancho, alto))
        
        for index in lista_imagenes :
            video.write(index)
            
        video.release()
       
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = algoritmo_genetico()
    ventana.windowTitle = "Algoritmos Geneticos"
    ventana.show()
    sys.exit(app.exec_())