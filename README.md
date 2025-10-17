# De resolver Sudokus a hacerlos: El generador de Sudokus

## Resumen
En las siguientes lineas se presentarán 3 algoritmos distintos: 
- Un algoritmo que resuelve cualquier sudoku de $n^2 \times n^2$ dado, revisando al mismo tiempo si puede ser resuelto.
- Un algoritmo que revisa cuántas soluciones tiene un sudoku de $n^2 \times n^2$  dado.
- Un generador de sudokus de $n^2 \times n^2$.

Todos estos algoritmos serán totalmente iterativos, sin ningún tipo de recursión utilizada. Esto nos ayudará a entender mejor lo que pasa detrás de cada algoritmo, y poder guardar solo los datos necesarios.
Para esto, se utilizará python, utilizando clases para clasificar los algoritmos como Creador y Solucionador, de tal manera
que los algoritmos relacionados puedan utilizar las funciones que comparten unos entre otros, y poder usar los algoritmos como
objetos para una mejor comprensión de lo que hace cada uno de ellos. La única librería que se utilizará será random.

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
```python  
    def __init__(self, sudoku: list[list[int]]) -> None:
            self.sudoku = [line[:] for line in sudoku]
            self.unsolved_sudoku = [line[:] for line in sudoku]
            self.box_size = int(len(sudoku)**0.5)
```
Dado un sudoku dado, lo copiamos, aparte obtenemoos el tamaño de los cuadrantes. 

Luego sigamos con  ```empty_cells()```
```python
    def empty_cells(self):
            empty_cell = []
            for i in range(len(self.sudoku)):
                for j in range(len(self.sudoku)):
                    if self.sudoku[i][j] == 0:
                        empty_cell.append([i,j])
            
            return empty_cell
```
Aquí lo único que hacemos es pasar a través de todo el sudoku y guardamos en una lista las coordenadas de todos los vacíos.

Despues, ```posible_values()```

```python
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
```
Esta utiliza la magia que tienen los sets en python de que al unirlos, no se repiten los valores.
Lo que hace es tomar todos los números de la fila, columna y cuadrante distintos de 0, los une en un set, y regresa el complemento de ese set sin contar el 0.

 Y por último y más importante, ```solve_sudoku()```
```python
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
```
Primero limpiamos el sudoku con ```self.sudoku = [line[:] for line in self.unsolved_sudoku]```, por si ya se había resuelto.
Aquí utilizamos ```memory``` como la parte más importante del código. Esta va a guardar el sudoku en el momento después de poner nuestra elección de numero, junto con la lista de números que no hemos probado en esa posición, y un indicador para saber qué celda vacía fue cambiada. 

Luego obtenemos ```self.empty_cell()``` y la guardamos para no tenerla que calcular cada vez que hacemos una iteración. Iniciamos el indicador al inicio de la lista con ```i=0```, y empezamos a tratar de resolver.

Calculamos los posibles valores para la posición del valor vacío. Esos valores los revolvemos, y empezamos revisando que la celda tenga posibles movimientos. De no ser así, entonces debemos regresarnos en la memoria. (Si no hay memoria, el sudoku no tiene solución ya que no hay ninguna manera de que podamos regresar a la anterior versión ni tampoco manera de seguir adelante.) Volvemos a revisar la posición que nos da el indicador, y ponemos el siguiente valor posible.

Por último, si es que siguen habiendo valores posibles, guardamos el sudoku hasta esa posición construida, los valores posibles y el indicador. Luego incrementamos el indicador para irnos con la siguiente celda vacía, con lo cual, si ya es igual de grande que la lista de celdas vacías, entonces quiere decir que ya completó el sudoku, con lo cual regresa verdadero.

Notese que siempre estamos modificando el sudoku obtenido de la clase, con lo que tan solo tendremos que llamar a ese dato al final para ver el sudoku resuelto.

---


La clase donde nos platicaron del proyecto fue un lunes. Cuando el profesor nos dió el desafío, entré rápidamente a los archivos compartidos por mi padre y encontré el código que él había construido. Lo encontré y lo puse a un lado para empezarlo después, de cualquier manera todavía tenía unas cuantas cosas que hacer, y pensé que podía hacerlo todo tan rápido que no me tomaría más de una tarde. Así que lo dejé aplazado un día. El martes se veía un buen día para empezarlo, pero para nada iba a dejar de ir al gimnasio, así que en cuanto llegue a mi casa, tomé una taza de café, comí, y luego entrené, me habían dado ya las 6:50 de la noche.

