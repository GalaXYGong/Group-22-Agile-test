let point = 0;
let countdownInterval = null;
let correct_answer = [];
let incorrect_answer = [];
let endGameCalled = false; // To ensure endGame is called only once
let timeLeft = 30;
let isPaused = false; // Initialize timeLeft outside the function for global access

function resetAnswer() {
    const submitButton = document.querySelector('input[id="submit_button"]');
    const descriptionBox = document.getElementById('respone_box');
    const next_questionButton = document.getElementById('next_question');
    const answer = document.getElementById('answer');
    const description = document.getElementById('description');
    const submit_container = document.getElementById('submit_container');

    submit_container.style.alignItems = 'center';
    submit_container.style.display = 'inline-block';
    descriptionBox.style.display = 'none';
    submitButton.style.display = 'flex';
    next_questionButton.style.color = 'initial';
    next_questionButton.style.border = 'none'; 
    answer.innerText = '';
    description.innerText = '';
    submitButton.style.marginTop = '30px';
    submitButton.style.textAlign = 'center';
    submitButton.style.alignItems = 'center';
}

function winstreak() {
    pauseCountdown();
    
    const container = document.getElementById('winstreak');
    const choices = document.getElementById('choices');
    const score_box = document.getElementsByClassName('score_container')[0];
    const question_text = document.getElementById('question_text');
    const banner_text = document.getElementsByClassName('banner_text_h1')[0];
    const banner = document.getElementsByClassName('banner')[0];
    const defaultContent = banner_text.innerHTML; // Store default text content

    banner_text.innerHTML = '3 in a Row!';
    banner_text.style.fontFamily = 'Bebas Neue';
    banner.style.backgroundColor = '#ee5b12';
    question_text.style.display = 'none';
    choices.style.display = 'none';
    score_box.style.display = 'none';
    container.style.display = 'flex';
    container.innerHTML += '<img id="winstreakImg" src="/static/questionPage/duck-winstreak.gif">'; 
    

    setTimeout(function() {
        question_text.style.display = '';
        choices.style.display = '';
        score_box.style.display = '';
        container.style.display = 'none';
        container.innerHTML = '';
        banner_text.innerHTML = defaultContent; // Reset text content
        banner.style.backgroundColor = ''; // Reset background color
        banner_text.style.fontFamily = '';
        resumeCountdown();
    }, 3000); // 3 seconds delay (3000 milliseconds)
}

function description(result) {
    const submitButton = document.querySelector('input[id="submit_button"]');
    const descriptionBox = document.getElementById('respone_box');
    const next_questionButton = document.getElementById('next_question');
    const answer = document.getElementById('answer');
    const description = document.getElementById('description');

    if (result) {
        descriptionBox.style.backgroundColor = '#D7FFB8';
        next_questionButton.style.color = 'green';
        descriptionBox.style.color = 'green';
        next_questionButton.style.border = '2px solid green'; 
        answer.innerText = 'correct';
        description.innerText = "  let's go";
        murloc_sound.play();
    } else {
        descriptionBox.style.backgroundColor = '#FFDFE0';
        next_questionButton.style.color = 'red';
        descriptionBox.style.color = 'red';
        next_questionButton.style.border = '2px solid red'; 
        answer.innerHTML = 'wrong';
        oof_sound.play();
    }
    descriptionBox.style.display = 'grid';
    descriptionBox.style.gridTemplateColumns = 'repeat(5, 1fr)';
    submitButton.style.display = 'none';
}

function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

function displayChoice(incorrect_list, answer) {
    const choice1 = document.getElementById('choice1');
    const choice2 = document.getElementById('choice2');
    const choice3 = document.getElementById('choice3');
    const choice4 = document.getElementById('choice4');

    const input1 = document.getElementById('value1');
    const input2 = document.getElementById('value2');
    const input3 = document.getElementById('value3');
    const input4 = document.getElementById('value4');

    let all_choice = [incorrect_list[0], incorrect_list[1], incorrect_list[2], answer];
    all_choice = shuffleArray(all_choice);

    [choice1, choice2, choice3, choice4].forEach((choice, i) => {
        choice.innerHTML = all_choice[i];
    });

    [input1, input2, input3, input4].forEach((input, i) => {
        input.value = all_choice[i];
    });
}

