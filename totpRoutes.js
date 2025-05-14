const admin = require("./firebase");
const speakeasy = require("speakeasy");

const verifyTotp = async (req, res) => {
  const { userId, token } = req.body;

  try {
    // Recupera o segredo TOTP armazenado no Firestore
    const userDoc = await admin.firestore().collection("users").doc(userId).get();
    const user = userDoc.data();

    if (!user || !user.totpSecret) {
      return res.status(400).send("Usuário não encontrado ou segredo TOTP não configurado.");
    }

    // Verifica o token com o segredo
    const verified = speakeasy.totp.verify({
      secret: user.totpSecret,
      encoding: "base32",
      token,
    });

    if (verified) {
      return res.status(200).send("Código TOTP válido!");
    } else {
      return res.status(400).send("Código TOTP inválido!");
    }
  } catch (error) {
    console.error("Erro ao verificar TOTP:", error);
    return res.status(500).send("Erro interno ao verificar o código.");
  }
};

module.exports = { verifyTotp };
