// HEADER
// Description : "reservation" is a page where customers can choose date, options and others for their future travel. Here the codes.
// Date : 09/10/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : json p236, cree + session storage, liste trip_booking (ltrip_booking_table), faire table trip_booking


function travel() {
    //no inputs, no outputs
    //call when the web page loads
    //display information about travel selected and display the picture of travel 

    id = new URLSearchParams(window.location.search).get('id');
    //title of travel
    document.getElementById('title_travel').innerHTML = trip_table[id].dest;

    //image of travel
    key = trip_table[id].images_dictio_keys
    document.getElementById('imgtravel').src = '../images/' + trip_table[id].image(key) + '.jpg';

    //description of travel (descriptions created by chatGPT)
    let description_travel = trip_table[id].desc
    document.getElementById("description_travel").innerHTML = description_travel

    //price of one night 
    let key_price = trip_table[id].price_dictio_keys
    document.getElementById("price_night").innerHTML = 'Prix par adulte pour une nuit : ' + trip_table[id].price(key_price[0]) + '€'

    //show the option of pet 
    key_option = trip_table[id].option_dictio_keys
    if (trip_table[id].option(key_option[1])){
        document.getElementById('pet_option').style.display = "block";
    }
    else{
        document.getElementById('pet_option').style.display = "none";
    }
}


function price() {
    //no inputs, no outputs
    //call when changing inputs
    //travel price calculation and display

    //take the price of trip 
    let id = new URLSearchParams(window.location.search).get('id');
    key_price = trip_table[id].price_dictio_keys
    let price_adults = trip_table[id].price(key_price[0])

    //number of people
    let number_adults = Number(document.getElementsByName('number_adults')[0].value);
    let number_children = Number(document.getElementsByName('number_children')[0].value);

    //date of travel
    let from_date = new Date(document.getElementById('from_date').value);
    let to_date = new Date(document.getElementById('to_date').value);
    let time_travel = (to_date.getTime() - from_date.getTime()) / (3600000 * 24);
    

    price_travel = 0;
    price_travel = time_travel * (number_adults * price_adults + number_children * price_adults * 40/100);
    
    //Option breakfast
    if ( document.getElementsByName('breakfast')[0].checked == true) {
        price_travel = price_travel + trip_table[id].price(key_price[1]) * (number_adults + number_children)
    }

    //Option pet
    if (document.getElementsByName('pet')[0].checked == true) {
        price_travel = price_travel + 20;
    }

    //show the price
    document.getElementById('price_travel').innerHTML = '';
    document.getElementById('price_travel').innerHTML = 'Coût : ' + price_travel + '€';

    // impossible issus so display price = 0
    if (number_adults < 0 || number_children < 0 || !(Number.isInteger(number_adults)) || !(Number.isInteger(number_children)) || price_travel < 0){
            document.getElementById('price_travel').innerHTML = 'Coût : ' + 0 + '€';
    }
}



function date_valid() {
    //no inputs, no outputs
    //call when changing inputs from_date or to_date
    //send an alert if from_date is after to_date 
    let from_date = new Date(document.getElementById('from_date').value);
    let to_date = new Date(document.getElementById('to_date').value);
    let time_travel = to_date.getTime() - from_date.getTime();
    if (time_travel<0){
        alert("Date invalide : date de = " + from_date + ',   date de retour = ' + to_date )
        document.getElementById('from_date').value  = "0000-00-00";
        document.getElementById('to_date').value  = "0000-00-00";
    }
}


function children_alone() {
    //no inputs, no outputs
    //call when changing inputs
    //send an alert if there is no adult to travel 
    let number_adults = Number(document.getElementsByName('number_adults')[0].value);

    if (number_adults == 0 ){
        alert("Les enfants doivent être accompagné d'au moins un adulte")
    }
}

function data() {
    //no inputs, no outputs
    //call when click on button
    //put information of trip in session storage

    var data_trip_json = sessionStorage.getItem("trip_booking");

    if ( typeof data_trip_json == 'object'){
        var data_trip = [] //create list of trip
    }
    else{
        var data_trip = JSON.parse(data_trip_json); // take the list of trip in JSON
    }

    data_trip.push(new Trip_booking(new URLSearchParams(window.location.search).get('id'),
                                            document.getElementById('from_date').value,
                                            document.getElementById('to_date').value,
                                            document.getElementsByName('number_adults')[0].value,
                                            document.getElementsByName('number_children')[0].value,
                                            document.getElementsByName('breakfast')[0].checked,
                                            document.getElementsByName('pet')[0].checked,
                                            price_travel))
    var new_data_trip_json = JSON.stringify(data_trip);
    sessionStorage.setItem("trip_booking",new_data_trip_json);
}




function other_travel(){
    //no inputs, no outputs
    //call when the web page loads
    //display 3 other travel

    var id1 = id;
    while (id1 == id || id1 + 1 == id || id1 + 2 == id ){
        id1 = Math.floor(Math.random() * ((trip_table.length) - 2));
        var id2 = id1 + 1;
        var id3 = id1 + 2;
    }
    
    document.getElementById('travel1').href = "reservation.html?id=" + id1
    document.getElementById('travel2').href = "reservation.html?id=" + id2
    document.getElementById('travel3').href = "reservation.html?id=" + id3

    var key = trip_table[id1].images_dictio_keys
    document.getElementById('travel_img1').src = '../images/' + trip_table[id1].image(key) + '.jpg';
    document.getElementById('travel_title1').innerHTML = trip_table[id1].dest;

    key = trip_table[id2].images_dictio_keys
    document.getElementById('travel_img2').src = '../images/' + trip_table[id2].image(key) + '.jpg';
    document.getElementById('travel_title2').innerHTML = trip_table[id2].dest;
    
    key = trip_table[id3].images_dictio_keys
    document.getElementById('travel_img3').src = '../images/' + trip_table[id3].image(key) + '.jpg';
    document.getElementById('travel_title3').innerHTML = trip_table[id3].dest;
}


function fun_to_call_after_trip_table(){
    travel()
    other_travel()
}


init_trip_table_then_call(fun_to_call_after_trip_table)


//chargement du header et du footer
$('header').load("header.html")
$('footer').load("footer.html")