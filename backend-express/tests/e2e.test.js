import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";

test("e2e: registrar y consultar una mascota por HTTP", { timeout: 15000 }, async (t) => {
  const proceso = spawn(process.execPath, ["src/server.js"], {
    cwd: new URL("../", import.meta.url),
    env: { ...process.env, PORT: "0" },
    stdio: ["ignore", "pipe", "inherit"],
  });
  const cierre = once(proceso, "close");
  t.after(async () => {
    proceso.kill();
    await cierre;
  });

  const url = await new Promise((resolve, reject) => {
    const limite = setTimeout(() => reject(new Error("El servidor no inicio a tiempo")), 10000);
    let salida = "";
    proceso.stdout.on("data", (datos) => {
      salida += datos.toString();
      const direccion = salida.match(/http:\/\/127\.0\.0\.1:\d+/);
      if (direccion) {
        clearTimeout(limite);
        resolve(direccion[0]);
      }
    });
    proceso.once("error", (error) => {
      clearTimeout(limite);
      reject(error);
    });
    proceso.once("exit", (codigo) => {
      clearTimeout(limite);
      reject(new Error("El servidor termino con codigo " + codigo));
    });
  });

  const inicial = await fetch(url + "/mascotas");
  assert.equal(inicial.status, 200);
  assert.deepEqual(await inicial.json(), []);

  const respuesta = await fetch(url + "/mascotas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre: "Luna", especie: "Gato" }),
  });
  assert.equal(respuesta.status, 201);
  const mascota = await respuesta.json();
  assert.deepEqual(mascota, { id: 1, nombre: "Luna", especie: "Gato" });

  const consulta = await fetch(url + "/mascotas/" + mascota.id);
  assert.equal(consulta.status, 200);
  assert.deepEqual(await consulta.json(), mascota);

  const listado = await fetch(url + "/mascotas");
  assert.equal(listado.status, 200);
  assert.deepEqual(await listado.json(), [mascota]);
});
