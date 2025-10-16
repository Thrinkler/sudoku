# De resolver Sudokus a hacerlos: El generador de Sudokus

## Resumen
En las siguientes lineas se presentarán 3 algoritmos distintos: 
- Un algoritmo que resuelve cualquier sudoku de $n^2 \times n^2$ dado, revisando al mismo tiempo si puede ser resuelto.
- Un algoritmo que revisa cuántas soluciones tiene un sudoku de $n^2 \times n^2$  dado.
- Un generador de sudokus de $n^2 \times n^2$.
  
Para esto, se utilizará python, utilizando clases para clasificar los algoritmos como Creador y Solucionador, de tal manera
que los algoritmos relacionados puedan utilizar las funciones que comparten unos entre otros, y poder usar los algoritmos como
objetos para una mejor comprensión de lo que hace cada uno de ellos. La única librería que se utilizará será random.

Todos los algoritmos serán iterativos, lo que nos ayudará a comprender mejor el proceso de cada uno de ellos.

## Introducción.

Cuando uno piensa en un sudoku, piensa muchas veces en un cúmulo místico de números en una reja, y lo más curioso es que con
tan solo esos números aparentemente aleatorios, y con tan solo siguiendo unas simples reglas, se puede generar uno y solo un

1. No se puede repetir un número en un mismo renglón
2. No se puede repetir un número en una misma columna
3. No se puede repetir un número en su cuadrante

En este texto les platicaré toda la travesía por la que pasé para producir los tres algoritmos, así como todo mi proceso de pensamiento para llegar a los mismos.

Pero empecemos por lo primero: qué pasó antes de tener la idea?

## Trasfondo

Aunque el protagonista de este artículo es el conjunto de los 3 algoritmos, primero permítanme platicarles acerca de los primeros acercamientos que tuve a la automatización de la solución de los sudokus.

Todo empieza en 2019, cuando empezaba ya con proyectos de Python pero ni siquiera sabía que eran las clases, pero también cuando mi padre estaba pasando varios de sus antiguos códigos a Python. Uno de esos códigos era un solucionador automático de los sudokus, optimizado a más no poder, totalmente iterativo, y aparte adjunto tenía un PDF con la explicación completa de cada paso en detalle.

Yo, pensando que por haber estado programando ya un tiempo le entendería a sus códigos completos, le eché un vistazo... Vi la palabra "def", no sabía qué significaba, y cerré todo el archivo tan rápido como si fuera un virus...

Al final mi padre me explicó qué eran las funciones, y que servían para "no repetir código", y de ahí continúa una historia donde usaba funciones para todo pero todavía no conocía acerca de las clases, aunque esa es otra historia...

En fin, pasa el tiempo, y mi pa empieza a utilizar ese algoritmo con un sudoku de $16 \times 16$ para probar la rapidez de las computadoras al correr un programa de python, pero nunca tuve la idea de verlo, ni siquiera de revisarlo. Hasta donde sabía, la creación de los sudokus abarcaban mucho tiempo, los algoritmos para resolverlos eran de tiempos gigantes, y aparte querían que fuera una solución única... Pero así como muchas cosas en la vida, esos temas, esos momentos... regresan a tí.

## El origen de la idea

Y fue cuando, en una clase de Modelado de mi carrera, el profesor presentó un algoritmo de resolución de sudokus. Ahí, terminando la presentación, se le ocurrió preguntar por un algoritmo para crear sudokus. Como nadie le respondió, propuso: "El que haga un algoritmo que genere sudokus, tendrá un punto extra sobre la materia... o al menos contará como un proyecto de clase".

