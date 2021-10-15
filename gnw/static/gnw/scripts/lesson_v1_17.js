if (lesson_js_signal.toUpperCase()==="QUIZ")
{
    quiz();
}
else if (lesson_js_signal.toUpperCase()==="VIDEO")
{
    video();
}
else if (lesson_js_signal.toUpperCase()==="ASSIGNMENT")
{
    assignment();
}
else if (lesson_js_signal.toUpperCase()==="COURSE MENU")
{
    course_menu_setup();
}

function quiz()
{
    let answered_correctly = [];
    let student_answers = [];

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
        let includes_audio = false;

        if (old_quizBox_div !== null)
        {
            old_quizBox_div.remove();
        }

        let quizBox_div = document.createElement("div");
        quizBox_div.id = "quizBox";
        quizBox_div.classList.add("container-md", "mt-5"); //Bootstrap 4

        let current_question_number = index + 1;

        let HTML_str = `<div id="questionNumberIndicator" class="mb-3">`;
        HTML_str += `<span>(` + current_question_number + ` of ` + mc_questions.length + `)</span></div>`;
        //HTML_str += `<div class="question ml-5 pl-5 pt-2">`;
        HTML_str += `<div class="container-md question pt-2">`;

        if (question['media_file_type'].toUpperCase() !== "NONE" && question['media_file_name'] !== null)
        {
            if (question['media_file_type'].toUpperCase() === 'IMAGE')
            {
                let src = img_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="mb-3 container-md text-center"><img src="` + src + `" class="img-fluid"></div>`;
            }
            else if (question['media_file_type'].toUpperCase() === 'AUDIO')
            {
                includes_audio = true;
                let src = audio_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="mb-3 container-md embed-responsive text-center">
                                <audio src="` + src + `">Your browser does not support the <code>audio</code> element.</audio>
                                <div class="audio-player">
                                    <div class="audio-player-back-ring"></div>
                                    <div class="audio-player-back-ring-center"></div>
                                    <div class="audio-player-progress-ring">
                                        <div class="audio-player-progress-segment audio-player-progress-segment-1" style="display: none;"></div>
                                        <div class="audio-player-progress-segment audio-player-progress-segment-2" style="display: none;"></div>
                                        <div class="audio-player-progress-segment audio-player-progress-segment-3" style="display: none;"></div>
                                        <div class="audio-player-progress-segment audio-player-progress-segment-4" style="display: none;"></div>
                                        <div class="audio-player-progress-ring-center"></div>
                                    </div>
                                    <div class="audio-player-controls">
                                        <img src="` + img_url + `Audio-Play.svg" class="audio-player-button">
                                    </div>
                                </div>
                             </div>`;
            }
        }

        HTML_str += `<div id="questionTitle" class="h5">` + question['question_title'] + `</div>`;
        HTML_str += `<div id="options">`;
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
            HTML_str += `<div class="d-flex align-items-right pt-3"><div class="ml-auto mr-5"><button class="btn btn-success submit">` + button_text + `</button></div></div>`;
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

        if (includes_audio)
        {
            audio_player();
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
        quizBox_div.classList.add("container-md", "mt-5"); //Bootstrap 4

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
                <div class="ml-auto mr-5"> <button class="btn btn-success" id="reviewWrongAnswers">Review</button></div>
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
        let includes_audio = false;

        if (old_quizBox_div !== null)
        {
            old_quizBox_div.remove();
        }

        let quizBox_div = document.createElement("div");
        quizBox_div.id = "quizBox";
        quizBox_div.classList.add("container-md", "mt-5"); //Bootstrap 4

        let current_question_number = index + 1;

        let HTML_str = `<div id="questionNumberIndicator" class="mb-3">`;
        HTML_str += `<span>(` + current_question_number + ` of ` + mc_questions.length + `)</span></div>`;
        HTML_str += `<div class="container-md question pt-2">`;

        if (question['media_file_type'].toUpperCase() !== "NONE" && question['media_file_name'] !== null)
        {
            if (question['media_file_type'].toUpperCase() === 'IMAGE')
            {
                src = img_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="mb-3 container-md text-center"><img src="` + src + `" class="img-fluid"></div>`;
            }
            else if (question['media_file_type'].toUpperCase() === 'AUDIO')
            {
                includes_audio = true;
                let src = audio_url + question['media_file_name'];
                HTML_str += `<div id="mediaFileContainer" class="mb-3 container-md embed-responsive text-center">
                                <audio src="` + src + `">Your browser does not support the <code>audio</code> element.</audio>
                                <div class="audio-player">
                                    <div class="audio-player-back-ring"></div>
                                    <div class="audio-player-back-ring-center"></div>
                                    <div class="audio-player-progress-ring">
                                        <div class="audio-player-progress-segment audio-player-progress-segment-1" style="display: none;"></div>
                                        <div class="audio-player-progress-segment audio-player-progress-segment-2" style="display: none;"></div>
                                        <div class="audio-player-progress-segment audio-player-progress-segment-3" style="display: none;"></div>
                                        <div class="audio-player-progress-segment audio-player-progress-segment-4" style="display: none;"></div>
                                        <div class="audio-player-progress-ring-center"></div>
                                    </div>
                                    <div class="audio-player-controls">
                                        <img src="` + img_url + `Audio-Play.svg" class="audio-player-button">
                                    </div>
                                </div>
                             </div>`;
            }
        }

        HTML_str += `<div id="questionTitle" class="h5">` + question['question_title'] + `</div>`;
        HTML_str += `<div id="options">`;
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
            HTML_str += `<div class="d-flex align-items-right pt-3"><div class="ml-auto mr-5"><button class="btn btn-success submit">` + button_text + `</button></div></div>`;
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

        if (includes_audio)
        {
            audio_player();
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

        let instructions = {};
        instructions['get_csrftoken'] = true;

        let call_body = {};
        call_body['url'] = '/progress/ajax/record_completed_lesson/';

        let postdata = {};
        postdata['random_slug'] = lesson_id;
        postdata['results'] = data_string;

        call_body['data'] = postdata;
        call_body['type'] = 'POST';
        call_body['dataType'] = 'text';

        make_ajax_call(instructions, call_body);
    }
}

//=========================================================================================================
//=========================================================================================================
//========================================VIDEO============================================================
//=========================================================================================================
//=========================================================================================================

function video()
{
    let vid = document.querySelector("video");

    //When the video finishes, display button to go next
    //=========================================================
    vid.addEventListener("ended", show_next_button_and_call_api);
    function show_next_button_and_call_api()
    {
        let instructions = {};
        instructions['get_csrftoken'] = true;

        let call_body = {};
        call_body['url'] = '/progress/ajax/record_completed_lesson/';

        let postdata = {};
        postdata['random_slug'] = lesson_id;
        postdata['results'] = '';

        call_body['data'] = postdata;
        call_body['type'] = 'POST';
        call_body['dataType'] = 'text';

        make_ajax_call(instructions, call_body);
        
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
                for (let i=0; i<number_of_choices; i++)
                {
                    seconds = convert_hhmmss_to_seconds(video_questions[question]['start_times'][i]);
                    times.push(seconds);
                }
                jump_to_times_array.push(times);

                for (let j=0; j<number_of_choices; j++)
                {
                    seconds = convert_hhmmss_to_seconds(video_questions[question]['end_times'][j]); 

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

    function preload_images()
    {
        //Preload the in-video multiple choice option images ('A', 'B', 'C', 'D') and make them hidden.
        //Otherwise they'd have to be loaded at question time and possibly without having been cached,
        //and if they fail to load or load too slowly, it'll look very bad.
        //Not using <link 'rel=prefetch'> or similar approaches because cross-browser support is spotty.
        let choice_dict = {1:"A", 2:"B", 3:"C", 4:"D"};
        for (let i=1;i<=4;i++)
        {
            let img = document.createElement('img');
            img.setAttribute("src", img_url + "orange_letter_" + choice_dict[i] + ".svg");
            img.classList.add('preload_mc_image');
            document.body.appendChild(img);
        }
    }

    if (video_questions)
    {
        preload_images();
        set_up_question_data();
        vid.addEventListener("timeupdate", identify_action_times);
    }

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
        let seconds = (+hms[0]) * 60 + (+hms[1]);
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

//=========================================================================================================
//=========================================================================================================
//========================================ASSIGNMENT=======================================================
//=========================================================================================================
//=========================================================================================================

function assignment()
{
    if (assignment_details['assignment_type'].toUpperCase()==='PHOTO_UPLOAD')
    {
        if (assignment_submitted === false)
        {
            set_up_photo_upload_page();
        }
        else
        {
            if (submitted_assignment_details['graded']===true)
            {
                set_up_graded_photos_assignment_page();
            }
            else
            {
                set_up_photos_submitted_page();
            }
        }
    }

    function set_up_photo_upload_page()
    {
        let exercise_area_div = document.getElementById("exerciseArea");
        let old_uploadBox_div = document.getElementById("uploadBox");

        if (old_uploadBox_div !== null)
        {
            old_uploadBox_div.remove();
        }

        let uploadBox_div = document.createElement("div");
        uploadBox_div.id = "uploadBox";
        uploadBox_div.classList.add("container-md", "mt-5"); //Bootstrap 4

        HTML_str = `<div id="instructionsBox">
                <p>请完成上一节课的作业，然后拍照上传。</p>
                <p>最多可以上传<span style="color:red;padding-left:4px;padding-right:4px;">8</span>张照片。</p>
                <p>老师会在一周内批改作业，批改好的作业会上传到此页。</p>
            </div>`;
        HTML_str += `<input type="file" id="fileElem" multiple accept="image/*">`;
        HTML_str += `<div id="upload_buttons" class="d-flex justify-content-center mt-4 mb-3"><button class="btn btn-success choose-files">选择照片</button></div>`;
        uploadBox_div.insertAdjacentHTML("afterbegin", HTML_str);
        exercise_area_div.insertAdjacentElement("afterbegin", uploadBox_div);

        const image_picker_button = document.querySelector("button.choose-files");
        image_picker_button.addEventListener("click", choose_files);

        const inputElement = document.getElementById("fileElem");
        inputElement.addEventListener("change", validateFiles, false);
    }

    function choose_files()
    {
        const fileElem = document.getElementById("fileElem");
        if (fileElem)
        {
            fileElem.click();
        }
    }

    function validateFiles() 
    {
        const fileList = this.files; 
        let errors = [];
        let max_files_error = "最多只能上传 8 张照片";
        let min_file_error = "请至少选择一张照片上传";
        let file_size_error = "每张图片大小不能超过 10 MB";
        let file_type_error = "只支持以下几种图片格式：jpg, jpeg, png, gif";

        //Check the number of files: max = 8, min=1
        if (fileList.length > 8)
        {
            errors.push(max_files_error);
        }
        if (fileList.length <= 0)
        {
            errors.push(min_file_error);
        }
        
        //Check the size of each file: max = 10 mb per file
        //Check the file types
        const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
        for (let i=0; i<fileList.length; i++)
        {
            if (fileList[i].size > 10000000) 
            {
                errors.push(file_size_error);
            }   

            if (!validImageTypes.includes(fileList[i].type.toLowerCase()))
            {
                errors.push(file_type_error);
                break;
            }
        }

        if (errors.length > 0)
        {
            //If there are errors, uploading is disabled.
            let upload_button = document.querySelector("button.upload-files");
            if (upload_button)
            {
                upload_button.disabled = true;
            }

            let header = '操作错误';
            let body ='';

            for (let i=0; i<errors.length; i++)
            {
                body += `<p>` + errors[i] + `</p>`;
                if (i === errors.length - 1)
                {
                    body += `<p>请重新选择</p>`;
                }
            }

            show_modal_message(body, header);
        }
        else
        {
            show_thumbnails(fileList);
        }
    }

    function show_thumbnails(fileList)
    {
        let old_thumbnail_list = document.getElementById("thumbnailList");
        if (old_thumbnail_list !== null)
        {
            old_thumbnail_list.remove();
        }

        let thumbnail_div = document.createElement("div");
        thumbnail_div.id = "thumbnailList";
        document.getElementById("uploadBox").appendChild(thumbnail_div);

        for (let i = 0; i < fileList.length; i++) 
        {
            const image_frame = document.createElement("div");
            thumbnail_div.appendChild(image_frame);

            const img = document.createElement("img");
            img.classList.add("obj");
            img.file = fileList[i];
            img.src = URL.createObjectURL(fileList[i]);
            img.height = 100;

            img.onload = function() {
                URL.revokeObjectURL(this.src);
            }

            image_frame.appendChild(img);
        }

        const buttons_div = document.getElementById("upload_buttons");
        const image_picker_button = document.querySelector("button.choose-files");

        image_picker_button.textContent = "重新选择";
        image_picker_button.blur();

        let upload_button = document.querySelector("button.upload-files");
        
        if (upload_button === null)
        {
            let HTML_str = `<button class="btn btn-success upload-files">上传照片</button>`;
            buttons_div.insertAdjacentHTML("beforeend", HTML_str);
            const file_upload_button = document.querySelector("button.upload-files");

            file_upload_button.addEventListener("click", handle_upload_request);
        }
        else
        {
            upload_button.blur();
            upload_button.disabled = false;
        }
    }

    function handle_upload_request()
    {
        document.querySelector("button.choose-files").disabled = true;
        document.querySelector("button.upload-files").disabled = true;

        show_fake_progress_bar("文件上传中...");

        let files = document.getElementById("fileElem").files;

        let fd = new FormData();

        fd.append('lesson_uuid', lesson_id);
        fd.append('course_slug', course_slug);

        for (let i=0;i<files.length;i++)
        {
            fd.append('image'+(i+1), files[i])
        }

        let instructions = {};
        instructions['get_csrftoken'] = true;

        let call_body = {};
        call_body['type'] = 'post';
        call_body['data'] = fd;
        call_body['url'] = '/api/submit-photo-assignment/';
        call_body['contentType'] = false;
        call_body['processData'] = false;

        //Reload the page if upload successful
        function force_reload()
        {
            window.location.reload();
        }

        //Show error message in modal if upload fails
        function show_error(xhr, status, errorThrown) 
        {
            remove_fake_progress_bar();

            let header = '上传失败';
            let body = `<p>作业上传失败，请再试一次。</p>
                        <p>如果连续失败，请联系我们。</p>
                        <p>error: `+ xhr.status + ` (` + xhr.statusText +`)</p>`;

            show_modal_message(body, header);

            document.querySelector("button.choose-files").disabled = false;
            document.querySelector("button.upload-files").disabled = false;
        }

        make_ajax_call(instructions, call_body, force_reload, show_error);
    }

    function set_up_photos_submitted_page()
    {
        let exercise_area_div = document.getElementById("exerciseArea");
        let old_uploadBox_div = document.getElementById("uploadBox");

        if (old_uploadBox_div !== null)
        {
            old_uploadBox_div.remove();
        }

        let uploadBox_div = document.createElement("div");
        uploadBox_div.id = "uploadBox";
        uploadBox_div.classList.add("container-md", "mt-5"); //Bootstrap 4

        let submitted_datetime = submitted_assignment_details['submitted_time'];
        let yyyy = submitted_datetime.substring(0,4);
        let mm = submitted_datetime.substring(5,7);
        let dd = submitted_datetime.substring(8,10);
        let submit_date = yyyy + '年' + mm + '月' + dd + '日';

        HTML_str = `<div id="instructionsBox">
                <p>作业已上传。</p>
                <p>上传日期：<span style="color:red;padding-left:4px;padding-right:4px;">`+submit_date+`</span></p>
                <p>老师会在一周内批改作业，批改好的作业会上传到此页。</p>
            </div>`;
        
        uploadBox_div.insertAdjacentHTML("afterbegin", HTML_str);
        exercise_area_div.insertAdjacentElement("afterbegin", uploadBox_div);
        document.getElementById("nextButtonBox").classList.add("show");
    }

    function show_fake_progress_bar(label_str)
    {
        let old_progress_div = document.getElementById("fakeProgressBarDiv");
        if (old_progress_div !== null)
        {
            old_progress_div.remove();
        }

        let elem = document.createElement("div");
        elem.id = "fakeProgressBarDiv";
        elem.classList.add("container-md");
        let HTML_str = 
            `<div class="text-center" style="font-size:1.6rem;">`+label_str+`</div>
            <div class="progress">
                <div class="progress-bar progress-bar-striped bg-success" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width:0%"></div>
            </div>`;
        elem.insertAdjacentHTML("afterbegin", HTML_str);
        document.getElementById("instructionsBox").appendChild(elem);
    }

    function remove_fake_progress_bar()
    {
        let old_progress_div = document.getElementById("fakeProgressBarDiv");
        if (old_progress_div !== null)
        {
            old_progress_div.remove();
        }
    }

    function set_up_graded_photos_assignment_page()
    {
        let exercise_area_div = document.getElementById("exerciseArea");
        let old_uploadBox_div = document.getElementById("uploadBox");

        if (old_uploadBox_div !== null)
        {
            old_uploadBox_div.remove();
        }

        let uploadBox_div = document.createElement("div");
        uploadBox_div.id = "uploadBox";
        uploadBox_div.classList.add("container-md", "mt-5"); //Bootstrap 4

        HTML_str = `<div id="instructionsBox">
                <p style="color:red;">作业已批改。</p>
                <p>下列图片是批改后的作业，内有老师的批改和评语。</p>
                <p>请下载所有图片并仔细订正。</p>
            </div>`;
        
        uploadBox_div.insertAdjacentHTML("afterbegin", HTML_str);
        exercise_area_div.insertAdjacentElement("afterbegin", uploadBox_div);
        document.getElementById("nextButtonBox").classList.add("show");

        let thumbnail_div = document.createElement("div");
        thumbnail_div.id = "thumbnailList";
        document.getElementById("uploadBox").appendChild(thumbnail_div);

        let imageList = submitted_assignment_details['photos'];

        for (let i = 0; i < imageList.length; i++) 
        {
            const image_frame = document.createElement("div");
            thumbnail_div.appendChild(image_frame);

            const img = document.createElement("img");
            img.src = imageList[i];
            img.height = 100;

            image_frame.appendChild(img);
        }
    }
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


function make_ajax_call(instruction_dict, call_body_dict, done_callback=null, fail_callback=null)
{
    if ('get_csrftoken' in instruction_dict && instruction_dict['get_csrftoken']===true)
    {
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
    }

    /* Sample call body:
    {
        url: api_url,
        data: {random_slug: lesson_id, results: lesson_results},
        type: "POST",
        dataType : "text",
    }
    */

    //If no callbacks are passed in, use defaults.
    if (done_callback === null)
    {
        done_callback = successful;
    }

    if (fail_callback === null)
    {
        fail_callback = unsuccessful;
    }

    $.ajax(call_body_dict)
    .done(done_callback)
    .fail(fail_callback)

    function successful(response)
    {
        console.log(response);
    }

    function unsuccessful( xhr, status, errorThrown ) 
    {
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    }
    
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
}

function show_modal_message(bodyHTML, headerHTML='')
{
    let old_modalDiv = document.getElementById("genericModalDiv");
    if (old_modalDiv !== null)
    {
        old_modalDiv.remove();
    }

    let HTML_str = 
        `<div class="modal" id="genericModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">`+ headerHTML +`</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">`+ bodyHTML +`</div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">关闭</button>
                    </div>
                </div>
            </div>
        </div>`;

    let elem = document.createElement("div");
    elem.id = "genericModalDiv";
    elem.insertAdjacentHTML("afterbegin", HTML_str);
    document.body.appendChild(elem);
    
    $('#genericModal').modal('show'); //Bootstrap function
}