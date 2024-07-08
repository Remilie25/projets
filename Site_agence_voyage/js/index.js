// HEADER
// Description : "index" is the main page of a booking site of a travel agency. Here the codes.
// Date : 09/10/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : filter on temp, tracking of dest in global view, style of filter btn

//Data
dest_list_id = "dest_list";
template_id = document.getElementById(dest_list_id).firstElementChild.id;
by_price_bool = false;
city_only_bool = false;
out_city_bool = false;

//Functions
function city_only(){
    if (city_only_bool){
        city_only_bool = false;
        document.getElementById('city_only_btn').style.background = '';
    }
    else{
        city_only_bool = true;
        document.getElementById('city_only_btn').style.background = 'green';
    }
    hide_dest_filter()
}

function out_city_only(){
    if (out_city_bool){
        out_city_bool = false;
        document.getElementById('out_city_btn').style.background = '';
    }
    else{
        out_city_bool = true;
        document.getElementById('out_city_btn').style.background = 'green';
    }
    hide_dest_filter()
}

function by_price(){
    if (by_price_bool){
        by_price_bool = false;
        document.getElementById("filter3").style.display = 'none';
        document.getElementById('by_price_btn').style.background = ''

    }
    else{
        by_price_bool = true;
        document.getElementById("filter3").style.display = 'inline';
        document.getElementById('by_price_btn').style.background = 'green'

    }
    hide_dest_filter()
}

function hide_dest_filter(){
    console.log('h w')
    var p_min = parseInt($("#price_min").val());
    var p_max = parseInt($("#price_max").val());
    
    for (id in trip_table){
        let trip = trip_table[id];
        if((by_price_bool && (p_min > trip.price("by_n") || p_max < trip.price("by_n"))) || (out_city_bool && trip.is_city) || (city_only_bool && !trip.is_city)){ //add cond for city and countryside
            document.getElementById("dest_" + id).style.display = 'none';
        }
        else{
            document.getElementById("dest_" + id).style.display = 'inline';
        }
    }
}

async function set_temp(){
    for (id in trip_table){
        let trip = trip_table[id];
        // let API_key = console.error('please enter here your API_key')
        const api_main_url = "https://api.openweathermap.org/data/2.5/weather?lat=";
        response = await fetch(api_main_url + trip.latitude + "&lon=" + trip.longitude + "&appid=" + API_key);
        weather_data = await response.json();
        trip.temp = weather_data.main.temp;
        let temp_p = document.getElementById('temp_' + id); 
        new_content = temp_p.innerText
            .replace(/{{temp}}/g, (parseInt(trip.temp * 10) / 10).toString())
        temp_p.innerText = new_content
    }
}

function fun_to_call_after_trip_table(){
    init_is_dest_visible()
    show_all()
    set_temp()
}

//This code is inspired from https://jqueryui.com/slider/#range
$("#slider-range").slider({
        range: true,
        min: 0,
        max: 1000,
        values: [ 0, 1000 ],
        slide: function( event, ui ) {
            $("#price_min").val( ui.values[ 0 ] + "€");
            $("#price_max").val( ui.values[ 1 ] + "€");
            hide_dest_filter()
        }
    }
);
//End of the code inspired


//Event managment
$("#price_min").keyup(
    function(){
        var p_min = $("#price_min").val();
        if (p_min == '€'){
            p_min = 0
        }
        else{
            p_min = parseInt(p_min)
        };
        var p_max = parseInt($("#price_max").val());
        if (p_min <= p_max){
            $("#slider-range").slider("values", [p_min, p_max]);
            $(this).val(p_min + '€')
        }
        else{
            $("#slider-range").slider("values", [p_max, p_max]);
            $(this).val(p_max + '€')
        };
        hide_dest_filter()
    }
)

$("#price_max").keyup(
    function(){
        var p_min = parseInt($("#price_min").val());
        var p_max = $("#price_max").val();
        if (p_max == '€'){
            p_max = 1000
        }
        else{
            p_max = parseInt(p_max)
        };
        if (p_min <= p_max){
            $("#slider-range").slider("values", [p_min, p_max])
            $(this).val(p_max + '€')
        }
        else{
            $("#slider-range").slider("values", [p_min, p_min])
            $(this).val(p_min + '€')
        };
        hide_dest_filter()
    }
)

//Main program
init_trip_table_then_call(fun_to_call_after_trip_table)

$("#price_min").val("0€");
$("#price_max").val("1000€");

//chargement du header et du footer
$('header').load("header.html")
$('footer').load("footer.html")