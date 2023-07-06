//copyright 2023 DE PRETTO REMI

function test(){ 									// pour tester des trucs tout ça tout ça
	var x = document.getElementById("T1");
	x.setAttribute("src", "./cartes/As_coeur.png");
T1.style.display = 'inline';
T2.style.display = 'inline';
T3.style.display = 'inline';
T4.style.display = 'inline';
T5.style.display = 'inline';
J11.style.display = 'inline';
J12.style.display = 'inline';
J21.style.display = 'inline';
J22.style.display = 'inline';
J31.style.display = 'inline';
J32.style.display = 'inline';
J41.style.display = 'inline';
J42.style.display = 'inline';
J51.style.display = 'inline';
J52.style.display = 'inline';
J61.style.display = 'inline';
J62.style.display = 'inline';
J71.style.display = 'inline';
J72.style.display = 'inline';
J81.style.display = 'inline';
J82.style.display = 'inline';
	// J11C.style.display = 'none';
	// J12C.style.display = 'none';
	J21C.style.display = 'none';
	J22C.style.display = 'none';
	J31C.style.display = 'none';
	J32C.style.display = 'none';
	J41C.style.display = 'none';
	J42C.style.display = 'none';
	J51C.style.display = 'none';
	J52C.style.display = 'none';
	J61C.style.display = 'none';
	J62C.style.display = 'none';
	J71C.style.display = 'none';
	J72C.style.display = 'none';
	J81C.style.display = 'none';
	J82C.style.display = 'none';

}

function strtoarray(x){													//F° convertit str en array
		r=[]
		ri=''
		for (var i = 1; i < c.length; i++) {
		if (c[i]==' ')	{
			var newLength = r.push(ri)
			ri=''
		}
		else if (i==c.length-1){
			ri=ri+c[i]
			var newLength = r.push(ri)
		}
		else{ 
			ri=ri+c[i]
		}
		}return r
	}

function Admin(c){														//gestion des commandes administrateurs
	if (c=='start'){
	socket.send(JSON.stringify({"action":false, 'pseudo': false, "admin":"start"}))
	}
	else{
	socket.send(JSON.stringify({"action":false, 'pseudo': false, "admin":c}))
	}
}

function ok(){ 															//F° qui s'occupe des commandes 
	c=document.getElementById("commande").value;
	if(c[0]!='/'){window.alert('comande invalide'); return}
	c=strtoarray(c)
	console.log(c)
	// '/p' -> pour creer son pseudo
	if(c[0]=='p'){ //pt enlever les numéro pour les joueurs car balek
		a=true
		for (var i=0; i<Jinfo['JnP'].length; i++){
			if (Jinfo['JnP'][i]==c[1]){
				a=false
		} 
			// if (Jinfo['NNP'][i]==c[1]){
				// a=false
		// }
		} 
		if (a==true){
		Mpseudo=c[1];
		// NP=c[1]
	socket.send(JSON.stringify({"action":true,'pseudo': Mpseudo}))
	}
	else{window.alert('Erreur tu as rentré le même pseudo ou le même nombre qu un n autre joueur')}}
	
	// '/spec' pour déterminer qui spec de base personne
	else if (c[0]=='spec'){Vspec=c[1];console.log('Vspec=',Vspec)	
	}
	
	else if (c[0]=='a'){
		Admin(c[1])
	}
}

function Fmise(s){														//F° occupe des V des Raises
	if(s=='set'){
    mise = document.getElementById("montant").value;
	//console.log(mise>Jinfo['Hmise'])
	//console.log(mise>Jinfo['Hmise'])
	if (mise>Jinfo['Hmise']){
		if (mise<Jinfo[Mpseudo][0]){
			//console.log(info[2])
	document.getElementById("RaiseV").innerHTML=mise;
	info[2]=mise}}
	}
	if(s=='1/2'){
	info[2]=Jinfo['Pot']/2
	document.getElementById("RaiseV").innerHTML=info[2];
	}
	if(s=='2/3'){
	info[2]=Jinfo['Pot']*2/3
	document.getElementById("RaiseV").innerHTML=info[2];
	}
	if(s=='3/4'){
	info[2]=Jinfo['Pot']*3/4
	document.getElementById("RaiseV").innerHTML=info[2];
	}
	if(s=='Pot'){
	info[2]=Jinfo['Pot']
	document.getElementById("RaiseV").innerHTML=info[2];
	}
	if(s=='All'){
	A="A"
	info[2]=Jinfo[Mpseudo][0]+Jinfo[Mpseudo][4]
	document.getElementById("RaiseV").innerHTML=info[2];
	}
}

