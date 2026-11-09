import express from "express";
import { crearMascota } from "./mascotas.js";

export function crearApp() {
  const app = express();
  const mascotas = [];
  app.use(express.json());

  app.get("/mascotas", (req, res) => {
    res.json(mascotas);
  });

  app.get("/mascotas/:id", (req, res) => {
    const mascota = mascotas.find((item) => item.id === Number(req.params.id));
    if (!mascota) {
      return res.status(404).json({ error: "Mascota no encontrada" });
    }
    res.json(mascota);
  });

  app.post("/mascotas", (req, res) => {
    const { nombre, especie } = req.body ?? {};
    let mascota;
    try {
      mascota = crearMascota(mascotas.length + 1, nombre, especie);
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
    mascotas.push(mascota);
    res.status(201).json(mascota);
  });

  return app;
}
