function _(el){
    document.getElementById(el);
}

function ajax_data(file_, el, send_data){
    var hr = new XMLHttpRequest();

    hr.open('POST', file_, true);
    hr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
    hr.onload = function(){
        if(this.status == 200) {
            console.log(this.responseText);
            _(el).innerHTML = hr.responseText
        }
    };

    hr.send(send_data);
}

function userprofile_page(){
    ajax_data('{%%}', 'pages', null);
}