function Fold(){														// envoie Fold au serveur
	socket.send(JSON.stringify({'action': 'F'})) 			
}

function Check(){														// envoie Check au serveur
	console.log('console ???')
	console.log('Jinfo[C]=',Jinfo['C'],Jinfo['C']==true)
	if(Jinfo['C']==true){
		socket.send(JSON.stringify({'action': 'C'}))}
	//console.log('Jinfo[PR]=',Jinfo['PR'],Jinfo['PR']==Mpseudo)
	else if(Jinfo['PR']==Mpseudo){
		if (Jinfo['R']=='C') {socket.send(JSON.stringify({'action': 'C'}))}
		else {window.alert('Tu ne peux pas check car une mise a été faite')}}
	else {window.alert('Tu ne peux pas check car une mise a été faite')}
}

function Pay(){															// envoie Pay au serveur
	if (Jinfo['Hmise']!=0)socket.send(JSON.stringify({'action': 'P'}))
	else{window.alert("Tu ne peux pas pay car aucune mise a été faite")}
}

function Raise(){														// envoie Raise au serveur
	//console.log('info2',info[2])
	if (info[2]<=Jinfo[Mpseudo][0]+Jinfo[Mpseudo][4]){
	if(BBV=='BB'){socket.send(JSON.stringify({'action':'R', 'amount':info[2]*BB[Jinfo['niv']]}))}
	else{socket.send(JSON.stringify({'action':'R', 'amount':info[2]}))}}
	else{window.alert("Tu ne peux pas raise cette valeur car tu n'as plus d'agent")}
	//document.getElementById('MPlayer1').innerHTML=info[2]
}

function trunc(n){			//F° tronque les float à 3 chiffres après la virgule | float -> str prendre que 3 dès que virgule puis str -> float
	n=n.toString() // n undefined WTF
	// console.log("wesh",parseFloat("45f"))
	nc=''
	c=-1
	for (var i = 0;i<n.length;i++){
		if(n[i]=='.'){
			c=3;nc=nc+n[i]}
		else if(c==0){
			nc=parseFloat(nc)
			// console.log("nc=",nc,"c=",c)
			return nc}
		else{
			nc=nc+n[i]
			c=c-1}
	}
	return nc
}

function sleep(ms) {													//permet de retarder js (car s'execute avant la DE PAGE HTML)
  return new Promise(resolve => setTimeout(resolve, ms));
}

function BSF(){															//met l'ordre des joueurs en commençant par J1 étant localement le J
	var BS = Jinfo['JnP'].slice();
	for (var i = 0; i < Jinfo['JnP'].length; i++) { 
	if (Jinfo['JnP'][i]==Mpseudo){ return BS }
	else { 
	var newLength = BS.push(BS[0]); 
	var first = BS.shift();
	info[3]=info[3]+1}}
	return BS
}

function convert(){ 													//creer une liste qui lorsque l'on rentre le pseudo J sort id correspndant
	BS=BSF()
	cj=["J1","J2","J3","J4","J5","J6","J7","J8"]
	for (var i = 0; i < Jinfo['JnP'].length; i++) { 
		j=i-info[3]
	if(j<0){j=j+Jinfo['JnP'].length}
		jeq[Jinfo['JnP'][i]]=cj[j]
		//jeq[BS[i]]="J"+j.toString()	->	ancienne méthode pseudo + carte marchait mais pas reste	
		}
	return
}

function BBF(){
	if(BBV=='BB')	{BBV=1}
	else	{BBV='BB'}
	console.log('timer',Jinfo)
	refresh(Jinfo)
}


async function GButtons(){												//affiche ou cache les buttons si à toi de jouer ou pas
	// console.log('Taking a break...');
	// await sleep(2000);
	// console.log('Two seconds later, showing sleep in a loop...');
	//console.log(Jinfo['EAJ'])
	if (Jinfo['EAJ']==Mpseudo){
		Buttons.style.display='inline' ;
	}
	
	else {
		Buttons.style.display='none' ;
	}
}

