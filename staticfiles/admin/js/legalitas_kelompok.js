// document.addEventListener(
//     "DOMContentLoaded",
//     function () {
//             console.log(document.getElementById("id_kelompok"));
            
//          const kelompok =
//             document.getElementById(
//                 "id_kelompok"
//             );

//         const item =
//             document.getElementById(
//                 "id_itemLegalitas"
//             );

//         if (!kelompok || !item) {
//             return;
//         }

//         kelompok.addEventListener(
//             "change",
//             function () {
//                 console.log("JS masuk");

       
//                 fetch(
//                     "/ajax/item-legalitas/?kelompok_id="
//                     + this.value
//                 )
//                 .then(
//                     r => r.json()
//                 )
//                 .then(data => {

//                     item.innerHTML = "";

//                     data.forEach(i => {

//                         const opt =
//                             document.createElement(
//                                 "option"
//                             );

//                         opt.value = i.id;

//                         opt.textContent =
//                             i.nmILega;

//                         item.appendChild(
//                             opt
//                         );
//                     });

//                 });

//             }
//         );

//     }
// );

document.addEventListener("DOMContentLoaded", function () {

    
    const kelompok = document.getElementById("id_kelompok");

    kelompok.onchange = function () {

        const kelompokId = this.value;

        console.log(
            "Kelompok:",
            kelompokId
        );

        fetch(
            `/ajax/item-legalitas/?kelompok_id=${kelompokId}`
        )
        .then(response => response.json())
        .then(data => {

            console.log(
                "Item Legalitas:",
                data
            );

            const itemLegalitas =
                document.getElementById(
                    "id_itemLegalitas"
                );

            itemLegalitas.innerHTML =
                '<option value="">---------</option>';

            data.forEach(item => {

                const option =
                    document.createElement(
                        "option"
                    );

                option.value = item.id;

                option.textContent =
                    item.nmILega;

                itemLegalitas.appendChild(
                    option
                );

            });

        })
        .catch(error => {
            console.error(error);
        });

    };


});