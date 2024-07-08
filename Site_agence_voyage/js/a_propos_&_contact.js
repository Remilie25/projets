// HEADER
// Description : "A propos & contact" is a page that describes agency profile. Here the codes.
// Date : 09/10/23
// Authors : De Pretto Remi, Aussant Esteban
// TO DO : 



function create_email() {
    //no inputs, no outputs
    //call when click on button
    //create mail

    var adresseEmail = 'masuperagencedevoyage@example.com';
    var sujet = 'Demande de renseignements';
    var corps = document.getElementById('mail').value;

    var lienEmail = 'mailto:' + encodeURIComponent(adresseEmail) + '?subject=' + encodeURIComponent(sujet) + '&body=' + encodeURIComponent(corps);

    window.location.href = lienEmail;
    
    document.getElementById('mail').value = 'Bonjour, je souhaiterais obtenir des renseignements sur'
}

//chargement du header et du footer
$('header').load("header.html")
$('footer').load("footer.html")