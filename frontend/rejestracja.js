const API = "http://127.0.0.1:8000";

// sprawdza czy hasla sie zgadzaja, zaklada konto przez api i przenosi na strone glowna
document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const blad = document.getElementById("blad");
    blad.textContent = "";

    const haslo = document.getElementById("haslo");
    const powtorzHaslo = document.getElementById("powtorzHaslo");
    if(haslo.value !== powtorzHaslo.value){
        blad.textContent = "hasla nie sa takie same.";
        return;
    }

    try{
        const odp = await fetch(`${API}/rejestracja`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nazwa: document.getElementById("nazwa").value.trim(),
                email: document.getElementById("email").value.trim(),
                haslo: haslo.value,
            }),
        });
        const dane = await odp.json()

        if(!odp.ok){
            blad.textContent = typeof dane.detail === "string"
                ? dane.detail
                : "Nazwa: min. 3 znaki, haslo min 8 znakow.";
            return;
        }
        localStorage.setItem("token", dane.access_token);
        window.location.href = "strona-glowna.html";
    }
    catch(err){
        blad.textContent = "nie mozna polaczyc sie z serwerem";;
    }
});