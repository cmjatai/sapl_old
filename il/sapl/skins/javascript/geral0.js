function getDomain() {
    return window.location.hostname.replace(/([a-zA-Z0-9]+.)/,"");
}

//document.domain = getDomain();

function reloadParentAndClose() {
    parent.jQuery.fancybox.close();
}

//Funcao para colar o footer no final da pagina.
function colaRodape(){
  var barraSuperiorHeight = $('.barraSuperior').outerHeight();
  var rodapeHeight = $('#rodape').outerHeight();
  var topoHeight = $('#topo').outerHeight();
  var conteudoPadding = parseFloat($('#conteudo').css('padding-top')) + parseFloat($('#conteudo').css('padding-bottom'));

  var conteudoHeight = $(window).height() - barraSuperiorHeight - rodapeHeight - topoHeight - conteudoPadding;
  $('#conteudo').css({'min-height': conteudoHeight + "px"});
}

//$(document).ready(colaRodape);
//$(window).on("resize",colaRodape);

//$(".pesquisa").click(function(){
//    $(this).toggleClass("ativo");
//});

function usuario_autenticar(){
    var form = document.lateral_form;

    if (form.__ac_name.value == "") {
        alert(" O nome do usu\u00e1rio deve ser preenchido!");
        form.__ac_name.focus();
        return;
    }

    if (form.__ac_password.value == "") {
       alert("A senha do usu\u00e1rio deve ser preenchida!");
       form.__ac_password.focus();
       return;
    }

    form.submit();
    return;
}

function palavra_chave_buscar() {
      var form = document.top_bar_form;

      if (form.txt_palavra_chave.value == "") {
         alert("A palavra-chave para busca deve ser preenchida!");
         form.txt_palavra_chave.focus();
         return false;
      }

      return true;

      /*-----
      location.href = "&dtml-portal_url;/generico/palavra_chave_buscar_proc?chave=" + form.txt_palavra_chave.value;
      -----*/
   }

function formata_data(campo){
    campo.value = filtra_campo(campo);
    vr = campo.value;
    tam = vr.length;

    if ( tam > 2 && tam < 5 )
        campo.value = vr.substr( 0, tam - 2  ) + '/' + vr.substr( tam - 2, tam );
    if ( tam >= 5 && tam <= 10 )
        campo.value = vr.substr( 0, 2 ) + '/' + vr.substr( 2, 2 ) + '/' + vr.substr( 4, 4 );
   }

function filtra_campo(campo){
    var s = "";
    var cp = "";
    vr = campo.value;
    tam = vr.length;
    for (i = 0; i < tam ; i++) {
        if (vr.substring(i,i + 1) != "/" && vr.substring(i,i + 1) != "-" && vr.substring(i,i + 1) != "."  && vr.substring(i,i + 1) != "," ){
            s = s + vr.substring(i,i + 1);}
    }
    campo.value = s;
    return cp = campo.value
   }


function changeUrl() {
    var redirect;
    redirect = document.getElementById('select-nav').value;
    document.location.href = redirect;
}







//customização   ======>>>>

var flagBack = false;

//window.onpopstate = function(e) {
	//location.href = e.currentTarget.document.URL;
	// window.history.back()
	//window.location.reload(true);,

	//if (flagBack) {
	//	flagBack = false;
	//	history.back();
	//	return;
	//}

	//window.location.reload();

	//location.href = document.referrer;
//};

var delayCampoBusca = -1;
var delayCampoBuscaMAX = 20;
var campoBuscaCenter = true;
var linkDomain = "";
var linkQuery = "";

var valueCampoBusca = '';
var flagGetPage = false;



    function colocaAjax(pos) {
    	jQuery(".ajax-"+pos).css('display', 'block');
    }

    function tiraAjax() {
    	jQuery(".ajax-Top").css('display', 'none');
    	jQuery(".ajax-Bottom").css('display', 'none');
    }


