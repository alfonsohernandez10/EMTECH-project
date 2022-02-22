from tkinter import *
from tkinter.ttk import*
import locale
import calendar
from mmap import ALLOCATIONGRANULARITY
from unicodedata import category, name
locale.setlocale(locale.LC_ALL, "")
from sklearn.datasets import fetch_california_housing
from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

#Creando el menú de acceso

def login():
    """ 
    Usuario: lifestore2022
    Contraseña: 123456

    """

    from inspect import getargs


    usuarioAccedio=False
    intentos=0
    mensaje_bienvenida="\nBienvenida(o) al sistema! \n"
    print(mensaje_bienvenida)

    while not usuarioAccedio:
        #Login credentials
        usuario=input("Ingrese su usuario: ")
        contraseña=input("Ingrese su contraseña: ")
        intentos +=1
        #Verify if password and user are correct
        if usuario=="lifestore2022" and contraseña =="123456":
            usuarioAccedio=True
            print("\n\n")
            print("Hola de nuevo")
        else:
            if usuario == "lifestore2022":
                print("Contraseña errónea,intente de nuevo")
                print ("Tienes,", 3- intentos, "intentos restantes")
            else:
                print(f"El usuario: '{usuario}' no está registrado")
                print ("Tienes,", 3- intentos, "intentos restantes")
        if intentos==3:
            print("Intentos agotados, por favor intente más tarde")
            exit()   
    print("Cargando...")

def punto_1():
    
    # Análisis de reviews y ventas 
    #{id_prod:[reviews]}
    prod_reviews ={}
    for sale in lifestore_sales:
    #Por cada venta que existe en lifestore sales vamos a obtener el id del producto
        prod_id=sale[1]
        review=sale[2]
        if prod_id not in prod_reviews.keys():    
            prod_reviews[prod_id]=[]
            #El valor para cada una de esas llaves (id del producto) será una lista vacía
        prod_reviews[prod_id].append(review)

    # Sacando el promedio de reviews para cada ID de producto
    #{id_prod:[review_prom,cant_reviews]}    
    id_review_prom={}
    for id,reviews in prod_reviews.items():
        rev_promedio=sum(reviews)/len(reviews)
        rev_promedio=int(rev_promedio*100)/100
        id_review_prom[id]=[rev_promedio,len(reviews)]   
        #Ésta lista contiene las reviews promedio  la cantidad de reviews recibidas

    #convirtiendo el diccionario de datos en lista
    #[[id_prod,review_prom,cant_reviews]]   
    dict_en_list=[]
    for id, lista in id_review_prom.items():
        rev_prom=lista[0]
        cantidad=lista[1]
        sub=[id,rev_prom,cantidad]
        dict_en_list.append(sub)

    def seg_elemento(sub):
        return sub[1]

    #[[id_prod,REVIEW_PROM,cant_reviews]] (sorted by qualication of the product)
    dicc_sort_qualif_review=sorted(dict_en_list,key=seg_elemento)
    #Nos otorga una lista ordenada de forma descendente en funcion del valor de la calificación del producto. 

    #[[id_prod,review_prom,CANT_REVIEWS]] (sorted by qualication of cant. de reviews=Vol_sales)
    dicc_en_list_sort_cant=sorted(dict_en_list,key=lambda lista:lista[2],reverse=True)
    #Nos otorga una lista ordenada de forma descendente en funcion del volumen de ventas.
    
    

    print(f"Descripción de los 5 productos con mayor demanda (mayor volúmen de ventas)")
    for sublista in dicc_en_list_sort_cant[:5]:
        id,rev, vol_ventas=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:2])
        precio=prod[2]
        stock=prod[4]
        datos=[id,rev,precio,vol_ventas,stock]
        print(f" \0\tID: {id} \0\tCalificación promedio: {rev}, \0\tVol. ventas: {vol_ventas} \tStock: {stock} \tProducto: {nombre}  ")
        

    print("\n")
            
    print(f"Descripción de los 5 productos con menor demanda (menor volúmen de ventas)")
    for sublista in dicc_en_list_sort_cant[-5:]:
        id,rev, vol_ventas=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])
        stock=prod[4]    
        print(f"\tID: {id} \tCalificación promedio: {rev}, \tVol. ventas: {vol_ventas} \t Stock: {stock} \tProducto: {nombre}")
    print("\n")
    
    print(f"Descripción de los 5 mejor calificados")
    for sublista in dicc_sort_qualif_review[-5:]:
        id,rev, vol_ventas=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])
        stock=prod[4]    
        print(f"\tID: {id} \tCalificación promedio: {rev}, \tVol. ventas: {vol_ventas} \t Stock: {stock} \tProducto: {nombre}")
    print("\n")

    # Obtención de búsquedas 
    #{id_prod:[id_searches]}
    prod_search ={}
    for search in lifestore_searches:
        id_product=search[1]
        if id_product not in prod_search.keys():
            prod_search[id_product]=[]
        prod_search[id_product].append(search[0])
        
    # Se crea el diccionario id_product-num_búsquedas
    # {id_prod:[num_searches]}    
    id_q_search={}
    for id,qsearch, in prod_search.items():
        if id not in id_q_search.keys():
            id_q_search[id]=len(qsearch)   
        
    #Ordenando el diccionario mediante una lista
    #[[id_prod,cant_search]]   
    dict_en_list=[]
    for data in id_q_search.items():
        id=data[0]
        qsearch=data[1]
        sub=[id,qsearch]
        dict_en_list.append(sub)

    dicc_en_list_sort_cant=sorted(dict_en_list,key=lambda lista:lista[1],reverse=True)
    #Nos otorga una lista ordenada de forma descendente en funcion del número de búsquedas.
    print("\n")
    print(f"Descripción de los 10 productos con más búsquedas")
    for sublista in dicc_en_list_sort_cant[:10]:
        id,q_searches=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])
        prod_cat= lifestore_products[indice_lsp]
        categoria=prod_cat[3]
        print(f"\tID: {id} \tBusquedas: {q_searches} \tCategoría: {categoria.capitalize()}\t\tProducto: {nombre}\t")
    print("\n")
    print(f"Descripción de los 10 productos con menos búsquedas")
    for sublista in dicc_en_list_sort_cant[-10:-1]:
        id,q_searches=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])
        prod_cat= lifestore_products[indice_lsp]
        categoria=prod_cat[3]
        print(f"\tID: {id}\t Busquedas: {q_searches}\t Categoría: {categoria.capitalize()}\t \tProducto: {nombre}\t")