Empecé a las 7 de la noche del martes. Consideraba que era un buen tiempo pues la clase empezaría a las 12 del día siguiente. Y yo, todo emocionado, empiezo a leer los archivos, hacerme una idea mental, y empezar a programar. Algo que mi padre sabe hacer es un algoritmo muy corto, pero al mismo tiempo, casi no nombra a sus variables, solo las nombra con puras letras, así que no entendía con tan solo leer el código qué estaba pasando de una manera intuitiva. Eso no evitó que al menos tratara de entender el código, y luego de más de una media hora de leer 20 lineas de código una y otra vez, entendí por fín lo que hacía. Al final, toda la ciencia era guardar en una memoria al sudoku, con sus posibles soluciones y las posiciones del número eliminado. 

Y de pronto me pasó algo... A veces me pasa que comprendo algo, pero a la hora de programarlo, subestimo al algoritmo, y ni siquiera le presto atención a lo que estoy haciendo. Esta vez fue una de esas veces, y realmente me tardé más de lo que debía porque ni siquiera quería revisar qué era lo que no funcionaba cada que había un error. Pasaba un error de indice fuera de rango, lo arreglaba evitando que llegara con un if. Había un problema con el backtracking, le ponía cada vez más datos para que lograra funcionar. Llegó un momento en que esa función fue de 50 lineas, Y SEGUÍA SIN FUNCIONAR.

Total que por fin, ya a las 8:30 de la noche, me decido a por fin leer todo lo que había escrito desde cero, como si me estuviera explicando a mí mismo qué hace cada parte. De esa manera, quité código que no se necesitaba, ifs que parecía que evitaban problemas pero que al final causaban más problemas, y entonces fue cuando me di cuenta de algo: La función de valores posibles estaba mal calculada...

Casi tiro mi computadora por la ventana. Directamente le vuelvo a copiar a mi padre el cálculo del cuadrante para que ya no haya problema, y procede el algoritmo a funcionar.

1 hora y 30 minutos... tratando de hacer y arreglar un código cuyo problema no era en sí ese código, sino una función que había hecho sin revisar nada. Me sentí como si hubiera tratando de construir una resortera y me hubiera tardado 10 horas.

Y lo peor de todo: Este código solo lo necesitaba para empezar a programar el contador de soluciones...



## Parte 2: El contador de soluciones

De nuevo explicaremos el código antes de seguir con la historia.

Dado que el contador de soluciones está en la misma clase que el solucionador, todos los métodos usados ya se explicaron anteriormente, por lo que pasaremos a explicar únicamente la clase ```find_all_solutions()```
```python
    def find_all_solutions(self):
        self.sudoku = [line[:] for line in self.unsolved_sudoku]
        solutions_count = 0
        memory = []
        empty_cell = self.empty_cells()

        i = 0
        

        x,y = empty_cell[i]
        pos_values = list(self.posible_values(x,y))
        has_found = False
        while True:
            
            if i < len(empty_cell):
                x,y = empty_cell[i]
                pos_values = list(self.posible_values(x,y))
                random.shuffle(pos_values)

            if i== len(empty_cell) or len(pos_values) == 0: # Si hay una solución, la contamos y regresamos
                if i == len(empty_cell): 
                    solutions_count+=1
                if not memory: return solutions_count # Si no hay donde regresar, encontramos todas.
                
                self.sudoku,pos_values,i = memory.pop()
                x,y = empty_cell[i]
                
            self.sudoku[x][y] = pos_values.pop()
            if len(pos_values) >0:
                memory.append([[line[:] for line in self.sudoku],pos_values,i])
                
            
            i+=1
```
Notemos que estamos usando casi el mismo código que el solucionador, aunque con unas distintas diferencias que explicaremos una por una.

