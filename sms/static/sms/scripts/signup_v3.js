//Attach event listener to SMS request button
var smsBtn = document.getElementById("smsBtn");
smsBtn.addEventListener("click", requestSMS);
var registration_token = token_django + '';

//Request SMS event handler
function requestSMS()
{
    smsBtn.removeEventListener("click", requestSMS);
    smsBtn.classList.add("disabled");
    
    var priorErrorMsg = document.querySelectorAll('.smsErrorMsg');
    if (priorErrorMsg.length > 0)
        {
            for (var i=priorErrorMsg.length-1; i>-1; i--)
                {
                    priorErrorMsg[i].parentElement.removeChild(priorErrorMsg[i]);
                }
        }
    
    var password_length_error = false;
    var password_match_error = false;
    var password_numeric_error = false;
    
    //Check the password inputs
    if (for_signup_django)
        {
            var password1 = document.querySelector("#password1InputDiv input").value
            var password2 = document.querySelector("#password2InputDiv input").value

            if (password1.length<8)
                {
                    password_length_error = true;
                }

            if (password1!==password2)
                {
                    password_match_error = true;
                }

            if (/^\d+$/.test(password1))
                {
                    password_numeric_error = true;
                }
        }
    
    //Then output error messages or send SMS if no errors
    if (password_length_error)
        {
            document.getElementById("password1InputDiv").insertAdjacentHTML("afterend", "<div class='smsErrorMsg'>密码长度不能少于8个数字与字母的组合</div>");
        }
    
    if (password_match_error)
        {
            document.getElementById("password2InputDiv").insertAdjacentHTML("afterend", "<div class='smsErrorMsg'>您输入了两个不同密码。请再次确认密码。</div>");
        }
    
    if (password_numeric_error)
        {
            document.getElementById("password1InputDiv").insertAdjacentHTML("afterend", "<div class='smsErrorMsg'>密码不能全部是数字，需要至少一个字母。</div>");
        }
    
    if (!(password_length_error || password_match_error || password_numeric_error))
        {
            ajax_request_sms_verification_code(registration_token);
        }
    else
        {
            smsBtn.addEventListener("click", requestSMS);
            smsBtn.classList.remove("disabled");
        }
}

function ajax_request_sms_verification_code(registration_token)
{
    var ajax_url = "/ajax/request_sms/" + registration_token + '/';
    
    function getCookie(name) 
    {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') 
        {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) 
            {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) 
                {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    var csrftoken = getCookie('csrftoken');
    
    function csrfSafeMethod(method) 
    {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $.ajax({
        url: ajax_url,
        data: {},
        type: "POST",
        dataType : "text",
    })
    // Code to run if the request succeeds (is done);
    // The response is passed to the function
    .done(function(result){
        
        var countdown = 90;
        
        var myInterval = setInterval(function(){
            smsBtn.textContent = countdown;
            countdown--;
            if (countdown<0)
                {
                    clearInterval(myInterval);
                    smsBtn.textContent = "获取验证码";
                    smsBtn.addEventListener("click", requestSMS);
                    smsBtn.classList.remove("disabled");
                }
        }, 1000)
    })
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    .fail(function( xhr, status, errorThrown ) {
        smsBtn.addEventListener("click", requestSMS);
        smsBtn.classList.remove("disabled");
        alert("AJAX FAILED: 短信验证获取失败。请您再试一次，如需要帮助请与我们联系，谢谢。");
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    })
}