function BOrdre(){
	window.alert("OOOOOOOOOOHHHHHH")
	cp=["Pseudo1","Pseudo2","Pseudo3","Pseudo4","Pseudo5","Pseudo6","Pseudo7","Pseudo8",]
	ct=["Tune1","Tune2","Tune3","Tune4","Tune5","Tune6","Tune7","Tune8",]
	cm=["MPlayer1","MPlayer2","MPlayer3","MPlayer4","MPlayer5","MPlayer6","MPlayer7","MPlayer8",]
	for (var i=0; i< info[3];i++){
		var newLength = cp.push(cp[0]); 
		var first = cp.shift()		
		var newLength = ct.push(ct[0]); 
		var first = ct.shift()		
		var newLength = cm.push(cm[0]); 
		var first = cm.shift()
		console.log(i,cp,cm,ct)
	}
}

async function boucletimer(){
	boucletimer=0
	while (boucletimer==0){
	await sleep(1000)
	timer()}
}

function timer(){
	console.log('niv=',niv,'Jinfoniv=',Jinfo['niv'])
	if (niv==Jinfo['niv']){
		cBB=cBB-1
		document.getElementById("nextLevelCountdown").innerHTML = cBB}
	else {
		if(Jinfo['niv']==0){cBB=420}
		else{cBB=cBB+420}
		document.getElementById("nextLevelCountdown").innerHTML = cBB
		niv=Jinfo['niv']}
	if(aEAJ==Jinfo['EAJ']){
		cEAJ=cEAJ-1
		document.getElementById("VcEAJ").innerHTML = cEAJ}
	else {
		cEAJ=30
		document.getElementById("VcEAJ").innerHTML = cEAJ
		aEAJ=Jinfo['EAJ']}
}

function specmod(){
	if (Jinfo[Mpseudo][1]=='F'){
	if (Vspec=='all'){
		for (var i = 0; i < Jinfo['JnF'].length; i++) { 
			if(Jinfo['JnF'][i]!=Mpseudo){
				x=jeq[Jinfo['JnF'][i]]+"1C"
				console.log(x)
				var x = document.getElementById(x);
				x.style.display = 'none';
				x=jeq[Jinfo['JnF'][i]]+"2C"
				console.log(x)
				var x = document.getElementById(x);
				x.style.display = 'none';}
			x=jeq[Jinfo['JnF'][i]]+"1"
			var x = document.getElementById(x);
			x.setAttribute("src", ceq[Jinfo[Jinfo['JnF'][i]][3][0]]);
			x.style.display = 'inline';
			x=jeq[Jinfo['JnF'][i]]+"2"
			var x = document.getElementById(x);
			x.setAttribute("src", ceq[Jinfo[Jinfo['JnF'][i]][3][1]]);
			x.style.display = 'inline';
		}			
	}
	else {	x=jeq[Vspec]+"1C"
				console.log(x)
				var x = document.getElementById(x);
				x.style.display = 'none';
				x=jeq[Vspec]+"2C"
				console.log(x)
				var x = document.getElementById(x);
				x.style.display = 'none';
			x=jeq[Vspec]+"1"
			var x = document.getElementById(x);
			x.setAttribute("src", ceq[Jinfo[Vspec][3][0]]);
			x.style.display = 'inline';
			x=jeq[Vspec]+"2"
			var x = document.getElementById(x);
			x.setAttribute("src", ceq[Jinfo[Vspec][3][1]]);
			x.style.display = 'inline';}}
}

