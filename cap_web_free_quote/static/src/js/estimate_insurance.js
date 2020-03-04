odoo.define('cap_web_free_quote.estimate_insurance', function (require) {
    "use strict";
    var ajax = require('web.ajax');

    $(document).ready(function () {
        $('.thankyou_req_quote').on('click', function(){
            var gender = $('#gender').val();
            var state = $('#state').val();
            var smoke = $('#do_you_smoke').val();
            var policy_type = $('#policy_type:checked').val();
            var reference = $('#reference').val();
            var birth_date = $('#date_of_birth').val();
            var rate_your_health = $('#rating').val();

            if(!birth_date || !gender || !state || !smoke || !policy_type) {
                alert("Please fill below details");
                $('#date_of_birth').focus();
                return;
            }

            if(birth_date) {
                birth_date = birth_date.split("/");
                birth_date = birth_date[2].trim() + '-' + birth_date[0].trim() + '-' + birth_date[1].trim();
            }

            ajax.jsonRpc('/thankyou/request_quote', 'call', {
                'gender': gender.trim(),
                'quote_state': state.trim(),
                'smoke': smoke == "Yes" ? true : false,
                'policy_type': policy_type.trim(),
                'reference': reference,
                'date_of_birth': birth_date.trim(),
                'rate_your_health': rate_your_health
            }).then(function (data) {
                if(data['thank_you_request_quote']) {
                    $('#thankyou_quote_receive_error_msg').hide();
                    $('#thankyou_quote_receive_msg').show();
                } else {
                    $('#thankyou_quote_receive_msg').hide();
                    $('#thankyou_quote_receive_error_msg').show();
                }
            });
        });

        $('.question_radio').on('change', function() {
            var display_block = $(this).val() == 'Yes';
            var current_div = $(this).parent().parent();
            var next_visible = current_div.attr('data-next');
            if(next_visible > 0) {
                var current_next = current_div.next();
                for(var index = 0; index < next_visible; index++) {
                    if(display_block) {
                        current_next.prop('required', true);
                        current_next.css('display', 'block');
                    } else {
                        current_next.removeProp('required');
                        current_next.css('display', 'none');
                        current_next.val(current_next.defaultValue);
                    }
                    current_next = current_next.next();
                }
            }
//            current_div.closest("input[type='hidden']").val($(this).val());
        });

        //Star Rating Thankyou page
        var $star_rating = $('.star-rating .fa');
        var SetRatingStar = function() {
            return $star_rating.each(function() {
                if (parseInt($star_rating.siblings('#rating').val()) >= parseInt($(this).data('rating'))) {
                    return $(this).removeClass('fa-star-o').addClass('fa-star');
                } else {
                    return $(this).removeClass('fa-star').addClass('fa-star-o');
                }
            });
        };
        $star_rating.on('click', function() {
            $star_rating.siblings('#rating').val($(this).data('rating'));
            return SetRatingStar();
        });
        SetRatingStar();
    });
});
