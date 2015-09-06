#encoding: utf8
import sys


#Funcion de Algoritmo Optimo
def optimumAlg(lines, cacheSize):
	wlDict = {}
	wlSize = len(lines)	
	for i in xrange(wlSize):
		if lines[i] not in wlDict:
			wlDict[lines[i]] = [i]
		else:
			wlDict[lines[i]].append(i)

	for line in wlDict:
		wlDict[line].append(sys.maxint)

	cache = {}
	futureItems = {}
	misses = 0

	for i in xrange(wlSize):
		print i
		wlDict[lines[i]].remove(i)
		nextTime = wlDict[lines[i]][0]
		if lines[i] not in cache:
			misses += 1			
			if len(cache) < cacheSize:
				futureItems[nextTime] = lines[i]
				cache[lines[i]] = nextTime
			else:
				maxItemPos = max(futureItems)
				del cache[futureItems[maxItemPos]]
				del futureItems[maxItemPos]
				cache[lines[i]] = nextTime
				futureItems[nextTime] = lines[i]
		else:
			del futureItems[cache[lines[i]]]
			futureItems[nextTime] = lines[i]
			cache[lines[i]] = nextTime

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
policy = sys.argv[2].upper()
cacheSize = int(sys.argv[3])

with open(wlFile,"r") as f:
	lines = f.readlines()
#Tranformacion del arreglo de lineas a tupla, para acelerar acceso a los datos
lines = tuple(lines)

print "\nEvaluando una caché",policy,"con",cacheSize,"entradas."
print "Procesando...\n"

if(policy == "OPTIMO"):	
	misses = optimumAlg(lines, cacheSize)
	
if(policy == "LRU"):
	misses = lruAlg(lines,cacheSize)

if(policy == "CLOCK"):
	misses = clockAlg(lines, cacheSize)
	
print "Resultados:"
print "\tMiss rate: ",((float(misses)/len(lines))*100),"%  (",misses,"misses de",len(lines),"referencias ).\n"
