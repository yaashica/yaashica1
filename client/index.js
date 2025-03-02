const checkWaterQuality = async () => {
    const tds = document.getElementById("tds").value;
    const turbidity = document.getElementById("turbidity").value;
    const temperature = document.getElementById("temperature").value;
    const conductivity = document.getElementById("conductivity").value;
    
    if (!tds || !turbidity || !temperature || !conductivity) {
        alert("Please enter all values!");
        return;
    }

    const SERVER_URL = "https://yaashica1.onrender.com";
    const isWaterPotable = async () => {
        const res = await fetch(`${SERVER_URL}/predict`, {
            method: "POST",
            body: JSON.stringify({ features: [tds, turbidity, temperature, conductivity] })
        });
        const resJson = await res.json();
        return resJson.prediction;
    };
    const outputCard = document.getElementById("output");

    outputCard.classList.remove("potable", "not-potable", "show");

    if (await isWaterPotable()) {
        outputCard.innerText = "✅ Water is Potable!";
        outputCard.classList.add("potable");
    } else {
        outputCard.innerText = "❌ Water is NOT Potable!";
        outputCard.classList.add("not-potable");
    }
    outputCard.classList.add("show");
};