function endGame(win, score, number_of_question, win_streak, question_length) {
    if (endGameCalled) return; // Ensure endGame is called only once
    endGameCalled = true;

    const banner = document.getElementsByClassName('banner')[0];
    const submitButton = document.querySelector('input[id="submit_button"]');
    const descriptionBox = document.getElementById('respone_box');
    const score_box = document.getElementsByClassName('score_container')[0];
    const correct_wrong = document.getElementById('answer');
    const next_questionButton = document.getElementById('next_question');
    const description_text = document.getElementById('description');
    const question_text = document.getElementById('question_text');
    const form = document.getElementById("question_form");
    const choices_form = document.getElementById('choices');
    const respone = document.createElement('h2');
    const respone_des = document.createElement('h3');
    const ducky = document.createElement("img");
    const time_container = document.getElementById('time_container');

    if (win) {
        respone.innerHTML = 'lets go!';
        ducky.src = '/static/questionPage/duck_win.gif';
        respone_des.innerHTML = "You did it!";
    } else {
        respone.innerHTML = 'Do it again!';
        ducky.src = '/static/questionPage/angry-duck.gif';
        respone_des.innerHTML = "You're a failure in every sense of the word.";
    }
    ducky.id = 'ducky';
    respone.id = 'respone_end';
    if (time_container) {
        time_container.style.display = 'none';
    }
    

    const score_outerdiv = document.createElement('div');
    const score_innerdiv = document.createElement('div');
    const score_outerdiv_incorrect = document.createElement('div');
    const score_innerdiv_incorrect = document.createElement('div');
    const score_div = document.createElement('div');
    score_outerdiv.id = 'score_correct_outter';
    score_innerdiv.id = 'score_correct_inner';
    score_outerdiv_incorrect.id = 'score_incorrect_outter';
    score_innerdiv_incorrect.id = 'score_incorrect_inner';
    score_innerdiv.innerHTML = score;
    score_innerdiv_incorrect.innerHTML = number_of_question - score;
    score_outerdiv.appendChild(score_innerdiv);
    score_outerdiv_incorrect.appendChild(score_innerdiv_incorrect);
    score_div.appendChild(score_outerdiv);
    score_div.appendChild(score_outerdiv_incorrect);
    score_div.id = 'score_div';

    choices_form.append(ducky,respone, respone_des, score_div);
    form.style.display = 'none';
    question_text.style.display = 'none';
    description_text.style.display = 'none';
    next_questionButton.style.backgroundColor = 'rgb(88,204,2)';
    next_questionButton.style.border = '2px solid rgb(88,204,2)';
    next_questionButton.value = 'Home';
    next_questionButton.style.color = 'white';
    correct_wrong.innerHTML = 'lesson review';
    correct_wrong.style.color = 'rgb(229, 229, 229)';
    score_box.style.display = 'none';
    descriptionBox.style.display = 'grid';
    descriptionBox.style.gridTemplateColumns = 'repeat(5, 1fr)';
    descriptionBox.style.backgroundColor = 'transparent';
    descriptionBox.style.borderTop = 'rgb(229, 229, 229) 1px solid';
    banner.style.display = 'none';
    submitButton.style.display = 'none';

    if (win_streak == question_length) {
        const specialButton = document.getElementById('special');
        specialButton.style.display = 'inline-block';
        specialButton.addEventListener('click', function() {
            window.location.href = '/bonus2';
        });
    }

    next_questionButton.addEventListener('click', function() {
        
        window.location.href = '/';
    })

    clearInterval(countdownInterval); // Stop the countdown
}
//endless
function startCountdown(win,score,number_of_question,question_length) {
    timeLeft = 30; // Ensure timeLeft is initialized to 30 seconds
    const countdownElement = document.getElementById('time');

    countdownInterval = setInterval(function() {
        

        // if no countdown element is found, then stop the function
        if (!countdownElement) {
            clearInterval(countdownInterval);
            return;
        }
        countdownElement.style.width = `${timeLeft *25}px`;
        countdownElement.innerHTML = timeLeft;

        if (timeLeft > 0) {
            timeLeft--; // Decrease timeLeft by 1 second
        } else {
            clearInterval(countdownInterval);
            countdownElement.style.width = '0px'; // Set the width to 0
            console.log("score: ", score);
            console.log("number_of_question: ", number_of_question);
            
            endGame(win, score, number_of_question, 0, question_length);
        }
    }, 1000);
}
function pauseCountdown() {
    isPaused = true;
}

