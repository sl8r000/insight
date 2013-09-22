$(document).ready(function() {
    var handle_failure = function() {
        $('#ajax_loader').hide();
        $('#user').animate({backgroundColor: 'white'}, 'slow', function() {
            $('#user').css('border', '');
            $('#submit').show();
            $('.alert').show();
        });
    };

    var display_questions = function(data) {
        
        $('#ajax_loader').hide();
        $('#user').animate({backgroundColor: 'white'}, 'slow', function() {
            $('#user').css('border', '');
            $('#submit').show();
        });

        var recs = data.result;
        $.each(recs, function(index, elt) {
            var template = $('#template').clone();

            var match = Math.round(100*elt[1]);
            var glory = elt[0].view_count;
            var tags = elt[0].tags;
            var title = elt[0].title;
            var link = elt[0].link;

            var tag_spans = new Array();
            for (var i = 0; i < tags.length; i++) {
                tag_spans[i] = '<span class="label">' + tags[i] + '</span>';
            }
            var tag_row = tag_spans.join('');

            template.removeAttr('id');
            template.find('.glory').text(glory);
            template.find('.question-title').html(title);
            template.find('a').attr('href', link);
            template.find('.tag-target').html(tag_row);

            template.hide();
            if (index < 5) {
                $('#response_landing').append(template);
                template.delay(100*index).fadeIn(400);
            }
            else {
                template.find('a').css('backgroundColor', '#a65400');
                $('#filtered_results_landing').append(template);
                template.show();
            }
            $('#filtered_results').show();
        });
    };

    var submit_request = function() {
        $('.alert').hide();
        $('#filtered_results').hide();
        $('#response_landing').empty();
        $('#submit').hide();
        $('#user').css('border', '2px solid #e67e22');
        $("#ajax_loader").fadeIn();
        $('#user').animate({backgroundColor: '#e67e22'}, 'slow');
        $.get('/recommended/' + $('#user').val())
        .success(display_questions).error(handle_failure);
    };

    $(document).keypress(function(e) {
        if(e.which == 13) {
            submit_request();
        }
    });

    $('#submit').click(function() {
        submit_request();
    });

    $('#show-filtered').click(function() {
        $('#show-filtered').hide();
        $('#filtered_results_landing').show();
    });

    $('.easy-input').click(function() {
        var username = $(this).text();
        $('#user').val(username);
        submit_request();
    });
});