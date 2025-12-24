# Math Arena - Gamified Educational Platform

**URL del Proyecto:** [URL_DEL_PROYECTO_EN_RAILWAY]

## Descripción
Math Arena es una plataforma web educativa gamificada diseñada para hacer del aprendizaje de las matemáticas una experiencia competitiva y atractiva. A través de un sistema de progresión basado en rangos, experiencia (XP) y rachas diarias, los usuarios pueden completar cursos, resolver desafíos y competir en "Arenas" de entrenamiento contra ejercicios generados proceduralmente. El objetivo es motivar a los estudiantes mediante mecánicas de juego aplicadas al estudio, fomentando la práctica constante y el dominio de temas como Álgebra, Geometría y Cálculo.

## Tecnologías Utilizadas
Para el desarrollo de este proyecto se han utilizado las siguientes tecnologías:
*   **HTML**: Estructura semántica de la aplicación y vistas.
*   **CSS**: Estilizado personalizado con diseño responsivo y temática "Gamer/Dark Mode".
*   **JS (JavaScript)**: Lógica del cliente para el Dashboard dinámico, HUD de usuario y generador de ejercicios en tiempo real.
*   **Python**: Lógica del backend utilizando el framework Flask para manejar rutas, autenticación y APIs REST.
*   **SQL**: Gestión de base de datos relacional (MySQL) para persistencia de usuarios, progreso, cursos y estadísticas.

## Funcionalidades del Sistema
El sistema cuenta con los siguientes módulos principales:

1.  **Dashboard Dinámico**:
    *   Visualización en tiempo real de estadísticas del jugador: Rango actual (Bronce, Plata, Oro), Puntos de Experiencia (XP) y Racha de días consecutivos.
    *   **Desafío Diario**: Misiones generadas aleatoriamente (ej. "Resolver 5 integrales") para ganar recompensas extra.
    *   **Progreso de Curso**: Barra de seguimiento del curso activo actual.

2.  **Sistema de Cursos**:
    *   Catálogo de cursos disponibles (Álgebra I, Geometría, Cálculo).
    *   **Vista Detallada del Curso**: Desglose por módulos/temas, lista de ejercicios prácticos y examen final para completar el curso.

3.  **Arenas (Modo de Juego)**:
    *   **Training Mode**: Generador infinito de ejercicios matemáticos (Suma de Polinomios, Ecuaciones Lineales) para cursos completados.
    *   **Ranked Match**: Sistema competitivo (simulado) para subir de rango en la temporada.
    *   Solo accesible una vez que el usuario ha completado el 100% del curso requisito.

4.  **Autenticación y Seguridad**:
    *   Registro y Login de usuarios.
    *   Protección de rutas administrativas y de juego mediante sesiones.

## Futuras Implementaciones
*   **Multiplayer Real**: Implementar sockets para competencias 1v1 en tiempo real.
*   **Tienda de Avatares**: Uso de los puntos ganados para personalizar el perfil del usuario.
*   **Más Generadores**: Ampliar la lógica `ExerciseGeneratorService` para cubrir temas de Cálculo y Física.
