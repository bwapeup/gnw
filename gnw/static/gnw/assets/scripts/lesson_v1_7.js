if (lesson_js_signal.toUpperCase()==="QUIZ")
{
    quiz();
}
else if (lesson_js_signal.toUpperCase()==="VIDEO")
{
    video();
}
else if (lesson_js_signal.toUpperCase()==="COURSE MENU")
{
    course_menu_setup();
}

function quiz()
{
    let mc_questions = [];
    let answered_correctly = [];
    let student_answers = [];

    for (question in quiz_questions)
    {
        mc_questions.push(quiz_questions[question]);
    }

    give_quiz.this_question_index = 0;
    function give_quiz()
    {
        if (mc_questions.length===0)
        {
            alert("No questions have been added to this quiz.");
            return;
        }

        let index = give_quiz.this_question_index;
        if (index < mc_questions.length)
        {
            if (mc_questions[index]['type_of_options'].toUpperCase()==='TEXT')
            {
                set_up_text_question(index);
            }
            else if (mc_questions[index]['type_of_options'].toUpperCase()==='IMAGE')
            {
                set_up_image_question(index);
            }
            else {
                alert("Unknown question type for multiple choice question.");
                return;
            }
        }
        else {
            show_results();
            prepare_data_for_api();
        }
    }

    give_quiz();

    function set_up_text_question(index, review=false)
    {
        let question = mc_questions[index];
        let exercise_area_div = document.getElementById("exerciseArea");
        let old_quizBox_div = document.getElementById("quizBox");

        if (old_quizBox_div !== null)
        {
            old_quizBox_div.remove();
        }

        let quizBox_div = document.createElement("div");
        quizBox_div.id = "quizBox";
        quizBox_div.classList.add("container", "mt-sm-5", "my-1"); //Bootstrap 4

        let current_question_number = index + 1;

        let HTML_str = `<div id="questionNumberIndicator" class="mb-3">`;
        HTML_str += `<span>(` + current_question_number + ` of ` + mc_questions.length + `)</span></div>`;
        HTML_str += `<div class="question ml-sm-5 pl-sm-5 pt-2">`;

        if (question['media_file_type'].toUpperCase() !== "NONE" && question['media_file_name'] !== null)
        {
            if (question['media_file_type'].toUpperCase() === 'IMAGE')
            {
                let src = img_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="my-5 container text-center"><img src="` + src + `" class="img-fluid"></div>`;
            }
            else if (question['media_file_type'].toUpperCase() === 'AUDIO')
            {
                let src = audio_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="my-5 container embed-responsive text-center"><audio src="` + src + `" autoplay controls>Your browser does not support the <code>audio</code> element.</audio></div>`;
            }
        }

        HTML_str += `<div id="questionTitle" class="py-2 h5">` + question['question_title'] + `</div>`;
        HTML_str += `<div class="ml-md-3 ml-sm-3 pl-md-5 pt-sm-0 pt-3" id="options">`;
        HTML_str += `<label class="options"><span id="textOption1" class="textOption">` + question['option_1'] + `</span><input type="radio" name="radio" data-option="1"><span class="checkmark"></span></label>`; 
        HTML_str += `<label class="options"><span id="textOption2" class="textOption">` + question['option_2'] + `</span><input type="radio" name="radio" data-option="2"><span class="checkmark"></span></label>`; 
        HTML_str += `<label class="options"><span id="textOption3" class="textOption">` + question['option_3'] + `</span><input type="radio" name="radio" data-option="3"><span class="checkmark"></span></label>`; 
        HTML_str += `<label class="options"><span id="textOption4" class="textOption">` + question['option_4'] + `</span><input type="radio" name="radio" data-option="4"><span class="checkmark"></span></label></div></div>`;
        
        let button_text = '';
        if (review)
        {
            button_text = "Next";
        }
        else {
            button_text = "Submit";
        }

        if (!review || (review && review_answers.last_question === false))
        {
            HTML_str += `<div class="d-flex align-items-right pt-3"><div class="ml-auto mr-sm-5"><button class="btn btn-success submit">` + button_text + `</button></div></div>`;
        }
        
        quizBox_div.insertAdjacentHTML("afterbegin", HTML_str);
        exercise_area_div.insertAdjacentElement("afterbegin", quizBox_div);

        let correct_choice = question['correct_choice'];

        if (review)
        {
            let student_answer = student_answers[index];
            document.querySelector("#textOption" + student_answer + "+input").checked = true;

            if (correct_choice !== parseInt(student_answer))
            {
                document.getElementById("textOption" + student_answer).classList.add("wrongAnswerLinethrough");
            }

            HTML_str = `<span class="check"></span>`;
            let correct_answer_span = document.getElementById("textOption" + correct_choice);
            correct_answer_span.insertAdjacentHTML("beforeend", HTML_str);
            correct_answer_span.classList.add("rightAnswerUnderline");

            if (review_answers.last_question)
            {
                document.getElementById("nextButtonBox").classList.add("show");
            }
            else {
                let submit_button = document.querySelector("button.submit");
                submit_button.addEventListener("click", review_answers);
            }
        }
        else {
            let correct_radio_input = document.querySelector("#textOption" + correct_choice + "+input");
            correct_radio_input.classList.add("correct");

            let submit_button = document.querySelector("button.submit");
            submit_button.addEventListener("click", submit_answer);
        }
    }

    function submit_answer()
    {
        let answered = false;

        if (mc_questions[give_quiz.this_question_index]['type_of_options'].toUpperCase()==='TEXT')
        {
            let radios = document.querySelectorAll(".options input");

            for (let i=0; i<radios.length; i++)
            {
                if (radios[i].checked)
                {
                    if (radios[i].classList.contains("correct"))
                    {
                        answered_correctly[give_quiz.this_question_index] = 1;
                    }
                    else{
                        answered_correctly[give_quiz.this_question_index] = 0;
                    }

                    student_answers[give_quiz.this_question_index] = radios[i].dataset.option;
                    answered = true;
                    break;
                }
            }
        }
        else if (mc_questions[give_quiz.this_question_index]['type_of_options'].toUpperCase()==='IMAGE')
        {
            let images = document.querySelectorAll(".imageOption");
            for(let i=0; i<images.length; i++)
            {
                if (images[i].classList.contains("selected"))
                {
                    if (images[i].classList.contains("correct"))
                    {
                        answered_correctly[give_quiz.this_question_index] = 1;
                    }
                    else{
                        answered_correctly[give_quiz.this_question_index] = 0;
                    }

                    student_answers[give_quiz.this_question_index] = images[i].dataset.option;
                    answered = true;
                    break;
                }
            }
        }
        

        if (answered)
        {
            give_quiz.this_question_index += 1;
            give_quiz();
        }
        else{
            let modalBox = document.getElementById("modalBoxForMissingAnswer");
            if (modalBox === null)
            {
                let HTML_str = `<div class="modal" id="needToSelectAnswerModal" tabindex="-1">
                        <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title"></h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>
                            <div class="modal-body">
                            <p>Please choose your answer.</p>
                            </div>
                            <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                        </div>
                    </div>`;
                
                let elem = document.createElement("div");
                elem.id = "modalBoxForMissingAnswer";
                elem.insertAdjacentHTML("afterbegin", HTML_str);
                document.body.appendChild(elem);
            }

            $('#needToSelectAnswerModal').modal('show'); //Bootstrap function
        }
    }

    function show_results()
    {
        let exercise_area_div = document.getElementById("exerciseArea");
        let old_quizBox_div = document.getElementById("quizBox");

        if (old_quizBox_div !== null)
        {
            old_quizBox_div.remove();
        }

        let quizBox_div = document.createElement("div");
        quizBox_div.id = "quizBox";
        quizBox_div.classList.add("container", "mt-sm-5", "my-1"); //Bootstrap 4

        let num_questions = mc_questions.length;
        let num_correct = answered_correctly.reduce((a,b)=>a+b, 0);
        let num_wrong = num_questions - num_correct;
        let percent_score = (Math.round(num_correct / num_questions * 100)) + '%';

        let HTML_str = `<div id="questionNumberIndicator"><span></span></div>`;
        HTML_str += `<div id="quizScoreTitle" class="py-2 h5">Your Score: <span id="yourScore">` + percent_score + `</span></div>`;
        HTML_str += `<table class="table table-bordered">
                    <tbody>`;
        HTML_str += `<tr>
                    <td>Total Questions</td>
                    <td>` + num_questions + `</td></tr>`;
        HTML_str += `<tr>
                    <td>Correct</td>
                    <td>` + num_correct + `</td></tr>`;
        HTML_str += `<tr>
                    <td>Wrong</td>
                    <td>` + num_wrong + `</td></tr>`;
        HTML_str += `<tr>
                    <td>Percentage</td>
                    <td>` + percent_score + `</td></tr>`;
        HTML_str += `</tbody>
                    </table>`;

        quizBox_div.insertAdjacentHTML("afterbegin", HTML_str);

        if (num_wrong > 0)
        {
            HTML_str = `<div class="d-flex align-items-right pt-3">
                <div class="ml-auto mr-sm-5"> <button class="btn btn-success" id="reviewWrongAnswers">Review</button></div>
                </div>`;
            quizBox_div.insertAdjacentHTML("beforeend", HTML_str);

            exercise_area_div.insertAdjacentElement("afterbegin", quizBox_div);
            let review_button = document.getElementById("reviewWrongAnswers");
            review_button.addEventListener("click", review_answers);
            review_answers.this_question_index = 0;
            review_answers.last_question = false;
        }
        else{
            exercise_area_div.insertAdjacentElement("afterbegin", quizBox_div);
            document.getElementById("nextButtonBox").classList.add("show");
        }
    }

    function review_answers()
    {
        let index = review_answers.this_question_index;
        if (index < mc_questions.length)
        {
            if (index === mc_questions.length - 1)
            {
                review_answers.last_question = true;
            }

            if (mc_questions[index]['type_of_options'].toUpperCase()==='TEXT')
            {
                set_up_text_question(index, true);
            }
            else if (mc_questions[index]['type_of_options'].toUpperCase()==='IMAGE')
            {
                set_up_image_question(index, true);
            }

            review_answers.this_question_index += 1;
        }
    }

    function set_up_image_question(index, review=false)
    {
        let src = '';
        let question = mc_questions[index];
        let exercise_area_div = document.getElementById("exerciseArea");
        let old_quizBox_div = document.getElementById("quizBox");

        if (old_quizBox_div !== null)
        {
            old_quizBox_div.remove();
        }

        let quizBox_div = document.createElement("div");
        quizBox_div.id = "quizBox";
        quizBox_div.classList.add("container", "mt-sm-5", "my-1"); //Bootstrap 4

        let current_question_number = index + 1;

        let HTML_str = `<div id="questionNumberIndicator" class="mb-3">`;
        HTML_str += `<span>(` + current_question_number + ` of ` + mc_questions.length + `)</span></div>`;
        HTML_str += `<div class="question ml-sm-5 pl-sm-5 pt-2">`;

        if (question['media_file_type'].toUpperCase() !== "NONE" && question['media_file_name'] !== null)
        {
            if (question['media_file_type'].toUpperCase() === 'IMAGE')
            {
                src = img_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="my-5 container text-center"><img src="` + src + `" class="img-fluid"></div>`;
            }
            else if (question['media_file_type'].toUpperCase() === 'AUDIO')
            {
                src = audio_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="my-5 container embed-responsive text-center"><audio src="` + src + `" autoplay controls>Your browser does not support the <code>audio</code> element.</audio></div>`;
            }
        }

        HTML_str += `<div id="questionTitle" class="py-2 h5">` + question['question_title'] + `</div>`;
        HTML_str += `<div class="ml-md-3 ml-sm-3 pl-md-5 pt-sm-0" id="options">`;
        HTML_str += `<div class="row w-75 my-5 justify-content-between"><div class="col-5 px-0 text-center imageOption position-relative" id="imageOption1" data-option="1"><img src="` + img_url + question['option_1'] + `" class="img-fluid mx-auto"></div><div class="col-5 px-0 text-center imageOption position-relative" id="imageOption2" data-option="2"><img src="` + img_url + question['option_2'] + `" class="img-fluid mx-auto"></div></div>`;
        HTML_str += `<div class="row w-75 my-5 justify-content-between"><div class="col-5 px-0 text-center imageOption position-relative" id="imageOption3" data-option="3"><img src="` + img_url + question['option_3'] + `" class="img-fluid mx-auto"></div><div class="col-5 px-0 text-center imageOption position-relative" id="imageOption4" data-option="4"><img src="` + img_url + question['option_4'] + `" class="img-fluid mx-auto"></div></div></div></div>`;
        
        let button_text = '';
        if (review)
        {
            button_text = "Next";
        }
        else {
            button_text = "Submit";
        }

        if (!review || (review && review_answers.last_question === false))
        {
            HTML_str += `<div class="d-flex align-items-right pt-3"><div class="ml-auto mr-sm-5"><button class="btn btn-success submit">` + button_text + `</button></div></div>`;
        }
        
        quizBox_div.insertAdjacentHTML("afterbegin", HTML_str);
        exercise_area_div.insertAdjacentElement("afterbegin", quizBox_div);

        let correct_choice = question['correct_choice'];

        if (review)
        {
            let student_answer = student_answers[index];
            let selected_div = document.getElementById("imageOption" + student_answer);

            if (correct_choice !== parseInt(student_answer))
            {
                selected_div.classList.add("wrongImageAnswer");
            }

            HTML_str = `<span class="check"></span>`;
            let correct_answer_div = document.getElementById("imageOption" + correct_choice);
            correct_answer_div.insertAdjacentHTML("beforeend", HTML_str);
            correct_answer_div.classList.add("rightImageAnswer");

            if (review_answers.last_question)
            {
                document.getElementById("nextButtonBox").classList.add("show");
            }
            else {
                let submit_button = document.querySelector("button.submit");
                submit_button.addEventListener("click", review_answers);
            }
        }
        else {
            let correct_image_div = document.getElementById("imageOption" + correct_choice);
            correct_image_div.classList.add("correct");

            let images = document.querySelectorAll(".imageOption img");
            for(let i=0;i<images.length;i++)
            {
                images[i].addEventListener("click", select_image_answer);
            }

            let submit_button = document.querySelector("button.submit");
            submit_button.addEventListener("click", submit_answer);
        }
    }

    function select_image_answer(e)
    {
        let image_selected = e.target;
        let image_div_selected = image_selected.parentElement;
        image_div_selected.classList.add("selected");

        let image_divs = document.querySelectorAll(".imageOption");
        for(let i=0;i<image_divs.length;i++)
        {
            if (image_divs[i] !== image_div_selected)
            {
                image_divs[i].classList.remove("selected");
            }
        }
    }

    function prepare_data_for_api()
    {
        //1. Total number of questions
        //2. Student score: correct/total
        //3. Student's wrong answers: (1). Question title: ... (2). Correct answer: Option 2-Text answer (image).
        //                            (3). Student's answer: Option 1-Text answer (image)
        let data_string = ``;
        data_string += `Total number of questions = ` + mc_questions.length + `. `;

        let num_correct = answered_correctly.reduce((a,b)=>a+b, 0);

        data_string += `Student's score = ` + num_correct + `/` + mc_questions.length + `. `;

        for (let i=0; i<answered_correctly.length; i++)
        {
            if (answered_correctly[i] === 0)
            {
                data_string += `{Wrong answer ` + (i+1) + `: `;
                data_string += `Question title = "` + mc_questions[i]['question_title'] + `"; `;
                data_string += `Correct choice = "` + mc_questions[i]['correct_choice'] + `"; `;
                data_string += `Student's choice = "` + student_answers[i] + `".} `;
            }
        }

        record_results_api(lesson_id, data_string);
    }
}