Para empezar, definimos ```x,y``` y ```pos_values``` antes para que el interprete de python sepa qué son cada uno de ellos. Esto porque ya cuando lo está solucionando, metemos a un ```if``` todo eso para que no calcule una posición cuando ya está completo el sudoku. En vez de eso, si está completo, tratamos a que está completo como si fuera un caso incorrecto, tan solo sumando 1 al recuento de soluciones. Se sigue el algoritmo del solucionador exactamente igual, con la única diferencia de que no regresa nada al terminar el ciclo.


---

Sigamos con la historia. Yo ya estaba muy cansado cuando por fin pudo resolver un sudoku el solucionador, pero efectivamente, el contador de soluciones era el corazón del algoritmo que había planeado para generar sudokus. No podía parar cuando apenas había empezado.

Descansé una media hora mientras cenaba, y a las 9:00 de la noche, luego de seguir con la espina, decidí continuar. Ahora el problema era más sencillo: Dado el sudoku completo, tan solo marcalo como incorrecto y regresate...

Pero ¿qué significa completo? Antes de hacer el código del solucionador, tenía en dos ifs qué pasaba si no encontraba una posible respuesta y qué pasaba si sí, pero antes, en vez de usar un iterador sobre la lista de vacíos, las eliminaba y guardaba cómo estaba después.

Lo primero que hice para el caso donde estuviera completo fue hacer un nuevo if con lo mismo que el caso donde estaba mal. Por alguna razón no funcionaba, tengo la teoría de que era porque primero ponía la respuesta correcta, luego me metía al de completarlo, me regresaba, pero como no había sumado la iteración del completo, entonces se desfazaba.

Ya eran las 9:30 de la noche. Realmente estaba cansado, así que decidí que el día siguiente sería muy bueno para continuar, de todas maneras me quedaban solo 14 horas y media para la clase. Podría continuarlo llegando a la facultad a las 8 de la mañana, y si me iba bien, lo terminaría a las 9.

Así que eso hice. A las 8 de la mañana del día siguiente seguí, y luego de una hora de leer, tratar de añadir partes y tratar de salvar mi código, terminé borrandolo y empezando desde cero. El solucionador tenía mucho código repetido que si se lo quitaba, se entendría mejor el algoritmo, y el contador de soluciones tenía un pegoste de un tercer caso que hacía que todo el código dejara de funcionar, así que arreglé el solucionador, copié el código de nuevo, y empecé de nuevo, ahora sabiendo algo muy claro: No voy a repetir código.

Fue ahí cuando puse la linea más clara, ```if i== len(empty_cell) or len(pos_values) == 0:```, donde tan solo le añadí el ```or len(pos_values) == 0``` para entender totalmente que ese código tenía que hacer lo mismo... Y seguía mandando error.

Seguía pasando un error, solo pasaba si terminaba, y era porque el iterador se volvía más grande de lo que debía si es que llegaba al máximo. Me tardé un poco tratando de entender el error, solucionarlo, y cuando ya por fin había entendido que no podía asignar a x,y si es que ya estaba completo el sudoku, le puse ese if a la primera parte, copié el código antes del iterador, y por fin funcionó.

Y lo había hecho, el corazón de mi proyecto, la parte fundamental para el generador de sudokus había llegado a su fin. Podía usar todo el tiempo que me quedaba para entrar a mi clase de probabilidad a las 10 de la mañana, tal vez incluso terminar el proyecto de una vez por todas... Tan solo eran... las 9:40.

## Parte 3: El generador

Aquí tenemos una nueva clase, la clase creator.

```python
def __init__(self, size = 3) -> None:
        self.size = size**2
```
Aquí tan solo definimos el tamaño de la matríz del sudoku con el tamaño de un cuadrante.

```python
def new_sudoku_ending(self):
        s = Solver([[0 for _ in range(self.size)]for _ in range(self.size)])
        s.solve_sudoku()
        return s.sudoku
```
Esta función lo único que hace es que el solucionador del sudoku resuelva un sudoku vacío. Dado que agarramos una de las posibilidades aleatoriamente, el final de todos los sudokus es aleatorio.

