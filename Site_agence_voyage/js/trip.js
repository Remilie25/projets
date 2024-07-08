// HEADER
// Description : Definition of the trip class
// Date : 15/11/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : finish trip class def

class Trip{
    constructor(dest, option_dictio, price_dictio, images_dictio, desc, is_city, longitude, latitude){
        this._dest = dest;
        this._option_dictio = option_dictio;
        this._price_dictio = price_dictio;
        this._img_dictio = images_dictio;
        this._desc = desc;
        this._is_city = is_city;
        this._longitude = longitude;
        this._latitude = latitude;
        this._temp
    }

    get dest(){ 
        return this._dest 
    }

    get option_dictio_keys(){
        return Object.keys(this._option_dictio)
    }

    option = function(key){
        return this._option_dictio[key]
    }

    get price_dictio_keys(){
        return Object.keys(this._price_dictio)
    }

    price = function(key){ 
        return this._price_dictio[key]
    }

    get images_dictio_keys(){
        return Object.keys(this._img_dictio)
    }

    image = function(key){ 
        return this._img_dictio[key][0]
    }

    image_alt = function(key){ 
        return this._img_dictio[key][1]
    }

    get desc(){
        return this._desc
    }

    get is_city(){
        return this._is_city
    }

    get longitude(){
        return this._longitude
    }

    get latitude(){
        return this._latitude
    }

    get temp(){
        return this._temp
    }

    set temp(new_temp){
        return this._temp = new_temp - 273.15
    }
}