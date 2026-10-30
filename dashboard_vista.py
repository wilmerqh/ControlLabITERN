# ==============================================================================
# MÓDULO 4: dashboard_vista.py
# Dashboard Principal (Modo Oscuro Lab #0F172A) con 4 Módulos:
# 1. Módulo Equipos (CRUD Completo y Buscador - Áreas: Laboratorio y Bodega)
# 2. Módulo Áreas (Únicas 2 Áreas Físicas Oficiales: Laboratorio y Bodega)
# 3. Módulo Inventario (CRUD Completo y Buscador)
# 4. Módulo Usuarios (Control de Usuarios con Bcrypt OWASP A02)
# ==============================================================================

# Importamos customtkinter para crear la interfaz gráfica moderna en modo oscuro
import customtkinter as ctk  # Librería gráfica con el alias corto "ctk"
# Importamos ttk y messagebox desde tkinter para las tablas Treeview y alertas de usuario
from tkinter import ttk, messagebox  # Herramientas para tablas con estilo y cuadros de diálogo
# Importamos todas las funciones de base de datos seguras desde crud_computadoras.py
from crud_computadoras import (  # Importación estructurada de funciones CRUD seguras
    inicializar_tablas_seguras,  # Verifica y crea las 4 tablas en MySQL si no existen
    registrar_equipo,  # Inserta una computadora con sentencias preparadas (%s) sin codigo_pc manual
    registrar_pc,  # Alias directo para registrar computadoras con codigo_pc autoincrementable
    actualizar_equipo,  # Modifica los datos de una computadora por su codigo_pc (%s)
    actualizar_pc,  # Alias directo para actualizar computadoras por codigo_pc
    eliminar_equipo,  # Elimina una computadora por su codigo_pc (%s)
    eliminar_pc,  # Alias directo para eliminar computadoras por codigo_pc
    obtener_equipos,  # Consulta todas las computadoras (columna 1: codigo_pc generado por MySQL)
    obtener_equipos_por_area,  # Filtra computadoras por área con WHERE id_area = %s (OWASP A03)
    buscar_equipos,  # Busca computadoras usando sentencia preparada LIKE %s
    obtener_areas,  # Consulta las 2 áreas físicas oficiales (Laboratorio y Bodega)
    registrar_articulo_inventario,  # Inserta herramientas o periféricos con %s
    actualizar_articulo_inventario,  # Modifica un artículo del inventario por su ID (%s)
    eliminar_articulo_inventario,  # Elimina un artículo del inventario por su ID (%s)
    obtener_articulos_inventario,  # Consulta todos los artículos del inventario
    buscar_articulos_inventario,  # Busca artículos usando sentencia preparada LIKE %s
    registrar_usuario,  # Inserta un nuevo usuario cifrando su clave con bcrypt (OWASP A02)
    obtener_usuarios,  # Consulta usuarios (solo ID y Usuario, nunca el hash de la clave)
    buscar_usuarios,  # Busca usuarios por nombre con sentencia preparada LIKE %s
    eliminar_usuario,  # Elimina un usuario por su ID (%s)
    cambiar_contrasena_usuario  # Actualiza la contraseña de un usuario con bcrypt (OWASP A02)
)  # Fin de la importación de funciones CRUD
# Importamos la función de generación de reportes en PDF desde generador_pdf.py
from generador_pdf import exportar_inventario_pdf  # Función para generar el reporte PDF del inventario

# ==============================================================================
# 1. CONFIGURACIÓN DE PALETA DE COLORES (MODO OSCURO LAB #0F172A)
# ==============================================================================

# Color azul noche muy oscuro para el fondo general de la aplicación
COLOR_FONDO = "#0F172A"  # Fondo principal solicitado (#0F172A)
# Color gris azulado oscuro para los paneles contenedores y el menú lateral
COLOR_PANELES = "#1E293B"  # Color de paneles (#1E293B)
# Color azul celeste vibrante para botones de acción estándar y bordes activos
COLOR_BOTONES = "#0EA5E9"  # Color primario de botones (#0EA5E9)
# Color blanco suave para que los textos sean legibles sobre el fondo oscuro
COLOR_TEXTO = "#F8FAFC"  # Color de texto (#F8FAFC)
# Color rojo vibrante para advertir y ejecutar acciones de eliminación
COLOR_PELIGRO = "#EF4444"  # Color para botón Eliminar (#EF4444)
# Color naranja ámbar para indicar acciones de edición y actualización
COLOR_ADVERTENCIA = "#F59E0B"  # Color para botón Editar/Actualizar (#F59E0B)
# Color verde esmeralda para acciones de éxito o confirmación
COLOR_EXITO = "#10B981"  # Color para confirmaciones (#10B981)

# ==============================================================================
# 2. FUNCIÓN PRINCIPAL QUE INICIA EL DASHBOARD COMPLETO
# ==============================================================================

