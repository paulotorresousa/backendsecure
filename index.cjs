const express = require("express");
const app = express();
const speakeasy = require("speakeasy");
const firebaseAdmin = require("firebase-admin");

app.use(express.json());

const serviceAccount = require("./path/to/your/serviceAccountKey.json"); // Atualize o caminho

firebaseAdmin.initializeApp({
  credential: firebaseAdmin.credential.cert(serviceAccount),
});

app.post("/verifyTotp", (req, res) => {
  const { token, userId } = req.body;

  const db = firebaseAdmin.firestore();
  const userRef = db.collection("users").doc(userId);

  userRef
    .get()
    .then((doc) => {
      if (!doc.exists) {
        return res.status(404).send("Usuário não encontrado");
      }

      const userData = doc.data();
      const secret = userData.secret;

      const verified = speakeasy.totp.verify({
        secret,
        encoding: "base32",
        token,
      });

      if (verified) {
        return res.status(200).send("Token verificado com sucesso");
      } else {
        return res.status(400).send("Token inválido");
      }
    })
    .catch((error) => {
      console.error("Erro ao verificar o TOTP:", error);
      res.status(500).send("Erro no servidor");
    });
});

app.listen(3000, () => {
  console.log("Servidor rodando na porta 3000");
});

