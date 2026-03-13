const el = (id) => document.getElementById(id);

const statusEl = el("status");

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? "#b91c1c" : "#166534";
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Erro na requisicao.");
  }
  return data;
}

el("btnGenerate").addEventListener("click", async () => {
  try {
    const bits = Number(el("bits").value || 16);
    const p = el("manualP").value.trim();
    const q = el("manualQ").value.trim();

    let payload;
    if (p && q) {
      payload = { p, q };
    } else if (!p && !q) {
      payload = { bits };
    } else {
      throw new Error("Informe os dois valores (p e q) ou deixe ambos vazios.");
    }

    const data = await postJson("/api/generate", payload);

    el("generatedPublicE").value = data.e;
    el("generatedPrivateD").value = data.d;
    el("generatedN").value = data.n;
    el("phi").value = data.phi;
    el("primeP").value = data.p;
    el("primeQ").value = data.q;

    // Preenche os campos digitaveis para facilitar testes.
    el("encryptE").value = data.e;
    el("encryptN").value = data.n;
    el("decryptD").value = data.d;
    el("decryptN").value = data.n;

    setStatus("Par de chaves gerado com sucesso.");
  } catch (err) {
    setStatus(err.message, true);
  }
});

el("btnEncrypt").addEventListener("click", async () => {
  try {
    const message = el("plainText").value;
    const e = el("encryptE").value.trim();
    const n = el("encryptN").value.trim();

    if (!e || !n) {
      throw new Error("Informe a chave publica (e, n) para cifrar.");
    }

    const data = await postJson("/api/encrypt", { message, e, n });
    el("cipherTextResult").value = data.ciphertext_text;
    setStatus("Mensagem cifrada com a chave publica.");
  } catch (err) {
    setStatus(err.message, true);
  }
});

el("btnDecrypt").addEventListener("click", async () => {
  try {
    const ciphertext = el("cipherTextInput").value;
    const d = el("decryptD").value.trim();
    const n = el("decryptN").value.trim();

    if (!d || !n) {
      throw new Error("Informe a chave privada (d, n) para decifrar.");
    }

    const data = await postJson("/api/decrypt", { ciphertext, d, n });
    el("decryptedText").value = data.message;
    setStatus("Mensagem decifrada com a chave privada.");
  } catch (err) {
    setStatus(err.message, true);
  }
});