async function reveal(){													//révèle les cartes selon l'indice Jinfo['R'] 
	if (Jinfo['R']=='3'){
		T1.setAttribute("src", ceq[Jinfo['ct'][0]]);		
		T2.setAttribute("src", ceq[Jinfo['ct'][1]]);	
		T3.setAttribute("src", ceq[Jinfo['ct'][2]]);
		T1.style.display = 'inline';
		T2.style.display = 'inline';
		T3.style.display = 'inline';
	}
	else if  (Jinfo['R']=='C'){
			J11.setAttribute("src", ceq[Jinfo[Mpseudo][3][0]]);
			J11.style.display = 'inline';
			J12.setAttribute("src", ceq[Jinfo[Mpseudo][3][1]]);
			J12.style.display = 'inline';
		
		for (var i = 0; i < Jinfo['JnF'].length; i++) { 
		if (Jinfo['JnF'][i]!=Mpseudo){
			x=jeq[Jinfo['JnF'][i]]+"1C"
			//console.log(x)
			var x = document.getElementById(x);
			x.setAttribute("src", "./cartes/dos.png" );
			x.style.display = 'inline';
			await sleep(333)
			x=jeq[Jinfo['JnF'][i]]+"2C"
			var x = document.getElementById(x);
			x.setAttribute("src", "./cartes/dos.png");
			x.style.display = 'inline';
			await sleep(333)}
	}specmod()}
	else if  (Jinfo['R']=='4'){specmod()
		T4.setAttribute("src", ceq[Jinfo['ct'][3]]);
		T4.style.display = 'inline';
	}
	else if (Jinfo['R']=='5'){specmod()
		T5.setAttribute("src", ceq[Jinfo['ct'][4]]);
		T5.style.display = 'inline';		
	}
	else if (Jinfo['R']=='J'){
		for (var i = 0; i < Jinfo['JnF'].length; i++) { 
			if(Jinfo['JnF'][i]!=Mpseudo){
				x=jeq[Jinfo['JnF'][i]]+"1C"
				console.log(x)
				var x = document.getElementById(x);
				x.style.display = 'none';
				x=jeq[Jinfo['JnF'][i]]+"2C"
				console.log(x)
				var x = document.getElementById(x);
				x.style.display = 'none';}
			x=jeq[Jinfo['JnF'][i]]+"1"
			var x = document.getElementById(x);
			x.setAttribute("src", ceq[Jinfo[Jinfo['JnF'][i]][3][0]]);
			x.style.display = 'inline';
			x=jeq[Jinfo['JnF'][i]]+"2"
			var x = document.getElementById(x);
			x.setAttribute("src", ceq[Jinfo[Jinfo['JnF'][i]][3][1]]);
			x.style.display = 'inline';
		}}
	else if(Jinfo['R']=='RST'){specmod()
		T1.style.display = 'none';
		T2.style.display = 'none';
		T3.style.display = 'none';
		T4.style.display = 'none';
		T5.style.display = 'none';
		for (var i = 0; i < Jinfo['JnF'].length; i++) { 
			x=jeq[Jinfo['JnF'][i]]+"1"
			console.log(x)
			var x = document.getElementById(x);
			x.style.display = 'none';
			x=jeq[Jinfo['JnF'][i]]+"2"
			console.log(x)
			var x = document.getElementById(x);
			x.style.display = 'none';}
	}
	for (var f = 0; f < Jinfo['JnP'].length; f++){
		if(Jinfo[Jinfo['JnP'][f]][1]=='F'){
			if (Jinfo['JnP'][f]!=Mpseudo){
			//console.log('Jinfo',Jinfo)
			//console.log('f',f)
			x=jeq[Jinfo['JnP'][f]]+"1"
			//console.log('x',x)
			var x = document.getElementById(x);
			x.style.display = 'none';
			x=jeq[Jinfo['JnP'][f]]+"2"
			//console.log('x',x)
			var x = document.getElementById(x);
			x.style.display = 'none';
			x=jeq[Jinfo['JnP'][f]]+"1C"
			//console.log('x',x)
			var x = document.getElementById(x);
			x.style.display = 'none';
			x=jeq[Jinfo['JnP'][f]]+"2C"
			//console.log('x',x)
			var x = document.getElementById(x);
			x.style.display = 'none';}}}
		
		}

