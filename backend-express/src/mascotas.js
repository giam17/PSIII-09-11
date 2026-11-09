export function crearMascota(id, nombre, especie) {
  if (typeof nombre !== "string" || typeof especie !== "string" || !nombre.trim() || !especie.trim()) {
    throw new Error("Nombre y especie son obligatorios");
  }

  return { id, nombre: nombre.trim(), especie: especie.trim() };
}
