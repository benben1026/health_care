var signupCheck = {email:false, username:false, password:false, passwordMatch:false};
var loginInfo = {login: false, email:'', username:'', gender:'', age:''}
function checkLogin(){
    $.ajax({
        url: '/api/user',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            console.log(data);
            if(data["Err"] == "No session"){
                $('#nav-login').hide();
                $('#nav-notLogin').show();
                loginInfo.login = false;
            }else{
                $('#nav-login').show();
                $('#nav-notLogin').hide();
                loginInfo.login = true;
                loginInfo.email = data['email'];
                loginInfo.username = data['username'];
                loginInfo.gender = data['gender'];
                loginInfo.age = data['age'];
                $('#nav-username').text(loginInfo.username);
            }
        },
        error:function(){
            console.log('Error occurs when checking login info');
        }
    })
}
function login(email, password,rememberMe){
    $.ajax({
        url: '/api/session',
        type: 'POST',
        dataType: 'json',
        contentType:'application/json',
        data: JSON.stringify({email:email, password:password, permanent:rememberMe}),
        success:function(data){
            console.log(data);
            if(data['Err']){
                alert(data['Err']);
            }else{
                location.reload();
            }
        },
        error:function(){
            alert('login error!');
        }
    });
}

function signupCheckEmail(){
	var email = $('#signup-email').val().trim();
	var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
	if(!re.test(email)){
		signupCheck.email = false;
		$('.signup-email-check').hide();
		$('#signup-email-invalid').show();
		return;
	}
	$.ajax({
		url:'/api/user/' + email,
		type:'GET',
		dataType:'json',
		success:function(data){
			$('.signup-email-check').hide();
			if(!data['exist']){
				signupCheck.email = true;
				$('#signup-email-ok').show();
			}else{
				signupCheck.email = false;
				$('#signup-email-used').show();
			}
		}
	});
}

function signupCheckPassword(){
	$('.signup-checkPassword-check').hide();
	if($('#signup-password').val() == $('#signup-checkPassword').val()){
		signupCheck.passwordMatch = true;
		$('#signup-checkPassword-ok').show();
	}else{
		signupCheck.passwordMatch = false;
		$('#signup-checkPassword-notMatch').show();
	}
}

$(document).ready(function(){
    checkLogin();

    $("#myRegister").click(function(){
        $("#myModalRegister").modal();
    });
	$("#myLogin").click(function(){
        $("#myModalLogin").modal();
    });
    $('#signup-email').blur(signupCheckEmail);
    $('#signup-checkPassword').blur(signupCheckPassword);
    $('#signup-password').blur(function(){
    	$('.signup-password-check').hide();
    	if($('#signup-password').val() != ''){
    		signupCheck.password = true;
    		$('#signup-password-ok').show();
    	}else{
    		signupCheck.password = false;
    		$('#signup-password-empty').show();
    	}
    });
    $('#signup-username').blur(function(){
    	$('.signup-username-check').hide();
    	if($('#signup-username').val() != ''){
    		signupCheck.username = true;
    		$('#signup-username-ok').show();
    	}else{
    		signupCheck.username = false;
    		$('#signup-username-empty').show();
    	}
    });
    $('#signup-form').submit(function(event){
    	//alert('form submitted');
    	event.preventDefault();
    	//console.log(signupCheck);
    	//console.log($('#signup-email').val().trim() + $('#signup-password') + $('#signup-username'))
    	if(!signupCheck.email || !signupCheck.username || !signupCheck.password || !signupCheck.passwordMatch){
    		alert('Please check the form again.');
    		return;
    	}
    	$.ajax({
    		url: '/api/user',
    		type: 'POST',
    		dataType: 'json',
    		data:JSON.stringify({email:$('#signup-email').val().trim(), password:$('#signup-password').val(), username:$('#signup-username').val(), gender:$('input[name=gender]:checked', '#signup-form').val(), age:$('#signup-age').val()}),
    		contentType:'application/json',
    		success:function(data){
    			console.log(data);
    		},
    		error:function(){
    			alert('error');
    		},
            complete:function(){
                login($('#signup-email').val().trim(), $('#signup-password').val());
            }
    	});
    });

    $('#login-form').submit(function(event){
        event.preventDefault();
        login($('#login-email').val(), $('#login-password').val(), $('#login-rememberMe').is(':checked'));
    });
});