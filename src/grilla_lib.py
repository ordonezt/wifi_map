import numpy as np
from nav_msgs.msg import OccupancyGrid

class Grilla:

    def __init__(self, dimension_x, dimension_y, resolucion):
        self.dimension_x = dimension_x
        self.dimension_y = dimension_y
        self.resolucion = resolucion

        # self.grilla = np.array(([-float('inf') for i in range(dimension_x)],\
        #                         [-float('inf') for i in range(dimension_y)]))
        self.grilla = np.ndarray((dimension_x, dimension_y), buffer=np.zeros((dimension_x, dimension_y), dtype=np.int), dtype=np.int)
        self.grilla.fill(-float('inf'))

    def agregar_punto(self, potencia, x, y):
        i, j = posicion2indice(x, y, self.resolucion)
        #if (i, j) != (i_anterior, j_anterior):
        if i < self.dimension_x and j < self.dimension_y:
            self.grilla[i, j] = potencia
        #    (i_anterior, j_anterior) = (i, j)

    def grilla2occupancy_grid(self):
        mapa_msg = OccupancyGrid()
        mapa_msg.header.frame_id = 'mapa'
        mapa_msg.info.resolution = self.resolucion
        mapa_msg.info.width = self.dimension_x
        mapa_msg.info.height = self.dimension_y
        mapa_msg.data = range(self.dimension_x * self.dimension_y)

        for i in range(len(self.grilla.flat)):
            mapa_msg.data[i] = self.grilla.flat[i]
        
        return mapa_msg

def posicion2indice(x, y, resolucion):
    return (int(x // resolucion), int(y // resolucion))