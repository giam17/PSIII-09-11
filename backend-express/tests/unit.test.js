import test from "node:test";
import assert from "node:assert/strict";
import { crearMascota } from "../src/mascotas.js";

test("unitaria: crear una mascota quitando espacios", () => {
  const mascota = crearMascota(1, " Luna ", " Gato ");

  assert.deepEqual(mascota, { id: 1, nombre: "Luna", especie: "Gato" });
});
