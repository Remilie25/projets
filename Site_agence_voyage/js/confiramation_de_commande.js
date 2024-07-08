// HEADER
// Description : "Confirmation de commande" is a page where customers can confirm their purchase. Here the codes.
// Date : 09/10/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : input space auto and / auto


function name_capitalize() {
    //no inputs, not outputs
    //call when changing input name 
    //capitalize the first lettre of name in input
    const name = document.getElementById("name");
    name.value = name.value[0].toUpperCase() + name.value.slice(1);
  }


function number_phone_space(){
    //no inputs, not outputs 
    //call when changing input phone
    //put a space every two numbers in input
    const phone = document.getElementById("phone");

    if(phone.value.slice(2,3) != ' ' && phone.value.slice(5,6) != ' ' && phone.value.slice(8,9) != ' ' && phone.value.slice(11,12) != ' ' ){ //see if user put space between number
        let space =  phone.value.slice(0,2) + ' ' + phone.value.slice(2,4) + ' ' + phone.value.slice(4,6) + ' ' + phone.value.slice(6,8) + ' ' +phone.value.slice(8,10);
        phone.value = space
    }
    
}

function number_carte_space(){
    //no inputs, not outputs 
    //call when changing input bankcarte
    //put a space every four numbers in input

    const bankcarte  = document.getElementById("bankcarte");

    if (bankcarte.value.slice(4,5) != ' ' && bankcarte.value.slice(9,10) != ' ' && bankcarte.value.slice(14,15) != ' '){ //see if user put space between number
        let space = bankcarte.value.slice(0,4) + ' ' + bankcarte.value.slice(4,8) + ' ' + bankcarte.value.slice(8,12) + ' ' + bankcarte.value.slice(12,16)
        bankcarte.value = space
    }
}

function date_carte() {
    //no inputs, not outputs 
    //call when changing input monthcarte
    //put / between month and year in input
    const monthcarte = document.getElementById("monthcarte")
    let x = monthcarte.value.slice(0,2) + '/' + monthcarte.value.slice(2,4);
    monthcarte.value = x
}


function data() {
    //no inputs, no outputs
    //call when click on button
    //put information to buy in session storage 
    var data_buy = { 
        name : document.getElementById('name').value,
        codepostal : document.getElementById('postalcode').value,
        city : document.getElementById('city').value,
        street : document.getElementById('street').value,
        email : document.getElementById('email').value,
        phone : document.getElementById('phone').value,
        bankcarte : document.getElementById('bankcarte').value,
        monthcarte : document.getElementById('monthcarte').value,
        CVC : document.getElementById('CVC').value
    }
    
    var data_buy_json = JSON.stringify(data_buy);
    sessionStorage.setItem("buy_information",data_buy_json);
}

//chargement du header et du footer
$('header').load("header.html")
$('footer').load("footer.html")