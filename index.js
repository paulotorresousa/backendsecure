const express = require("express");
const cors = require("cors");
const firebaseAdmin = require("firebase-admin");
const { verifyTotp } = require("./totpRoutes");

const app = express();
app.use(cors());
app.use(express.json());

// Inicializando o Firebase Admin SDK
const serviceAccount = require("./serviceAccountKey.json");

firebaseAdmin.initializeApp({
  credential: firebaseAdmin.credential.cert(serviceAccount),
});

app.post("/verifyTotp", verifyTotp);

app.listen(3000, () => {
  console.log("Backend rodando na porta 3000");
});