# Definimos la función iniciar_dashboard que construye y despliega la ventana principal
def iniciar_dashboard():  # Inicio de la función constructora del Dashboard
    # Nos aseguramos de que las tablas en MySQL estén listas de forma preventiva
    inicializar_tablas_seguras()  # Inicialización segura de tablas y datos base

    # Configuramos el modo de apariencia global en modo oscuro
    ctk.set_appearance_mode("dark")  # Activamos el tema oscuro nativo

    # Instanciamos la ventana principal de CustomTkinter
    ventana_dashboard = ctk.CTk()  # Ventana raíz del Dashboard
    # Asignamos el título oficial en la barra superior de la ventana
    ventana_dashboard.title("ControlLabITERN - Gestión de Laboratorio (Seguridad OWASP)")  # Título
    # Establecemos el tamaño inicial en 1020x660 para máxima comodidad visual
    ventana_dashboard.geometry("1020x660")  # Dimensiones amplias y cómodas
    # Fijamos el tamaño mínimo permitido para evitar desbordamientos
    ventana_dashboard.minsize(960, 620)  # Dimensiones mínimas
    # Pintamos el fondo principal con el color azul noche del laboratorio
    ventana_dashboard.configure(fg_color=COLOR_FONDO)  # Aplicamos el fondo #0F172A

    # ==========================================================================
    # 3. ESTILO VISUAL MODO OSCURO PARA TODAS LAS TABLAS TREEVIEW (TTK)
    # ==========================================================================

    # Creamos el objeto Style para configurar la apariencia de las tablas Treeview
    estilo_tablas = ttk.Style()  # Administrador de estilos TTK
    # Seleccionamos el tema 'clam' que permite personalización de colores oscuros
    estilo_tablas.theme_use("clam")  # Tema base adaptable
    # Configuramos el diseño oscuro para las celdas y filas de datos
    estilo_tablas.configure(  # Configuración visual de filas
        "Treeview",  # Selector de la tabla Treeview
        background=COLOR_FONDO,  # Fondo de cada fila (#0F172A)
        foreground=COLOR_TEXTO,  # Color de texto blanco suave (#F8FAFC)
        fieldbackground=COLOR_FONDO,  # Fondo de campos vacíos
        rowheight=28,  # Altura de 28 píxeles por fila para mejor lectura
        font=("Segoe UI", 10),  # Fuente clara y legible
        borderwidth=0  # Sin bordes toscos
    )  # Fin de configuración de filas
    # Configuramos el diseño oscuro para los encabezados superiores de las tablas
    estilo_tablas.configure(  # Configuración visual de encabezados
        "Treeview.Heading",  # Selector de encabezados
        background=COLOR_PANELES,  # Fondo gris azulado (#1E293B)
        foreground=COLOR_TEXTO,  # Texto blanco (#F8FAFC)
        font=("Segoe UI", 10, "bold"),  # Letra en negrita para resaltar columnas
        relief="flat"  # Encabezados planos y modernos
    )  # Fin de configuración de encabezados
    # Asignamos el color azul (#0EA5E9) cuando el usuario selecciona cualquier fila
    estilo_tablas.map(  # Mapeo dinámico de estados
        "Treeview",  # Aplicado a la tabla Treeview
        background=[("selected", COLOR_BOTONES)],  # Fondo azul al seleccionar
        foreground=[("selected", COLOR_TEXTO)]  # Texto blanco al seleccionar
    )  # Fin del mapeo dinámico

    # ==========================================================================
    # 4. GESTIÓN DE NAVEGACIÓN ENTRE LOS 4 MÓDULOS DEL SISTEMA
    # ==========================================================================

    # Función que oculta los 4 paneles antes de desplegar el módulo seleccionado
    def ocultar_todos_los_modulos():  # Limpia la pantalla central
        # Ocultamos el panel de Equipos
        panel_modulo_equipos.pack_forget()  # Esconde Equipos
        # Ocultamos el panel de Áreas
        panel_modulo_areas.pack_forget()  # Esconde Áreas
        # Ocultamos el panel de Inventario
        panel_modulo_inventario.pack_forget()  # Esconde Inventario
        # Ocultamos el panel de Usuarios
        panel_modulo_usuarios.pack_forget()  # Esconde Usuarios

    # Función para mostrar el Módulo 1: 'Equipos'
    def mostrar_modulo_equipos():  # Activa la vista de Equipos
        # Ocultamos cualquier otro módulo activo
        ocultar_todos_los_modulos()  # Limpia la pantalla central
        # Mostramos el panel de Equipos ocupando todo el espacio central
        panel_modulo_equipos.pack(fill="both", expand=True, padx=20, pady=20)  # Muestra Equipos
        # Recargamos la tabla de equipos con los datos más recientes de MySQL
        cargar_tabla_equipos()  # Llena el Treeview de Equipos

    # Función para mostrar el Módulo 2: 'Áreas'
    def mostrar_modulo_areas():  # Activa la vista de Áreas
        # Ocultamos cualquier otro módulo activo
        ocultar_todos_los_modulos()  # Limpia la pantalla central
        # Mostramos el panel de Áreas ocupando el espacio central
        panel_modulo_areas.pack(fill="both", expand=True, padx=20, pady=20)  # Muestra Áreas
        # Recargamos la tabla de las 2 áreas físicas (Laboratorio y Bodega)
        cargar_tabla_areas()  # Llena el Treeview de Áreas

    # Función para mostrar el Módulo 3: 'Inventario'
    def mostrar_modulo_inventario():  # Activa la vista de Inventario
        # Ocultamos cualquier otro módulo activo
        ocultar_todos_los_modulos()  # Limpia la pantalla central
        # Mostramos el panel de Inventario en el espacio central
        panel_modulo_inventario.pack(fill="both", expand=True, padx=20, pady=20)  # Muestra Inventario
        # Recargamos la tabla de inventario desde MySQL
        cargar_tabla_inventario()  # Llena el Treeview de Inventario

    # Función para mostrar el Módulo 4: 'Usuarios'
    def mostrar_modulo_usuarios():  # Activa la vista de Usuarios
        # Ocultamos cualquier otro módulo activo
        ocultar_todos_los_modulos()  # Limpia la pantalla central
        # Mostramos el panel de Usuarios en el espacio central
        panel_modulo_usuarios.pack(fill="both", expand=True, padx=20, pady=20)  # Muestra Usuarios
        # Recargamos la lista de usuarios desde MySQL
        cargar_tabla_usuarios()  # Llena el Treeview de Usuarios

    # ==========================================================================
    # 5. MENÚ LATERAL IZQUIERDO CON 4 BOTONES DE NAVEGACIÓN
    # ==========================================================================

    # Creamos el contenedor vertical para el menú lateral
    panel_menu_lateral = ctk.CTkFrame(ventana_dashboard, width=220, fg_color=COLOR_PANELES, corner_radius=0)  # Marco del menú
    # Empaquetamos el menú lateral anclado a la izquierda
    panel_menu_lateral.pack(side="left", fill="y")  # Se estira verticalmente
    # Bloqueamos su tamaño para que no se deforme al agregar elementos
    panel_menu_lateral.pack_propagate(False)  # Mantiene sus 220 píxeles de ancho fijo

    # Etiqueta con el logo y nombre de la institución
    etiqueta_logo = ctk.CTkLabel(panel_menu_lateral, text="ControlLab\nITERN", font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXTO)  # Logo
    # Posicionamos el título en la parte superior del menú
    etiqueta_logo.pack(pady=(35, 8), padx=15)  # Margen superior
    # Etiqueta informativa sobre la seguridad aplicada
    etiqueta_owasp = ctk.CTkLabel(panel_menu_lateral, text="Seguridad OWASP Top 10\n(A02 & A03 Blindados)", font=("Segoe UI", 11), text_color=COLOR_BOTONES)  # Subtítulo OWASP
    # Posicionamos la etiqueta debajo del título
    etiqueta_owasp.pack(pady=(0, 25), padx=15)  # Margen inferior antes de los botones

    # --- Botón 1 de Navegación: Equipos ---
    boton_nav_equipos = ctk.CTkButton(panel_menu_lateral, text="🖥️  Equipos", font=("Segoe UI", 15, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, hover_color="#0284C7", height=42, command=mostrar_modulo_equipos)  # Botón Equipos
    # Empaquetamos el botón en el menú
    boton_nav_equipos.pack(fill="x", padx=18, pady=6)  # Espaciado del botón Equipos

    # --- Botón 2 de Navegación: Áreas ---
    boton_nav_areas = ctk.CTkButton(panel_menu_lateral, text="🏢  Áreas", font=("Segoe UI", 15, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, hover_color="#0284C7", height=42, command=mostrar_modulo_areas)  # Botón Áreas
    # Empaquetamos el botón debajo de Equipos
    boton_nav_areas.pack(fill="x", padx=18, pady=6)  # Espaciado del botón Áreas

    # --- Botón 3 de Navegación: Inventario ---
    boton_nav_inventario = ctk.CTkButton(panel_menu_lateral, text="📦  Inventario", font=("Segoe UI", 15, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, hover_color="#0284C7", height=42, command=mostrar_modulo_inventario)  # Botón Inventario
    # Empaquetamos el botón debajo de Áreas
    boton_nav_inventario.pack(fill="x", padx=18, pady=6)  # Espaciado del botón Inventario

    # --- Botón 4 de Navegación: Usuarios (Módulo de Administración) ---
    boton_nav_usuarios = ctk.CTkButton(panel_menu_lateral, text="👥  Usuarios", font=("Segoe UI", 15, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, hover_color="#0284C7", height=42, command=mostrar_modulo_usuarios)  # Botón Usuarios
    # Empaquetamos el botón debajo de Inventario
    boton_nav_usuarios.pack(fill="x", padx=18, pady=6)  # Espaciado del botón Usuarios

    # ==========================================================================
    # 6. CONTENEDOR CENTRAL PARA DESPLEGAR LOS MÓDULOS
    # ==========================================================================

    # Creamos el contenedor central donde se mostrará el módulo activo
    area_central = ctk.CTkFrame(ventana_dashboard, fg_color=COLOR_FONDO, corner_radius=0)  # Contenedor central
    # Hacemos que ocupe todo el espacio a la derecha del menú lateral
    area_central.pack(side="right", fill="both", expand=True)  # Se expande en pantalla completa

    # ==========================================================================
    # 7. MÓDULO 1: EQUIPOS (FORMULARIO CON SOLO LABORATORIO Y BODEGA)
    # ==========================================================================

    # Creamos el panel contenedor del Módulo Equipos
    panel_modulo_equipos = ctk.CTkFrame(area_central, fg_color=COLOR_PANELES, corner_radius=12)  # Marco de Equipos

    # Título principal del módulo
    etiqueta_titulo_equipos = ctk.CTkLabel(panel_modulo_equipos, text="Módulo de Equipos de Cómputo", font=("Segoe UI", 20, "bold"), text_color=COLOR_TEXTO)  # Título Equipos
    # Posicionamos el título en la parte superior izquierda
    etiqueta_titulo_equipos.pack(anchor="w", padx=20, pady=(15, 6))  # Margen del título

    # --- BUSCADOR DE EQUIPOS EN LA PARTE SUPERIOR ---
    panel_busqueda_equipos = ctk.CTkFrame(panel_modulo_equipos, fg_color="transparent")  # Contenedor horizontal del buscador
    # Empaquetamos el panel del buscador
    panel_busqueda_equipos.pack(fill="x", padx=20, pady=(0, 10))  # Se estira horizontalmente

    # Caja de texto para ingresar el término de búsqueda
    caja_buscar_equipos = ctk.CTkEntry(panel_busqueda_equipos, placeholder_text="Buscar equipo por código, procesador, área...", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=34)  # Entry buscador
    # Empaquetamos la caja de búsqueda a la izquierda con expansión
    caja_buscar_equipos.pack(side="left", fill="x", expand=True, padx=(0, 8))  # Ocupa la mayor parte del ancho

    # Función que ejecuta la búsqueda de equipos con SELECT ... LIKE %s
    def accion_buscar_equipos():  # Evento al hacer clic en Buscar
        # Obtenemos el texto ingresado en la caja de búsqueda
        termino = caja_buscar_equipos.get().strip()  # Texto buscado
        # Si el usuario no escribió nada, le recordamos ingresar un dato
        if not termino:  # Si la caja está vacía
            # Mostramos un aviso informativo
            messagebox.showinfo("Búsqueda", "Ingresa un término para buscar equipos.")  # Aviso
            # Salimos de la función
            return  # Detiene la búsqueda
        # Llamamos a buscar_equipos() que ejecuta la sentencia preparada LIKE %s
        resultados = buscar_equipos(termino)  # Consulta protegida
        # Limpiamos las filas actuales del Treeview
        for fila in tabla_equipos.get_children():  # Recorre filas actuales
            # Borramos cada fila
            tabla_equipos.delete(fila)  # Elimina fila
        # Insertamos en el Treeview solo los resultados encontrados
        for equipo in resultados:  # Recorre filas coincidentes
            # Dibuja la fila en la tabla
            tabla_equipos.insert("", "end", values=equipo)  # Inserta fila filtrada

    # Función para limpiar el filtro de búsqueda y volver a mostrar todos los equipos
    def accion_limpiar_equipos():  # Evento del botón Limpiar Filtro
        # Vaciamos la caja de texto del buscador
        caja_buscar_equipos.delete(0, "end")  # Limpia la caja
        # Restablecemos el ComboBox interactivo de filtro de área a 'Todas las áreas'
        combo_filtro_area.set("Todas las áreas")  # Restablece la selección de área
        # Recargamos todos los equipos desde MySQL
        cargar_tabla_equipos()  # Muestra todos los registros

    # Botón '🔎 Buscar' conectado a la búsqueda segura con LIKE %s
    boton_buscar_equipos = ctk.CTkButton(panel_busqueda_equipos, text="🔎 Buscar", font=("Segoe UI", 12, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, width=100, height=34, command=accion_buscar_equipos)  # Botón Buscar
    # Empaquetamos el botón de búsqueda
    boton_buscar_equipos.pack(side="left", padx=(0, 6))  # Ubicado al lado de la caja

    # Botón 'Limpiar Filtro' para restaurar la vista completa de la tabla
    boton_limpiar_equipos = ctk.CTkButton(panel_busqueda_equipos, text="Limpiar Filtro", font=("Segoe UI", 12), fg_color="#475569", text_color=COLOR_TEXTO, hover_color="#334155", width=110, height=34, command=accion_limpiar_equipos)  # Botón Limpiar
    # Empaquetamos el botón de limpiar
    boton_limpiar_equipos.pack(side="left")  # Ubicado a la derecha del botón Buscar

    # --- FORMULARIO DE EQUIPOS (ÁREAS EXCLUSIVAS: LABORATORIO Y BODEGA - CÓDIGO AUTOINCREMENTABLE) ---
    # Variable mutable que guarda el codigo_pc en edición (None si es nuevo registro autoincrementable)
    codigo_pc_edicion = [None]  # Lista con un elemento para rastrear el codigo_pc en edición

    # Marco del formulario organizado en 3 columnas
    form_equipos = ctk.CTkFrame(panel_modulo_equipos, fg_color="transparent")  # Contenedor del formulario
    # Empaquetamos el formulario
    form_equipos.pack(fill="x", padx=20, pady=(0, 8))  # Se estira a lo ancho
    # Configuramos las 3 columnas proporcionales
    form_equipos.grid_columnconfigure(0, weight=1)  # Columna 0
    form_equipos.grid_columnconfigure(1, weight=1)  # Columna 1
    form_equipos.grid_columnconfigure(2, weight=1)  # Columna 2

    # Campo 1: Área Física (ComboBox con SOLO 'Laboratorio' y 'Bodega')
    etiqueta_area_eq = ctk.CTkLabel(form_equipos, text="Área Física:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta Área
    etiqueta_area_eq.grid(row=0, column=0, sticky="w", padx=4, pady=(0, 2))  # Fila 0, Columna 0
    # ComboBox configurado exclusivamente con las 2 únicas áreas físicas del instituto
    combo_area_equipo = ctk.CTkComboBox(form_equipos, values=["Laboratorio", "Bodega"], fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, button_color=COLOR_BOTONES, dropdown_fg_color=COLOR_PANELES, dropdown_text_color=COLOR_TEXTO, state="readonly", height=32)  # ComboBox solo Laboratorio y Bodega
    combo_area_equipo.set("Laboratorio")  # Opción por defecto inicial: Laboratorio
    combo_area_equipo.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 6))  # Fila 1, Columna 0

    # Campo 2: Procesador (Entry)
    etiqueta_proc_eq = ctk.CTkLabel(form_equipos, text="Procesador:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta Procesador
    etiqueta_proc_eq.grid(row=0, column=1, sticky="w", padx=4, pady=(0, 2))  # Fila 0, Columna 1
    caja_procesador_equipo = ctk.CTkEntry(form_equipos, placeholder_text="Ej: Intel Core i5", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=32)  # Entry Procesador
    caja_procesador_equipo.grid(row=1, column=1, sticky="ew", padx=4, pady=(0, 6))  # Fila 1, Columna 1

    # Campo 3: RAM (Entry)
    etiqueta_ram_eq = ctk.CTkLabel(form_equipos, text="Memoria RAM:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta RAM
    etiqueta_ram_eq.grid(row=0, column=2, sticky="w", padx=4, pady=(0, 2))  # Fila 0, Columna 2
    caja_ram_equipo = ctk.CTkEntry(form_equipos, placeholder_text="Ej: 16 GB DDR4", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=32)  # Entry RAM
    caja_ram_equipo.grid(row=1, column=2, sticky="ew", padx=4, pady=(0, 6))  # Fila 1, Columna 2

    # Campo 4: Almacenamiento (Entry)
    etiqueta_alm_eq = ctk.CTkLabel(form_equipos, text="Almacenamiento:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta Almacenamiento
    etiqueta_alm_eq.grid(row=2, column=0, sticky="w", padx=4, pady=(0, 2))  # Fila 2, Columna 0
    caja_almacenamiento_equipo = ctk.CTkEntry(form_equipos, placeholder_text="Ej: 512 GB SSD", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=32)  # Entry Almacenamiento
    caja_almacenamiento_equipo.grid(row=3, column=0, sticky="ew", padx=4, pady=(0, 6))  # Fila 3, Columna 0

    # Campo 5: Estado (ComboBox)
    etiqueta_est_eq = ctk.CTkLabel(form_equipos, text="Estado:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta Estado
    etiqueta_est_eq.grid(row=2, column=1, sticky="w", padx=4, pady=(0, 2))  # Fila 2, Columna 1
    combo_estado_equipo = ctk.CTkComboBox(form_equipos, values=["Activa", "En Mantenimiento", "Dañada"], fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, button_color=COLOR_BOTONES, dropdown_fg_color=COLOR_PANELES, dropdown_text_color=COLOR_TEXTO, state="readonly", height=32)  # ComboBox Estado
    combo_estado_equipo.set("Activa")  # Opción por defecto
    combo_estado_equipo.grid(row=3, column=1, sticky="ew", padx=4, pady=(0, 6))  # Fila 3, Columna 1

    # Indicador de Código Automático (sin campo de texto manual)
    etiqueta_info_cod = ctk.CTkLabel(form_equipos, text="⚡ Código PC: Generado por MySQL (Auto)", font=("Segoe UI", 11, "italic"), text_color="#38BDF8")  # Etiqueta informativa
    etiqueta_info_cod.grid(row=3, column=2, sticky="ew", padx=4, pady=(0, 6))  # Fila 3, Columna 2

    # Función que guarda un nuevo equipo o actualiza uno existente según codigo_pc_edicion
    def accion_guardar_o_actualizar_equipo():  # Evento del botón principal del formulario
        # Leemos los datos de las cajas de texto y comboboxes (sin pedir código manual)
        area = combo_area_equipo.get()  # Área seleccionada (Laboratorio o Bodega)
        procesador = caja_procesador_equipo.get().strip()  # Procesador ingresado
        ram = caja_ram_equipo.get().strip()  # Memoria RAM ingresada
        almacenamiento = caja_almacenamiento_equipo.get().strip()  # Almacenamiento ingresado
        estado = combo_estado_equipo.get()  # Estado seleccionado

        # Validamos que los campos obligatorios no estén vacíos
        if not procesador or not ram or not almacenamiento:  # Validación
            # Mostramos una alerta al usuario
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos del equipo.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción

        # CASO 1: Si no estamos editando (es un nuevo registro autoincrementable)
        if codigo_pc_edicion[0] is None:  # Inserción nueva
            # Llamamos a registrar_pc() usando sentencias preparadas (%s) sin codigo_pc manual
            if registrar_pc(area, procesador, ram, almacenamiento, estado):  # Si se guardó en MySQL
                # Notificamos éxito al usuario
                messagebox.showinfo("Éxito", f"La computadora fue registrada correctamente en el área '{area}' con código autogenerado.")  # Mensaje
                # Limpiamos los campos del formulario
                limpiar_formulario_equipos()  # Deja el formulario en blanco
                # Recargamos la tabla
                cargar_tabla_equipos()  # Actualiza la vista
        # CASO 2: Si estamos en modo de edición (actualizamos por codigo_pc)
        else:  # Modo actualización
            # Obtenemos el codigo_pc del equipo en edición
            codigo_a_actualizar = codigo_pc_edicion[0]  # Código numérico
            # Llamamos a actualizar_pc() que ejecuta UPDATE ... WHERE codigo_pc = %s
            if actualizar_pc(codigo_a_actualizar, area, procesador, ram, almacenamiento, estado):  # Si se actualizó
                # Notificamos éxito al usuario
                messagebox.showinfo("Éxito", f"La computadora con Código PC #{codigo_a_actualizar} fue actualizada exitosamente.")  # Mensaje
                # Restablecemos el formulario y el botón a su estado normal
                limpiar_formulario_equipos()  # Limpia y vuelve a modo registro
                # Recargamos la tabla
                cargar_tabla_equipos()  # Actualiza la vista

    # Función auxiliar para vaciar el formulario de equipos y resetear el botón a "Registrar"
    def limpiar_formulario_equipos():  # Restablece formulario
        # Vaciamos la variable de edición
        codigo_pc_edicion[0] = None  # Regresa a modo nuevo registro
        # Limpiamos las cajas de texto
        caja_procesador_equipo.delete(0, "end")  # Limpia procesador
        caja_ram_equipo.delete(0, "end")  # Limpia RAM
        caja_almacenamiento_equipo.delete(0, "end")  # Limpia almacenamiento
        combo_area_equipo.set("Laboratorio")  # Restablece a Laboratorio por defecto
        combo_estado_equipo.set("Activa")  # Restablece estado
        # Restauramos el texto y color del botón principal
        boton_guardar_equipo.configure(text="Registrar Equipo", fg_color=COLOR_BOTONES, hover_color="#0284C7")  # Botón estándar

    # Botón dinámico del formulario (cambia entre "Registrar Equipo" y "Actualizar Equipo")
    boton_guardar_equipo = ctk.CTkButton(form_equipos, text="Registrar Equipo", font=("Segoe UI", 13, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, hover_color="#0284C7", height=34, command=accion_guardar_o_actualizar_equipo)  # Botón Guardar/Actualizar
    # Ubicamos el botón ocupando las 3 columnas del formulario
    boton_guardar_equipo.grid(row=4, column=0, columnspan=3, sticky="ew", padx=4, pady=(2, 2))  # Fila 4 completa

    # --- FILTRO INTERACTIVO POR ÁREA (ARRIBA DEL TREEVIEW DE COMPUTADORAS) ---
    # Contenedor horizontal para el filtro interactivo por área física
    panel_filtro_area = ctk.CTkFrame(panel_modulo_equipos, fg_color="transparent")  # Marco para la barra de filtro
    # Empaquetamos el panel del filtro justo encima del Treeview de computadoras
    panel_filtro_area.pack(fill="x", padx=20, pady=(6, 4))  # Se estira a lo ancho arriba de la tabla

    # Etiqueta que identifica el selector de filtrado por área
    etiqueta_filtro_area = ctk.CTkLabel(panel_filtro_area, text="Filtrar por Área Física:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta del filtro
    # Empaquetamos la etiqueta a la izquierda
    etiqueta_filtro_area.pack(side="left", padx=(0, 10))  # Alineación izquierda

    # Función interactiva que se ejecuta cada vez que el usuario cambia la opción del ComboBox
    def accion_filtrar_por_area(area_seleccionada):  # Función de filtrado interactivo por área
        # Si el usuario elige 'Laboratorio', consultamos computadoras donde id_area = 1
        if area_seleccionada == "Laboratorio":  # Verificamos si seleccionó Laboratorio
            # Ejecuta SELECT con WHERE id_area = 1 mediante sentencias preparadas (%s)
            equipos_filtrados = obtener_equipos_por_area(1)  # id_area 1 en MySQL (Laboratorio)
        # Si el usuario elige 'Bodega', consultamos computadoras donde id_area = 2
        elif area_seleccionada == "Bodega":  # Verificamos si seleccionó Bodega
            # Recarga el Treeview solo con las PCs del área 2 (Bodega)
            equipos_filtrados = obtener_equipos_por_area(2)  # id_area 2 en MySQL (Bodega)
        # Si elige 'Todas las áreas' (o cualquier otra opción), hace el SELECT general
        else:  # Opción 'Todas las áreas'
            # Consulta general de todos los equipos registrados sin filtrar por área
            equipos_filtrados = obtener_equipos()  # SELECT general de todas las PCs
        # Limpiamos las filas actuales de la tabla Treeview de computadoras
        for fila in tabla_equipos.get_children():  # Recorremos cada fila existente
            # Borramos la fila
            tabla_equipos.delete(fila)  # Limpieza de fila previa
        # Insertamos en el Treeview únicamente las computadoras que corresponden al filtro
        for equipo in equipos_filtrados:  # Recorremos los registros devueltos
            # Agregamos cada equipo a la tabla
            tabla_equipos.insert("", "end", values=equipo)  # Dibuja la fila en el Treeview

    # ComboBox interactivo con las 3 opciones requeridas: 'Todas las áreas', 'Laboratorio', 'Bodega'
    combo_filtro_area = ctk.CTkComboBox(  # Instanciamos el ComboBox de filtrado interactivo
        panel_filtro_area,  # Asignamos al panel del filtro arriba del Treeview
        values=["Todas las áreas", "Laboratorio", "Bodega"],  # Opciones exactas requeridas
        command=accion_filtrar_por_area,  # Función interactiva conectada al cambio de opción
        fg_color=COLOR_FONDO,  # Color de fondo coherente con el modo oscuro (#0F172A)
        text_color=COLOR_TEXTO,  # Color de texto legible en blanco
        border_color=COLOR_BOTONES,  # Borde con acento azul (#0284C7)
        button_color=COLOR_BOTONES,  # Botón con color institucional
        dropdown_fg_color=COLOR_PANELES,  # Fondo de la lista desplegable (#1E293B)
        dropdown_text_color=COLOR_TEXTO,  # Texto de los elementos desplegables
        state="readonly",  # Modo solo lectura para evitar escritura de datos inválidos
        width=180,  # Ancho en píxeles del ComboBox
        height=32  # Alto en píxeles del ComboBox
    )  # Fin de la definición del ComboBox
    # Configuramos el valor inicial por defecto como 'Todas las áreas'
    combo_filtro_area.set("Todas las áreas")  # Valor por defecto inicial
    # Empaquetamos el ComboBox a la izquierda
    combo_filtro_area.pack(side="left", padx=(0, 10))  # Alineado a la izquierda con margen

    # Botón '📄 Exportar a PDF' ubicado junto al filtro interactivo para acceso rápido
    boton_exportar_pdf_filtro = ctk.CTkButton(panel_filtro_area, text="📄 Exportar a PDF", font=("Segoe UI", 12, "bold"), fg_color="#10B981", text_color=COLOR_TEXTO, hover_color="#059669", width=140, height=32, command=lambda: accion_exportar_pdf())  # Botón Exportar PDF
    # Empaquetamos el botón a la derecha en la barra del filtro
    boton_exportar_pdf_filtro.pack(side="right")  # Alineación a la derecha

    # --- TABLA TREEVIEW DE EQUIPOS ---
    # Contenedor para la tabla de equipos
    contenedor_tabla_equipos = ctk.CTkFrame(panel_modulo_equipos, fg_color=COLOR_FONDO, corner_radius=8)  # Marco de la tabla
    # Empaquetamos el contenedor
    contenedor_tabla_equipos.pack(fill="both", expand=True, padx=20, pady=(2, 6))  # Se expande

    # Definimos las columnas del Treeview de Equipos (primera columna: codigo_pc autoincrementable)
    columnas_equipos = ("codigo_pc", "area", "procesador", "ram", "almacenamiento", "estado")  # 6 columnas
    # Creamos el Treeview
    tabla_equipos = ttk.Treeview(contenedor_tabla_equipos, columns=columnas_equipos, show="headings")  # Tabla Equipos

    # Encabezados de las 6 columnas (la primera columna muestra el codigo_pc autogenerado por MySQL)
    tabla_equipos.heading("codigo_pc", text="Código PC (Auto)")  # Columna 1: codigo_pc autoincrementable de MySQL
    tabla_equipos.heading("area", text="Área Física")  # Columna 2: Área Física
    tabla_equipos.heading("procesador", text="Procesador")  # Columna 3: Procesador
    tabla_equipos.heading("ram", text="RAM")  # Columna 4: RAM
    tabla_equipos.heading("almacenamiento", text="Almacenamiento")  # Columna 5: Almacenamiento
    tabla_equipos.heading("estado", text="Estado")  # Columna 6: Estado

    # Ancho de las 6 columnas
    tabla_equipos.column("codigo_pc", width=110, anchor="center")  # Código PC centrado
    tabla_equipos.column("area", width=120, anchor="center")  # Área centrada
    tabla_equipos.column("procesador", width=160, anchor="w")  # Procesador a la izquierda
    tabla_equipos.column("ram", width=95, anchor="center")  # RAM centrada
    tabla_equipos.column("almacenamiento", width=120, anchor="center")  # Almacenamiento centrado
    tabla_equipos.column("estado", width=120, anchor="center")  # Estado centrado

    # Barra de desplazamiento vertical para la tabla de equipos
    scroll_equipos = ctk.CTkScrollbar(contenedor_tabla_equipos, orientation="vertical", command=tabla_equipos.yview, fg_color=COLOR_PANELES, button_color=COLOR_BOTONES)  # Scrollbar
    # Conectamos la tabla con la barra de desplazamiento
    tabla_equipos.configure(yscrollcommand=scroll_equipos.set)  # Sincronización
    # Empaquetamos la barra y la tabla
    scroll_equipos.pack(side="right", fill="y", padx=(0, 4), pady=4)  # Barra a la derecha
    tabla_equipos.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)  # Tabla a la izquierda

    # Función para cargar los registros en la tabla de equipos desde MySQL respetando el filtro
    def cargar_tabla_equipos():  # Actualiza el Treeview según el filtro
        # Leemos la selección activa en el ComboBox de filtro de área
        area_actual = combo_filtro_area.get()  # Obtiene 'Todas las áreas', 'Laboratorio' o 'Bodega'
        # Ejecutamos la función de filtrado con el área actual para actualizar la tabla
        accion_filtrar_por_area(area_actual)  # Recarga la tabla con los datos correspondientes

    # --- BOTONES DE ACCIÓN DEBAJO DE LA TABLA DE EQUIPOS (EDITAR Y ELIMINAR) ---
    panel_acciones_equipos = ctk.CTkFrame(panel_modulo_equipos, fg_color="transparent")  # Contenedor inferior de botones
    # Empaquetamos el panel de acciones
    panel_acciones_equipos.pack(fill="x", padx=20, pady=(2, 12))  # Se estira a lo ancho

    # Función que carga los datos de la fila seleccionada en el formulario para editar
    def accion_editar_equipo():  # Evento del botón Editar
        # Obtenemos la fila seleccionada en el Treeview
        seleccion = tabla_equipos.selection()  # Fila seleccionada
        # Si no hay ninguna fila seleccionada, mostramos advertencia
        if not seleccion:  # Ninguna fila elegida
            # Aviso al usuario
            messagebox.showwarning("Selección Requerida", "Por favor selecciona un equipo de la tabla para editarlo.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Extraemos los valores de la fila seleccionada (6 columnas)
        valores_fila = tabla_equipos.item(seleccion[0], "values")  # Tupla con los 6 valores
        # Guardamos el codigo_pc de la fila en la variable de edición
        codigo_pc_edicion[0] = valores_fila[0]  # Guarda el codigo_pc autogenerado
        # Asignamos el área asegurando que sea una de las 2 permitidas (Laboratorio o Bodega)
        area_seleccionada = valores_fila[1]  # Área leída de la fila
        # Si el área es Bodega la colocamos, en caso contrario dejamos Laboratorio
        combo_area_equipo.set(area_seleccionada if area_seleccionada in ["Laboratorio", "Bodega"] else "Laboratorio")  # Carga área
        # Limpiamos las cajas de texto antes de llenarlas
        caja_procesador_equipo.delete(0, "end")  # Limpia procesador
        # Insertamos el procesador de la fila
        caja_procesador_equipo.insert(0, valores_fila[2])  # Carga procesador
        # Limpiamos la caja de RAM
        caja_ram_equipo.delete(0, "end")  # Limpia RAM
        # Insertamos la RAM de la fila
        caja_ram_equipo.insert(0, valores_fila[3])  # Carga RAM
        # Limpiamos la caja de almacenamiento
        caja_almacenamiento_equipo.delete(0, "end")  # Limpia almacenamiento
        # Insertamos el almacenamiento de la fila
        caja_almacenamiento_equipo.insert(0, valores_fila[4])  # Carga almacenamiento
        # Asignamos el estado en el ComboBox
        combo_estado_equipo.set(valores_fila[5])  # Carga estado
        # Cambiamos el texto del botón por 'Actualizar' mostrando el Código PC autogenerado
        boton_guardar_equipo.configure(text=f"Actualizar Equipo (Código PC: #{valores_fila[0]})", fg_color=COLOR_ADVERTENCIA, hover_color="#D97706")  # Modo actualización

    # Función que elimina el equipo seleccionado de la base de datos previa confirmación
    def accion_eliminar_equipo():  # Evento del botón Eliminar
        # Obtenemos la selección de la tabla
        seleccion = tabla_equipos.selection()  # Fila seleccionada
        # Validamos que el usuario haya seleccionado una fila
        if not seleccion:  # Si no hay selección
            # Mostramos advertencia
            messagebox.showwarning("Selección Requerida", "Por favor selecciona un equipo de la tabla para eliminarlo.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Extraemos los datos de la fila
        valores_fila = tabla_equipos.item(seleccion[0], "values")  # Valores
        # Obtenemos el codigo_pc del equipo (posición 0)
        codigo_a_eliminar = valores_fila[0]  # Código PC numérico autogenerado
        # Solicitamos confirmación explícita al usuario antes de borrar (OWASP A05)
        confirmado = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar permanentemente la computadora con Código PC #{codigo_a_eliminar}?")  # Confirmación
        # Si el usuario confirma la eliminación
        if confirmado:  # Usuario dijo SÍ
            # Ejecutamos la eliminación segura mediante DELETE FROM ... WHERE codigo_pc = %s
            if eliminar_pc(codigo_a_eliminar):  # Borrado en MySQL por codigo_pc
                # Notificamos éxito
                messagebox.showinfo("Éxito", f"La computadora #{codigo_a_eliminar} fue eliminada correctamente.")  # Mensaje
                # Si estábamos editando ese equipo que se acaba de borrar, reseteamos el formulario
                if codigo_pc_edicion[0] == codigo_a_eliminar:  # Si coincidía con el de edición
                    # Limpiamos el formulario
                    limpiar_formulario_equipos()  # Resetea a modo nuevo registro
                # Recargamos la tabla de equipos
                cargar_tabla_equipos()  # Actualiza la vista

    # Botón '✏️ Editar' ubicado debajo de la tabla de equipos
    boton_editar_equipo = ctk.CTkButton(panel_acciones_equipos, text="✏️ Editar Seleccionada", font=("Segoe UI", 13, "bold"), fg_color=COLOR_ADVERTENCIA, text_color=COLOR_TEXTO, hover_color="#D97706", height=34, command=accion_editar_equipo)  # Botón Editar
    # Empaquetamos el botón Editar a la izquierda
    boton_editar_equipo.pack(side="left", padx=(0, 10))  # A la izquierda

    # Botón '🗑️ Eliminar' ubicado debajo de la tabla de equipos
    boton_eliminar_equipo = ctk.CTkButton(panel_acciones_equipos, text="🗑️ Eliminar Seleccionada", font=("Segoe UI", 13, "bold"), fg_color=COLOR_PELIGRO, text_color=COLOR_TEXTO, hover_color="#DC2626", height=34, command=accion_eliminar_equipo)  # Botón Eliminar
    # Empaquetamos el botón Eliminar al lado de Editar
    boton_eliminar_equipo.pack(side="left", padx=(0, 10))  # Al lado de Editar

    # Botón 'Cancelar Edición' para regresar a modo nuevo registro sin recargar
    boton_cancelar_eq = ctk.CTkButton(panel_acciones_equipos, text="Cancelar Edición", font=("Segoe UI", 12), fg_color="#475569", text_color=COLOR_TEXTO, hover_color="#334155", height=34, command=limpiar_formulario_equipos)  # Botón Cancelar
    # Empaquetamos el botón Cancelar Edición
    boton_cancelar_eq.pack(side="left")  # Ubicado al lado de Eliminar

    # Función para exportar a PDF únicamente los equipos visibles actualmente en el Treeview
    def accion_exportar_pdf():  # Evento al hacer clic en Exportar a PDF
        # Obtenemos la lista con los valores de cada fila que está en el Treeview en este momento
        filas_visibles = [tabla_equipos.item(item, "values") for item in tabla_equipos.get_children()]  # Filas visibles
        # Si la tabla no contiene filas en este momento
        if not filas_visibles:  # Verificamos si no hay equipos mostrados
            # Mostramos un aviso al usuario
            messagebox.showwarning("Sin Datos", "No hay equipos en la tabla para exportar al reporte PDF.")  # Aviso
            # Salimos de la función
            return  # Detiene la exportación
        # Leemos el filtro actualmente seleccionado en el ComboBox de área
        filtro_actual = combo_filtro_area.get()  # 'Todas las áreas', 'Laboratorio' o 'Bodega'
        # Llamamos a exportar_inventario_pdf pasando las filas visibles y el filtro aplicado
        exportar_inventario_pdf(filas_visibles, filtro_actual)  # Genera el PDF con los datos visibles

    # Botón '📄 Exportar a PDF' ubicado en la barra de acciones inferiores
    boton_exportar_pdf_acciones = ctk.CTkButton(panel_acciones_equipos, text="📄 Exportar a PDF", font=("Segoe UI", 12, "bold"), fg_color="#10B981", text_color=COLOR_TEXTO, hover_color="#059669", height=34, command=accion_exportar_pdf)  # Botón Exportar PDF inferior
    # Empaquetamos el botón a la derecha
    boton_exportar_pdf_acciones.pack(side="right")  # Alineación a la derecha

    # ==========================================================================
    # 8. MÓDULO 2: ÁREAS (EXCLUSIVAMENTE LAS 2 ÁREAS FÍSICAS: LABORATORIO Y BODEGA)
    # ==========================================================================

    # Creamos el panel contenedor para el Módulo Áreas
    panel_modulo_areas = ctk.CTkFrame(area_central, fg_color=COLOR_PANELES, corner_radius=12)  # Marco de Áreas

    # Título principal del módulo de áreas físicas
    etiqueta_titulo_areas = ctk.CTkLabel(panel_modulo_areas, text="Módulo de Áreas Físicas del Instituto", font=("Segoe UI", 20, "bold"), text_color=COLOR_TEXTO)  # Título Áreas
    # Posicionamos el título
    etiqueta_titulo_areas.pack(anchor="w", padx=20, pady=(20, 6))  # Margen superior

    # Subtítulo explicativo destacando las 2 únicas áreas físicas oficiales
    etiqueta_sub_areas = ctk.CTkLabel(panel_modulo_areas, text="Las 2 áreas físicas oficiales registradas en el sistema (Laboratorio y Bodega):", font=("Segoe UI", 13), text_color=COLOR_BOTONES)  # Subtítulo oficial
    # Posicionamos el subtítulo
    etiqueta_sub_areas.pack(anchor="w", padx=20, pady=(0, 15))  # Margen inferior

    # Contenedor para el Treeview de áreas físicas
    contenedor_tabla_areas = ctk.CTkFrame(panel_modulo_areas, fg_color=COLOR_FONDO, corner_radius=8)  # Marco de tabla Áreas
    # Empaquetamos el contenedor
    contenedor_tabla_areas.pack(fill="both", expand=True, padx=20, pady=(0, 20))  # Se expande

    # Columnas de la tabla de áreas
    columnas_areas = ("id", "nombre_area", "descripcion")  # Columnas Áreas
    # Creamos el Treeview
    tabla_areas = ttk.Treeview(contenedor_tabla_areas, columns=columnas_areas, show="headings")  # Tabla Áreas

    # Encabezados de Áreas
    tabla_areas.heading("id", text="ID")  # Título ID
    tabla_areas.heading("nombre_area", text="Área Física Oficial")  # Título Nombre
    tabla_areas.heading("descripcion", text="Propósito y Uso Operativo")  # Título Descripción

    # Ancho de columnas de Áreas
    tabla_areas.column("id", width=60, anchor="center")  # ID
    tabla_areas.column("nombre_area", width=160, anchor="center")  # Nombre
    tabla_areas.column("descripcion", width=460, anchor="w")  # Descripción

    # Empaquetamos la tabla de Áreas
    tabla_areas.pack(fill="both", expand=True, padx=6, pady=6)  # Se dibuja la tabla

    # Función que carga las 2 áreas físicas en la tabla Treeview (sin Servidores ni Redes)
    def cargar_tabla_areas():  # Llena tabla_areas
        # Borramos las filas actuales
        for fila in tabla_areas.get_children():  # Recorre filas
            # Borra fila
            tabla_areas.delete(fila)  # Elimina fila
        # Obtenemos las 2 áreas de la base de datos
        lista_areas_bd = obtener_areas()  # Lee áreas en MySQL
        # Si no hubo registros devueltos, usamos las 2 áreas oficiales de respaldo
        if not lista_areas_bd:  # Si la lista está vacía
            # Datos de respaldo con las 2 áreas oficiales
            lista_areas_bd = [  # Respaldo oficial
                (1, "Laboratorio", "Área principal para computadoras y prácticas de estudiantes en uso"),  # Laboratorio (en uso)
                (2, "Bodega", "Área de resguardo para repuestos, herramientas y equipos guardados")  # Bodega (guardados)
            ]  # Fin respaldo
        # Insertamos cada una de las 2 áreas en la tabla
        for area in lista_areas_bd:  # Recorre áreas oficiales
            # Agrega la fila al Treeview
            tabla_areas.insert("", "end", values=area)  # Dibuja fila

    # ==========================================================================
    # 9. MÓDULO 3: INVENTARIO (BUSCADOR + FORMULARIO + TREEVIEW + EDITAR Y ELIMINAR)
    # ==========================================================================

    # Creamos el panel contenedor del Módulo Inventario
    panel_modulo_inventario = ctk.CTkFrame(area_central, fg_color=COLOR_PANELES, corner_radius=12)  # Marco de Inventario

    # Título principal del módulo
    etiqueta_titulo_inv = ctk.CTkLabel(panel_modulo_inventario, text="Módulo de Inventario (Herramientas y Periféricos)", font=("Segoe UI", 20, "bold"), text_color=COLOR_TEXTO)  # Título Inventario
    # Posicionamos el título
    etiqueta_titulo_inv.pack(anchor="w", padx=20, pady=(15, 6))  # Margen superior

    # --- BUSCADOR DE INVENTARIO EN LA PARTE SUPERIOR ---
    panel_busqueda_inv = ctk.CTkFrame(panel_modulo_inventario, fg_color="transparent")  # Contenedor del buscador de inventario
    # Empaquetamos el panel del buscador
    panel_busqueda_inv.pack(fill="x", padx=20, pady=(0, 10))  # Se estira horizontalmente

    # Caja de texto para buscar artículos en inventario
    caja_buscar_inv = ctk.CTkEntry(panel_busqueda_inv, placeholder_text="Buscar artículo por nombre, categoría o estado...", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=34)  # Entry buscador inventario
    # Empaquetamos la caja de texto
    caja_buscar_inv.pack(side="left", fill="x", expand=True, padx=(0, 8))  # Ocupa el ancho disponible

    # Función que ejecuta la búsqueda de artículos con SELECT ... LIKE %s
    def accion_buscar_inventario():  # Evento del botón Buscar en inventario
        # Obtenemos el término escrito
        termino_inv = caja_buscar_inv.get().strip()  # Texto buscado
        # Si la caja está vacía, mostramos advertencia
        if not termino_inv:  # Caja vacía
            # Aviso al usuario
            messagebox.showinfo("Búsqueda", "Ingresa un término para buscar en inventario.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Consultamos los artículos usando la sentencia preparada LIKE %s
        resultados_inv = buscar_articulos_inventario(termino_inv)  # Búsqueda segura
        # Limpiamos las filas actuales del Treeview
        for fila in tabla_inventario.get_children():  # Recorre filas
            # Borra fila
            tabla_inventario.delete(fila)  # Elimina fila
        # Insertamos los artículos coincidentes en la tabla
        for item in resultados_inv:  # Recorre resultados
            # Dibuja fila
            tabla_inventario.insert("", "end", values=item)  # Inserta fila filtrada

    # Función para limpiar el filtro del inventario y mostrar todos los registros
    def accion_limpiar_inventario():  # Evento del botón Limpiar Filtro
        # Limpiamos la caja de búsqueda
        caja_buscar_inv.delete(0, "end")  # Limpia caja
        # Recargamos todos los artículos de inventario desde MySQL
        cargar_tabla_inventario()  # Muestra todos los artículos

    # Botón '🔎 Buscar' del inventario
    boton_buscar_inv = ctk.CTkButton(panel_busqueda_inv, text="🔎 Buscar", font=("Segoe UI", 12, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, width=100, height=34, command=accion_buscar_inventario)  # Botón Buscar Inventario
    # Empaquetamos el botón Buscar
    boton_buscar_inv.pack(side="left", padx=(0, 6))  # Ubicado al lado de la caja

    # Botón 'Limpiar Filtro' del inventario
    boton_limpiar_inv = ctk.CTkButton(panel_busqueda_inv, text="Limpiar Filtro", font=("Segoe UI", 12), fg_color="#475569", text_color=COLOR_TEXTO, hover_color="#334155", width=110, height=34, command=accion_limpiar_inventario)  # Botón Limpiar Inventario
    # Empaquetamos el botón Limpiar Filtro
    boton_limpiar_inv.pack(side="left")  # Ubicado a la derecha del botón Buscar

    # --- FORMULARIO DE INVENTARIO ---
    # Variable mutable que guarda el ID del artículo en edición (None si es nuevo)
    id_item_edicion = [None]  # Rastreador del ID en edición

    # Marco del formulario de inventario
    form_inventario = ctk.CTkFrame(panel_modulo_inventario, fg_color="transparent")  # Marco del formulario
    # Empaquetamos el formulario
    form_inventario.pack(fill="x", padx=20, pady=(0, 8))  # Se estira a lo ancho
    # Configuramos 2 columnas iguales
    form_inventario.grid_columnconfigure(0, weight=1)  # Columna 0
    form_inventario.grid_columnconfigure(1, weight=1)  # Columna 1

    # Campo 1: Nombre (Entry)
    etiqueta_nom_inv = ctk.CTkLabel(form_inventario, text="Nombre (Pinzas, Cables, Teclados, etc.):", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta
    etiqueta_nom_inv.grid(row=0, column=0, sticky="w", padx=4, pady=(0, 2))  # Fila 0, Columna 0
    caja_nombre_inventario = ctk.CTkEntry(form_inventario, placeholder_text="Ej: Pinza Ponchadora RJ45 / Teclado USB", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=32)  # Entry
    caja_nombre_inventario.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 6))  # Fila 1, Columna 0

    # Campo 2: Categoría (ComboBox)
    etiqueta_cat_inv = ctk.CTkLabel(form_inventario, text="Categoría:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta
    etiqueta_cat_inv.grid(row=0, column=1, sticky="w", padx=4, pady=(0, 2))  # Fila 0, Columna 1
    combo_categoria_inventario = ctk.CTkComboBox(form_inventario, values=["Herramienta", "Periférico"], fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, button_color=COLOR_BOTONES, dropdown_fg_color=COLOR_PANELES, dropdown_text_color=COLOR_TEXTO, state="readonly", height=32)  # ComboBox
    combo_categoria_inventario.set("Herramienta")  # Opción inicial
    combo_categoria_inventario.grid(row=1, column=1, sticky="ew", padx=4, pady=(0, 6))  # Fila 1, Columna 1

    # Campo 3: Cantidad (Entry numérico)
    etiqueta_cant_inv = ctk.CTkLabel(form_inventario, text="Cantidad:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta
    etiqueta_cant_inv.grid(row=2, column=0, sticky="w", padx=4, pady=(0, 2))  # Fila 2, Columna 0
    caja_cantidad_inventario = ctk.CTkEntry(form_inventario, placeholder_text="Ej: 15", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=32)  # Entry
    caja_cantidad_inventario.grid(row=3, column=0, sticky="ew", padx=4, pady=(0, 6))  # Fila 3, Columna 0

    # Campo 4: Estado (ComboBox)
    etiqueta_est_inv = ctk.CTkLabel(form_inventario, text="Estado:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta
    etiqueta_est_inv.grid(row=2, column=1, sticky="w", padx=4, pady=(0, 2))  # Fila 2, Columna 1
    combo_estado_inventario = ctk.CTkComboBox(form_inventario, values=["Disponible", "En Uso", "Dañado"], fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, button_color=COLOR_BOTONES, dropdown_fg_color=COLOR_PANELES, dropdown_text_color=COLOR_TEXTO, state="readonly", height=32)  # ComboBox
    combo_estado_inventario.set("Disponible")  # Opción inicial
    combo_estado_inventario.grid(row=3, column=1, sticky="ew", padx=4, pady=(0, 6))  # Fila 3, Columna 1

    # Función que guarda o actualiza un artículo según id_item_edicion
    def accion_guardar_o_actualizar_inventario():  # Evento del botón principal de inventario
        # Obtenemos los valores del formulario
        nombre = caja_nombre_inventario.get().strip()  # Nombre
        categoria = combo_categoria_inventario.get()  # Categoría
        cantidad_texto = caja_cantidad_inventario.get().strip()  # Cantidad
        estado = combo_estado_inventario.get()  # Estado

        # Validamos que los campos obligatorios contengan texto
        if not nombre or not cantidad_texto:  # Si falta algún campo
            # Mostramos advertencia al usuario
            messagebox.showwarning("Campos Incompletos", "Por favor ingresa el Nombre y la Cantidad del artículo.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción

        # Validamos que la cantidad sea un número entero
        if not cantidad_texto.isdigit():  # Si no es un entero positivo
            # Mostramos advertencia
            messagebox.showwarning("Cantidad Inválida", "La cantidad debe ser un número entero (ej: 10).")  # Aviso
            # Salimos de la función
            return  # Detiene la acción

        # CASO 1: Inserción de un nuevo artículo en inventario
        if id_item_edicion[0] is None:  # Nuevo artículo
            # Llamamos a registrar_articulo_inventario() con sentencia preparada (%s)
            if registrar_articulo_inventario(nombre, categoria, int(cantidad_texto), estado):  # Si se guardó en MySQL
                # Notificamos éxito
                messagebox.showinfo("Éxito", f"El artículo '{nombre}' fue registrado en el inventario.")  # Mensaje
                # Limpiamos el formulario
                limpiar_formulario_inventario()  # Vuelve a modo nuevo registro
                # Recargamos la tabla
                cargar_tabla_inventario()  # Actualiza la vista
        # CASO 2: Actualización de un artículo existente por su ID
        else:  # Modo actualización
            # Obtenemos el ID del artículo que se está editando
            id_a_actualizar = id_item_edicion[0]  # ID numérico
            # Llamamos a actualizar_articulo_inventario() que ejecuta UPDATE ... WHERE id = %s
            if actualizar_articulo_inventario(id_a_actualizar, nombre, categoria, int(cantidad_texto), estado):  # Si se actualizó
                # Notificamos éxito
                messagebox.showinfo("Éxito", f"El artículo '{nombre}' (ID: {id_a_actualizar}) fue actualizado exitosamente.")  # Mensaje
                # Limpiamos el formulario
                limpiar_formulario_inventario()  # Vuelve a modo registro normal
                # Recargamos la tabla
                cargar_tabla_inventario()  # Actualiza la vista

    # Función auxiliar para vaciar el formulario de inventario y restablecer el botón
    def limpiar_formulario_inventario():  # Restablece formulario de inventario
        # Vaciamos la variable de edición
        id_item_edicion[0] = None  # Regresa a modo nuevo registro
        # Limpiamos las cajas de texto
        caja_nombre_inventario.delete(0, "end")  # Limpia nombre
        caja_cantidad_inventario.delete(0, "end")  # Limpia cantidad
        combo_categoria_inventario.set("Herramienta")  # Restablece categoría
        combo_estado_inventario.set("Disponible")  # Restablece estado
        # Restauramos el texto y color del botón principal
        boton_guardar_inv.configure(text="Registrar en Inventario", fg_color=COLOR_BOTONES, hover_color="#0284C7")  # Botón estándar

    # Botón dinámico del formulario de inventario
    boton_guardar_inv = ctk.CTkButton(form_inventario, text="Registrar en Inventario", font=("Segoe UI", 13, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, hover_color="#0284C7", height=34, command=accion_guardar_o_actualizar_inventario)  # Botón Guardar/Actualizar
    # Ubicamos el botón ocupando las 2 columnas del formulario
    boton_guardar_inv.grid(row=4, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 2))  # Fila 4 completa

    # --- TABLA TREEVIEW DE INVENTARIO ---
    # Contenedor para el Treeview de inventario
    contenedor_tabla_inv = ctk.CTkFrame(panel_modulo_inventario, fg_color=COLOR_FONDO, corner_radius=8)  # Marco de la tabla
    # Empaquetamos el contenedor
    contenedor_tabla_inv.pack(fill="both", expand=True, padx=20, pady=(2, 6))  # Se expande

    # Columnas del Treeview de Inventario (incluyendo 'id' para editar y eliminar)
    columnas_inv = ("id", "nombre", "categoria", "cantidad", "estado")  # 5 columnas
    # Creamos el Treeview de inventario
    tabla_inventario = ttk.Treeview(contenedor_tabla_inv, columns=columnas_inv, show="headings")  # Tabla Inventario

    # Encabezados de las 5 columnas
    tabla_inventario.heading("id", text="ID")  # Título ID
    tabla_inventario.heading("nombre", text="Nombre del Artículo")  # Título Nombre
    tabla_inventario.heading("categoria", text="Categoría")  # Título Categoría
    tabla_inventario.heading("cantidad", text="Cantidad")  # Título Cantidad
    tabla_inventario.heading("estado", text="Estado")  # Título Estado

    # Ancho de las 5 columnas
    tabla_inventario.column("id", width=50, anchor="center")  # ID centrado
    tabla_inventario.column("nombre", width=250, anchor="w")  # Nombre a la izquierda
    tabla_inventario.column("categoria", width=140, anchor="center")  # Categoría
    tabla_inventario.column("cantidad", width=90, anchor="center")  # Cantidad
    tabla_inventario.column("estado", width=130, anchor="center")  # Estado

    # Barra de desplazamiento vertical para la tabla de inventario
    scroll_inv = ctk.CTkScrollbar(contenedor_tabla_inv, orientation="vertical", command=tabla_inventario.yview, fg_color=COLOR_PANELES, button_color=COLOR_BOTONES)  # Scrollbar
    # Vinculamos la tabla con la barra
    tabla_inventario.configure(yscrollcommand=scroll_inv.set)  # Sincronización
    # Empaquetamos la barra y la tabla
    scroll_inv.pack(side="right", fill="y", padx=(0, 4), pady=4)  # Barra a la derecha
    tabla_inventario.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)  # Tabla a la izquierda

    # Función que recarga los artículos en la tabla de inventario desde MySQL
    def cargar_tabla_inventario():  # Actualiza el Treeview
        # Borramos las filas actuales
        for fila in tabla_inventario.get_children():  # Recorre filas actuales
            # Borra fila
            tabla_inventario.delete(fila)  # Elimina fila
        # Obtenemos los registros desde la base de datos
        for articulo in obtener_articulos_inventario():  # Recorre artículos
            # Inserta la fila en la tabla
            tabla_inventario.insert("", "end", values=articulo)  # Agrega fila

    # --- BOTONES DE ACCIÓN DEBAJO DE LA TABLA DE INVENTARIO (EDITAR Y ELIMINAR) ---
    panel_acciones_inv = ctk.CTkFrame(panel_modulo_inventario, fg_color="transparent")  # Contenedor inferior de acciones
    # Empaquetamos el panel de acciones
    panel_acciones_inv.pack(fill="x", padx=20, pady=(2, 12))  # Se estira a lo ancho

    # Función que carga el artículo seleccionado en el formulario para editarlo
    def accion_editar_inventario():  # Evento del botón Editar en inventario
        # Obtenemos la selección del Treeview
        seleccion = tabla_inventario.selection()  # Fila seleccionada
        # Si no hay selección, mostramos advertencia
        if not seleccion:  # Ninguna fila seleccionada
            # Aviso al usuario
            messagebox.showwarning("Selección Requerida", "Por favor selecciona un artículo de la tabla para editarlo.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Extraemos los valores de la fila
        valores_fila = tabla_inventario.item(seleccion[0], "values")  # Tupla de 5 valores
        # Guardamos el ID del artículo en la variable de edición
        id_item_edicion[0] = valores_fila[0]  # Guarda el ID
        # Limpiamos las cajas de texto antes de llenarlas
        caja_nombre_inventario.delete(0, "end")  # Limpia nombre
        caja_cantidad_inventario.delete(0, "end")  # Limpia cantidad
        # Cargamos los datos del artículo en el formulario
        caja_nombre_inventario.insert(0, valores_fila[1])  # Carga nombre
        combo_categoria_inventario.set(valores_fila[2])  # Carga categoría
        caja_cantidad_inventario.insert(0, valores_fila[3])  # Carga cantidad
        combo_estado_inventario.set(valores_fila[4])  # Carga estado
        # Cambiamos el texto del botón a 'Actualizar' y le damos color ámbar
        boton_guardar_inv.configure(text=f"Actualizar Artículo (ID: {valores_fila[0]})", fg_color=COLOR_ADVERTENCIA, hover_color="#D97706")  # Modo actualización

    # Función que elimina el artículo seleccionado de MySQL previa confirmación
    def accion_eliminar_inventario():  # Evento del botón Eliminar en inventario
        # Obtenemos la selección del Treeview
        seleccion = tabla_inventario.selection()  # Fila seleccionada
        # Si no hay selección, mostramos advertencia
        if not seleccion:  # Ninguna fila seleccionada
            # Aviso al usuario
            messagebox.showwarning("Selección Requerida", "Por favor selecciona un artículo de la tabla para eliminarlo.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Extraemos los valores de la fila seleccionada
        valores_fila = tabla_inventario.item(seleccion[0], "values")  # Valores
        # Obtenemos el ID del artículo (posición 0)
        id_a_eliminar = valores_fila[0]  # ID del artículo
        # Obtenemos el nombre del artículo (posición 1)
        nombre_a_eliminar = valores_fila[1]  # Nombre del artículo
        # Pedimos confirmación al usuario antes de borrar
        confirmado = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar permanentemente el artículo '{nombre_a_eliminar}' (ID: {id_a_eliminar})?")  # Confirmación
        # Si el usuario confirma la acción
        if confirmado:  # Usuario dijo SÍ
            # Ejecutamos la eliminación segura mediante DELETE FROM ... WHERE id = %s
            if eliminar_articulo_inventario(id_a_eliminar):  # Borrado en MySQL
                # Notificamos éxito
                messagebox.showinfo("Éxito", f"El artículo '{nombre_a_eliminar}' fue eliminado correctamente.")  # Mensaje
                # Si estábamos editando este artículo, reseteamos el formulario
                if id_item_edicion[0] == id_a_eliminar:  # Coincide con edición
                    # Limpiamos el formulario
                    limpiar_formulario_inventario()  # Vuelve a modo nuevo registro
                # Recargamos la tabla de inventario
                cargar_tabla_inventario()  # Actualiza la vista

    # Botón '✏️ Editar' de inventario
    boton_editar_inv = ctk.CTkButton(panel_acciones_inv, text="✏️ Editar Seleccionada", font=("Segoe UI", 13, "bold"), fg_color=COLOR_ADVERTENCIA, text_color=COLOR_TEXTO, hover_color="#D97706", height=34, command=accion_editar_inventario)  # Botón Editar
    # Empaquetamos el botón Editar a la izquierda
    boton_editar_inv.pack(side="left", padx=(0, 10))  # A la izquierda

    # Botón '🗑️ Eliminar' de inventario
    boton_eliminar_inv = ctk.CTkButton(panel_acciones_inv, text="🗑️ Eliminar Seleccionada", font=("Segoe UI", 13, "bold"), fg_color=COLOR_PELIGRO, text_color=COLOR_TEXTO, hover_color="#DC2626", height=34, command=accion_eliminar_inventario)  # Botón Eliminar
    # Empaquetamos el botón Eliminar al lado de Editar
    boton_eliminar_inv.pack(side="left", padx=(0, 10))  # Al lado de Editar

    # Botón 'Cancelar Edición' de inventario
    boton_cancelar_inv = ctk.CTkButton(panel_acciones_inv, text="Cancelar Edición", font=("Segoe UI", 12), fg_color="#475569", text_color=COLOR_TEXTO, hover_color="#334155", height=34, command=limpiar_formulario_inventario)  # Botón Cancelar
    # Empaquetamos el botón Cancelar Edición
    boton_cancelar_inv.pack(side="left")  # Ubicado al lado de Eliminar

    # ==========================================================================
    # 10. MÓDULO 4: CONTROL DE USUARIOS (SEGURIDAD OWASP A02 Y A03)
    # ==========================================================================

    # Creamos el panel contenedor del Módulo Usuarios
    panel_modulo_usuarios = ctk.CTkFrame(area_central, fg_color=COLOR_PANELES, corner_radius=12)  # Marco de Usuarios

    # Título principal del módulo de usuarios
    etiqueta_titulo_usuarios = ctk.CTkLabel(panel_modulo_usuarios, text="Módulo de Control de Usuarios (Criptografía Bcrypt - OWASP A02)", font=("Segoe UI", 20, "bold"), text_color=COLOR_TEXTO)  # Título Usuarios
    # Posicionamos el título
    etiqueta_titulo_usuarios.pack(anchor="w", padx=20, pady=(15, 6))  # Margen superior

    # Subtítulo explicativo sobre la seguridad de contraseñas
    etiqueta_sub_usuarios = ctk.CTkLabel(panel_modulo_usuarios, text="Las contraseñas se almacenan con salt criptográfico irreversible. Nunca se muestra el hash en pantalla.", font=("Segoe UI", 12), text_color=COLOR_BOTONES)  # Subtítulo
    # Posicionamos el subtítulo
    etiqueta_sub_usuarios.pack(anchor="w", padx=20, pady=(0, 10))  # Margen inferior

    # --- BUSCADOR DE USUARIOS EN LA PARTE SUPERIOR ---
    panel_busqueda_usr = ctk.CTkFrame(panel_modulo_usuarios, fg_color="transparent")  # Contenedor del buscador de usuarios
    # Empaquetamos el panel del buscador
    panel_busqueda_usr.pack(fill="x", padx=20, pady=(0, 10))  # Se estira a lo ancho

    # Caja de texto para buscar usuarios por su nombre
    caja_buscar_usr = ctk.CTkEntry(panel_busqueda_usr, placeholder_text="Buscar usuario por nombre de cuenta...", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=34)  # Entry buscador usuario
    # Empaquetamos la caja de texto
    caja_buscar_usr.pack(side="left", fill="x", expand=True, padx=(0, 8))  # Ocupa el espacio disponible

    # Función que busca usuarios por nombre usando sentencia preparada LIKE %s
    def accion_buscar_usuario():  # Evento del botón Buscar Usuario
        # Obtenemos el nombre buscado
        termino_usr = caja_buscar_usr.get().strip()  # Texto ingresado
        # Si la caja está vacía, mostramos aviso
        if not termino_usr:  # Si está vacía
            # Aviso informativo
            messagebox.showinfo("Búsqueda", "Ingresa un nombre de usuario para buscar.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Consultamos los usuarios coincidentes
        resultados_usr = buscar_usuarios(termino_usr)  # Consulta segura con %s
        # Limpiamos el Treeview de usuarios
        for fila in tabla_usuarios.get_children():  # Recorre filas
            # Borra fila
            tabla_usuarios.delete(fila)  # Elimina fila
        # Insertamos solo los usuarios encontrados (ID y Nombre, nunca el hash)
        for usuario in resultados_usr:  # Recorre filas
            # Agrega la fila al Treeview
            tabla_usuarios.insert("", "end", values=usuario)  # Muestra usuario

    # Función para limpiar el filtro de búsqueda y ver todos los usuarios
    def accion_limpiar_usuario():  # Evento del botón Limpiar Filtro en usuarios
        # Vaciamos la caja de texto
        caja_buscar_usr.delete(0, "end")  # Limpia la caja
        # Recargamos todos los usuarios de la base de datos
        cargar_tabla_usuarios()  # Muestra todos los usuarios

    # Botón '🔎 Buscar' de usuarios
    boton_buscar_usr = ctk.CTkButton(panel_busqueda_usr, text="🔎 Buscar", font=("Segoe UI", 12, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, width=100, height=34, command=accion_buscar_usuario)  # Botón Buscar
    # Empaquetamos el botón Buscar
    boton_buscar_usr.pack(side="left", padx=(0, 6))  # Al lado de la caja

    # Botón 'Limpiar Filtro' de usuarios
    boton_limpiar_usr = ctk.CTkButton(panel_busqueda_usr, text="Limpiar Filtro", font=("Segoe UI", 12), fg_color="#475569", text_color=COLOR_TEXTO, hover_color="#334155", width=110, height=34, command=accion_limpiar_usuario)  # Botón Limpiar
    # Empaquetamos el botón Limpiar
    boton_limpiar_usr.pack(side="left")  # Al lado del botón Buscar

    # --- FORMULARIO PARA REGISTRAR NUEVO USUARIO (BCRYPT OWASP A02) ---
    form_usuarios = ctk.CTkFrame(panel_modulo_usuarios, fg_color="transparent")  # Marco del formulario de usuarios
    # Empaquetamos el marco del formulario
    form_usuarios.pack(fill="x", padx=20, pady=(0, 10))  # Se estira horizontalmente
    # Configuramos 2 columnas de igual ancho
    form_usuarios.grid_columnconfigure(0, weight=1)  # Columna 0
    form_usuarios.grid_columnconfigure(1, weight=1)  # Columna 1

    # Campo 1: Nombre de Usuario (Entry)
    etiqueta_nom_usr = ctk.CTkLabel(form_usuarios, text="Nombre de Usuario:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta
    etiqueta_nom_usr.grid(row=0, column=0, sticky="w", padx=4, pady=(0, 2))  # Fila 0, Columna 0
    caja_usuario_nuevo = ctk.CTkEntry(form_usuarios, placeholder_text="Ej: docente_lab / tecnico1", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=32)  # Entry
    caja_usuario_nuevo.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 6))  # Fila 1, Columna 0

    # Campo 2: Contraseña (Entry con show="*" para ocultar texto)
    etiqueta_pass_usr = ctk.CTkLabel(form_usuarios, text="Contraseña (Se cifrará con Bcrypt):", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXTO)  # Etiqueta
    etiqueta_pass_usr.grid(row=0, column=1, sticky="w", padx=4, pady=(0, 2))  # Fila 0, Columna 1
    caja_contrasena_nueva = ctk.CTkEntry(form_usuarios, placeholder_text="Ingresa la contraseña segura", show="*", fg_color=COLOR_FONDO, text_color=COLOR_TEXTO, border_color=COLOR_BOTONES, height=32)  # Entry contraseña
    caja_contrasena_nueva.grid(row=1, column=1, sticky="ew", padx=4, pady=(0, 6))  # Fila 1, Columna 1

    # Función que guarda un nuevo usuario cifrando su contraseña con bcrypt
    def accion_guardar_usuario():  # Evento del botón Registrar Usuario
        # Obtenemos el nombre de usuario escrito
        nombre_usr = caja_usuario_nuevo.get().strip()  # Usuario ingresado
        # Obtenemos la contraseña en texto plano ingresada
        clave_plana = caja_contrasena_nueva.get().strip()  # Contraseña ingresada

        # Validamos que no se dejen campos vacíos
        if not nombre_usr or not clave_plana:  # Validación
            # Alerta al usuario
            messagebox.showwarning("Campos Incompletos", "Por favor ingresa tanto el Nombre de Usuario como la Contraseña.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción

        # Validamos una longitud mínima de seguridad para la contraseña
        if len(clave_plana) < 4:  # Mínimo 4 caracteres
            # Advertencia de seguridad
            messagebox.showwarning("Contraseña Débil", "La contraseña debe tener al menos 4 caracteres.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción

        # Llamamos a registrar_usuario() que cifra con bcrypt y ejecuta INSERT INTO ... VALUES (%s, %s)
        if registrar_usuario(nombre_usr, clave_plana):  # Si se registró con éxito en MySQL
            # Notificamos éxito indicando la protección bcrypt
            messagebox.showinfo("Éxito", f"El usuario '{nombre_usr}' fue registrado exitosamente con cifrado seguro Bcrypt.")  # Mensaje
            # Limpiamos las cajas de texto del formulario
            caja_usuario_nuevo.delete(0, "end")  # Limpia usuario
            caja_contrasena_nueva.delete(0, "end")  # Limpia clave
            # Recargamos la tabla de usuarios
            cargar_tabla_usuarios()  # Actualiza la vista

    # Botón 'Registrar Usuario'
    boton_guardar_usr = ctk.CTkButton(form_usuarios, text="Registrar Usuario Seguro (Bcrypt)", font=("Segoe UI", 13, "bold"), fg_color=COLOR_BOTONES, text_color=COLOR_TEXTO, hover_color="#0284C7", height=34, command=accion_guardar_usuario)  # Botón
    # Ubicamos el botón ocupando las 2 columnas del formulario
    boton_guardar_usr.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 2))  # Fila 2 completa

    # --- TABLA TREEVIEW DE USUARIOS (SOLO ID Y USUARIO, NUNCA EL HASH) ---
    contenedor_tabla_usr = ctk.CTkFrame(panel_modulo_usuarios, fg_color=COLOR_FONDO, corner_radius=8)  # Marco de la tabla
    # Empaquetamos el contenedor
    contenedor_tabla_usr.pack(fill="both", expand=True, padx=20, pady=(2, 6))  # Se expande

    # Columnas del Treeview de Usuarios (estrictamente solo ID y Usuario por seguridad OWASP)
    columnas_usr = ("id", "usuario")  # 2 columnas seguras
    # Creamos el Treeview
    tabla_usuarios = ttk.Treeview(contenedor_tabla_usr, columns=columnas_usr, show="headings")  # Tabla Usuarios

    # Encabezados de las 2 columnas
    tabla_usuarios.heading("id", text="ID")  # Título ID
    tabla_usuarios.heading("usuario", text="Nombre de Usuario")  # Título Nombre de Usuario

    # Ancho de las columnas
    tabla_usuarios.column("id", width=70, anchor="center")  # ID centrado
    tabla_usuarios.column("usuario", width=450, anchor="w")  # Nombre de usuario a la izquierda

    # Barra de desplazamiento vertical para la tabla de usuarios
    scroll_usr = ctk.CTkScrollbar(contenedor_tabla_usr, orientation="vertical", command=tabla_usuarios.yview, fg_color=COLOR_PANELES, button_color=COLOR_BOTONES)  # Scrollbar
    # Conectamos la tabla con la barra
    tabla_usuarios.configure(yscrollcommand=scroll_usr.set)  # Sincronización
    # Empaquetamos la barra y la tabla
    scroll_usr.pack(side="right", fill="y", padx=(0, 4), pady=4)  # Barra a la derecha
    tabla_usuarios.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)  # Tabla a la izquierda

    # Función que recarga los usuarios en la tabla desde MySQL
    def cargar_tabla_usuarios():  # Actualiza tabla_usuarios
        # Borramos las filas actuales
        for fila in tabla_usuarios.get_children():  # Recorre filas actuales
            # Borra fila
            tabla_usuarios.delete(fila)  # Elimina fila
        # Obtenemos la lista de usuarios (solo ID y Usuario)
        for usuario in obtener_usuarios():  # Recorre usuarios de MySQL
            # Insertamos la fila en la tabla
            tabla_usuarios.insert("", "end", values=usuario)  # Agrega fila

    # --- BOTONES DE ACCIÓN DEBAJO DE LA TABLA DE USUARIOS (ELIMINAR Y CAMBIAR CONTRASEÑA) ---
    panel_acciones_usr = ctk.CTkFrame(panel_modulo_usuarios, fg_color="transparent")  # Contenedor inferior de acciones
    # Empaquetamos el panel de acciones
    panel_acciones_usr.pack(fill="x", padx=20, pady=(2, 12))  # Se estira a lo ancho

    # Función que permite cambiar la contraseña de un usuario cifrándola con bcrypt
    def accion_cambiar_contrasena():  # Evento del botón Cambiar Contraseña
        # Obtenemos la selección del Treeview
        seleccion = tabla_usuarios.selection()  # Fila seleccionada
        # Si no hay fila seleccionada, mostramos advertencia
        if not seleccion:  # Ningún usuario elegido
            # Aviso al usuario
            messagebox.showwarning("Selección Requerida", "Por favor selecciona un usuario de la tabla para cambiar su contraseña.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Extraemos los datos de la fila seleccionada
        valores_fila = tabla_usuarios.item(seleccion[0], "values")  # Valores de usuario
        # Obtenemos el ID del usuario
        id_usr_cambio = valores_fila[0]  # ID del usuario
        # Obtenemos el nombre del usuario
        nombre_usr_cambio = valores_fila[1]  # Nombre del usuario
        # Abrimos un cuadro de diálogo moderno para pedir la nueva contraseña
        dialogo = ctk.CTkInputDialog(text=f"Ingresa la nueva contraseña para el usuario '{nombre_usr_cambio}':", title="Cambiar Contraseña (Bcrypt)")  # Diálogo de entrada
        # Capturamos la nueva contraseña escrita por el administrador
        nueva_clave = dialogo.get_input()  # Entrada del usuario
        # Si el usuario presionó Cancelar o no escribió nada
        if nueva_clave is None or not nueva_clave.strip():  # Entrada vacía o cancelada
            # Salimos sin realizar cambios
            return  # Detiene la acción
        # Validamos que la nueva contraseña tenga longitud adecuada
        if len(nueva_clave.strip()) < 4:  # Mínimo 4 caracteres
            # Advertencia de seguridad
            messagebox.showwarning("Contraseña Inválida", "La nueva contraseña debe tener al menos 4 caracteres.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Llamamos a cambiar_contrasena_usuario() que cifra con bcrypt y ejecuta UPDATE ... WHERE id_usuario = %s
        if cambiar_contrasena_usuario(id_usr_cambio, nueva_clave.strip()):  # Actualización en MySQL
            # Notificamos éxito
            messagebox.showinfo("Éxito", f"La contraseña de '{nombre_usr_cambio}' fue actualizada y cifrada con Bcrypt exitosamente.")  # Mensaje

    # Función que elimina un usuario previa confirmación (protegiendo al admin principal)
    def accion_eliminar_usuario():  # Evento del botón Eliminar Usuario
        # Obtenemos la selección del Treeview
        seleccion = tabla_usuarios.selection()  # Fila seleccionada
        # Si no hay fila seleccionada, mostramos advertencia
        if not seleccion:  # Ningún usuario elegido
            # Aviso al usuario
            messagebox.showwarning("Selección Requerida", "Por favor selecciona un usuario de la tabla para eliminarlo.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Extraemos los datos de la fila
        valores_fila = tabla_usuarios.item(seleccion[0], "values")  # Valores
        # Obtenemos el ID del usuario
        id_usr_eliminar = valores_fila[0]  # ID del usuario
        # Obtenemos el nombre del usuario
        nombre_usr_eliminar = valores_fila[1]  # Nombre del usuario
        # Si el usuario es el 'admin' principal, evitamos su eliminación para no bloquear el sistema
        if str(nombre_usr_eliminar).strip().lower() == "admin":  # Protección de cuenta admin
            # Advertencia de seguridad
            messagebox.showwarning("Acción Bloqueada", "Por motivos de seguridad del laboratorio, la cuenta 'admin' principal no puede ser eliminada.")  # Aviso
            # Salimos de la función
            return  # Detiene la acción
        # Pedimos confirmación al usuario antes de borrar la cuenta
        confirmado = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar permanentemente al usuario '{nombre_usr_eliminar}' (ID: {id_usr_eliminar})?")  # Confirmación
        # Si el usuario confirma
        if confirmado:  # Usuario dijo SÍ
            # Ejecutamos DELETE FROM usuarios WHERE id_usuario = %s
            if eliminar_usuario(id_usr_eliminar):  # Borrado en MySQL
                # Notificamos éxito
                messagebox.showinfo("Éxito", f"El usuario '{nombre_usr_eliminar}' fue eliminado correctamente.")  # Mensaje
                # Recargamos la tabla de usuarios
                cargar_tabla_usuarios()  # Actualiza la vista

    # Botón '🔑 Cambiar Contraseña'
    boton_cambiar_pass = ctk.CTkButton(panel_acciones_usr, text="🔑 Cambiar Contraseña", font=("Segoe UI", 13, "bold"), fg_color=COLOR_ADVERTENCIA, text_color=COLOR_TEXTO, hover_color="#D97706", height=34, command=accion_cambiar_contrasena)  # Botón Cambiar Contraseña
    # Empaquetamos el botón a la izquierda
    boton_cambiar_pass.pack(side="left", padx=(0, 10))  # A la izquierda

    # Botón '🗑️ Eliminar Usuario'
    boton_eliminar_usr = ctk.CTkButton(panel_acciones_usr, text="🗑️ Eliminar Usuario", font=("Segoe UI", 13, "bold"), fg_color=COLOR_PELIGRO, text_color=COLOR_TEXTO, hover_color="#DC2626", height=34, command=accion_eliminar_usuario)  # Botón Eliminar Usuario
    # Empaquetamos el botón al lado de Cambiar Contraseña
    boton_eliminar_usr.pack(side="left")  # Al lado de Cambiar Contraseña

    # ==========================================================================
    # 11. INICIALIZACIÓN POR DEFECTO DEL DASHBOARD Y BUCLE PRINCIPAL
    # ==========================================================================

    # Mostramos inicialmente el Módulo 1: Equipos al abrir la aplicación
    mostrar_modulo_equipos()  # Despliega Equipos como vista inicial

    # Iniciamos el bucle principal de eventos de CustomTkinter para mantener la ventana activa
    ventana_dashboard.mainloop()  # Bucle principal de la interfaz gráfica