//=========================================================================================================
//=========================================================================================================
//========================================VIDEO============================================================
//=========================================================================================================
//=========================================================================================================

function video()
{
    var vid = document.querySelector("video");

    //When the video finishes, display button to go next
    //=========================================================
    vid.addEventListener("ended", show_next_button_and_call_api);
    function show_next_button_and_call_api()
    {
        let data_string = ``;
        record_results_api(lesson_id, data_string);
        
        document.getElementById("nextButtonBox").classList.add("show");
        vid.addEventListener("playing", runVideo);
    }

    //In case the video is being re-watched, the "next" button needs to disappear:
    //=========================================================
    vid.addEventListener("playing", runVideo);
    function runVideo()
    {
        document.getElementById("nextButtonBox").classList.remove("show");
        vid.removeEventListener("playing", runVideo);
    }

    //Set up in-video multiple-choice questions
    //=========================================================
    let action_times_array = [];
    let functions_array = [];
    let choices_array = [];
    let jump_to_times_array = [];
    let branching_bool_array = [];

    function set_up_question_data()
    {
        let times = [];
        let seconds = 0;
        let branching = false;
        let number_of_choices = 0;
        let correct_choice_number = 0;

        for (question in video_questions)
        {
            seconds = convert_hhmmss_to_seconds(video_questions[question]['pause_time']); 
            action_times_array.push(seconds); 

            functions_array.push(pauseTime);

            number_of_choices = video_questions[question]["number_of_choices"];
            correct_choice_number = video_questions[question]["correct_choice"];
            choices_array.push([number_of_choices, correct_choice_number]);
            
            branching = video_questions[question]['branching_video'];
            branching_bool_array.push(branching);

            if (branching)
            {
                times = [];
                for (let i=1; i<=number_of_choices; i++)
                {
                    seconds = convert_hhmmss_to_seconds(video_questions[question]['start_time_branch_' + i]);
                    times.push(seconds);
                }
                jump_to_times_array.push(times);

                for (let j=1; j<=number_of_choices; j++)
                {
                    seconds = convert_hhmmss_to_seconds(video_questions[question]['end_time_branch_' + j]); 

                    action_times_array.push(seconds);
                    functions_array.push(jumpTime);
                    choices_array.push(0);

                    seconds = convert_hhmmss_to_seconds(video_questions[question]['resume_time']);

                    jump_to_times_array.push(seconds);
                    branching_bool_array.push(0);
                }
            }
            else
            {
                seconds = convert_hhmmss_to_seconds(video_questions[question]['resume_time']);
                jump_to_times_array.push(seconds);
            }
            
        }
    }

    set_up_question_data();

    vid.addEventListener("timeupdate", identify_action_times);
    function identify_action_times()
    {
        if (!vid.paused) //If the user is just seeking, then it should not trigger function.
        {
            let action_time = Math.floor(vid.currentTime); 
            let call_time_milli = Date.now();
            //console.log(action_time);
            let index = action_times_array.indexOf(action_time);

            if (index > -1)
            {
                //timeupdate event fires multiple times per second
                //only the first one should be processed
                let call_function = true;
                if (functions_array[index].lastCall[0]===action_time) 
                {
                    if ((call_time_milli/1000 - functions_array[index].lastCall[1]) < 2)
                    {
                        call_function = false;
                    }
                }

                if (call_function)
                {
                    functions_array[index].lastCall = [action_time, call_time_milli/1000];
                    functions_array[index](index);
                }
            }
        }
    }

    //lastCall[0] = last action_time called, lastCall[1] = when this call happened
    //If the function was called for the same action_time within the last 2 seconds,
    //it should not be called again because it's just 'timeupdate' firing multiple events
    //within 1 second
    pauseTime.lastCall = [-1, -1.0]; 
    function pauseTime(index, option='click') //option: placeholder for other options like speech recognition
    {
        vid.pause();
        hide_controls();

        if (option.toUpperCase()==='CLICK')
        {
            set_up_click_options(index);
        }
        else if (option.toUpperCase()==='SPEECH')
        {
            //set_up_speech_recognition(index);
        }
        else
        {
            set_up_click_options(index);
        }
    }

    jumpTime.lastCall = [-1, -1.0];
    function jumpTime(index)
    {
        vid.currentTime = jump_to_times_array[index];
        vid.play();
    }

    function jump(event)
    {
        let selected_node = event.target;
        let index = parseInt(selected_node.dataset.index);
        if (selected_node.classList.contains("branching"))
        {
            let branch_start_time_index = parseInt(selected_node.dataset.branchingjumptoindex);
            vid.currentTime = jump_to_times_array[index][branch_start_time_index];
        }
        else
        {
            vid.currentTime = jump_to_times_array[index];
        }

        let choices_div = selected_node.parentElement;
        choices_div.remove();

        vid.play();
        show_controls();
    }

    function convert_hhmmss_to_seconds(hhmmss_str)
    {
        let hms = hhmmss_str.split(":");
        let seconds = (+hms[0]) * 60 * 60 + (+hms[1]) * 60 + (+hms[2]);
        return seconds;
    }

    function set_up_click_options(index)
    {
        //If the multiple chocies box already exists, it should be removed first.
        let choices_div = document.getElementById("choicesdiv");
        if (choices_div !== null)
        {
            choices_div.remove();
        }

        //Create the choices box
        choices_div = document.createElement("div");
        choices_div.id = "choicesdiv";

        choices_div.style.display = "flex";
        choices_div.style.alignItems = "center";
        choices_div.style.justifyContent = "space-around";
        choices_div.style.position = "absolute";
        choices_div.style.top = "50%";
        choices_div.style.left = "50%";
        choices_div.style.transform = "translate(-50%,-50%)";
        choices_div.style.width = "60rem";
        choices_div.style.height = "30rem";
        choices_div.style.zIndex = "2147483647";

        let video_box = document.getElementById("videoBox");
        video_box.appendChild(choices_div);

        let num_choices = choices_array[index][0];
        let correct_choice = choices_array[index][1];
        let branching_video = branching_bool_array[index];

        let choice_dict = {1:"A", 2:"B", 3:"C", 4:"D"};

        for (i=1;i<=num_choices;i++)
        {
            let elem = document.createElement("img");
            elem.setAttribute("data-index", index.toString()); //Need this to access resume_time

            if (branching_video)
            {
                elem.classList.add("branching");
                elem.setAttribute("data-branchingjumptoindex", (i-1).toString()); 
            }
            
            elem.style.width = "auto";
            elem.style.height = "25%";
            elem.style.backgroundColor = "white";
            elem.style.border = "2px solid orange";
            elem.style.borderRadius = "50%";
            elem.style.cursor = "pointer";
            elem.style.boxShadow = "5px 5px 5px 1px rgba(46, 61, 73, 0.6)";

            if (correct_choice === i)
            {
                elem.classList.add("correct");
            }

            elem.setAttribute("src", img_url + "orange_letter_" + choice_dict[i] + ".svg");
            
            elem.addEventListener("click", jump);
            choices_div.appendChild(elem);
        }
    }

    function hide_controls()
    {
        //"#video-controls" is in the HTML, as part of the code that creates the video player
        document.getElementById("video-controls").classList.add("hidden");
    }

    function show_controls()
    {
        //"#video-controls" is in the HTML, as part of the code that creates the video player
        document.getElementById("video-controls").classList.remove("hidden");
    }
}




function record_results_api(lesson_id, lesson_results='')
{
    let api_url = "/progress/ajax/record_completed_lesson/";
    
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
        url: api_url,
        data: {random_slug: lesson_id, results: lesson_results},
        type: "POST",
        dataType : "text",
    })
    // Code to run if the request succeeds (is done);
    // The response is passed to the function
    .done(function(response){
        console.log(response);
    })
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    .fail(function( xhr, status, errorThrown ) {
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    })
}


function course_menu_setup()
{
    let last_lesson_number = 0;
    let lesson_number = 0;

    let lesson_number_spans = document.querySelectorAll(".lesson-number");

    for (let i=0; i<lesson_number_spans.length; i++)
    {
        lesson_number = parseInt(lesson_number_spans[i].textContent);

        if (lesson_number < last_lesson_number)
        {
            lesson_number = last_lesson_number + 1;
        }

        last_lesson_number = lesson_number;

        if (lesson_number >= 10)
        {
            lesson_number_spans[i].textContent = lesson_number;
        }
        else 
        {
            lesson_number_spans[i].textContent = '0' + lesson_number;
        }
    }
}