#encoding: utf8
import sys


#Funcion de Algoritmo Optimo
def optimumAlg(lines, cacheSize):
	wlDict = {}
	i = 0
	for line in lines:
		if line not in wlDict:
			wlDict[line] = [i]
		else:
			wlDict[line].append(i)
		i += 1
	
	maxInt = sys.maxint
	for line in wlDict:
		wlDict[line].append(maxInt)

	cache = {}
	futureItems = {}
	misses = 0
	i = 0
	for line in lines:
		wlDict[line].remove(i)
		nextTime = wlDict[line][0]
		if line not in cache:
			misses += 1			
			if len(cache) < cacheSize:
				futureItems[nextTime] = line
				cache[line] = nextTime
			else:
				maxItemPos = max(futureItems)
				del cache[futureItems[maxItemPos]]
				del futureItems[maxItemPos]
				cache[line] = nextTime
				futureItems[nextTime] = line
		else:
			del futureItems[cache[line]]
			futureItems[nextTime] = line
			cache[line] = nextTime
		
		i += 1

	return misses



'''Function LRU'''
def lruAlg(lines,cacheSize):
	
	counter = 0
	misses=0
	cache = {}
	contDict = {}
	
	for line in lines:
				
		if line not in cache:
			
			if(len(cache) < cacheSize):
				cache[line]=counter
				contDict[counter]=line
				counter+= 1
				misses+= 1
				
			else:
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
					
	return misses				



#Algoritmo clock			
def clockAlg(lines, cacheSize):
	misses=0
	DicBit={}
	DicDatos={}
	DatoCache={}
	apuntador=1
	lineas=len(lines)


	for j in xrange(cacheSize):
		DicBit[j+1]=0



	for i in xrange(lineas):
		
		
		if DatoCache.has_key(lines[i]):
			pos=DatoCache[lines[i]]
			if DicBit[pos]==0:
				DicBit[pos]=1
		else:
			misses+=1

			if DicBit[apuntador] == 0:
					DicBit[apuntador]=1
					if len(DatoCache) < cacheSize:
						DatoCache[lines[i]]=apuntador
						DicDatos[apuntador]=lines[i]
						
					else:
						del DatoCache[DicDatos[apuntador]]
						DicDatos[apuntador]=lines[i]
						DatoCache[lines[i]]=apuntador
					
					if apuntador < cacheSize:
						apuntador+=1
					else:
						apuntador=1



			else:	
					
					
					while (DicBit[apuntador]==1):
						
						DicBit[apuntador]=0
						if apuntador < cacheSize:
							apuntador+=1
						else:
							apuntador=1
							
						
					if (DicBit[apuntador]==0):
						del DatoCache[DicDatos[apuntador]]
						DicDatos[apuntador]=lines[i]
						DicBit[apuntador]=1
						DatoCache[lines[i]]=apuntador
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
print "\tMiss rate: %.2f%% (%d misses de %d referencias)\n" % ( ((float(misses)/len(lines))*100), misses , len(lines) )
