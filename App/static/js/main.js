$(document).ready(function(){
    $('.flag-toggle').click(function(){
        var button = $(this);
        var questionnaireId = button.data('questionnaire-id');
        var questionId = button.data('question-id');
        var userType = button.data('user-type'); 

        let endpoint = userType === 'doctor' ?
            "/dashboard/doctor/toggle_flag" :
            "/dashboard/anesthesiologist/toggle_flag";

        $.ajax({
            url: endpoint,
            method: 'POST',
            data: {
                questionnaire_id: questionnaireId,
                question_id: questionId
            },
            success: function(response){
                if(response.flagged){
                    button.removeClass('btn-warning').addClass('btn-danger');
                    button.text('Flagged');
                } else {
                    button.removeClass('btn-danger').addClass('btn-warning');
                    button.text('Flag');
                }
            },
            error: function(xhr, status, error){
                console.log("Error toggling flag: ", error);
            }
        });
    });
});

$(document).ready(function () {
    const approveRadio = document.getElementById('approve');
    const declineRadio = document.getElementById('decline');
    const dateField = document.getElementById('operationDate');

    if (approveRadio && declineRadio && dateField) {
        const toggleDateRequirement = () => {
            if (approveRadio.checked) {
                dateField.setAttribute('required', 'required');
            } else {
                dateField.removeAttribute('required');
            }
        };

        approveRadio.addEventListener('change', toggleDateRequirement);
        declineRadio.addEventListener('change', toggleDateRequirement);

        // Apply on load
        toggleDateRequirement();
    }
});
