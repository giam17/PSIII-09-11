import { crearApp } from "./app.js";

const app = crearApp();
const servidor = app.listen(Number(process.env.PORT ?? 3000), "127.0.0.1", () => {
  console.log("Servidor en http://127.0.0.1:" + servidor.address().port);
});
