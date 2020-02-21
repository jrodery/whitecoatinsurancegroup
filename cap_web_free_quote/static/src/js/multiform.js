odoo.define('cap_web_free_quote.free_quote', function (require){
    "use strict";

    $(document).ready(function (){
        //jQuery time
        var current_fs, next_fs, previous_fs; //fieldsets
        var left, opacity, scale; //fieldset properties which we will animate
        var animating; //flag to prevent quick multi-click glitches

        $(".format-amount").focusout(function(){
            $(this).val(Number($(this).val()).toLocaleString('en-US'));
        });

        $(".format-email").focusout(function(){
            var email = $(this).val();
            var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            if(!regex.test(email)){
                $(this).focus();
                if(!$(this).hasClass('fill-required')){
                    $(this).addClass('fill-required');
                }
            } else {
                if($(this).hasClass('fill-required')){
                    $(this).removeClass('fill-required');
                }
            }
        });

        $('.format-phone').focusout(function(){
            $(this).val(
                $(this).val().replace(/(\d\d\d)(\d\d\d)(\d\d\d\d)/, '$1-$2-$3')
            );
        });

        $(".check_amount_format").focusout(function(){
            var str = $(this).val();
            if(!$.isNumeric(str)){
                $(this).focus();
                $(this).val('');
                $(this).attr('placeholder', 'Please follow this format. Ex.: 12345.11');
                $(this).addClass('fill-required');
            } else {
                if($(this).hasClass('fill-required')){
                    $(this).removeClass('fill-required');
                }
            }
        });

        $(".next").click(function(){
            var self = $(this);
            if(animating) return false;
            animating = true;
            var missed_required_input = false;
            current_fs = self.closest('fieldset');
            next_fs = self.closest('fieldset').next();
            current_fs.find('input').each(function(){
                if($(this).prop('required') && !$(this).val().trim()){
                    missed_required_input = true;
                    animating = false;
                    if(!$(this).hasClass('fill-required')){
                        $(this).addClass('fill-required');
                    }
                } else {
                    if($(this).hasClass('fill-required')){
                        $(this).removeClass('fill-required');
                    }
                }
            });
            if(!missed_required_input) {
                current_fs.find('textarea').each(function(){
                    if($(this).prop('required') && !$(this).val().trim()){
                        missed_required_input = true;
                        animating = false;
                        if(!$(this).hasClass('fill-required')){
                            $(this).addClass('fill-required');
                        }
                    } else {
                        if($(this).hasClass('fill-required')){
                            $(this).removeClass('fill-required');
                        }
                    }
                });
            }
            if(!missed_required_input) {
                current_fs.find('select').each(function(){
                    if($(this).prop('required') && !$(this).val().trim()){
                        missed_required_input = true;
                        animating = false;
                        if(!$(this).hasClass('fill-required')){
                            $(this).addClass('fill-required');
                        }
                    } else {
                        if($(this).hasClass('fill-required')){
                            $(this).removeClass('fill-required');
                        }
                    }
                });
            }
            if(!missed_required_input){
                //activate next step on progressbar using the index of next_fs
                $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                //show the next fieldset
                next_fs.show();
                //hide the current fieldset with style
                current_fs.animate({opacity: 0},{
                    step: function(now, mx){
                        //as the opacity of current_fs reduces to 0 - stored in "now"
                        //1. scale current_fs down to 80%
                        scale = 1 - (1 - now) * 0.2;
                        //2. bring next_fs from the right(50%)
                        left = (now * 50)+"%";
                        //3. increase opacity of next_fs to 1 as it moves in
                        opacity = 1 - now;
                        current_fs.css({
                            'transform': 'scale('+scale+')',
                            'position': 'absolute'
                          });
                        next_fs.css({'left': left, 'opacity': opacity});
                    },
                    duration: 800,
                    complete: function(){
                        current_fs.hide();
                        animating = false;
                    },
                    //this comes from the custom easing plugin
                    easing: 'easeInOutBack'
                });
                if(self.hasClass('show_total')) {
                    $('#msform').parent().next().css("display", "block");
                }
            }
        });

        $(".previous").click(function(){
            if(animating) return false;
            animating = true;

            current_fs = $(this).parent();
            previous_fs = $(this).closest('fieldset').prev();

            //de-activate current step on progressbar
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

            //show the previous fieldset
            previous_fs.show();
            //hide the current fieldset with style
            current_fs.animate({opacity: 0},{
                step: function(now, mx){
                    //as the opacity of current_fs reduces to 0 - stored in "now"
                    //1. scale previous_fs from 80% to 100%
                    scale = 0.8 + (1 - now) * 0.2;
                    //2. take current_fs to the right(50%) - from 0%
                    left = ((1-now) * 50)+"%";
                    //3. increase opacity of previous_fs to 1 as it moves in
                    opacity = 1 - now;
                    current_fs.css({'left': left});
                    previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity, 'position': 'relative'});
                },
                duration: 800,
                complete: function(){
                    current_fs.hide();
                    animating = false;
                },
                //this comes from the custom easing plugin
                easing: 'easeInOutBack'
            });
            if($(this).hasClass('hide_total')) {
                $('#msform').parent().next().css("display", "none")
            }
        });
    });
});