function openLink(link, pesquisa, func, recursive, pagina)  {

	if (recursive == undefined)
		recursive = true

    if (recursive)
		colocaAjax("Top");
    else
    	colocaAjax("Bottom");
	jQuery.get(link+"&func="+func+"&random="+Math.random(), function(data, event, event1) {
		tiraAjax();

		if (func == 1 ) {
			if (!flagGetPage) {
				flagGetPage = true;
                if (pagina > 1)
                    jQuery( "#conteudoBusca"+func+'-2' ).append( data );
                else {
                    jQuery( "#conteudoBusca"+func ).append( data );
                    jQuery( "#conteudoBusca"+func+'-2' ).html( '' );
                }
			}
			else
				jQuery( "#conteudoBusca"+func ).html( data );

			if (recursive)
				openLink(link, pesquisa, 2, recursive, pagina)
		}
		else if (func == 2) {
			//jQuery( "#campoBuscaInteligente" ).val(pesquisa.trim());

			if (!flagGetPage) {
				flagGetPage = true;
				jQuery( "#conteudoBusca"+func ).append( data );
			}
			else
				jQuery( "#conteudoBusca"+func ).html( data );

			if (recursive)
				openLink(link, pesquisa, 3, recursive, pagina)

		}
		else if (func == 3) {
			//jQuery( "#campoBuscaInteligente" ).val(pesquisa.trim());
			jQuery( "#conteudoBusca"+func ).html( data );
		}
		else if (func == 89) {
			delayCampoBusca = -1;
			jQuery( "#conteudoBusca2" ).html( data );
		}

		else if (func == 90) {
			delayCampoBusca = -1;
			//jQuery( "#campoBuscaInteligente" ).val(pesquisa.trim());
			jQuery( "#conteudoBusca2" ).html( data );
		}

        contextBgColor(link);
	});
}


function startCampoBusca()  {

	if (delayCampoBusca == -1 || delayCampoBusca++ < delayCampoBuscaMAX)
		return;
	delayCampoBusca = -1;


	//if (linkQuery.length > 0)

	//else
	//	window.history.pushState(null, null, '&dtml-portal_url;/1?history=1');


	var campoBusca =  jQuery( "#campoBuscaInteligente" );
	var page =  jQuery( "#page" );
	var step =  jQuery( "#step" );
	var printer =  jQuery( "#printer" );
	var cod_parlamentar =  jQuery( "#cod_parlamentar" );
	var tip_materia =  jQuery( "#tip_materia" );
	var mtnm =  jQuery( "#mtnm" );
	var mt_tramitando =  jQuery( "#mt_tramitando" );
	var mt_status =  jQuery( "#mt_status" );
	var nm_tip_norma =  jQuery( "#nm_tip_norma" );
	var autostart =  jQuery( "#autostart" );

	if (campoBusca.length < 1)
		return;

	campoBusca = campoBusca[0].value;

	SetCookie('campoBuscaInteligente',campoBusca,1);



	if (campoBuscaCenter) {
		jQuery( "#busca_new form fieldset" ).addClass("fieldBuscaLeft");
    	jQuery( "#topo #logo" ).remove();
		campoBuscaCenter = false;
	}
	linkQuery = "?pesquisa="+campoBusca
	+"&mtnm="+mtnm[0].value
	+"&page="+page[0].value
	+"&step="+step[0].value
	+"&printer="+printer[0].value
	+"&cod_parlamentar="+cod_parlamentar[0].value
	+"&tip_materia="+tip_materia[0].value
	+"&mt_tramitando="+mt_tramitando[0].value
	+"&mt_status="+mt_status[0].value
	+"&nm_tip_norma="+nm_tip_norma[0].value;

	if (autostart.length > 0)
		linkQuery += "&autostart="+autostart[0].value;

	// window.history.replaceState(null, null, '&dtml-portal_url;/1'+linkQuery);


	if (!flagGetPage)
		linkQuery += "&scroll=1";
	else {
		window.history.pushState(null, null, 'http://sapl.camarajatai.go.gov.br/sapl/1'+linkQuery+"&history=1");
		window.history.replaceState(null, null, 'http://sapl.camarajatai.go.gov.br/sapl/1'+linkQuery+"&history=1");
	}

	link = "http://sapl.camarajatai.go.gov.br/sapl/generico/busca_inteligente_proc"+linkQuery;

	if (flagGetPage)
		openLink(link, campoBusca, 1, true, +page[0].value);
	else
		openLink(link, campoBusca, 1, false, +page[0].value);

}