function refresh(J){												// refresh toutes les infos dès que le serv les envoies
	console.log("J",J)
	if (J["type"]=="J"){ Jinfo=J
//		for( var w in J) {Jinfo[w]=J[w]}
	}
	if (lJ!=Jinfo['JnP'].length){lJ=Jinfo['JnP'].length;info[4]=false}   
	if (Jinfo['R']!='RST'){info[4]=false}
	//if (info[4]==false){BOrdre();info[4]=true}
	//console.log(info[4])
	GButtons()
	//if (info[4]==false){info[3]=0;convert()}
	if (J["P"]==true){
		info[3]=0
		convert();		
		for (var i=0;i<BS.length; i++){
			//console.log("punaise")
			document.getElementById(cp[i]).innerHTML = BS[i]};
		return}	
	//console.log(J["type"]=="J")
	s=0
	//console.log('Rémi:',Jinfo['Rémi'])
	console.log('avant',Jinfo)
		if(BBV=='BB'){	
		for (var i = 0; i < BS.length; i++) { 
			Jinfo[BS[i]][0]=trunc(Jinfo[BS[i]][0]/BB[Jinfo['niv']])
			Jinfo[BS[i]][2]=trunc(Jinfo[BS[i]][2]/BB[Jinfo['niv']])		
			Jinfo[BS[i]][4]=trunc(Jinfo[BS[i]][4]/BB[Jinfo['niv']])	}
		Jinfo['Pot']=trunc(Jinfo['Pot']/BB[Jinfo['niv']])
		Jinfo['Hmise']=trunc(Jinfo['Hmise']/BB[Jinfo['niv']])
		//console.log('Hmise',Jinfo['Hmise'])
	}
		else if (BBV==1){
		for (var i = 0; i < Jinfo['JnP'].length; i++) { 
			Jinfo[BS[i]][0]=trunc(Jinfo[BS[i]][0]*BB[Jinfo['niv']])
			Jinfo[BS[i]][2]=trunc(Jinfo[BS[i]][2]*BB[Jinfo['niv']])		
			Jinfo[BS[i]][4]=trunc(Jinfo[BS[i]][4]*BB[Jinfo['niv']])	}
		Jinfo['Pot']=trunc(Jinfo['Pot']*BB[Jinfo['niv']])
		Jinfo['Hmise']=trunc(Jinfo['Hmise']*BB[Jinfo['niv']])
		//console.log('Hmise',info['Hmise'])
		BBV=false
	}
	console.log('après',Jinfo)
	
	for (var i=0; i<BS.length; i++){
		//console.log(i)
		document.getElementById(ct[i]).innerHTML = Jinfo[BS[i]][0]
		document.getElementById(cm[i]).innerHTML = Jinfo[BS[i]][4]
		//console.log('EAJ',Jinfo['EAJ'],'JnPi',Jinfo['JnP'][i])
		if (BS[i]==Jinfo['EAJ']) {
				x=ccp[i]
				//console.log('x',x)
				var x = document.getElementById(x);
				x.style.color = 'red';}
//				x.style.color = rgb(220, 0, 0);}
		else if (Jinfo[BS[i]][0]<=0){
			if(Jinfo[BS[i]][5]<=0){
				x=ccp[i]
				//console.log('x',x)
				var x = document.getElementById(x);
				x.style.color = 'brown';}
			else{x=ccp[i]
				//console.log('x',x)
				var x = document.getElementById(x);
				x.style.color = 'blue';}}
		else {x=ccp[i]
				//console.log('x',x)
				var x = document.getElementById(x);
				x.style.color = 'blue';}
//				x.style.color = rgb(25, 25, 220);}
		for (var z=0; z<Jinfo['V'].length; z++){
			if (BS[i]==Jinfo['V'][z]){x=ccp[i]
				//console.log('x',x)
				var x = document.getElementById(x);
				x.style.color = 'green';}}
		if(Jinfo[BS[i]][2]!='D'){s=s+Jinfo[BS[i]][2]}
	}
		document.getElementById('VPOT').innerHTML = trunc(Jinfo['Pot']-s)
		document.getElementById('TVPOT').innerHTML = trunc(Jinfo['Pot'])
		document.getElementById('currentBlinds').innerHTML = BB[Jinfo['niv']-1]
		document.getElementById('nextBlinds').innerHTML = BB[Jinfo['niv']]
		if(Jinfo['Hmise']!=0){ if (Jinfo['Hmise']<Jinfo[Mpseudo][0]){document.getElementById('PayV').innerHTML=Jinfo['Hmise']-Jinfo[Mpseudo][4]}
								else {document.getElementById('PayV').innerHTML=Jinfo[Mpseudo][0]}}
		else{document.getElementById('PayV').innerHTML=''}
		info[2]=Jinfo['Hmise']+1
		if (info[2]<Jinfo[Mpseudo][0]){		document.getElementById('RaiseV').innerHTML=info[2]}
		else {document.getElementById('RaiseV').innerHTML=''}
		reveal()
}


// var html = document.forms["poker"];
var ip="ws://localhost:23614"

// ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
// ssl_context.load_verify_locations("")

var socket = null;
// Connexion vers un serveur HTTP
// prennant en charge le protocole WebSocket ("ws://").
socket = new WebSocket(ip);
socket.onerror = function(error) {
    console.error(error);						};

// Lorsque la connexion est établie.
socket.onopen = function(event) {
console.log("Connexion établie.");				};

    // Lorsque la connexion se termine.
