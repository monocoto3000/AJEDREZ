import xml.etree.ElementTree as ET

class MaquinaTuring:
    def __init__(self, xml_file):
        self.estados = {}
        self.transiciones = {}  
        self.estado_inicial = None
        self.estado_final = None
        # self.max_pasos = 3000  
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
            lee = transicion.find('read')
            lee = lee.text if lee is not None and lee.text else ' '
            
            clave = (origen, lee)
            
            escribe = transicion.find('write')
            escribe = escribe.text if escribe is not None and escribe.text else lee
            
            direccion = transicion.find('move')
            direccion = direccion.text if direccion is not None and direccion.text else 'S'
            
            destino = transicion.find('to').text
            
            self.transiciones[clave] = (escribe, direccion, destino)

    def validarCadena(self, cinta):
        cinta = list(cinta + ' ' * 3)  
        posicion = 0
        estado_actual = self.estado_inicial
        resultados = []
        output = []
        # pasos = 0

        configuraciones_visitadas = set()

        while True:
            # pasos += 1
            
            if posicion < 0:
                cinta.insert(0, ' ')
                posicion = 0
            elif posicion >= len(cinta):
                cinta.append(' ')

            simbolo = cinta[posicion]
            clave = (estado_actual, simbolo)

            configuracion = (estado_actual, posicion, ''.join(cinta))

            if configuracion in configuraciones_visitadas:
                resultados.append(('Ciclo infinito detectado', posicion, "error"))
                break

            configuraciones_visitadas.add(configuracion)

            cinta_visible = ''.join(cinta)
            resultados.append((cinta_visible, posicion, estado_actual))

            transicion = self.transiciones.get(clave) or self.transiciones.get((estado_actual, ' '))

            if not transicion:
                resultados.append((cinta_visible, posicion, "no valido"))
                break

            escribe, direccion, nuevo_estado = transicion
            
            if escribe != ' ':
                cinta[posicion] = escribe
                output.append(escribe)

            estado_actual = nuevo_estado
            if direccion == 'R':
                posicion += 1
            elif direccion == 'L':
                posicion -= 1

            if estado_actual == self.estado_final:
                resultados.append((cinta_visible, posicion, "valido"))
                break

        # else: 
        #     resultados.append(('Límite de pasos excedido', posicion, "error"))

        return resultados