//cookies
function SetCookie(cookieName,cookieValue,nDays) {
	var today = new Date();
	var expire = new Date();
	if (nDays==null || nDays==0) nDays=1;
	expire.setTime(today.getTime() + 3600000*24*nDays);
	document.cookie = cookieName+"="+escape(cookieValue)
	+ ";expires="+expire.toGMTString();
}

function ReadCookie(cookieName) {
	var theCookie=" "+document.cookie;
	var ind=theCookie.indexOf(" "+cookieName+"=");
	if (ind==-1) ind=theCookie.indexOf(";"+cookieName+"=");
	if (ind==-1 || cookieName=="") return "";
	var ind1=theCookie.indexOf(";",ind+1);
	if (ind1==-1) ind1=theCookie.length;
	return unescape(theCookie.substring(ind+cookieName.length+2,ind1));
}


jQuery(function() {

    //colaRodape();

	jQuery( document ).scroll(function() {
		if (flagGetPage) {
			if ( (document.documentElement.clientHeight+jQuery( document ).scrollTop())*1.1 > jQuery( document ).height()) {


				var page =  parseInt("0"+jQuery( "#page" )[0].value);

				if (page < parseInt(jQuery( ".linkPageLast").attr('data'))) {
					jQuery( "#page" ).val(page+1);

					flagGetPage = false;
					delayCampoBusca = delayCampoBuscaMAX;
				}
			}

		}
	});



	var cb = jQuery( "#campoBuscaInteligente" ).ready(function(data) {

		var campoBusca =  jQuery( "#campoBuscaInteligente" );
		campoBusca = campoBusca[0].value;

		flagBack = true;
		var autostart =  jQuery( "#autostart" );
		if (autostart.length == 0 || autostart[0].value != 'on') {
			return;
		}
		flagGetPage = true;
		jQuery( "#busca_new form fieldset" ).addClass("fieldBuscaLeft");
		delayCampoBusca = delayCampoBuscaMAX;

	}).keyup( function(event) {


		if (!event.ctrlKey && event.keyCode == 13) {
			jQuery( "#autostart" ).val("on");
			jQuery( "#page" ).val(1);
			flagGetPage = true;
			jQuery( "#conteudo" ).html('');

            $('html, body').animate({
            	scrollTop: 0
            }, 0);

			delayCampoBusca = delayCampoBuscaMAX;
		}
		else if (!event.ctrlKey && (event.keyCode > 64 || event.keyCode == 8)) {
    		jQuery( "#page" ).val(1);
			flagGetPage = true;
			jQuery( "#conteudo" ).html('');
			jQuery( "#autostart" ).val("on");
			delayCampoBusca = 0;
		}
		else {
/*			if (event.target.value != valueCampoBusca) {
				valueCampoBusca = event.target.value
				jQuery( "#page" ).val(1);
				flagGetPage = true;
				jQuery( "#conteudo" ).html('');
				jQuery( "#autostart" ).val("on");
				delayCampoBusca = 0;
			}*/
		}
	});

    //var href = location.href
    //if (href.indexOf('ordem_dia_sessao_index_html') == -1)
    //    jQuery(cb).focus();

	setInterval(startCampoBusca, 500);


});