socket.onclose = function(event) {
        console.log("Connexion terminé.");		};

    // Lorsque le serveur envoi un message.
socket.onmessage = function(event) {
console.log("Message:", JSON.parse(event.data), JSON.parse(event.data)["type"]); refresh(JSON.parse(event.data))}
		// Jinfo=event.data};



Jinfo={"Vadim": false, "niv":-1, "Hmise":20,"R":"","EAJ":"","JnF":[],"JnP":[], "Pot": 0, "ct": []}

//A FAIRE : mise et argent pour les bons J / Pay valeur -

BBV=false
info = [1500,30,20,0,false]  // info=[tune,pot,mise,nbr_try,ordre déjà fait]
ceq = ["./cartes/2_coeur.png","./cartes/3_coeur.png","./cartes/4_coeur.png","./cartes/5_coeur.png","./cartes/6_coeur.png","./cartes/7_coeur.png","./cartes/8_coeur.png","./cartes/9_coeur.png","./cartes/10_coeur.png","./cartes/J_coeur.png","./cartes/Q_coeur.png","./cartes/K_coeur.png","./cartes/As_coeur.png","./cartes/2_carreau.png","./cartes/3_carreau.png","./cartes/4_carreau.png","./cartes/5_carreau.png","./cartes/6_carreau.png","./cartes/7_carreau.png","./cartes/8_carreau.png","./cartes/9_carreau.png","./cartes/10_carreau.png","./cartes/J_carreau.png","./cartes/Q_carreau.png","./cartes/K_carreau.png","./cartes/As_carreau.png","./cartes/2_trefle.png","./cartes/3_trefle.png","./cartes/4_trefle.png","./cartes/5_trefle.png","./cartes/6_trefle.png","./cartes/7_trefle.png","./cartes/8_trefle.png","./cartes/9_trefle.png","./cartes/10_trefle.png","./cartes/J_trefle.png","./cartes/Q_trefle.png","./cartes/K_trefle.png","./cartes/As_trefle.png","./cartes/2_pic.png","./cartes/3_pic.png","./cartes/4_pic.png","./cartes/5_pic.png","./cartes/6_pic.png","./cartes/7_pic.png","./cartes/8_pic.png","./cartes/9_pic.png","./cartes/10_pic.png","./cartes/J_pic.png","./cartes/Q_pic.png","./cartes/K_pic.png","./cartes/As_pic.png"]
// Jinfo={"Vadim": false, "NNP":["1","3","4","5","6","7","8"], "niv":1, "Hmise":20,"R":"C","EAJ":"2","JnF":["1","2","3","4","5","6","7","8"],"JnP":["1","2","3","4","5","6","7","8"], "Pot": 0, "1": [1500, false, 20, [44, 37]], "2": [1500, false, 20, [8, 33]], "3": [1500, false, 20, [38, 21]], "ct": [40, 36, 9, 25, 30], "4": [1500, false, 20, [17, 16]], "5": [1500, false, 20, [20, 4]], "6": [1500, false, 20, [11, 3]], "7": [1500, false, 20, [41, 1]], "8": [1500, false, 20, [28, 7]]}
ccp=["Player1","Player2","Player3","Player4","Player5","Player6","Player7","Player8"]
cp=["Pseudo1","Pseudo2","Pseudo3","Pseudo4","Pseudo5","Pseudo6","Pseudo7","Pseudo8",]
ct=["Tune1","Tune2","Tune3","Tune4","Tune5","Tune6","Tune7","Tune8",]
cm=["MPlayer1","MPlayer2","MPlayer3","MPlayer4","MPlayer5","MPlayer6","MPlayer7","MPlayer8",]
BB=[20,30,40,60,80,100,140]
B=[10,15,20,30,40,50,70]
A='R'
BS=[]
// jeq=["J1","J2","J3","J4","J5","J6","J7","J8"]
jeq={}
Mpseudo=""
BS=[]
lJ=0
niv=-1
aEAJ=''
cEAJ=30
cBB=0
Vspec=''

boucletimer()

// BBV=='BB' mais pas bon V de raise  puis après si re BB alors one peut miser en dessous de la mise   OK
// problème check quand mise																			OK
// all in alors que pas assez d'argent																	OK
// change couleur de EAJ																				OK
// couleur marche mais pas bonne personne 																OK
//timer la fonction décompte le temps des J et BB avec 1 variable qui retient le dernier EAJ et dès que change reset le timer 


