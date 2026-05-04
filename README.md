# Autenticación con Auth0 en Flask

Este proyecto consiste en la implementación de un sistema de autenticación utilizando Auth0 en una aplicación desarrollada con Python y Flask. Se permite el registro, inicio de sesión y la gestión de información del usuario mediante el uso de la propiedad `user_metadata`.

---

## Objetivo

Implementar un flujo completo de autenticación y gestión de usuario que incluya:

* Inicio de sesión con Auth0
* Personalización del Universal Login
* Edición de datos del usuario
* Consumo de la API de Auth0 para almacenar información

---

## Tecnologías utilizadas

* Python
* Flask
* Auth0
* HTML (templates)

---

## Desarrollo paso a paso

### 1. Configuración del login con Auth0

Para la autenticación se utilizó Auth0 como proveedor externo. Se creó una aplicación en el panel de Auth0 y se configuraron las variables de entorno necesarias como:

* AUTH0_DOMAIN
* AUTH0_CLIENT_ID
* AUTH0_CLIENT_SECRET

En el archivo `app.py` se configuró la integración utilizando la librería `authlib`, lo que permitió redirigir al usuario a la página de login de Auth0 mediante la ruta `/login`.

Una vez el usuario ingresa sus credenciales, Auth0 valida la información y redirige a la aplicación mediante la ruta `/callback`, donde se obtiene la información del usuario y se guarda en sesión.

---

### 2. Personalización del Universal Login

Se personalizó la interfaz de autenticación desde el panel de Auth0 en la sección de "Branding".

Se modificaron aspectos visuales como:

* Colores
* Estilo del botón
* Apariencia general del formulario

Esto permitió ofrecer una experiencia más acorde con la identidad visual de la aplicación.

---

### 3. Creación del formulario de perfil

Se desarrolló una vista (`/profile`) donde el usuario autenticado puede visualizar y editar sus datos personales.

Se creó un formulario HTML que permite ingresar:

* Tipo de documento
* Número de documento
* Dirección
* Teléfono

Estos datos se manejan mediante la propiedad `user_metadata`, lo que permite asociarlos directamente al usuario en Auth0.

---

### 4. Consumo de la API de Auth0

Para guardar la información ingresada por el usuario, se implementó el consumo de la API de gestión de Auth0.

Primero, se configuró una aplicación de tipo Machine to Machine en Auth0, la cual permite obtener un token de acceso mediante el flujo `client_credentials`.

Luego, desde Flask se implementaron funciones para:

1. Obtener el token de acceso
2. Enviar una solicitud HTTP tipo PATCH al endpoint de usuarios

Esto permite actualizar la propiedad `user_metadata` del usuario autenticado con la información ingresada en el formulario.

De esta forma, los datos quedan almacenados directamente en Auth0.

---

## Flujo de la aplicación

1. El usuario accede a la aplicación
2. Se autentica mediante Auth0
3. La aplicación recibe la información del usuario
4. El usuario accede a su perfil
5. Ingresa o edita sus datos
6. La aplicación envía los datos a la API de Auth0
7. Auth0 almacena la información en `user_metadata`

---

## Ejecución del proyecto

1. Crear entorno virtual:

```
python -m venv venv
```

2. Activar entorno:

```
source venv/bin/activate  (Mac/Linux)
venv\Scripts\activate     (Windows)
```

3. Instalar dependencias:

```
pip install -r requirements.txt
```

4. Crear archivo `.env` con las credenciales de Auth0

5. Ejecutar:

```
python app.py
```

---

## Notas importantes

* El archivo `.env` no se incluye en el repositorio por seguridad
* Se utiliza `user_metadata` para almacenar información personalizada del usuario
* La autenticación se maneja completamente mediante Auth0

---

## 📌 Autor

Trabajo realizado por Juan Pablo León Duque
