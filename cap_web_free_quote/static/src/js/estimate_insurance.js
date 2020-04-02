odoo.define('cap_web_free_quote.estimate_insurance', function (require) {
    "use strict";
    var ajax = require('web.ajax');

    $(document).ready(function () {

        var face_amount = document.querySelector("#ixn-website-quoter > div > div > div > div:nth-child(3) > div:nth-child(1) > div > div:nth-child(7) > div:nth-child(2) > input[type=text]");
        var benefit = document.querySelector("#wrap > section > div > div.offset-lg-1.col-lg-5.col-xs-6 > div > div:nth-child(2) > div.thankyou_panel_1_total_btn > span");

        face_amount.value = benefit.innerText

        $('.thankyou_req_quote').on('click', function(){
            var requested_benefit = $('#requested_benefit').val();
            var gender = $('#gender').val();
            var state = $('#state').val();
            var smoke = $('#do_you_smoke').val();
            var policy_type = $('#policy_type:checked').val();
            var reference = $('#reference').val();
            var birth_date = $('#date_of_birth').val();
            var rate_your_health = $('#rating').val();

            if(!requested_benefit || !birth_date || !gender || !state || !smoke || !policy_type) {
                alert("Please fill the form");
                $('#requested_benefit').focus();
                return;
            }

            if(birth_date) {
                birth_date = birth_date.split("/");
                birth_date = birth_date[2].trim() + '-' + birth_date[0].trim() + '-' + birth_date[1].trim();
            }

            ajax.jsonRpc('/thankyou/request_quote', 'call', {
                'requested_benefit': requested_benefit,
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
            window.location.href = "/thank-you-page-life-calculator";
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

        $('.question_radio_no').on('change', function() {
            var display_block_no = $(this).val() == 'No';
            var current_div_no = $(this).parent().parent();
            var next_visible_no = current_div_no.attr('data-next');
            if(next_visible_no > 0) {
                var current_next_no = current_div_no.next();
                for(var index = 0; index < next_visible_no; index++) {
                    if(display_block_no) {
                        current_next_no.prop('required', true);
                        current_next_no.css('display', 'block');
                    } else {
                        current_next_no.removeProp('required');
                        current_next_no.css('display', 'none');
                        current_next_no.val(current_next_no.defaultValue);
                    }
                    current_next_no = current_next_no.next();
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
