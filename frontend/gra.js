const API = "http://127.0.0.1:8000";

const TLUMACZENIA = {
    "Overwhelmingly Positive": "Przytłaczająco pozytywne",
    "Very Positive": "Bardzo pozytywne",
    "Positive": "Pozytywne",
    "Mostly Positive": "W większości pozytywne",
    "Mixed": "Mieszane",
    "Mostly Negative": "W większości negatywne",
    "Negative": "Negatywne",
    "Very Negative": "Bardzo negatywne",
    "Overwhelmingly Negative": "Przytłaczająco negatywne",
};

const id = new URLSearchParams(window.location.search).get("id");

function ustawOkladke(gra) {
    const img = document.getElementById("okladka");
    if (!gra.steam_appid) {
        if (gra.image) img.src = gra.image;
        return;
    }
    const baza = `https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/${gra.steam_appid}`;
    img.src = `${baza}/library_600x900.jpg`;
    img.onerror = () => {
        img.onerror = () => {
            img.onerror = null;
            if (gra.image) img.src = gra.image;
        };
        img.src = `${baza}/header.jpg`;
    };
}

async function wczytajSteam(appId) {
    try {
        const odp = await fetch(`${API}/steam/details/${appId}`);
        if (!odp.ok) throw new Error("blad");
        const d = await odp.json();

        document.getElementById("opis").textContent = d.opis || "";

        if (d.metacritic) {
            document.getElementById("metacritic").textContent = d.metacritic ?? "brak danych";
        }
        if (d.steam_ocena) {
            document.getElementById("steam-ocena").textContent =
                TLUMACZENIA[d.steam_ocena] || d.steam_ocena;

            const razem = (d.pozytywne || 0) + (d.negatywne || 0);
            if (razem > 0) {
                const procent = Math.round((d.pozytywne / razem) * 100);
                document.getElementById("steam-liczby").textContent =
                    `${procent}% z ${razem.toLocaleString("pl-PL")} recenzji`;
            }
        }
    } catch (blad) {
        console.error("Szczegóły ze Steama:", blad);
    }
}

async function wczytajGre() {
    try {
        const odp = await fetch(`${API}/gry/${id}`);
        if (!odp.ok) throw new Error("brak gry");
        const gra = await odp.json();

        document.title = gra.tytul;
        document.getElementById("tytul").textContent = gra.tytul;
        document.getElementById("moja-ocena").textContent =
            gra.ocena ? `Moja ocena: ${gra.ocena}/10` : "Moja ocena: brak";
        ustawOkladke(gra);

        if (gra.steam_appid) wczytajSteam(gra.steam_appid);
    } catch (blad) {
        console.error(blad);
        document.getElementById("tytul").textContent = "Nie znaleziono gry";
    }
}

wczytajGre();