$(document).ready(function() {

    $('div.vote-buttons img.vote-up').click(function() {

        var id = {{ thread.id }};
        var vote_type = 'up';

        if ($(this).hasClass('selected')) {
            var vote_action = 'recall-vote'
            $.post('/ajax/thread/vote', {id:id, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-up').removeAttr('src')
                        .attr('src', 'images/vote-up-off.png')
                        .removeClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        } else {

            var vote_action = 'vote'
            $.post('/ajax/thread/vote', {id:id, type:vote_type, action:vote_action}, function(response) {
                if (isInt(response)) {
                    $('img.vote-up').removeAttr('src')
                        .attr('src', 'images/vote-up-on.png')
                        .addClass('selected');
                    $('div.vote-tally span.num').html(response);
                }
            });
        }
    });
