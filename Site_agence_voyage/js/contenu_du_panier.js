// HEADER
// Description : "contenu du panier" is a page where customers can see what they are about to book. Here the codes.
// Date : 09/10/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : 

//Data
dest_list_id = "dest_list";
template_id = document.getElementById(dest_list_id).firstElementChild.id;

//Functions
function build_trip_booking_table(trip_data_json){
    //Builds trip_table with trip instances
    trip_booking_table = []
    for (trip of trip_data_json){
        trip_booking_table.push(new Trip_booking(trip._id, trip._from_date, trip._to_date, trip._number_adults, trip._number_children, trip._breakfast, 
            trip._pet, trip._price))
    }
}

function calculate_total(){
    total = 0
    for (trip of trip_booking_table){
        total = total + trip.price
    }
    document.getElementById('total').innerText = 'Total : ' + total
}

function init_trip_booking_table(){
    var trip_booking_table_in_storage = sessionStorage.getItem("trip_booking")
    if (!(trip_booking_table_in_storage == null)){
        build_trip_booking_table(JSON.parse(trip_booking_table_in_storage))
    }
    else{
        trip_booking_table = []
    }
    calculate_total()
}

function fun_to_call_after_trip_table(){
    init_is_dest_visible()
    init_trip_booking_table()
    for (trip of trip_booking_table){
        add_dest(trip.id)
        load_trip_info(trip)
    }
}

function del_trip_from_trip_booking_table(id){
    new_trip_booking_table = []
    for (trip of trip_booking_table){
        if (id != trip.id){
            new_trip_booking_table.push(trip)
        }
    }
    trip_booking_table = new_trip_booking_table
}

function del_dest_properly(id){
    if (window.confirm("Etes-vous vraiment sur de vouloir supprimer votre voyage ?")){
        del_dest(id)
        total = total - trip_booking_table[id].price
        del_trip_from_trip_booking_table(id)
        sessionStorage.setItem("trip_booking", JSON.stringify(trip_booking_table))
    }
}

function load_trip_info(trip){
    let dest_div = document.getElementById('dest_' + trip.id)
    if (trip.breakfast){
    breakfast = 'avec'
    }
    else{
        breakfast = 'sans'
    }
    new_content = dest_div.innerHTML
        .replace(/{{grown_up}}/g, trip.number_adults)
        .replace(/{{children}}/g, trip.number_children)
        .replace(/{{from}}/g, trip.from_date)
        .replace(/{{end}}/g, trip.to_date)
        .replace(/{{grown_up}}/g, trip._number_adults)
        .replace(/{{breakfast}}/g, breakfast)

    dest_div.innerHTML = new_content
}

//Main program
init_trip_table_then_call(fun_to_call_after_trip_table)

//chargement du header et du footer
$('header').load("header.html")
$('footer').load("footer.html")