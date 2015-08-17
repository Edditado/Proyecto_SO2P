#encoding: utf8
import sys


def optimumAlg(lines, cacheSize):
	cache = []
	misses = 0

	for i1 in range(0,len(lines)):
		#print i1
		if not lines[i1] in cache:
			if len(cache) < cacheSize:
				cache.append(lines[i1])
				misses += 1
				#print cache
			else:
				farIndex = None
				futureLines = lines[i1+1:]
				for i2 in range(0,len(cache)):
					if not cache[i2] in futureLines:
						cache[i2] = lines[i1]
						misses += 1
						#print cache
						farIndex = None
						break
					else:
						ind = futureLines.index(cache[i2])
						if ind > farIndex:
							farIndex = ind

				if farIndex is not None:
					cache[cache.index(futureLines[farIndex])] = lines[i1]
					misses += 1
					#print cache

	return misses





wlFile = sys.argv[1]
policy = sys.argv[2]
cacheSize = int(sys.argv[3])

file = open(wlFile,"r")
lines = file.readlines()
file.close()

print "\nEvaluando una caché",policy,"con",cacheSize,"entradas."
print "Procesando...\n"

if(policy == "OPTIMO" or policy == "ÓPTIMO" or policy == "optimo" or policy == "óptimo"):
	misses = optimumAlg(lines, cacheSize)

print "Resultados:"
print "\tMiss rate: ",((float(misses)/len(lines))*100),"%  (",misses,"misses de",len(lines),"referencias ).\n"