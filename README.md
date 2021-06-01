<h1>Ni C - -</h1>

- Introducción
- Correr el Compilador
- Estatutos Secuenciales
- Expresiones Aritméticas
- Estatutos Condicionales
- Funciones
- Arreglos y Matrices
- Clases

<h2>Introducción</h2>
<p>El propósito de este compilador es facilitar el trabajo del programador con un lenguaje de programación orientado a objetos que mezcla elementos de Python y C + +. Gracias a la sintaxis que desarrollamos, el programador podrá hacer uso de sus conocimientos en diferentes lenguajes para programar de una manera intuitiva.</p>
<p>Esta es una guía para las primeros usuarios. En ella, encontrarás los pasos necesarios a seguir para poder correr el compilador y ejecutar diferentes estatutos.</p>

<h2>Correr el compilador</h2>
<p>Para correr el compilador, es necesario descargar la última version de Python. Es necesario saber cómo correr archivos .py de Python.</p>
<p>Correr este compilador es bastante sencillo, lo primero que debes de hacer es descargar este repositorio y guardarlo en tu máquina.</p>
<p>Para crear tu programa, deberás crear un archivo .txt con el código y guardarlo dentro de la carpeta del repositorio que descargaste.</p>

```
program patito;
char c[10];
{
    def void main()
    int i;
    char d;
    {
        for(i = 0; i < 10; i = i + 1){
            input(d);
            c[i] = d;
        }
        for(i = 0; i < 10; i = i + 1){
            print(c[i]);
        }
    }
}
```

<p>Después, utilizando un IDE o el método que gustes, corre el archivo llamado ScannerParser.py. Te deberá aparecer un mensaje para escribir el nombre de tu archivo.</p>
<p>¡Y listo! Una vez que hayas escrito el nombre del código que creaste, el compilador lo intentará ejecutar.</p>

<h2>Estatutos Secuenciales</h2>
<h3>Declaración y Asignación</h3>
<p>A diferencia de otros lenguajes de programación, en este se deberán de declarar las variables sin inicializar justo antes de las llaves de cada función si son locales, o bien, justo después de definir en nombre del programa. De esta manera:</p>

```
program decas;
int global;
{
    def void main()
    float local;
    {
        local = 2;
    }
}
```

<h3>Lectura</h3>
<p>Para la entrada del usuario, se debe llamar a la función 'input(variable)' y poner adentro la variable que se desea guardar.</p>

```
program lectura;
{
    def void main()
    char a;
    {
        input(a);
    }
}
```

<h3>Print</h3>
<p>Para imprimir, es igual que Python. El usuario deberá llamar a la función 'print(var)' y meter como argumento la variable que se desea imprimir.</p>

```
program imprime;
{
    def void main()
    char a;
    {
        input(a);
        print(a);
    }
}
```

<h2>Expresiones Aritméticas</h2>
<p>Las expresiones aritméticas funcionan igual que Python, es decir, se utilizan 'and' y 'or' para las hiper expresiones, todo lo demás es igual.</p>

```
program aritmetica;
{
    def void main()
    float a;
    {
        a = 5 / 2 * (20 + 13);
        b = 1 and 0;
        print(a);
        print(b);
    }
}
```

<h2>Estatutos Condicionales</h2>
<p>Los estatutos condicionales funcionan igual que C. Estos son algunos ejemplos.</p>

```
program forif;
int a[5];
char c;
{
    def void main()
    int i, k, temp, arr1, arr2;
    {
        for(i = 0; i < 5; i = i + 1) {
            input(k);
            a[i] = k;
        }
        if(a[0] < a[1]){
            print(i);
        } else {
            print(k);
        }
    }
}
```

```
program while;
int resp;
{
    def void main()
    int i;
    {
        i = 0;
        resp = 1;
        input(i);
        while(i > 0){
            resp = resp * i;
            i = i - 1;
        }
        print(resp);
    }
}
```

<h2>Funciones</h2>
<p>Las funciones se definen poniendo la palabra 'def' al principio de cada inicialización seguido de su tipo y su nombre. Al igual que C, puedes definir funciones de tipo void, int, float, o char.</p>

```
program funciones;
int a[5];
{
    def void sort(int k)
    int i, temp;
    {
        for(i = 0; i < 5; i = i + 1) {
            for(k = 0; k < 5 - 1; k = k + 1){
                if(a[k] > a[k + 1]){
                    temp = a[k];
                    a[k] = a[k + 1];
                    a[k + 1] = temp;
                }
            }
        }
        for(i = 0; i < 5; i = i + 1) {
            print(a[i]);
        }
    }

    def void main()
    int k, i;
    {
        for(i = 0; i < 5; i = i + 1) {
            input(k);
            a[i] = k;
        }
        sort(k);
    }
}
```

<h2>Arreglos y Matrices</h2>
<p>En este lenguaje puedes crear arreglos y matrices. Se inicializan y asignan de manera similar al lenguaje C.</p>

```
program matrices;
int loquesea;
int a[2][2];
int b[2][2];
int c[2][2];
{
    def void multmat()
    int i, j, k, l, m;
    {
        i = 0;
        for(i = 0; i < 2; i = i + 1) {
            for(j = 0; j < 2; j = j + 1) {
                c[i][j] = 0;
                for(k = 0; k < 2; k = k + 1) {
                    c[i][j] = a[i][k] * b[k][j] + c[i][j];
                }
            }
        }

        for(i = 0; i < 2; i = i + 1) {
            for(j = 0; j < 2; j = j + 1) {
                print(c[i][j]);
            }
        }
    }

    def void main()
    {
        a[0][0] = 1;
        a[0][1] = 2;
        a[1][0] = 3;
        a[1][1] = 4;
        b[0][0] = 1;
        b[0][1] = 1;
        b[1][0] = 1;
        b[1][1] = 1;

        multmat();
    }
}
```

<h2>Clases</h2>
<p>También puedes crear objetos como en cualquier lenguaje orientado a objetos.</p>

```
program clases;
{
    class Animal {
        float estatura;
        float peso;

        def void setEstatura(float e) {
            estatura = e * 5;
        }

        def void setPeso(float p) {
            peso = p * 5;
        }

        def float getEstatura() {
            return estatura;
        }

        def float getPeso() {
            return peso;
        }
    }
    def void main()
    float i, j;
    float z, m;
    Animal perro;
    Animal gato;
    {
        z = 3.11;
        m = 100;
        i = 3;
        j = i;
        j = i +100;
        perro.setEstatura(10.0);
        perro.setPeso(1.0);
        gato.setEstatura(10.0);
        gato.setPeso(2.0);
        print(perro.getEstatura());
        print(perro.getPeso());
        print(gato.getEstatura());
        print(gato.getPeso());
    }
}
```
<h2>Video</h2>
<p>https://drive.google.com/file/d/131ba4mDTrO65dZt6CsMLWEmeMIIk32y1/view?usp=sharing<p>

<p>Esperemos que disfruten de este lenguaje.</p>