def punto_2():

    # Análisis de reviews y ventas 
    #{id_prod:[reviews]}
    prod_reviews ={}
    for sale in lifestore_sales:
    #Por cada venta que existe en lifestore sales vamos a obtener el id del producto
        prod_id=sale[1]
        review=sale[2]
        if prod_id not in prod_reviews.keys():    
            prod_reviews[prod_id]=[]
            #El valor para cada una de esas llaves (id del producto) será una lista vacía
        prod_reviews[prod_id].append(review)

    # Sacando el promedio de reviews para cada ID de producto
    #{id_prod:[review_prom,cant_reviews]}    
    id_review_prom={}
    for id,reviews in prod_reviews.items():
        rev_promedio=sum(reviews)/len(reviews)
        rev_promedio=int(rev_promedio*100)/100
        id_review_prom[id]=[rev_promedio,len(reviews)]   
        #Ésta lista contiene las reviews promedio  la cantidad de reviews recibidas

    #convirtiendo el diccionario de datos en lista
    #[[id_prod,review_prom,cant_reviews]]   
    dict_en_list=[]
    for id, lista in id_review_prom.items():
        rev_prom=lista[0]
        cantidad=lista[1]
        sub=[id,rev_prom,cantidad]
        dict_en_list.append(sub)

    def seg_elemento(sub):
        return sub[1]

    #[[id_prod,REVIEW_PROM,cant_reviews]] (sorted by qualication of the product)
    dicc_sort_qualif_review=sorted(dict_en_list,key=seg_elemento,reverse=True)
    #Nos otorga una lista ordenada de forma descendente en funcion del valor de la calificación del producto. 

    #[[id_prod,review_prom,CANT_REVIEWS]] (sorted by qualication of cant. de reviews=Vol_sales)
    dicc_en_list_sort_cant=sorted(dict_en_list,key=lambda lista:lista[2],reverse=True)
    #Nos otorga una lista ordenada de forma descendente en funcion del volumen de ventas.

    print(f"Descripción de los 5 productos con mayor demanda (mayor volúmen de ventas)")
    for sublista in dicc_en_list_sort_cant[:5]:
        id,rev, vol_ventas=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])    
        print(f"ID: {id} \tCalificación promedio: {rev}, \tVol. ventas: {vol_ventas} \tProducto: {nombre}")
    print("\n")

    print(f"Descripción de los 5 productos mejores calificados por usuario")
    for sublista in dicc_sort_qualif_review[:5]:
        id,rev, vol_ventas=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])
        print(f"ID: {id} \tCalificación promedio: {rev}, \tVol. ventas: {vol_ventas} \tProducto: {nombre}")
    print("\n")
        
    print(f"Descripción de los 5 productos con menor demanda (menor volúmen de ventas)")
    for sublista in dicc_en_list_sort_cant[-5:]:
        id,rev, vol_ventas=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])    
        print(f"ID: {id} \tCalificación promedio: {rev}, \tVol. ventas: {vol_ventas} \tProducto: {nombre}")
    print("\n")

    print(f"Descripción de los 5 productos con menor calificación de usuario")
    for sublista in dicc_sort_qualif_review[-5:]:
        id,rev, vol_ventas=sublista
        indice_lsp=id-1
        prod=lifestore_products[indice_lsp]
        nombre=prod[1]
        nombre=nombre.split(",")
        nombre=" ".join(nombre[:4])
        print(f"ID: {id} \tCalificación promedio: {rev}, \tVol. ventas: {vol_ventas} \tProducto: {nombre}")                
