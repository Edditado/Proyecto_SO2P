#encoding: utf8
import sys


#Funcion de Algoritmo Optimo
def optimumAlg(lines, cacheSize):
	#Diccionario de lineas con las posiciones donde se vuelven a repetir, 
	#para facilitar busqueda de la linea menos usada en el futuro de la cache:
	#{"linea":[pos1,pos2,..]}
	wlDict = {}
	wlSize = len(lines)	
	for i in xrange(wlSize):
		if lines[i] not in wlDict:
			wlDict[lines[i]] = [i]

		else:
			wlDict[lines[i]].append(i)

	#print len(wlDict)

	#La cache será un Set (Conjunto) de lineas, los sets se forman de elementos unicos y su acceso es muy rápido
	cache = set([])

	#Numero de misses
	misses = 0
	#Iteracion de la tupla de lineas
	for i in xrange(wlSize):
		#print i

		#Se remueve la posición de la linea actual de wlDict, así el primer elemento del arreglo 
		#de dicha linea será la próxima posición en donde será usada nuevamente.
		wlDict[lines[i]].remove(i)
		if lines[i] not in cache:
			if len(cache) < cacheSize:
				cache.add(lines[i])
				misses += 1
				#print cache
			else:
				#Diccionario de lineas futuras del cache: {pos:"linea",...}:
				futureItems = {}
				#Iteración de las lineas en cache
				for item in cache:
					#Si el arreglo (valor) de la linea actual(llave) en wlDict está vacio
					#significa que la linea actual no se repetirá en el futuro
					if wlDict[item] == []:
						#Se reemplaza la linea actual del cache por la linea actual de la tupla de lineas
						#y se sale del ciclo
						cache.discard(item)
						cache.add(lines[i])
						futureItems = {}
						misses += 1
						#print cache
						break
					else:
						#Se va añadiendo el primer elemento del arreglo(de wlDict) de la linea actual(de cache) 
						#al diccionario de lineas futuras
						futureItems[wlDict[item][0]] = item

				if futureItems != {}:
					#Se reemplaza el mayor del diccionario de lineas futuras, es decir el que será
					#el menos usado en el futuro, por la linea actual de la tupla de lineas
					cache.discard(futureItems[max(futureItems)])
					cache.add(lines[i])
					misses += 1
					#print cache

	return misses

'''Function LRU'''
def lruAlg(lines,cacheSize):
	
	counter = 0 #contador incrementará automaticamente
	misses=0
	#cache = set([]) 
	cache = {}
	contDict = {}
	
	for line in lines:
		
		
		if line not in cache:
			
			if(len(cache) < cacheSize):
				cache[line]=counter
				contDict[counter]=line
				#contDict[n] = counter
				counter+= 1
				misses+= 1
				
			else:
				#tomaré el primer elemento del diccionario contDict clave(desde lines)->valor(contDict) como minimo para el reemplazo
				minimum = min(contDict)		
				del cache[contDict[minimum]]
				del contDict[minimum]
				cache[line]=counter
				contDict[counter] = line
				counter+= 1
				misses+= 1	
				
		else:
			del contDict[cache[line]]
			cache[line]=counter
			contDict[counter]=line
			counter+=1
			#print stack
	#print misses
					
	return misses				


#Algoritmo clock			
def clockAlg(lines, cacheSize):
	misses=0
	DicBit={}
	DicDatos={}
	DatoCache=[]
	apuntador=1
	lineas=len(lines)


	for j in xrange(cacheSize):
		DicBit[j+1]=0
	for i in xrange(lineas):
		
		if lines[i] in DatoCache:
			pos=(DatoCache.index(lines[i]))+1
			if DicBit[pos]==0:
				DicBit[pos]=1
		else:
			misses+=1

			if DicBit[apuntador] == 0:
					DicBit[apuntador]=1
					if len(DatoCache) < cacheSize:
						DatoCache.append(lines[i]) 
						DicDatos[apuntador]=lines[i]
						if apuntador < cacheSize:
							apuntador+=1
						else:
							apuntador=1
					else:
						DatoCache.remove(DicDatos[apuntador])
						DicDatos[apuntador]=lines[i]
						DatoCache.insert(apuntador-1,lines[i])
						if apuntador < cacheSize:
							apuntador+=1
						else:
							apuntador=1

			else:
					while (lines[i] in DatoCache)== False:
						if DicBit[apuntador]==1:
							DicBit[apuntador]=0
							if apuntador < cacheSize:
								apuntador+=1
							else:
								apuntador=1
						else:
							DatoCache.remove(DicDatos[apuntador])
							DicDatos[apuntador]=lines[i]
							DicBit[apuntador]=1
							DatoCache.insert(apuntador-1, lines[i])
							if apuntador < cacheSize:
								apuntador+=1
							else:
								apuntador=1
	return misses






#Obtencion de argumentos de la linea de comandos
wlFile = sys.argv[1]
policy = sys.argv[2]
cacheSize = int(sys.argv[3])

with open(wlFile,"r") as f:
	lines = f.readlines()
#Tranformacion del arreglo de lineas a tupla, para acelerar acceso a los datos
lines = tuple(lines)

print "\nEvaluando una caché",policy,"con",cacheSize,"entradas."
print "Procesando...\n"

if(policy == "OPTIMO" or policy == "ÓPTIMO" or policy == "optimo" or policy == "óptimo"):
	
	
	misses = optimumAlg(lines, cacheSize)
if(policy == "LRU" or policy == "lru"):
	misses = lruAlg(lines,cacheSize)
	#misses = lruAlg(lines, cacheSize)

if(policy == "clock" or policy == "Clock" or policy == "Clock"):
	misses = clockAlg(lines, cacheSize)
print "Resultados:"
print "\tMiss rate: ",((float(misses)/len(lines))*100),"%  (",misses,"misses de",len(lines),"referencias ).\n"
