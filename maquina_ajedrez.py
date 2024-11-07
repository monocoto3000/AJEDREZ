import xml.etree.ElementTree as ET

class MaquinaTuring:
    def __init__(self, xml_file):
        self.estados = {}
        self.transiciones = {}  # Cambiado a diccionario para búsqueda más eficiente
        self.estado_inicial = None
        self.estado_final = None
        self.max_pasos = 10000  # Límite de pasos para evitar bucles infinitos
        self.maquina(xml_file)

    def maquina(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        automaton = root.find('automaton')
        
        # Procesar estados
        for estado in automaton.findall('state'):
            estado_id = estado.get('id')
            es_inicial = estado.find('initial') is not None
            es_final = estado.find('final') is not None
            self.estados[estado_id] = (es_inicial, es_final)
            if es_inicial:
                self.estado_inicial = estado_id
            if es_final:
                self.estado_final = estado_id

        # Optimizar estructura de transiciones
        for transicion in automaton.findall('transition'):
            origen = transicion.find('from').text
            lee = transicion.find('read')
            lee = lee.text if lee is not None and lee.text else ' '
            
            # Crear clave compuesta para búsqueda rápida
            clave = (origen, lee)
            
            escribe = transicion.find('write')
            escribe = escribe.text if escribe is not None and escribe.text else lee
            
            direccion = transicion.find('move')
            direccion = direccion.text if direccion is not None and direccion.text else 'S'
            
            destino = transicion.find('to').text
            
            # Almacenar la transición en el diccionario
            self.transiciones[clave] = (escribe, direccion, destino)

    def validarCadena(self, cinta):
        # Convertir la cinta a una lista y añadir espacio extra limitado
        cinta = list(cinta + ' ' * 3)  # Añadimos solo 3 espacios extra
        posicion = 0
        estado_actual = self.estado_inicial
        resultados = []
        output = []
        pasos = 0

        while pasos < self.max_pasos:
            pasos += 1
            
            # Expandir cinta solo cuando sea necesario
            if posicion < 0:
                cinta.insert(0, ' ')
                posicion = 0
            elif posicion >= len(cinta):
                cinta.append(' ')

            simbolo = cinta[posicion]
            clave = (estado_actual, simbolo)
            
            # Obtener transición del diccionario (más eficiente)
            transicion = self.transiciones.get(clave) or self.transiciones.get((estado_actual, ' '))

            # Crear una vista de la cinta actual de manera eficiente
            cinta_visible = ''.join(cinta)
            resultados.append((cinta_visible, posicion, estado_actual))

            if not transicion:
                resultados.append((cinta_visible, posicion, "no valido"))
                break

            escribe, direccion, nuevo_estado = transicion
            
            # Actualizar cinta y guardar output solo si es necesario
            if escribe != ' ':
                cinta[posicion] = escribe
                output.append(escribe)

            # Actualizar estado y posición
            estado_actual = nuevo_estado
            if direccion == 'R':
                posicion += 1
            elif direccion == 'L':
                posicion -= 1

            if estado_actual == self.estado_final:
                resultados.append((cinta_visible, posicion, estado_actual, "valido"))
                break

        else:  # Si se alcanza el límite de pasos
            resultados.append(('Límite de pasos excedido', posicion, estado_actual, "error"))

        return resultados