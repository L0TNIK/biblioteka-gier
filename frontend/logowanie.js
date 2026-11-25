const API = "http://127.0.0.1:8000";

// przechwytuje wyslanie formularza logowania, pobiera token i przenosi na strone glowna
document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const blad = document.getElementById("blad");
    blad.textContent = ""

    try{
        const odp = await fetch(`${API}/logowanie`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nazwa: document.getElementById("nazwa").value.trim(),
                haslo: document.getElementById("haslo").value,
            }),
        });
        const dane = await odp.json();

        if(!odp.ok){
            blad.textContent = typeof dane.detail === "string" ? dane.detail : "Sprawdz dane w formularzu."
            return;
        }
        localStorage.setItem("token", dane.access_token);
        window.location.href = "strona-glowna.html";
    }
    catch(err){
        blad.textContent = "nioe mozna polaczyc sie z serwerem.";
    }
});