def punto_3():
        #Dividiendo por meses las ventas
    #[[Id_sale,month]]
    id_fecha = [ [sale[0],sale[3]] for sale in lifestore_sales if sale[4]==0]

    # Categorizando las ventas por mes con un diccionario
    ##{Month,[Id_sales]}
    categorizacion_meses={}
    for par in id_fecha:
            id=par[0]
            _,mes,_=par[1].split("/")
            #Esto divide el string de la fecha y lo añade en tres variables 
            if mes not in categorizacion_meses.keys():
            #Si el mes no existe como llave en categorizacion_meses lo añade        
                    categorizacion_meses[mes]=[]
                    #categorizacion_meses es el key y el value será una lista
            categorizacion_meses[mes].append(id)
    # {Mes,[Ingreso,vol_venta]}
    mes_info={}
    for mes,ids_venta in categorizacion_meses.items():
            lista_mes=ids_venta
            suma_venta=0
            for id_venta in lista_mes:
                    indice=id_venta-1
                    info_venta=lifestore_sales[indice]
                    id_product=info_venta[1]
                    info_prod=lifestore_products[id_product-1]
                    precio=info_prod[2]
                    suma_venta+=precio
            mes_info[mes]=[suma_venta,len(lista_mes)]

    # Obtenemos la lista para ordenar los elementos en función del mes,ingreso y ventas
    # [[mes,ingreso,vol_ventas]]  
    print("\n")
    print("Ingreso mensual y ventas totales")

    mes_ingreso_ventas=[]

    for mes, datos in mes_info.items(): 
            ingreso_anual=0
            cant_anual=0
            ganancias, ventas=datos
            ing_mensual=datos[0]
            ingreso_anual=ingreso_anual+ing_mensual
            # cant_anual=cant_anual+datos[1]
            sub=[mes,ganancias,ventas]
            mes_ingreso_ventas.append(sub)
            
    #Se crean las listas ordenadas de acuerdo a cada dato        
    ord_mes=sorted(mes_ingreso_ventas)
    ord_ingreso=sorted(mes_ingreso_ventas,key=lambda x:x[1],reverse=True)
    ord_ventas=sorted(mes_ingreso_ventas,key=lambda x:x[2],reverse=True)
    #Se calculan valores mensuales y anuales

    suma_anual=0
    cant_anual=0
    for ord in ord_mes:
            mes=ord[0]
            ingreso=int(ord[1])
            ventas=ord[2]
            suma_anual=suma_anual+ingreso
            cant_anual=cant_anual+ventas
            prom_ventas_mensuales=suma_anual/len(mes)
            print(f"\tMes: {calendar.month_name[int(mes)].capitalize()}  \tTotal ingreso:   {locale.currency(ingreso,grouping=True)}  \tCantidad de ventas: {ventas}" )
    #Se imprimen los valores mensuales y totales anual        
    print(f"Ingreso total anual: {locale.currency(suma_anual,grouping=True)}")
    print(f"Ventas anuales totales: {(cant_anual)}")
    print(f"Ventas promedio mensuales: {locale.currency(prom_ventas_mensuales,grouping=True)} \n(Tómese en cuenta que los últimos meses del año no se registran ventas)")
    print("\n")

    print("Top 5 meses con más alto ingreso")
    suma_top_mes=0
    cant_top_mes=0
    for ord in ord_ingreso[:5]:
            mes=ord[0]
            ingreso=int(ord[1])
            ventas=ord[2]
            suma_top_mes=suma_top_mes+ingreso
            cant_top_mes=cant_top_mes+ventas
            prom_ventas_mensuales=suma_anual/len(mes)
            print(f"\tMes: {calendar.month_name[int(mes)].capitalize()}  \tTotal ingreso:   {locale.currency(ingreso,grouping=True)}  \tCantidad de ventas: {ventas} ")
    print("\n")


    print("Top 5 meses con mayores ventas")
    suma_top_mes=0
    cant_top_mes=0
    for ord in ord_ventas[:5]:
            mes=ord[0]
            ingreso=int(ord[1])
            ventas=ord[2]
            suma_top_mes=suma_top_mes+ingreso
            cant_top_mes=cant_top_mes+ventas
            prom_ventas_mensuales=suma_anual/len(mes)
            print(f"\tMes: {calendar.month_name[int(mes)].capitalize()}  \tTotal ingreso:   {locale.currency(ingreso,grouping=True)}  \tCantidad de ventas: {ventas} ")
    print(f"Ingreso total: {locale.currency(suma_top_mes,grouping=True)}")
    print(f"Ventas totales: {(cant_top_mes)}")        
def menu():
    login()
    while True:
        print("\n¿Que operación desea hacer:?")
        print("\t1. Realizar el punto 1: Oprima 1")
        print("\t2. Realizar el punto 2: Oprima 2")
        print("\t3. Realizar el punto 3: Oprima 3")
        print("\t0. Salir")
        seleccion=input("> ")
        if seleccion =="1":
            punto_1()
        elif seleccion=="2":
            punto_2()
            print("\n")
        elif seleccion=="3":
            punto_3()
            print("\n")
        elif seleccion=="0":
            exit()
        else:
            print("Opción no valida")
menu()






                