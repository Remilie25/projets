// HEADER
// Description : Definitions of functions to manage template related to destinations. Requires database.js to work (and trip.js by recursivity)
// Date : 09/10/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : finish the generalisation of the functions then testing

//Init of some var
is_dest_visible = []

//Functions

function add_dest(dest_id){//, template_id, dest_list_id){
    //Inputs : dest_id is the id of the dest that the function adds, template_id is the id of the template in the HTML and 
    //dest_list_id is the id of the list of dest in the HTML. 
    //No outputs. Change the document by adding the destination with data into "dest_list".

    if (!(is_dest_visible[dest_id])){
        let template = document.getElementById(template_id);
        let trip = trip_table[dest_id]
        let image_dest_key = trip.images_dictio_keys[0];

        let new_dest = document.importNode(template.content, true);
        new_dest_id = new_dest.firstElementChild.id
            .replace(/{{dest_id}}/g, dest_id);
        
        new_content = new_dest.firstElementChild.innerHTML
            .replace(/{{dest_id}}/g, dest_id)
            .replace(/{{image_dest}}/g, trip.image(image_dest_key))
            .replace(/{{image_desc}}/g, trip.image_alt(image_dest_key))
            .replace(/{{dest_name}}/g, trip.dest)
            .replace(/{{desc}}/g, trip.desc)
        
        new_dest.firstElementChild.innerHTML = new_content;
        new_dest.firstElementChild.id = new_dest_id;

        let dest_list = document.getElementById(dest_list_id);
        dest_list.appendChild(new_dest);
        is_dest_visible[dest_id] = true;
    }
    else{
        console.log("The destination with the id " + dest_id + " is already shown.")
    }
}

function del_dest(dest_id){
    //Inputs : dest_id is the id of the dest that the function erases and pop_up is a bool that indicates if the user has to confirm.
    //No outputs. Change the document by suppressing a destination of "dest_list"

    if (is_dest_visible){
        var dl = document.getElementById(dest_list_id);
        var dest = document.getElementById("dest_" + dest_id);   
        dl.removeChild(dest);
        is_dest_visible[dest_id] = false;
    }
    else{
        console.log("The destination with the id " + dest_id + " is already concealed.");
    }
}

function init_is_dest_visible(){
    //init all destination to false in is_dest_visible
    is_dest_visible = []
    for (i = 0; i < trip_table.length; i ++){
        is_dest_visible.push(false)
    }
}

function show_all(){
    for (let i = 0; i < trip_table.length; i ++){
        add_dest(i)
    }
}

function del_dest_pop_up(dest_id){
    if (window.confirm("Etes-vous vraiment sur de vouloir supprimer votre voyage ?")){
        del_dest(dest_id)
    }
}