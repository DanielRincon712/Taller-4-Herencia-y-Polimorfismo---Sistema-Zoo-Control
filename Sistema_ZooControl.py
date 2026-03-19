"""
Sistema de Gestión de Zoológico
================================
Integra encapsulamiento, herencia, polimorfismo y composición.
"""

# ══════════════════════════════════════════════════════════
# CLASE BASE: ANIMAL
# ══════════════════════════════════════════════════════════
class Animal:
    def __init__(self, identificador, especie, peso):
        self.__identificador = identificador  # Atributo privado
        self.__especie = especie              # Atributo privado
        self.__peso = peso                    # Atributo privado

    # --- Getters ---
    def get_identificador(self):
        return self.__identificador

    def get_especie(self):
        return self.__especie

    def get_peso(self):
        return self.__peso

    # --- Setters con validación ---
    def set_peso(self, nuevo_peso):
        if nuevo_peso > 0:
            self.__peso = nuevo_peso
        else:
            print("Error: El peso de un animal no puede ser negativo o cero.")

    def mostrar_info(self):
        return f"[{self.__identificador}] Especie: {self.__especie} | Peso: {self.__peso}kg"

    # ── NUEVO: método polimórfico (debe ser implementado por cada subclase) ──
    def calcular_racion_diaria(self):
        raise NotImplementedError(
            f"La clase '{type(self).__name__}' debe implementar calcular_racion_diaria()."
        )


# ══════════════════════════════════════════════════════════
# SUBCLASE: MAMIFERO
# Ración diaria = 5% del peso corporal en carne (kg)
# ══════════════════════════════════════════════════════════
class Mamifero(Animal):
    PORCENTAJE_RACION = 0.05  # Constante de clase: 5%

    def __init__(self, identificador, especie, peso, meses_gestacion):
        super().__init__(identificador, especie, peso)
        self.__meses_gestacion = meses_gestacion  # Atributo privado de Mamifero

    def get_meses_gestacion(self):
        return self.__meses_gestacion

    # ── NUEVO: polimorfismo — sobreescritura del método de Animal ──
    def calcular_racion_diaria(self):
        """Retorna el 5% del peso corporal en kg de carne por día."""
        return round(self.get_peso() * self.PORCENTAJE_RACION, 2)


# ══════════════════════════════════════════════════════════
# SUBCLASE: REPTIL
# Ración = 2 roedores por semana → ración diaria = 2/7
# ══════════════════════════════════════════════════════════
class Reptil(Animal):
    ROEDORES_POR_SEMANA = 2

    def __init__(self, identificador, especie, peso, es_venenoso):
        super().__init__(identificador, especie, peso)
        self.__es_venenoso = es_venenoso  # Booleano

    def get_es_venenoso(self):
        return "Sí" if self.__es_venenoso else "No"

    # ── NUEVO: polimorfismo — sobreescritura del método de Animal ──
    def calcular_racion_diaria(self):
        """Retorna la ración diaria en roedores (fracción de la semana)."""
        return round(self.ROEDORES_POR_SEMANA / 7, 4)


# ══════════════════════════════════════════════════════════
# CLASE BASE DEL INVENTARIO
# ══════════════════════════════════════════════════════════
class ItemInventario:
    def __init__(self, codigo, nombre, cantidad):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__cantidad = cantidad  # Atributo privado — se modifica vía método

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    # ── NUEVO: setter con validación para reducir stock ──
    def reducir_stock(self, cantidad):
        """Descuenta 'cantidad' del stock disponible con validación."""
        if cantidad <= 0:
            print(f"  ⚠ Cantidad inválida ({cantidad}). Debe ser mayor a 0.")
            return
        if cantidad > self.__cantidad:
            print(
                f"  ⚠ Stock insuficiente de '{self.__nombre}'. "
                f"Disponible: {self.__cantidad}, requerido: {cantidad}."
            )
            return
        self.__cantidad -= cantidad
        print(
            f"  ✔ '{self.__nombre}': descontado {cantidad}. "
            f"Stock restante: {self.__cantidad}."
        )

    # Método polimórfico (a sobreescribir en las subclases)
    def gestionar_uso(self):
        return "Uso genérico no definido."


# ══════════════════════════════════════════════════════════
# SUBCLASES DE INVENTARIO
# ══════════════════════════════════════════════════════════
class Alimento(ItemInventario):
    def __init__(self, codigo, nombre, cantidad, tipo_dieta):
        super().__init__(codigo, nombre, cantidad)
        self.__tipo_dieta = tipo_dieta

    def gestionar_uso(self):
        return (
            f"ALIMENTO [{self.get_nombre()}]: Distribuir en zona de animales "
            f"de dieta '{self.__tipo_dieta}'. Quedan {self.get_cantidad()} kg/unidades."
        )


