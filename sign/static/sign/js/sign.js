function sign_in_page(){
    let sign_in_form = document.createElement('form');
    sign_in_form.setAttribute('action', '/sign/signin/');
    sign_in_form.setAttribute('method', 'get');

    let sign_in_csrf_token = document.createElement('input');
    sign_in_csrf_token.setAttribute('type', 'hidden');
    sign_in_csrf_token.setAttribute('name', 'csrfmiddlewaretoken');
    sign_in_csrf_token.setAttribute('value', $('#csrf_token').val());

    sign_in_form.appendChild(sign_in_csrf_token);
    document.body.appendChild(sign_in_form);
    sign_in_form.submit();
}


function sign_in_process(){
    let form_info = $('#sign_in_form')[0];
    let input_tags = form_info.getElementsByTagName('input');
    for(let i=0; i<input_tags.length; i++){
        let tag_name = input_tags[i].name;
        let tag_value = input_tags[i].value;
        if((tag_name === 'sign_id' && tag_value === '') || (tag_name === 'sign_pw' && tag_value === '')){
            return alert("로그인 정보 미입력 됨");
        }
    }

    let form_data = new FormData(form_info);
    $.ajax({
        type        : 'POST',
        url         : '/sign/signin/',
        data        : form_data,
        contentType : false,
        processData : false,
        beforeSend  : function(){
            // $('#loading-bar').show();
        },
        success     : function (data) {
            if(data.result === 'SUCCESS'){
                alert("로그인 성공");
                window.location.href = '/main/';
            }else if(data.result === 'FAIL' && data.error_code === 'LOGIN_ID_NE'){
                alert("해당 계정 없음");
            }else if(data.result === 'FAIL' && data.error_code === 'LOGIN_PW_NE'){
                alert("비밀번호 불일치");
            }
        },
        complete    : function(){
            // $('#loading-bar').hide();
        },
        error       : function (error) {
            console.log("error", error);
        }
    });
}


function sign_up_process(){
    let form_info = $('#sign_up_form')[0];
    let input_tags = form_info.getElementsByTagName('input');
    for(let i=0; i<input_tags.length; i++){
        let tag_name = input_tags[i].name;
        let tag_value = input_tags[i].value;
        if((tag_name === 'sign_id' && tag_value === '')
            || (tag_name === 'sign_pw' && tag_value === '')
            || (tag_name === 'sign_pw_re' && tag_value === '')
            || (tag_name === 'nick_name' && tag_value === '')){
            return alert("회원가입 정보 미입력 됨");
        }
    }

    let sign_pw = $("#sign_pw").val();
    let sign_pw_re = $("#sign_pw_re").val();
    if(sign_pw !== sign_pw_re){
        return alert("비밀번호 정보가 불일치합니다.");
    }

    let form_data = new FormData(form_info);
    $.ajax({
        type        : 'POST',
        url         : '/sign/signup/',
        data        : form_data,
        contentType : false,
        processData : false,
        beforeSend  : function(){
            // $('#loading-bar').show();
        },
        success     : function (data) {
            if(data.result === 'SUCCESS'){
                alert("회원가입 성공");
                window.location.href = '/sign/signin/';
            }else if(data.result === 'FAIL' && data.error_code === 'DUPLE'){
                alert("ID 중복");
            }
        },
        complete    : function(){
            // $('#loading-bar').hide();
        },
        error       : function (error) {
            console.log("error", error);
        }
    });
}