import test from "node:test";
import assert from "node:assert/strict";
import request from "supertest";
import { crearApp } from "../src/app.js";

test("integracion: rechazar una mascota incompleta sin guardarla", async () => {
  const app = crearApp();

  const respuesta = await request(app).post("/mascotas").send({ nombre: "Luna" });
  assert.equal(respuesta.status, 400);
  assert.deepEqual(respuesta.body, { error: "Nombre y especie son obligatorios" });

  const listado = await request(app).get("/mascotas");
  assert.equal(listado.status, 200);
  assert.deepEqual(listado.body, []);
});
