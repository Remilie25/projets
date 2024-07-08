// HEADER
// Description : Definition of the trip_booking class
// Date : 6/12/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : 

class Trip_booking{
    constructor(id, from_date, to_date, number_adults, number_children, breakfast, pet, price){
        this._id = id
        this._from_date = from_date
        this._to_date = to_date
        this._number_adults = number_adults
        this._number_children = number_children
        this._breakfast = breakfast
        this._pet = pet
        this._price = price
    }

    get id(){
        return this._id
    }

    get from_date(){
        return this._from_date
    }

    get to_date(){
        return this._to_date
    }

    get number_adults(){
        return this._number_adults
    }

    get number_children(){
        return this._number_children
    }

    get breakfast(){
        return this._breakfast
    }

    get pet(){
        return this._pet
    }

    get price(){
        return this._price
    }
}