```python
def create_sudoku(self, max_clues=17):
        sudoku = self.new_sudoku_ending()

        clues = len(sudoku)* len(sudoku[0])
        pos_clues = [[[x,y] for x in range(0,len(sudoku))]for y in range(0,len(sudoku))]

        p_clues = []
        not_watched_clues = []
        for line in pos_clues:
            p_clues += [i[:] for i in line]
            not_watched_clues += [i[:] for i in line]
        
        n =0

        while True:
            if len(not_watched_clues) == 0: #Si ya se probó quitar todos los números 
                return sudoku               #y hay más de una solución si los quitas, regresa el sudoku
            
            x,y = random.choice(not_watched_clues)
            removed_clue = sudoku[x][y]        
            sudoku[x][y] = 0
            not_watched_clues.remove([x,y])

            s = Solver(sudoku)
            if(s.find_all_solutions() == 1):
                clues-=1
                p_clues.remove([x,y])
                not_watched_clues = [line[:] for line in p_clues]

            else:
                sudoku[x][y] = removed_clue
                
            n+=1
            print(n, clues)
```
Aquí lo primero que hacemos es obtener uno de los finales del sudoku. Con ese vamos a operar.

Obtenemos el número de pistas que tiene el sudoku. Como está resuelto, el número de pistas es el tamaño de toda la matríz generada. De la misma manera, generamos todas las coordenadas de las claves, y las guardamos en dos arreglos distintos.

Inicamos la busqueda iterativa. Primero revisamos si es que hay pistas no vistas, si es que no las hay, quiere decir que ya no podemos quitar ninguna pista sin obtener más de una solución y regresamos el sudoku con menos pistas. En otro caso, tomamos de la lista de pistas no vistas, la quitamos de las que no hemos visto, y ponemos un 0 en ese lugar en el sudoku. Los 0 representan los lugares vacíos. Luego, con el sudoku ya cambiado, genera un solucionador para que revise cuántas posibles soluciones hay. Si solo tiene una solucion, sabemos que sin esa pista sigue teniendo una respuesta única, por lo que buscaremos de nuevo si se puede quitar otra pista. En otro caso, debemos de regresar la pista a su lugar.


### Bonus: Encontrar un sudoku con claves mínimas.

Aunque posteriormente haremos una extensión de este proyecto enfocado en algebra, donde demostraremos una manera de generar sudokus en base de una plantilla, podemos ver muy fácilmente que con nuestro anterior algoritmo estamos entrando a un "minimo local" en vez de un "minimo absoluto", donde, para un sudoku de $9 \times 9$, el número minimo de claves está entre 81 y 17 (demostrado en 2012 que 17 es el número mínimo de posibilidades para un sudoku de $9 \times 9$). Con pruebas prácticas, el número que he logrado llegar antes de no poder quitar más pistas es de 25 a 17, pero es frustrante llegar a 24 claves y no poder bajar de ahí, cuando anteriormente había llegado a 20. Así que refactoricé el algoritmo de creación con  un pequeño cambio:

```python
def create_min_sudoku(self, max_clues=17):
        sudoku = self.new_sudoku_ending()
        solved_sudoku = [line[:] for line in sudoku]

        clues = len(sudoku)* len(sudoku[0])
        pos_clues = [[[x,y] for x in range(0,len(sudoku))]for y in range(0,len(sudoku))]

        p_clues = []
        not_watched_clues = []
        for line in pos_clues:
            p_clues += [i[:] for i in line]
            not_watched_clues += [i[:] for i in line]
        n =0

        min_ret_sudoku = []
        min_clues = clues

        has_not_complete_one = True

        while clues > max_clues and (n<500 or has_not_complete_one):

            if len(not_watched_clues) == 0: #Si ya se probó quitar todos los números 
                if clues < min_clues:       #y hay más de una solución si los quitas
                    min_ret_sudoku = [line[:] for line in sudoku]
                    min_clues = clues
                has_not_complete_one = False
                a,b = random.randint(0,len(sudoku)-1),random.randint(0,len(sudoku)-1)

                for line in [[(a+i)%len(sudoku),(b+random.randint(0,len(sudoku)-1))%len(sudoku)] for i in range(len(sudoku))]:
                    if line not in p_clues:
                        p_clues.append(line)
                        sudoku[line[0]][line[1]] = solved_sudoku[line[0]][line[1]]
                        clues+=1
                not_watched_clues = [line[:] for line in p_clues]
                
            
            x,y = random.choice(not_watched_clues)
            removed_clue = sudoku[x][y]        
            sudoku[x][y] = 0

            s = Solver(sudoku)
            if(s.find_all_solutions() == 1):
                clues-=1
                p_clues.remove([x,y])
                not_watched_clues = [line[:] for line in p_clues]

            else:
                sudoku[x][y] = removed_clue
                not_watched_clues.remove([x,y])
            if n%5 == 0:
                print(n, clues)
            n+=1

        return min_ret_sudoku
```

