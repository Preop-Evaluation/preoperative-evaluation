$(document).ready(function(){
    $('.flag-toggle').click(function(){
         var button = $(this);
         var questionnaireId = button.data('questionnaire-id');
         var questionId = button.data('question-id');
         $.ajax({
              url: "/dashboard/anesthesiologist/toggle_flag", // URL defined in your toggle route
              method: 'POST',
              data: { questionnaire_id: questionnaireId, question_id: questionId },
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
