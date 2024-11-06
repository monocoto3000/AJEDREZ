import xml.etree.ElementTree as ET

class MaquinaTuring:
    def __init__(self, xml_file):
        self.estados = {}
        self.transiciones = []
        self.estado_inicial = None
        self.estado_final = None
        
        self.maquina(xml_file)

    def maquina(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
                
        automaton = root.find('automaton')
        
        for estado in automaton.findall('state'):
            estado_id = estado.get('id')
            es_inicial = estado.find('initial') is not None
            es_final = estado.find('final') is not None
            self.estados[estado_id] = (es_inicial, es_final)
            if es_inicial:
                self.estado_inicial = estado_id
            if es_final:
                self.estado_final = estado_id

        for transicion in automaton.findall('transition'):
            origen = transicion.find('from').text
            lee = transicion.find('read').text if transicion.find('read') is not None else ''  
            escribe = transicion.find('write').text if transicion.find('write') is not None else ''
            direccion = transicion.find('move').text if transicion.find('move') is not None else 'S'
            destino = transicion.find('to').text
            self.transiciones.append((origen, lee, escribe, direccion, destino))

    def validarCadena(self, cinta):
        cinta = list(cinta)  
        posicion = 0
        estado_actual = self.estado_inicial
        resultados = []

        while True:
            if posicion < 0:  
                cinta.insert(0, ' ')  
                posicion = 0
            elif posicion >= len(cinta):  
                cinta.append(' ') 
            
            simbolo = cinta[posicion] if posicion < len(cinta) else ' ' 
            transicion = next((t for t in self.transiciones if t[0] == estado_actual and t[1] == simbolo), None)

            cinta_aux = ''.join(cinta)

            resultados.append((cinta_aux, posicion, estado_actual))  

            if transicion:
                estado_actual = transicion[4]
                cinta[posicion] = transicion[2]

                if transicion[3] == 'R':
                    posicion += 1
                elif transicion[3] == 'L':
                    posicion -= 1
                elif transicion[3] == 'S':
                    pass  

                if self.estados[estado_actual][1]:  
                    resultados[-1] = (cinta_aux, posicion, "Cadena válida :D")  
                    break
            else:
                resultados[-1] = (cinta_aux, posicion, "Cadena no válida D:")  
                break

        return resultados