Este tiene un pequeño cambio, tomado directamente de la función de encontrar distintas soluciones. Si es que se le acaban las respuestas, en vez de entregar el sudoku, levanta una bandera de que ya encontró al menos uno, si es que tiene el minimo de pistas, lo guarda, en una variable que contiene solo el sudoku con menor número de claves. Luego genera unas posiciones aleatorias para luego ponerlas dentro del sudoku, contando cada clave añadida. De aquí vuelve a generar las claves posibles y las guarda como claves no vistas y vuelve a empezar el algoritmo. Termina hasta que llega ya sea a un número de pistas máximo que quieres o si ya completó 500 iteraciones.

---

Y entonces ahí estaba, 9:40 de la mañana, ya con el sentimiento de que por fin logré completar el solucionador y al mismo tiempo ya estaba en la parte final. Así, la hora no hizo más que motivarme, y entonces, sintiendo como si hubiera por fin terminado de haber reparado el motor de un deportivo en medio del desierto, empecé a programar la primera versión del generador.

La primera versión hacía lo que se me había ocurrido al inicio, verificar si una posición aleatoria era una clave, y quitarla. Verificar que solo hubiera una solución, y si es que había más, volver a poner el número quitado e intentar con otro.

Dado el tiempo, se me ocurrió utilizar números aleatorios para agarrar una posición aleatoria, agarrar la primera clave que me encuentre, quitarla y verificar que tuviera una única solución. Luego pararlo pasadas unas 500 iteraciones, y regresar el sudoku generado. Ese fue el algoritmo que programé en mis ultimos 10 minutos antes de ir corriendo a mi clase, y logré por fin que funcionara. 

Ya tenía el algoritmo completo. Literalmente me tardé más en solucionar un sudoku que en crearlo. 10 minutos. 

Ese fue el algoritmo que le presenté a mi profesor, a lo que él me pidió que hiciera un artículo de cómo se me habían ocurrido cada uno de los algoritmos. Ya estaba sin presiones, ya estaba tranquilo. Me acosté en el pasto luego de la clase, con un dolor de cabeza descomunal que solo lo podía atribuir a una cosa: El código que presenté es la peor manera de generar un sudoku, y sobretodo, debía de haber una mejor manera de parar el código.

Así que voy con mis amigos, ahí, mientras estoy con ellos, entiendo que ya tengo todas las posiciones de las claves en un inicio, y puedo ir pasando por ellas para quitarlas del sudoku, verificar que funciona sin ellas, y quitarlas de la lista. También veo que es mucho más fácil tener todas las posiciones ya revisadas guardadas, y pasar por las que no he visto... O mejor, guardar todas las que no he visto e irlas eliminando mientras paso por ellas.

Y de esa manera, llegué al mejor algoritmo para encontrar una solución única, y que con el mismo estoy seguro que no puedes quitar ni una sola pista más sin que ya no tenga otra solución.

Y de esta manera, completé el proyecto del sudoku en 4 horas de trabajo duro, y al mismo tiempo volver a respetar al algoritmo de generadores.


## Conclusión

A veces estos proyectos que empiezan siendo un simple desafío, terminan demostrandonos todas las cosas que nos faltan aprender, así como todas las cosas que nos han faltado aprender, pero también nos ayuda a entender nuestras debilidades y fortalezas ante los proyectos que nos encontremos. Este proyecto empezó con una idea de cómo funcionaría al final, pero nunca me imaginé que el camino hasta donde quería llegar tuviera tantos obstaculos y que me demostrara a respetar hasta los algoritmos que me parecen simples de explicar. 

Este proyecto es un simple generador de sudokus que logra resolverlos al mismo tiempo. Espero que les haya gustado este artículo del proceso para construir un buen algoritmo.

