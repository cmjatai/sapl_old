function getDomain() {
    return window.location.hostname.replace(/([a-zA-Z0-9]+.)/,"");
}

//document.domain = getDomain();

function reloadParentAndClose() {
    parent.jQuery.fancybox.close();
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