Yo, que unas semanas antes saqué un 11/25 en el primer examen, que en el primer proyecto en el README se me olvidó cambiar la linea para correr el código (gracias módulos de python por ya no correr como un archivo), pero también que ya me estaba sintiendo lo suficientemente seguro de mí mismo como para enfrentarme a un ejercicio así, me propuse a hacerlo, es más, si ya había hecho mi proyecto de un ecosistema artificial [A-Ecosystem](https://github.com/Thrinkler/A-Ecosystem), qué me impediría tratar de resolver este problema. "Es más," pensé. "Lo entregaré en dos días, y como tengo exámen, lo empezaré mañana" 

Y bueno, les tengo que admitir que enfrenté a este proyecto con una arrogancia que fue bajando mientras más fallas salían a la luz, pero ya lo verán en las siguientes lineas.

## La idea

La idea era muy sencilla. Utilizando un solucionador de sudoku encima de una "plantilla de sudokus" (una matríz sin ningún dato dentro), generaría una respuesta de sudoku totalmente aleatoria y nueva. Luego, le iría quitando aleatoriamente uno de los datos a la respuesta del sudoku, y pasaría un programa que verifique que solo hay una solución. Luego de eso, repetiría el proceso de quitar y verificar una cantidad de veces hasta que llegara a la menor cantidad de datos y que ya no pudiera quitarle más.

Eso se escuchaba fácil, tan solo necesitaba mi propio solucionador para poder controlar la aleatoriedad de los datos, y el verificador de soluciones... ¿Qué podría salir mal? 

## Parte 1: El solucionador de Sudokus.

Antes de seguir la historia, vamos a explicar el solucionador paso por paso.

Primero que nada, el ```__init__``` es fácil de explicar:
    
    def __init__(self, sudoku: list[list[int]]) -> None:
            self.sudoku = [line[:] for line in sudoku]
            self.unsolved_sudoku = [line[:] for line in sudoku]
            self.box_size = int(len(sudoku)**0.5)

Dado un sudoku dado, lo copiamos, aparte obtenemoos el tamaño de los cuadrantes. 

Luego sigamos con  ```empty_cells()```

    def empty_cells(self):
            empty_cell = []
            for i in range(len(self.sudoku)):
                for j in range(len(self.sudoku)):
                    if self.sudoku[i][j] == 0:
                        empty_cell.append([i,j])
            
            return empty_cell
Aquí lo único que hacemos es pasar a través de todo el sudoku y guardamos en una lista las coordenadas de todos los vacíos.

Despues, ```posible_values()```

    def posible_values (self, int_row:int,int_column:int):
            row = set(self.sudoku[int_row])
            column = set([r[int_column] for r in self.sudoku])
    
            start_row = self.box_size* (int_row//self.box_size)
            start_column = self.box_size* (int_column//self.box_size)
            
            box = set()
            for r in range(start_row, start_row + self.box_size):
                for c in range(start_column, start_column + self.box_size):
                    box.add(self.sudoku[r][c])
            
            all_digits = row.union(column).union(box) -set([0])
            return (set(range(1,len(self.sudoku)+1))-all_digits)

Esta utiliza la magia que tienen los sets en python de que al unirlos, no se repiten los valores.
Lo que hace es tomar todos los números de la fila, columna y cuadrante distintos de 0, los une en un set, y regresa el complemento de ese set sin contar el 0.

 Y por último y más importante, ```solve_sudoku()```

    def solve_sudoku(self):
      self.sudoku = [line[:] for line in self.unsolved_sudoku]
      memory = []
      empty_cell = self.empty_cells()
      i = 0
      while i< len(empty_cell):
          x,y = empty_cell[i]
          pos_values = list(self.posible_values(x,y))
          random.shuffle(pos_values)
          
          if len(pos_values) == 0: # Si no hay soluciones, nos regresamos uno
              if not memory: return False # Si no hay donde regresar, no hay soluciones
              self.sudoku,pos_values,i = memory.pop() #Regresamos y continuamos
              x,y = empty_cell[i]
          self.sudoku[x][y] = pos_values.pop()

          if pos_values:
              memory.append([[line[:] for line in self.sudoku],pos_values,i])
              
          i+=1
      return True  
Primero limpiamos el sudoku con ```self.sudoku = [line[:] for line in self.unsolved_sudoku]```, por si ya se había resuelto.
Aquí utilizamos ```memory``` como la parte más importante del código. Esta va a guardar el sudoku en el momento después de poner nuestra elección de numero, junto con la lista de números que no hemos probado en esa posición, y un indicador para saber qué celda vacía fue cambiada. 

Luego obtenemos ```self.empty_cell()``` y la guardamos para no tenerla que calcular cada vez que hacemos una iteración. Iniciamos el indicador al inicio de la lista con ```i=0```, y empezamos a tratar de resolver.

Calculamos los posibles valores para la posición del valor vacío. Esos valores los revolvemos, y empezamos revisando que la celda tenga posibles movimientos. De no ser así, entonces debemos regresarnos en la memoria. (Si no hay memoria, el sudoku no tiene solución ya que no hay ninguna manera de que podamos regresar a la anterior versión ni tampoco manera de seguir adelante.) Volvemos a revisar la posición que nos da el indicador, y ponemos el siguiente valor posible.

Por último, si es que siguen habiendo valores posibles, guardamos el sudoku hasta esa posición construida, los valores posibles y el indicador. Luego incrementamos el indicador para irnos con la siguiente celda vacía, con lo cual, si ya es igual de grande que la lista de celdas vacías, entonces quiere decir que ya completó el sudoku, con lo cual regresa verdadero.



Notese que siempre estamos modificando el sudoku obtenido de la clase, con lo que tan solo tendremos que llamar a ese dato al final para ver qué tantas soluciones hay


Cuando el profesor nos dió el desafío, entré rápidamente a los archivos compartidos por mi padre y encontré el código que él había construido. Algo que mi padre sabe hacer es un algoritmo muy corto, pero al mismo tiempo, todas sus variables son puras letras, así que no entendía con tan solo leer el código qué estaba pasando.