class ImplementoAseo(ItemInventario):
    def __init__(self, codigo, nombre, cantidad, area_asignada):
        super().__init__(codigo, nombre, cantidad)
        self.__area_asignada = area_asignada

    def gestionar_uso(self):
        return (
            f"MANTENIMIENTO [{self.get_nombre()}]: Entregar al personal "
            f"de la zona '{self.__area_asignada}'. Stock: {self.get_cantidad()}."
        )


class Medicina(ItemInventario):
    def __init__(self, codigo, nombre, cantidad, requiere_refrigeracion):
        super().__init__(codigo, nombre, cantidad)
        self.__requiere_refrigeracion = requiere_refrigeracion

    def gestionar_uso(self):
        refri_txt = "EN NEVERA" if self.__requiere_refrigeracion else "A TEMPERATURA AMBIENTE"
        return (
            f"VETERINARIA [{self.get_nombre()}]: Uso médico estricto. "
            f"Almacenar {refri_txt}. Unidades: {self.get_cantidad()}."
        )


# ══════════════════════════════════════════════════════════
# FUNCIÓN DE ALIMENTACIÓN DIARIA (conecta Animal con Alimento)
# ══════════════════════════════════════════════════════════
def alimentar_animal(animal, alimento_inventario):
    """
    Calcula la ración diaria del animal (polimorfismo)
    y descuenta esa cantidad del stock del alimento.
    """
    racion = animal.calcular_racion_diaria()
    print(f"\n🐾 {animal.mostrar_info()}")
    print(f"   Ración diaria calculada: {racion} unidades/kg")
    alimento_inventario.reducir_stock(racion)


# ══════════════════════════════════════════════════════════
# PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":

    # ── Bloque 1: prueba de encapsulamiento (el código original) ──
    print("─" * 55)
    print("  BLOQUE 1: Encapsulamiento y validación")
    print("─" * 55)
    animal_generico = Animal("A001", "Desconocida", 50.5)
    print(animal_generico.mostrar_info())
    animal_generico.set_peso(55.0)
    print(f"Nuevo peso actualizado: {animal_generico.get_peso()}kg")
    animal_generico.set_peso(-10)  # Debe mostrar error

    # ── Bloque 2: prueba de herencia (el código original) ──
    print("\n" + "─" * 55)
    print("  BLOQUE 2: Herencia")
    print("─" * 55)
    leon  = Mamifero("M001", "León Africano", 190.0, 3.5)
    cobra = Reptil("R001", "Cobra Real", 6.0, True)
    print(leon.mostrar_info(),  f"| Gestación: {leon.get_meses_gestacion()} meses")
    print(cobra.mostrar_info(), f"| Venenoso: {cobra.get_es_venenoso()}")

    # ── Bloque 3: inventario con polimorfismo (el código original) ──
    print("\n" + "─" * 55)
    print("  BLOQUE 3: Inventario — polimorfismo en gestionar_uso()")
    print("─" * 55)
    lista_inventario = [
        Alimento("AL-01", "Carne de Res", 150, "Carnívoro"),
        Alimento("AL-02", "Pacas de Heno", 300, "Herbívoro"),
        ImplementoAseo("IM-01", "Escoba de Cerda Dura", 15, "Jaulas Felinos"),
        ImplementoAseo("IM-02", "Pala Recolectora", 8, "Zona Elefantes"),
        Medicina("MD-01", "Antibiótico Amplio Espectro", 50, True),
    ]
    for item in lista_inventario:
        print(item.gestionar_uso())

    # ── Bloque 4: NUEVO — calcular_racion_diaria + reducir_stock ──
    print("\n" + "─" * 55)
    print("  BLOQUE 4: Ración diaria + descuento de stock")
    print("─" * 55)

    # Alimentos del inventario que usarán los animales
    carne   = Alimento("AL-01", "Carne de Res", 150, "Carnívoro")
    roedores = Alimento("AL-03", "Roedores", 20, "Carnívoro")

    # Animales del zoológico
    tigre  = Mamifero("M002", "Tigre Bengala", 220.0, 3.7)
    iguana = Reptil("R002", "Iguana Verde", 4.0, False)

    # calcular_racion_diaria() → polimorfismo (Mamifero vs Reptil)
    # reducir_stock()          → encapsulamiento en ItemInventario
    alimentar_animal(leon,   carne)
    alimentar_animal(tigre,  carne)
    alimentar_animal(cobra,  roedores)
    alimentar_animal(iguana, roedores)

    print("\n📦 Stock final de alimentos:")
    print(f"   {carne.get_nombre()}: {carne.get_cantidad()} kg")
    print(f"   {roedores.get_nombre()}: {roedores.get_cantidad()} unidades")

    # ── Prueba de error controlado ──
    print("\n⚠  Prueba stock insuficiente:")
    roedores.reducir_stock(100)  # Más de lo disponible

    print("\n" + "─" * 55)