function resumeCountdown() {
    isPaused = false;
}

function Send(incorrect_questions, correct_questions, score) {
    // Convert the string into a list of integers
    incorrect_questions = incorrect_questions.map(Number);
    correct_questions = correct_questions.map(Number);

    fetch('/question/update_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            score: score,
            correct_questions: correct_questions,
            incorrect_questions: incorrect_questions,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        //alert('Result submitted successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

oof_sound = new Audio('/static/assets/oof.mp3');
murloc_sound = new Audio('/static/assets/murloc.mp3');
murloc_sound.preload = 'auto';
oof_sound.preload = 'auto';

document.addEventListener('DOMContentLoaded', function() {
    const winS = document.getElementById('winstreak');
    winS.style.display = 'none';

    const respone_box = document.getElementById('respone_box');
    const score = document.getElementById('score_number');
    const elementHtml = document.getElementById('to_JS').innerHTML;
    const full_object = JSON.parse(elementHtml);
    const number_of_question = full_object.length;
    let win_streak = 0;
    questionCount = 0;
    let index = 0;

    respone_box.style.display = 'none';

    const form = document.getElementById("question_form");
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission

        var selectedOption = document.querySelector('input[name="choice"]:checked');
        if (selectedOption) {
            console.log("Selected value: ", selectedOption.value);
            if (selectedOption.value === full_object[index - 1].correct) {
                console.log("Correct answer");
                timeLeft += 2; // Add 2 seconds if answer is correct
                point += 1;
                score.innerHTML = point;
                console.log(point);
                win_streak += 1;
                correct_answer.push(full_object[index - 1].id);
                description(true);
            } else {
                win_streak = 0;
                console.log("Wrong answer");
                incorrect_answer.push(full_object[index - 1].id);
                description(false);
            }
        } else {
            description(false);
            incorrect_answer.push(full_object[index - 1].id);
        }
    });

    function displayQuestion(question_list, index) {
        if (index >= question_list.length) {
            return alert('No more questions');
        }
        const questionElement = document.getElementById('question_text');
        questionElement.innerHTML = question_list[index].question;
    }

    displayQuestion(full_object, index);
    displayChoice(full_object[index].incorrect_list, full_object[index].correct);
    index++;
    
    const nextQuestionButton = document.getElementById('next_question');
    nextQuestionButton.addEventListener('click', function(event) {
        event.preventDefault();
        console.log(point);
        if (index < full_object.length) {
            if (win_streak === 3) {
                winstreak();
                timeLeft += 5;
                win_streak = 0;
            }
            displayQuestion(full_object, index);
            displayChoice(full_object[index].incorrect_list, full_object[index].correct);
            index++;
            document.getElementById("question_form").reset();
            resetAnswer();
        } else {
            const win = point >= number_of_question / 2;
            endGame(win, point, number_of_question, win_streak, full_object.length);
            Send(incorrect_answer, correct_answer, point);
        }
    });

    function startCountdown() {
        timeLeft = 30; // Ensure timeLeft is initialized to 30 seconds
        const countdownElement = document.getElementById('time');

        countdownInterval = setInterval(function() {
            if (!countdownElement) {
                clearInterval(countdownInterval);
                return;
            }
            countdownElement.style.width = `${timeLeft * 25}px`;
            countdownElement.innerHTML = timeLeft;

            if (timeLeft > 0 && !isPaused) {
                timeLeft--; // Decrease timeLeft by 1 second
            } 
            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
                countdownElement.style.width = '0px'; // Set the width to 0
                const win = point >= number_of_question / 2;
                endGame(win, point, number_of_question, 0, full_object.length);
                
            }
        }, 1000);
    }


    startCountdown();
});
