const payload = {
    family: id,
    guests: checked
};

fetch("/confirm", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
})
.then(r => r.json())
.then(data => {

    if(data.success){

        alert("Спасибо! ❤️");

    }else{

        alert("Ошибка отправки.");

    }

});