// HEADER
// Description : Definition of trip_table. Requires trip.js to be work.
// Date : 24/11/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : adjusting the value of destinations in the json

function build_trip_table(trip_data_json){
    //Builds trip_table with trip instances
    trip_table = []
    for (trip of trip_data_json){
        trip_table.push(new Trip(trip._dest, trip._option_dictio, trip._price_dictio, trip._img_dictio, trip._desc, trip._is_city, 
            trip._longitude, trip._latitude))
    }
}

async function fetch_trip_table(){
    const reponse = await fetch('../database/trip_data.json');
    const trip_data_json = await reponse.json();
    build_trip_table(trip_data_json)
}

async function init_trip_table_then_call(f){
    var trip_table_in_storage = sessionStorage.getItem("trip_table")
    if (trip_table_in_storage == null){
        await fetch_trip_table()
        sessionStorage.setItem("trip_table", JSON.stringify(trip_table))
    }
    else{
        build_trip_table(JSON.parse(trip_table_in_storage))
    }

    //function should need trip_table to work
    f()
}