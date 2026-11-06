<h1> CC5303_lab2 </h1>
En el siguiente laboratorio partiremos con base al __laboratirio 1__, la idea en esta ocacion es llegar a poseer una infraestructura en que tengamos multiples clientes conectados a multiples servidores.

Las distintas etapas del laboratorio estan definidas mediante el _tag_ y una breve descripción de la etapa.

__f6b25a1__ Inicio del laboratorio

En esta etapa tenemos la aplicacion webapp.py que creamos en el laboratorio 1 y ahora crearemos un cliente que consultara el numero random para dejarlo en un archivo de salida

__616cf2c__ Uso de volumenes compartidos

En esta etapa veremos como podemos compartir carpetas desde el HOST con el contenedor, esto puede ser usado para que la app utilice configuraciones o para tener persistencia en los datos generados al ejecutar el contenedor.
- Nota: el cliente mismos es el encargado de crear la carpeta de log si esta no existe

__616cf2c__ Los contenedores deben partir en un orden y manejo de la salud del contenedor

En esta etapa veremos como organizamos la ejecución de los contenedores, ie, como podemos hacer que un contenedor dependa de que otro este arriba antes de partir. Ademas veremos los estados que un contenedor puede tener.